# -*- coding: utf-8 -*-
"""Illustrative SVG cover art for projects (original, abstract; not screenshots)."""

W, H = 1200, 675


def _wrap(defs, body, bg):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
        f"<defs>{defs}</defs><rect width='{W}' height='{H}' fill='{bg}'/>{body}</svg>\n"
    )


def frogie():
    defs = ("<linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0e3b2a'/>"
            "<stop offset='1' stop-color='#05140d'/></linearGradient>")
    pads = "".join(
        f"<ellipse cx='{x}' cy='{y}' rx='{r}' ry='{r*0.42:.0f}' fill='#1f6b43' opacity='{o}'/>"
        for x, y, r, o in [(180, 560, 120, .9), (480, 610, 90, .7), (960, 580, 140, .85), (1110, 470, 70, .6), (90, 430, 60, .5)]
    )
    frog = (
        "<g transform='translate(600 380)'>"
        "<ellipse cx='0' cy='60' rx='210' ry='120' fill='#39ff88'/>"
        "<ellipse cx='0' cy='80' rx='150' ry='80' fill='#b6ffd2'/>"
        "<circle cx='-110' cy='-40' r='70' fill='#39ff88'/><circle cx='110' cy='-40' r='70' fill='#39ff88'/>"
        "<circle cx='-110' cy='-40' r='42' fill='#fff'/><circle cx='110' cy='-40' r='42' fill='#fff'/>"
        "<circle cx='-100' cy='-36' r='22' fill='#05140d'/><circle cx='120' cy='-36' r='22' fill='#05140d'/>"
        "<path d='M-70 50 Q0 100 70 50' fill='none' stroke='#05140d' stroke-width='12' stroke-linecap='round'/>"
        "</g>"
    )
    flies = "".join(f"<circle cx='{x}' cy='{y}' r='7' fill='#e8f2ec' opacity='.8'/>" for x, y in [(240, 160), (930, 120), (1040, 250), (330, 270)])
    return _wrap(defs, f"<rect width='{W}' height='{H}' fill='url(#g)'/>{pads}{flies}{frog}", "#05140d")


def shadow():
    defs = ("<radialGradient id='s' cx='.5' cy='.5' r='.5'><stop offset='.7' stop-color='#0a1a14' stop-opacity='0'/>"
            "<stop offset='1' stop-color='#020403'/></radialGradient>"
            "<clipPath id='c'><circle cx='600' cy='337' r='250'/></clipPath>")
    sky = "".join(
        f"<rect x='{x}' y='{y}' width='{w}' height='{H-y}' fill='#0d1f18'/>"
        for x, y, w in [(0, 420, 120), (110, 360, 90), (210, 450, 140), (360, 300, 110), (480, 390, 80), (570, 250, 100),
                        (680, 400, 130), (820, 330, 90), (920, 430, 120), (1050, 370, 150)]
    )
    wins = "".join(f"<rect x='{x}' y='{y}' width='10' height='14' fill='#39ff88' opacity='.55'/>"
                   for x, y in [(380, 330), (400, 360), (590, 280), (620, 310), (600, 360), (840, 360), (700, 430), (130, 390)])
    scope = (
        "<g clip-path='url(#c)'><rect width='1200' height='675' fill='#0f2a20'/>"
        "<g transform='translate(-600 -337) scale(2)'>" + sky + wins + "</g></g>"
        "<circle cx='600' cy='337' r='250' fill='none' stroke='#39ff88' stroke-width='6'/>"
        "<line x1='350' y1='337' x2='560' y2='337' stroke='#39ff88' stroke-width='3'/>"
        "<line x1='640' y1='337' x2='850' y2='337' stroke='#39ff88' stroke-width='3'/>"
        "<line x1='600' y1='87' x2='600' y2='297' stroke='#39ff88' stroke-width='3'/>"
        "<line x1='600' y1='377' x2='600' y2='587' stroke='#39ff88' stroke-width='3'/>"
        "<circle cx='600' cy='337' r='5' fill='#ff4d4d'/>"
        + "".join(f"<line x1='{600+k*30}' y1='392' x2='{600+k*30}' y2='402' stroke='#39ff88' stroke-width='2'/>" for k in (-3, -2, -1, 1, 2, 3))
    )
    return _wrap(defs, sky + wins + f"<rect width='{W}' height='{H}' fill='#020403' opacity='.55'/>" + scope, "#050807")


def streets():
    defs = ("<linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3a1408'/>"
            "<stop offset='.55' stop-color='#c2561c'/><stop offset='1' stop-color='#f0a83a'/></linearGradient>")
    sun = "<circle cx='820' cy='430' r='120' fill='#ffd27a' opacity='.9'/>"
    city = "".join(f"<rect x='{x}' y='{y}' width='{w}' height='{H-y}' fill='#140a06'/>"
                   for x, y, w in [(0, 470, 160), (150, 420, 120), (260, 480, 150), (400, 440, 110), (500, 500, 160),
                                   (650, 455, 120), (760, 490, 140), (890, 430, 120), (1000, 475, 200)])
    minaret = ("<rect x='1075' y='250' width='22' height='230' fill='#140a06'/><path d='M1070 252 L1086 200 L1102 252Z' fill='#140a06'/>"
               "<path d='M940 432 Q980 360 1020 432Z' fill='#140a06'/>")
    wires = "<path d='M0 360 Q300 420 600 380 T1200 400' fill='none' stroke='#140a06' stroke-width='3'/>"
    return _wrap(defs, f"<rect width='{W}' height='{H}' fill='url(#g)'/>{sun}{wires}{city}{minaret}", "#3a1408")


