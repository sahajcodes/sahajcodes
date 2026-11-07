from common import *

def build():
    p = "h-"
    W, H = 900, 600
    img = b64file(os.path.join(A, "img", "id.jpg"))

    # ---- measured typography ----
    S = 510 / tw("Sahajpreet", "serif", 1)          # name fits the left column
    S = min(S, 138)
    base1 = 256
    base2 = base1 + S * 0.885
    pitch = ("Aspiring Software Engineer focused on problem-solving, building real-world "
             "applications, and continuously expanding my technical skills.")
    ps = 17.0
    while tw(pitch, "serifi", ps) > 788: ps -= 0.25
    greet = "hello, world \u2014 I\u2019m"
    gsize = 17
    cw = tw("m", "mono", gsize)

    roles = ["Aspiring Software Engineer", "Student Developer", "Independent Builder", "Technology Explorer"]

    # typed greeting: one tspan per char
    ch = "".join(
        f'<tspan class="h-ch" style="animation-delay:{0.35 + i * 0.06:.2f}s">{esc(c)}</tspan>'
        for i, c in enumerate(greet))
    typed_end = 0.35 + len(greet) * 0.06

    # ---- portrait arch ----
    px, py, pw, ph = 590, 104, 254, 340
    r = pw / 2
    arch = (f"M{px},{py+r} A{r},{r} 0 0 1 {px+pw},{py+r} L{px+pw},{py+ph-26} "
            f"Q{px+pw},{py+ph} {px+pw-26},{py+ph} L{px+26},{py+ph} Q{px},{py+ph} {px},{py+ph-26} Z")

    # ---- roles ----
    role_t = "".join(
        f'<text class="h-role h-r{i}" x="56" y="448" style="animation-delay:{2.0 + 3*i:.1f}s">{esc(t)}</text>'
        for i, t in enumerate(roles))
    pager = "".join(
        f'<rect class="h-pg h-p{i}" x="{56 + i*34}" y="470" width="26" height="3" rx="1.5" fill="{MATCHA}" '
        f'style="animation-delay:{2.0 + 3*i:.1f}s"/>' for i in range(4))

    # ---- chips ----
    f1 = 11.5
    c1t = "Panchkula, Haryana, India"
    c1w = 16 + 14 + tw(c1t, "mono", f1) + 16
    c2t = "Student Developer \u00b7 Independent Builder \u00b7 Open-Source Learner"
    c2w = 16 + tw(c2t, "mono", f1) + 16
    cy = 536
    chips = (
        f'<g class="h-up" style="animation-delay:2.7s">'
        f'<rect x="56" y="{cy}" width="{c1w:.1f}" height="30" rx="15" fill="none" stroke="{MATCHA}" stroke-opacity=".45"/>'
        f'<g transform="translate(75 {cy+15})"><path d="M0,-7 a5,5 0 0 1 5,5 c0,3.4 -5,8.5 -5,8.5 s-5,-5.1 -5,-8.5 a5,5 0 0 1 5,-5z" fill="{MATCHA}"/>'
        f'<circle cx="0" cy="-2" r="1.8" fill="{DEEP}"/></g>'
        f'<text x="{56+16+14+2}" y="{cy+19.5}" font-family="{MONO}" font-size="{f1}" fill="{IVORY}">{esc(c1t)}</text>'
        f'<rect x="{56+c1w+10:.1f}" y="{cy}" width="{c2w:.1f}" height="30" rx="15" fill="{MATCHA}" fill-opacity=".1" stroke="{MATCHA}" stroke-opacity=".28"/>'
        f'<text x="{56+c1w+10+16:.1f}" y="{cy+19.5}" font-family="{MONO}" font-size="{f1}" fill="{MATCHA}">{esc(c2t)}</text>'
        f'</g>')

    # ---- stamp text ring ----
    ring_t = "ASPIRING ENGINEER \u00b7 BUILDER \u00b7 LEARNER \u00b7 "
    sr = 37.5
    circ = 2 * math.pi * sr

    gr_def, gr_use = grain(p, W, H, 28, "255 255 255", 0.06)
    css = """
.h-serif{font-family:%(SERIF)s}.h-mono{font-family:%(MONO)s}
.h-ch{animation:h-show .01s step-end both}
@keyframes h-show{from{fill-opacity:0}to{fill-opacity:1}}
.h-cur{animation:h-type %(tt).2fs steps(%(n)d,end) .35s both}
@keyframes h-type{from{transform:translateX(0)}to{transform:translateX(%(tx).2fpx)}}
.h-blink{animation:h-blink 1.05s steps(1,end) infinite}
@keyframes h-blink{0%%,55%%{opacity:1}56%%,100%%{opacity:0}}
.h-rise{animation:h-rise 1.15s cubic-bezier(.16,.84,.24,1) both}
@keyframes h-rise{from{transform:translateY(%(rise).1fpx)}to{transform:translateY(0)}}
.h-up{animation:h-up .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes h-up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.h-draw{animation:h-draw 1.2s cubic-bezier(.6,0,.2,1) both}
@keyframes h-draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.h-role{opacity:0;animation:h-role 12s cubic-bezier(.3,.7,.3,1) infinite both}
.h-r0{opacity:1}
@keyframes h-role{0%%{opacity:0;transform:translateY(34px)}4.5%%{opacity:1;transform:translateY(0)}23%%{opacity:1;transform:translateY(0)}27.5%%{opacity:0;transform:translateY(-34px)}100%%{opacity:0;transform:translateY(-34px)}}
.h-pg{opacity:.28;animation:h-pg 12s linear infinite both}
.h-p0{opacity:1}
@keyframes h-pg{0%%{opacity:.28}3%%{opacity:1}24%%{opacity:1}28%%{opacity:.28}100%%{opacity:.28}}
.h-float{animation:h-float 7s ease-in-out infinite alternate}
@keyframes h-float{from{transform:translateY(-5px)}to{transform:translateY(6px)}}
.h-spin{animation:h-spin 26s linear infinite}
@keyframes h-spin{to{transform:rotate(360deg)}}
.h-twinkle{animation:h-tw 4.5s ease-in-out infinite alternate}
@keyframes h-tw{from{transform:rotate(-12deg) scale(.82);opacity:.55}to{transform:rotate(12deg) scale(1.1);opacity:1}}
.h-portrait{animation:h-up 1.2s cubic-bezier(.2,.7,.2,1) .5s both}
""" % dict(SERIF=SERIF, MONO=MONO, tt=len(greet) * 0.06, n=len(greet), tx=len(greet) * cw, rise=S * 1.15)
    css += REDUCED

    body = f"""
<defs>
<style>{fontcss()}{css}</style>
<radialGradient id="{p}bg" cx="28%" cy="38%" r="85%"><stop offset="0" stop-color="#7a0b2e"/><stop offset=".55" stop-color="{CHERRY}"/><stop offset="1" stop-color="{DEEP}"/></radialGradient>
<linearGradient id="{p}gb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}"/><stop offset=".5" stop-color="{ROSE}"/><stop offset="1" stop-color="{MATCHA}" stop-opacity=".35"/></linearGradient>
<linearGradient id="{p}edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}" stop-opacity=".7"/><stop offset=".5" stop-color="{ROSE}" stop-opacity=".25"/><stop offset="1" stop-color="{MATCHA}" stop-opacity=".6"/></linearGradient>
{dots(p, MATCHA, .22)}
{gr_def}
<clipPath id="{p}card"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="{p}arch"><path d="{arch}"/></clipPath>
<clipPath id="{p}c1"><rect x="40" y="{base1 - S*0.86:.1f}" width="540" height="{S*1.08:.1f}"/></clipPath>
<clipPath id="{p}c2"><rect x="40" y="{base2 - S*0.86:.1f}" width="540" height="{S*1.2:.1f}"/></clipPath>
<clipPath id="{p}cr"><rect x="50" y="410" width="520" height="50"/></clipPath>
<path id="{p}ring" d="M0,{sr} a{sr},{sr} 0 1 1 0,{-2*sr} a{sr},{sr} 0 1 1 0,{2*sr}" fill="none" transform="rotate(-90)"/>
</defs>

<g clip-path="url(#{p}card)">
<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>
<rect x="520" y="0" width="380" height="{H}" fill="url(#{p}dots)"/>
{gr_use}
</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="27.5" fill="none" stroke="url(#{p}edge)" stroke-width="1.5"/>

<!-- top editorial row -->
<g class="h-up" style="animation-delay:.05s">
<text x="56" y="54" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MATCHA}">01 \u2014 INTRODUCTION</text>
<text x="{px+pw}" y="54" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{IVORY}" fill-opacity=".6">SAHAJCODES</text>
</g>
<g transform="translate(56 72)"><rect class="h-draw" width="788" height="1" fill="{IVORY}" fill-opacity=".22" style="transform-origin:0 0;animation-delay:.1s"/></g>

<!-- typed greeting -->
<text x="56" y="130" font-family="{MONO}" font-size="{gsize}" fill="{MATCHA}" xml:space="preserve">{ch}</text>
<g class="h-cur" style="transform:translateX({len(greet)*cw:.2f}px)"><g class="h-blink" style="animation-delay:{typed_end:.2f}s"><rect x="57" y="{130-gsize+1}" width="{cw*0.75:.2f}" height="{gsize+3}" fill="{MATCHA}"/></g></g>
"""
    body += f"""
<!-- name: rising mask -->
<g clip-path="url(#{p}c1)"><text class="h-rise" x="52" y="{base1}" font-family="{SERIF}" font-size="{S:.1f}" fill="{IVORY}" style="animation-delay:.85s">Sahajpreet</text></g>
<g clip-path="url(#{p}c2)"><text class="h-rise" x="52" y="{base2:.1f}" font-family="{SERIF}" font-style="italic" font-size="{S:.1f}" fill="{MATCHA}" style="animation-delay:1.05s">Kaur</text></g>
<g transform="translate({56 + tw('Kaur','serifi',S) + 26:.1f} {base2 - S*0.3:.1f})">
<rect class="h-draw" width="{max(40, 540 - (56 + tw('Kaur','serifi',S) + 26)):.1f}" height="1" fill="{MATCHA}" fill-opacity=".55" style="transform-origin:0 0;animation-delay:1.5s"/></g>

<!-- cycling roles -->
<text x="56" y="414" font-family="{MONO}" font-size="10.5" letter-spacing="3" fill="{IVORY}" fill-opacity=".55" class="h-up" style="animation-delay:1.7s">CURRENTLY \u2014</text>
<g clip-path="url(#{p}cr)" font-family="{SERIF}" font-size="34" fill="{IVORY}">{role_t}</g>
{pager}

<!-- pitch -->
<text class="h-up" x="56" y="508" font-family="{SERIF}" font-style="italic" font-size="{ps:.2f}" fill="{IVORY}" fill-opacity=".88" style="animation-delay:2.4s">{esc(pitch)}</text>
{chips}

<!-- portrait -->
<g class="h-portrait">
<g class="h-float"><path d="{arch}" transform="translate(16 16)" fill="none" stroke="{MATCHA}" stroke-opacity=".5" stroke-width="1.2"/></g>
<path d="{arch}" fill="#000"/>
<image xlink:href="data:image/jpeg;base64,{img}" x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMin slice" clip-path="url(#{p}arch)"/>
<path d="{arch}" fill="none" stroke="url(#{p}gb)" stroke-width="1.8"/>
</g>
<g class="h-up" style="animation-delay:1.6s">
<g transform="translate({px+8} {py+ph-6})">
<circle r="55" fill="{IVORY}"/><circle r="55" fill="none" stroke="{MATCHA}" stroke-width="1.2" stroke-opacity=".9" transform="scale(.93)"/>
<g class="h-spin"><use xlink:href="#{p}ring" style="display:none"/>
<text font-family="{MONO}" font-size="8.6" font-weight="700" fill="{CHERRY}"><textPath xlink:href="#{p}ring" startOffset="0" textLength="{circ-1.5:.1f}" lengthAdjust="spacing">{esc(ring_t)}</textPath></text></g>
<circle r="21" fill="{CHERRY}"/>
<g stroke="{MATCHA}" stroke-width="1.5" fill="none" stroke-linecap="round"><circle cx="-5" cy="5" r="5"/><circle cx="5.5" cy="6.5" r="5"/><path d="M-5,0 Q-3,-7 3,-11 M5.5,1.5 Q5,-6 3,-11"/><path d="M3,-11 q5,-3 8,0 q-3,4 -8,0z" fill="{MATCHA}" stroke="none"/></g>
</g></g>
<g transform="translate(566 128)"><g class="h-twinkle"><path d="M0,-9 Q1,-1 9,0 Q1,1 0,9 Q-1,1 -9,0 Q-1,-1 0,-9z" fill="{MATCHA}"/></g></g>
</svg>"""
    return svg_open(p, W, H, "Sahajpreet Kaur \u2014 Aspiring Software Engineer",
                    "Animated hero: typed greeting, rising name reveal, cycling roles, portrait, location and identity.") + body
