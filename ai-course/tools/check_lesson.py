"""Check a lesson's problems: every solution passes all tests, every starter fails at least one.

python tools/check_lesson.py lessons/<id>
"""
import json, sys, os, traceback

def run(code, tests):
    results = []
    for t in tests:
        ns = {}
        try:
            exec(code, ns)
            exec(t['code'], ns)
            results.append((t['name'], True, ''))
        except Exception as e:
            results.append((t['name'], False, f'{type(e).__name__}: {e}'))
    return results

lesson = json.load(open(os.path.join(sys.argv[1], 'lesson.json')))
ok = True
for q in lesson['quiz']:
    assert 0 <= q['answer'] < len(q['options']), q['q']
for p in lesson['problems']:
    sol = run(p['solution'], p['tests'])
    st = run(p['starter'], p['tests'])
    bad = [r for r in sol if not r[1]]
    if bad: ok = False; print('SOLUTION FAILS', p['id'], bad)
    if all(r[1] for r in st): ok = False; print('STARTER PASSES EVERYTHING', p['id'])
    print(f"{p['id']}: solution {sum(r[1] for r in sol)}/{len(sol)}, starter {sum(r[1] for r in st)}/{len(st)}")
print('OK' if ok else 'PROBLEMS FOUND'); sys.exit(0 if ok else 1)
