"""Build timing.json (and hf/assets/voice.wav when takes exist), then sync the composition.

python tools/voice.py <lesson_dir>
With audio/<id>.wav for every scene: measures takes, concatenates them with a 0.45 s gap and
1.5 s tail, writes hf/assets/voice.wav and timing.json. Without takes: estimates durations from
word count at Ratan's measured rate and marks timing.json provisional, so the animatic can be
built before the voice exists.
"""
import json, os, subprocess, sys, re, shutil
GAP, TAIL, WPS = 0.45, 1.5, 3.36   # 286 words came to 85 s at Ratan's tuned pace
lesson = os.path.abspath(sys.argv[1])
N = json.load(open(os.path.join(lesson, 'narration.json')))
wav = lambda i: os.path.join(lesson, 'audio', i + '.wav')
have = all(os.path.exists(wav(s['id'])) for s in N)
def probe(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
dur = {s['id']: (probe(wav(s['id'])) if have else round(len(s['text'].split()) / WPS / s['pace'], 3)) for s in N}
starts, t = {}, 0.0
for s in N:
    starts[s['id']] = round(t, 3); t += dur[s['id']] + GAP
total = round(t - GAP + TAIL, 2)
timing = {'starts': starts, 'dur': dur, 'total': total, 'provisional': not have}
json.dump(timing, open(os.path.join(lesson, 'timing.json'), 'w'), indent=1)
if have:
    ins, chains = [], []
    for k, s in enumerate(N):
        ins += ['-i', wav(s['id'])]
        ms = int(starts[s['id']] * 1000)
        chains.append(f'[{k}:a]aresample=44100,aformat=channel_layouts=mono,adelay={ms}[a{k}]')
    mix = ''.join(f'[a{k}]' for k in range(len(N)))
    fc = ';'.join(chains) + f';{mix}amix=inputs={len(N)}:normalize=0,apad=whole_dur={total}[out]'
    subprocess.check_call(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fc, '-map', '[out]',
                           os.path.join(lesson, 'hf', 'assets', 'voice.wav')])
else:
    # silent placeholder so the animatic renders; replaced by the real track once takes exist
    subprocess.check_call(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                           '-t', str(total), os.path.join(lesson, 'hf', 'assets', 'voice.wav')])
# vendored libraries (headless Chrome cannot reach CDNs from every environment)
shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor'),
                os.path.join(lesson, 'hf', 'assets', 'lib'), dirs_exist_ok=True)
# sync the composition: scene clip timings, root duration and the TIMING literal
p = os.path.join(lesson, 'hf', 'index.html'); h = open(p).read()
ids = [s['id'] for s in N]
for k, i in enumerate(ids):
    end = starts[ids[k + 1]] if k + 1 < len(ids) else total
    h = re.sub(rf'(id="{i.upper()}" data-start=")[\d.]+(" data-duration=")[\d.]+', rf'\g<1>{starts[i]}\g<2>{round(end - starts[i], 3)}', h)
h = re.sub(r'(data-composition-id="main" data-start="0" data-duration=")[\d.]+', rf'\g<1>{total}', h)
h = re.sub(r'(<audio id="voice"[^>]*data-duration=")[\d.]+', rf'\g<1>{total}', h)
h = re.sub(r'/\*TIMING\*/.*?/\*END\*/', '/*TIMING*/' + json.dumps({'starts': starts, 'total': total}) + '/*END*/', h, flags=re.S)
open(p, 'w').write(h)
print(('measured' if have else 'PROVISIONAL (no takes yet)'), json.dumps(timing))
