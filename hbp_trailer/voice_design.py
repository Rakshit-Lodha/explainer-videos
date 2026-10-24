# Designs one Japanese voice per speaking character (3 previews each). Run directly only.
import os,sys,requests,json,base64,concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env'); K=os.environ['ELEVEN_LABS_API_KEY']
V={
 'narcissa':("A woman in her forties, aristocratic, cold and refined, a hushed, frightened alto whisper, controlled and pleading, speaking Japanese.",
   "セブルス……お願い、誓ってくれる？あの子を守ると。私にはもう、あなたしか頼れる人がいないの。闇の帝王は、あの子に不可能な任務を与えたのよ。失敗すれば、あの子は殺される。だから、どうか、お願いだから、誓ってちょうだい。"),
 'bellatrix':("A woman in her mid-forties, harsh, fanatical and unhinged, urgent and scornful, slightly raspy, speaking Japanese.",
   "シシー、待って！あの男は信用できない！闇の帝王の信頼を得ているなんて、嘘に決まってるわ。あいつはずっと私たちを騙してきたのよ。お願いだから、行かないで、シシー！後悔することになるわよ！絶対に、絶対にね！"),
 'dumbledore':("A very old, wise and gentle wizard, warm aged baritone, slow, calm and kind, slightly breathy and tired, speaking Japanese.",
   "ハリー、君の力が必要じゃ。わしにはもう、あまり時間が残されておらん。だからこそ、君に頼みたいのじゃ。ヴォルデモートの過去を知ることが、奴を倒す唯一の道なのじゃよ。わしを信じてくれるかね。共に行こう、ハリー。"),
 'harry':("A young adult man with a light, youthful voice, intense and desperate, raw emotion, capable of a sudden fierce shout, speaking Japanese.",
   "セクタムセンプラ！……嘘だろ、そんなつもりじゃなかった。ただ、あいつを止めたかっただけなんだ。あの本に書いてあった呪文が、こんなことになるなんて。僕は、いったい何をしてしまったんだ。誰か、誰か助けてくれ！"),
 'slughorn':("An elderly, very portly gentleman, plummy and jovial voice gone quiet with shame and fear, a little wheezy, speaking Japanese.",
   "……すまない。本当に、すまない。あの夜のことは、ずっと忘れようとしてきたのだ。あの少年が何を聞いたのか、私は分かっていたはずなのに。教えるべきではなかった。この記憶を、君に託そう。どうか、許してくれたまえ。"),
 'riddle11':("A young adult man with a very light, soft, high and youthful voice, calm and unnervingly flat, eerily self-possessed, quiet and slightly cold, speaking Japanese.",
   "僕は……特別なんだ。ずっと分かってた。僕には、他の子にはできないことができる。動物を言いなりにできるし、意地悪な奴には、痛い目を見せることもできる。僕は普通じゃないんだ。先生も、本当は分かってるんでしょう？"),
 'riddle16':("A young adult man, smooth, polite and charming light tenor, soft-spoken, cold and calculating underneath, speaking Japanese.",
   "先生……ホークラックスについて、教えていただけますか？もちろん、純粋な学問的興味からです。図書館では詳しいことが分からなくて。先生ほど博識な方なら、きっとご存知だと思いまして。ほんの少しだけで構いません。"),
 'snape':("A man around forty, deep, slow, dry and cold baritone, speaking almost under his breath, controlled, with hidden grief, speaking Japanese.",
   "アバダ ケダブラ。……私は、約束を果たしただけだ。誰にも理解されなくて構わない。それが、私の選んだ道なのだから。後悔などしていない。少なくとも、そう自分に言い聞かせている。さあ、行くぞ、ドラコ。急げ。"),
}
def go(n):
    d,t=V[n]
    r=requests.post('https://api.elevenlabs.io/v1/text-to-voice/design',headers={'xi-api-key':K},json={'voice_description':d,'model_id':'eleven_ttv_v3','text':t,'auto_generate_text':False},timeout=180)
    if r.status_code!=200: print(n,r.status_code,r.text[:300]); return
    ids=[]
    for i,p in enumerate(r.json()['previews']):
        open(f'audio/voices/{n}_p{i}.mp3','wb').write(base64.b64decode(p['audio_base_64'])); ids.append(p['generated_voice_id'])
    json.dump(ids,open(f'audio/voices/{n}_ids.json','w')); print('ok',n,len(ids))
if __name__=='__main__':
    for n in V: assert len(V[n][1])>=100,(n,len(V[n][1]))
    with cf.ThreadPoolExecutor(3) as ex: list(ex.map(go, sys.argv[1:] or list(V)))
