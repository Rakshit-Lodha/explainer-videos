"""Synthesise per-scene ambience beds locally with ffmpeg (no API), then mix them on the scene timeline."""
import subprocess, json
FF='/opt/homebrew/bin/ffmpeg'
TOTAL=206.2
def gen(name,src,filt,dur):
    subprocess.run([FF,'-y','-loglevel','error','-f','lavfi','-i',src,'-af',filt,'-t',str(dur),'-ar','44100','-ac','2',f'sfx/{name}.wav'],check=True)
# ---- base textures (60 s each, looped by trimming per use) ----
gen('ocean',"anoisesrc=c=brown:r=44100:a=0.9:seed=3","lowpass=f=700,tremolo=f=0.11:d=0.55,highpass=f=40,volume=2.2",60)
gen('lap',"anoisesrc=c=pink:r=44100:a=0.5:seed=5","bandpass=f=1800:w=900,tremolo=f=0.45:d=0.8,volume=0.9",60)
gen('wind',"anoisesrc=c=pink:r=44100:a=0.8:seed=7","bandpass=f=650:w=500,tremolo=f=0.17:d=0.65,volume=1.6",60)
gen('gale',"anoisesrc=c=pink:r=44100:a=1.0:seed=9","bandpass=f=900:w=800,tremolo=f=0.3:d=0.5,volume=2.4",60)
gen('crackle',"aevalsrc='if(gt(random(0),0.9992),(random(1)-0.5)*1.6,0)':s=44100:c=stereo","lowpass=f=5000,highpass=f=300,volume=2.0",60)
gen('hum',"aevalsrc='0.35*sin(2*PI*110*t)+0.25*sin(2*PI*165*t)+0.18*sin(2*PI*330*t)':s=44100:c=stereo","tremolo=f=0.2:d=0.4,lowpass=f=900",60)
gen('shimmer',"aevalsrc='0.2*sin(2*PI*880*t)*sin(2*PI*0.3*t)+0.15*sin(2*PI*1320*t)*sin(2*PI*0.21*t)':s=44100:c=stereo","tremolo=f=5:d=0.3,volume=0.6",60)
# drone pad = placeholder music, whole length
gen('pad',"aevalsrc='0.22*sin(2*PI*110*t)+0.16*sin(2*PI*164.81*t)+0.12*sin(2*PI*220*t)+0.09*sin(2*PI*277.18*t)':s=44100:c=stereo","tremolo=f=0.1:d=0.5,lowpass=f=1200",TOTAL)
# ---- timeline: (texture, start, end, gain dB) ----
beds=[
 ('ocean',0,23,-23),('lap',0,23,-34),('wind',0,21,-34),            # S1 shore
 ('ocean',20,62,-22),('lap',24,62,-30),('wind',40,62,-32),           # S2 sailing
 ('wind',60,77,-27),('crackle',66,77,-33),                          # S3 climb
 ('wind',75,100,-30),('crackle',76,100,-28),('hum',84,100,-30),      # S4 cracks
 ('hum',99,108,-26),('shimmer',100,108,-30),                        # S4 hidden world
 ('ocean',106,115,-27),('lap',106,129,-33),                         # S5 shore workshop
 ('wind',128,148,-25),                                              # S6 bridge
 ('wind',148,156,-31),('gale',156,164,-20),('wind',164,173,-28),     # S7 night / storm / calm
 ('wind',172,206,-30),('shimmer',196,206,-28),                      # S8 summit
]
inp=['-i','sfx/pad.wav'];fc=['[0:a]volume=-20dB,afade=t=in:d=3,afade=t=out:st=%s:d=4[p]'%(TOTAL-4)];labels=['[p]']
for k,(n,a,b,g) in enumerate(beds,1):
    inp+=['-stream_loop','-1','-i',f'sfx/{n}.wav']
    d=b-a
    fc.append(f'[{k}:a]atrim=0:{d},asetpts=PTS-STARTPTS,volume={g}dB,afade=t=in:d=1.5,afade=t=out:st={d-1.5}:d=1.5,adelay={int(a*1000)}|{int(a*1000)}[b{k}]')
    labels.append(f'[b{k}]')
fc.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[o]')
subprocess.run([FF,'-y','-loglevel','error',*inp,'-filter_complex',';'.join(fc),'-map','[o]','-ar','44100','-ac','2','sfx/ambience.wav'],check=True)
print('ok')
