import json
TOTAL=206.2
sh=json.load(open('shots.json'))
vids={'2a','2d','4a','4c','4d','6a','7b'}   # fixed-length Seedance drafts
stretch={'3b2','1a','1b','1c','2b','2c','2e','3a','4b','5a','5b','6b','6c','7a','7c','8a','8c','8d'}  # new clips, stretched to window
vdur={'2a':7.04,'2d':8.04,'3b':5.0,'4a':8.04,'4c':8.04,'4d':7.04,'6a':7.04,'7b':8.04}
# insert 5c, fix anchors
out=[]
SRC={'4b':'clips/or/4b2.mp4'}   # regenerated shovel shot
for s in sh:
    if s['id']=='3b': out.append(dict(id='3b2',t=66.8,kf='3a_last')); continue
    out.append(dict(id=s['id'],t=s['t'],kf=s['kf']))
    if s['id']=='5b': out.append(dict(id='5c',t=121.8,kf='5c_ship'))
for i,s in enumerate(out):
    s['v']=(s['id'] in vids) or (s['id'] in stretch)
shots=[];prev_end=0.0
for i,s in enumerate(out):
    start=prev_end
    if s['id'] in vids: end=start+vdur[s['id']]
    else:
        nxt=out[i+1]['t'] if i+1<len(out) else TOTAL
        end=max(nxt,start+2.0)
    shots.append(dict(id=s['id'],kf=s['kf'],v=s['v'],s=round(start,3),e=round(end,3)))
    if s['id'] in stretch: shots[-1]['e']=round(end,3)
    prev_end=end
shots[-1]['e']=TOTAL
import subprocess, shutil
shots[-1]['e']=TOTAL
FF='/opt/homebrew/bin/ffmpeg'; FP='/opt/homebrew/bin/ffprobe'
for x in shots:
    if x['id'] in stretch:
        src=SRC.get(x['id'],f"clips/or/{x['id']}.mp4")
        sd=float(subprocess.check_output([FP,'-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
        h=int(subprocess.check_output([FP,'-v','error','-select_streams','v:0','-show_entries','stream=height','-of','csv=p=0',src]))
        win=x['e']-x['s']
        vf=[]
        if h==1280: vf.append('crop=720:1080:0:100')
        vf.append(f'setpts=PTS*{win/sd:.5f}'); vf.append('fps=30')
        subprocess.run([FF,'-y','-loglevel','error','-i',src,'-vf',','.join(vf),'-t',f'{win:.3f}','-an','-c:v','libx264','-crf','17','-g','15','-pix_fmt','yuv420p',f"hf_story/assets/{x['id']}.mp4"],check=True)
J=json.dumps(shots)
wraps=[]
for x in shots:
    if x['v']:
        inner=f'<video id="V_{x["id"]}" class="clip" src="assets/{x["id"]}.mp4" data-start="{x["s"]}" data-duration="{round(x["e"]-x["s"],3)}" data-track-index="1" muted playsinline></video>'
    else:
        inner=f'<img id="I_{x["id"]}" src="assets/{x["kf"]}.png" />'
    wraps.append(f'    <div class="shotwrap" id="W_{x["id"]}">{inner}</div>')
html=open('story_template.html').read().replace('/*SHOTS*/[]',J).replace('<!--WRAPS-->','\n'.join(wraps))
open('hf_story/index.html','w').write(html)
for s in shots: print(s['id'],s['s'],s['e'],'VIDEO' if s['v'] else 'still')
