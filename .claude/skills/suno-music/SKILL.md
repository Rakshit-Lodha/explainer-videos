---
name: suno-music
description: Generate an instrumental background track on suno.com by driving the user's logged-in Chrome session, download it, then trim, fade and duck it under the voiceover with ffmpeg. Use when a video needs music from the user's Suno subscription.
---

# Suno music skill

Suno has no public API, so this runs through the Claude-in-Chrome tools against the user's signed-in session. The user has authorised using their subscription and downloading the result for this workflow; credits and download quota are spent, so generate once and pick from the two candidates Suno returns rather than re-rolling.

## Load the browser tools first
Load the Chrome tools in one `ToolSearch` call (`tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `computer`, `tabs_close_mcp`), then call `tabs_context_mcp` before anything else. Never reuse tab ids from an earlier session. Close the tab when finished.

## Steps
1. Navigate to `https://suno.com/create`. Wait a few seconds; `computer` fails with "browser-internal URL" until the page has loaded, so call `tabs_context_mcp` and retry.
2. Confirm the user is signed in (left sidebar shows their account). If a login or CAPTCHA appears, stop and ask the user to complete it; never enter credentials.
3. Use **Advanced** mode. Leave **Lyrics empty**: the placeholder says an empty box means instrumental.
4. Scroll the left panel and click into **Styles**. Type a style prompt. The one that worked:
   `instrumental, ambient electronic, soft warm pads, gentle pulsing arpeggio, subtle lo-fi texture, calm curious modern explainer underscore, no drums, no vocals, slow build, 90 seconds`
   Adapt the mood to the topic, keep "instrumental", "no vocals", and avoid strong drums so the voice stays clear.
5. Click **Create**. Two candidates appear within roughly a minute. Suno ignores the requested length; tracks came back at about 3 minutes 20 seconds, which is fine because the track is trimmed later.
6. Open the `...` menu on a candidate, choose **Download**. A dialog lists M4A, MP3, WAV, MP4 and stems. **M4A downloaded reliably; MP3 stayed on "Preparing..." for a long time.** Pick M4A unless the user asks otherwise, then click **Unlock & Download**. This uses one download from the plan quota, shown in the dialog.
7. The file lands in `~/Downloads/<title>.m4a` (wait up to about 30 s). Verify with `ls -lat ~/Downloads | head`. Copy it to `<topic>/music/`.
8. Close the dialog and close the tab.

## Process the track (ffmpeg)
Trim to the video length, fade, lower the level, and duck under the voice with a sidechain compressor. `asplit` is unnecessary: feed the voice into the compressor once or ffmpeg errors with "output unconnected".

```
ffmpeg -y -i music/track.m4a -i hf/assets/voice.wav -filter_complex \
"[0:a]atrim=0:TOTAL,asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,volume=0.55,afade=t=in:d=2.5,afade=t=out:st=TOTAL-4:d=4[m];\
[1:a]aformat=channel_layouts=stereo[sc];\
[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=40:release=500[d];\
[d]alimiter=limit=0.9[o]" -map "[o]" -t TOTAL hf/assets/music.wav
```

Replace `TOTAL` with the value in `timing.json`. In the composition the music `<audio>` uses `data-volume="1"` because the level and fades are already baked in. Until the track exists, use a silent placeholder (`ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t TOTAL music.wav`) so the composition checks pass.

## Done when
Mean level of the music bed is well below the voice (it was about -29 dB against a voice near -20 dB), and the final mix is loudness-normalised in the last ffmpeg pass. If the user asks for a different mood, repeat from step 3; if the browser actions fail two or three times, stop and report instead of looping.
