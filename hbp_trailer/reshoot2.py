# Re-shoot round 2, requested by the user on 2026-10-24: standoff + Riddle hair, 2 Seedance clips (~$1.88). Run directly only.
import concurrent.futures as cf
from video import run, SEED
K='keyframes169/'
JOBS=[
 ('09_standoff','09_standoff',"Tense standoff in the flooded bathroom: the two boys hold their wands pointed at each other, breathing hard; the pale blonde boy's lips begin to move as he starts a curse; water sprays from the cracked basin. The camera pushes in steadily toward the black-haired boy with glasses on the left. No spells fire, nothing breaks."),
 ('14_slugclub','14_slugclub',"The handsome dark-haired teenage boy leans slowly toward the stout professor and speaks softly, lowering the ringed hand from his chin; his neat side-parted hair stays exactly the same throughout. The professor's jovial smile slowly freezes. Candles flicker; a thin white fog begins to creep in from the edges of the frame. Slow push-in."),
]
if __name__=='__main__':
    with cf.ThreadPoolExecutor(2) as ex: res=list(ex.map(lambda j: run(j[0],SEED,j[2],K+j[1]+'.png'),JOBS))
    print('done',sum(1 for r in res if r),'of',len(JOBS))
