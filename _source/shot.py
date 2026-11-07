"""Render helper: inline-seek screenshots. usage: shot.py name t1 t2 ..."""
import sys, os
from playwright.sync_api import sync_playwright
ROOT="/home/claude/profile"; name=sys.argv[1]; times=[float(t) for t in sys.argv[2:]] or [0,2,5,9,13]
svg=open(f"{ROOT}/assets/{name}.svg",encoding="utf-8").read()
os.makedirs("/home/claude/shots",exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":960,"height":900})
    pg.set_content(f"<body style='margin:0;background:#ddd;padding:20px'>{svg}</body>"); pg.wait_for_timeout(600)
    for t in times:
        pg.evaluate("""t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});}""",t)
        pg.wait_for_timeout(120)
        el=pg.query_selector("svg"); el.screenshot(path=f"/home/claude/shots/{name}_{t:g}s.png")
    b.close()
print("ok")
