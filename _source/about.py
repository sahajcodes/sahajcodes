from common import *

def wrap(text, font, size, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if tw(t, font, size) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def lines_svg(lines, x, y, lh, attrs):
    return "".join(f'<text x="{x}" y="{y + i*lh:.1f}" {attrs}>{esc(l)}</text>' for i, l in enumerate(lines))

def art_network():
    nodes = [(26, 104), (74, 46), (132, 92), (186, 36), (238, 78), (112, 128), (206, 122), (262, 30)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (2, 6), (4, 6), (3, 7), (0, 5), (4, 7)]
    s = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{MATCHA}" stroke-opacity=".42" stroke-width="1.2"/>' for a, b in edges)
    for i, (x, y) in enumerate(nodes):
        if i == 2:
            s += (f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="{IVORY}" stroke-opacity=".5" class="a-tw" style="animation-delay:.2s"/>'
                  f'<circle cx="{x}" cy="{y}" r="8" fill="{IVORY}"/>')
        else:
            s += f'<circle cx="{x}" cy="{y}" r="4.6" fill="{MATCHA}" class="a-tw" style="animation-delay:{(i*0.37)%2:.2f}s"/>'
    return s

def art_creative():
    return (f'<g class="a-fl1"><circle cx="86" cy="68" r="42" fill="{MATCHA}" fill-opacity=".92"/></g>'
            f'<g class="a-fl2"><rect x="106" y="36" width="78" height="78" rx="14" fill="{ROSE}" fill-opacity=".88" transform="rotate(14 145 75)"/></g>'
            f'<g class="a-fl1"><path d="M196,118 L232,48 L268,118 Z" fill="none" stroke="{IVORY}" stroke-width="1.6" stroke-linejoin="round"/></g>'
            f'<path d="M20,128 H268" stroke="{IVORY}" stroke-opacity=".28" stroke-dasharray="2 6" stroke-linecap="round"/>'
            f'<g transform="translate(206 84)"><g class="a-fl2"><path d="M0,0 L0,24 L7,18 L12,29 L17,27 L12,16 L21,16 Z" fill="{IVORY}"/></g></g>')

def art_learn():
    steps = ""
    for i in range(5):
        x = 20 + i * 52; h = 22 + i * 20
        steps += (f'<rect x="{x}" y="{136-h}" width="48" height="{h}" rx="4" fill="{IVORY}" fill-opacity="{.10 + i*.03:.2f}"/>'
                  f'<rect x="{x}" y="{136-h}" width="48" height="2.5" rx="1.2" fill="{MATCHA}"/>')
    flag = (f'<g transform="translate(246 12)"><path d="M0,0 V34" stroke="{IVORY}" stroke-width="1.6"/>'
            f'<path d="M1,2 H22 L16,9 L22,16 H1 Z" fill="{ROSE}"/></g>')
    path = f'<path d="M44,92 C70,60 92,66 118,56 S164,48 196,36 S232,22 246,18" fill="none" stroke="{MATCHA}" stroke-width="1.4" stroke-dasharray="3 6" stroke-linecap="round"/>'
    star = f'<g transform="translate(272 22)"><g class="a-tw2"><path d="M0,-7 Q1,-1 7,0 Q1,1 0,7 Q-1,1 -7,0 Q-1,-1 0,-7z" fill="{MATCHA}"/></g></g>'
    return steps + path + flag + star

def build():
    p = "a-"
    W, H = 900, 640
    LW = 414
    # ---- left column typography ----
    hs = 56.0
    while tw("engineer by practice.", "serifi", hs) > LW - 6: hs -= 0.5
    intro = ("I\u2019m an aspiring software engineer and student developer from Panchkula, Haryana. "
             "I enjoy turning ideas into working applications, learning by building, and solving problems one step at a time.")
    il = wrap(intro, "serif", 19.5, LW)
    base1, base2 = 148, 148 + hs * 0.98
    iy = base2 + 50
    cy0 = iy + len(il) * 28 + 26
    caps = [("01", "Problem solving", "C++ \u00b7 Python \u00b7 DSA practice"),
            ("02", "Web development", "HTML5 \u00b7 CSS3 \u00b7 JavaScript \u00b7 Flask \u00b7 Bootstrap"),
            ("03", "Building real-world apps", "From idea to working project"),
            ("04", "Version control", "Git \u00b7 GitHub \u00b7 VS Code")]
    cap_svg = ""
    for i, (n, t, d) in enumerate(caps):
        y = cy0 + 38 + i * 44
        cap_svg += (f'<g class="a-up" style="animation-delay:{1.0 + i*0.14:.2f}s">'
                    f'<text x="56" y="{y}" font-family="{MONO}" font-size="11" fill="{SAGE}" font-weight="700">{n}</text>'
                    f'<text x="92" y="{y}" font-family="{SERIF}" font-size="23" fill="{CHERRY}">{esc(t)}</text>'
                    f'<text x="92" y="{y+15}" font-family="{MONO}" font-size="9.5" fill="{CHERRY}" fill-opacity=".6">{esc(d)}</text>'
                    f'<rect x="56" y="{y+23}" width="{LW}" height="1" fill="{CHERRY}" fill-opacity=".13"/></g>')

    # ---- carousel ----
    cx, cyy, cw, ch = 500, 100, 344, 484
    slides = [
        ("01", "Emerging tech & AI", "Exploring emerging technologies and AI, and where they are heading next.", art_network(), "AI"),
        ("02", "Creative digital projects", "Building creative digital projects that turn ideas into something people can use.", art_creative(), "CREATE"),
        ("03", "Learning & problem-solving", "Learning, experimenting and problem-solving, one small experiment at a time.", art_learn(), "LEARN"),
    ]
    sl = ""
    for i, (n, t, d, art, _) in enumerate(slides):
        tl = wrap(t, "serif", 36, 288)
        dl = wrap(d, "serif", 17, 288)
        sl += (f'<g class="a-slide a-s{i}" style="animation-delay:{4*i}s">'
               f'<g transform="translate(28 66)">{art}</g>'
               f'<text x="28" y="262" font-family="{SERIF}" font-style="italic" font-size="20" fill="{MATCHA}">{n}</text>'
               + lines_svg(tl, 28, 306, 38, f'font-family="{SERIF}" font-size="36" fill="{IVORY}"')
               + lines_svg(dl, 28, 306 + 38 * 1 + 38 + 8 if len(tl) > 1 else 306 + 38 + 8, 24, f'font-family="{SERIF}" font-size="17" fill="{IVORY}" fill-opacity=".78"')
               + '</g>')
    cnt = "".join(f'<text class="a-fade a-c{i}" x="{cw-28}" y="38" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{IVORY}" fill-opacity=".8" style="animation-delay:{4*i}s">0{i+1} / 03</text>' for i in range(3))
    segw = (cw - 56 - 16) / 3
    segs, labs = "", ""
    for i, s in enumerate(slides):
        x = 28 + i * (segw + 8)
        segs += (f'<rect x="{x:.1f}" y="426" width="{segw:.1f}" height="4" rx="2" fill="{IVORY}" fill-opacity=".2"/>'
                 f'<g transform="translate({x:.1f} 426)"><rect class="a-fill a-f{i}" width="{segw:.1f}" height="4" rx="2" fill="{MATCHA}" style="transform-origin:0 0;transform:scaleX({1 if i==0 else 0})"/></g>')
        labs += f'<text class="a-lab a-l{i}" x="{x:.1f}" y="452" font-family="{MONO}" font-size="9.5" letter-spacing="2" fill="{IVORY}" style="animation-delay:{4*i}s{";opacity:1" if i==0 else ""}">{s[4]}</text>'

    gr_def, gr_use = grain(p, W, H, 28, "60 7 26", 0.03)
    css = f"""
.a-up{{animation:a-up .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes a-up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.a-rise{{animation:a-rise 1.1s cubic-bezier(.16,.84,.24,1) both}}
@keyframes a-rise{{from{{transform:translateY({hs*1.1:.0f}px)}}to{{transform:translateY(0)}}}}
.a-draw{{animation:a-draw 1s cubic-bezier(.6,0,.2,1) both}}
@keyframes a-draw{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.a-card{{animation:a-card 1s cubic-bezier(.2,.7,.2,1) .25s both}}
@keyframes a-card{{from{{opacity:0;transform:translateY(22px)}}to{{opacity:1;transform:translateY(0)}}}}
.a-slide{{opacity:0;animation:a-slide 12s cubic-bezier(.3,.7,.3,1) infinite both}}
.a-s0{{opacity:1}}
@keyframes a-slide{{0%{{opacity:0;transform:translateX(30px)}}3.6%{{opacity:1;transform:translateX(0)}}29.5%{{opacity:1;transform:translateX(0)}}33.3%{{opacity:0;transform:translateX(-30px)}}100%{{opacity:0;transform:translateX(-30px)}}}}
.a-fade{{opacity:0;animation:a-fade 12s linear infinite both}}
.a-c0{{opacity:.8}}
@keyframes a-fade{{0%{{opacity:0}}3.6%{{opacity:1}}29.5%{{opacity:1}}33.3%{{opacity:0}}100%{{opacity:0}}}}
.a-lab{{opacity:.38;animation:a-lab 12s linear infinite both}}
@keyframes a-lab{{0%{{opacity:.38}}3.6%{{opacity:1}}29.5%{{opacity:1}}33.3%{{opacity:.38}}100%{{opacity:.38}}}}
.a-f0{{animation:a-f0 12s linear infinite both}}.a-f1{{animation:a-f1 12s linear infinite both}}.a-f2{{animation:a-f2 12s linear infinite both}}
@keyframes a-f0{{0%{{transform:scaleX(0)}}33.3%{{transform:scaleX(1)}}100%{{transform:scaleX(1)}}}}
@keyframes a-f1{{0%,33.3%{{transform:scaleX(0)}}66.6%{{transform:scaleX(1)}}100%{{transform:scaleX(1)}}}}
@keyframes a-f2{{0%,66.6%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}
.a-tw{{animation:a-tw 2.6s ease-in-out infinite alternate}}
@keyframes a-tw{{from{{opacity:.35}}to{{opacity:1}}}}
.a-tw2{{animation:a-tw2 3.4s ease-in-out infinite alternate}}
@keyframes a-tw2{{from{{transform:rotate(-14deg) scale(.8)}}to{{transform:rotate(14deg) scale(1.15)}}}}
.a-fl1{{animation:a-fl 5s ease-in-out infinite alternate}}.a-fl2{{animation:a-fl 6.5s ease-in-out -2s infinite alternate}}
@keyframes a-fl{{from{{transform:translateY(-4px)}}to{{transform:translateY(5px)}}}}
"""
    css += REDUCED

    # name block: masks
    clip1 = f'<clipPath id="{p}c1"><rect x="40" y="{base1-hs*0.8:.1f}" width="460" height="{hs*1.1:.1f}"/></clipPath>'
    clip2 = f'<clipPath id="{p}c2"><rect x="40" y="{base2-hs*0.8:.1f}" width="460" height="{hs*1.15:.1f}"/></clipPath>'
    w2 = tw("engineer by practice.", "serifi", hs)

    return svg_open(p, W, H, "About Sahajpreet Kaur",
        "Editorial about section: introduction, core capabilities and an auto-advancing three-slide interests carousel.") + f"""
<defs><style>{fontcss()}{css}</style>
<linearGradient id="{p}gb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}"/><stop offset=".5" stop-color="{ROSE}"/><stop offset="1" stop-color="{MATCHA}" stop-opacity=".4"/></linearGradient>
<linearGradient id="{p}edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CHERRY}" stop-opacity=".55"/><stop offset=".5" stop-color="{SAGE}" stop-opacity=".5"/><stop offset="1" stop-color="{CHERRY}" stop-opacity=".45"/></linearGradient>
<linearGradient id="{p}card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a0b2e"/><stop offset=".6" stop-color="{CHERRY}"/><stop offset="1" stop-color="{DEEP}"/></linearGradient>
<filter id="{p}sh" x="-20%" y="-10%" width="140%" height="130%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="{DEEP}" flood-opacity=".28"/></filter>
{dots(p, SAGE, .5)}{gr_def}
<clipPath id="{p}outer"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="{p}cardclip"><rect width="{cw}" height="{ch}" rx="28"/></clipPath>
{clip1}{clip2}
</defs>
<g clip-path="url(#{p}outer)"><rect width="{W}" height="{H}" fill="{IVORY}"/>
<rect x="470" y="0" width="430" height="{H}" fill="url(#{p}dots)" opacity=".55"/>
<circle cx="880" cy="40" r="120" fill="{MATCHA}" fill-opacity=".35"/>
{gr_use}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="27.5" fill="none" stroke="url(#{p}edge)" stroke-width="1.5"/>

<g class="a-up" style="animation-delay:.05s">
<text x="56" y="54" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{CHERRY}">02 \u2014 ABOUT</text>
<text x="844" y="54" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{CHERRY}" fill-opacity=".55">PANCHKULA \u00b7 INDIA</text></g>
<g transform="translate(56 72)"><rect class="a-draw" width="788" height="1" fill="{CHERRY}" fill-opacity=".22" style="transform-origin:0 0;animation-delay:.1s"/></g>

<g transform="translate(56 {base2-hs*0.5:.1f})"><rect class="a-draw" width="{w2+10:.1f}" height="{hs*0.36:.1f}" rx="5" fill="{MATCHA}" fill-opacity=".85" style="transform-origin:0 0;animation-delay:1.0s"/></g>
<g clip-path="url(#{p}c1)"><text class="a-rise" x="54" y="{base1}" font-family="{SERIF}" font-size="{hs}" fill="{CHERRY}" style="animation-delay:.3s">Curious by nature,</text></g>
<g clip-path="url(#{p}c2)"><text class="a-rise" x="54" y="{base2:.1f}" font-family="{SERIF}" font-style="italic" font-size="{hs}" fill="{CHERRY}" style="animation-delay:.5s">engineer by practice.</text></g>
<g class="a-up" style="animation-delay:.8s">{lines_svg(il, 56, iy, 28, f'font-family="{SERIF}" font-size="19.5" fill="{DEEP}" fill-opacity=".86"')}</g>
<text class="a-up" x="56" y="{cy0}" font-family="{MONO}" font-size="10.5" letter-spacing="3" fill="{CHERRY}" fill-opacity=".7" style="animation-delay:.95s">CORE CAPABILITIES</text>
{cap_svg}

<g class="a-card"><g transform="translate({cx} {cyy})">
<g filter="url(#{p}sh)"><rect width="{cw}" height="{ch}" rx="28" fill="url(#{p}card)"/></g>
<rect x=".75" y=".75" width="{cw-1.5}" height="{ch-1.5}" rx="27.3" fill="none" stroke="url(#{p}gb)" stroke-width="1.5"/>
<g clip-path="url(#{p}cardclip)"><rect width="{cw}" height="{ch}" fill="url(#{p}dots)" opacity=".18"/></g>
<text x="28" y="38" font-family="{MONO}" font-size="10.5" letter-spacing="3" fill="{MATCHA}">INTERESTS</text>
{cnt}
<rect x="28" y="52" width="{cw-56}" height="1" fill="{IVORY}" fill-opacity=".14"/>
{sl}
{segs}{labs}
</g></g>
</svg>"""
