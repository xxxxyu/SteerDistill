(() => {
  'use strict';
  const root = document.querySelector('[data-concept-motion]');
  if (!root) return;
  let captions = [
    'Align environment states to locate behavioral divergence.',
    'Teacher guidance is tested through student execution.',
    'Distill corrections; act independently at inference.'
  ];
  const control = root.querySelector('[data-concept-play]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let stage = 0;
  let playing = !reduced.matches;
  let visible = true;
  function render() {
    root.dataset.stage = stage;
    root.classList.toggle('is-paused', !playing);
    root.querySelector('[data-concept-caption]').textContent = captions[stage];
    control.textContent = playing ? 'Pause Ⅱ' : 'Play ▷';
    control.setAttribute('aria-pressed', String(playing));
    control.setAttribute('aria-label', playing ? 'Pause method animation' : 'Play method animation');
  }
  control.addEventListener('click', () => { playing = !playing; render(); });
  reduced.addEventListener('change', () => { if (reduced.matches) { playing = false; render(); } });
  const observer = new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    root.classList.toggle('is-offscreen', !visible);
  });
  observer.observe(root);
  let timer;
  function start() {
    clearInterval(timer);
    observer.observe(root);
    timer = setInterval(() => {
      if (playing && visible && !document.hidden) { stage = (stage + 1) % captions.length; render(); }
    }, 3600);
  }
  start();
  window.addEventListener('pagehide', () => { clearInterval(timer); observer.disconnect(); });
  window.addEventListener('pageshow', start);
  render();
})();
