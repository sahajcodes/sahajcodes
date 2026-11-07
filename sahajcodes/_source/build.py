import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import importlib
names = sys.argv[1:] or ["hero","about","stack","id","connect"]
out = {"hero":"hero.svg","about":"about-life.svg","stack":"stack.svg","id":"id-dashboard.svg","connect":"connect.svg"}
for n in names:
    m = importlib.import_module(n)
    svg = m.build()
    path = os.path.join(A, out[n]); open(path, "w", encoding="utf-8").write(svg)
    print(out[n], round(len(svg)/1024), "KB")
