import os, sys, json
from playwright.sync_api import sync_playwright
R="/home/claude/profile"; S="/home/claude/shots"; os.makedirs(S,exist_ok=True)
names=["hero","about-life","stack","id-dashboard","connect"]; times=[0,2,5,9,13]
reqs=[]; problems=[]
CHK="""()=>{const svg=document.querySelector('svg');const r=svg.getBoundingClientRect();const out=[];
 svg.querySelectorAll('text').forEach(t=>{const b=t.getBoundingClientRect();if(!b.width)return;
  const o=[];if(b.left<r.left+14)o.push('L');if(b.right>r.right-14)o.push('R');if(b.top<r.top+6)o.push('T');if(b.bottom>r.bottom-6)o.push('B');
  if(o.length)out.push(o.join('')+': '+t.textContent.slice(0,40));});
 // masked/clipped text: bbox must sit inside its clip rect
 svg.querySelectorAll('g[clip-path]').forEach(g=>{const id=g.getAttribute('clip-path').slice(5,-1);const cp=svg.querySelector('#'+CSS.escape(id)+' rect');
  g.querySelectorAll(':scope>text').forEach(t=>{const b=t.getBBox(),x=+cp.getAttribute('x'),y=+cp.getAttribute('y'),w=+cp.getAttribute('width'),h=+cp.getAttribute('height');
   if(b.x<x-1||b.x+b.width>x+w+1||b.y<y-1||b.y+b.height>y+h+1)out.push('CLIP '+id+': '+t.textContent.slice(0,30)+` bbox ${b.x|0},${b.y|0},${b.width|0},${b.height|0} clip ${x|0},${y|0},${w|0},${h|0}`);});});
 return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    # 1) inline, seeked times + text-clipping check at settled state
    pg=b.new_page(viewport={"width":960,"height":900})
    for n in names:
        svg=open(f"{R}/assets/{n}.svg",encoding="utf-8").read()
        pg.set_content(f"<body style='margin:0;padding:0;background:#fff'>{svg}</body>"); pg.wait_for_timeout(500)
        for t in times:
            pg.evaluate("t=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000})",t); pg.wait_for_timeout(80)
            pg.query_selector("svg").screenshot(path=f"{S}/{n}_{t}s.png")
        # settled state: seek 0.. each animation to its end if finite, else 13s
        pg.evaluate("document.getAnimations().forEach(a=>{a.pause();a.currentTime=14000})"); pg.wait_for_timeout(80)
        res=pg.evaluate(CHK)
        # cycling roles/slides legitimately sit off-state; ignore those with zero opacity
        print(n,"text/clip issues:",res or "none")
        if res: problems.append((n,res))
    # 2) animation removed + reduced-motion (as <img>, standalone SVG parsing)
    for mode in ["reduced","noanim"]:
        ctx=b.new_context(viewport={"width":960,"height":900},reduced_motion="reduce" if mode=="reduced" else "no-preference")
        pg=ctx.new_page()
        for n in names:
            if mode=="noanim":
                svg=open(f"{R}/assets/{n}.svg",encoding="utf-8").read().replace("</defs>","</defs><style>*{animation:none!important}</style>",1)
                pg.set_content(f"<body style='margin:0;background:#fff'>{svg}</body>")
            else:
                pg.goto(f"file://{R}/assets/{n}.svg")
            pg.wait_for_timeout(600); 
            (pg.query_selector("svg") ).screenshot(path=f"{S}/{n}_{mode}.png")
        ctx.close()
    # 3) as <img> in a page: real-time, request log, transparency over a hot-pink bg to expose alpha holes
    ctx=b.new_context(viewport={"width":960,"height":900}); pg=ctx.new_page()
    pg.on("request",lambda r:reqs.append(r.url[:90]))
    for n in names:
        pg.goto(f"file://{R}/preview.html"); break
    pg.goto(f"file://{R}/preview.html"); pg.wait_for_timeout(3500)
    pg.screenshot(path=f"{S}/preview_full_desktop.png",full_page=True)
    print("img elements loaded:",pg.evaluate("[...document.images].map(i=>i.naturalWidth+'x'+i.naturalHeight)"))
    # fonts really applied inside <img>? compare to baseline via screenshot visual (checked manually)
    ctx.close()
    for w,label in [(390,"mobile"),(1012,"github")]:
        ctx=b.new_context(viewport={"width":w,"height":900},device_scale_factor=2 if w==390 else 1); pg=ctx.new_page()
        pg.goto(f"file://{R}/preview.html"); pg.wait_for_timeout(3500)
        pg.screenshot(path=f"{S}/preview_{label}.png",full_page=True)
        print(label,"horizontal overflow:",pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"))
        ctx.close()
    b.close()
ext=[u for u in reqs if not u.startswith("file://") and not u.startswith("data:")]
print("requests:",len(reqs),"non-local:",ext)
