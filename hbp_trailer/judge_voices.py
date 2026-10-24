import os,base64,requests,json,glob,concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env'); G=os.environ['GEMINI_API_KEY']
WANT={'narcissa':'aristocratic woman in her forties, hushed frightened pleading whisper',
 'dumbledore':'very old wise gentle wizard, warm aged baritone, calm',
 'harry':'teenage boy, intense and desperate, sudden fierce shout',
 'slughorn':'portly elderly gentleman, plummy, quiet shame and fear',
 'riddle11':'eerie calm child, soft and flat, unnervingly self-possessed',
 'riddle16':'smooth polite charming young man, cold underneath',
 'snape':'deep slow dry cold baritone, almost under his breath'}
def ask(path,want):
  try:
    return _ask(path,want)
  except Exception as e:
    return {'error':type(e).__name__}
def _ask(path,want):
    b=base64.b64encode(open(path,'rb').read()).decode()
    q=("Listen to this Japanese voice sample. Reply as JSON with keys: apparent_age, gender, pitch, tone, naturalness_1to10, "
       "pronunciation_issues, match_1to10 (how well it matches this casting brief: '"+want+"').")
    r=requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={G}',
      json={'contents':[{'parts':[{'inlineData':{'mimeType':'audio/mpeg','data':b}},{'text':q}]}],'generationConfig':{'responseMimeType':'application/json'}},timeout=300)
    if r.status_code!=200: return {'error':r.status_code,'body':r.text[:200]}
    return json.loads(r.json()['candidates'][0]['content']['parts'][0]['text'])
if __name__=='__main__':
    files=sorted(glob.glob('audio/voices/*_p[0-9].mp3'))
    with cf.ThreadPoolExecutor(3) as ex: res=list(ex.map(lambda f: ask(f,WANT[os.path.basename(f).rsplit('_p',1)[0]]),files))
    out={os.path.basename(f):r for f,r in zip(files,res)}
    json.dump(out,open('audio/voices/judge.json','w'),indent=1,ensure_ascii=False)
    for f,r in out.items(): print(f, r.get('match_1to10'), r.get('naturalness_1to10'), r.get('apparent_age'), r.get('tone'), r.get('pronunciation_issues'), r.get('error',''))
