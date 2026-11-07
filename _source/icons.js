const React=require('/opt/npm-tools/node_modules/react');const S=require('/opt/npm-tools/node_modules/react-dom/server');
const si=require('/opt/npm-tools/node_modules/react-icons/si'),vsc=require('/opt/npm-tools/node_modules/react-icons/vsc'),fa6=require('/opt/npm-tools/node_modules/react-icons/fa6');
const want={cpp:si.SiCplusplus,python:si.SiPython,javascript:si.SiJavascript,html5:si.SiHtml5,css:si.SiCss,flask:si.SiFlask,bootstrap:si.SiBootstrap,git:si.SiGit,github:si.SiGithub,leetcode:si.SiLeetcode,vscode:vsc.VscVscode,linkedin:fa6.FaLinkedin};
const out={};
for(const k in want){const m=S.renderToStaticMarkup(React.createElement(want[k]));const vb=m.match(/viewBox="([^"]+)"/)[1];const ds=[...m.matchAll(/ d="([^"]+)"/g)].map(x=>x[1]);out[k]={viewBox:vb,d:ds};console.log(k,vb,ds.length,ds.join('').length);}
require('fs').writeFileSync(__dirname+'/icons.json',JSON.stringify(out));
