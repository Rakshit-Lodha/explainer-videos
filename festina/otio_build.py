import opentimelineio as otio
R=30
def rt(s): return otio.opentime.RationalTime(round(s*R),R)
def rng(s): return otio.opentime.TimeRange(otio.opentime.RationalTime(0,R),rt(s))
tl=otio.schema.Timeline(name="Festina Lente minimal intro")
v=otio.schema.Track(name="video",kind=otio.schema.TrackKind.Video)
v.append(otio.schema.Clip(name="bust plate + HTML type + light burst",media_reference=otio.schema.ExternalReference(target_url="hf/assets/bust.png"),source_range=rng(1.5)))
a=otio.schema.Track(name="sfx",kind=otio.schema.TrackKind.Audio)
a.append(otio.schema.Clip(name="SFX riser + burst (ElevenLabs sound-generation)",media_reference=otio.schema.ExternalReference(target_url="hf/assets/sfx.wav"),source_range=rng(1.5)))
tl.tracks.extend([v,a]); otio.adapters.write_to_file(tl,"build/festina.otio"); print("ok")
