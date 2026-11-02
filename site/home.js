/* Native continuous scroll into a separately addressable article. No scroll interception. */
(() => {
  const surface=document.querySelector('[data-article-surface]'),root=surface.querySelector('#main-article');
  const homeURL=SitePaths.url('index.html'),articleURL=SitePaths.url('article.html');
  const homeTitle=document.title,postTitle=surface.querySelector('h1').textContent+' · SteerDistill';
  let inArticle=false,pending=false;
  const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){ResearchArticle.mount(root);observer.disconnect()}},{rootMargin:'900px 0px'});
  observer.observe(surface);
  // Existing published index.html#section links continue to resolve to the independent post.
  const articleIDs=['article-start','problem','method','learning','guidance','recovery','results','resources','notes'];
  if(articleIDs.includes(location.hash.slice(1))){location.replace(articleURL+location.hash);return}
  function update(){
    pending=false;
    const next=surface.getBoundingClientRect().top<=document.querySelector('.site-header').offsetHeight+30;
    if(next===inArticle)return;
    inArticle=next;
    // Passive scrolling updates the address without adding history entries. Explicit links remain normal navigation.
    const hash=location.hash;
    const target=next?articleURL+((articleIDs.includes(hash.slice(1))||hash.startsWith('#note-'))?hash:''):homeURL;
    history.replaceState({...history.state,continuousArticle:next},'',target);
    document.title=next?postTitle:homeTitle;SiteShell.current(next?'article':'home');
  }
  addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(update)}},{passive:true});
  addEventListener('pageshow',update);
  document.addEventListener('article:ready',update);
})();
