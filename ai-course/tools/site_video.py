"""720p copy of a lesson's master for the course site: python tools/site_video.py lessons/<id>

Writes site/videos/<id>.mp4 (about 2-3 MB, committed so the Vercel deployment has it) and a
poster frame site/videos/<id>.jpg from the end of the first scene.
"""
import json, os, subprocess, sys
lesson = os.path.abspath(sys.argv[1]); lid = os.path.basename(lesson)
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'videos'); os.makedirs(SITE, exist_ok=True)
src = os.path.join(lesson, 'build', lid + '.mp4')
if not os.path.exists(src): sys.exit(f'no master at {src}; render and master the lesson first')
out = os.path.join(SITE, lid + '.mp4')
subprocess.check_call(['ffmpeg', '-y', '-v', 'error', '-i', src, '-vf', 'scale=1280:720:flags=lanczos', '-c:v', 'libx264',
                       '-preset', 'slow', '-crf', '26', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k',
                       '-movflags', '+faststart', out])
starts = list(json.load(open(os.path.join(lesson, 'timing.json')))['starts'].values())
at = starts[1] - 1.2 if len(starts) > 1 else 1
subprocess.check_call(['ffmpeg', '-y', '-v', 'error', '-ss', str(at), '-i', src, '-frames:v', '1', '-vf', 'scale=1280:720',
                       '-q:v', '4', os.path.join(SITE, lid + '.jpg')])
print(out, f'{os.path.getsize(out) / 1e6:.1f} MB')
