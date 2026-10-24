# Builds the 60 s soundtrack: voices + sfx + ducked score, then muxes it onto the picture and normalises loudness.
import subprocess, sys
SCORE=sys.argv[1] if len(sys.argv)>1 else 'music/score_v2.mp3'
TAG=sys.argv[2] if len(sys.argv)>2 else 'v4'
DRAMA=len(sys.argv)>3 and sys.argv[3]=='drama'
PIC='build/picture_drama.mp4' if DRAMA else 'build/picture_v5.mp4'
STOPS=[13.0,27.0,39.5,50.5]
FF='/opt/homebrew/bin/ffmpeg'; TOTAL=60.0
VOICES=[('01_bellatrix',0.2),('02_narcissa',3.9),('04_dumbledore',9.5),('10_harry',24.8),('11_slughorn',27.5),('13_riddle11',32.2),
        ('14_riddle16',34.66),('17_dumbledore',43.85),('19_dumbledore',51.0),('20_snape',54.0),('21_snape_tight',55.53)]
SFX=[ # name, start, max length, gain
 ('rain',0,3.9,0.6),('match',0,1.5,0.8),('vow',3.8,3.2,0.6),('boom',6.85,3,1.0),('bridge',7.0,2.5,0.8),
 ('study',9.5,3.5,0.4),('dungeon_amb',13,6.5,0.4),('pageturn',16.45,1.2,0.7),('chime',17.6,1.9,0.5),('cabinet',19.5,3,0.5),('bathroom',22.5,4.5,0.5),
 ('spell',26.6,1.4,0.9),('office',27,3,0.35),('pensieve',30,2,0.6),('wardrobe',32.3,2.7,0.5),('clockchime',35,3,0.45),
 ('cliff',39.5,1.5,0.7),('cave',41,6.5,0.6),('fire',47.5,3,0.9),('tower',50.5,5.5,0.6),('curse',55.3,1.0,0.8),('hutfire',56,4,0.5),
]
def chain(i,start,length,gain):
    ms=int(start*1000); f=f'atrim=0:{length},afade=t=out:st={max(length-0.2,0)}:d=0.2,' if length else ''
    return f'[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,{f}volume={gain},adelay={ms}|{ms}'
if __name__=='__main__':
    MUTE=(",volume=0:enable='"+'+'.join(f'between(t,{t-0.25},{t-0.001})' for t in STOPS)+"'") if DRAMA else ''
    if DRAMA: SFX=SFX+[('boom',t,3,1.0) for t in STOPS]
    ins=[]; parts=[]; vl=[]; sl=[]
    for n,t in VOICES:
        i=len(ins)//2; ins+=['-i',f'audio/lines/{n}.mp3']; parts.append(chain(i,t,None,1.8)+f'[v{i}]'); vl.append(f'[v{i}]')
    for n,t,L,g in SFX:
        i=len(ins)//2; ins+=['-i',f'audio/sfx/{n}.mp3']; parts.append(chain(i,t,L,g)+f'[s{i}]'); sl.append(f'[s{i}]')
    m=len(ins)//2; ins+=['-i',SCORE]
    files=ins[1::2]
    for p in parts:  # wiring check: which file each chain reads, and when it starts
        idx=int(p[1:p.index(':')]); d=p.split('adelay=')[1].split('|')[0]
        print(f'  input {idx:2d} {files[idx]:32s} at {int(d)/1000:6.2f}s')
    parts.append(''.join(vl)+f'amix=inputs={len(vl)}:normalize=0,apad=whole_dur={TOTAL},asplit=2[vbus][vsc]')
    parts.append(''.join(sl)+f'amix=inputs={len(sl)}:normalize=0,apad=whole_dur={TOTAL}'+MUTE+'[sbus]')
    parts.append(f'[{m}:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{TOTAL},volume=0.45,afade=t=out:st={TOTAL-1.5}:d=1.5[mus]')
    parts.append('[mus][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=450'+MUTE+'[duck]')
    parts.append('[vbus][sbus][duck]amix=inputs=3:normalize=0,alimiter=limit=0.95[out]')
    subprocess.run([FF,'-v','error','-y',*ins,'-filter_complex',';'.join(parts),'-map','[out]','-t',str(TOTAL),'-c:a','pcm_s16le',f'build/mix_{TAG}.wav'],check=True)
    subprocess.run([FF,'-v','error','-y','-i',PIC,'-i',f'build/mix_{TAG}.wav','-map','0:v','-map','1:a','-c:v','copy',
        '-af','loudnorm=I=-14:TP=-1.5:LRA=7','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',f'build/rough_cut_{TAG}.mp4'],check=True)
    print('wrote',f'build/rough_cut_{TAG}.mp4')
