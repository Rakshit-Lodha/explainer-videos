# Writes build/hbp_trailer.otio: video track of shots, dialogue track, SFX track, music track. Documents the edit.
import opentimelineio as otio, importlib.util, os
R=24
import ast, types
def consts(path,names):  # read list constants without executing the script
    ns=types.SimpleNamespace()
    for node in ast.parse(open(path).read()).body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in names:
            setattr(ns,node.targets[0].id,ast.literal_eval(node.value))
    return ns
A=consts('assemble.py',{'EDL'}); M=consts('mix.py',{'VOICES','SFX'})
rt=lambda s: otio.opentime.RationalTime(round(s*R),R)
def clip(name,path,start_in,dur,meta=None):
    c=otio.schema.Clip(name=name,media_reference=otio.schema.ExternalReference(target_url=os.path.abspath(path)),
        source_range=otio.opentime.TimeRange(rt(start_in),rt(dur)))
    if meta: c.metadata['hbp']=meta
    return c
tl=otio.schema.Timeline(name='Harry Potter and the Half-Blood Prince: anime trailer')
v=otio.schema.Track(name='Video',kind=otio.schema.TrackKind.Video)
for sid,src,dur,inp,sub,fx in A.EDL:
    path=f'keyframes169/{src[6:]}.png' if src.startswith('still:') else f'clips/{src}.mp4'
    v.append(clip(f'{sid} {src}',path,inp,dur,{'subtitle':sub,'fx':fx}))
tl.tracks.append(v)
def placed(track_name,items):
    t=otio.schema.Track(name=track_name,kind=otio.schema.TrackKind.Audio); pos=0.0
    for name,path,start,length in sorted(items,key=lambda x:x[2]):
        if start>pos: t.append(otio.schema.Gap(source_range=otio.opentime.TimeRange(rt(0),rt(start-pos)))); pos=start
        t.append(clip(name,path,0,length)); pos=start+length
    return t
dur=lambda p: float(os.popen(f"/opt/homebrew/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 '{p}'").read())
tl.tracks.append(placed('Dialogue',[(n,f'audio/lines/{n}.mp3',t,dur(f'audio/lines/{n}.mp3')) for n,t in M.VOICES]))
# SFX overlap, so they go on stacked lanes
lanes=[]
for n,t,L,g in sorted(M.SFX,key=lambda x:x[1]):
    for lane in lanes:
        if lane[-1][2]+lane[-1][3]<=t: lane.append((n,f'audio/sfx/{n}.mp3',t,L)); break
    else: lanes.append([(n,f'audio/sfx/{n}.mp3',t,L)])
for i,l in enumerate(lanes): tl.tracks.append(placed(f'SFX {i+1}',l))
tl.tracks.append(placed('Music',[('score_v2','music/score_v2.mp3',0,60.0)]))
otio.adapters.write_to_file(tl,'build/hbp_trailer.otio'); print('wrote build/hbp_trailer.otio,',len(tl.tracks),'tracks, video',tl.tracks[0].duration().to_seconds(),'s')
