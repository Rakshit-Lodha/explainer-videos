"""Sarvam (Ratan) takes, one per scene: python tools/tts.py <lesson_dir> [s1 s3 ...]"""
import json, base64, os, sys, requests
from dotenv import load_dotenv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT, '.env'))
key = os.environ.get('SARVAM_API_KEY')
if not key: sys.exit('SARVAM_API_KEY is not set (add it to .env or the environment settings)')
lesson = os.path.abspath(sys.argv[1]); only = sys.argv[2:]
os.makedirs(os.path.join(lesson, 'audio'), exist_ok=True)
for s in json.load(open(os.path.join(lesson, 'narration.json'))):
    if only and s['id'] not in only: continue
    r = requests.post('https://api.sarvam.ai/text-to-speech', headers={'api-subscription-key': key}, json={
        'text': s['text'], 'target_language_code': 'en-IN', 'speaker': 'ratan', 'model': 'bulbul:v3',
        'pace': s['pace'], 'temperature': s['temperature']}, timeout=120)
    if r.status_code != 200: print(s['id'], r.status_code, r.text[:300]); continue
    open(os.path.join(lesson, 'audio', s['id'] + '.wav'), 'wb').write(base64.b64decode(r.json()['audios'][0]))
    print('ok', s['id'])
