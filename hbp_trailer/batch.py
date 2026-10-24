import sys, concurrent.futures as cf
from video import run, VEO, SEED
K='keyframes169/'
SHOTS=[ # id, model, keyframe, motion
 ('01','V','01_spinners',"Heavy rain falls. The two hooded women hurry up the cobbled lane; the blonde woman looks fearfully ahead, the black-haired woman glances back at the camera and grins. Cloaks whip in the wind, rain splashes on the cobbles, the window light flickers. Camera tracks slowly backward, low to the ground."),
 ('02','S','02_vow',"The glowing ribbon of red-gold fire uncoils from the wand tip and wraps tighter around both clasped wrists, crackling and sparking; the hands grip harder. The man's face behind stays still and unblinking. Lamp flame flickers. Camera slowly pushes in."),
 ('03','S','03_bridge',"Black smoke trails corkscrew down out of the storm clouds and slam into the suspension bridge; cables snap and whip, the deck twists, buckles and begins to fold into the river with huge splashes; tiny people run. Slow wide camera drift. Epic destruction."),
 ('04','V','04_dumbledore',"Slow push-in. The old wizard slowly raises his blackened, withered right hand into the firelight; the gold ring with the black stone glints. He lifts his eyes and looks calmly into the camera over his spectacles. Fire and candle flames flicker gently. Subtle, deliberate motion."),
 ('06','V','06_book',"The boy reads the old book intently, eyes moving across the cramped handwritten notes; he slowly turns a page, then his eyes narrow with curiosity. Steam drifts from the cauldrons, the candle flickers, students move softly in the background. Gentle slow push-in."),
 ('07','V','07_felix',"The fat bald professor slowly turns the tiny vial in his fingers, beaming proudly; golden droplets leap out of the vial like little fish and hang glittering in the air, spreading warm gold light across his face. Steam drifts. Slow push-in on the vial."),
 ('08','V','08_cabinet',"The pale blonde boy presses his palm against the tall black cabinet and leans closer to it, breathing shakily; the little yellow bird in the cage flutters, then falls still. Dust drifts through green shafts of light. Camera slowly pushes in."),
 ('09','S','09_sectum',"The boy slashes his wand diagonally across the frame and shouts, water spraying around him from the cracked basin; a burst of pale white spell-light flares from the wand tip. Fast, violent motion, slight camera shake."),
 ('10','S','10_bathroom',"A blinding white slash of spell-light crosses the room; every mirror explodes into glittering shards; the pale blonde boy is thrown back and falls onto the wet flooded floor; the black-haired boy staggers backward in horror. Water sprays, glass flies. Slow-motion feel."),
 ('11','V','11_memory',"The fat bald professor, sweating and frightened, slowly draws the luminous silver thread of memory from his temple with his wand tip; it curls through the air and flows down into the small glass vial. His face crumples with shame and he lowers his eyes. Candles flicker. Slow push-in."),
 ('12','V','12_pensieve',"Top-down shot: the silver mist in the stone basin swirls faster and faster like a whirlpool; the camera slowly descends straight down into the basin until the swirling silver light fills the entire frame."),
 ('13','V','13_riddle',"In the bleak orphanage room, the boy sitting on the bed slowly turns his head to look directly at the camera, a faint cold smile forming; behind him the wooden wardrobe begins to rattle and shake by itself. The candle flickers. Very slow push-in. Eerie stillness."),
 ('14','V','14_slugclub',"The handsome dark-haired teenage boy leans slowly toward the stout professor and speaks softly, lowering the ringed hand from his chin; the professor's jovial smile slowly freezes. Candles flicker; a thin white fog begins to creep in from the edges of the frame. Slow push-in."),
 ('15','V','15_cliff',"Huge waves explode against the black sea cliffs, spray flying; the old wizard holds his lit wand up and the boy follows him along the wet ledge toward the dark crack in the cliff. Cloaks whip in the wind. Slow camera drift."),
 ('16','S','16_lake',"The tiny boat glides slowly across the still black lake toward the green glow; the camera tilts down toward the water, where pale drowned faces and hands drift just beneath the surface, one hand slowly twitching. Eerie, very slow motion, gentle ripples."),
 ('17','V','17_basin',"The crying boy tips the crystal goblet of glowing green potion to the old wizard's lips; the old man shudders and trembles, eyes squeezed shut, face grey. Green light pulses from the basin. Close, intimate, slow push-in."),
 ('18','S','18_fire',"The old wizard sweeps his raised wand and the colossal ring of fire roars and whips around the island, flames surging and embers flying; skeletal figures in the black water recoil and sink beneath the surface; the boy crouches and shields his face. Camera slowly circles at a low angle. Dynamic, powerful."),
 ('19','V','19_tower',"Wind whips cloaks and hair; the green skull and serpent churn and glow in the storm clouds. The gaunt man in black walks slowly forward from the stairwell door toward the old wizard, who leans weakly on the battlements and turns his head toward him. Slow, tense push-in."),
 ('20','S','20_curse',"The gaunt man's hair whips in the wind; his eyes harden, he thrusts his wand forward, and a brilliant jet of green light erupts from the tip, rushing toward the camera and flooding the whole frame with green. Intense and fast."),
 ('21','V','21_dawn',"Dawn breaks over the still lake; golden light spreads across the water; the phoenix spreads its wings and climbs slowly into the pale gold sky until it disappears. Mist drifts. Very slow camera drift, peaceful and mournful."),
]
if __name__=='__main__':
    RATE={'V':0.12,'S':0.94}; CAP=10.0
    only=sys.argv[1:]
    jobs=[s for s in SHOTS if not only or s[0] in only]
    planned=sum(RATE[m] for _,m,_,_ in jobs)
    print(f'{len(jobs)} clips, planned ${planned:.2f} (cap ${CAP})')
    if planned>CAP: sys.exit('over cap')
    def go(s):
        i,m,kf,p=s
        return run(f'{i}_{kf.split("_",1)[1]}', VEO if m=='V' else SEED, p, K+kf+'.png')
    with cf.ThreadPoolExecutor(5) as ex: res=list(ex.map(go,jobs))
    print('done', sum(1 for r in res if r), 'of', len(jobs))
