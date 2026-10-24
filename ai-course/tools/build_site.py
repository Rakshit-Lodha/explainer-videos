"""Assemble the static course site's data: python tools/build_site.py

Writes site/data/course.json (the outline, with an id on every lesson that has been built),
copies each lessons/<id>/lesson.json to site/data/lessons/<id>.json and the mastered video
lessons/<id>/build/<id>.mp4 to site/videos/<id>.mp4 when it exists.
"""
import json, os, shutil, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(HERE, '..'); SITE = os.path.join(C, 'site')
os.makedirs(os.path.join(SITE, 'data', 'lessons'), exist_ok=True); os.makedirs(os.path.join(SITE, 'videos'), exist_ok=True)
course = json.load(open(os.path.join(C, 'course.json')))
built = {}
for p in sorted(glob.glob(os.path.join(C, 'lessons', '*', 'lesson.json'))):
    d = json.load(open(p)); lid = d['id']; num = lid.split('-')[0]
    mp4 = os.path.join(os.path.dirname(p), 'build', lid + '.mp4')
    d['video'] = None
    if os.path.exists(mp4):
        shutil.copy2(mp4, os.path.join(SITE, 'videos', lid + '.mp4')); d['video'] = f'videos/{lid}.mp4'
        # poster: a frame from the end of the first scene, where the lesson's question is on screen
        t = json.load(open(os.path.join(os.path.dirname(p), 'timing.json')))['starts']
        at = list(t.values())[1] - 1.2 if len(t) > 1 else 1
        subprocess.check_call(['ffmpeg', '-y', '-v', 'error', '-ss', str(at), '-i', mp4, '-frames:v', '1', '-q:v', '3',
                               os.path.join(SITE, 'videos', lid + '.jpg')])
        d['poster'] = f'videos/{lid}.jpg'
    json.dump(d, open(os.path.join(SITE, 'data', 'lessons', lid + '.json'), 'w'), indent=1, ensure_ascii=False)
    built[num] = lid
for m in course['modules']:
    for l in m['lessons']:
        if l['num'] in built: l['id'] = built[l['num']]
json.dump(course, open(os.path.join(SITE, 'data', 'course.json'), 'w'), indent=1, ensure_ascii=False)
print('lessons built:', ', '.join(built.values()) or 'none')
