import os, requests, concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env')
K=os.environ['ELEVEN_LABS_API_KEY']
NOMUSIC=", realistic field recording, no music, no voices"
S={
'shore':("Gentle ocean waves lapping and washing over a rocky shore at dusk, soft and a little distant",24),
'sailing':("A small wooden sailboat gliding over calm sea, water lapping against the hull, soft breeze in the sail, faint rope creak",28),
'spray':("A sailboat heeling over in a gust, spray and waves splashing against the bow, canvas sail flapping and snapping",9),
'climb':("Slow footsteps on rock and loose pebbles on a windy mountain slope, soft wind",16),
'cracks':("Delicate crackling of stone and ice, glassy tinkling of tiny shards, quiet and mysterious",24),
'split':("A heavy rock face cracking open with a deep stone rumble followed by a bright magical whoosh of light",8),
'world':("Distant waterfalls and a gentle shimmering magical ambience of a hidden valley, very soft wind chimes",12),
'bridge':("Steady mountain wind over a deep chasm, thin whistling gusts, soft cloth flapping",22),
'night':("Quiet high mountain ridge at night, soft low wind, the faint crackle of a lantern flame",12),
'storm':("A fierce howling blizzard wind with blowing snow and a lantern rattling in the gale",10),
'summit':("Calm high mountain summit at dawn, soft steady wind, a distant bird call, very peaceful",30),
'bloom':("A warm swelling magical shimmer as a great light blooms open, uplifting, airy",8),
}
def go(item):
    n,(p,d)=item
    r=requests.post('https://api.elevenlabs.io/v1/sound-generation',headers={'xi-api-key':K},json={'text':p+NOMUSIC,'duration_seconds':d,'prompt_influence':0.55},timeout=180)
    if r.status_code!=200: print(n,r.status_code,r.text[:200]); return
    open(f'sfx/{n}.mp3','wb').write(r.content); print('ok',n,d)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(go,S.items()))
