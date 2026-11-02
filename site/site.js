/* Global navigation/theme behavior; shared by landing, article, cases and records. */
window.SiteShell = (() => {
  const header = document.querySelector('.site-header');
  const button = header.querySelector('.site-theme');
  function theme(dark, save = false) {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    button.setAttribute('aria-pressed', String(dark));
    button.setAttribute('aria-label', dark ? '切换浅色主题' : '切换深色主题');
    if (save) try { localStorage.setItem('steerdistill-theme', dark ? 'dark' : 'light'); } catch {}
  }
  function current(page) {
    header.dataset.page = page;
    header.querySelectorAll('[data-nav]').forEach(a => {
      if (a.dataset.nav === page) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }
  button.addEventListener('click', () => theme(document.documentElement.dataset.theme !== 'dark', true));
  addEventListener('storage', e => { if (e.key === 'steerdistill-theme') theme(e.newValue === 'dark'); });
  theme(document.documentElement.dataset.theme === 'dark');
  current(document.body.dataset.page);
  return { current };
})();
