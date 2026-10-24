"""Timeline record for a lesson: python tools/otio_build.py lessons/<id>  ->  build/<id>.otio

A video track of scenes and a voice track of takes, both from timing.json. It documents the
edit; the render itself is driven by Hyperframes.
"""
import json, os, sys
import opentimelineio as otio
lesson = os.path.abspath(sys.argv[1]); lid = os.path.basename(lesson); FPS = 30
T = json.load(open(os.path.join(lesson, 'timing.json'))); N = json.load(open(os.path.join(lesson, 'narration.json')))
rt = lambda s: otio.opentime.RationalTime(round(s * FPS), FPS)
rng = lambda a, d: otio.opentime.TimeRange(rt(a), rt(d))
tl = otio.schema.Timeline(name=f'AI from Scratch {lid}')
video = otio.schema.Track(name='Scenes', kind=otio.schema.TrackKind.Video)
voice = otio.schema.Track(name='Voice', kind=otio.schema.TrackKind.Audio)
ids = [s['id'] for s in N]
comp = otio.schema.ExternalReference(target_url='hf/index.html', available_range=rng(0, T['total']))
for k, i in enumerate(ids):
    end = T['starts'][ids[k + 1]] if k + 1 < len(ids) else T['total']
    video.append(otio.schema.Clip(name=i.upper(), media_reference=comp.clone(), source_range=rng(T['starts'][i], end - T['starts'][i])))
    gap = T['starts'][i] - (voice.duration().to_seconds() if len(voice) else 0)
    if gap > 1e-3: voice.append(otio.schema.Gap(source_range=rng(0, gap)))
    take = otio.schema.ExternalReference(target_url=f'audio/{i}.wav', available_range=rng(0, T['dur'][i]))
    voice.append(otio.schema.Clip(name=i, media_reference=take, source_range=rng(0, T['dur'][i]),
                                  metadata={'narration': N[k]['text'], 'speaker': N[k].get('speaker', 'priya')}))
tl.tracks.extend([video, voice])
os.makedirs(os.path.join(lesson, 'build'), exist_ok=True)
out = os.path.join(lesson, 'build', lid + '.otio'); otio.adapters.write_to_file(tl, out)
print(out, f'video {video.duration().to_seconds():.2f}s, voice {voice.duration().to_seconds():.2f}s')
