import json, opentimelineio as otio
T=json.load(open('timing.json')); fps=30
rt=lambda s: otio.opentime.RationalTime(round(s*fps),fps)
tl=otio.schema.Timeline(name='How UPI Moves Money in Seconds'); tl.global_start_time=rt(0)
v=otio.schema.Track(name='Motion graphics',kind=otio.schema.TrackKind.Video)
vo=otio.schema.Track(name='Voiceover (Sarvam Ratan)',kind=otio.schema.TrackKind.Audio)
mu=otio.schema.Track(name='Music (Suno)',kind=otio.schema.TrackKind.Audio)
ids=['s1','s2','s3','s4','s5','s6']; names=['Stall','Alias directory','Request journey','Sealed PIN','Ledgers and settlement','Paid']
ends=[T['starts'][i] for i in ids[1:]]+[T['total']]
for i,n,e in zip(ids,names,ends):
    st=T['starts'][i]
    v.append(otio.schema.Clip(name=f'{i} {n}',media_reference=otio.schema.ExternalReference(target_url='hf/index.html#'+i),
        source_range=otio.opentime.TimeRange(rt(st),rt(e-st)),metadata={'tool':'hyperframes'}))
    vo.append(otio.schema.Clip(name=f'{i} narration',media_reference=otio.schema.ExternalReference(target_url=f'audio/{i}.wav'),
        source_range=otio.opentime.TimeRange(rt(0),rt(T['dur'][i]))))
    gap=e-st-T['dur'][i]
    if i!='s6': vo.append(otio.schema.Gap(source_range=otio.opentime.TimeRange(rt(0),rt(gap))))
mu.append(otio.schema.Clip(name='Quiet Curiosity',media_reference=otio.schema.ExternalReference(target_url='music/quiet_curiosity.m4a'),
    source_range=otio.opentime.TimeRange(rt(0),rt(T['total']))))
tl.tracks.extend([v,vo,mu]); otio.adapters.write_to_file(tl,'build/upi.otio'); print('wrote build/upi.otio',tl.duration().to_seconds())
