# Builds build/storyboard.jpg from the keyframes. Run with system python3 (needs Pillow).
from PIL import Image, ImageDraw, ImageFont
SUP='/System/Library/Fonts/Supplemental/'
G=lambda n,s: ImageFont.truetype(SUP+n,s)
SH=[ # shot, keyframe, start, end, English subtitle, note
 ('1','01_spinners','0:00','0:02.5',None,'Rain. Narcissa and Bellatrix hurry up the lane.'),
 ('2','02_vow','0:02.5','0:06','Severus… will you swear it?','The Unbreakable Vow. A boom on the cut.'),
 ('3','03_bridge','0:06','0:09.5',None,'Death Eaters tear a London bridge apart.'),
 ('4','04_dumbledore','0:09.5','0:13','Harry, I need your help.','Dumbledore raises his dead hand. The ring glints.'),
 ('5','05_bookpage','0:13','0:15','This book is the property of the Half-Blood Prince.',"Insert: the Prince's inscription, slow push-in."),
 ('6','06_book','0:15','0:17.5',None,"Harry reads the Prince's notes."),
 ('7','07_felix','0:17.5','0:19.5',None,'Slughorn shows off Felix Felicis.'),
 ('8','08_cabinet','0:19.5','0:22.5',None,'Draco works on the cabinet. The bird falls silent.'),
 ('9','09_sectum','0:22.5','0:24','Sectumsempra!',"Harry shouts the Prince's spell."),
 ('10','10_bathroom','0:24','0:27',None,'Mirrors explode. Draco falls. Silence.'),
 ('11','11_memory','0:27','0:30',"I'm sorry.",'Slughorn gives up his memory.'),
 ('12','12_pensieve','0:30','0:32',None,'Into the Pensieve.'),
 ('13','13_riddle','0:32','0:35',"I'm… special.",'The orphanage, 1938. The wardrobe rattles.'),
 ('14','14_slugclub','0:35','0:39','Sir… what can you tell me about Horcruxes?','1943. After the party, Riddle stays behind.'),
 ('15','15_cliff','0:39','0:41',None,'The sea cliffs. The choir enters.'),
 ('16','16_lake','0:41','0:44',None,'The lake of the dead.'),
 ('17','17_basin','0:44','0:47','Make it… stop…','Harry makes Dumbledore drink.'),
 ('18','18_fire','0:47','0:50.5',None,"Inferi rise. Dumbledore's ring of fire."),
 ('19','19_tower','0:50.5','0:54','Severus… please.','The tower under the Dark Mark.'),
 ('20','20_curse','0:54','0:56','Avada Kedavra.','Green light floods the frame. Cut to white.'),
 ('21','21_dawn','0:56','1:00',None,'Dawn. The white tomb. The phoenix rises. Fade to black.'),
]
W,H=960,540
def frame(img,sub):
    im=Image.open(f'keyframes/{img}.png').convert('RGB').resize((W,H)); d=ImageDraw.Draw(im)
    if sub:
        f=G('Georgia.ttf',30 if len(sub)<45 else 26); w=d.textlength(sub,font=f)
        d.text(((W-w)/2,H-62),sub,font=f,fill='white',stroke_width=3,stroke_fill='black')
    return im
cols,P,CAP=3,14,74
rows=(len(SH)+cols-1)//cols
sheet=Image.new('RGB',(cols*W+(cols+1)*P,rows*(H+CAP)+(rows+1)*P+90),(14,14,18))
d=ImageDraw.Draw(sheet)
d.text((P,24),'Harry Potter and the Half-Blood Prince: anime trailer storyboard (60 s)',font=G('Georgia Bold.ttf',40),fill='white')
for i,(n,img,a,b,sub,note) in enumerate(SH):
    x=P+(i%cols)*(W+P); y=90+P+(i//cols)*(H+CAP+P)
    sheet.paste(frame(img,sub),(x,y))
    d.text((x,y+H+8),f'{n}   {a}–{b}',font=G('Georgia Bold.ttf',26),fill=(245,185,66))
    d.text((x,y+H+40),note,font=G('Georgia.ttf',24),fill=(210,210,215))
sheet.save('build/storyboard.jpg',quality=85); print(sheet.size)
