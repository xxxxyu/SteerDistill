(async()=>{
 'use strict';
 const U=EvidenceUI,root=document.querySelector('#main-article');
 const articleURL=new URL('design-lab/main-article.zh.json',document.baseURI),caseURL=new URL('design-lab/article-content/cases.zh.json',document.baseURI);
 const pageHash=id=>new URL('index.html#'+id,document.baseURI).href;
 const make=(tag,cls,value)=>U.make(tag,cls,value);
 function prose(section){const node=make('div','main-prose');section.append(node);return node}
 function methodDiagram(block){
  const figure=make('figure','method-diagram'),title=make('h3','',block.title),list=make('ol','method-path');
  for(const step of block.steps){const item=make('li'),heading=make('h4','',step.title),copy=make('p','',step.text);item.append(heading,copy);list.append(item)}
  figure.append(title,list);
  if(Number.isInteger(block.retryFrom)&&Number.isInteger(block.retryTo)){
   const loop=make('div','method-retry');loop.setAttribute('aria-label','核验未通过时，将反馈返回 Teacher 并重试');
   loop.innerHTML='<svg viewBox="0 0 400 52" role="img" aria-label="核验未通过时反馈并重试"><defs><marker id="method-retry-head" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M1 1L7 4L1 7"/></marker></defs><path d="M300 2V23H100V2" marker-end="url(#method-retry-head)"/><text x="200" y="47" text-anchor="middle">核验未通过</text></svg>';figure.append(loop);
  }
  return figure;
 }
 function targetDiagram(block){
  const figure=make('figure','target-diagram'),title=make('h3','',block.title),layout=make('div','target-layout'),sources=make('div','target-sources');
  for(const row of block.rows){const item=make('div','target-row'),when=make('p','target-when',row.when),source=make('p','target-source',row.source),loss=make('span','target-loss',row.loss);source.append(loss);item.append(when,source);sources.append(item)}
  const merge=make('div','target-merge');merge.setAttribute('aria-hidden','true');merge.innerHTML='<svg viewBox="0 0 60 160"><path d="M0 30H28V80H55M0 130H28V80M48 73L55 80L48 87"/></svg>';
  const learner=make('div','target-learner');learner.append(make('p','target-name',block.learner),make('p','target-input',block.learnerInput));layout.append(sources,merge,learner);figure.append(title,layout);return figure;
 }
 function applyHero(data){
  document.title=data.paperTitle;const heading=document.querySelector('.paper-identity h1');heading.setAttribute('aria-label',data.paperTitle);
  const subtitle=data.paperTitle.replace(/^SteerDistill:\s*/,''),parts=subtitle.split(' via '),title=document.querySelector('.paper-full-title');title.replaceChildren(document.createTextNode(parts[0]));if(parts.length>1){title.append(make('br','title-break'),document.createTextNode(' via '+parts.slice(1).join(' via ')))}
  const hero=data.hero,tldr=document.querySelector('.paper-tldr');tldr.replaceChildren(make('strong','','TL;DR'),document.createTextNode(' '+hero.tldr));
  const nav=document.querySelector('.reading-header nav');nav.replaceChildren();for(const item of hero.nav){const a=make('a','',item.label);a.href=pageHash(item.id);nav.append(a)}
  const links=document.querySelector('.paper-resources');links.replaceChildren();for(const item of hero.links){const a=make('a','',item.label);a.href=new URL(item.href,document.baseURI);links.append(a)}
  const notes=document.querySelector('.paper-author-notes');notes.replaceChildren(make('span','','* '+hero.authorNotes.equal),make('span','','‡ '+hero.authorNotes.lead));
  document.querySelector('.press-figure-head strong').textContent=hero.benchmarkTitle;
  const caption=document.querySelector('.press-caption>a');caption.textContent=hero.benchmarkCaptionLink.label;caption.href=hero.benchmarkCaptionLink.href.startsWith('#')?pageHash(hero.benchmarkCaptionLink.href.slice(1)):new URL(hero.benchmarkCaptionLink.href,document.baseURI);
  document.querySelectorAll('.concept-motion svg>text').forEach((node,i)=>{node.textContent=hero.conceptLabels[i]});document.querySelector('.concept-foot>a').textContent=hero.conceptMethodLink;
  document.querySelector('.article-footer>span').textContent=data.footer.brand;document.querySelector('.article-footer>a').textContent=data.footer.codeLabel;
 }
 try{
  const responses=await Promise.all([fetch(articleURL,{cache:'no-cache'}),fetch(caseURL,{cache:'no-cache'})]);if(responses.some(r=>!r.ok))throw Error('正文数据无法读取');const [data,cases]=await Promise.all(responses.map(r=>r.json()));applyHero(data);root.replaceChildren();
  const registry=new Map(cases.sections.map(section=>[section.id,section.case]));
  for(const chapter of data.sections){
   const section=make('section','main-chapter');section.id=chapter.id;let copy=prose(section);copy.append(make('h2','',chapter.title));
   for(const block of chapter.blocks){
    if(block.type==='paragraph'){if(!copy)copy=prose(section);const p=make('p');if(block.id)p.id=block.id;p.innerHTML=block.html;copy.append(p)}
    else if(block.type==='case'){const evidence=registry.get(block.caseKey);if(!evidence)throw Error('案例缺失：'+block.caseKey);ArticleCaseEmbed.mount(section,{case:{...evidence,href:SitePaths.url(evidence.href)},variant:'flow'});copy=null}
    else if(block.type==='method-diagram'){section.append(methodDiagram(block));copy=null}
    else if(block.type==='target-diagram'){section.append(targetDiagram(block));copy=null}
   }
   root.append(section);
  }
  const resources=make('section','main-resources');resources.id=data.resources.id;const heading=prose(resources);heading.append(make('h2','',data.resources.title));const links=make('nav','resource-links');links.setAttribute('aria-label',data.resources.title);
  for(const item of data.resources.links){const a=make('a');a.href=new URL(item.href,document.baseURI);a.append(make('strong','',item.label),make('span','',item.description));links.append(a)}resources.append(links);root.append(resources);
  root.dataset.ready='true';document.dispatchEvent(new CustomEvent('article:ready',{detail:data}));
  await document.fonts.ready;requestAnimationFrame(()=>requestAnimationFrame(()=>{if(location.hash)document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView({block:'start'})}));
 }catch(error){root.textContent='正文暂时无法读取，请刷新重试。';console.error(error)}
})();
