/* Shared helpers: data loading and per-browser progress (localStorage, best effort). */
const KEY = 'aifs-progress-v1';
export function loadProgress() {
  try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; }
}
export function saveProgress(p) {
  try { localStorage.setItem(KEY, JSON.stringify(p)); } catch { /* private mode: progress just isn't kept */ }
}
export function lessonState(p, id) {
  p[id] = p[id] || { quiz: {}, solved: {}, code: {}, watched: false };
  return p[id];
}
/* a lesson is done when every quiz question is answered correctly and every problem passes */
export function lessonScore(st, lesson) {
  const q = lesson ? lesson.quiz.length : 0, pr = lesson ? lesson.problems.length : 0;
  const qr = st ? Object.values(st.quiz).filter(a => a.correct).length : 0;
  const ps = st ? Object.values(st.solved).filter(Boolean).length : 0;
  return { done: qr + ps, total: q + pr, complete: lesson && qr === q && ps === pr };
}
export async function getJSON(url) {
  const r = await fetch(url, { cache: 'no-cache' });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.json();
}
export function h(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const k in attrs || {}) {
    if (k === 'class') e.className = attrs[k];
    else if (k === 'html') e.innerHTML = attrs[k];
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), attrs[k]);
    else if (attrs[k] != null && attrs[k] !== false) e.setAttribute(k, attrs[k]);
  }
  for (const c of kids.flat()) if (c != null) e.append(c);
  return e;
}
export function allLessons(course) {
  return course.modules.flatMap(m => m.lessons.map(l => ({ ...l, module: m })));
}
