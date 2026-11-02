/* Render the same post for direct reading and the homepage continuation. */
window.ResearchArticle = (() => {
 'use strict';
 const U=EvidenceUI,make=(tag,cls,value)=>U.make(tag,cls,value);
 const url=path=>SitePaths.url(path);
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

 let content;
 async function load(){
  if(!content)content=Promise.all(['design-lab/main-article.zh.json','design-lab/article-content/cases.zh.json'].map(async path=>{
   const response=await fetch(url(path));if(!response.ok)throw Error('Article data unavailable');return response.json();
  })).catch(error=>{content=null;throw error});
  return content;
 }
 async function mount(root){
  if(root.dataset.ready==='true')return;
  try{
   const [data,cases]=await load(),registry=new Map(cases.sections.map(section=>[section.id,section.case]));
   const fragment=document.createDocumentFragment(),notes=[];
   for(const chapter of data.sections){
    const section=make('section','main-chapter');section.id=chapter.id;let copy=prose(section);copy.append(make('h2','',chapter.title));
    for(const block of chapter.blocks){
     if(block.type==='paragraph'){
      if(!copy)copy=prose(section);const p=make('p');if(block.id)p.id=block.id;p.innerHTML=block.html;
      if(block.note){
       const number=notes.length+1,note=block.note,group=make('div','noted-paragraph');
       const ref=make('a','note-ref',String(number));ref.href='#note-'+note.id;ref.id='ref-'+note.id;ref.setAttribute('aria-label','注 '+number);ref.setAttribute('role','doc-noteref');const sup=make('sup');sup.append(ref);p.append(sup);
       const side=make('aside','sidenote');side.setAttribute('aria-label','注 '+number);side.append(make('span','',String(number)),document.createTextNode(' '+note.text));group.append(p,side);copy.append(group);notes.push({...note,number});
      }else copy.append(p);
     }else if(block.type==='case'){
      const evidence=registry.get(block.caseKey);if(!evidence)throw Error('Missing case: '+block.caseKey);
      ArticleCaseEmbed.mount(section,{case:{...evidence,href:url(evidence.href)},variant:'flow'});copy=null;
     }else if(block.type==='method-diagram'){section.append(methodDiagram(block));copy=null}
     else if(block.type==='target-diagram'){section.append(targetDiagram(block));copy=null}
    }
    fragment.append(section);
   }
   const endnotes=make('section','post-endnotes');endnotes.id='notes';endnotes.setAttribute('role','doc-endnotes');endnotes.append(make('h2','','注释'));const list=make('ol');
   for(const note of notes){const li=make('li');li.id='note-'+note.id;li.append(document.createTextNode(note.text+' '));const back=make('a','note-back','返回正文');back.href='#ref-'+note.id;back.setAttribute('aria-label','返回注 '+note.number+' 的正文');li.append(back);list.append(li)}endnotes.append(list);fragment.append(endnotes);
   const resources=make('section','main-resources');resources.id=data.resources.id;resources.append(make('h2','',data.resources.title));const links=make('nav','resource-links');links.setAttribute('aria-label',data.resources.title);
   for(const item of data.resources.links){const a=make('a');a.href=url(item.href);a.append(make('strong','',item.label),make('span','',item.description));links.append(a)}resources.append(links);fragment.append(resources);
   root.replaceChildren(fragment);root.dataset.ready='true';document.dispatchEvent(new CustomEvent('article:ready',{detail:data}));
  }catch(error){root.replaceChildren(make('p','','文章暂时无法读取。'));const retry=make('button','article-retry','重新载入');retry.onclick=()=>mount(root);root.append(retry);console.error(error)}
 }
 return {mount,load};
})();
