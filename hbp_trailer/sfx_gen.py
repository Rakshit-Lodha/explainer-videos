# Generates sound effects and ambience beds with ElevenLabs sound generation. Run directly only.
import os,sys,requests,concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
NOMUSIC=", no music, no voices"
S={ # name: (prompt, seconds)
 'rain':("Heavy night rain on cobblestones and brick, water running in a gutter, a distant dog barking once",6),
 'match':("A single match struck and flaring alight, close-up",1.5),
 'vow':("A magical fiery rope crackling and hissing as it tightens, glowing embers, low magical hum swelling",3.5),
 'boom':("One huge deep cinematic boom impact with a long low tail",3),
 'bridge':("A steel suspension bridge collapsing: metal groaning and snapping cables, shrieking wind of dark smoke, huge splash into a river, distant screams",4),
 'study':("Quiet crackling fireplace in a stone study, a ticking clock, soft",4),
 'dungeon':("Old dungeon classroom ambience: bubbling cauldrons, a page turning, a quill scratching on parchment",7),
 'dungeon_amb':("Old stone dungeon classroom ambience: cauldrons bubbling softly, faint murmur of fire under cauldrons, steam hiss. No paper, no page sounds",6.5),
 'pageturn':("A single page of an old thick paper book being turned, one crisp page flip, close-up",1.2),
 'chime':("A single high glassy magical chime with a soft shimmer",2),
 'cabinet':("An old wooden cabinet door creaking, slow shaky nervous breathing, dusty room tone",3),
 'bathroom':("Water spraying from a broken pipe in a tiled stone bathroom, splashing, tense room tone",3),
 'spell':("A sharp magical spell crack followed by a burst of shattering mirrors and falling glass",2),
 'office':("Candlelit office at night, a grandfather clock ticking slowly, faint candle flutter",6),
 'pensieve':("A soft swirling magical whoosh, like silver mist being drawn downward, dreamy",2.5),
 'wardrobe':("An old wooden wardrobe rattling and trembling by itself in a silent room",3),
 'clockchime':("A grandfather clock striking once, the chime fading into silence",3),
 'cliff':("Huge ocean waves crashing against sea cliffs at night, strong wind",2.5),
 'cave':("Water dripping in a vast underground cave, a deep sub-bass drone, eerie silence",7),
 'fire':("Water exploding upward then a roaring magical fire whipping around in a circle, intense flames",3.5),
 'tower':("High stone tower at night, strong cold wind gusting, cloaks flapping",6),
 'curse':("A rushing roar like a train in a tunnel, a burst of magical energy, cut off abruptly",2),
 'hutfire':("A wooden hut burning at night, roaring crackling flames, timber collapsing, sparks, night wind",4),
 'dawn':("Dawn by a still lake, very soft birdsong, gentle water lapping, peaceful",4),
}
def go(n):
    p,d=S[n]
    r=requests.post('https://api.elevenlabs.io/v1/sound-generation',headers={'xi-api-key':K},json={'text':p+NOMUSIC,'duration_seconds':max(d,0.5),'prompt_influence':0.55},timeout=180)
    if r.status_code!=200: print(n,r.status_code,r.text[:200]); return
    open(f'audio/sfx/{n}.mp3','wb').write(r.content); print('ok',n)
if __name__=='__main__':
    with cf.ThreadPoolExecutor(2) as ex: list(ex.map(go, sys.argv[1:] or list(S)))
