"""Generate per-scene narration with Gemini TTS through the Gemini API, then join the takes.

Auth: GEMINI_API_KEY (Google AI Studio key) in ../.env, via the Gemini API generateContent endpoint.

Usage:  python tts_gemini.py            # all scenes
        python tts_gemini.py s3 s4      # only these scene ids
Outputs audio_gemini/<id>.wav and timing_gemini.json (same shape as timing.json).
"""
import base64, json, os, subprocess, sys
import requests
from dotenv import load_dotenv

load_dotenv("../.env")
cfg = json.load(open("narration_gemini.json"))
os.makedirs("audio_gemini", exist_ok=True)

key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not key:
    sys.exit("No credentials: add GEMINI_API_KEY to ../.env")

# The Cloud TTS REST endpoint rejects API keys (401), so use the Gemini API directly.
url = f"https://generativelanguage.googleapis.com/v1beta/models/{cfg['model']}:generateContent"
wanted = set(sys.argv[1:])
for s in cfg["scenes"]:
    if wanted and s["id"] not in wanted:
        continue
    body = {
        "contents": [{"parts": [{"text": f"{cfg['global_prompt']} {s['style']}\n\nSay the following:\n{s['text']}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": cfg["voice"]}}},
        },
    }
    r = requests.post(url, headers={"x-goog-api-key": key, "Content-Type": "application/json"}, json=body, timeout=240)
    if r.status_code != 200:
        print(s["id"], r.status_code, r.text[:400])
        continue
    part = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]
    pcm = base64.b64decode(part["data"])  # 16-bit little-endian mono PCM, 24 kHz
    open(f"audio_gemini/{s['id']}.pcm", "wb").write(pcm)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
                           "-i", f"audio_gemini/{s['id']}.pcm", f"audio_gemini/{s['id']}.wav"])
    os.remove(f"audio_gemini/{s['id']}.pcm")
    print("ok", s["id"], part.get("mimeType"))

# ---- join takes: 0.45 s gaps, 1.5 s tail, same scheme as the Sarvam track ----
ids = [s["id"] for s in cfg["scenes"]]
if all(os.path.exists(f"audio_gemini/{i}.wav") for i in ids):
    dur = {i: float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"audio_gemini/{i}.wav"]).strip())
        for i in ids}
    gap, tail, t, starts, inputs, filt = 0.45, 1.5, 0.0, {}, [], []
    for k, i in enumerate(ids):
        starts[i] = round(t, 3)
        inputs += ["-i", f"audio_gemini/{i}.wav"]
        filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(t*1000)}[a{k}]")
        t += dur[i] + gap
    total = round(t - gap + tail, 2)
    mix = "".join(f"[a{k}]" for k in range(len(ids))) + f"amix=inputs={len(ids)}:normalize=0,apad=whole_dur={total}[o]"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt) + ";" + mix,
                           "-map", "[o]", "-t", str(total), "audio_gemini/voice_gemini.wav"])
    json.dump({"starts": starts, "dur": dur, "total": total}, open("timing_gemini.json", "w"), indent=1)
    print("joined -> audio_gemini/voice_gemini.wav, total", total, "s")
