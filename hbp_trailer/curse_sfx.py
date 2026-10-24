# Three options for the Avada Kedavra spell sound. Run directly only.
import os,requests,concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
O={
 'c1':"Anime dark magic spell: crackling electric green energy building quickly, then a sharp powerful burst of magical light with a deep whoosh and boom, short tail",
 'c2':"Deadly magic curse cast from a wand: a hissing sizzle of energy, a violent rushing beam of light shooting forward, ending in a cold metallic impact, cinematic",
 'c3':"Cinematic spell blast: a fast reversed whoosh sucking inward, then an explosive crack of dark energy, sub bass drop and a ghostly echo",
}
def go(k):
    r=requests.post('https://api.elevenlabs.io/v1/sound-generation',headers={'xi-api-key':K},json={'text':O[k]+', no music, no voices','duration_seconds':2.2,'prompt_influence':0.6},timeout=180)
    if r.status_code!=200: print(k,r.status_code,r.text[:200]); return
    open(f'audio/sfx/curse_options/{k}.mp3','wb').write(r.content); print('ok',k)
if __name__=='__main__':
    with cf.ThreadPoolExecutor(2) as ex: list(ex.map(go,O))
