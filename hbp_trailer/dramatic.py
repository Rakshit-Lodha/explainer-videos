# Dramatic-cut picture pass over the locked edit: hard stops to black before each act, white flash frames on spells, shake on impacts.
import subprocess
FF='/opt/homebrew/bin/ffmpeg'
STOPS=[13.0,27.0,39.5,50.5]       # act starts; the 0.25 s before each goes to black (audio muted in mix.py drama mode)
FLASH=[(3.8,0.083),(25.65,0.09),(54.9,0.083)]   # Vow, Sectumsempra, curse
SHAKE=[(7.0,7.5),(25.6,26.1),(47.5,48.0)]       # bridge, Sectumsempra, fire
B=0.25
if __name__=='__main__':
    bt="+".join(f"between(t,{s-B},{s-0.001})" for s in STOPS)
    ft="+".join(f"between(t,{a},{a+d})" for a,d in FLASH)
    st="+".join(f"between(t,{a},{b})" for a,b in SHAKE)
    g=(f"[0:v]split[a][b];[b]scale=2112:1188,crop=1920:1080:x='96+34*sin(t*83)':y='54+22*sin(t*101)'[sh];"
       f"[a][sh]overlay=enable='{st}',drawbox=color=white:t=fill:enable='{ft}',drawbox=color=black:t=fill:enable='{bt}',format=yuv420p[v]")
    subprocess.run([FF,'-v','error','-y','-i','build/picture_v4.mp4','-filter_complex',g,'-map','[v]','-c:v','libx264','-crf','18','-preset','medium','-r','24','build/picture_drama.mp4'],check=True)
    print('wrote build/picture_drama.mp4')
