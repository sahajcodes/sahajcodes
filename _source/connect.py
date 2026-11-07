from common import *

def build():
    p = "c-"
    W, H = 900, 500
    img = b64file(os.path.join(A, "img", "right_pointing.png"))
    ih = 404; iw = ih * 1199 / 1312
    ix, iy = 30, 70
    cards = [
        ("GitHub", "github", "github.com/sahajcodes"),
        ("LinkedIn", "linkedin", "in/sahajpreetkaur02"),
        ("LeetCode", "leetcode", "leetcode.com/u/sahaj_kaur02"),
    ]
    cx0, cw, chh, gap, cy0 = 486, 358, 84, 18, 168
    cs = ""
    for i, (name, ic, handle) in enumerate(cards):
        y = cy0 + i * (chh + gap)
        d = 0.5 + i * 0.18
        cs += f"""
<g class="c-in" style="animation-delay:{d:.2f}s"><g transform="translate({cx0} {y})">
<g filter="url(#{p}sh)"><rect width="{cw}" height="{chh}" rx="24" fill="{IVORY}"/></g>
<rect x=".75" y=".75" width="{cw-1.5}" height="{chh-1.5}" rx="23.3" fill="none" stroke="url(#{p}gb)" stroke-width="1.3"/>
<circle cx="46" cy="{chh/2}" r="26" fill="{CHERRY}"/>
{icon(ic, 46, chh/2, 26, MATCHA)}
<text x="90" y="{chh/2-2}" font-family="{SERIF}" font-size="30" fill="{CHERRY}">{name}</text>
<text x="90" y="{chh/2+20}" font-family="{MONO}" font-size="10.5" fill="{CHERRY}" fill-opacity=".68">{esc(handle)}</text>
<g transform="translate({cw-44} {chh/2})"><circle r="19" fill="{MATCHA}"/>
<g class="c-nudge" style="animation-delay:{1.4 + i*.25:.2f}s"><path d="M-7,0 H6 M1,-6 L7,0 L1,6" fill="none" stroke="{CHERRY}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g></g>
</g>
<g transform="translate({cx0-44} {y+chh/2})"><g class="c-chev" style="animation-delay:{1.2 + i*.3:.2f}s"><path d="M0,-9 L9,0 L0,9" fill="none" stroke="{MATCHA}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/><path d="M12,-9 L21,0 L12,9" fill="none" stroke="{MATCHA}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".5"/></g></g>
</g>"""
    gr_def, gr_use = grain(p, W, H, 28, "255 255 255", 0.05)
    css = """
.c-in{animation:c-in .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes c-in{from{opacity:0;transform:translateX(46px)}to{opacity:1;transform:translateX(0)}}
.c-up{animation:c-up .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes c-up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.c-rise{animation:c-rise 1.1s cubic-bezier(.16,.84,.24,1) both}
@keyframes c-rise{from{transform:translateY(70px)}to{transform:translateY(0)}}
.c-draw{animation:c-draw 1s cubic-bezier(.6,0,.2,1) both}
@keyframes c-draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.c-nudge{animation:c-nudge 1.9s ease-in-out infinite}
@keyframes c-nudge{0%,100%{transform:translateX(0)}45%{transform:translateX(5px)}}
.c-chev{animation:c-chev 1.9s ease-in-out infinite}
@keyframes c-chev{0%,100%{transform:translateX(0);opacity:.55}45%{transform:translateX(9px);opacity:1}}
.c-float{animation:c-float 6s ease-in-out infinite alternate}
@keyframes c-float{from{transform:translateY(-3px)}to{transform:translateY(4px)}}
.c-char{animation:c-char 1.1s cubic-bezier(.2,.7,.2,1) .15s both}
@keyframes c-char{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
.c-spin{animation:c-spin 60s linear infinite}
@keyframes c-spin{to{transform:rotate(360deg)}}
""" + REDUCED
    return svg_open(p, W, H, "Let\u2019s connect \u2014 GitHub, LinkedIn and LeetCode",
        "Character on the left with three social cards on the right: GitHub, LinkedIn and LeetCode, with gently nudging arrows.") + f"""
<defs><style>{fontcss()}{css}</style>
<radialGradient id="{p}bg" cx="30%" cy="60%" r="90%"><stop offset="0" stop-color="#7a0b2e"/><stop offset=".55" stop-color="{CHERRY}"/><stop offset="1" stop-color="{DEEP}"/></radialGradient>
<linearGradient id="{p}gb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CHERRY}" stop-opacity=".45"/><stop offset=".5" stop-color="{SAGE}" stop-opacity=".7"/><stop offset="1" stop-color="{ROSE}" stop-opacity=".7"/></linearGradient>
<linearGradient id="{p}edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MATCHA}" stop-opacity=".7"/><stop offset=".5" stop-color="{ROSE}" stop-opacity=".25"/><stop offset="1" stop-color="{MATCHA}" stop-opacity=".6"/></linearGradient>
<filter id="{p}sh" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#000" flood-opacity=".28"/></filter>
{dots(p, MATCHA, .2)}{gr_def}
<clipPath id="{p}outer"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="{p}c1"><rect x="470" y="78" width="400" height="76"/></clipPath>
</defs>
<g clip-path="url(#{p}outer)"><rect width="{W}" height="{H}" fill="url(#{p}bg)"/>
<rect x="0" y="0" width="450" height="{H}" fill="url(#{p}dots)"/>{gr_use}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="27.5" fill="none" stroke="url(#{p}edge)" stroke-width="1.5"/>

<g class="c-up" style="animation-delay:.05s">
<text x="{cx0}" y="54" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MATCHA}">05 \u2014 CONNECT</text>
<text x="844" y="54" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{IVORY}" fill-opacity=".6">SAY HELLO</text></g>
<g transform="translate({cx0} 72)"><rect class="c-draw" width="{cw}" height="1" fill="{IVORY}" fill-opacity=".22" style="transform-origin:0 0;animation-delay:.1s"/></g>
<g clip-path="url(#{p}c1)"><text class="c-rise" x="{cx0-2}" y="136" font-family="{SERIF}" font-size="60" fill="{IVORY}" style="animation-delay:.3s">Let\u2019s <tspan font-style="italic" fill="{MATCHA}">connect.</tspan></text></g>

<g transform="translate(224 300)"><circle r="176" fill="{MATCHA}"/><circle r="176" fill="none" stroke="{IVORY}" stroke-opacity=".55" transform="scale(1.07)" stroke-dasharray="2 8" stroke-linecap="round" class="c-spin"/></g>
<ellipse cx="{ix+iw/2:.0f}" cy="{iy+ih-4}" rx="150" ry="11" fill="{DEEP}" fill-opacity=".35"/>
<g class="c-char"><g class="c-float"><image xlink:href="data:image/png;base64,{img}" x="{ix}" y="{iy}" width="{iw:.1f}" height="{ih}" preserveAspectRatio="xMidYMid meet"/></g></g>
{cs}
</svg>"""
