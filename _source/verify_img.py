import time
from playwright.sync_api import sync_playwright
R="/home/claude/profile"; S="/home/claude/shots"
names=["hero","about-life","stack","id-dashboard","connect"]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":920,"height":3700})
    html=("<body style='margin:0;padding:10px;background:#fff'>"+"".join(f"<img id='i{i}' src='assets/{n}.svg?v=1' style='display:block;width:900px;margin-bottom:10px'>" for i,n in enumerate(names))+"</body>")
    open(f"{R}/_imgtest.html","w").write(html); pg.goto(f"file://{R}/_imgtest.html"); pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
    t0=time.time()
    for t in [0.6,2,5,9,13]:
        d=t-(time.time()-t0)
        if d>0: time.sleep(d)
        for i,n in enumerate(names):
            pg.query_selector(f"#i{i}").screenshot(path=f"{S}/{n}_img_{t:g}s.png")
        print("shot",t,flush=True)
    b.close()
