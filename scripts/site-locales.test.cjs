const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
function context({page='home',search='',saved=null}={}){
 const storage=new Map(saved?[['steerdistill-language',saved]]:[]),location=new URL('https://example.org/SteerDistill/'+(page==='home'?'index.html':'article.html')+search);
 const c={URL,URLSearchParams,location,localStorage:{getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)},document:{body:{dataset:{page}},documentElement:{},querySelector:()=>null,querySelectorAll:()=>[],addEventListener(){}}};c.window=c;
 for(const file of ['site/locale.js','site/home-locale.js'])vm.runInNewContext(fs.readFileSync(path.join(root,file),'utf8'),c);
 return c;
}
test('shared locale honors explicit selection, then saved preference, with original page defaults',()=>{
 assert.equal(context().SiteLocale.lang,'en');assert.equal(context({page:'article'}).SiteLocale.lang,'zh');
 assert.equal(context({saved:'zh'}).SiteLocale.lang,'zh');assert.equal(context({saved:'zh',search:'?lang=en'}).SiteLocale.lang,'en');
 const c=context({search:'?lang=zh'}),url=c.SiteLocale.url('design-lab/paper-cases.html?group=training&case=directory-navigation#case-start');
 assert.equal(url,'/SteerDistill/design-lab/paper-cases.html?group=training&case=directory-navigation&lang=zh#case-start');
 assert.equal(c.SiteLocale.url('https://scalewob.github.io/'),'https://scalewob.github.io/');
});
test('all demo task descriptions and step annotations have reviewed Chinese translations',()=>{
 const c=context({search:'?lang=zh'}),catalog=JSON.parse(fs.readFileSync(path.join(root,'demos/catalog.json')));
 for(const task of catalog.tasks){
  for(const field of ['label','task'])assert.notEqual(c.HomeLocale.t(task[field]),task[field],task.id+' '+field);
  const data=JSON.parse(fs.readFileSync(path.join(root,'demos',task.path,'replay.json'))),copy=JSON.stringify(data);
  for(const run of data.runs)for(const step of run.steps)assert.notEqual(c.HomeLocale.t(step.title),step.title,task.id+' '+step.title);
  assert.equal(JSON.stringify(data),copy);
 }
 assert.equal(context({search:'?lang=en'}).HomeLocale.t('Focus the search field'),'Focus the search field');
});
test('every generated entry has one switch and shared locale; article remains explicitly Chinese',()=>{
 for(const file of ['index.html','article.html','design-lab/paper-cases.html','design-lab/case-records.html']){
  const html=fs.readFileSync(path.join(root,file),'utf8');assert.equal((html.match(/class="site-language"/g)||[]).length,1,file);assert.match(html,/site\/locale\.js/);
 }
 const article=fs.readFileSync(path.join(root,'article.html'),'utf8');assert.match(article,/post-surface" lang="zh-CN"/);assert.doesNotMatch(article,/home-locale\.js/);
});
