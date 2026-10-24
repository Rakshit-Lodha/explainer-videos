import os, sys, base64, requests
from dotenv import load_dotenv
load_dotenv('../.env')
H={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY']}
def gen(name,prompt,size='1024x1536'):
    r=requests.post('https://api.openai.com/v1/images/generations',headers=H,json={'model':'gpt-image-2.5-sunburst-2026-09-08','prompt':prompt,'size':size},timeout=300)
    if r.status_code!=200: print(name,r.status_code,r.text[:400]); return
    open(f'keyframes/{name}.png','wb').write(base64.b64decode(r.json()['data'][0]['b64_json'])); print('ok',name)
STYLE="Flat vector illustration, dark navy background (#0a1020), warm amber glow (#f5b942), teal accents (#4fd1c5), soft bloom, minimal clean shapes, no text, no people faces, calm modern explainer style, vertical 9:16 composition."
gen('ref_style',STYLE+" Style reference sheet: a glowing waveform, a row of small glowing token blocks, a neural-network node graph with thin teal lines, a decoder funnel, a simple glowing speech bubble. Arranged on a grid with generous space.")
gen('s1_prompt',STYLE+" A softly glowing empty text-input bar near the middle of the frame with a blinking cursor, and a gentle amber waveform blooming above it like light rising from the bar, a few faint musical-note shapes drifting in the dark, empty upper third of the frame for captions, a thin horizontal ground line.")
