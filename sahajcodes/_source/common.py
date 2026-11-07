"""Shared helpers: palette, font embedding, text measurement, icons, textures."""
import base64, json, os, math
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
SRC = os.path.join(ROOT, "src")

# ---- palette (from the Cherry x Matcha brief) ----
CHERRY, MATCHA = "#670626", "#BAD797"
DEEP, IVORY, SAGE, ROSE, TAUPE = "#3D071A", "#F7F3E8", "#8FAE75", "#D9A6AD", "#B9AE9B"

SERIF = "'Instrument Serif','Iowan Old Style','Palatino Linotype',Georgia,serif"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"

_fonts = {}
def _f(key):
    if key not in _fonts:
        fn = {"serif": "InstrumentSerif-Regular", "serifi": "InstrumentSerif-Italic",
              "mono": "JetBrainsMono-Regular", "monob": "JetBrainsMono-Bold"}[key]
        t = TTFont(os.path.join(SRC, fn + ".ttf"))
        _fonts[key] = (t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm)
    return _fonts[key]

def tw(text, font, size, ls=0.0):
    """Advance width of text (kerning ignored) in px."""
    cmap, hmtx, upm = _f(font)
    w = 0
    for ch in text:
        g = cmap.get(ord(ch))
        assert g, f"glyph missing in {font}: {ch!r} U+{ord(ch):04X}"
        w += hmtx[g][0]
    return w * size / upm + ls * len(text)

def b64file(path):
    return base64.b64encode(open(path, "rb").read()).decode()

def fontcss():
    def ff(fam, fn, wt, st):
        d = b64file(os.path.join(A, "fonts", fn))
        return (f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:{st};"
                f"src:url(data:font/woff2;base64,{d}) format('woff2');}}")
    return "".join([
        ff("Instrument Serif", "InstrumentSerif-Regular.subset.woff2", 400, "normal"),
        ff("Instrument Serif", "InstrumentSerif-Italic.subset.woff2", 400, "italic"),
        ff("JetBrains Mono", "JetBrainsMono-Regular.subset.woff2", 400, "normal"),
        ff("JetBrains Mono", "JetBrainsMono-Bold.subset.woff2", 700, "normal"),
    ])

ICONS = json.load(open(os.path.join(SRC, "icons.json")))
def icon(name, cx, cy, size, fill):
    """Brand glyph centred on (cx,cy), fitted into size x size."""
    ic = ICONS[name]
    _, _, w, h = [float(v) for v in ic["viewBox"].split()]
    s = size / max(w, h)
    tx, ty = cx - w * s / 2, cy - h * s / 2
    paths = "".join(f'<path d="{d}"/>' for d in ic["d"])
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})" fill="{fill}">{paths}</g>'

REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}"

def grain(p, w, h, rx, color="255 255 255", op=0.07, freq=0.85):
    r, g, b = [float(v) / 255 for v in color.split()]
    return (f'<filter id="{p}grain" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="2" seed="7" stitchTiles="stitch"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 {r:.3f}  0 0 0 0 {g:.3f}  0 0 0 0 {b:.3f}  0 0 0 0.9 -0.25"/></filter>',
            f'<rect width="{w}" height="{h}" rx="{rx}" filter="url(#{p}grain)" opacity="{op}"/>')

def dots(p, color, op, gap=14, r=1.1):
    return (f'<pattern id="{p}dots" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{gap/2}" cy="{gap/2}" r="{r}" fill="{color}" opacity="{op}"/></pattern>')

def svg_open(p, w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{p}t {p}d">'
            f'<title id="{p}t">{title}</title><desc id="{p}d">{desc}</desc>')

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
