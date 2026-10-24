import subprocess, re
FF='/opt/homebrew/bin/ffmpeg'; TOTAL=206.2
def mean_db(p):
    o=subprocess.run([FF,'-i',p,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1])
names=['shore','sailing','spray','climb','cracks','split','world','bridge','night','storm','summit','bloom']
for n in names: subprocess.run([FF,'-y','-loglevel','error','-i',f'sfx/{n}.mp3','-ar','44100','-ac','2',f'sfx/{n}.wav'],check=True)
M={n:mean_db(f'sfx/{n}.wav') for n in names}
BED,CUE=-39.0,-32.0
# (clip, start, length, offset_in_clip, target_mean_db, fade_in, fade_out)
C=[
 ('shore',0.0,21.5,0,BED,1.0,1.6),
 ('sailing',20.4,28.0,0,BED,1.6,2.0),('sailing',46.4,15.6,6,BED,2.0,1.6),
 ('spray',44.0,8.5,0,CUE,.3,1.2),
 ('climb',60.3,16.0,0,BED,1.2,1.5),
 ('cracks',75.8,24.0,0,BED+1,1.5,1.5),
 ('split',91.8,8.0,0,CUE+1,.2,1.0),
 ('world',99.6,8.8,0,BED+1,1.2,1.8),
 ('shore',106.6,22.2,0,BED,1.5,1.8),
 ('bridge',128.4,20.0,0,BED,1.5,1.8),
 ('bridge',147.6,8.6,6,BED-2,1.2,1.4),
 ('storm',156.0,8.6,0,CUE+2,.8,1.2),
 ('bridge',163.8,8.6,10,BED-2,1.0,1.6),
 ('summit',172.2,30.0,0,BED,2.0,2.5),
 ('bloom',196.6,8.4,0,CUE,.8,1.5),
]
inp=[];fc=[];lab=[]
for k,(n,st,ln,off,tgt,fi,fo) in enumerate(C):
    inp+=['-i',f'sfx/{n}.wav']
    g=tgt-M[n]
    fc.append(f"[{k}:a]atrim={off}:{off+ln},asetpts=PTS-STARTPTS,highpass=f=90,volume={g:.1f}dB,afade=t=in:d={fi},afade=t=out:st={ln-fo:.2f}:d={fo},adelay={int(st*1000)}|{int(st*1000)}[c{k}]")
    lab.append(f'[c{k}]')
fc.append(''.join(lab)+f'amix=inputs={len(C)}:normalize=0,alimiter=limit=0.8,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[o]')
subprocess.run([FF,'-y','-loglevel','error',*inp,'-filter_complex',';'.join(fc),'-map','[o]','-ar','44100','-ac','2','sfx/ambience_v2.wav'],check=True)
print({n:round(v,1) for n,v in M.items()})
