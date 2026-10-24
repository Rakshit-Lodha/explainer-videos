# Generates the 60 s score with the ElevenLabs Music API from a section plan. Run directly only.
import os,json,requests
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
PLAN={'positive_global_styles':['dark cinematic fantasy trailer score','orchestral','anime film soundtrack','instrumental'],
 'negative_global_styles':['lyrics','vocals singing words','pop','EDM','upbeat'],
 'sections':[
  {'section_name':'Music box','positive_local_styles':['lone music box','slightly out of tune','eerie','sparse','rainy night'],'negative_local_styles':['drums','strings'],'duration_ms':6500,'lines':[]},
  {'section_name':'Omen','positive_local_styles':['sudden deep boom at the start','dark low string tremolo','ominous brass swell'],'negative_local_styles':['music box'],'duration_ms':6500,'lines':[]},
  {'section_name':'The Prince','positive_local_styles':['low strings','slow building pulse','mysterious','tension rising','ticking percussion'],'negative_local_styles':['loud drums'],'duration_ms':14000,'lines':[]},
  {'section_name':'Memory','positive_local_styles':['near silence','single sustained low cello note','sparse','haunting','memory'],'negative_local_styles':['drums','melody'],'duration_ms':12500,'lines':[]},
  {'section_name':'The Cave','positive_local_styles':['wordless low choir enters','full orchestra builds','taiko drums','epic crescendo','massive hit at the end'],'negative_local_styles':['lyrics'],'duration_ms':11000,'lines':[]},
  {'section_name':'The Tower','positive_local_styles':['orchestra drops out','thin high dissonant string tremolo','cold wind-like','dread'],'negative_local_styles':['drums','choir'],'duration_ms':5500,'lines':[]},
  {'section_name':'Reveal','positive_local_styles':['near silence then a low dark brass and string sting','ominous sub drone','menacing reveal','abrupt hard ending'],'negative_local_styles':['drums','choir','flute'],'duration_ms':4000,'lines':[]},
 ]}
if __name__=='__main__':
    assert sum(s['duration_ms'] for s in PLAN['sections'])==60000
    r=requests.post('https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128',headers={'xi-api-key':K},
        json={'composition_plan':PLAN,'model_id':'music_v1'},timeout=600)
    print(r.status_code, r.headers.get('content-type'))
    if r.status_code==200: open('music/score_v2.mp3','wb').write(r.content); print('wrote music/score_v2.mp3')
    else: print(r.text[:500])
