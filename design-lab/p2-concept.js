(() => {
  'use strict';
  const root = document.querySelector('[data-concept-motion]');
  if (!root) return;
  let captions = [
    '对齐环境状态，找到行为分歧。',
    'Teacher 给出指导，student 执行并接受核验。',
    '把修正蒸馏进量化模型，推理时独立执行。'
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
    control.textContent = playing ? '暂停 Ⅱ' : '播放 ▷';
    control.setAttribute('aria-pressed', String(playing));
    control.setAttribute('aria-label', playing ? '暂停方法动效' : '播放方法动效');
  }
  document.addEventListener('article:ready', event => { if(event.detail?.hero?.conceptCaptions){captions=event.detail.hero.conceptCaptions;render();} });
  control.addEventListener('click', () => { playing = !playing; render(); });
  reduced.addEventListener('change', () => { if (reduced.matches) { playing = false; render(); } });
  const observer = new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    root.classList.toggle('is-offscreen', !visible);
  });
  observer.observe(root);
  const timer = setInterval(() => {
    if (playing && visible && !document.hidden) { stage = (stage + 1) % captions.length; render(); }
  }, 3600);
  window.addEventListener('pagehide', () => { clearInterval(timer); observer.disconnect(); }, { once: true });
  render();
})();
