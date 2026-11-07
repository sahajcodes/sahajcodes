from common import *
import json

def flow(items, x0, y0, width, size=11.5, h=30, gap=8, delay0=1.2, step=0.07, style="solid", color=MATCHA):
    """Lay chips out in wrapping rows. items: (label, icon_name|None)."""
    x, y, out, n = x0, y0, "", 0
    for label, ic in items:
        w = 14 + (22 if ic else 0) + tw(label, "mono", size) + 14
        if x + w > x0 + width and x > x0:
            x = x0; y += h + gap
        d = f"{delay0 + n*step:.2f}s"; n += 1
        dash = ' stroke-dasharray="3 3"' if style == "dashed" else ""
        fillop = ".0" if style == "dashed" else ".10"
        out += (f'<g class="s-up" style="animation-delay:{d}">'
                f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity="{fillop}" stroke="{color}" stroke-opacity=".5"{dash}/>')
        tx = x + 14
        if ic:
            out += icon(ic, x + 14 + 7, y + h / 2, 14, color); tx = x + 14 + 22
        out += f'<text x="{tx:.1f}" y="{y + h/2 + 4:.1f}" font-family="{MONO}" font-size="{size}" fill="{IVORY}">{esc(label)}</text></g>'
        x += w + gap
    return out, y + h

def build():
    p = "s-"
    W = 900
    CX, CY = 450, 382
    PH = json.load(open(os.path.join(SRC, "phases.json")))
    T = 40.0   # orbit period base
    orbits = [
        # name, tilt, rx, ry, colour, period, direction, dash, items
        ("Languages",  -20, 336, 92, MATCHA, 44, 1, "", [("C++", "cpp"), ("Python", "python"), ("JavaScript", "javascript"), ("HTML5", "html5"), ("CSS3", "css")]),
        ("Frameworks",  20, 336, 92, ROSE,   44, 1, "", [("Flask", "flask"), ("Bootstrap", "bootstrap")]),
        ("Tools",        0, 238, 70, TAUPE,  44, 1, "3 5", [("Git", "git"), ("GitHub", "github"), ("VS Code", "vscode")]),
    ]
    css = ["""
.s-up{animation:s-up .8s cubic-bezier(.2,.7,.2,1) both}
@keyframes s-up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.s-fade{animation:s-fade 1.2s ease both}
@keyframes s-fade{from{opacity:0}to{opacity:1}}
.s-rise{animation:s-rise 1.1s cubic-bezier(.16,.84,.24,1) both}
@keyframes s-rise{from{transform:translateY(70px)}to{transform:translateY(0)}}
.s-draw{animation:s-draw 1s cubic-bezier(.6,0,.2,1) both}
@keyframes s-draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.s-spin{animation:s-spin 40s linear infinite}
@keyframes s-spin{to{transform:rotate(360deg)}}
.s-pulse{animation:s-pulse 3.2s ease-in-out infinite alternate}
@keyframes s-pulse{from{opacity:.35}to{opacity:1}}
"""]
    orb_svg, icon_svg = "", ""
    ease = "cubic-bezier(.37,0,.63,1)"
    k = 0
    for oi, (nm, tilt, rx, ry, col, per, rev, dash, items) in enumerate(orbits):
        css.append(f"@keyframes s-x{oi}{{from{{transform:translateX({-rx}px)}}to{{transform:translateX({rx}px)}}}}"
                   f"@keyframes s-y{oi}{{from{{transform:translateY({-ry}px)}}to{{transform:translateY({ry}px)}}}}"
                   f".s-ox{oi}{{animation:s-x{oi} {per/2}s {ease} infinite alternate}}"
                   f".s-oy{oi}{{animation:s-y{oi} {per/2}s {ease} infinite alternate}}")
        da = f' stroke-dasharray="{dash}"' if dash else ""
        orb_svg += (f'<g transform="translate({CX} {CY}) rotate({tilt})"><ellipse class="s-fade" style="animation-delay:{.3+oi*.25:.2f}s" rx="{rx}" ry="{ry}" fill="none" stroke="{col}" stroke-opacity=".55" stroke-width="1.3"{da}/></g>')
        inner = ""
        n = len(items)
        for ii, (label, ic) in enumerate(items):
            phi = PH[k]
            x0 = -rx * math.cos(phi); y0 = rev * ry * math.sin(phi)
            dx = -(phi / (2 * math.pi)) * per
            dy = dx - per / 4 - (0 if rev == 1 else per / 2)
            inner += (f'<g class="s-fade" style="animation-delay:{1.0+k*.12:.2f}s"><g class="s-ox{oi}" style="transform:translateX({x0:.2f}px);animation-delay:{dx:.2f}s">'
                      f'<g class="s-oy{oi}" style="transform:translateY({y0:.2f}px);animation-delay:{dy:.2f}s">'
                      f'<g transform="rotate({-tilt})">'
                      f'<circle r="27" fill="{DEEP}" fill-opacity=".55"/><circle r="25" fill="{IVORY}" stroke="{col}" stroke-width="1.6"/>'
                      f'{icon(ic, 0, 0, 27, CHERRY)}'
                      f'<text y="45" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="{IVORY}" stroke="{DEEP}" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke">{esc(label)}</text>'
                      f'</g></g></g></g>')
            k += 1
        icon_svg += f'<g transform="translate({CX} {CY}) rotate({tilt})">{inner}</g>'

    # ---- chip columns ----
    cy0 = 626
    cols = [(56, 232), (56 + 232 + 28, 196), (56 + 232 + 28 + 196 + 28, 788 - 232 - 196 - 56)]
    heads = [("LANGUAGES", MATCHA), ("FRAMEWORKS", ROSE), ("TOOLS & CURRENTLY EXPLORING", TAUPE)]
    chip_svg, bottoms = "", []
    for ci, ((x, w), (ht, col)) in enumerate(zip(cols, heads)):
        chip_svg += (f'<g class="s-up" style="animation-delay:.9s"><circle cx="{x+4}" cy="{cy0}" r="3.5" fill="{col}"/>'
                     f'<text x="{x+16}" y="{cy0+4}" font-family="{MONO}" font-size="10.5" letter-spacing="2.5" fill="{IVORY}" fill-opacity=".75">{esc(ht)}</text>'
                     f'<rect x="{x}" y="{cy0+16}" width="{w}" height="1" fill="{IVORY}" fill-opacity=".18"/></g>')
    c1, b1 = flow([("C++", "cpp"), ("Python", "python"), ("JavaScript", "javascript"), ("HTML5", "html5"), ("CSS3", "css")], cols[0][0], cy0 + 32, cols[0][1], color=MATCHA, delay0=1.5)
    c2, b2 = flow([("Flask", "flask"), ("Bootstrap", "bootstrap")], cols[1][0], cy0 + 32, cols[1][1], color=ROSE, delay0=1.9)
    c3a, b3a = flow([("Git", "git"), ("GitHub", "github"), ("VS Code", "vscode")], cols[2][0], cy0 + 32, cols[2][1], color=TAUPE, delay0=2.1)
    ly = b3a + 24
    c3l = f'<text class="s-up" x="{cols[2][0]}" y="{ly}" font-family="{MONO}" font-size="9.5" letter-spacing="2.5" fill="{MATCHA}" style="animation-delay:2.4s">NOW EXPLORING</text>'
    c3b, b3 = flow([("DSA", None), ("OOP", None), ("Backend Development", None), ("Artificial Intelligence", None)], cols[2][0], ly + 12, cols[2][1], size=10.5, h=28, color=MATCHA, style="dashed", delay0=2.5)
    chip_svg += c1 + c2 + c3a + c3l + c3b
    H = int(max(b1, b2, b3) + 44)

    gr_def, gr_use = grain(p, W, H, 28, "255 255 255", 0.05)
    css.append(REDUCED)
    return svg_open(p, W, H, "Technology stack",
        "Three tilted elliptical orbits carry brand icons for languages, frameworks and tools, with grouped chips below.") + f"""
<defs><style>{fontcss()}{''.join(css)}</style>
<radialGradient id="{p}bg" cx="50%" cy="42%" r="75%"><stop offset="0" stop-color="#6e0b2f"/><stop offset=".55" stop-color="#4d0a24"/><stop offset="1" stop-color="{DEEP}"/></radialGradient>
<linearGradient id="{p}edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}" stop-opacity=".7"/><stop offset=".5" stop-color="{ROSE}" stop-opacity=".25"/><stop offset="1" stop-color="{MATCHA}" stop-opacity=".6"/></linearGradient>
{dots(p, MATCHA, .2)}{gr_def}
<clipPath id="{p}outer"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="{p}c1"><rect x="40" y="96" width="460" height="64"/></clipPath>
<clipPath id="{p}c2"><rect x="40" y="152" width="460" height="64"/></clipPath>
</defs>
<g clip-path="url(#{p}outer)"><rect width="{W}" height="{H}" fill="url(#{p}bg)"/>
<rect x="0" y="230" width="{W}" height="320" fill="url(#{p}dots)"/>{gr_use}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="27.5" fill="none" stroke="url(#{p}edge)" stroke-width="1.5"/>

<g class="s-up" style="animation-delay:.05s">
<text x="56" y="54" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MATCHA}">03 \u2014 TOOLKIT</text>
<text x="844" y="54" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{IVORY}" fill-opacity=".6">LANGUAGES \u00b7 FRAMEWORKS \u00b7 TOOLS</text></g>
<g transform="translate(56 72)"><rect class="s-draw" width="788" height="1" fill="{IVORY}" fill-opacity=".22" style="transform-origin:0 0;animation-delay:.1s"/></g>
<g clip-path="url(#{p}c1)"><text class="s-rise" x="54" y="150" font-family="{SERIF}" font-size="68" fill="{IVORY}" style="animation-delay:.3s">The tools I</text></g>
<g clip-path="url(#{p}c2)"><text class="s-rise" x="54" y="206" font-family="{SERIF}" font-style="italic" font-size="68" fill="{MATCHA}" style="animation-delay:.5s">build with.</text></g>

{orb_svg}
<g transform="translate({CX} {CY})">
<g class="s-spin"><circle r="44" fill="none" stroke="{MATCHA}" stroke-opacity=".5" stroke-dasharray="2 7" stroke-linecap="round"/></g>
<circle r="32" fill="{CHERRY}" stroke="{MATCHA}" stroke-width="1.4"/>
<circle r="32" fill="none" stroke="{MATCHA}" stroke-opacity=".35" class="s-pulse" transform="scale(1.2)"/>
<text y="6" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{MATCHA}">&lt;/&gt;</text></g>
{icon_svg}
{chip_svg}
</svg>"""
