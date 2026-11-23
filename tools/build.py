# -*- coding: utf-8 -*-
"""Generate the static Runia0 site into the repository root.

Usage:  python3 tools/build.py
Output: index.html, en/index.html, gizlilik.html, en/privacy.html, 404.html,
        sitemap.xml, robots.txt
"""
import json
import os
from datetime import date
from html import escape as e

from content import BASE_URL, GITHUB, GROUPS, PROJECTS, T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()

PAGES = {
    "home": {"tr": "", "en": "en/"},
    "privacy": {"tr": "gizlilik.html", "en": "en/privacy.html"},
}

GH_ICON = (
    '<svg aria-hidden="true" viewBox="0 0 16 16" width="18" height="18"><path fill="currentColor" '
    'd="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
)

LOGO = (
    '<svg class="logo" aria-hidden="true" viewBox="0 0 64 64" width="32" height="32">'
    '<rect width="64" height="64" rx="14" fill="#0b1f14"/>'
    '<path d="M17 46V18h13a8 8 0 010 16H17m12 0l9 12" fill="none" stroke="#e8f2ec" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="45" cy="38" r="7" fill="none" stroke="#39ff88" stroke-width="4"/></svg>'
)


def prefix(lang):
    return "../" if lang == "en" else ""


def head(lang, page, title, desc):
    t = T[lang]
    p = prefix(lang)
    canonical = BASE_URL + PAGES[page][lang]
    alt_tr = BASE_URL + PAGES[page]["tr"]
    alt_en = BASE_URL + PAGES[page]["en"]
    og_locale = "tr_TR" if lang == "tr" else "en_US"
    og_alt = "en_US" if lang == "tr" else "tr_TR"
    ld = ""
    if page == "home":
        data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": BASE_URL + "#website",
                    "name": "Runia0",
                    "url": BASE_URL,
                    "inLanguage": ["tr", "en"],
                    "publisher": {"@id": BASE_URL + "#org"},
                },
                {
                    "@type": "Organization",
                    "@id": BASE_URL + "#org",
                    "name": "Runia0",
                    "url": BASE_URL,
                    "logo": BASE_URL + "assets/logo-512.png",
                    "slogan": "Ideas into things that work.",
                    "founder": {"@id": BASE_URL + "#founder"},
                    "sameAs": [GITHUB],
                },
                {
                    "@type": "Person",
                    "@id": BASE_URL + "#founder",
                    "name": "Berat Çetin",
                    "jobTitle": "Founder & Independent Developer",
                    "worksFor": {"@id": BASE_URL + "#org"},
                    "knowsAbout": [
                        "Software Development",
                        "Artificial Intelligence",
                        "Game Development",
                        "Digital Products",
                    ],
                },
            ],
        }
        ld = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{alt_tr}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_tr}">
<meta name="theme-color" content="#050807">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{p}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Runia0">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Runia0 — Ideas into things that work.">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{p}assets/style.css">
{ld}</head>
<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
"""


def header(lang, page, with_nav=True):
    t = T[lang]
    p = prefix(lang)
    home = p + PAGES["home"][lang] if lang == "tr" else p + "en/"
    home = home or "./"
    other = t["other"]
    other_href = p + PAGES[page][other] if PAGES[page][other] else p
    if other_href == "":
        other_href = "./"
    if lang == "tr" and other == "en":
        other_href = PAGES[page]["en"]
    if lang == "en" and other == "tr":
        other_href = "../" + PAGES[page]["tr"]
    nav = ""
    if with_nav:
        base = "" if page == "home" else home
        nav = f"""<nav aria-label="{'Ana menü' if lang == 'tr' else 'Main'}">
  <ul>
    <li><a href="{base}#focus">{e(t['nav_focus'])}</a></li>
    <li><a href="{base}#projects">{e(t['nav_projects'])}</a></li>
    <li><a href="{base}#about">{e(t['nav_about'])}</a></li>
    <li><a href="{base}#contact">{e(t['nav_contact'])}</a></li>
  </ul>
</nav>"""
    return f"""<header class="site-header">
<div class="wrap bar">
<a class="brand" href="{home}">{LOGO}<span>Runia0</span></a>
{nav}
<a class="lang" href="{other_href}" hreflang="{other}" lang="{other}"><span aria-hidden="true">{t['other_short']}</span><span class="sr">{e(t['other_label'])}</span></a>
</div>
</header>
"""


def footer(lang):
    t = T[lang]
    priv = PAGES["privacy"][lang]
    if lang == "en":
        priv = "privacy.html"
    return f"""<footer class="site-footer">
<div class="wrap foot">
<p class="mono">© {date.today().year} Runia0 · {e(t['footer'])}</p>
<ul>
<li><a href="{priv}">{e(t['privacy'])}</a></li>
<li><a href="{GITHUB}" rel="me">GitHub</a></li>
</ul>
</div>
</footer>
"""


def card(pr, lang):
    t = T[lang]
    concept = pr["group"] == "concept"
    stack = ""
    if pr["stack"]:
        stack = (
            f'<div class="meta"><dt>{e(t["stack"])}</dt><dd><ul class="tags">'
            + "".join(f"<li>{e(s)}</li>" for s in pr["stack"])
            + "</ul></dd></div>"
        )
    if pr.get("link"):
        link = f'<a class="ext" href="{pr["link"]}">{GH_ICON}{e(t["view_code"])}<span class="sr"> — {e(pr["name"][lang])}</span></a>'
    else:
        msg = pr.get("nolink", {}).get(lang, t["no_link"])
        link = f'<p class="nolink">{e(msg)}</p>'
    cats = " ".join(pr["cats"])
    return f"""<li class="card{' card--concept' if concept else ''}" data-cats="{cats}" data-group="{pr['group']}" id="p-{pr['id']}">
