# Generates each spoken line with Eleven v4 in the chosen character voice. Run directly only.
import os,sys,json,requests,base64,concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
LINES=[ # id, character, shot start (s), text with v4 audio tags
 ('01_bellatrix','bellatrix',0.3,'[urgent, scornful, breathless] シシー、待って！あの男は信用できない！'),
 ('02_narcissa','narcissa',3.0,'[hushed, frightened whisper] セブルス……誓ってくれる？'),
 ('04_dumbledore','dumbledore',9.5,'[warmly, calm and grave] ハリー、君の力が必要じゃ。'),
 ('10_harry','harry',25.0,'[shouting, desperate] セクタムセンプラ！'),
 ('11_slughorn','slughorn',27.0,'[whispering, ashamed] ……すまない。'),
 ('13_riddle11','riddle11',32.0,'[softly, flat and eerie] 僕は……特別なんだ。'),
 ('14_riddle16','riddle16',35.0,'[softly, polite and charming] 先生……ホークラックスについて、教えていただけますか？'),
 ('17_dumbledore','dumbledore',44.0,'[weak, broken, pleading] もう……やめてくれ……'),
 ('19_dumbledore','dumbledore',50.5,'[quietly, at peace] セブルス……頼む。'),
 ('20_snape','snape',54.0,'[low, cold, deliberate] アバダ ケダブラ。'),
 ('21_snape','snape',56.3,'[low, cold, furious] この私が……半純血のプリンスだ。'),
]
def go(l,voices,stab):
    lid,ch,_,text=l
    if ch not in voices: print('skip',lid,'(no voice yet)'); return
    r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voices[ch]['voice_id']}/with-timestamps?output_format=mp3_44100_128",
        headers={'xi-api-key':K},json={'text':text,'model_id':'eleven_v4','voice_settings':{'stability':stab,'similarity_boost':0.75}},timeout=180)
    if r.status_code!=200: print(lid,r.status_code,r.text[:300]); return
    j=r.json(); open(f'audio/lines/{lid}.mp3','wb').write(base64.b64decode(j['audio_base64']))
    json.dump(j.get('alignment'),open(f'audio/lines/{lid}.json','w'),ensure_ascii=False); print('ok',lid)
if __name__=='__main__':
    voices=json.load(open('audio/voices/voices.json'))
    only=sys.argv[1:]
    with cf.ThreadPoolExecutor(3) as ex: list(ex.map(lambda l: go(l,voices,0.4),[l for l in LINES if not only or l[0] in only]))
