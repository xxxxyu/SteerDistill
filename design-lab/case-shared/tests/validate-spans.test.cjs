const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const context={window:{}};
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../evidence-ui.js'),'utf8'),context);
const validate=context.window.EvidenceUI.validateSpans;
test('exact spans preserve source and the selected duplicate occurrence',()=>{
 const source='same then same',spans=[{start:10,end:14,text:'same'}];
 assert.equal(validate(source,spans),spans);assert.equal(source,'same then same');
});
test('UTF-16 offsets agree with JavaScript source slices',()=>assert.equal(validate('x😀y',[{start:1,end:3,text:'😀'}]).length,1));
for(const [kind,spans] of Object.entries({negative:[{start:-1,end:1,text:'a'}],fractional:[{start:.5,end:1,text:'a'}],empty:[{start:1,end:1,text:''}],outside:[{start:0,end:4,text:'abc'}],mismatch:[{start:0,end:1,text:'z'}],overlap:[{start:0,end:2,text:'ab'},{start:1,end:3,text:'bc'}],reversed:[{start:2,end:3,text:'c'},{start:0,end:1,text:'a'}]}))test('reject '+kind,()=>assert.throws(()=>validate('abc',spans),/Invalid evidence span/));

// Minimal DOM checks exercise literal text/code/mark nesting without a browser.
const dom={createElement(tag){return {tagName:tag,children:[],className:'',append(...children){this.children.push(...children)},get textContent(){return this.children.map(c=>typeof c==='string'?c:c.textContent).join('')},set textContent(value){this.children=[value]}}},createTextNode(text){return {textContent:text}}};
context.document=dom;
const U=context.window.EvidenceUI;
test('optional inline code preserves raw span coordinates and explicit tone',()=>{
 const text="Use `call_name` then 'quoted'.",spans=[{start:4,end:15,text:'`call_name`',tone:'before'}];
 const node=U.highlightedText(text,spans,{inlineCode:true}),mark=node.children.find(c=>c.tagName==='mark');
 assert.equal(node.textContent,"Use call_name then 'quoted'.");
 assert.equal(mark.className,'ev-mark-before');assert.equal(mark.children[0].tagName,'code');assert.equal(mark.textContent,'call_name');assert.equal(spans[0].text,'`call_name`');
 assert.equal(U.highlightedText(text,spans).textContent,text);
});
test('inline code supports a partial code span and a span crossing code boundaries',()=>{
 const text='A `alpha beta` Z';
 const partial=U.highlightedText(text,[{start:9,end:13,text:'beta'}],{inlineCode:true});
 assert.equal(partial.textContent,'A alpha beta Z');assert.equal(partial.children.find(c=>c.tagName==='mark').children[0].textContent,'beta');
 const whole=U.highlightedText(text,[{start:0,end:text.length,text}],{inlineCode:true});
 assert.equal(whole.children[0].textContent,'A alpha beta Z');assert.equal(whole.children[0].children.filter(c=>c.tagName==='code').length,1);
});
