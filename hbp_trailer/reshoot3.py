# Re-shoot round 3, approved 2026-10-24: shots 17 (Seedance), 19 and 21 (Veo Lite, Veo Fast fallback), start+end frames. Run directly only.
import concurrent.futures as cf
from video import run, VEO, SEED
K='keyframes169/'; FAST='google/veo-3.1-fast'
JOBS=[
 ('17_basin',SEED,'17_basin','17_basin_end',"The old wizard shudders and slowly lifts his head, crying out in anguish with his eyes squeezed shut; the crying boy keeps one hand on his shoulder and holds the goblet steady. The green light from the basin pulses. Static camera, minimal motion, no new gestures."),
 ('19_tower',VEO,'19_tower','19_tower_end',"Wind whips cloaks and hair; the green skull glows in the clouds. The gaunt man in black takes one slow step forward and raises his wand, pointing it at the old wizard, who faces him calmly and raises one hand slightly. Static wide camera. No spell fires."),
 ('21_prince',VEO,'21_prince','21_prince_end',"The gaunt man turns his face fully toward the camera as the camera pushes in to a close-up; his lips move as he speaks coldly; firelight flickers orange on his face; sparks drift from the burning hut behind him."),
]
def go(j):
    n,m,a,b,p=j
    r=run(n,m,p,K+a+'.png',last=K+b+'.png')
    if r is None and m==VEO:
        print(n,'Veo Lite failed, retrying once on Veo Fast'); r=run(n,FAST,p,K+a+'.png',last=K+b+'.png')
    return r
if __name__=='__main__':
    with cf.ThreadPoolExecutor(3) as ex: res=list(ex.map(go,JOBS))
    print('done',sum(1 for r in res if r),'of',len(JOBS))
