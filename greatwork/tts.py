import json, base64, os, sys, requests
from dotenv import load_dotenv
load_dotenv('../.env')
key=os.environ['SARVAM_API_KEY']
for s in json.load(open('narration.json')):
    if len(sys.argv)>1 and s['id'] not in sys.argv[1:]: continue
    r=requests.post('https://api.sarvam.ai/text-to-speech',headers={'api-subscription-key':key},json={
        'text':s['text'],'target_language_code':'en-IN','speaker':'ratan','model':'bulbul:v3',
        'pace':s['pace'],'temperature':s['temperature']},timeout=120)
    if r.status_code!=200: print(s['id'],r.status_code,r.text[:300]); continue
    open(f"audio/{s['id']}.wav",'wb').write(base64.b64decode(r.json()['audios'][0]))
    print('ok',s['id'])
