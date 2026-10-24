import os, sys, json, time, base64, requests
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENROUTER_API_KEY'],'Content-Type':'application/json'}
STYLE=" Keep the flat vector illustrated art style, palette and lighting of the input image exactly; smooth cinematic camera motion; the character keeps the same design; no text, no captions."
def data_uri(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
def run(name,model,prompt,first,duration,last=None,resolution='720p',audio=False,out='clips/or',poll=15,timeout=1500,url_map=None):
    def img(p): return (url_map or {}).get(p) or data_uri(p)
    fi=[{'type':'image_url','image_url':{'url':img(first)},'frame_type':'first_frame'}]
    if last: fi.append({'type':'image_url','image_url':{'url':img(last)},'frame_type':'last_frame'})
    body={'model':model,'prompt':prompt+STYLE,'duration':duration,'resolution':resolution,'aspect_ratio':'9:16','generate_audio':audio,'frame_images':fi}
    r=requests.post('https://openrouter.ai/api/v1/videos',headers=H,json=body,timeout=180)
    if r.status_code not in (200,201,202): print(name,'SUBMIT',r.status_code,r.text[:400]); return None
    j=r.json(); t0=time.time()
    while time.time()-t0<timeout:
        s=requests.get(j['polling_url'],headers=H,timeout=60).json()
        if s.get('status')=='completed': break
        if s.get('status')=='failed': print(name,'FAILED',str(s)[:400]); return None
        time.sleep(poll)
    else: print(name,'TIMEOUT',j['id']); return None
    json.dump(s,open(f'{out}/{name}.json','w'),indent=1)
    v=requests.get(s['unsigned_urls'][0],headers=H,timeout=300)
    open(f'{out}/{name}.mp4','wb').write(v.content); print('ok',name,len(v.content),'bytes',s.get('usage') or '')
    return s
if __name__=='__main__':
    import concurrent.futures as cf
    sh={x['id']:x for x in json.load(open('shots.json'))}['1a']
    jobs=[('test_1a_lite','google/veo-3.1-lite'),('test_1a_fast','google/veo-3.1-fast')]
    with cf.ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda a: run(a[0],a[1],sh['motion'],f"keyframes/{sh['kf']}.png",4),jobs))
