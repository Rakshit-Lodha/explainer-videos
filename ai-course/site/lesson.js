import { loadProgress, saveProgress, lessonState, lessonScore, getJSON, h, allLessons } from './common.js';

const id = new URLSearchParams(location.search).get('id');
const main = document.getElementById('main');
const course = await getJSON('data/course.json');
const order = allLessons(course).filter(l => l.id);
const meta = order.find(l => l.id === id);
if (!meta) {
  main.innerHTML = '';
  main.append(h('h1', {}, 'Lesson not found'), h('p', {}, h('a', { href: './' }, '← Back to the course')));
  throw new Error('unknown lesson ' + id);
}
const L = await getJSON(`data/lessons/${id}.json`);
const prog = loadProgress();
const st = lessonState(prog, id);
const save = () => { saveProgress(prog); updateHeader(); };
document.title = `${meta.num} ${L.title} · AI from Scratch`;

function updateHeader() {
  const sc = lessonScore(st, L);
  document.getElementById('lprog').textContent = sc.complete ? 'lesson complete ✓' : `${sc.done} / ${sc.total} done`;
}

main.textContent = '';
main.append(
  h('div', { class: 'crumbs' }, h('a', { href: './' }, 'Course'), ` / Module ${meta.module.n}: ${meta.module.title} / ${meta.num}`),
  h('h1', {}, L.title),
  h('p', { class: 'lede' }, L.summary),
);

/* video */
const vbox = h('div', { class: 'video' });
if (L.video) {
  const v = h('video', { controls: '', preload: 'metadata', playsinline: '', src: L.video, poster: L.poster });
  v.addEventListener('ended', () => { st.watched = true; save(); });
  vbox.append(v);
} else vbox.append(h('div', { class: 'none' }, 'The video for this lesson is still being rendered.'));
main.append(vbox);

main.append(h('h2', {}, 'Key ideas'), h('ul', { class: 'ideas' }, L.key_ideas.map(k => h('li', {}, k))));
if (L.llm_link) main.append(h('div', { class: 'callout' }, h('b', {}, 'Why it matters for language models. '), L.llm_link));

/* quiz */
main.append(h('h2', {}, 'Quiz'));
L.quiz.forEach((q, qi) => {
  const box = h('div', { class: 'q' }, h('div', { class: 'qn' }, `Question ${qi + 1} of ${L.quiz.length}`), h('div', {}, q.q));
  const opts = h('div', { class: 'opts' });
  const explain = h('div', { class: 'explain' });
  const buttons = q.options.map((o, oi) => h('button', { class: 'opt', type: 'button', onclick: () => answer(oi) }, o));
  opts.append(...buttons);
  box.append(opts, explain);
  function render(chosen) {
    buttons.forEach((b, i) => {
      b.disabled = true;
      b.classList.toggle('right', i === q.answer);
      b.classList.toggle('wrong', i === chosen && chosen !== q.answer);
    });
    explain.textContent = '';
    explain.append(h('b', {}, chosen === q.answer ? 'Right. ' : 'Not quite. '), q.explain, ' ');
    if (chosen !== q.answer) explain.append(h('button', { class: 'btn', type: 'button', onclick: reset }, 'Try again'));
  }
  function reset() {
    delete st.quiz[qi]; save();
    buttons.forEach(b => { b.disabled = false; b.classList.remove('right', 'wrong'); });
    explain.textContent = '';
  }
  function answer(oi) { st.quiz[qi] = { chosen: oi, correct: oi === q.answer }; save(); render(oi); }
  if (st.quiz[qi]) render(st.quiz[qi].chosen);
  main.append(box);
});

/* problems */
let worker = null, pending = null;
function getWorker() {
  if (!worker) {
    worker = new Worker('py-worker.js');
    worker.onmessage = ({ data }) => { if (pending) pending(data); };
    worker.onerror = e => { e.preventDefault(); worker = null; if (pending) pending({ type: 'error', text: 'Could not load the Python runtime (Pyodide). Check your connection and try again.' }); };
  }
  return worker;
}
function runTests(code, tests, onStatus) {
  return new Promise(resolve => {
    let timer = null;
    const arm = ms => { clearTimeout(timer); timer = setTimeout(() => { worker.terminate(); worker = null; pending = null; resolve({ type: 'error', text: `Stopped after ${ms / 1000} s. Is there a loop that never ends?` }); }, ms); };
    pending = data => {
      if (data.type === 'status') { onStatus(data.text); arm(data.text.startsWith('Running') ? 10000 : 90000); return; }
      clearTimeout(timer); pending = null; resolve(data);
    };
    arm(90000);
    getWorker().postMessage({ id: Date.now(), code, tests });
  });
}

