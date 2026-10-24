import os, sys, json, time, base64, requests, concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Key '+os.environ['FAL_AI'],'Content-Type':'application/json'}
STYLE_SUFFIX=" Keep the flat vector illustrated art style, palette and lighting of the input image exactly; smooth cinematic camera motion; the character keeps the same design; no text, no captions."
def data_uri(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
def run(endpoint,body,out_prefix,poll=6,timeout=1500):
    r=requests.post('https://queue.fal.run/'+endpoint,headers=H,json=body,timeout=120)
    if r.status_code not in (200,201): print(out_prefix,'SUBMIT',r.status_code,r.text[:300]); return None
    q=r.json(); t0=time.time()
    while time.time()-t0<timeout:
        s=requests.get(q['status_url'],headers=H,timeout=60).json()
        if s.get('status')=='COMPLETED': break
        if s.get('status') in ('FAILED','ERROR'): print(out_prefix,'FAILED',str(s)[:300]); return None
        time.sleep(poll)
    else: print(out_prefix,'TIMEOUT',q.get('request_id')); return None
    res=requests.get(q['response_url'],headers=H,timeout=120)
    if res.status_code!=200: print(out_prefix,'RESULT',res.status_code,res.text[:300]); return None
    j=res.json(); json.dump(j,open(out_prefix+'.json','w'),indent=1)
    url=(j.get('video') or {}).get('url')
    if url: open(out_prefix+'.mp4','wb').write(requests.get(url,timeout=300).content)
    print('ok',out_prefix,'request',q.get('request_id')); return j
if __name__=='__main__':
    sh={s['id']:s for s in json.load(open('shots.json'))}
    ids=sys.argv[1:]
    def go(i):
        s=sh[i]
        body={'image_url':data_uri(f"keyframes/{s['kf']}.png"),'prompt':s['motion']+STYLE_SUFFIX,'duration':str(int(round(s['d']))),'draft':True,'generate_audio':False,'aspect_ratio':'auto'}
        return run('bytedance/seedance-2.5/image-to-video',body,f'clips/draft/{i}')
    with cf.ThreadPoolExecutor(3) as ex: list(ex.map(go,ids))
