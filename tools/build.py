# -*- coding: utf-8 -*-
"""Generate the static Runia0 site into the repository root.

Usage:  python3 tools/build.py
"""
import json
import os
import posixpath
from datetime import date
from html import escape as e

from content import AI_ROLE, BASE_URL, FEATURED, GITHUB, GROUPS, LOG, PROJECTS, T
from covers import cover_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
BY_ID = {p["id"]: p for p in PROJECTS}


# ----------------------------------------------------------------- paths
def path(lang, key, pid=None):
    """Repository-relative file path of a page."""
    tr = {"home": "index.html", "projects": "projeler.html", "privacy": "gizlilik.html", "project": f"projeler/{pid}.html"}
    en = {"home": "en/index.html", "projects": "en/projects.html", "privacy": "en/privacy.html", "project": f"en/projects/{pid}.html"}
    return (tr if lang == "tr" else en)[key]


def pretty(p):
    """Public URL path (directory form for index pages)."""
    return p[: -len("index.html")] if p.endswith("index.html") else p


def absurl(p):
    return BASE_URL + pretty(p)


def rel(frm, to):
    """Relative link from page `frm` to repo path `to`."""
    r = posixpath.relpath(to, posixpath.dirname(frm) or ".")
    if r.endswith("index.html"):
        r = r[: -len("index.html")] or "./"
    return r


# ----------------------------------------------------------------- icons
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
ARROW = '<span aria-hidden="true">→</span>'


# ----------------------------------------------------------------- layout
def head(lang, me, key, title, desc, pid=None, ld=None, og_image=None):
    p = lambda to: rel(me, to)
    other = "en" if lang == "tr" else "tr"
    canonical = absurl(path(lang, key, pid))
    og = og_image or BASE_URL + "assets/og.png"
    lds = ""
    for block in ld or []:
        lds += '<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False) + "</script>\n"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{absurl(path('tr', key, pid))}">
