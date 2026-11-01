/* Render the original user turns; keep source wording separate from editorial summaries. */
window.CaseTaskSource={create(task){
 const details=document.createElement('details');details.className='ev-disclosure original-task';
 const summary=document.createElement('summary');summary.textContent='原始任务描述';details.append(summary);
 const body=document.createElement('div');body.className='original-turns';
 const turns=task.question||[];
 turns.forEach((messages,index)=>{
  const users=(Array.isArray(messages)?messages:[messages]).filter(m=>m.role==='user');
  if(!users.length)return;
  const turn=document.createElement('section');turn.className='original-turn';
  if(turns.length>1){const label=document.createElement('h3');label.textContent=`用户 · 第 ${index+1} 轮`;turn.append(label)}
  users.forEach(m=>{const p=document.createElement('p');p.textContent=typeof m.content==='string'?m.content:JSON.stringify(m.content,null,2);turn.append(p)});
  body.append(turn);
 });details.append(body);return details;
}};
