import os, sys, base64, requests, concurrent.futures as cf
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY']}
MODEL='gpt-image-2.5-sunburst-2026-09-08'
STYLE=("Dark seinen anime character model sheet, in the style of a mature hand-drawn TV anime: crisp ink linework, hard two-tone cel shading with deep "
       "ink-black shadows, slightly desaturated palette, subtle film grain. Plain dark slate-grey studio background. Layout left to right: full-body front view, "
       "full-body three-quarter view, full-body back view, and on the right two large head close-ups (neutral, and one strong expression). "
       "Same character, same outfit and proportions in every view. No text, no labels, no logos, no watermark. Original character design, not based on any actor. ")
CHARS={
 'harry':"A sixteen-year-old boy at an old British boarding school, slight and wiry, a little short for his age. Messy jet-black hair that sticks up at the back. Vivid green eyes behind round thin-framed glasses with a small taped repair. A faint thin zig-zag scar on his forehead, mostly under his fringe. Long black school gown over a white shirt and grey jumper, a red-and-gold striped tie loosened, a slim wooden wand in one hand. Expression close-up: tense, determined, jaw set.",
 'dumbledore':"A very old, very tall and thin wizard of about one hundred and fifteen. Silver-white hair and a silver beard so long it could be tucked into his belt. Half-moon spectacles perched on a long, crooked nose that looks as if it has been broken at least twice. Bright, piercing light-blue eyes that twinkle. Long, elegant fingers. Flowing deep-purple velvet robes with a high collar and a travelling cloak, buckled boots. His RIGHT hand is blackened and shrivelled, dead-looking and burnt to the wrist, and on that hand he wears a heavy, ugly gold ring set with a cracked black stone. Expression close-up: grave and weary, with quiet kindness.",
 'snape':"A gaunt schoolmaster in his late thirties with sallow, pale skin and a large hooked nose. Lank shoulder-length black hair hanging around his face. Flat, cold dark eyes, a thin unsmiling mouth. A severe all-black high-collared coat with many small buttons and a long black cloak, a dark wand. Expression close-up: a cold sneer, with a trace of hidden sorrow.",
 'draco':"A sixteen-year-old pureblood schoolboy wizard with a pale, pointed face and sleek white-blonde hair. Cold grey eyes. This year he looks ill: thinner, skin with a greyish tinge, dark shadows under his eyes, haunted and sleepless, the arrogance worn down into fear. Immaculate black school robes with a silver-and-green striped tie, an expensive silver-buttoned waistcoat, left sleeve hiding his forearm. Expression close-up: desperate, eyes wet, on the edge of breaking.",
 'slughorn':"An enormously fat old wizard with a great round belly straining against his waistcoat. Completely bald, shiny head. A huge silver-white walrus moustache. Pale, protruding gooseberry-green eyes. Small, plump hands with several gold rings. A rich emerald-green velvet smoking jacket with gold frogging, a straining waistcoat with gold buttons and a watch chain, maroon velvet slippers. Jovial and vain, a collector of famous students. Expression close-up: sweating, frightened and guilty.",
 'narcissa':"A tall, slim aristocratic witch in her forties, pale skin, long straight pale blonde hair, cold light-blue eyes. Beautiful, but with an expression as if there were a nasty smell under her nose. A long black hooded travelling cloak over a fitted high-necked black gown, a thin silver chain. Expression close-up: desperate, pleading, eyes glistening.",
 'bellatrix':"A tall witch in her mid-forties with heavy-lidded dark eyes and a thick mane of glossy, wild black hair. Once beautiful, now gaunt and hollow-cheeked from years in a prison, skin pale and stretched over sharp cheekbones. A tattered black corseted dress and long black cloak, a curved dark wand. Fanatical and unhinged. Expression close-up: a wide, manic, mocking grin.",
 'riddle':"An eleven-year-old orphan boy in 1930s London, tall for his age, pale, strikingly handsome, with neat dark hair and dark eyes. A threadbare grey orphanage jumper over a collared shirt, grey short trousers, grey socks and scuffed black shoes. Unnervingly calm and self-possessed, too still for a child. Expression close-up: a faint, cold, knowing smile.",
}
def gen(name):
    r=requests.post('https://api.openai.com/v1/images/generations',headers=H,json={'model':MODEL,'prompt':STYLE+CHARS[name],'size':'1536x1024'},timeout=400)
    if r.status_code!=200: print(name,r.status_code,r.text[:400]); return
    open(f'characters/{name}.png','wb').write(base64.b64decode(r.json()['data'][0]['b64_json'])); print('ok',name, r.json().get('usage',''))
if __name__=='__main__':
    with cf.ThreadPoolExecutor(8) as ex: list(ex.map(gen, sys.argv[1:] or list(CHARS)))
