"""Assemble the static course site's data: python tools/build_site.py

Writes site/data/course.json (the outline, with an id on every lesson that has been built),
copies each lessons/<id>/lesson.json to site/data/lessons/<id>.json, and links the lesson's
720p video and poster when tools/site_video.py has made them.
"""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(HERE, '..'); SITE = os.path.join(C, 'site')
os.makedirs(os.path.join(SITE, 'data', 'lessons'), exist_ok=True)
course = json.load(open(os.path.join(C, 'course.json')))
built = {}
for p in sorted(glob.glob(os.path.join(C, 'lessons', '*', 'lesson.json'))):
    d = json.load(open(p)); lid = d['id']; num = lid.split('-')[0]
    d['video'] = f'videos/{lid}.mp4' if os.path.exists(os.path.join(SITE, 'videos', lid + '.mp4')) else None
    d['poster'] = f'videos/{lid}.jpg' if os.path.exists(os.path.join(SITE, 'videos', lid + '.jpg')) else None
    json.dump(d, open(os.path.join(SITE, 'data', 'lessons', lid + '.json'), 'w'), indent=1, ensure_ascii=False)
    built[num] = lid
for m in course['modules']:
    for l in m['lessons']:
        if l['num'] in built: l['id'] = built[l['num']]
json.dump(course, open(os.path.join(SITE, 'data', 'course.json'), 'w'), indent=1, ensure_ascii=False)
print('lessons built:', ', '.join(built.values()) or 'none')
