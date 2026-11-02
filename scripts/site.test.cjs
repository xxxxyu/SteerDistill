const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const pages=['index.html','article.html','design-lab/paper-cases.html','design-lab/case-records.html'];
test('every entry uses the same shell and resolves its local dependencies',()=>{
 for(const file of pages){
  const html=fs.readFileSync(path.join(root,file),'utf8');
  assert.equal((html.match(/class="site-header"/g)||[]).length,1,file);
  assert.equal((html.match(/class="site-theme"/g)||[]).length,1,file);
  assert.match(html,/site\/site\.css/);assert.match(html,/site\/site\.js/);
  assert.doesNotMatch(html,/case-theme\.js|site-shell\.js/);
  for(const match of html.matchAll(/(?:src|href|poster)="([^"#]+)"/g)){
   if(/^(?:https?:|mailto:|data:)/.test(match[1]))continue;
   const asset=decodeURIComponent(match[1].split(/[?#]/)[0]);
   assert.ok(fs.existsSync(path.resolve(root,path.dirname(file),asset)),`${file}: ${asset}`);
  }
 }
});
test('site URLs preserve root and GitHub project prefixes without duplication',()=>{
 const script=fs.readFileSync(path.join(root,'design-lab/case-shared/site-paths.js'),'utf8');
 for(const prefix of ['/','/SteerDistill/']){
  const context={URL,window:{},document:{currentScript:{src:`https://example.com${prefix}design-lab/case-shared/site-paths.js`}}};
  vm.runInNewContext(script,context);const url=context.window.SitePaths.url;
  for(const resource of ['index.html','article.html#method','design-lab/paper-cases.html?group=training']){
   assert.equal(url(resource),prefix+resource);assert.equal(url(url(resource)),prefix+resource);
  }
 }
});
test('article notes have unique targets and frozen case embeds remain complete',()=>{
 const data=JSON.parse(fs.readFileSync(path.join(root,'design-lab/main-article.zh.json')));
 const notes=data.sections.flatMap(s=>s.blocks.filter(b=>b.note).map(b=>b.note.id));
 assert.equal(new Set(notes).size,notes.length);
 assert.equal(data.post.author.name,'Xiangyu Li');
 assert.deepEqual(data.sections.flatMap(s=>s.blocks.filter(b=>b.type==='case').map(b=>b.caseKey)),['problem','method','guidance','recovery']);
});
