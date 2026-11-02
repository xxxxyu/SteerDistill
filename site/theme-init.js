/* Runs before styles: all pages share one persisted preference. */
try { document.documentElement.dataset.theme = localStorage.getItem('steerdistill-theme') === 'dark' ? 'dark' : 'light'; }
catch { document.documentElement.dataset.theme = 'light'; }
