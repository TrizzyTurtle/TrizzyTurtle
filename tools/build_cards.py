#!/usr/bin/env python3
"""Generates the SVG graphics in assets/ for the profile README.

    python3 tools/build_cards.py

Every graphic is a self-contained SVG: no external fonts, images or scripts,
so GitHub can show it from an <img> tag. Edit the text or colours here and run
the script again; the README does not need to change.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

INK = "#f2f5f9"      # main text
MUTED = "#a3afc2"    # secondary text
DIM = "#6f7b90"      # labels
LINE = "#263045"     # borders
PANEL = "#0c111b"    # dark panel
PANEL2 = "#121928"   # raised panel
BAR = "#3a4660"      # placeholder text line
BAR2 = "#2a3550"     # fainter placeholder line
GREEN = "#3ddc84"
AMBER = "#ffb454"

STYLE = f"""
.s{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
@media (prefers-reduced-motion:no-preference){{
  .pulse{{animation:pulse 2.4s ease-in-out infinite}}
  .flow{{animation:flow 1.4s linear infinite}}
  .blink{{animation:blink 1.1s steps(2) infinite}}
  .float{{animation:float 5s ease-in-out infinite}}
  .d1{{animation-delay:.6s}} .d2{{animation-delay:1.2s}} .d3{{animation-delay:1.8s}}
}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
@keyframes flow{{to{{stroke-dashoffset:-28}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
"""


def frame(w, h, a1, a2, label, body, extra_defs=""):
    """The card: rounded dark panel, faint grid and two colour glows."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#111828"/><stop offset="1" stop-color="#0a0e16"/></linearGradient>
<radialGradient id="g1" cx=".85" cy=".1" r=".8"><stop offset="0" stop-color="{a1}" stop-opacity=".26"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx=".05" cy="1" r=".7"><stop offset="0" stop-color="{a2}" stop-opacity=".16"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/></radialGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
<linearGradient id="accv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
<clipPath id="card"><rect width="{w}" height="{h}" rx="22"/></clipPath>
{extra_defs}
</defs>
<style>{STYLE}</style>
<g clip-path="url(#card)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
<rect width="{w}" height="{h}" fill="url(#g1)"/>
<rect width="{w}" height="{h}" fill="url(#g2)"/>
{body}
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="21.25" fill="none" stroke="#2c3649" stroke-width="1.5"/>
</svg>
"""


def text(x, y, s, size, fill=INK, weight=400, cls="s", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def bar(x, y, w, h=6, fill=BAR, op=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}" opacity="{op}"/>'


def chips(x, y, labels, size=14):
    """A row of monospace tags. Monospace keeps the widths predictable."""
    out, cx = [], x
    h = size + 14
    for lab in labels:
        w = round(len(lab) * size * 0.62 + 24)
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="#ffffff" fill-opacity=".05" stroke="#ffffff" stroke-opacity=".14"/>')
        out.append(text(cx + w / 2, y + h / 2 + size * 0.35, lab, size, "#c9d3e2", cls="m", anchor="middle"))
        cx += w + 8
    return "".join(out)


def pill(x, y, private=True, right=False):
    """'Private repo' (lock) or 'Public repo' (open) tag. With right=True, x is the right edge."""
    lab = "PRIVATE REPO" if private else "PUBLIC REPO"
    col = "#c9d3e2" if private else GREEN
    w = round(len(lab) * 12 * 0.66 + 46)
    if right:
        x -= w
    shackle = "M3 7V4.6a3.5 3.5 0 0 1 7 0V7" if private else "M3 7V4.6a3.5 3.5 0 0 1 6.6-1.6"
    return (f'<g transform="translate({x},{y})">'
            f'<rect width="{w}" height="28" rx="14" fill="{col}" fill-opacity=".08" stroke="{col}" stroke-opacity=".35"/>'
            f'<g transform="translate(13,6)"><rect x="0" y="7" width="13" height="9.5" rx="2.2" fill="{col}"/>'
            f'<path d="{shackle}" fill="none" stroke="{col}" stroke-width="1.9" stroke-linecap="round"/></g>'
            f'{text(34, 18.5, lab, 12, col, 600, "m", extra="letter-spacing=\'.8\'")}</g>')


def bot(x, y, col, size=24):
    """A small robot face."""
    s = size / 24
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<line x1="12" y1="0" x2="12" y2="-5" stroke="{col}" stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="12" cy="-6" r="2.2" fill="{col}"/>'
            f'<rect width="24" height="20" rx="6.5" fill="{col}"/>'
            f'<circle cx="8" cy="9" r="2.4" fill="{PANEL}"/><circle cx="16" cy="9" r="2.4" fill="{PANEL}"/>'
            f'<rect x="8" y="14" width="8" height="1.8" rx=".9" fill="{PANEL}" opacity=".6"/></g>')


def cursor(x, y, cls=""):
    return (f'<g transform="translate({x},{y})"><path class="{cls}" d="M0 0V13L3.6 9.8 5.9 15 8 14.1 5.7 9H10.2Z" '
            f'fill="#fff" stroke="{PANEL}" stroke-width="1"/></g>')


def sparkle(cx, cy, r, fill):
    k = r * 0.26
    return (f'<path transform="translate({cx},{cy})" fill="{fill}" '
            f'd="M0 {-r}L{k} {-k}L{r} 0L{k} {k}L0 {r}L{-k} {k}L{-r} 0L{-k} {-k}Z"/>')


def check(cx, cy, col):
    return (f'<circle cx="{cx}" cy="{cy}" r="8" fill="{col}" fill-opacity=".18"/>'
            f'<path d="M{cx - 3.6} {cy + .2}l2.5 2.6 4.6-5.2" fill="none" stroke="{col}" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


# ----------------------------------------------------------------------------
# Wide banners (featured projects)
# ----------------------------------------------------------------------------
def status_pill(x, y, label):
    """A green 'live' tag with a pulsing dot."""
    w = round(len(label) * 12 * 0.66 + 44)
    return (f'<g transform="translate({x},{y})">'
            f'<rect width="{w}" height="28" rx="14" fill="{GREEN}" fill-opacity=".1" stroke="{GREEN}" stroke-opacity=".45"/>'
            f'<circle cx="17" cy="14" r="7" fill="{GREEN}" opacity=".2"/><circle class="pulse" cx="17" cy="14" r="4" fill="{GREEN}"/>'
            f'{text(32, 18.5, label, 12, GREEN, 600, "m", extra="letter-spacing=\'.8\'")}</g>')


def banner(title, tag, tags, a1, a2, art, label, extra_defs="", status=None):
    w, h = 1200, 360
    body = [pill(56, 46)]
    if status:
        body.append(status_pill(207, 46, status))
    body.append(text(54, 138, title, 54, INK, 700, extra="letter-spacing='-1'"))
    body.append('<rect x="56" y="160" width="60" height="5" rx="2.5" fill="url(#acc)"/>')
    for i, line in enumerate(tag):
        body.append(text(56, 206 + i * 31, line, 22, MUTED))
    body.append(chips(56, 286, tags))
    body.append(f'<g transform="translate(628,40)">{art}</g>')
    return frame(w, h, a1, a2, label, "".join(body), extra_defs)


def art_apexbot(a1, a2):
    o = ['<clipPath id="win"><rect width="516" height="280" rx="14"/></clipPath>',
         f'<rect width="516" height="280" rx="14" fill="{PANEL}"/>',
         '<g clip-path="url(#win)">']
    # title bar
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        o.append(f'<circle cx="{18 + i * 16}" cy="17" r="4.6" fill="{c}" opacity=".85"/>')
    o.append(f'<rect x="168" y="7" width="180" height="20" rx="10" fill="#151d2c"/>')
    o.append(text(258, 21, "portal / workspace", 10.5, DIM, cls="m", anchor="middle"))
    o.append(f'<line x1="0" y1="34" x2="516" y2="34" stroke="{LINE}"/>')
    # team sidebar
    o.append(f'<rect x="0" y="34" width="126" height="246" fill="#0e1420"/>')
    o.append(f'<line x1="126" y1="34" x2="126" y2="280" stroke="{LINE}"/>')
    o.append(text(16, 58, "TEAM", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    people = [("#8b9bff", 52, a1, 40), ("#ff8fb1", 44, a2, 38), ("#5fd3c6", 58, "#8e9bb3", 46), ("#ffc46b", 48, "#8e9bb3", 46)]
    for i, (c, nw, rc, rw) in enumerate(people):
        y = 72 + i * 44
        o.append(f'<circle cx="27" cy="{y + 13}" r="11.5" fill="{c}" opacity=".92"/>')
        o.append(f'<circle cx="27" cy="{y + 10}" r="4" fill="{PANEL}" opacity=".55"/>'
                 f'<path d="M19.5 {y + 21.5}a7.5 6.5 0 0 1 15 0z" fill="{PANEL}" opacity=".55"/>')
        o.append(bar(46, y + 4, nw, 6))
        o.append(f'<rect x="46" y="{y + 16}" width="{rw}" height="10" rx="5" fill="{rc}" opacity=".38"/>')
    # workspace status
    o.append(f'<rect x="142" y="48" width="358" height="76" rx="11" fill="{PANEL2}" stroke="{LINE}"/>')
    o.append(f'<circle cx="164" cy="74" r="10" fill="{GREEN}" opacity=".16"/>')
    o.append(f'<circle class="pulse" cx="164" cy="74" r="5" fill="{GREEN}"/>')
    o.append(text(182, 79, "Workspace connected", 14.5, INK, 600))
    o.append(text(160, 106, "reachable · same server · session valid", 10.5, MUTED, cls="m"))
    o.append(f'<rect x="418" y="62" width="68" height="24" rx="12" fill="{a1}" fill-opacity=".16" stroke="{a1}" stroke-opacity=".7"/>')
    o.append(text(452, 78, "paired", 11, "#b7c1ff", 600, "m", "middle"))
    # bots
    o.append(text(142, 146, "BOTS", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    cols = ["#8b9bff", "#5fd3c6", "#ff8fb1", "#ffc46b", "#b58bff"]
    for n in range(6):
        i, j = n % 3, n // 3
        x, y = 142 + i * 122, 156 + j * 58
        if n == 5:
            o.append(f'<rect x="{x}" y="{y}" width="114" height="50" rx="10" fill="none" stroke="{BAR}" stroke-dasharray="4 4"/>')
            o.append(f'<path d="M{x + 40} {y + 25}h10M{x + 45} {y + 20}v10" stroke="{MUTED}" stroke-width="1.8" stroke-linecap="round"/>')
            o.append(text(x + 58, y + 29, "New bot", 10.5, MUTED))
            continue
        o.append(f'<rect x="{x}" y="{y}" width="114" height="50" rx="10" fill="{PANEL2}" stroke="{LINE}"/>')
        o.append(bot(x + 12, y + 18, cols[n], 22))
        o.append(bar(x + 44, y + 17, (42, 34, 48, 38, 44)[n], 6))
        o.append(bar(x + 44, y + 30, (30, 40, 26, 34, 28)[n], 5, BAR2))
        o.append(f'<circle {"class=\"pulse d1\"" if n == 1 else ""} cx="{x + 101}" cy="{y + 13}" r="3.6" fill="{AMBER if n == 3 else GREEN}"/>')
    o.append('</g>')
    o.append(f'<rect width="516" height="280" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    return "".join(o)


def art_apexsocial(a1, a2):
    defs = (f'<linearGradient id="img" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>'
            '<clipPath id="c1"><rect x="10" y="46" width="130" height="112" rx="8"/></clipPath>'
            '<clipPath id="c2"><rect x="230" y="46" width="64" height="80" rx="6"/></clipPath>'
            '<clipPath id="c3"><rect x="230" y="182" width="118" height="46" rx="6"/></clipPath>')

    def photo(clip, x, y, w, h):
        # a little sunset: sun and two hills, scaled to the frame
        return (f'<g clip-path="url(#{clip})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#img)"/>'
                f'<circle cx="{x + w * .74}" cy="{y + h * .3}" r="{min(w, h) * .13}" fill="#fff" opacity=".9"/>'
                f'<path d="M{x} {y + h}L{x + w * .32} {y + h * .5}L{x + w * .54} {y + h * .8}L{x + w * .72} {y + h * .58}L{x + w} {y + h}Z" fill="#170b24" opacity=".42"/></g>')

    o = [text(0, 24, "SOURCE POST", 9.5, DIM, 600, "m", extra="letter-spacing='1'")]
    o.append(f'<rect x="0" y="36" width="150" height="210" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(photo("c1", 10, 46, 130, 112))
    o.append(bar(10, 170, 130, 6))
    o.append(bar(10, 184, 100, 6))
    o.append(bar(10, 198, 118, 6))
    o.append(bar(10, 218, 38, 6, a1, .8))
    o.append(bar(54, 218, 46, 6, a1, .8))
    o.append(f'<circle cx="143" cy="42" r="15" fill="#151d2c" stroke="{a2}" stroke-width="1.5"/>')
    o.append(sparkle(141, 43, 8, a2))
    o.append(sparkle(149, 35, 3.4, a2))
    # split into platform variants
    for d in ("M150 140C186 140 186 76 220 76", "M150 140C186 140 186 208 220 208",
              "M360 76C388 76 380 126 400 130", "M360 208C388 208 380 162 400 158"):
        o.append(f'<path class="flow" d="{d}" fill="none" stroke="{a1}" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round" opacity=".9"/>')
    # Instagram variant
    o.append(f'<rect x="220" y="12" width="140" height="126" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(f'<rect x="231" y="22" width="13" height="13" rx="4" fill="none" stroke="{a1}" stroke-width="1.6"/><circle cx="237.5" cy="28.5" r="2.8" fill="none" stroke="{a1}" stroke-width="1.5"/>')
    o.append(text(251, 33, "Instagram", 12, INK, 600))
    o.append(photo("c2", 230, 46, 64, 80))
    o.append(text(304, 58, "4:5 crop", 9.5, MUTED, cls="m"))
    o.append(bar(304, 68, 44, 5, BAR))
    o.append(bar(304, 79, 30, 5, BAR2))
    o.append(f'<rect x="304" y="104" width="44" height="20" rx="10" fill="{GREEN}" fill-opacity=".15" stroke="{GREEN}" stroke-opacity=".8"/>')
    o.append(text(326, 118, "LIVE", 9.5, GREEN, 700, "m", "middle"))
    # Facebook variant
    o.append(f'<rect x="220" y="150" width="140" height="118" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(f'<circle cx="237.5" cy="166.5" r="6.6" fill="none" stroke="{a2}" stroke-width="1.6"/><path d="M238.6 170.5v-5.4a1.7 1.7 0 0 1 1.7-1.7M236 166.6h4" fill="none" stroke="{a2}" stroke-width="1.5" stroke-linecap="round"/>')
    o.append(text(251, 171, "Facebook", 12, INK, 600))
    o.append(photo("c3", 230, 182, 118, 46))
    o.append(text(230, 251, "original", 9.5, MUTED, cls="m"))
    o.append(f'<rect x="290" y="237" width="58" height="20" rx="10" fill="{AMBER}" fill-opacity=".15" stroke="{AMBER}" stroke-opacity=".8"/>')
    o.append(text(319, 251, "DRY RUN", 9.5, AMBER, 700, "m", "middle"))
    # confirmation
    o.append(f'<rect x="400" y="84" width="116" height="120" rx="12" fill="{PANEL2}" stroke="{a1}" stroke-opacity=".7" stroke-width="1.5"/>')
    o.append(text(414, 108, "Confirm", 13, INK, 600))
    o.append(check(422, 128, GREEN))
    o.append(bar(436, 125, 62, 6))
    o.append(check(422, 150, AMBER))
    o.append(bar(436, 147, 48, 6))
    o.append('<rect x="414" y="170" width="88" height="22" rx="11" fill="url(#acc)"/>')
    o.append(text(458, 185, "Publish", 11, "#150a1c", 700, anchor="middle"))
    return "".join(o), defs


# ----------------------------------------------------------------------------
# Half-width cards
# ----------------------------------------------------------------------------
def card(title, tag, tags, a1, a2, art, label, private=True, extra_defs=""):
    w, h = 600, 372
    body = [f'<g transform="translate(28,28)">{art}</g>']
    body.append(text(27, 258, title, 31, INK, 700, extra="letter-spacing='-.5'"))
    body.append(pill(572, 235, private, right=True))
    body.append(text(28, 289, tag, 17, MUTED))
    body.append(chips(28, 312, tags, 13))
    return frame(w, h, a1, a2, label, "".join(body), extra_defs)


def art_crew(a1, a2):
    cols = [a1, "#ff8fb1", "#ffc46b", "#8b9bff", "#b58bff", "#7ee081"]
    o = [f'<rect width="172" height="184" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>']
    o.append('<rect x="6" y="8" width="160" height="40" rx="9" fill="#fff" opacity=".05"/>')
    for i in range(4):
        y = 15 + i * 42
        o.append(bot(14, y + 5, cols[i], 26))
        o.append(bar(50, y + 6, (58, 46, 64, 50)[i], 6))
        o.append(bar(50, y + 19, (92, 70, 84, 60)[i], 5, BAR2))
    o.append(f'<circle class="pulse" cx="156" cy="20" r="4.2" fill="{a1}"/>')
    o.append(text(192, 11, "CLOUD VM · ONE SCREEN PER BOT", 9.5, DIM, 600, "m", extra="letter-spacing='.8'"))
    for n in range(6):
        i, j = n % 3, n // 3
        x, y = 192 + i * 120, 22 + j * 83
        o.append(f'<rect x="{x}" y="{y}" width="112" height="75" rx="9" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
        o.append(f'<circle cx="{x + 11}" cy="{y + 11}" r="3" fill="{cols[n]}"/>')
        o.append(bar(x + 20, y + 8, 34, 6, BAR2))
        if n == 0:      # browser page
            o.append(f'<rect x="{x + 10}" y="{y + 24}" width="92" height="20" rx="4" fill="{cols[n]}" opacity=".22"/>')
            o.append(bar(x + 10, y + 51, 70, 5))
            o.append(bar(x + 10, y + 61, 48, 5, BAR2))
        elif n == 1:    # terminal
            o.append(text(x + 10, y + 34, "$ npm test", 9, "#7ee081", cls="m"))
            o.append(text(x + 10, y + 48, "42 passed", 9, MUTED, cls="m"))
            o.append(f'<rect class="blink" x="{x + 10}" y="{y + 55}" width="6" height="10" fill="#7ee081"/>')
        elif n == 2:    # chart
            for k, bh in enumerate((14, 24, 18, 32, 26, 38)):
                o.append(f'<rect x="{x + 12 + k * 15}" y="{y + 64 - bh}" width="9" height="{bh}" rx="2" fill="{cols[n]}" opacity="{.45 + k * .1}"/>')
        elif n == 3:    # document
            for k, bw in enumerate((80, 92, 64, 86)):
                o.append(bar(x + 10, y + 25 + k * 11, bw, 5, BAR if k == 0 else BAR2))
        elif n == 4:    # spreadsheet
            for k in range(4):
                o.append(f'<line x1="{x + 10}" y1="{y + 26 + k * 12}" x2="{x + 102}" y2="{y + 26 + k * 12}" stroke="{BAR2}"/>')
            for k in range(4):
                o.append(f'<line x1="{x + 10 + k * 30.6}" y1="{y + 26}" x2="{x + 10 + k * 30.6}" y2="{y + 62}" stroke="{BAR2}"/>')
            o.append(f'<rect x="{x + 41}" y="{y + 38.5}" width="30" height="11" fill="{cols[n]}" opacity=".35"/>')
        else:           # idle
            o.append(text(x + 56, y + 46, "idle", 10, DIM, cls="m", anchor="middle"))
    o.append(cursor(262, 70, "float"))
    o.append(cursor(498, 62, "float d2"))
    o.append(cursor(350, 152, "float d1"))
    return "".join(o)


def art_mediaflow(a1, a2):
    defs = (f'<linearGradient id="t1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="#ff7a59"/></linearGradient>'
            f'<linearGradient id="t2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c8cff"/><stop offset="1" stop-color="{a2}"/></linearGradient>'
            f'<linearGradient id="t3" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#1f8a70"/><stop offset="1" stop-color="{a1}"/></linearGradient>')
    o = []
    # brief
    o.append(f'<rect x="0" y="10" width="118" height="164" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(text(13, 32, "BRIEF", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    for k, bw in enumerate((92, 76, 88)):
        o.append(bar(13, 42 + k * 12, bw, 5, BAR if k == 0 else BAR2))
    o.append(text(13, 96, "BRAND KIT", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    for k, c in enumerate((a1, "#7c8cff", "#f2f5f9")):
        o.append(f'<circle cx="{21 + k * 20}" cy="112" r="7.5" fill="{c}"/>')
    o.append(text(13, 143, "PHOTOS", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    for k in range(3):
        o.append(f'<rect x="{13 + k * 32}" y="150" width="27" height="16" rx="4" fill="url(#t{k + 1})" opacity=".85"/>')
    # director
    o.append(f'<rect x="146" y="56" width="104" height="72" rx="14" fill="{PANEL2}" stroke="{a1}" stroke-opacity=".75" stroke-width="1.5"/>')
    o.append(sparkle(168, 80, 8, a1))
    o.append(text(182, 85, "Creative", 12.5, INK, 600))
    o.append(text(160, 104, "Director", 12.5, INK, 600))
    o.append(text(160, 119, "plans layout", 8.5, MUTED, cls="m"))
    # spec
    o.append(f'<rect x="278" y="22" width="112" height="140" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(text(290, 42, "DesignSpec", 9.5, DIM, 600, "m"))
    spec = [("{", MUTED), ('  "layout":', "#8fd0ff"), ('  "slots": [', "#8fd0ff"), ('  "copy":', "#8fd0ff"), ('  "brand":', "#8fd0ff"), ("}", MUTED)]
    for k, (ln, c) in enumerate(spec):
        o.append(f'<text x="290" y="{62 + k * 15}" class="m" font-size="10" fill="{c}" xml:space="preserve">{escape(ln)}</text>')
    o.append(bar(360, 70, 18, 5, a1, .8))
    o.append(bar(346, 100, 30, 5, a1, .8))
    o.append(bar(352, 115, 22, 5, a1, .8))
    # connectors
    for d in ("M118 92H146", "M250 92H278", "M390 92H418"):
        o.append(f'<path class="flow" d="{d}" stroke="{a1}" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round"/>')
    # rendered creatives
    tiles = [(418, 14, 60, 60, 1), (486, 14, 58, 100, 2), (418, 82, 60, 84, 3), (486, 122, 58, 44, 1)]
    for x, y, tw, th, g in tiles:
        o.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="url(#t{g})"/>')
        o.append(bar(x + 8, y + th - 22, tw * .55, 5, "#fff", .95))
        o.append(bar(x + 8, y + th - 12, tw * .34, 4, "#fff", .6))
    o.append(text(481, 183, "deterministic render", 8.5, DIM, cls="m", anchor="middle"))
    return "".join(o), defs


def art_pdfpro(a1, a2):
    defs = '<clipPath id="pw"><rect width="544" height="184" rx="12"/></clipPath>'
    o = [f'<rect width="544" height="184" rx="12" fill="{PANEL}"/>', '<g clip-path="url(#pw)">']
    # tabs
    o.append(f'<rect x="10" y="8" width="118" height="26" rx="7" fill="{PANEL2}" stroke="{LINE}"/>')
    o.append(text(22, 25, "report.pdf", 10.5, INK, cls="m"))
    o.append(f'<circle cx="114" cy="21" r="2.6" fill="{a1}"/>')
    o.append(text(146, 25, "invoice.pdf", 10.5, DIM, cls="m"))
    o.append(text(250, 25, "notes.pdf", 10.5, DIM, cls="m"))
    o.append(f'<line x1="0" y1="42" x2="544" y2="42" stroke="{LINE}"/>')
    # tool strip
    o.append(f'<rect x="0" y="42" width="48" height="142" fill="#0e1420"/><line x1="48" y1="42" x2="48" y2="184" stroke="{LINE}"/>')
    for k in range(4):
        y = 54 + k * 32
        on = k == 1
        o.append(f'<rect x="11" y="{y}" width="26" height="26" rx="7" fill="{a1 if on else PANEL2}" fill-opacity="{.22 if on else 1}" stroke="{a1 if on else LINE}"/>')
    o.append(f'<path d="M19 72.5l8-8 3 3-8 8h-3z" fill="{MUTED}"/>')                       # pen
    o.append(text(24, 105, "T", 14, "#ffb3b3", 700, anchor="middle"))                     # text tool (active)
    o.append(f'<rect x="18" y="125" width="12" height="12" rx="2" fill="none" stroke="{MUTED}" stroke-width="1.6"/>')   # shape
    o.append(f'<path d="M17 171c3-9 5 5 7-2s3-5 6 0" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-linecap="round"/>')  # signature
    # page thumbnails
    for k in range(2):
        o.append(f'<rect x="62" y="{56 + k * 66}" width="42" height="56" rx="3" fill="#f4f1ea" opacity="{.95 if k == 0 else .5}" stroke="{a1 if k == 0 else "none"}" stroke-width="2"/>')
        for m in range(4):
            o.append(bar(68, 64 + k * 66 + m * 9, (30, 26, 30, 18)[m], 3, "#9aa0ab", .9 if k == 0 else .5))
    # the page
    o.append('<rect x="124" y="56" width="298" height="150" rx="4" fill="#f6f3ec"/>')
    o.append(bar(146, 74, 132, 9, "#262b36"))
    o.append(f'<rect x="143" y="101" width="196" height="15" rx="3" fill="#ffd84d" opacity=".7"/>')
    for k, bw in enumerate((250, 190, 236, 150)):
        o.append(bar(146, 92 + k * 13, bw, 6, "#8d94a1"))
    o.append(f'<rect class="blink" x="284" y="71" width="2.2" height="15" fill="{a1}"/>')
    # text box being placed
    o.append(f'<rect x="146" y="146" width="150" height="26" rx="3" fill="{a1}" fill-opacity=".1" stroke="{a1}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    for hx, hy in ((146, 146), (296, 146), (146, 172), (296, 172)):
        o.append(f'<rect x="{hx - 3}" y="{hy - 3}" width="6" height="6" fill="#fff" stroke="{a1}" stroke-width="1.2"/>')
    o.append(text(156, 164, "Approved, 14 Nov", 11.5, "#b3261e", 600))
    # inspector
    o.append(f'<rect x="438" y="56" width="94" height="116" rx="10" fill="{PANEL2}" stroke="{LINE}"/>')
    o.append(text(450, 75, "TEXT", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    o.append(bar(450, 85, 70, 6))
    o.append(bar(450, 99, 52, 6, BAR2))
    for k, c in enumerate(("#b3261e", "#1f6feb", "#1a7f37", "#f2f5f9")):
        o.append(f'<circle cx="{457 + k * 20}" cy="128" r="6.5" fill="{c}" stroke="{"#fff" if k == 0 else "none"}" stroke-width="1.6"/>')
    o.append(bar(450, 150, 70, 6, BAR2))
    o.append(f'<circle cx="496" cy="153" r="6" fill="{a1}"/>')
    o.append(cursor(302, 160))
    o.append('</g>')
    o.append(f'<rect width="544" height="184" rx="12" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    return "".join(o), defs


def art_spend(a1, a2):
    o = [f'<rect width="170" height="184" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>']
    o.append(text(16, 28, "BILLED SPEND", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    o.append(text(16, 62, "$", 24, MUTED, 600))
    for k, bw in enumerate((20, 30, 30)):          # the figure is blurred out on purpose
        o.append(f'<rect x="{34 + (0, 26, 62)[k]}" y="42" width="{bw}" height="24" rx="6" fill="{INK}" opacity=".85"/>')
    o.append(f'<rect x="16" y="78" width="100" height="20" rx="10" fill="{GREEN}" fill-opacity=".14"/>')
    o.append(text(66, 92, "vs last period", 9, GREEN, cls="m", anchor="middle"))
    for k, (lab, c, bw) in enumerate((("Text models", a1, 96), ("Video models", a2, 62))):
        y = 122 + k * 30
        o.append(f'<circle cx="21" cy="{y - 4}" r="4.5" fill="{c}"/>')
        o.append(text(32, y, lab, 11, MUTED))
        o.append(bar(16, y + 8, 138, 6, BAR2))
        o.append(bar(16, y + 8, bw, 6, c))
    # chart
    o.append(f'<rect x="186" y="0" width="358" height="184" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(text(202, 28, "DAILY SPEND", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    o.append(f'<circle cx="428" cy="24" r="4" fill="{a1}"/>{text(437, 28, "text", 9.5, MUTED, cls="m")}')
    o.append(f'<circle cx="478" cy="24" r="4" fill="{a2}"/>{text(487, 28, "video", 9.5, MUTED, cls="m")}')
    for gy in (64, 98, 132):
        o.append(f'<line x1="202" y1="{gy}" x2="528" y2="{gy}" stroke="{LINE}" stroke-dasharray="2 4"/>')
    o.append(f'<line x1="202" y1="56" x2="528" y2="56" stroke="{AMBER}" stroke-width="1.3" stroke-dasharray="6 5" opacity=".9"/>')
    o.append(text(528, 50, "budget", 9, AMBER, cls="m", anchor="end"))
    txt = (34, 42, 30, 48, 56, 44, 38, 60, 52, 66, 58, 72, 50, 64, 78, 70)
    vid = (10, 16, 8, 20, 12, 24, 14, 10, 26, 18, 30, 16, 22, 34, 20, 28)
    for k, (t, v) in enumerate(zip(txt, vid)):
        x = 204 + k * 20.4
        o.append(f'<rect x="{x:.1f}" y="{166 - t}" width="12" height="{t}" rx="2.5" fill="{a1}"/>')
        o.append(f'<rect x="{x:.1f}" y="{166 - t - v - 2}" width="12" height="{v}" rx="2.5" fill="{a2}"/>')
    o.append(f'<line x1="202" y1="167" x2="528" y2="167" stroke="{BAR}"/>')
    return "".join(o)


def art_vault(a1, a2):
    o = []
    # shield with keyhole
    o.append('<path d="M74 14l56 20v46c0 40-24 70-56 86-32-16-56-46-56-86V34z" fill="url(#accv)" opacity=".16"/>')
    o.append('<path d="M74 14l56 20v46c0 40-24 70-56 86-32-16-56-46-56-86V34z" fill="none" stroke="url(#accv)" stroke-width="2.5" stroke-linejoin="round"/>')
    o.append(f'<circle class="pulse" cx="74" cy="78" r="15" fill="{a1}"/>')
    o.append(f'<path d="M66 124l5-36h6l5 36z" fill="{a1}"/>')
    o.append(f'<circle cx="74" cy="78" r="5.5" fill="{PANEL}"/>')
    # entries
    o.append(f'<rect x="164" y="0" width="380" height="184" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(f'<circle cx="184" cy="24" r="4.5" fill="{GREEN}"/>')
    o.append(text(196, 28, "vault unlocked · encrypted on this device", 10, MUTED, cls="m"))
    o.append(f'<line x1="164" y1="42" x2="544" y2="42" stroke="{LINE}"/>')
    for k, c in enumerate((a1, a2, "#8b9bff")):
        y = 54 + k * 42
        o.append(f'<rect x="180" y="{y}" width="30" height="30" rx="8" fill="{c}" opacity=".9"/>')
        o.append(f'<rect x="189" y="{y + 9}" width="12" height="12" rx="3" fill="{PANEL}" opacity=".5"/>')
        o.append(bar(222, y + 5, (86, 64, 100)[k], 6))
        if k == 0:
            o.append(text(222, y + 27, "hunter-violet-42", 10.5, "#d7dfeb", cls="m"))
        else:
            for d in range(12):
                o.append(f'<circle cx="{225 + d * 9.2}" cy="{y + 23}" r="2.7" fill="{MUTED}"/>')
        o.append(f'<rect x="478" y="{y + 4}" width="50" height="22" rx="11" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".14"/>')
        o.append(text(503, y + 19, "hide" if k == 0 else "show", 9.5, MUTED, cls="m", anchor="middle"))
    return "".join(o)


def art_wifi(a1, a2):
    o = []
    cx, cy = 76, 138
    for k, r in enumerate((30, 58, 86)):
        d = r * 0.7071
        o.append(f'<path class="pulse d{k + 1}" d="M{cx - d:.1f} {cy - d:.1f}A{r} {r} 0 0 1 {cx + d:.1f} {cy - d:.1f}" fill="none" stroke="{a1}" stroke-width="9" stroke-linecap="round" opacity="{1 - k * .22}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{a1}"/>')
    o.append(text(cx, 176, "laptop Wi-Fi only", 9.5, DIM, cls="m", anchor="middle"))
    # signal trace
    o.append(f'<rect x="170" y="0" width="374" height="184" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(text(186, 28, "SIGNAL STRENGTH (RSSI)", 9.5, DIM, 600, "m", extra="letter-spacing='1'"))
    o.append(f'<rect x="372" y="42" width="84" height="126" rx="6" fill="{a2}" opacity=".12"/>')
    o.append(f'<rect x="384" y="14" width="60" height="20" rx="10" fill="{a2}" fill-opacity=".16" stroke="{a2}" stroke-opacity=".8"/>')
    o.append(text(414, 28, "motion", 9.5, a2, 700, "m", "middle"))
    for gy in (78, 128):
        o.append(f'<line x1="186" y1="{gy}" x2="528" y2="{gy}" stroke="{AMBER}" stroke-width="1.2" stroke-dasharray="5 5" opacity=".75"/>')
    o.append(text(528, 72, "threshold", 9, AMBER, cls="m", anchor="end"))
    ys = [104, 100, 106, 102, 98, 105, 101, 107, 103, 99, 104, 100, 106, 102, 97, 104, 108, 101, 99,
          70, 138, 58, 146, 80, 124, 66, 112, 100, 105, 101, 106, 102, 98, 104, 101]
    pts = " ".join(f"{186 + i * 10.05:.1f},{y}" for i, y in enumerate(ys))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{a1}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle class="pulse" cx="{186 + 22 * 10.05:.1f}" cy="146" r="4.5" fill="{a2}"/>')
    return "".join(o)


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
def header():
    a1, a2 = "#7c8cff", "#35d6c0"
    w, h = 1200, 300
    o = [text(64, 92, "HELLO, I'M", 15, DIM, 600, "m", extra="letter-spacing='3'")]
    o.append(f'<text x="58" y="178" class="s" font-size="92" font-weight="800" fill="url(#acc)" letter-spacing="-3">Tristan</text>')
    o.append(text(64, 228, "I build AI agent tools, automation", 26, MUTED))
    o.append(text(64, 262, "and full-stack products.", 26, MUTED))
    # terminal
    tx, ty, tw, th = 716, 38, 428, 224
    o.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>')
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        o.append(f'<circle cx="{tx + 20 + i * 16}" cy="{ty + 18}" r="4.6" fill="{c}" opacity=".85"/>')
    o.append(f'<line x1="{tx}" y1="{ty + 36}" x2="{tx + tw}" y2="{ty + 36}" stroke="{LINE}"/>')
    lines = [("$ ", "ls work/", None),
             (None, "apexbot/   apexsocial/   crew/", a2),
             (None, "mediaflow/   pdf-pro/   ...", a2),
             ("$ ", "cat stack.txt", None),
             (None, "TypeScript  Python  Swift  C++", "#c9d3e2")]
    for i, (prompt, body, col) in enumerate(lines):
        y = ty + 66 + i * 27
        if prompt:
            o.append(f'<text x="{tx + 22}" y="{y}" class="m" font-size="16" xml:space="preserve"><tspan fill="{a1}">$ </tspan><tspan fill="{INK}">{escape(body)}</tspan></text>')
        else:
            o.append(f'<text x="{tx + 22}" y="{y}" class="m" font-size="16" fill="{col}" xml:space="preserve">{escape(body)}</text>')
    y = ty + 66 + 5 * 27
    o.append(f'<text x="{tx + 22}" y="{y}" class="m" font-size="16" fill="{a1}">$</text>')
    o.append(f'<rect class="blink" x="{tx + 42}" y="{y - 14}" width="9" height="17" fill="{INK}"/>')
    return frame(w, h, a1, a2, "Tristan. I build AI agent tools, automation and full-stack products.", "".join(o))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"header.svg": header()}

    a = ("#7c8cff", "#b58bff")
    files["apexbot.svg"] = banner(
        "ApexBot", ["A company portal for AI agent workspaces.", "Teams sign in, pair a server and run bots."],
        ["Next.js", "TypeScript", "Postgres", "Playwright"], *a, art_apexbot(*a),
        "ApexBot: a company portal for AI agent workspaces. In production with over 100 internal users. Private repository.",
        status="IN PRODUCTION · 100+ USERS")

    a = ("#ff5fa2", "#ffb057")
    art, defs = art_apexsocial(*a)
    files["apexsocial.svg"] = banner(
        "ApexSocial", ["Compose once, preview every platform,", "publish to Instagram and Facebook."],
        ["Python", "FastAPI", "Meta Graph API", "OpenAI"], *a, art,
        "ApexSocial: compose once, preview every platform, publish to Instagram and Facebook. Private repository.", defs)

    a = ("#35d6c0", "#4ea8ff")
    files["crew.svg"] = card("Crew", "A desktop app for a team of AI agent bots.",
                             ["Electron", "React", "TypeScript"], *a, art_crew(*a),
                             "Crew: a desktop app for a team of AI agent bots. Private repository.")

    a = ("#ffb454", "#ff6fae")
    art, defs = art_mediaflow(*a)
    files["mediaflow.svg"] = card("MediaFlow", "Brief in, export-ready social creatives out.",
                                  ["TypeScript", "React", "Postgres"], *a, art,
                                  "MediaFlow: brief in, export-ready social creatives out. Private repository.", extra_defs=defs)

    a = ("#ff6b6b", "#ffb057")
    art, defs = art_pdfpro(*a)
    files["pdf-pro.svg"] = card("PDF Pro", "A native macOS PDF editor.",
                                ["Swift", "SwiftUI", "PDFKit"], *a, art,
                                "PDF Pro: a native macOS PDF editor. Private repository.", extra_defs=defs)

    a = ("#4ea8ff", "#b58bff")
    files["byteplus-spend.svg"] = card("BytePlus Spend", "A dashboard for AI model spending.",
                                       ["Next.js", "TypeScript", "Recharts"], *a, art_spend(*a),
                                       "BytePlus Spend: a dashboard for AI model spending. Private repository.")

    a = ("#5ad68a", "#35d6c0")
    files["passwordvault.svg"] = card("PasswordVault", "A local, encrypted password manager.",
                                      ["C++17", "wxWidgets", "libsodium"], *a, art_vault(*a),
                                      "PasswordVault: a local, encrypted password manager. Public repository.", private=False)

    a = ("#4ea8ff", "#ff6fae")
    files["wifi-motion.svg"] = card("Wi-Fi Motion Detector", "Senses movement from Wi-Fi signal changes.",
                                    ["Python", "macOS", "Windows", "Linux"], *a, art_wifi(*a),
                                    "Wi-Fi Motion Detector: senses movement from Wi-Fi signal changes. Public repository.", private=False)

    for name, svg in files.items():
        (OUT / name).write_text(svg)
        print(f"{name}: {len(svg) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
