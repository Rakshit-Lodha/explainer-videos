# Saves chosen voice-design previews as permanent voices. Run directly only.
import os,sys,json,requests
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
import importlib.util
spec=importlib.util.spec_from_file_location('vd','voice_design.py'); vd=importlib.util.module_from_spec(spec); spec.loader.exec_module(vd)
if __name__=='__main__':
    picks=dict(a.split('=') for a in sys.argv[1:])  # e.g. snape=0
    saved=json.load(open('audio/voices/voices.json')) if os.path.exists('audio/voices/voices.json') else {}
    for n,i in picks.items():
        gid=json.load(open(f'audio/voices/{n}_ids.json'))[int(i)]
        r=requests.post('https://api.elevenlabs.io/v1/text-to-voice',headers={'xi-api-key':K},
            json={'voice_name':f'HBP {n}','voice_description':vd.V[n][0],'generated_voice_id':gid},timeout=120)
        if r.status_code!=200: print(n,r.status_code,r.text[:300]); continue
        saved[n]={'voice_id':r.json()['voice_id'],'preview':f'{n}_p{i}.mp3'}; print('saved',n)
    json.dump(saved,open('audio/voices/voices.json','w'),indent=1)
