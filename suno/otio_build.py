import json, opentimelineio as otio
M=json.load(open('timing_eleven_map.json')); E=json.load(open('eleven/timing_eleven.json')); fps=30
rt=lambda s: otio.opentime.RationalTime(round(s*fps),fps)
tl=otio.schema.Timeline(name='How Suno Works'); tl.global_start_time=rt(0)
v=otio.schema.Track(name='Motion graphics',kind=otio.schema.TrackKind.Video)
vo=otio.schema.Track(name='Voiceover (ElevenLabs, cloned voice, eleven_v4)',kind=otio.schema.TrackKind.Audio)
mu=otio.schema.Track(name='Music (Suno, How It Works)',kind=otio.schema.TrackKind.Audio)
names=['Prompt','Sound as tokens','Learning to predict','Prompt steering','Tokens back to sound','Payoff']
T0,D,total=M['T0'],M['DUR'],M['total']
for k,n in enumerate(names):
    v.append(otio.schema.Clip(name=f's{k+1} {n}',media_reference=otio.schema.ExternalReference(target_url=f'hf_eleven/index.html#S{k+1}'),
        source_range=otio.opentime.TimeRange(rt(T0[k]),rt(D[k])),metadata={'tool':'hyperframes'}))
vo.append(otio.schema.Clip(name='narration (all scenes)',media_reference=otio.schema.ExternalReference(target_url='eleven/voice.mp3'),
    source_range=otio.opentime.TimeRange(rt(0),rt(E['total']))))
mu.append(otio.schema.Clip(name='How It Works',media_reference=otio.schema.ExternalReference(target_url='music/track.m4a'),
    source_range=otio.opentime.TimeRange(rt(0),rt(total))))
tl.tracks.extend([v,vo,mu]); otio.adapters.write_to_file(tl,'build/suno.otio'); print('wrote build/suno.otio',tl.duration().to_seconds())