main.append(h('h2', {}, 'Code'));
L.problems.forEach(p => {
  const key = p.id;
  const box = h('div', { class: 'prob' });
  const title = h('h3', {}, p.title);
  const ta = h('textarea', { spellcheck: 'false', 'aria-label': `Code for ${p.title}` });
  ta.value = st.code[key] ?? p.starter;
  const ed = h('div', { class: 'editor' }, ta);
  const runBtn = h('button', { class: 'btn primary', type: 'button' }, 'Run tests');
  const hintBtn = h('button', { class: 'btn', type: 'button' }, 'Hint');
  const resetBtn = h('button', { class: 'btn', type: 'button' }, 'Reset code');
  const status = h('span', { class: 'status' });
  const results = h('ul', { class: 'results' });
  const hints = h('ol', { class: 'hints' });
  const sol = h('details', { class: 'sol', hidden: '' }, h('summary', {}, 'Show a solution'), h('pre', {}, p.solution));
  box.append(title, h('div', { html: p.prompt }), ed, h('div', { class: 'row' }, runBtn, hintBtn, resetBtn, status), results, hints, sol);
  main.append(box);

  let cm = null;
  if (window.CodeMirror) {
    cm = CodeMirror.fromTextArea(ta, { mode: 'python', theme: 'material-darker', lineNumbers: true, indentUnit: 4, viewportMargin: Infinity,
      extraKeys: { Tab: c => c.somethingSelected() ? c.indentSelection('add') : c.replaceSelection('    '), 'Ctrl-Enter': () => run(), 'Cmd-Enter': () => run() } });
  } else {
    ta.addEventListener('keydown', e => { if (e.key === 'Tab') { e.preventDefault(); ta.setRangeText('    ', ta.selectionStart, ta.selectionEnd, 'end'); } });
  }
  const getCode = () => cm ? cm.getValue() : ta.value;
  const setCode = v => cm ? cm.setValue(v) : (ta.value = v);
  let saveT = null;
  const onEdit = () => { clearTimeout(saveT); saveT = setTimeout(() => { st.code[key] = getCode(); saveProgress(prog); }, 400); };
  cm ? cm.on('change', onEdit) : ta.addEventListener('input', onEdit);

  const mark = () => { title.querySelector('.ok')?.remove(); if (st.solved[key]) title.append(h('span', { class: 'ok' }, '✓ solved')); };
  mark();
  let failures = 0, shown = 0;
  if (st.solved[key]) sol.hidden = false;

  async function run() {
    runBtn.disabled = true; results.textContent = ''; status.textContent = 'Starting…';
    const res = await runTests(getCode(), p.tests, t => status.textContent = t);
    runBtn.disabled = false;
    if (res.type === 'error') { status.textContent = res.text; return; }
    const passed = res.results.filter(r => r.ok).length;
    status.textContent = passed === res.results.length ? `All ${passed} tests pass.` : `${passed} of ${res.results.length} tests pass.`;
    for (const r of res.results) {
      const li = h('li', { class: r.ok ? 'pass' : 'fail' }, h('span', { class: 'mk' }, r.ok ? '✓' : '✗'), h('span', {}, r.name));
      if (!r.ok && r.msg) li.append(h('span', { class: 'msg' }, r.msg));
      if (r.stdout) li.append(h('span', { class: 'msg' }, 'printed: ' + r.stdout.trim()));
      results.append(li);
    }
    if (passed === res.results.length) { st.solved[key] = true; sol.hidden = false; }
    else if (++failures >= 2) sol.hidden = false;   // a solution is offered after two failed runs
    st.code[key] = getCode(); save(); mark();
  }
  runBtn.onclick = run;
  hintBtn.onclick = () => {
    if (shown < p.hints.length) hints.append(h('li', {}, p.hints[shown++]));
    if (shown >= p.hints.length) hintBtn.disabled = true;
  };
  resetBtn.onclick = () => { if (confirm('Replace your code with the starter code?')) { setCode(p.starter); delete st.code[key]; saveProgress(prog); } };
});

/* previous / next */
const i = order.findIndex(l => l.id === id);
const pn = h('nav', { class: 'pn' });
pn.append(i > 0 ? h('a', { href: `lesson.html?id=${order[i - 1].id}` }, `← ${order[i - 1].num} ${order[i - 1].title}`) : h('a', { href: './' }, '← All lessons'));
pn.append(i < order.length - 1 ? h('a', { href: `lesson.html?id=${order[i + 1].id}` }, `${order[i + 1].num} ${order[i + 1].title} →`) : h('span', { class: 'muted' }, 'More lessons soon'));
main.append(pn);
updateHeader();
