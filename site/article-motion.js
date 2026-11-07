/* Two reading figures, each with one clock and an inspectable sequence.
 * SVG geometry is illustrative. It does not encode measured probabilities. */
window.ArticleMotion = (() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  let serial = 0;
  const stories = {
    repair: [
      ['定位', '对齐环境状态，定位首次分歧；回到此前的历史与状态。'],
      ['指导', 'Teacher 给出指导 G，冻结 student 在原上下文中生成并执行修正。'],
      ['反馈', '核验未通过：把执行反馈交还 Teacher，细化指导，从同一状态重试。'],
      ['接受', '环境变化和返回信息通过核验后，保留该响应与对应指导。'],
      ['继续', '撤去指导继续执行；当前修正通过核验，并不代表整条任务完成。']
    ],
    distill: [
      ['同一上下文', '历史与响应前缀组成 c。训练中的 student 始终只接收 c，不看指导。'],
      ['修正轮次', '修正轮次：冻结快照接收 c 与 G，以其 token 分布提供 forward KL 监督。'],
      ['其他轮次', '其他轮次：Teacher 和学习者都只接收 c，使用 reverse KL。'],
      ['更新并再执行', '仅更新量化 student 的参数，再用新模型收集轨迹，寻找尚未解决的错误。']
    ]
  };
  function el(tag, cls, text) {
    const n = document.createElement(tag); if (cls) n.className = cls;
    if (text) n.textContent = text; return n;
  }
  function svgEl(tag, attrs = {}, text) {
    const n = document.createElementNS(NS, tag);
    for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v);
    if (text) n.textContent = text; return n;
  }
  function text(g,x,y,value,cls='',anchor='start') {
    g.append(svgEl('text',{x,y,class:cls,'text-anchor':anchor},value));
  }
  function path(g,d,cls='am-wire',extra={}) {g.append(svgEl('path',{d,class:cls,...extra}));}
  function rect(g,x,y,w,h,cls='am-box',rx=3) {g.append(svgEl('rect',{x,y,width:w,height:h,rx,class:cls}));}
  function group(g,stage,cls='',leave) {
    const n=svgEl('g',{'data-enter':stage,class:cls,...(leave===undefined?{}:{'data-leave':leave})});g.append(n);return n;
  }
  function arrow(g,d,marker,cls='am-wire',extra={}) {path(g,d,cls,{'marker-end':`url(#${marker})`,pathLength:1,...extra});}
  function signal(g,d,phase){path(g,d,'am-signal',{pathLength:1,'data-flow':phase});}
  function mark(g,x,y,kind='check') {
    path(g,kind==='check'?`M${x-5} ${y}l4 4 8-9`:`M${x-4} ${y-4}l8 8m0-8-8 8`,'am-mark');
  }
  function distribution(g,x,y,learner=false,teacher=false) {
    const bars=svgEl('g',{transform:`translate(${x} ${y})`,class:'am-distribution','aria-hidden':'true'});
    const corrected=[.2,.45,.9,.3,.55,.2],ordinary=[.45,.2,.35,.85,.25,.5],initial=[.7,.3,.25,.45,.6,.35];
    for(let i=0;i<6;i++){
      const bar=svgEl('rect',{x:i*8,y:-22,width:5,height:22,rx:.5,class:learner?'am-learner-bar':'am-target-bar'});
      bar.style.cssText=`--am-initial:${initial[i]};--am-corrected:${corrected[i]};--am-teacher:${ordinary[i]};${learner?'':`transform:scaleY(${(teacher?ordinary:corrected)[i]})`}`;
      bars.append(bar);
    }
    g.append(bars);
  }
  function setup(mobile,label) {
    const id='article-arrow-'+(++serial),svg=svgEl('svg',{
      viewBox:mobile?'0 0 360 570':'0 0 680 380',
      class:'am-svg '+(mobile?'am-mobile':'am-desktop'),role:'img','aria-label':label
    });
    const defs=svgEl('defs'),marker=svgEl('marker',{id,viewBox:'0 0 10 10',refX:8,refY:5,markerWidth:6,markerHeight:6,orient:'auto-start-reverse'});
    marker.append(svgEl('path',{d:'M2 2L8 5L2 8',fill:'none',stroke:'context-stroke','stroke-width':1.3}));defs.append(marker);svg.append(defs);return {svg,id};
  }
  function repair(mobile) {
    const {svg:s,id}=setup(mobile,'按环境状态定位分歧；指导 student 修订，用执行反馈重试，通过局部核验后撤去指导继续。');
    s.setAttribute('viewBox',mobile?'0 0 360 490':'0 0 680 360');
    const w=mobile?360:680, start=mobile?90:135, gap=mobile?49:86;
    text(s,0,26,'Teacher','am-label');text(s,0,70,'Student','am-label');
    const trace=group(s,0);
    for (let row=0;row<2;row++) {
      path(trace,`M${start} ${21+row*44}H${start+gap*4}`,'am-track');
      for(let i=0;i<5;i++) {
        const x=start+gap*i,y=21+row*44;
        trace.append(svgEl('circle',{cx:x,cy:y,r:4,class:i<2?'am-dot':'am-empty'}));
      }
    }
    const x=start+gap*2;
    path(trace,`M${x} 29V55`,'am-alignment');
    const fail=group(trace,0,'am-red');mark(fail,x,65,'cross');
    text(trace,mobile?350:650,104,'首次行为分歧','am-small am-blue','end');
    path(trace,`M${x} 82v17H${mobile?235:535}`,'am-wire am-dashed');
    text(s,0,126,'恢复出错前的历史与环境状态','am-small');
    path(s,`M0 139H${w}`,'am-rule');
    // The same candidate slot is retried; accepted correction replaces it.
    const gx=0,gy=mobile?170:181, sx=mobile?0:245,sy=mobile?290:181, vx=mobile?230:500,vy=mobile?290:181;
    const guide=group(s,1,'am-blue');
    path(guide,`M${gx+1} ${gy+5}V${gy+58}`,'am-editorial-rule');
    text(guide,gx+14,gy+25,'Teacher 指导','am-node-title');
    text(group(guide,1,'am-first',3),gx+14,gy+47,'G · 指出遗漏的条件','am-small');
    text(group(guide,3,'am-revised'),gx+14,gy+47,'G′ · 根据反馈细化','am-small');
    const candidate=group(s,1);
    path(candidate,`M${sx} ${sy+62}H${sx+176}`,'am-rule');
    text(candidate,sx+14,sy+25,'冻结 student','am-node-title');
    text(group(candidate,1,'am-first',3),sx+14,sy+47,'生成并执行修正','am-small');
    text(group(candidate,3,'am-blue'),sx+14,sy+47,'修正通过核验','am-small');
    arrow(candidate,mobile?'M88 245V281':'M200 212H236',id,'am-wire am-blue');
    signal(candidate,mobile?'M88 245V281':'M200 212H236',1);
    const verify=group(s,1);
    path(verify,`M${vx+13} ${vy+62}H${vx+113}`,'am-rule');
    text(verify,vx+63,vy+27,'局部核验','am-node-title','middle');
    text(verify,vx+63,vy+47,'状态与返回信息','am-tiny','middle');
    arrow(verify,mobile?'M184 321H222':'M429 212H492',id);
    const feedback=group(s,2,'am-red');
    arrow(feedback,mobile?'M293 287V263Q293 257 287 257H242V203H214':'M563 174V157H96V174',id,'am-wire am-red am-draw');
    text(feedback,mobile?242:330,mobile?250:150,'执行反馈', 'am-small am-red',mobile?'start':'middle');
    signal(feedback,mobile?'M293 287V263Q293 257 287 257H242V203H214':'M563 174V157H96V174',2);
    const rejected=group(s,2,'am-red',3);mark(rejected,vx+113,vy-9,'cross');
    const accepted=group(s,3,'am-blue');mark(accepted,vx+113,vy-9);
    // Retained response remains distinct from its continuation.
    const output=group(s,3,'am-blue'),oy=mobile?411:299;
    arrow(output,mobile?'M293 361V382H88V401':'M563 251V276H88V290',id,'am-wire am-blue am-draw');
    signal(output,mobile?'M293 361V382H88V401':'M563 251V276H88V290',3);
    path(output,`M1 ${oy+4}V${oy+48}`,'am-editorial-rule');
    text(output,14,oy+22,'保留修正','am-node-title');
    text(output,14,oy+41,'响应 y* ＋ 对应指导 G′','am-small');
    const continuation=group(s,4),cx=mobile?230:360;
    arrow(continuation,`M184 ${oy+26}H${cx-9}`,id,'am-wire am-blue');
    signal(continuation,`M184 ${oy+26}H${cx-9}`,4);
    text(continuation,mobile?217:265,oy+12,'撤去 G′','am-tiny am-blue','middle');
    for(let i=0;i<3;i++)rect(continuation,cx+i*(mobile?39:74),oy+17,mobile?25:54,9,'am-action',0);
    text(continuation,cx,oy+48,'无指导继续执行','am-small');

    return s;
  }
  function distill(mobile) {
    const {svg:s,id}=setup(mobile,'同一上下文 c；修正轮次由带指导的冻结 student 监督，其他轮次由 BF16 Teacher 监督；学习者始终不看指导。');
    if(!mobile)s.setAttribute('viewBox','0 0 680 390');
    text(s,0,22,'保留轨迹','am-label');
    const tape=group(s,0);
    for(let i=0;i<7;i++)rect(tape,i*(mobile?49:49),41,35,9,i===2?'am-action':'am-tape',0);
    path(tape,'M100 60H132','am-turn-marker');
    text(tape,115,94,'修正轮次','am-small am-blue','middle');
    text(tape,mobile?265:285,94,'其他轮次','am-small','middle');
    const ctx=group(s,0);text(ctx,mobile?0:393,mobile?125:45,'c = 历史 ＋ 响应前缀','am-context');
    text(ctx,mobile?0:393,mobile?148:68,'不含指导','am-small');
    path(s,mobile?'M0 165H360':'M0 115H680','am-rule');
    const sy=mobile?203:160,ty=mobile?317:276;
    const source=group(s,0,'am-source');
    text(source,0,sy-15,'修正轮次','am-small am-blue');
    path(source,`M1 ${sy+5}V${sy+62}`,'am-editorial-rule am-blue');
    text(source,14,sy+26,'冻结 student 快照','am-node-title');
    text(source,14,sy+49,'输入 c ＋ G','am-context am-blue');
    distribution(source,145,sy+55);

    const teacher=group(s,0,'am-teacher');
    text(teacher,0,ty-15,'其他轮次','am-small');path(teacher,`M1 ${ty+5}V${ty+62}`,'am-editorial-rule am-neutral');
    text(teacher,14,ty+26,'全精度 Teacher','am-node-title');text(teacher,14,ty+49,'输入 c','am-context');
    distribution(teacher,145,ty+55,false,true);
    const ly=mobile?452:202,lx=mobile?99:447;
    const learner=group(s,0,'am-learner');path(learner,`M${lx} ${ly}H${lx+(mobile?260:226)}M${lx} ${ly+80}H${lx+(mobile?260:226)}`,'am-learner-rule');
    text(learner,lx+15,ly+27,'训练中的量化 student','am-node-title');
    text(learner,lx+15,ly+52,'输入 c','am-context am-blue');
    text(group(learner,3),lx+15,ly+70,'参数更新','am-small am-blue');
    distribution(learner,lx+(mobile?198:165),ly+65,true);
    const fkl=group(s,1,'am-fkl',2);
    const rkl=group(s,2,'am-rkl',3);
    arrow(fkl,mobile?'M210 236H316V442':'M210 193H335Q350 193 350 208V222H437',id,'am-wire am-blue am-draw');
    arrow(rkl,mobile?'M210 350H263V442':'M210 309H335Q350 309 350 294V262H437',id,'am-wire am-blue am-draw');
    signal(fkl,mobile?'M210 236H316V442':'M210 193H335Q350 193 350 208V222H437',1);
    signal(rkl,mobile?'M210 350H263V442':'M210 309H335Q350 309 350 294V262H437',2);
    text(fkl,mobile?224:240,mobile?217:181,'Forward KL','am-small am-blue');
    text(rkl,mobile?224:240,mobile?330:337,'Reverse KL','am-small am-blue');
    const update=group(s,3,'am-blue');
    arrow(update,mobile?'M90 497H28V557H345':'M560 290V365H260',id,'am-wire am-blue am-draw');
    signal(update,mobile?'M90 497H28V557H345':'M560 290V365H260',3);
    text(update,mobile?40:275,mobile?548:355,'更新参数 → 下一轮独立执行','am-small am-blue');
    // A fine guide connects c to the learner; G has no path to the learner input.
    if(!mobile){path(ctx,'M560 80V190','am-wire am-dashed');}
    text(s,0,mobile?412:385,'token 分布示意','am-tiny');
    return s;
  }
  function mount(kind,title) {
    const figure=el('figure',`${kind==='repair'?'method-diagram':'target-diagram'} article-motion`);
    figure.dataset.story=kind;figure.dataset.stage='0';
    const head=el('div','am-heading');head.append(el('h3','',title));
    const play=el('button','am-play','暂停 Ⅱ');play.type='button';head.append(play);figure.append(head);
    const stage=el('div','am-canvas');stage.append(...[false,true].map(kind==='repair'?repair:distill));figure.append(stage);
    const controls=el('div','am-steps');controls.setAttribute('role','group');controls.setAttribute('aria-label',title+'：逐步查看');
    const steps=stories[kind],buttons=steps.map(([label],i)=>{const b=el('button','',label);b.type='button';b.setAttribute('aria-label',`第 ${i+1} 步：${label}`);b.append(el('span','am-step-progress'));controls.append(b);return b;});
    const caption=el('figcaption','am-caption');const counter=el('span','am-counter'),copy=el('span');caption.append(counter,copy);figure.append(controls,caption);
    const reduced=matchMedia('(prefers-reduced-motion: reduce)'),phaseMs=4400,total=phaseMs*steps.length;
    let elapsed=reduced.matches?(steps.length-1)*phaseMs:0,playing=!reduced.matches,visible=false,frame=0,previous=0,current=-1;
    const reveals=[...stage.querySelectorAll('[data-enter]')];
    function paint() {
      const index=Math.min(steps.length-1,Math.floor(elapsed/phaseMs));
      if(index!==current){
        current=index;figure.dataset.stage=String(index);
        reveals.forEach(n=>n.dataset.revealed=String(index>=Number(n.dataset.enter)&&(n.dataset.leave===undefined||index<Number(n.dataset.leave))));
        buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
        counter.textContent=String(index+1).padStart(2,'0');copy.textContent=steps[index][1];
      }
      figure.style.setProperty('--am-progress',(elapsed%phaseMs)/phaseMs);
    }
    function tick(now){if(previous)elapsed=(elapsed+now-previous)%total;previous=now;paint();frame=requestAnimationFrame(tick);}
    function sync(){
      cancelAnimationFrame(frame);previous=0;
      const run=playing&&visible&&!document.hidden;
      figure.dataset.running=String(run);play.textContent=playing?'暂停 Ⅱ':'播放 ▷';
      play.setAttribute('aria-label',(playing?'暂停':'播放')+'：'+title);play.setAttribute('aria-pressed',String(playing));
      if(run)frame=requestAnimationFrame(tick);
    }
    play.onclick=()=>{if(!playing&&reduced.matches&&current===steps.length-1){elapsed=0;paint();}playing=!playing;sync();};
    buttons.forEach((b,i)=>b.onclick=()=>{elapsed=i*phaseMs;playing=false;paint();sync();});
    SiteVisibility.observe(figure,next=>{
      visible=next;
      if(visible&&playing){elapsed=0;paint();for(const a of figure.getAnimations({subtree:true}))if(a instanceof CSSAnimation)a.currentTime=0;}
      sync();
    });
    reduced.addEventListener('change',()=>{if(reduced.matches){playing=false;elapsed=(steps.length-1)*phaseMs;paint();sync();}});
    paint();sync();return figure;
  }
  return {mount};
})();
