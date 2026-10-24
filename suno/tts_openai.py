import json, os, sys, requests
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY']}
MODEL='gpt-4o-mini-tts-2025-12-15'
for s in json.load(open('narration.json')):
    if len(sys.argv)>1 and s['id'] not in sys.argv[1:]: continue
    r=requests.post('https://api.openai.com/v1/audio/speech',headers=H,json={
        'model':MODEL,'voice':s.get('voice','cedar'),'input':s['text'],'instructions':s['instructions'],'response_format':'wav'},timeout=180)
    if r.status_code!=200: print(s['id'],r.status_code,r.text[:300]); continue
    open(f"audio_openai/{s['id']}.wav",'wb').write(r.content); print('ok',s['id'])
