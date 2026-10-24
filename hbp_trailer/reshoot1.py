# Re-shoot round 1, approved by the user on 2026-10-24: 8 clips, ~$6.70. Run directly only.
import concurrent.futures as cf
from video import run, VEO, SEED
K='keyframes169/'
JOBS=[ # name, model, first frame, last frame, motion
 ('01_spinners',SEED,'01_spinners',None,"The two hooded women walk briskly up the rainy cobbled lane toward the camera at a steady walking pace, not running; the black-haired woman leans in, talking urgently and gesturing with one hand; the blonde woman keeps walking, face set and frightened. Heavy rain falls, puddles ripple. The camera tracks slowly backward with them. Natural, smooth walking motion."),
 ('04_dumbledore',SEED,'04_dumbledore',None,"Slow push-in. The old wizard slowly lifts his blackened, withered right hand a little higher into the light; the gold ring with the black stone glints. He raises his eyes and looks calmly into the camera over his spectacles. The fire stays inside the fireplace in the background; candle flames flicker gently; nothing else catches fire. Subtle, deliberate motion."),
 ('07_felix',SEED,'07_felix',None,"The fat bald professor lifts the tiny glowing vial a little higher and turns it slightly in his fingers, his smug smile widening with pride. The gold potion glows softly and stays inside the vial. The students in the foreground shift slightly. Torch flames flicker. Slow push-in. Calm, minimal motion."),
 ('08_cabinet',SEED,'08_cabinet',None,"The pale blonde boy stands still with his palm on the cabinet door, breathing slowly and shakily, shoulders rising and falling; he closes his eyes. Dust motes drift through the green light. The camera slowly pushes in toward his face. Minimal, quiet motion."),
 ('10_bathroom',SEED,'10a_duel','10b_fallen',"A thin white slash of spell-light flies from the black-haired boy's wand and strikes the blonde boy; the mirrors behind him shatter outward into glittering shards; the blonde boy is knocked backward, falls onto the wet flooded floor and lies still; the black-haired boy staggers back in horror and covers his mouth. Static wide camera. No blood."),
 ('12_pensieve',SEED,'12_pensieve',None,"Top-down shot. The silvery substance in the stone basin swirls slowly and gently, neither liquid nor gas. The boy and the old wizard lean slowly forward over the rim, their faces lowering toward the silver surface; the camera sinks slowly down into the softly glowing silver until it fills the whole frame. Slow, dreamlike, calm."),
 ('13_riddle',SEED,'13_riddle',None,"In the bare orphanage room, the boy slowly lowers the book in his lap and looks straight at the camera, calm and unsmiling; behind him the old wardrobe door trembles slightly on its hinges. Grey light from the window, the candle flickers. Very slow push-in. Eerie stillness. The boy stays seated."),
 ('20_curse',VEO,'20_curse',None,"The gaunt man's hair whips in the wind; his eyes harden, he thrusts his wand forward, and a brilliant jet of green light erupts from the tip, rushing toward the camera and flooding the whole frame with green. Intense and fast."),
]
if __name__=='__main__':
    print(len(JOBS),'clips, planned ~$6.70')
    def go(j):
        n,m,a,b,p=j
        return run(n,m,p,K+a+'.png',last=(K+b+'.png' if b else None))
    with cf.ThreadPoolExecutor(4) as ex: res=list(ex.map(go,JOBS))
    print('done',sum(1 for r in res if r),'of',len(JOBS))