<article>
<h4>{e(pr['name'][lang])}</h4>
<p>{e(pr['desc'][lang])}</p>
<dl>
<div class="meta"><dt>{e(t['status'])}</dt><dd><span class="badge badge--{pr['group']}">{e(pr['status'][lang])}</span></dd></div>
<div class="meta"><dt>{e(t['role'])}</dt><dd>{e(pr['role'][lang])}</dd></div>
{stack}
</dl>
{link}
</article>
</li>"""


def home(lang):
    t = T[lang]
    out = [head(lang, "home", t["title"], t["description"]), header(lang, "home")]
    focus = "".join(
        f'<li class="focus-item"><span class="idx mono" aria-hidden="true">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>'
        for i, (a, b) in enumerate(t["focus"])
    )
    filters = "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(v)}</button>'
        for k, v in t["filters"]
    )
    groups = []
    for g in GROUPS:
        items = [card(p, lang) for p in PROJECTS if p["group"] == g]
        if not items:
            continue
        groups.append(
            f'<section class="group group--{g}" aria-labelledby="g-{g}" data-group-section="{g}">'
            f'<h3 id="g-{g}">{e(t["groups"][g])}</h3>'
            f'<ul class="cards" role="list">{"".join(items)}</ul></section>'
        )
    out.append(f"""<main id="main">
<section class="hero">
<div class="wrap">
<p class="kicker mono">{e(t['hero_kicker'])}</p>
<h1>Ideas into things that <span class="hl">work.</span></h1>
<p class="sub mono">Independent by nature. Built through code.</p>
<p class="lead">{e(t['hero_lead'])}</p>
<p class="ctas"><a class="btn btn--primary" href="#projects">{e(t['cta_projects'])}</a>
<a class="btn" href="{GITHUB}" rel="me">{GH_ICON}{e(t['cta_github'])}</a></p>
</div>
</section>

<section id="focus" class="section" aria-labelledby="focus-h">
<div class="wrap">
<h2 id="focus-h">{e(t['focus_title'])}</h2>
<ul class="focus" role="list">{focus}</ul>
</div>
</section>

<section id="projects" class="section" aria-labelledby="projects-h">
<div class="wrap">
<h2 id="projects-h">{e(t['projects_title'])}</h2>
<p class="note">{e(t['projects_note'])}</p>
<div class="filters" role="group" aria-label="{e(t['filter_label'])}">{filters}</div>
<p class="empty" hidden>{e(t['empty'])}</p>
<p class="sr" aria-live="polite" id="filter-status"></p>
{''.join(groups)}
</div>
</section>

<section id="about" class="section" aria-labelledby="about-h">
<div class="wrap about">
<h2 id="about-h">{e(t['about_title'])}</h2>
<div class="about-card">
<p class="about-name">{e(t['about_name'])}</p>
<p class="about-role">{e(t['about_role'])}</p>
<p>{e(t['about_text'])}</p>
</div>
</div>
</section>

<section id="contact" class="section" aria-labelledby="contact-h">
<div class="wrap">
<h2 id="contact-h">{e(t['contact_title'])}</h2>
<p>{e(t['contact_text'])}</p>
<p><a class="btn btn--primary" href="{GITHUB}" rel="me">{GH_ICON}github.com/Runia0</a></p>
</div>
</section>
</main>
""")
    out.append(footer(lang))
    out.append(f'<script src="{prefix(lang)}assets/main.js" defer></script>\n</body>\n</html>\n')
    return "".join(out)


def privacy(lang):
    t = T[lang]
    body = "".join(f"<p>{e(x)}</p>" for x in t["privacy_body"])
    home_href = "./" if lang == "tr" else "./"
    return (
        head(lang, "privacy", t["privacy_title"], t["privacy_desc"])
        + header(lang, "privacy", with_nav=False)
        + f"""<main id="main" class="section">
<div class="wrap prose">
<h1>{e(t['privacy_h1'])}</h1>
{body}
<p><a href="https://docs.github.com/{'en/' if lang == 'en' else ''}site-policy/privacy-policies/github-general-privacy-statement">{e(t['privacy_github'])}</a></p>
<p><a href="{home_href}">← {e(t['back_home'])}</a></p>
</div>
</main>
"""
        + footer(lang)
        + "</body>\n</html>\n"
    )


def not_found():
    # 404 is served from any path depth, so use absolute URLs.
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — Runia0</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{BASE_URL}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE_URL}assets/style.css">
</head>
<body>
<main id="main" class="section nf">
<div class="wrap prose">
<p class="kicker mono">404</p>
<h1>{T['tr']['nf_title']} <span class="muted" lang="en">/ {T['en']['nf_title']}</span></h1>
<p><a class="btn btn--primary" href="{BASE_URL}">{T['tr']['back_home']}</a>
<a class="btn" href="{BASE_URL}en/" lang="en">{T['en']['back_home']}</a></p>
</div>
</main>
</body>
</html>
"""


def sitemap():
    urls = []
    for page in PAGES:
        for lang in ("tr", "en"):
            loc = BASE_URL + PAGES[page][lang]
            alts = "".join(
                f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL + PAGES[page][l]}"/>'
                for l in ("tr", "en")
            )
            urls.append(f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>{alts}</url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n"
    )


def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n"


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel)


if __name__ == "__main__":
    write("index.html", home("tr"))
    write("en/index.html", home("en"))
    write("gizlilik.html", privacy("tr"))
    write("en/privacy.html", privacy("en"))
    write("404.html", not_found())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
