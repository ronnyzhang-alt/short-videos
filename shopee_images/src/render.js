const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const n of process.argv.slice(2)){const p=await b.newPage({viewport:{width:1080,height:800}});
await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.waitForLoadState('networkidle');
await p.screenshot({path:n+'.jpg',type:'jpeg',quality:92,fullPage:true});console.log(n,'ok');}
await b.close()})();
