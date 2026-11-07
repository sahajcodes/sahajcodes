from common import *
import random

def wrapl(text, font, size, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if tw(t, font, size) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def barcode(x, y, w, h, seed="SAHAJCODES"):
    rnd = random.Random(seed)
    out, cx = "", x
    while cx < x + w - 1:
        bw = rnd.choice([1, 1, 1.6, 2.2, 3])
        gap = rnd.choice([1.2, 1.6, 2.2])
        if cx + bw > x + w: break
        out += f'<rect x="{cx:.1f}" y="{y}" width="{bw}" height="{h}" fill="{IVORY}"/>'
        cx += bw + gap
    return out

def guilloche(w, y0, y1, n=11):
    out = ""
    for k in range(n):
        yy = y0 + (y1 - y0) * k / (n - 1)
        pts = " ".join(f"{x:.0f},{yy + 5 * math.sin(x / 22 + k * .55):.1f}" for x in range(0, int(w) + 8, 8))
        out += f'<polyline points="{pts}" fill="none" stroke="{IVORY}" stroke-opacity=".055" stroke-width=".8"/>'
    return out

def pend_keyframes(P=3.4, A0=7.0, tau=1.9, total=7.5, n=40):
    kf = ""
    for i in range(n + 1):
        t = total * i / n
        th = A0 * math.exp(-t / tau) * math.sin(2 * math.pi * t / P)
        kf += f"{100*i/n:.2f}%{{transform:rotate({th:.3f}deg)}}"
    kb = ""
    for i in range(25):
        th = 1.7 * math.sin(2 * math.pi * i / 24)
        kb += f"{100*i/24:.2f}%{{transform:rotate({th:.3f}deg)}}"
    return kf, kb

def build():
    p = "d-"
    W, H = 900, 730
    PX = 270            # pivot x
    img = b64file(os.path.join(A, "img", "id.jpg"))
    cx, cy, cw, ch = 135, 172, 270, 478     # card box
    kfa, kfb = pend_keyframes()
    t_impact = 0.15 + 1.1 * 0.75

    # -------- card interior (local coords) --------
    # portrait window
    wx, wy, ww, wh = 24, 70, 222, 180
    name_s = 40
    card = f"""
<rect width="{cw}" height="{ch}" rx="26" fill="url(#{p}cherry)"/>
<g clip-path="url(#{p}cc)">
<rect width="{cw}" height="{ch}" fill="url(#{p}foil)" opacity=".9"/>
{guilloche(cw, 262, ch - 10, 16)}
<circle cx="{cw+30}" cy="-20" r="150" fill="none" stroke="{MATCHA}" stroke-opacity=".10"/>
<circle cx="{cw+30}" cy="-20" r="118" fill="none" stroke="{MATCHA}" stroke-opacity=".07"/>
</g>
<rect x="{PX-cx-18}" y="14" width="36" height="9" rx="4.5" fill="#a9c786"/>
<rect x="{PX-cx-18}" y="14" width="36" height="9" rx="4.5" fill="none" stroke="{DEEP}" stroke-opacity=".7"/>
<g font-family="{MONO}" font-size="8.5" letter-spacing="3"><text x="24" y="52" fill="{MATCHA}">DEVELOPER ID</text><text x="{cw-24}" y="52" text-anchor="end" fill="{IVORY}" fill-opacity=".55">NOV 2026</text></g>
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="#000"/>
<image xlink:href="data:image/jpeg;base64,{img}" x="{wx}" y="{wy}" width="{ww}" height="{wh}" preserveAspectRatio="xMidYMin slice" clip-path="url(#{p}win)"/>
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="none" stroke="url(#{p}foilb)" stroke-width="1.8"/>
<g transform="translate({wx+ww-6} {wy+wh-4})"><circle r="21" fill="url(#{p}seal)"/><circle r="21" fill="none" stroke="{IVORY}" stroke-opacity=".6"/><circle r="16" fill="none" stroke="{DEEP}" stroke-opacity=".35" stroke-dasharray="1.5 2.5"/>
<g stroke="{DEEP}" stroke-width="1.5" fill="none" stroke-linecap="round"><circle cx="-4" cy="4.5" r="4.2"/><circle cx="4.5" cy="5.5" r="4.2"/><path d="M-4,0.5 Q-2.5,-5.5 2.5,-9 M4.5,1.5 Q4,-5 2.5,-9"/></g><path d="M2.5,-9 q4.5,-2.5 7,0 q-2.5,3.5 -7,0z" fill="{DEEP}"/></g>
<text x="24" y="{wy+wh+44}" font-family="{SERIF}" font-size="{name_s}" fill="{IVORY}">Sahajpreet</text>
<text x="24" y="{wy+wh+44+name_s*0.86:.1f}" font-family="{SERIF}" font-style="italic" font-size="{name_s}" fill="{MATCHA}">Kaur</text>
<text x="24" y="{wy+wh+44+name_s*0.86+26:.1f}" font-family="{MONO}" font-size="9" letter-spacing="1.6" fill="{MATCHA}" fill-opacity=".9">ASPIRING SOFTWARE ENGINEER</text>
<g font-family="{MONO}"><text x="24" y="{wy+wh+44+name_s*0.86+56:.1f}" font-size="7.5" letter-spacing="2" fill="{IVORY}" fill-opacity=".5">HANDLE</text>
<text x="24" y="{wy+wh+44+name_s*0.86+70:.1f}" font-size="10.5" fill="{IVORY}">@sahajcodes</text>
<text x="146" y="{wy+wh+44+name_s*0.86+56:.1f}" font-size="7.5" letter-spacing="2" fill="{IVORY}" fill-opacity=".5">BASE</text>
<text x="146" y="{wy+wh+44+name_s*0.86+70:.1f}" font-size="10.5" fill="{IVORY}">PANCHKULA, IN</text></g>
{barcode(24, ch-72, ww, 30)}
<text x="{cw/2}" y="{ch-24}" text-anchor="middle" font-family="{MONO}" font-size="7.5" letter-spacing="5" fill="{IVORY}" fill-opacity=".7">SAHAJCODES</text>
<g stroke="{MATCHA}" stroke-opacity=".5" fill="none" stroke-width="1"><path d="M10,24 V10 H24"/><path d="M{cw-10},24 V10 H{cw-24}"/><path d="M10,{ch-24} V{ch-10} H24"/><path d="M{cw-10},{ch-24} V{ch-10} H{cw-24}"/></g>
<g clip-path="url(#{p}cc)"><g transform="skewX(-18)"><rect class="d-sweep" x="-260" y="-30" width="70" height="{ch+60}" fill="url(#{p}sweep)" style="transform:translateX(0px)"/></g></g>
<rect x=".75" y=".75" width="{cw-1.5}" height="{ch-1.5}" rx="25.3" fill="none" stroke="url(#{p}foilb)" stroke-width="1.5"/>
"""

    # -------- lanyard + clasp (absolute coords) --------
    def band(sign):
        # sign=-1 left, +1 right ; mirrored about PX
        pts = [(-34, -14), (-10, -14), (9, 100), (-8, 100)]
        pts = [(PX + sign * x, y) for x, y in pts]
        d = "M" + " L".join(f"{x:.1f},{y}" for x, y in pts) + "Z"
        a, b = (PX + sign * -30, -14), (PX + sign * -3.5, 100)
        c, e = (PX + sign * -14, -14), (PX + sign * 5, 100)
        return (f'<path d="{d}" fill="url(#{p}strap)"/>'
                f'<path d="M{PX+sign*-31:.1f},-14 L{PX+sign*-6:.1f},98" stroke="{MATCHA}" stroke-opacity=".7" stroke-width="1" stroke-dasharray="3 3" fill="none"/>'
                f'<path d="M{PX+sign*-13:.1f},-14 L{PX+sign*6:.1f},98" stroke="{MATCHA}" stroke-opacity=".7" stroke-width="1" stroke-dasharray="3 3" fill="none"/>')
    strap = band(-1) + band(1)
    clasp = f"""
<rect x="{PX-23}" y="92" width="46" height="20" rx="5" fill="url(#{p}metal)" stroke="#6f6657" stroke-width=".8"/>
<rect x="{PX-23}" y="97" width="46" height="1" fill="#fff" fill-opacity=".55"/><rect x="{PX-23}" y="106" width="46" height="1" fill="#000" fill-opacity=".18"/>
<circle cx="{PX-14}" cy="102" r="1.8" fill="#6f6657"/><circle cx="{PX+14}" cy="102" r="1.8" fill="#6f6657"/>
<ellipse cx="{PX}" cy="123" rx="8" ry="11" fill="none" stroke="url(#{p}metal)" stroke-width="4"/>
<ellipse cx="{PX}" cy="123" rx="8" ry="11" fill="none" stroke="#6f6657" stroke-width=".6" stroke-opacity=".8"/>
<path d="M{PX-17},140 H{PX+17} L{PX+13},166 H{PX-13} Z" fill="url(#{p}metal)" stroke="#6f6657" stroke-width=".8" stroke-linejoin="round"/>
<rect x="{PX-9}" y="147" width="18" height="3" rx="1.5" fill="#000" fill-opacity=".22"/>
<rect x="{PX-13}" y="164" width="26" height="6" rx="3" fill="url(#{p}metal)" stroke="#6f6657" stroke-width=".8"/>
"""
    ring = f'<ellipse cx="{PX}" cy="{cy+19}" rx="10.5" ry="15" fill="none" stroke="url(#{p}metal)" stroke-width="3.6"/><ellipse cx="{PX}" cy="{cy+19}" rx="10.5" ry="15" fill="none" stroke="#6f6657" stroke-width=".6"/>'

    # -------- right dashboard panel --------
    rx0, rw = 470, 374
    rows = [("Featured repositories", "02"), ("Languages", "05"), ("Frameworks", "02"), ("Developer tools", "03"), ("Focus areas", "04")]
    row_svg = ""
    for i, (l, v) in enumerate(rows):
        yy = 290 + i * 30
        row_svg += (f'<g class="d-up" style="animation-delay:{1.5 + i*.12:.2f}s">'
                    f'<text x="{rx0+24}" y="{yy}" font-family="{MONO}" font-size="11" fill="{CHERRY}">{esc(l)}</text>'
                    f'<text x="{rx0+rw-24}" y="{yy+3}" text-anchor="end" font-family="{SERIF}" font-style="italic" font-size="28" fill="{CHERRY}">{v}</text>'
                    f'<rect x="{rx0+24}" y="{yy+12}" width="{rw-48}" height="1" fill="{CHERRY}" fill-opacity=".13"/></g>')
    repos = [("Attendly", "jaspreetghumaan/attendly", "QR-based attendance management system featuring time-limited QR sessions."),
             ("Digital Stock Register", "sahajcodes/digital-stock-register", "Web-based laboratory inventory management system.")]
    rep_svg = ""
    for i, (n, path, d) in enumerate(repos):
        y0 = 484 + i * 108
        dl = wrapl(d, "mono", 10, rw - 48)
        rep_svg += (f'<g class="d-up" style="animation-delay:{2.2 + i*.2:.2f}s">'
                    f'<rect x="{rx0}" y="{y0}" width="{rw}" height="98" rx="18" fill="url(#{p}cherry)"/>'
                    f'<rect x="{rx0+.75}" y="{y0+.75}" width="{rw-1.5}" height="96.5" rx="17.3" fill="none" stroke="url(#{p}foilb)" stroke-width="1.2"/>'
                    f'<text x="{rx0+24}" y="{y0+32}" font-family="{SERIF}" font-size="26" fill="{IVORY}">{esc(n)}</text>'
                    f'<text x="{rx0+24}" y="{y0+49}" font-family="{MONO}" font-size="9" letter-spacing=".5" fill="{MATCHA}">github.com/{esc(path)}</text>'
                    + "".join(f'<text x="{rx0+24}" y="{y0+68+j*13}" font-family="{MONO}" font-size="10" fill="{IVORY}" fill-opacity=".78">{esc(l)}</text>' for j, l in enumerate(dl))
                    + '</g>')

    gr_def, gr_use = grain(p, W, H, 28, "60 7 26", 0.03)
    css = f"""
.d-up{{animation:d-up .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes d-up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.d-rise{{animation:d-rise 1.1s cubic-bezier(.16,.84,.24,1) both}}
@keyframes d-rise{{from{{transform:translateY(64px)}}to{{transform:translateY(0)}}}}
.d-draw{{animation:d-draw 1s cubic-bezier(.6,0,.2,1) both}}
@keyframes d-draw{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.d-drop{{animation:d-drop 1.25s linear .15s both}}
@keyframes d-drop{{0%{{transform:translateY(-740px);animation-timing-function:cubic-bezier(.55,.05,.85,.5)}}74%{{transform:translateY(0);animation-timing-function:ease-out}}84%{{transform:translateY(9px);animation-timing-function:ease-in-out}}93%{{transform:translateY(-2px);animation-timing-function:ease-in-out}}100%{{transform:translateY(0)}}}}
.d-pa{{animation:d-pa 7.5s linear {t_impact:.2f}s both}}
@keyframes d-pa{{{kfa}}}
.d-pb{{animation:d-pb 3.4s linear {t_impact:.2f}s infinite both}}
@keyframes d-pb{{{kfb}}}
.d-sweep{{animation:d-sweep 6s cubic-bezier(.45,0,.35,1) 3.2s infinite both}}
@keyframes d-sweep{{0%{{transform:translateX(0)}}30%{{transform:translateX(640px)}}100%{{transform:translateX(640px)}}}}
.d-shine{{animation:d-shine 6s ease-in-out infinite alternate}}
@keyframes d-shine{{from{{opacity:.35}}to{{opacity:.9}}}}
"""
    css += REDUCED

    return svg_open(p, W, H, "Sahajpreet Kaur \u2014 developer identity card",
        "A Cherry-coloured hanging ID card on a lanyard that drops in, settles with damped pendulum motion and swings gently, beside a dated profile snapshot and featured repositories.") + f"""
<defs><style>{fontcss()}{css}</style>
<linearGradient id="{p}bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c7e0aa"/><stop offset=".55" stop-color="{MATCHA}"/><stop offset="1" stop-color="#a9c886"/></linearGradient>
<linearGradient id="{p}cherry" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7d0c31"/><stop offset=".55" stop-color="{CHERRY}"/><stop offset="1" stop-color="#4a0a22"/></linearGradient>
<linearGradient id="{p}foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}" stop-opacity=".0"/><stop offset=".35" stop-color="{ROSE}" stop-opacity=".10"/><stop offset=".55" stop-color="{IVORY}" stop-opacity=".05"/><stop offset=".8" stop-color="{MATCHA}" stop-opacity=".12"/><stop offset="1" stop-color="{MATCHA}" stop-opacity=".0"/></linearGradient>
<linearGradient id="{p}foilb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}"/><stop offset=".3" stop-color="{IVORY}"/><stop offset=".55" stop-color="{ROSE}"/><stop offset=".8" stop-color="{MATCHA}"/><stop offset="1" stop-color="{IVORY}" stop-opacity=".7"/></linearGradient>
<linearGradient id="{p}seal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}"/><stop offset=".45" stop-color="{IVORY}"/><stop offset=".75" stop-color="{ROSE}"/><stop offset="1" stop-color="{MATCHA}"/></linearGradient>
<linearGradient id="{p}sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".34"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4efe3"/><stop offset=".3" stop-color="#c9c0ad"/><stop offset=".55" stop-color="#8d8472"/><stop offset=".75" stop-color="#d9d2c2"/><stop offset="1" stop-color="#a49a86"/></linearGradient>
<linearGradient id="{p}strap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2f0614"/><stop offset=".5" stop-color="{DEEP}"/><stop offset="1" stop-color="#52091f"/></linearGradient>
<filter id="{p}sh" x="-30%" y="-10%" width="160%" height="130%"><feDropShadow dx="0" dy="18" stdDeviation="14" flood-color="{DEEP}" flood-opacity=".38"/></filter>
{dots(p, CHERRY, .16)}{gr_def}
<clipPath id="{p}outer"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="{p}cc"><rect width="{cw}" height="{ch}" rx="26"/></clipPath>
<clipPath id="{p}win"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16"/></clipPath>
<clipPath id="{p}c1"><rect x="450" y="84" width="420" height="72"/></clipPath>
<clipPath id="{p}c2"><rect x="450" y="136" width="420" height="72"/></clipPath>
</defs>
<g clip-path="url(#{p}outer)"><rect width="{W}" height="{H}" fill="url(#{p}bg)"/>
<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}dots)"/>
<circle cx="150" cy="560" r="190" fill="#fff" fill-opacity=".14"/>
{gr_use}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="27.5" fill="none" stroke="{CHERRY}" stroke-opacity=".35" stroke-width="1.5"/>

<g class="d-up" style="animation-delay:.05s">
<text x="{rx0}" y="54" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{CHERRY}">04 \u2014 IDENTITY</text>
<text x="844" y="54" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{CHERRY}" fill-opacity=".6">DASHBOARD</text></g>
<g transform="translate({rx0} 72)"><rect class="d-draw" width="{rw}" height="1" fill="{CHERRY}" fill-opacity=".3" style="transform-origin:0 0;animation-delay:.1s"/></g>
<g clip-path="url(#{p}c1)"><text class="d-rise" x="{rx0-2}" y="134" font-family="{SERIF}" font-size="60" fill="{CHERRY}" style="animation-delay:.3s">Verified,</text></g>
<g clip-path="url(#{p}c2)"><text class="d-rise" x="{rx0-2}" y="188" font-family="{SERIF}" font-style="italic" font-size="60" fill="{CHERRY}" style="animation-delay:.5s">at a glance.</text></g>

<g class="d-up" style="animation-delay:1.3s">
<rect x="{rx0}" y="222" width="{rw}" height="214" rx="20" fill="{IVORY}"/>
<rect x="{rx0+.75}" y="222.75" width="{rw-1.5}" height="212.5" rx="19.3" fill="none" stroke="{CHERRY}" stroke-opacity=".25"/>
<text x="{rx0+24}" y="252" font-family="{MONO}" font-size="9.5" letter-spacing="2.5" fill="{CHERRY}" fill-opacity=".7">PROFILE SNAPSHOT \u00b7 AS OF 07 NOV 2026</text></g>
{row_svg}
<text class="d-up" x="{rx0}" y="468" font-family="{MONO}" font-size="9.5" letter-spacing="2.5" fill="{CHERRY}" fill-opacity=".75" style="animation-delay:2.0s">FEATURED REPOSITORIES</text>
{rep_svg}
<text class="d-up" x="{rx0}" y="{H-22}" font-family="{MONO}" font-size="8.5" fill="{CHERRY}" fill-opacity=".62" style="animation-delay:2.8s">Counted from this profile\u2019s own stack list. No third-party statistics shown.</text>

<!-- hanging assembly: drop -> damped pendulum -> gentle swing about the lanyard pivot -->
<g class="d-drop"><g transform="translate({PX} 0)"><g class="d-pa"><g class="d-pb"><g transform="translate({-PX} 0)">
{strap}
<g filter="url(#{p}sh)"><g transform="translate({cx} {cy})">{card}</g></g>
{ring}
{clasp}
</g></g></g></g></g>
</svg>"""
