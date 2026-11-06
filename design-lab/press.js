(()=>{
'use strict';
const root=document.querySelector('[data-press-chart]');if(!root)return;
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const models=['Qwen3-8B','Qwen3.5-4B','Gemma 4 12B-it'];
const methods=['BF16','GPTQ','EfficientQAT','BitDistiller','On-Policy QAD','QeRL','Ours'];
const benchmarks=[['bfcl_v4','BFCL V4'],['tau2_bench','τ²-Bench'],['webshop','WebShop'],['alfworld','ALFWorld'],['search_qa','Search QA']];
const label=m=>m==='Ours'?'SteerDistill':m;
const fills={BF16:'var(--red)',GPTQ:'#dad7cf',EfficientQAT:'#c9c5bb',BitDistiller:'#b5b0a5','On-Policy QAD':'#9d988c',QeRL:'#858177',Ours:'var(--blue)'};
const expanded=root.dataset.pressSettings==='expanded';
let data=[],model=models[0],precision='W4A16',metric='average',comparison=root.dataset.defaultComparison||'key';
const settingRows=which=>data.filter(r=>r.model===which&&(!expanded||r.precision===precision||r.precision==='BF16'));
const file=location.pathname.split('/').pop().replace('.html','');document.querySelectorAll('[data-press-link]').forEach(a=>{if(a.dataset.pressLink===file)a.setAttribute('aria-current','page')});
function grouped(){
 const active=comparison==='key'?['BF16','QeRL','Ours']:methods;
 const wide=document.body.dataset.page === 'home';
 const w=wide?1280:1000,h=wide?330:420,L=48,R=18,T=32,B=wide?55:67,plotW=w-L-R,plotH=h-T-B,group=plotW/5;
 const unit=comparison==='key'?37:20,gap=comparison==='key'?6:4,total=active.length*(unit+gap)-gap;
 let axisLabels="",barLabels="";
 let s=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(model+' '+precision)} scores on five benchmarks; vertical axis starts at zero">`;
 s+=`<text x="${L}" y="14" class="axis-label">Score (%)</text>`;
 [0,25,50,75,100].forEach(t=>{const y=T+plotH*(1-t/100);if(t!==0)s+=`<line x1="${L}" x2="${w-R}" y1="${y}" y2="${y}" class="gridline"/>`;axisLabels+=`<text x="${L-12}" y="${y+4}" text-anchor="end" class="tick">${t}</text>`});
 benchmarks.forEach(([key,title],i)=>{
  const start=L+i*group+(group-total)/2;
  active.forEach((method,j)=>{
   const row=settingRows(model).find(r=>r.method===method),v=row[key],barH=plotH*v/100,x=start+j*(unit+gap),y=T+plotH-barH;
   const cls=method==='Ours'?'ours':method==='BF16'?'bf16':'baseline';
   s+=`<rect x="${x}" y="${y}" width="${unit}" height="${barH}" fill="${fills[method]}" class="benchmark-bar ${cls}" style="--bar-delay:${i*65+j*22}ms" tabindex="0" role="img" aria-label="${esc(title+' · '+label(method)+' · '+v.toFixed(2))}"><title>${esc(model+' / '+precision+' / '+title+' / '+label(method)+': '+v.toFixed(2))}</title></rect>`;
   if(comparison==='key'||method==='Ours'||method==='BF16')barLabels+=`<text x="${x+unit/2}" y="${y-7}" text-anchor="middle" class="bar-value ${cls}" style="--bar-delay:${i*65+j*22}ms">${v.toFixed(2)}</text>`;
  });
  axisLabels+=`<text x="${L+i*group+group/2}" y="${h-34}" text-anchor="middle" class="benchmark-label">${title}</text>`;
 });
 s+=`<g class="chart-value-layer">${barLabels}</g><g class="chart-axis-layer"><line x1="${L}" x2="${w-R}" y1="${T+plotH}" y2="${T+plotH}" class="gridline zero"/>${axisLabels}</g></svg>`;
 root.querySelector('.press-legend').innerHTML=active.map(m=>`<span><i class="legend-${m==='BF16'?'reference':''}" style="--series:${fills[m]}"></i>${esc(label(m))}</span>`).join('');
 return s;
}
function horizontal(which){
 const max=metric==='average'?70:100,rows=settingRows(which);
 const axis=`<div class="h-axis"><span>0</span><span>${max/2}</span><span>${max}%</span></div>`;
 return `<section class="model-plate"><h3>${esc(which)}</h3>${axis}<div class="h-rows">`+methods.map(method=>{const v=rows.find(r=>r.method===method)[metric];return `<div class="h-row ${method==='Ours'?'ours':method==='BF16'?'bf16':''}"><span class="h-label">${esc(label(method))}</span><div class="h-track"><i style="width:${v/max*100}%;--series:${fills[method]}" role="img" aria-label="${esc(label(method)+' '+v.toFixed(2))}"></i></div><b>${v.toFixed(2)}</b></div>`}).join('')+'</div></section>';
}
function render(){
 const type=root.dataset.pressChart;
 root.querySelector('.press-plot').innerHTML=type==='grouped'?grouped():type==='multiples'?'<div class="model-plates">'+models.map(horizontal).join('')+'</div>':horizontal(model);
 root.querySelectorAll('[data-press-model]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.pressModel===model&&(!expanded||b.dataset.pressPrecision===precision))));
 root.querySelectorAll('[data-comparison]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.comparison===comparison)));
 const rows=settingRows(model),ours=rows.find(r=>r.method==='Ours'),bf=rows.find(r=>r.method==='BF16'),best=rows.filter(r=>!['BF16','Ours'].includes(r.method)).reduce((a,b)=>a.average>b.average?a:b);
 let summary;
 if(type==='multiples')summary=metric==='average'?'五项基准的平均分，比较各模型的七种方法。':'所选基准上，三个模型的七种方法对比。';
 else if(type==='horizontal'&&metric!=='average')summary='所选基准的七种方法对比，BF16 为全精度参考。';
 else summary=`${model}${expanded?' · '+precision:''}: average score ${ours.average.toFixed(2)} (BF16: ${bf.average.toFixed(2)}), ${(ours.average-best.average).toFixed(2)} points above the strongest quantized baseline, ${best.method}.`;
 if(window.SiteLocale?.lang==='zh'&&type==='grouped')summary=`${model}${expanded?' · '+precision:''}：平均分 ${ours.average.toFixed(2)}（BF16：${bf.average.toFixed(2)}），比最强量化基线 ${best.method} 高 ${(ours.average-best.average).toFixed(2)} 分。`;
 root.querySelector('[data-press-summary]').textContent=summary;
 const settingLabel=root.querySelector('[data-press-setting-label]');if(settingLabel)settingLabel.textContent=precision+' · BF16 reference';
 root.dataset.ready='true';
}
root.querySelectorAll('[data-press-model]').forEach(b=>b.onclick=()=>{if(!data.length)return;model=b.dataset.pressModel;precision=b.dataset.pressPrecision||'W4A16';render()});
root.querySelectorAll('[data-comparison]').forEach(b=>b.onclick=()=>{if(!data.length)return;comparison=b.dataset.comparison;render()});
const select=root.querySelector('[data-press-metric]');if(select)select.onchange=()=>{if(!data.length)return;metric=select.value;render()};
fetch(expanded?'experiments/data/benchmark_results.csv':'experiments/data/results-chart.json').then(r=>{
 if(!r.ok)throw Error('unavailable');
 if(!expanded)return r.json();
 return r.text().then(csv=>{
  const lines=csv.trim().split(/\r?\n/),keys=lines.shift().split(',');
  return lines.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[keys[i],i<3?v:Number(v)])));
 });
}).then(d=>{data=d;render()}).catch(()=>{root.querySelector('.press-plot').textContent=window.HomeLocale?.t('Benchmark data could not be loaded. Please reload.')||'Benchmark data could not be loaded. Please reload.'});
})();