<link rel="alternate" hreflang="en" href="{absurl(path('en', key, pid))}">
<link rel="alternate" hreflang="x-default" href="{absurl(path('tr', key, pid))}">
<meta name="theme-color" content="#050807">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{p('assets/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{p('assets/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p('assets/apple-touch-icon.png')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Runia0">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="{630 if not og_image else 675}">
<meta property="og:locale" content="{'tr_TR' if lang == 'tr' else 'en_US'}">
<meta property="og:locale:alternate" content="{'en_US' if lang == 'tr' else 'tr_TR'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{p('assets/style.css')}">
{lds}</head>
<body>
<a class="skip" href="#main">{e(T[lang]['skip'])}</a>
"""


def header(lang, me, key, pid=None):
    t = T[lang]
    home = rel(me, path(lang, "home"))
    homeh = "" if key == "home" else home
    other = t["other"]
    items = [
        (homeh + "#work", t["nav_work"]),
        (rel(me, path(lang, "projects")), t["nav_projects"]),
        (homeh + "#process", t["nav_process"]),
        (homeh + "#about", t["nav_about"]),
        (homeh + "#contact", t["nav_contact"]),
    ]
    cur = 1 if key in ("projects", "project") else -1
    nav = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if i == cur and key == "projects" else ""}>{e(lbl)}</a></li>'
        for i, (h, lbl) in enumerate(items)
    )
    return f"""<header class="site-header">
<div class="wrap bar">
<a class="brand" href="{home}">{LOGO}<span>Runia0</span></a>
<nav aria-label="{e(t['nav_label'])}"><ul>{nav}</ul></nav>
<a class="lang" href="{rel(me, path(other, key, pid))}" hreflang="{other}" lang="{other}"><span aria-hidden="true">{t['other_short']}</span><span class="sr">{e(t['other_label'])}</span></a>
</div>
</header>
"""


def footer(lang, me):
    t = T[lang]
    return f"""<footer class="site-footer">
<div class="wrap foot">
<p class="mono">© {date.today().year} Runia0 · {e(t['footer'])}</p>
<ul>
<li><a href="{rel(me, path(lang, 'projects'))}">{e(t['nav_projects'])}</a></li>
<li><a href="{rel(me, path(lang, 'privacy'))}">{e(t['privacy'])}</a></li>
<li><a href="{GITHUB}" rel="me">GitHub</a></li>
</ul>
</div>
</footer>
<script src="{rel(me, 'assets/main.js')}" defer></script>
</body>
</html>
"""


# ----------------------------------------------------------------- pieces
def cover_img(me, pr, lang, eager=False):
    alt = T[lang]["cover_alt"].format(name=pr["name"][lang])
    return (f'<img src="{rel(me, "assets/covers/" + pr["id"] + ".svg")}" alt="{e(alt)}" width="1200" height="675"'
            f'{"" if eager else " loading=\"lazy\""} decoding="async">')


def badge(pr, lang):
    return f'<span class="badge badge--{pr["group"]}">{e(pr["status"][lang])}</span>'


def card(me, pr, lang):
    t = T[lang]
    concept = pr["group"] == "concept"
    stack = ""
    if pr["stack"]:
        stack = (f'<div class="meta"><dt>{e(t["stack"])}</dt><dd><ul class="tags">'
                 + "".join(f"<li>{e(s)}</li>" for s in pr["stack"]) + "</ul></dd></div>")
    detail = rel(me, path(lang, "project", pr["id"]))
    if pr.get("link"):
        link = f'<a class="ext" href="{pr["link"]}">{GH_ICON}{e(t["view_code"])}<span class="sr"> — {e(pr["name"][lang])}</span></a>'
    else:
        link = f'<p class="nolink">{e(pr.get("nolink", {}).get(lang, t["no_link"]))}</p>'
    search = " ".join([pr["name"][lang], pr["desc"][lang], " ".join(pr["stack"]), pr["status"][lang]]).lower()
    return f"""<li class="card{' card--concept' if concept else ''}" data-cats="{' '.join(pr['cats'])}" data-group="{pr['group']}" data-search="{e(search)}">
<article>
<h3><a class="stretch" href="{detail}">{e(pr['name'][lang])}</a></h3>
<p>{e(pr['desc'][lang])}</p>
<dl>
<div class="meta"><dt>{e(t['status'])}</dt><dd>{badge(pr, lang)}</dd></div>
<div class="meta"><dt>{e(t['role'])}</dt><dd>{e(pr['role'][lang])}</dd></div>
{stack}
</dl>
{link}
</article>
</li>"""


def project_groups(me, lang, level="h3"):
    t = T[lang]
    out = []
    for g in GROUPS:
        items = [card(me, p, lang) for p in PROJECTS if p["group"] == g]
        if items:
            out.append(f'<section class="group group--{g}" aria-labelledby="g-{g}" data-group-section="{g}">'
                       f'<{level} id="g-{g}">{e(t["groups"][g])}</{level}>'
                       f'<ul class="cards" role="list">{"".join(items)}</ul></section>')
    return "".join(out)


def org_ld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": BASE_URL + "#website", "name": "Runia0", "url": BASE_URL,
             "inLanguage": ["tr", "en"], "publisher": {"@id": BASE_URL + "#org"}},
            {"@type": "Organization", "@id": BASE_URL + "#org", "name": "Runia0", "url": BASE_URL,
             "logo": BASE_URL + "assets/logo-512.png", "slogan": "Ideas into things that work.",
             "founder": {"@id": BASE_URL + "#founder"}, "sameAs": [GITHUB]},
            {"@type": "Person", "@id": BASE_URL + "#founder", "name": "Berat Çetin",
             "jobTitle": "Founder & Independent Developer", "worksFor": {"@id": BASE_URL + "#org"},
             "knowsAbout": ["Software Development", "Artificial Intelligence", "Game Development", "Digital Products"]},
        ],
    }


def crumbs_ld(lang, trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]}


def fmt_date(d, lang):
    y, m = d.split("-")[:2]
    tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    en = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{(tr if lang == 'tr' else en)[int(m) - 1]} {y}"


# ----------------------------------------------------------------- pages
def home(lang):
    t = T[lang]
    me = path(lang, "home")
    n_projects = len(PROJECTS)
    n_games = sum(1 for p in PROJECTS if "games" in p["cats"] and p["status"]["en"].lower().startswith("playable"))
    featured = "".join(
        f"""<li class="feat">
<article>
<div class="feat-img">{cover_img(me, BY_ID[i], lang)}</div>
<div class="feat-body">
<p class="feat-meta">{badge(BY_ID[i], lang)}<span class="mono muted">{' · '.join(BY_ID[i]['stack'][:3])}</span></p>
<h3><a class="stretch" href="{rel(me, path(lang, 'project', i))}">{e(BY_ID[i]['name'][lang])}</a></h3>
<p>{e(BY_ID[i]['desc'][lang])}</p>
<span class="more">{e(t['details'])} {ARROW}</span>
</div>
</article>
</li>""" for i in FEATURED)
    focus = "".join(
        f'<li class="focus-item"><span class="idx mono" aria-hidden="true">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>'
        for i, (a, b) in enumerate(t["focus"]))
    process = "".join(
        f'<li class="step"><span class="idx mono" aria-hidden="true">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>'
        for i, (a, b) in enumerate(t["process"]))
    stack = sorted({s for p in PROJECTS for s in p["stack"]}, key=str.lower)
    stack_html = "".join(f"<li>{e(s)}</li>" for s in stack)
    log = "".join(f'<li><time datetime="{d}" class="mono">{d}</time><p>{e(txt[lang])}</p></li>' for d, txt in LOG)
    body = f"""<main id="main">
<section class="hero">
<div class="hero-grid" aria-hidden="true"></div>
<div class="wrap hero-in">
<div>
<p class="kicker mono">{e(t['hero_kicker'])}</p>
<h1>Ideas into things that <span class="hl">work.</span></h1>
<p class="sub mono">Independent by nature. Built through code.</p>
<p class="lead">{e(t['hero_lead'])}</p>
<p class="ctas"><a class="btn btn--primary" href="{rel(me, path(lang, 'projects'))}">{e(t['cta_projects'])}</a>
<a class="btn" href="{GITHUB}" rel="me">{GH_ICON}{e(t['cta_github'])}</a></p>
</div>
<div class="term" aria-hidden="true">
<div class="term-bar"><i></i><i></i><i></i><span class="mono">runia0 ~ build</span></div>
<pre class="mono"><span class="c">$</span> runia0 status
<span class="ok">●</span> frogie            <span class="d">playable</span>
<span class="ok">●</span> shadow-protocol   <span class="d">playable</span>
<span class="ok">●</span> sokaklarin-kanunu <span class="d">playable</span>
<span class="wip">●</span> iplik             <span class="d">pre-release</span>
<span class="wip">●</span> night-shift       <span class="d">early dev</span>
<span class="c">$</span> <span class="cursor">▍</span></pre>
</div>
</div>
<div class="wrap">
<ul class="stats" role="list">
<li><b>{n_projects}</b><span>{e(t['stat_projects'])}</span></li>
<li><b>{n_games}</b><span>{e(t['stat_games'])}</span></li>
<li><b>2</b><span>{e(t['stat_langs'])}</span></li>
</ul>
</div>
</section>

<section id="work" class="section" aria-labelledby="work-h">
<div class="wrap">
<div class="sec-head"><h2 id="work-h">{e(t['featured_title'])}</h2>
<a class="link-more" href="{rel(me, path(lang, 'projects'))}">{e(t['all_projects'])} {ARROW}</a></div>
<ul class="feats" role="list">{featured}</ul>
<p class="note small">{e(t['featured_note'])}</p>
</div>
</section>

<section id="focus" class="section" aria-labelledby="focus-h">
<div class="wrap">
<h2 id="focus-h">{e(t['focus_title'])}</h2>
<ul class="focus" role="list">{focus}</ul>
</div>
</section>

<section id="process" class="section" aria-labelledby="process-h">
<div class="wrap">
<h2 id="process-h">{e(t['process_title'])}</h2>
<ol class="steps" role="list">{process}</ol>
<p class="ai-note">{e(t['process_ai'])}</p>
<h3 class="sub-h">{e(t['stack_title'])}</h3>
<ul class="tags tags--lg" role="list">{stack_html}</ul>
</div>
</section>

<section id="log" class="section" aria-labelledby="log-h">
<div class="wrap">
<h2 id="log-h">{e(t['log_title'])}</h2>
<ol class="log" role="list">{log}</ol>
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
"""
    return head(lang, me, "home", t["title"], t["description"], ld=[org_ld()]) + header(lang, me, "home") + body + footer(lang, me)


def projects_page(lang):
    t = T[lang]
    me = path(lang, "projects")
    filters = "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(v)}</button>'
        for k, v in t["filters"])
    body = f"""<main id="main" class="section">
<div class="wrap">
<h1>{e(t['projects_title'])}</h1>
<p class="note">{e(t['projects_note'])}</p>
<div class="toolbar">
<label class="search"><span class="sr">{e(t['search_label'])}</span>
<input type="search" id="q" placeholder="{e(t['search_ph'])}" autocomplete="off"></label>
<div class="filters" role="group" aria-label="{e(t['filter_label'])}">{filters}</div>
</div>
<p class="empty" hidden>{e(t['empty'])}</p>
<p class="sr" aria-live="polite" id="filter-status" data-label="{e(t['shown'])}"></p>
{project_groups(me, lang, "h2")}
</div>
</main>
"""
    title = f"{t['projects_title']} — Runia0"
    ld = [crumbs_ld(lang, [(t["home"], absurl(path(lang, "home"))), (t["projects_title"], absurl(me))])]
    return head(lang, me, "projects", title, t["projects_desc"], ld=ld) + header(lang, me, "projects") + body + footer(lang, me)


def project_page(lang, pr):
    t = T[lang]
    pid = pr["id"]
    me = path(lang, "project", pid)
    name = pr["name"][lang]
    meta = [
        (t["status"], badge(pr, lang)),
        (t["role"], e(pr["role"][lang])),
    ]
    if pr.get("date"):
        meta.append((t["date"], f'<time datetime="{pr["date"]}">{fmt_date(pr["date"], lang)}</time>'))
    if pr["stack"]:
        meta.append((t["stack"], '<ul class="tags">' + "".join(f"<li>{e(s)}</li>" for s in pr["stack"]) + "</ul>"))
    meta_html = "".join(f'<div class="meta"><dt>{e(k)}</dt><dd>{v}</dd></div>' for k, v in meta)
    if pr.get("link"):
        link = f'<p><a class="btn btn--primary" href="{pr["link"]}">{GH_ICON}{e(t["view_code"])}</a></p>'
    else:
        link = f'<p class="nolink">{e(pr.get("nolink", {}).get(lang, t["no_link"]))}</p>'
    sections = ""
    if pr.get("overview"):
        sections += f'<section aria-labelledby="ov"><h2 id="ov">{e(t["overview"])}</h2>' + "".join(f"<p>{e(x)}</p>" for x in pr["overview"][lang]) + "</section>"
    if pr.get("features"):
        sections += f'<section aria-labelledby="ft"><h2 id="ft">{e(t["features"])}</h2><ul class="checks">' + "".join(f"<li>{e(x)}</li>" for x in pr["features"][lang]) + "</ul></section>"
    if pr.get("next"):
        sections += f'<section aria-labelledby="nx"><h2 id="nx">{e(t["next"])}</h2><ul class="checks checks--todo">' + "".join(f"<li>{e(x)}</li>" for x in pr["next"][lang]) + "</ul></section>"
    if pr.get("notes"):
        sections += f'<aside class="callout"><p><b>{e(t["notes"])}:</b> {e(pr["notes"][lang])}</p></aside>'
    # neighbours
    idx = PROJECTS.index(pr)
    prev_p, next_p = PROJECTS[idx - 1], PROJECTS[(idx + 1) % len(PROJECTS)]
    pager = (f'<nav class="pager" aria-label="{e(t["nav_projects"])}">'
             f'<a href="{rel(me, path(lang, "project", prev_p["id"]))}"><span aria-hidden="true">←</span> {e(prev_p["name"][lang])}</a>'
             f'<a href="{rel(me, path(lang, "project", next_p["id"]))}">{e(next_p["name"][lang])} <span aria-hidden="true">→</span></a></nav>')
    body = f"""<main id="main" class="section">
<div class="wrap">
<nav class="crumbs" aria-label="{e(t['breadcrumb'])}"><ol>
<li><a href="{rel(me, path(lang, 'home'))}">{e(t['home'])}</a></li>
<li><a href="{rel(me, path(lang, 'projects'))}">{e(t['projects_title'])}</a></li>
<li aria-current="page">{e(name)}</li></ol></nav>
<div class="detail-head">
<div>
<h1>{e(name)}</h1>
<p class="lead">{e(pr['desc'][lang])}</p>
<dl class="detail-meta">{meta_html}</dl>
{link}
</div>
<div class="detail-img">{cover_img(me, pr, lang, eager=True)}</div>
</div>
<div class="prose detail-body">{sections}</div>
<p><a href="{rel(me, path(lang, 'projects'))}"><span aria-hidden="true">←</span> {e(t['back_projects'])}</a></p>
{pager}
</div>
</main>
"""
    title = f"{name} — Runia0"
    ld = [crumbs_ld(lang, [(t["home"], absurl(path(lang, "home"))), (t["projects_title"], absurl(path(lang, "projects"))), (name, absurl(me))])]
    return (head(lang, me, "project", title, pr["desc"][lang], pid=pid, ld=ld)
            + header(lang, me, "project", pid) + body + footer(lang, me))


def privacy(lang):
    t = T[lang]
    me = path(lang, "privacy")
    body_txt = "".join(f"<p>{e(x)}</p>" for x in t["privacy_body"])
    gh = f"https://docs.github.com/{'en/' if lang == 'en' else ''}site-policy/privacy-policies/github-general-privacy-statement"
    body = f"""<main id="main" class="section">
<div class="wrap prose">
<h1>{e(t['privacy_h1'])}</h1>
{body_txt}
<p><a href="{gh}">{e(t['privacy_github'])}</a></p>
<p><a href="{rel(me, path(lang, 'home'))}"><span aria-hidden="true">←</span> {e(t['back_home'])}</a></p>
</div>
</main>
"""
    return head(lang, me, "privacy", t["privacy_title"], t["privacy_desc"]) + header(lang, me, "privacy") + body + footer(lang, me)


def not_found():
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


def all_pages():
    pages = []
    for key in ("home", "projects", "privacy"):
        pages.append((key, None))
    for p in PROJECTS:
        pages.append(("project", p["id"]))
    return pages


def sitemap():
    urls = []
    for key, pid in all_pages():
        for lang in ("tr", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{absurl(path(l, key, pid))}"/>' for l in ("tr", "en"))
            urls.append(f"<url><loc>{absurl(path(lang, key, pid))}</loc><lastmod>{TODAY}</lastmod>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


def write(relpath, text):
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    import shutil
    for d in ("projeler", "en/projects", "assets/covers"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    for lang in ("tr", "en"):
        write(path(lang, "home"), home(lang))
        write(path(lang, "projects"), projects_page(lang))
        write(path(lang, "privacy"), privacy(lang))
        for p in PROJECTS:
            write(path(lang, "project", p["id"]), project_page(lang, p))
    for p in PROJECTS:
        write(f"assets/covers/{p['id']}.svg", cover_svg(p))
    write("404.html", not_found())
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n")
    print(f"built {len(all_pages()) * 2} pages, {len(PROJECTS)} covers")
