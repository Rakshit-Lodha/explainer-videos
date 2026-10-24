# Rough cut: trims each clip to its screenplay duration, burns English subtitles, concatenates.
# Run with system python3 (Pillow) from hbp_trailer/.
import os, subprocess, glob
from PIL import Image, ImageDraw, ImageFont
FF='/opt/homebrew/bin/ffmpeg'; W,H=1920,1080
FONT=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',50)
SPEED={'01':1.25}  # lip-sync retime: slow the talking part to cover the line
EDL=[ # shot, source (clip name in clips/ or 'still:<keyframe>'), duration, in-point, subtitle, fx
 ('01','01_spinners',3.8,0,"Cissy, wait! He can't be trusted!",'fadein'),
 ('02','02_vow',3.2,0,'Severus… will you swear it?',None),
 ('03','03_bridge',2.5,0.8,None,None),
 ('04','04_dumbledore',3.5,0,'Harry, I need your help.',None),
 ('05','still:05_bookpage',2.0,0,'This book is the property of the Half-Blood Prince.',None),
 ('06','06_book',2.5,0,None,None),
 ('07','07_felix',2.0,0,None,None),
 ('08','08_cabinet',3.0,0,None,None),
 ('09','09_standoff',2.5,0,None,None),
 ('10','09_sectum',2.0,0,'Sectumsempra!',None),
 ('11','11_memory',3.0,0,"I'm sorry.",None),
 ('12','12_pensieve',2.0,1.5,None,None),
 ('13','13_riddle',3.0,0,"I'm… special.",None),
 ('14','14_slugclub',4.5,0,'Sir… what can you tell me about Horcruxes?',None),
 ('15','15_cliff',1.5,0,None,None),
 ('16','16_lake',2.5,0,None,None),
 ('17','17_basin',4.0,0,'Make it… stop…',None),
 ('18','18_fire',3.0,0,None,None),
 ('19','19_tower',3.5,0,'Severus… please.',None),
 ('20','20_curse',2.0,2.5,'Avada Kedavra.','towhite'),
 ('21','21_prince',4.0,0,'I am the Half-Blood Prince.','fromwhite_quickblack'),
]
os.makedirs('build/seg',exist_ok=True)
def sub_png(text,path):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if text:
        w=d.textlength(text,font=FONT); d.text(((W-w)/2,H-120),text,font=FONT,fill='white',stroke_width=4,stroke_fill='black')
    im.save(path)
def run(cmd): subprocess.run(cmd,check=True)
segs=[]
for sid,src,dur,inp,sub,fx in EDL:
    out=f'build/seg/{sid}.mp4'; png=f'build/seg/{sid}_sub.png'; sub_png(sub,png)
    vf='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,setsar=1'
    if fx=='fadein': vf+=',fade=t=in:st=0:d=0.6'
    if fx=='towhite': vf+=f',fade=t=out:st={dur-0.3}:d=0.3:color=white'
    if fx=='fromwhite_toblack': vf+=f',fade=t=in:st=0:d=0.6:color=white,fade=t=out:st={dur-1.2}:d=1.2'
    if fx=='fromwhite_quickblack': vf+=f',fade=t=in:st=0:d=0.4:color=white,fade=t=out:st={dur-0.3}:d=0.3'
    if src.startswith('still:'):
        n=int(dur*24)
        inputs=['-loop','1','-t',str(dur),'-i',f'keyframes169/{src[6:]}.png']
        fade=vf.split('setsar=1',1)[1]
        vf=f"scale=3840:-1,zoompan=z='1+0.10*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=24,setsar=1"+fade
    else:
        clip=f'clips/{src}.mp4'
        cdur=float(subprocess.run(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',clip],capture_output=True,text=True).stdout)
        if sid in SPEED:
            vf=f'setpts=PTS*{SPEED[sid]},'+vf
            inputs=['-ss',str(inp),'-i',clip]
        elif inp+dur>cdur+0.01:  # clip too short: slow it down slightly to fill the slot
            vf=f'setpts=PTS*{dur/(cdur-inp):.4f},'+vf
            inputs=['-ss',str(inp),'-i',clip]
        else:
            inputs=['-ss',str(inp),'-t',str(dur),'-i',clip]
    run([FF,'-v','error','-y',*inputs,'-i',png,'-filter_complex',f'[0:v]{vf}[v];[v][1:v]overlay=0:0,format=yuv420p','-t',str(dur),'-an','-c:v','libx264','-crf','18','-preset','medium',out])
    segs.append(out)
open('build/seg/list.txt','w').write(''.join(f"file '{os.path.basename(s)}'\n" for s in segs))
run([FF,'-v','error','-y','-f','concat','-safe','0','-i','build/seg/list.txt','-c','copy','build/picture_v5.mp4'])
print('wrote build/picture_v5.mp4')
