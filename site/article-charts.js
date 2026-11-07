/* Figures use the manuscript's numerical inputs, re-composed for the reading column. */
window.ArticleCharts=(()=>{
 'use strict';
 const D=ResearchChartData,NS='http://www.w3.org/2000/svg';
 let serial=0;
 function node(tag,cls,value){const n=document.createElement(tag);if(cls)n.className=cls;if(value)n.textContent=value;return n;}
 function svgNode(tag,attrs={},value){const n=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);if(value)n.textContent=value;return n;}
 function text(s,x,y,value,cls='ac-tick',anchor='start'){s.append(svgNode('text',{x,y,class:cls,'text-anchor':anchor},value));}
 function path(s,d,attrs={}){const n=svgNode('path',{d,...attrs});s.append(n);return n;}
 function line(s,x1,y1,x2,y2,cls='ac-grid'){s.append(svgNode('line',{x1,y1,x2,y2,class:cls}));}
 function svg(w,h,label){return svgNode('svg',{viewBox:`0 0 ${w} ${h}`,role:'img','aria-label':label});}
 function focusable(n,label,status){n.setAttribute('tabindex','0');n.setAttribute('role','img');n.setAttribute('aria-label',label);n.append(svgNode('title',{},label));for(const event of ['pointerenter','focus'])n.addEventListener(event,()=>{status.textContent=label;});}
 function legend(methods){const n=node('div','ac-legend');for(const m of methods){const item=node('span'),swatch=node('i');swatch.style.background=D.colors[m];item.append(swatch,document.createTextNode(D.label(m)));n.append(item);}return n;}
 const animateOnView=root=>SiteVisibility.chart(root);
 function head(figure,title,subtitle){const h=node('header','ac-head');h.append(node('h3','',title));if(subtitle)h.append(node('p','ac-subtitle',subtitle));figure.append(h);}
 function failure(root,retry){root.replaceChildren(node('p','ac-error','图表暂时无法读取。'));const b=node('button','ac-retry','重新载入');b.type='button';b.onclick=retry;root.append(b);}
 function average(){
  const figure=node('figure','article-chart ac-average');figure.dataset.chart='average';head(figure,'五项基准的平均表现');
  const controls=node('div','ac-settings');controls.setAttribute('role','group');controls.setAttribute('aria-label','模型与量化设置');
  const buttons=D.settings.map(([model,precision],i)=>{const b=node('button');b.type='button';b.append(document.createTextNode(model),node('span','',precision));b.setAttribute('aria-pressed',String(i===0));b.onclick=()=>{selected=i;render();};controls.append(b);return b;});
  const plot=node('div','ac-plot'),summary=node('p','ac-summary ac-sr'),status=node('p','ac-inspect ac-sr','指向或聚焦柱形，查看精确分数。');status.setAttribute('aria-live','polite');
  const cap=node('figcaption','ac-caption');cap.append(node('span','','五项基准报告指标的无权重平均；BF16 为对应模型的全精度参考。'));
  const download=node('a','','数据');download.href=SitePaths.url('experiments/data/benchmark_results.csv');cap.append(download);
  figure.append(controls,plot,summary,status,cap);let rows=null,selected=0,width=680;
  function render(){
   if(!rows)return;const[model,precision]=D.settings[selected],values=D.selected(rows,model,precision),mobile=width<500;
   const mobileWidth=Math.max(280,Math.round(width));
   const s=svg(mobile?mobileWidth:680,mobile?326:310,`${model} ${precision}，五项基准平均分，数值轴从零开始。`),max=70;
   const axes=svgNode('g',{class:'ac-axis-layer','pointer-events':'none'});
   if(mobile){
    const L=108,R=mobileWidth-33,T=38,bottom=284;
    for(const v of [0,20,40,60]){const x=L+(R-L)*v/max;line(s,x,T-10,x,bottom);text(axes,x,308,String(v),'ac-tick','middle');}
    text(s,L,17,'平均分 (%)','ac-axis-title');
    values.forEach((row,i)=>{const y=T+i*35;const name=D.label(row.method);text(s,L-10,y+12,name,'ac-method','end');const n=svgNode('rect',{x:L,y,width:(R-L)*row.average/max,height:17,fill:D.colors[row.method],class:'ac-bar ac-horizontal',style:`--delay:${i*50}ms`});focusable(n,`${name}：${row.average.toFixed(2)}`,status);s.append(n);text(s,L+(R-L)*row.average/max+6,y+12,row.average.toFixed(2),'ac-value');});
    line(axes,L,T-10,L,bottom,'ac-baseline');
   }else{
    const L=38,R=670,T=30,B=252,H=B-T,step=(R-L)/7;
    text(s,L,13,'平均分 (%)','ac-axis-title');
    for(const v of [0,20,40,60]){const y=B-H*v/max;line(v===0?axes:s,L,y,R,y,v===0?'ac-baseline':'ac-grid');text(axes,L-9,y+4,String(v),'ac-tick','end');}
    values.forEach((row,i)=>{const cx=L+step*(i+.5),h=H*row.average/max,n=svgNode('rect',{x:cx-23,y:B-h,width:46,height:h,fill:D.colors[row.method],class:'ac-bar',style:`--delay:${i*55}ms`});focusable(n,`${D.label(row.method)}：${row.average.toFixed(2)}`,status);s.append(n);text(s,cx,B-h-9,row.average.toFixed(2),'ac-value','middle');
     const parts=row.method==='On-Policy QAD'?['On-Policy','QAD']:[D.label(row.method)];parts.forEach((name,j)=>text(s,cx,B+24+j*15,name,'ac-method','middle'));
    });
   }
   s.append(axes);
   plot.replaceChildren(s);buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===selected)));
   const ours=values.find(r=>r.method==='Ours'),ref=values[0],best=values.filter(r=>!['Ours','BF16'].includes(r.method)).reduce((a,b)=>a.average>b.average?a:b);
   summary.textContent=`${model} · ${precision}：SteerDistill ${ours.average.toFixed(2)}，比最强量化基线高 ${(ours.average-best.average).toFixed(2)} 分；BF16 ${ref.average.toFixed(2)}。`;
   status.textContent='指向或聚焦柱形，查看精确分数。';figure.dataset.ready='true';
  }
  async function load(){try{rows=await D.scores();render();}catch{failure(plot,load);}}
  new ResizeObserver(entries=>{const w=entries[0].contentRect.width;if(Math.abs(w-width)>1){width=w;render();}}).observe(figure);
  load();animateOnView(figure);return figure;
 }
 function efficiency(){
  const figure=node('figure','article-chart ac-efficiency');figure.dataset.chart='efficiency';head(figure,'训练与执行的成本','Qwen3-8B · W4A16 · τ²-Bench');figure.append(legend(D.methods));
  const pair=node('div','ac-pair');figure.append(pair);
  function panel(title){const n=node('section','ac-panel');n.append(node('h4','',title));const plot=node('div','ac-plot'),status=node('p','ac-inspect');status.setAttribute('aria-live','polite');n.append(plot,status);pair.append(n);return {element:n,plot,status};}
  const train=panel('训练 GPU 小时'),infer=panel('推理输出 token');
  const cap=node('figcaption','ac-caption');cap.append(node('span','','训练曲线为四次独立评测的均值，阴影为 ±1 标准差。推理 token 按各方法各自成功的任务平均。'));const download=node('a','','数据');download.href=SitePaths.url('experiments/data/efficiency.json');cap.append(download);figure.append(cap);
  function axes(s,{minX,maxX,xTicks,xTitle}){
   const L=38,R=310,T=30,B=238,minY=25,maxY=34,x=v=>L+(v-minX)/(maxX-minX)*(R-L),y=v=>B-(v-minY)/(maxY-minY)*(B-T);
   text(s,L,12,'Pass@1 (%)','ac-axis-title');
   for(const v of [26,28,30,32,34]){line(s,L,y(v),R,y(v));text(s,L-8,y(v)+4,String(v),'ac-tick','end');}
   line(s,L,B,R,B,'ac-baseline');
   for(const v of xTicks){line(s,x(v),B,x(v),B+4,'ac-baseline');text(s,x(v),B+19,String(v),'ac-tick','middle');}
   text(s,(L+R)/2,284,xTitle,'ac-axis-title','middle');return {x,y,L,R,T,B};
  }
  async function load(){try{
   const d=await D.efficiency();pair.replaceChildren(train.element,infer.element);
   const s=svg(328,294,'训练成本：成功率随 GPU 小时变化，带四次评测的标准差。');
   const{x,y,L,R,T,B}=axes(s,{minX:0,maxX:112,xTicks:[0,32,64,96,112],xTitle:'训练成本 (GPU 小时)'});
   // Include endpoint markers and their focus stroke without moving the data or ticks.
   const markerPadding=5;
   const clipId='training-reveal-'+(++serial),defs=svgNode('defs'),clip=svgNode('clipPath',{id:clipId});clip.append(svgNode('rect',{x:L-markerPadding,y:T,width:R-L+2*markerPadding,height:B-T,class:'ac-line-window'}));defs.append(clip);s.append(defs);
   const lines=svgNode('g',{'clip-path':`url(#${clipId})`});s.append(lines);
   line(s,L,y(d.bf16.pass_at_1),R,y(d.bf16.pass_at_1),'ac-reference');text(s,R-2,y(d.bf16.pass_at_1)-7,`BF16 · ${d.bf16.pass_at_1.toFixed(2)}`,'ac-reference-label','end');
   for(const [name,key,dash]of [['On-Policy QAD','On-Policy QAD','2 4'],['QeRL','QeRL','6 3'],['SteerDistill','Ours','']]){
    const mean=d.series[name],sd=d.std[name],points=mean.map((v,i)=>[x(d.hours[i]),y(v)]);
    const upper=mean.map((v,i)=>`${x(d.hours[i])},${y(v+sd[i])}`).join(' L'),lower=mean.map((v,i)=>`${x(d.hours[i])},${y(v-sd[i])}`).reverse().join(' L');
    path(lines,`M${upper} L${lower} Z`,{fill:D.colors[key],class:'ac-band'});
    path(lines,'M'+points.map(p=>p.join(',')).join(' L'),{stroke:D.colors[key],class:'ac-curve','stroke-dasharray':dash});
    points.forEach(([cx,cy],i)=>{const point=svgNode('circle',{cx,cy,r:3,fill:D.colors[key],class:'ac-point'});focusable(point,`${name} · ${d.hours[i]} GPU 小时：${mean[i].toFixed(2)}% ± ${sd[i].toFixed(2)}`,train.status);lines.append(point);});
   }
   const checkpoint=d.hours.indexOf(32),hx=x(d.hours[checkpoint]),hy=y(d.series.SteerDistill[checkpoint]);path(s,`M${hx} ${hy+8}V${hy+31}H${hx+7}`,{class:'ac-guide'});text(s,hx+10,hy+37,`${d.hours[checkpoint]} h · ${d.series.SteerDistill[checkpoint].toFixed(2)}%`,'ac-callout');
   train.plot.replaceChildren(s);train.status.textContent='指向或聚焦检查点，查看均值与标准差。';
   const scatter=svg(328,294,'推理成本：成功任务平均输出 token 与任务成功率。');const a=axes(scatter,{minX:3.6,maxX:5.5,xTicks:[4,4.5,5,5.5],xTitle:'输出 token / 成功任务 (K)'});
   // Authored offsets preserve the seven method names at the article's half-column width.
   const offsets={BF16:[9,-9,'start'],Ours:[9,14,'start'],QeRL:[8,-5,'start'],'On-Policy QAD':[-7,16,'end'],BitDistiller:[8,-6,'start'],EfficientQAT:[8,15,'start'],GPTQ:[-9,15,'end']};
   D.methods.forEach((key,i)=>{
    const tx=key==='BF16'?d.bf16.output_tokens_k:d.tokens[key].W4A16,score=key==='BF16'?d.bf16.pass_at_1:d.tau2[key].W4A16,cx=a.x(tx),cy=a.y(score);
    const group=svgNode('g',{class:'ac-scatter-mark',style:`--delay:${i*70}ms`}),point=svgNode('circle',{cx,cy,r:key==='Ours'?5:4,fill:D.colors[key],class:'ac-point'});focusable(point,`${D.label(key)}：${tx.toFixed(1)}K token，Pass@1 ${score.toFixed(2)}%`,infer.status);group.append(point);
    const[dx,dy,anchor]=offsets[key];text(group,cx+dx,cy+dy,key==='On-Policy QAD'?'On-Policy QAD':D.label(key),'ac-point-label',anchor);scatter.append(group);
   });infer.plot.replaceChildren(scatter);infer.status.textContent='越靠左上，输出更少、成功率更高。';figure.dataset.ready='true';
  }catch{failure(pair,load);}}
  load();animateOnView(train.element);animateOnView(infer.element);return figure;
 }
 return {mount:kind=>kind==='average'?average():efficiency()};
})();
