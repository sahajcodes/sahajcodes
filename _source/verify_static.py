import re, hashlib, base64, io, sys, os, xml.etree.ElementTree as ET
from PIL import Image
R="/home/claude/profile"; names=["hero","about-life","stack","id-dashboard","connect"]
orig={"jpeg":hashlib.sha256(open("/mnt/user-data/uploads/id_png.jpg","rb").read()).hexdigest(),
      "png":hashlib.sha256(open("/mnt/user-data/uploads/right_pointing_png.png","rb").read()).hexdigest()}
allids={}; ok=True
def fail(m):
    global ok; ok=False; print("  FAIL:",m)
for n in names:
    s=open(f"{R}/assets/{n}.svg",encoding="utf-8").read()
    print(n, f"{len(s)/1024:.0f} KB")
    ET.fromstring(s)                                  # well-formed XML
    for bad in ["<script","foreignObject","javascript:","@import","<link","http://www.w3.org/1999/xhtml"]:
        if bad in s: fail(f"contains {bad}")
    # external references: only data: URIs, fragment refs, and the SVG/XLink namespaces
    for m in re.finditer(r'(?:xlink:href|href|src)="([^"]*)"',s):
        if not (m.group(1).startswith("data:") or m.group(1).startswith("#")): fail("external ref "+m.group(1)[:60])
    for m in re.finditer(r'url\(\s*([^)]+)\)',s):
        u=m.group(1).strip("'\" ")
        if not (u.startswith("#") or u.startswith("data:")): fail("external url() "+u[:60])
    if re.search(r'https?://',re.sub(r'xmlns(:\w+)?="[^"]*"','',s)): fail("http(s) string found in SVG: "+re.search(r'https?://[^\s"\')]+',re.sub(r'xmlns(:\w+)?="[^"]*"','',s)).group(0))
    ids=re.findall(r'\sid="([^"]+)"',s)
    if len(ids)!=len(set(ids)): fail("duplicate ids inside file")
    pref={i.split('-')[0] for i in ids}
    if len(pref)!=1: fail(f"mixed id prefixes {pref}")
    for i in ids:
        if i in allids: fail(f"id {i} also in {allids[i]}")
        allids[i]=n
    # fonts embedded
    ff=re.findall(r'url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)',s)
    print("  fonts:",len(ff),"woff2 faces;", "magic ok" if all(base64.b64decode(f)[:4]==b'wOF2' for f in ff) else "BAD MAGIC")
    if len(ff)!=4: fail("expected 4 embedded fonts")
    # animation rules: every finite animation must use fill-mode both
    css="".join(re.findall(r'<style>(.*?)</style>',s,flags=re.S)); css=re.sub(r'url\(data:[^)]*\)','',css)
    decls=re.findall(r'animation:([^;}]+)',css)
    for d in decls:
        if 'infinite' not in d and 'both' not in d and 'none' not in d: fail("finite animation w/o fill-mode both: "+d.strip()[:70])
    inl=re.findall(r'style="[^"]*animation-delay:[^"]*"',s)
    print(f"  {len(decls)} animation rules, {len(inl)} delayed elements; reduced-motion rule:", "prefers-reduced-motion" in css)
    if "prefers-reduced-motion" not in css: fail("no reduced-motion rule")
    if "SMIL" in s or "<animate" in s: print("  (uses SMIL)")
    # images byte-identity + alpha
    for mime,b in re.findall(r'data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)',s):
        raw=base64.b64decode(b); h=hashlib.sha256(raw).hexdigest()
        print("  image",mime,len(raw),"bytes sha256 match:",h==orig[mime])
        if h!=orig[mime]: fail("embedded image differs from original")
        if mime=="png":
            im=Image.open(io.BytesIO(raw)); a=im.getchannel("A"); print("   png",im.mode,im.size,"alpha",a.getextrema())
            if im.mode!="RGBA" or a.getextrema()!=(0,255): fail("alpha lost")
print("ids unique across all 5 files:",len(allids))
print("STATIC:", "PASS" if ok else "FAIL")
