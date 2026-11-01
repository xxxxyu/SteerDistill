(() => {
  'use strict';
  const toggle = document.querySelector('.reading-theme');
  const themeRoot = document.documentElement;
  function setTheme(theme, save = false) {
    themeRoot.dataset.theme = theme;
    const dark = theme === 'dark';
    toggle.setAttribute('aria-pressed', String(dark));
    toggle.setAttribute('aria-label', dark ? '切换浅色主题' : '切换深色主题');
    toggle.title = dark ? '浅色主题' : '深色主题';
    if (save) { try { localStorage.setItem('steerdistill-theme', theme); } catch {} }
  }
  setTheme(themeRoot.dataset.theme || 'light');
  toggle.addEventListener('click', () => setTheme(themeRoot.dataset.theme === 'dark' ? 'light' : 'dark', true));
  let scheduled = false;
  function updateCurrent() {
    scheduled = false;
    const links = [...document.querySelectorAll('.reading-header nav a')];
    const sections = links.map(link => document.getElementById(new URL(link.href).hash.slice(1)));
    const headerBottom = document.querySelector('.reading-header').getBoundingClientRect().bottom;
    let current = -1;
    sections.forEach((section, index) => { if (section && section.getBoundingClientRect().top <= headerBottom + 130) current = index; });
    links.forEach((link, index) => {
      if (index === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateCurrent); } }, { passive: true });
  addEventListener('resize', updateCurrent);
  document.addEventListener('article:ready', updateCurrent);
  updateCurrent();
  const chart = document.querySelector('[data-press-chart]');
  if (chart) {
    chart.classList.add('chart-motion-ready');
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) { chart.classList.add('bars-playing'); observer.disconnect(); }
    }, { threshold: .12 });
    observer.observe(chart);
  }
})();