def nightshift():
    defs = ("<linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#020409'/>"
            "<stop offset='1' stop-color='#0b1a2a'/></linearGradient>")
    stars = "".join(f"<circle cx='{x}' cy='{y}' r='2' fill='#e8f2ec' opacity='.6'/>"
                    for x, y in [(100, 80), (260, 140), (420, 60), (700, 110), (880, 70), (1010, 150), (1150, 90), (560, 180)])
    moon = "<circle cx='1020' cy='130' r='55' fill='#e8f2ec'/><circle cx='1045' cy='115' r='50' fill='#020409'/>"
    station = (
        "<rect x='180' y='300' width='840' height='46' fill='#e8f2ec'/>"
        "<rect x='180' y='346' width='840' height='10' fill='#39ff88'/>"
        "<rect x='260' y='356' width='16' height='220' fill='#1a2a38'/><rect x='924' y='356' width='16' height='220' fill='#1a2a38'/>"
        "<rect x='420' y='440' width='70' height='136' rx='8' fill='#c94a3a'/><rect x='434' y='460' width='42' height='30' fill='#ffd27a'/>"
        "<rect x='710' y='440' width='70' height='136' rx='8' fill='#c94a3a'/><rect x='724' y='460' width='42' height='30' fill='#ffd27a'/>"
        "<rect x='0' y='576' width='1200' height='99' fill='#05080c'/>"
        "<polygon points='180,356 1020,356 1100,576 100,576' fill='#39ff88' opacity='.07'/>"
        "<text x='600' y='334' font-family='system-ui,Arial,sans-serif' font-weight='800' font-size='30' text-anchor='middle' fill='#050807' letter-spacing='8'>NIGHT SHIFT</text>"
    )
    shadow = "<ellipse cx='1080' cy='560' rx='16' ry='50' fill='#000' opacity='.9'/><circle cx='1080' cy='500' r='14' fill='#000'/>"
    return _wrap(defs, f"<rect width='{W}' height='{H}' fill='url(#g)'/>{stars}{moon}{station}{shadow}", "#020409")


def iplik():
    defs = ("<linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#2a0f14'/>"
            "<stop offset='1' stop-color='#0d0507'/></linearGradient>")
    thread = ("<path d='M-20 520 C220 380 300 640 520 470 S820 160 980 300 S1160 420 1240 210' fill='none' stroke='#C94A5A' stroke-width='10' stroke-linecap='round'/>"
              "<path d='M-20 560 C240 420 320 680 540 510 S840 200 1000 340 S1180 460 1240 250' fill='none' stroke='#FFF9F5' stroke-width='3' opacity='.5'/>")
    quote = ("<text x='120' y='250' font-family='Georgia,serif' font-size='240' fill='#C94A5A' opacity='.9'>“</text>"
             "<text x='130' y='330' font-family='Georgia,serif' font-style='italic' font-size='54' fill='#FFF9F5'>Damlaya damlaya…</text>")
    return _wrap(defs, f"<rect width='{W}' height='{H}' fill='url(#g)'/>{thread}{quote}", "#0d0507")


def hicaz():
    import math
    lines = []
    for k, (amp, col, op) in enumerate([(70, '#39ff88', 1), (50, '#e8f2ec', .5), (95, '#1f6b43', .8)]):
        pts = " ".join(f"{x},{337 + amp*math.sin(x/(60+k*25)+k)*math.sin(x/400):.1f}" for x in range(0, 1201, 8))
        lines.append(f"<polyline points='{pts}' fill='none' stroke='{col}' stroke-width='5' opacity='{op}'/>")
    keys = "".join(f"<rect x='{80+i*76}' y='560' width='66' height='80' rx='6' fill='{'#39ff88' if i in (1, 4) else '#0f2219'}'/>" for i in range(14))
    return _wrap("", "".join(lines) + keys, "#050807")


def matlab():
    nums = "".join(
        f"<text x='{380+c*150}' y='{220+r*110}' font-family='ui-monospace,Menlo,monospace' font-size='56' fill='{'#39ff88' if (r+c)%3==0 else '#e8f2ec'}' text-anchor='middle'>{v}</text>"
        for r, row in enumerate([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]) for c, v in enumerate(row)
    )
    br = ("<path d='M300 140 H270 V590 H300' fill='none' stroke='#e8f2ec' stroke-width='8'/>"
          "<path d='M900 140 H930 V590 H900' fill='none' stroke='#e8f2ec' stroke-width='8'/>"
          "<text x='990' y='380' font-family='ui-monospace,Menlo,monospace' font-size='44' fill='#a3b8ab'>&gt;&gt; A'</text>")
    return _wrap("", nums + br, "#08110c")


def generic(name):
    initials = "".join(w[0] for w in name.replace("&", " ").split()[:2]).upper()
    grid = "".join(f"<line x1='{x}' y1='0' x2='{x}' y2='{H}' stroke='#0f2219' stroke-width='2'/>" for x in range(0, W + 1, 75))
    grid += "".join(f"<line x1='0' y1='{y}' x2='{W}' y2='{y}' stroke='#0f2219' stroke-width='2'/>" for y in range(0, H + 1, 75))
    txt = (f"<text x='600' y='400' font-family='system-ui,Arial,sans-serif' font-weight='800' font-size='200' "
           f"text-anchor='middle' fill='#e8f2ec' opacity='.9'>{initials}</text>"
           "<rect x='560' y='450' width='80' height='10' fill='#39ff88'/>")
    return _wrap("", grid + txt, "#050807")


BUILDERS = {
    "frogie": frogie, "shadow": shadow, "streets": streets, "nightshift": nightshift,
    "iplik": iplik, "hicaz": hicaz, "matlab": matlab,
}


def cover_svg(project):
    key = project.get("cover", "generic")
    if key in BUILDERS:
        return BUILDERS[key]()
    return generic(project["name"]["en"])
