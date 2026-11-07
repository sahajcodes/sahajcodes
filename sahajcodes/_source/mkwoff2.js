// Minimal WOFF2 encoder (null glyf/loca transform, brotli via node zlib)
const fs=require('fs'),zlib=require('zlib');
const KNOWN=['cmap','head','hhea','hmtx','maxp','name','OS/2','post','cvt ','fpgm','glyf','loca','prep','CFF ','VORG','EBDT','EBLC','gasp','hdmx','kern','LTSH','PCLT','VDMX','vhea','vmtx','BASE','GDEF','GPOS','GSUB','EBSC','JSTF','MATH','CBDT','CBLC','COLR','CPAL','SVG ','sbix','acnt','avar','bdat','bloc','bsln','cvar','fdsc','feat','fmtx','fvar','gvar','hsty','just','lcar','mort','morx','opbd','prop','trak','Zapf','Silf','Glat','Gloc','Feat','Sill'];
function b128(n){const o=[];do{o.unshift(n&0x7f);n=Math.floor(n/128);}while(n>0);for(let i=0;i<o.length-1;i++)o[i]|=0x80;return Buffer.from(o);}
const [,,inp,outp]=process.argv;
const sfnt=fs.readFileSync(inp);
const flavor=sfnt.readUInt32BE(0),n=sfnt.readUInt16BE(4);
let tabs=[];
for(let i=0;i<n;i++){const o=12+16*i;tabs.push({tag:sfnt.toString('latin1',o,o+4),off:sfnt.readUInt32BE(o+8),len:sfnt.readUInt32BE(o+12)});}
tabs.sort((a,b)=>a.tag<b.tag?-1:1);
const gi=tabs.findIndex(t=>t.tag==='glyf'),li=tabs.findIndex(t=>t.tag==='loca');
if(gi>=0){const [l]=tabs.splice(li,1);tabs.splice(tabs.findIndex(t=>t.tag==='glyf')+1,0,l);}
let dir=[],data=[],sfntSize=12+16*tabs.length;
for(const t of tabs){
  const ki=KNOWN.indexOf(t.tag);let flags=ki>=0?ki:63;
  if(t.tag==='glyf'||t.tag==='loca')flags|=0xC0;
  dir.push(Buffer.from([flags]));if(ki<0)dir.push(Buffer.from(t.tag,'latin1'));
  dir.push(b128(t.len));
  data.push(sfnt.subarray(t.off,t.off+t.len));sfntSize+=(t.len+3)&~3;
}
const raw=Buffer.concat(data);
const comp=zlib.brotliCompressSync(raw,{params:{[zlib.constants.BROTLI_PARAM_MODE]:zlib.constants.BROTLI_MODE_FONT,[zlib.constants.BROTLI_PARAM_QUALITY]:11,[zlib.constants.BROTLI_PARAM_SIZE_HINT]:raw.length}});
const dirB=Buffer.concat(dir);
let total=48+dirB.length+comp.length;const pad=(4-total%4)%4;total+=pad;
const h=Buffer.alloc(48);h.write('wOF2',0,'latin1');h.writeUInt32BE(flavor,4);h.writeUInt32BE(total,8);h.writeUInt16BE(tabs.length,12);h.writeUInt32BE(sfntSize,16);h.writeUInt32BE(comp.length,20);h.writeUInt16BE(1,24);
fs.writeFileSync(outp,Buffer.concat([h,dirB,comp,Buffer.alloc(pad)]));
console.log(outp,total,'bytes');
