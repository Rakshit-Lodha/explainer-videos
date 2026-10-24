import json, sys, concurrent.futures as cf
from or_video import run
sh={s['id']:s for s in json.load(open('shots.json'))}
MOVE=" Clear, noticeable camera movement and character motion, not a static shot."
FAST='google/veo-3.1-fast'; RATE=0.08
jobs=[ # id, duration, first, last
 ('1a',6,None,None),('1b',4,None,None),('1c',6,None,None),('2b',6,None,None),('2c',6,None,None),('2e',6,None,None),
 ('3a',4,None,None),('4b',6,None,None),('5a',6,'5a_raft','5b_boat'),('5b',6,'5b_boat','5c_ship'),
 ('6b',4,None,None),('6c',4,None,None),('7a',6,None,None),('7c',6,None,None),('8a',6,None,None),('8c',6,None,None)]
planned=sum(d*RATE for _,d,_,_ in jobs)+0.85
CAP=8.2
print(f'planned Veo cost ${planned-0.85:.2f} + Seedance ~$0.85 = ${planned:.2f} (cap ${CAP})')
if planned>CAP: sys.exit('over cap')
def go(j):
    i,d,f,l=j; s=sh[i]
    return run(i,FAST,s['motion']+MOVE,f"keyframes/{f or s['kf']}.png",d,last=(f"keyframes/{l}.png" if l else None))
only=sys.argv[1:]
with cf.ThreadPoolExecutor(4) as ex:
    list(ex.map(go,[j for j in jobs if not only or j[0] in only]))
