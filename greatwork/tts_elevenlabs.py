"""ElevenLabs TTS (Eleven v4) with character-level timestamps -> scene timing for the video.

Reads  narration_eleven.json:
{
  "voice_id_env": "ELEVENT_LABS_VOICE_ID",      # name of the .env variable holding the voice id
  "api_key_env":  "ELEVEN_LABS_API_KEY",
  "model": "eleven_v4",
  "stability": 0.5, "similarity_boost": 0.75,    # the only two settings v4 exposes
  "mode": "whole",                               # "whole" = one call, "scene" = one call per scene
  "scene_gap": "\\n\\n",                          # text placed between scenes in whole mode
  "scenes": [ {"id": "s1", "text": "[warmly] ... "}, ... ]
}

Usage (run from the topic folder, e.g. upi/):
  python tts_elevenlabs.py --dry-run           # print plan and character count, spend nothing
  python tts_elevenlabs.py                     # generate everything
  python tts_elevenlabs.py --only s3 --mode scene   # regenerate one scene (scene mode)
  python tts_elevenlabs.py --stability 0.35 --out eleven_s35   # A/B another setting into another folder

Outputs in --out (default eleven/):
  voice.mp3          the narration
  alignment.json     per-character times for the exact text sent
  timing_eleven.json {"scenes": {id: {"start","end"}}, "sentences": [{"scene","start","end","text"}], "total"}
Scene start/end are the first and last spoken character of each scene's text.
"""
import argparse, base64, json, os, re, subprocess, sys
import requests
from dotenv import load_dotenv

ap = argparse.ArgumentParser()
ap.add_argument("--config", default="narration_eleven.json")
ap.add_argument("--out", default="eleven")
ap.add_argument("--mode")
ap.add_argument("--only", nargs="*")
ap.add_argument("--stability", type=float)
ap.add_argument("--similarity", type=float)
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

load_dotenv("../.env")
cfg = json.load(open(args.config))
mode = args.mode or cfg.get("mode", "whole")
stab = args.stability if args.stability is not None else cfg.get("stability", 0.5)
sim = args.similarity if args.similarity is not None else cfg.get("similarity_boost", 0.75)
gap = cfg.get("scene_gap", "\n\n").encode().decode("unicode_escape")
scenes = cfg["scenes"]
chars = sum(len(s["text"]) for s in scenes)
print(f"mode={mode} model={cfg['model']} stability={stab} similarity={sim} scenes={len(scenes)} characters~{chars}")
if args.dry_run:
    sys.exit(0)

key = os.environ.get(cfg.get("api_key_env", "ELEVEN_LABS_API_KEY")) or os.environ.get("ELEVENLABS_API_KEY")
voice = os.environ.get(cfg.get("voice_id_env", "ELEVENT_LABS_VOICE_ID")) or os.environ.get("ELEVENLABS_VOICE_ID")
if not key or not voice:
    sys.exit("Missing API key or voice id in ../.env")
os.makedirs(args.out, exist_ok=True)


def synth(text):
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps",
        params={"output_format": "mp3_44100_128"},
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        json={"text": text, "model_id": cfg["model"],
              "voice_settings": {"stability": stab, "similarity_boost": sim}},
        timeout=300)
    if r.status_code != 200:
        sys.exit(f"ElevenLabs error {r.status_code}: {r.text[:400]}")
    j = r.json()
    return base64.b64decode(j["audio_base64"]), j["alignment"]


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).strip())


def sentences(text, al, offset=0.0, base=0, scene=None):
    """Split on . ? ! boundaries inside the aligned text and return start/end of each sentence."""
    out, start_i = [], None
    ch = al["characters"]
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    n = len(text)
    i = 0
    while i < n:
        if start_i is None and not text[i].isspace() and text[i] not in "[]":
            # skip over a leading [tag]
            if text[i] == "[":
                i = text.index("]", i) + 1
                continue
            start_i = i
        if start_i is not None and text[i] in ".?!" and (i + 1 == n or text[i + 1].isspace()):
            seg = re.sub(r"\[[^\]]*\]", "", text[start_i:i + 1]).strip()
            out.append({"scene": scene, "start": round(offset + st[base + start_i], 2),
                        "end": round(offset + en[base + i], 2), "text": seg})
            start_i = None
        i += 1
    return out


timing = {"scenes": {}, "sentences": []}
if mode == "whole":
    full, spans = "", {}
    for k, s in enumerate(scenes):
        if k:
            full += gap
        # first spoken char = first char after any leading [tags] and whitespace
        lead = re.match(r"^(\s*\[[^\]]*\]\s*)*", s["text"]).end()
        spans[s["id"]] = (len(full), len(full) + len(s["text"]), len(full) + lead)
        full += s["text"]
    audio, al = synth(full)
    open(f"{args.out}/voice.mp3", "wb").write(audio)
    json.dump({"text": full, "alignment": al}, open(f"{args.out}/alignment.json", "w"))
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    for sid, (a, b, lead) in spans.items():
        timing["scenes"][sid] = {"start": round(st[lead], 2), "end": round(en[b - 1], 2)}
        timing["sentences"] += sentences(full[a:b], al, 0.0, a, sid)
    timing["total"] = round(dur(f"{args.out}/voice.mp3"), 2)
else:
    parts, t = [], 0.0
    for s in scenes:
        path = f"{args.out}/{s['id']}.mp3"
        if args.only and s["id"] not in args.only and os.path.exists(path):
            al = json.load(open(f"{args.out}/{s['id']}.alignment.json"))
        else:
            audio, al = synth(s["text"])
            open(path, "wb").write(audio)
            json.dump(al, open(f"{args.out}/{s['id']}.alignment.json", "w"))
        d = dur(path)
        lead = re.match(r"^(\s*\[[^\]]*\]\s*)*", s["text"]).end()
        timing["scenes"][s["id"]] = {"start": round(t + al["character_start_times_seconds"][lead], 2),
                                     "end": round(t + al["character_end_times_seconds"][-1], 2)}
        timing["sentences"] += sentences(s["text"], al, t, 0, s["id"])
        parts.append((path, t)); t += d + 0.45
    inputs, filt = [], []
    for k, (p, start) in enumerate(parts):
        inputs += ["-i", p]
        filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(start*1000)}[a{k}]")
    total = round(t - 0.45 + 1.5, 2)
    mix = "".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}[o]"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt) + ";" + mix,
                           "-map", "[o]", "-t", str(total), f"{args.out}/voice.mp3"])
    timing["total"] = total

json.dump(timing, open(f"{args.out}/timing_eleven.json", "w"), indent=1)
print(json.dumps(timing["scenes"], indent=1)); print("total", timing["total"])
