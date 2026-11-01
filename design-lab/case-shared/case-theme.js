/* Common sun/moon control; keep the existing persistent theme preference. */
window.CaseTheme=(()=>{
 const key='steerdistill-theme',mounted=new WeakSet();
 function icon(kind){
  const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('aria-hidden','true');svg.classList.add('theme-'+kind);
  const path=document.createElementNS(ns,'path');path.setAttribute('d',kind==='moon'?'M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7Z':'M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5');
  if(kind==='sun'){const circle=document.createElementNS(ns,'circle');circle.setAttribute('cx','12');circle.setAttribute('cy','12');circle.setAttribute('r','4');svg.append(circle)}svg.append(path);return svg;
 }
 function set(dark){
  document.documentElement.dataset.theme=dark?'dark':'light';
  document.querySelectorAll('.case-theme').forEach(button=>{button.setAttribute('aria-pressed',String(dark));button.setAttribute('aria-label',dark?'切换浅色主题':'切换深色主题')});
  try{localStorage.setItem(key,dark?'dark':'light')}catch{}
 }
 function mount(button){
  if(!button||mounted.has(button))return;mounted.add(button);button.classList.add('case-theme');button.type='button';button.replaceChildren(icon('moon'),icon('sun'));button.onclick=()=>set(document.documentElement.dataset.theme!=='dark');set(document.documentElement.dataset.theme==='dark');
 }
 document.querySelectorAll('.case-site .case-header-inner .theme-toggle,.case-site .case-header-inner .reading-theme').forEach(mount);
 return {mount,set};
})();
