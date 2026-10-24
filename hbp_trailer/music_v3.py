# Three dramatic score variants, sections locked to the v4 edit (hits on cuts). Run directly only.
import os,requests,concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
S=[ # name, ms, styles, avoid  (ElevenLabs minimum 3000 ms per section)
 ('Dread',3800,['low ominous drone','sparse dark piano notes','tension'],['drums','melody']),
 ('Vow riser',3200,['rising string tremolo riser','accelerating','building tension to a peak'],['drums']),
 ('Bridge hit then pulse',6000,['massive deep brass braam hit at the very start','huge cinematic impact','then drops to a low heartbeat pulse and sub bass'],['soft start']),
 ('Ostinato',9000,['driving staccato string ostinato','fast and relentless','ticking percussion','building intensity'],['soft pads']),
 ('Duel riser',3000,['sharp riser','snare roll building to a peak'],['melody']),
 ('Duel hit',3000,['huge impact hit at the very start','then sudden silence'],['music continuing']),
 ('Memory',11500,['eerie minor key piano motif','reversed swells','haunting celesta','unsettling, building','cut off abruptly at the end'],['drums']),
 ('Drop',8000,['full epic drop from the very start','powerful choir','taiko drums','dark brass ostinato','maximum intensity'],['soft']),
 ('Fire hit',3000,['biggest impact hit of the track at the very start','choir and brass peak','ringing out'],['quiet']),
 ('Tower',3000,['sudden near silence','thin high violin harmonic','sub drone','dread'],['drums','choir']),
 ('Curse',3000,['fast riser climaxing in a huge impact'],['melody']),
 ('Reveal',3500,['dark menacing low brass motif','slow and heavy','abrupt hard stop at the end'],['choir','soft']),
]
V={'A':['hybrid cinematic trailer score','deep brass braams','risers and impacts','taiko','orchestral','instrumental'],
   'B':['dark Japanese anime orchestral soundtrack','choir','strings','distorted electric guitar','epic','instrumental'],
   'C':['dark gothic orchestral score','pipe organ','choir','orchestra','epic','instrumental']}
def go(k):
    plan={'positive_global_styles':V[k],'negative_global_styles':['lyrics','singing words','pop','EDM','upbeat','cheerful'],
          'sections':[{'section_name':n,'positive_local_styles':p,'negative_local_styles':a,'duration_ms':ms,'lines':[]} for n,ms,p,a in S]}
    r=requests.post('https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128',headers={'xi-api-key':K},json={'composition_plan':plan,'model_id':'music_v1'},timeout=600)
    if r.status_code!=200: print(k,r.status_code,r.text[:300]); return
    open(f'music/score_v3{k}.mp3','wb').write(r.content); print('ok',k)
if __name__=='__main__':
    assert sum(s[1] for s in S)==60000, sum(s[1] for s in S)
    with cf.ThreadPoolExecutor(3) as ex: list(ex.map(go,'ABC'))
