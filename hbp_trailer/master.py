# Final master: two-pass loudnorm (-14 LUFS, -1.5 dBTP) of the mix onto the locked picture.
import subprocess,json,re
FF='/opt/homebrew/bin/ffmpeg'; PIC='build/picture_v4.mp4'; MIX='build/mix_final.wav'; OUT='../HBP_Anime_Trailer.mp4'
e=subprocess.run([FF,'-hide_banner','-i',MIX,'-af','loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
j=json.loads(e[e.rindex('{'):e.rindex('}')+1])
af=(f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
    f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000")
subprocess.run([FF,'-v','error','-y','-i',PIC,'-i',MIX,'-map','0:v','-map','1:a','-c:v','copy','-af',af,'-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',OUT],check=True)
print('measured input',j['input_i'],'LUFS',j['input_tp'],'dBTP; wrote',OUT)
