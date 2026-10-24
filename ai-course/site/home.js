import { loadProgress, lessonScore, getJSON, h, allLessons } from './common.js';

const course = await getJSON('data/course.json');
const prog = loadProgress();
const ready = allLessons(course).filter(l => l.id);
const lessons = Object.fromEntries(await Promise.all(ready.map(async l => [l.id, await getJSON(`data/lessons/${l.id}.json`)])));

let done = 0, total = 0, next = null;
const root = document.getElementById('modules');
root.textContent = '';
for (const m of course.modules) {
  const ul = h('ul', { class: 'lessons' });
  for (const l of m.lessons) {
    if (!l.id) {
      ul.append(h('li', { class: 'soon' }, h('span', { class: 'num' }, l.num), h('span', { class: 't' }, l.title), h('span', { class: 'pill' }, 'soon')));
      continue;
    }
    const sc = lessonScore(prog[l.id], lessons[l.id]);
    done += sc.done; total += sc.total;
    if (!sc.complete && !next) next = l;
    const href = `lesson.html?id=${encodeURIComponent(l.id)}`;
    const pill = sc.complete ? h('span', { class: 'pill done' }, '✓ done')
      : sc.done ? h('span', { class: 'pill go' }, `${sc.done}/${sc.total}`) : h('span', { class: 'pill go' }, 'start');
    ul.append(h('li', { class: 'ready', onclick: () => location.href = href },
      h('span', { class: 'num' }, l.num), h('span', { class: 't' }, h('a', { href }, l.title)), pill));
  }
  root.append(h('section', { class: 'module' }, h('h2', {}, h('span', { class: 'n' }, `Module ${m.n}`), m.title), ul));
}
const all = allLessons(course).length;
document.getElementById('count').textContent = `${ready.length} of ${all} lessons ready`;
const pct = total ? Math.round(100 * done / total) : 0;
document.getElementById('pct').textContent = `${pct}% of available work complete`;
document.getElementById('bar').style.width = pct + '%';
if (next) document.getElementById('resume').append(h('a', { href: `lesson.html?id=${encodeURIComponent(next.id)}` }, `Continue: ${next.num} →`));
