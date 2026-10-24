import os, json, time, base64, requests
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENROUTER_API_KEY'],'Content-Type':'application/json'}
PROMPT=("The marble bust stays perfectly still and calm at the centre while the camera pushes in slowly. "
 "Torn paper sketches, glass discs, metal cylinders and red and blue spheres rush outward in streaking motion blur "
 "and then begin to slow, orbit rings turning gently. Keep the cream paper background, red, blue and black palette, "
 "and the title typography exactly as in the input image; smooth cinematic motion; no new text.")
img='data:image/png;base64,'+base64.b64encode(open('keyframe.png','rb').read()).decode()
body={'model':'google/veo-3.1-fast','prompt':PROMPT,'duration':4,'resolution':'720p','aspect_ratio':'16:9',
      'generate_audio':False,'frame_images':[{'type':'image_url','image_url':{'url':img},'frame_type':'first_frame'}]}
r=requests.post('https://openrouter.ai/api/v1/videos',headers=H,json=body,timeout=180)
if r.status_code not in (200,201,202): print('SUBMIT',r.status_code,r.text[:400]); raise SystemExit(1)
j=r.json(); t0=time.time()
while time.time()-t0<1500:
    s=requests.get(j['polling_url'],headers=H,timeout=60).json()
    if s.get('status')=='completed': break
    if s.get('status')=='failed': print('FAILED',str(s)[:400]); raise SystemExit(1)
    time.sleep(15)
else: print('TIMEOUT',j['id']); raise SystemExit(1)
json.dump(s,open('clips/intro.json','w'),indent=1)
v=requests.get(s['unsigned_urls'][0],headers=H,timeout=300)
open('clips/intro.mp4','wb').write(v.content); print('ok',len(v.content),'bytes',s.get('usage'))
