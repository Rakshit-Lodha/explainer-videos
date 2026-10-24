import os, sys, base64, requests
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY']}
MODEL='gpt-image-2.5-sunburst-2026-09-08'
def save(name,r):
    if r.status_code!=200: print(name,r.status_code,r.text[:400]); return
    open(f'keyframes/{name}.png','wb').write(base64.b64decode(r.json()['data'][0]['b64_json'])); print('ok',name)
def gen(name,prompt,size='1024x1536'):
    save(name,requests.post('https://api.openai.com/v1/images/generations',headers=H,json={'model':MODEL,'prompt':prompt,'size':size},timeout=300))
def edit(name,prompt,refs,size='1024x1536'):
    """Scene keyframe conditioned on reference images (consistency)."""
    files=[('image[]',(os.path.basename(p),open(p,'rb'),'image/png')) for p in refs]
    save(name,requests.post('https://api.openai.com/v1/images/edits',headers=H,data={'model':MODEL,'prompt':prompt,'size':size},files=files,timeout=300))
STYLE="Flat vector illustration, dark navy background (#0a1020), warm amber glow (#f5b942), teal accents (#4fd1c5), soft bloom, minimal clean shapes, no text, calm modern explainer style, vertical 9:16 composition."
EXPLORER="The Explorer: a small slender figure in a long teal (#4fd1c5) coat with a high collar and a soft hood down, dark navy trousers and boots, a plain faceless rounded head in shadow, carrying a small round amber (#f5b942) glowing lantern in the right hand. Same proportions and silhouette every time."
if __name__=='__main__':
    which=sys.argv[1:] or ['ref_style','ref_explorer']
    if 'ref_style' in which:
        gen('ref_style',STYLE+" Style reference sheet for an explainer about doing great work, arranged on a clean grid with generous space: four small environment swatches (a dark shoreline at dusk with a calm sea, a small sailboat on water, a tall mountain whose far edge breaks into a jagged fractal outline with thin teal light leaking from small cracks, a high peak at dawn with a glowing bud of light on the horizon), plus a few small props: an amber lantern, a thin teal bridge, a sprout growing into a tree.")
    if 'ref_explorer' in which:
        gen('ref_explorer',STYLE+" Character reference sheet, plain navy background, four poses of the same character in a row: front view, side view, back view, and a close-up of the lantern in hand. "+EXPLORER)
