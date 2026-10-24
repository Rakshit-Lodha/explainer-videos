import os, sys, json, time, base64, requests, concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENROUTER_API_KEY'],'Content-Type':'application/json'}
STYLE=(" Keep the hand-drawn dark seinen anime style of the input image exactly: ink linework, hard cel shading, palette and lighting."
       " Characters keep exactly the same faces, hair and costumes. Smooth cinematic motion, no morphing, no text, no subtitles.")
VEO='google/veo-3.1-lite'; SEED='bytedance/seedance-2.5'
def data_uri(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
def run(name,model,prompt,first,duration=4,last=None,resolution='720p'):
    fi=[{'type':'image_url','image_url':{'url':data_uri(first)},'frame_type':'first_frame'}]
    if last: fi.append({'type':'image_url','image_url':{'url':data_uri(last)},'frame_type':'last_frame'})
    body={'model':model,'prompt':prompt+STYLE,'duration':duration,'resolution':resolution,'aspect_ratio':'16:9','generate_audio':False,'frame_images':fi}
    r=requests.post('https://openrouter.ai/api/v1/videos',headers=H,json=body,timeout=180)
    if r.status_code not in (200,201,202): print(name,'SUBMIT',r.status_code,r.text[:400]); return None
    j=r.json(); t0=time.time()
    while time.time()-t0<1500:
        s=requests.get(j['polling_url'],headers=H,timeout=60).json()
        if s.get('status')=='completed': break
        if s.get('status')=='failed': print(name,'FAILED',str(s)[:400]); return None
        time.sleep(15)
    else: print(name,'TIMEOUT',j['id']); return None
    json.dump(s,open(f'clips/{name}.json','w'),indent=1)
    v=requests.get(s['unsigned_urls'][0],headers=H,timeout=300)
    open(f'clips/{name}.mp4','wb').write(v.content); print('ok',name,len(v.content),'bytes',s.get('usage') or '')
    return s
TESTS=[
 ('test_04_veo',VEO,"Slow push-in. The old wizard slowly raises his blackened, withered right hand into the firelight; the gold ring with the black stone glints. He lifts his eyes and looks calmly into the camera over his spectacles. Fire and candle flames flicker gently. Subtle, deliberate motion.",'keyframes/04_dumbledore.png'),
 ('test_18_seed',SEED,"The old wizard sweeps his raised wand and the colossal ring of fire roars and whips around the island, flames surging and embers flying; skeletal figures in the black water recoil and sink beneath the surface; the boy crouches and shields his face. Camera slowly circles at a low angle. Dynamic, powerful.",'keyframes/18_fire.png'),
]
if __name__=='__main__':
    with cf.ThreadPoolExecutor(2) as ex: list(ex.map(lambda t: run(t[0],t[1],t[2],t[3]),TESTS))
