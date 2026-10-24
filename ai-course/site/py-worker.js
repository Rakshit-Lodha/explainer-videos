/* Runs learner code against a problem's tests in Pyodide, off the main thread.
   The page terminates and restarts this worker when a run takes too long (infinite loops). */
importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js');

const RUNNER = `
import sys, io, json, traceback

def _first_line_in(tb, fname):
    for f in reversed(traceback.extract_tb(tb)):
        if f.filename == fname:
            return f.lineno
    return None

def _run(code, tests):
    out = []
    for t in tests:
        ns = {'__name__': '__main__'}
        buf, old = io.StringIO(), sys.stdout
        sys.stdout = buf
        ok, msg = True, ''
        try:
            exec(compile(code, 'solution.py', 'exec'), ns)
            exec(compile(t['code'], 'test', 'exec'), ns)
        except SyntaxError as e:
            ok, msg = False, f'SyntaxError: {e.msg} (line {e.lineno} of your code)'
        except AssertionError as e:
            ok, msg = False, str(e) or 'a check failed'
        except Exception as e:
            line = _first_line_in(e.__traceback__, 'solution.py')
            ok, msg = False, f'{type(e).__name__}: {e}' + (f' (line {line} of your code)' if line else '')
        finally:
            sys.stdout = old
        out.append({'name': t['name'], 'ok': ok, 'msg': msg, 'stdout': buf.getvalue()[:2000]})
    return json.dumps(out)
`;

let ready = null;
async function boot() {
  const py = await loadPyodide();
  py.runPython(RUNNER);
  return py;
}

self.onmessage = async ({ data }) => {
  try {
    if (!ready) { postMessage({ type: 'status', text: 'Loading Python (first run takes a few seconds)…' }); ready = boot(); }
    const py = await ready;
    if (/\b(import|from)\s+numpy\b/.test(data.code + data.tests.map(t => t.code).join('\n'))) {
      postMessage({ type: 'status', text: 'Loading NumPy…' });
      await py.loadPackage('numpy');
      if (!py.loadedPackages.numpy) throw new Error('Could not load NumPy. Check your connection and try again.');
    }
    postMessage({ type: 'status', text: 'Running tests…' });
    py.globals.set('_code', data.code);
    py.globals.set('_tests', py.toPy(data.tests));
    const res = JSON.parse(py.runPython('_run(_code, _tests)'));
    postMessage({ type: 'result', id: data.id, results: res });
  } catch (e) {
    postMessage({ type: 'error', id: data.id, text: String(e && e.message || e) });
  }
};
