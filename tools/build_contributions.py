#!/usr/bin/env python3
"""Draws assets/contributions.svg: the last year of GitHub contributions.

    python3 tools/build_contributions.py [login]

Reads the contribution calendar through the `gh` CLI (which must be signed in)
and draws it in the same style as the other cards. It is a snapshot: run it
again to refresh the picture.
"""
import json
import subprocess
import sys
from datetime import date

from build_cards import DIM, INK, MUTED, OUT, frame, text

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "TrizzyTurtle"
QUERY = """query($login:String!){ user(login:$login){ contributionsCollection{ contributionCalendar{
  totalContributions weeks{ contributionDays{ date contributionCount contributionLevel weekday } } } } } }"""
LEVELS = {"NONE": "#1a2334", "FIRST_QUARTILE": "#1d4a52", "SECOND_QUARTILE": "#207f7b",
          "THIRD_QUARTILE": "#2fbfa9", "FOURTH_QUARTILE": "#86f3dc"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch(login):
    r = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={login}"],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def pretty(d):
    y, m, dd = (int(p) for p in d.split("-"))
    return f"{dd} {MONTHS[m - 1]} {y}"


def build(cal):
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    total = cal["totalContributions"]
    w, h = 1200, 322
    x0, y0, pitch, cell = 100, 150, 20, 15
    o = []

    # heading
    o.append(f'<text x="48" y="72" class="s" font-size="34" font-weight="800" letter-spacing="-.5">'
             f'<tspan fill="url(#acc)">{total:,}</tspan><tspan fill="{INK}" font-weight="700"> contributions in the last year</tspan></text>')
    o.append(text(49, 100, f"Public and private repositories · {pretty(days[0]['date'])} to {pretty(days[-1]['date'])}", 15.5, MUTED))

    # month labels: where a new month starts, but not squeezed against the previous label
    last_x = -100
    for i, wk in enumerate(weeks):
        first = date.fromisoformat(wk["contributionDays"][0]["date"])
        prev = date.fromisoformat(weeks[i - 1]["contributionDays"][0]["date"]) if i else None
        x = x0 + i * pitch
        if (prev is None or first.month != prev.month) and x - last_x >= 3 * pitch and i < len(weeks) - 1:
            o.append(text(x, y0 - 12, MONTHS[first.month - 1], 13, DIM, cls="m"))
            last_x = x
    for wd, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(text(x0 - 14, y0 + wd * pitch + 12, lab, 13, DIM, cls="m", anchor="end"))

    # the grid
    for i, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            n = d["contributionCount"]
            tip = f"{n} contribution{'' if n == 1 else 's'} on {pretty(d['date'])}"
            o.append(f'<rect x="{x0 + i * pitch}" y="{y0 + d["weekday"] * pitch}" width="{cell}" height="{cell}" rx="3.5" '
                     f'fill="{LEVELS[d["contributionLevel"]]}"><title>{tip}</title></rect>')

    # legend
    ly = 54
    lx = x0 + len(weeks) * pitch - (pitch - cell)
    o.append(text(lx, ly + 12, "More", 13, DIM, cls="m", anchor="end"))
    lx -= 46
    for k, c in enumerate(reversed(list(LEVELS.values()))):
        o.append(f'<rect x="{lx - (k + 1) * pitch + (pitch - cell)}" y="{ly}" width="{cell}" height="{cell}" rx="3.5" fill="{c}"/>')
    o.append(text(lx - 5 * pitch - 6, ly + 12, "Less", 13, DIM, cls="m", anchor="end"))

    return frame(w, h, "#7c8cff", "#35d6c0",
                 f"{total:,} contributions in the last year, across public and private repositories.", "".join(o))


if __name__ == "__main__":
    svg = build(fetch(LOGIN))
    (OUT / "contributions.svg").write_text(svg)
    print(f"contributions.svg: {len(svg) / 1024:.1f} KB")
