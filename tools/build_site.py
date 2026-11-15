"""Builds the LENIX site (3D redesign) into the project root.

Run from anywhere:  python tools/build_site.py

Product copy, comparison tables and the demo blocks live in tools/build_pages.py (imported here as `old`).
This file owns the page shell, the home page chapters and the Platform and About pages.
To add a product: add it to PRODUCTS in build_pages.py, give it a shape below, and add a shape of that
name to assets/scene.js if none of the existing ones fits.
"""
import io
import os
import sys
from html import escape as e

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as old  # noqa: E402

ROOT = old.ROOT
ARW, SUN, MOON = old.ARW, old.SUN, old.MOON
PRODUCTS = old.PRODUCTS

# 3D shape the particle cloud takes for each product, and the stage of a working life it covers.
SHAPE = {"builtsync": "tower", "ezjob": "card", "courseatlas": "calendar", "smartsite": "site"}
STAGE = {"builtsync": "Run the site", "ezjob": "Hire", "courseatlas": "Train", "smartsite": "Secure the site"}
HOME_SHOT = {"smartsite": ("site-aerial.jpg", 1448, 1086, "Aerial view of a construction site")}

BOOT = """<script>
(function(){var d=document.documentElement,t;try{t=localStorage.getItem('lenix-theme')}catch(e){}
if(t!=='light'&&t!=='dark'){t=window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'}
d.setAttribute('data-theme',t);
if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)){d.classList.add('enter');
try{if(!sessionStorage.getItem('lenix-seen')){d.classList.add('first');sessionStorage.setItem('lenix-seen','1')}}catch(e){}}
})();
</script>"""

LOGO = ('<img class="on-dark" src="assets/logo-on-dark.png" alt="LENIX" width="628" height="220">'
        '<img class="on-light" src="assets/logo-on-light.png" alt="LENIX" width="655" height="220">')
CHEV = '<svg viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def btn(label, href, cls="solid", ext=False, mag=True, extra=""):
    return '<a class="btn %s%s" href="%s" data-t="%s"%s%s><span>%s</span>%s</a>' % (
        cls, " mag" if mag else "", href, e(label), ' target="_blank" rel="noopener"' if ext else "", extra, e(label), ARW)


def head(title, desc):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
%s
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/showcase.css">
<link rel="stylesheet" href="assets/app.css">
</head>
""" % (e(title), e(desc), BOOT)


def nav(current):
    is_prod = current in [p["slug"] + ".html" for p in PRODUCTS]
    panel = "".join(
        '<a href="%s.html" style="--c:%s"><i></i><span><b>%s</b><small>%s</small></span>%s</a>'
        % (p["slug"], p["accent"], e(p["name"]), e(p["kind"]), ARW) for p in PRODUCTS)
    links = [("platform.html", "Platform"), ("index.html#services", "Services"), ("about.html", "About")]

    def cur(h):
        return ' aria-current="page"' if h == current else ""
    flat = "".join('<a href="%s"%s>%s</a>' % (h, cur(h), t) for h, t in links)
    mobile = "".join('<a href="%s.html">%s <small>%s</small></a>' % (p["slug"], e(p["name"]), e(STAGE[p["slug"]])) for p in PRODUCTS)
    mobile += "".join('<a href="%s">%s</a>' % (h, t) for h, t in links) + '<a href="#contact">Talk to us</a>'
    return """<canvas id="gl" aria-hidden="true"></canvas>
<div class="grain" aria-hidden="true"></div>
<div class="veil" aria-hidden="true"><img src="assets/logo-on-dark.png" class="on-dark" alt=""><img src="assets/logo-on-light.png" class="on-light" alt=""><b>0</b></div>
<div class="cur" aria-hidden="true"><i></i><span></span></div>
<div class="progress" aria-hidden="true"></div>
<header class="nav" id="nav">
  <div class="nav-in">
    <a class="nav-logo" href="index.html" aria-label="LENIX home">%s</a>
    <nav class="nav-links" aria-label="Primary">
      <div class="nav-dd%s">
        <button type="button" aria-expanded="false" aria-haspopup="true">Products %s</button>
        <div class="nav-panel">%s<p>More products are on the way.</p></div>
      </div>
      %s
    </nav>
    <div class="nav-act">
      <button class="icon-btn js-theme" type="button" aria-label="Switch theme">%s%s</button>
      %s
      <button class="icon-btn nav-burger js-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span></button>
    </div>
  </div>
</header>
<nav class="mmenu" id="mmenu" aria-label="Mobile">%s
  <button class="js-theme" type="button"><span class="js-theme-label">Light theme</span></button>
</nav>
""" % (LOGO, " is-cur" if is_prod else "", CHEV, panel, flat, SUN, MOON, btn("Talk to us", "#contact", "solid sm"), mobile)


def close_cta(heading="Want a walkthrough or a pilot?"):
    return """<section class="close" id="contact" data-shape="xmark" data-alpha=".42">
  <div class="wrap">
    <h2 data-split>%s</h2>
    <p class="lede" data-r>Tell us about your sites and your workforce. We will show you the products on your own use case.</p>
    <div class="close-links" data-r>
      <a href="mailto:lenix@clarity.com.sg" data-cur="Email">lenix@clarity.com.sg</a>
      <a href="tel:+6589948015" data-cur="Call">+65 8994 8015</a>
    </div>
  </div>
</section>
""" % e(heading)


def footer(scripts=""):
    return """<footer class="ft">
  <div class="wrap">
    <a href="index.html" aria-label="LENIX home">%s</a>
    <nav aria-label="Footer">%s<a href="platform.html">Platform</a><a href="about.html">About</a></nav>
    <span>&copy; 2026 LENIX Pte Ltd. A Clarity Group company.</span>
  </div>
</footer>
<script src="assets/site.js"></script>
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/vendor/ScrollTrigger.min.js"></script>
<script src="assets/vendor/lenis.min.js"></script>
<script src="assets/app.js"></script>
<script type="module" src="assets/scene.js"></script>
%s</body>
</html>
""" % (LOGO, "".join('<a href="%s.html">%s</a>' % (p["slug"], e(p["name"])) for p in PRODUCTS), scripts)


def page(title, desc, current, main, accent="var(--violet)", scripts=""):
    return head(title, desc) + '<body style="--c:%s">\n%s<main>\n%s</main>\n%s' % (accent, nav(current), main, footer(scripts))


def wrap_shape(html, shape, alpha, pos="center"):
    return '<div data-shape="%s" data-alpha="%s" data-pos="%s">\n%s</div>\n' % (shape, alpha, pos, html)


def services(heading="The team behind the products."):
    rows = [("Venture Lab", "Incubates and tests new operational tools before they scale."),
            ("Pilot Data", "Runs data pilots that turn raw field signals into operational forecasts."),
            ("Digital Transformation", "Re-engineers legacy workflows into connected, data-driven systems."),
            ("IT Solutions", "Deploys and maintains the hardware, network and infrastructure that keep teams online.")]
    body = "".join('<div data-r><span class="mono">%s</span><h3>%s</h3><p>%s</p>%s</div>' % ("ABCD"[i], e(a), e(b), ARW) for i, (a, b) in enumerate(rows))
    return """<section class="band" id="services" data-shape="field" data-alpha=".34">
  <div class="wrap">
    <div class="shead">
      <h2 data-split>%s</h2>
      <p class="lede" data-r>Beyond its own platforms, LENIX builds, pilots and maintains the digital backbone between site and strategy.</p>
    </div>
    <div class="svc">%s</div>
  </div>
</section>
""" % (e(heading), body)


def clients():
    return """<section class="band" id="clients">
  <div class="wrap">
    <div class="shead">
      <h2 data-split>Reserved for the companies that build what comes next.</h2>
      <p class="lede" data-r>We are taking on pilot partners now, and this wall is kept for the companies that run on our products.</p>
    </div>
    %s
  </div>
</section>
""" % old.client_wall()


# --------------------------------------------------------------------------- home
def home():
    n = len(PRODUCTS)
    marks, panels, shots, rail = "", "", "", ""
    for i, p in enumerate(PRODUCTS):
        shape = SHAPE[p["slug"]]
        shot = p["shot"] or HOME_SHOT[p["slug"]]
        href, label = p["demo"]
        demo = btn(label, href if not href.startswith("#") else "%s.html%s" % (p["slug"], href), "line", ext=not href.startswith("#"))
        marks += '<i class="wp" data-shape="%s" data-pos="right" data-y="%s" style="top:calc((%d * 105vh - 60vh) * %d / %d + 62vh)"></i>' % (shape, "0.1" if shape == "tower" else "0.45", n, i, n)
        panels += """
      <article class="pp" style="--c:%s">
        <i class="wp-m" data-shape="%s" data-pos="right"></i>
        <span class="mono">%s</span>
        <h3>%s</h3>
        <p>%s</p>
        <ul>%s</ul>
        <div class="cta-row">%s%s</div>
        <a class="pv" href="%s.html" tabindex="-1" aria-hidden="true"><img src="assets/%s" alt="" width="%d" height="%d" loading="lazy"></a>
      </article>""" % (p["accent"], shape, e(p["kind"]), e(p["name"]), e(p["home_copy"]),
                       "".join("<li>%s</li>" % e(x) for x in p["home_feats"]),
                       btn("How %s works" % p["name"], p["slug"] + ".html"), demo, p["slug"], shot[0], shot[1], shot[2])
        shots += '<a href="%s.html" data-cur="Open" aria-label="%s: full breakdown"><img src="assets/%s" alt="%s" width="%d" height="%d" loading="lazy"></a>' % (
            p["slug"], e(p["name"]), shot[0], e(shot[3]), shot[1], shot[2])
        rail += '<button type="button" aria-pressed="false">%s</button>' % e(p["name"])

    steps = [("Hire", "Match verified skilled-trades and technical talent with the employers who need them.", "EZJOB", "ezjob.html", "var(--cyan)"),
             ("Train", "Find the right course on the right date, across Singapore's training providers.", "Course Atlas", "courseatlas.html", "var(--magenta)"),
             ("Deploy", "Check workers in on site with location and face verification, and see attendance live.", "BuiltSync", "builtsync.html", "var(--violet)"),
             ("Pay", "Turn verified hours into payslips that workers can confirm or dispute in the app.", "BuiltSync payroll", "builtsync.html#functions", "var(--violet)"),
             ("Secure", "Know who is on site and where they were last read, with one tag per worker, vehicle and item.", "Smart Site", "smartsite.html", "var(--orange)")]
    hp = "".join('<a class="hp" href="%s" style="--c:%s" data-cur="Open"><span class="mono">%s</span><h3>%s</h3><p>%s</p><span class="go">See how %s</span></a>'
                 % (h, c, e(prod), e(t), e(d), ARW) for t, d, prod, h, c in steps)
    hp += ('<a class="hp end" href="#contact" style="--c:var(--text-3)"><span class="mono">Next</span><h3>More to come</h3>'
           '<p>New tools start in our Venture Lab, with a site that needs them.</p><span class="go">Bring us a problem %s</span></a>' % ARW)

    names = "".join('<a href="%s.html"><span>%s</span></a>' % (p["slug"], e(p["name"])) for p in PRODUCTS) + '<span class="dim">More to come</span>'

    main = """<section class="h3" id="top" data-shape="globe" data-pos="right">
  <div class="wrap h3-in">
    <p class="h3-tag mono" data-h>LENIX. Workforce technology from Singapore</p>
    <h1 data-split="hero">Every workforce, connected.</h1>
    <p class="h3-sub" data-h>Hire skilled talent, train and certify your people, and run every site from check-in to payslip, on technology built to work together.</p>
    <div class="cta-row" data-h>%(b1)s%(b2)s</div>
  </div>
  <div class="wrap h3-foot mono" data-h><span>1.3521&deg; N, 103.8198&deg; E</span><span class="js-clock">SGT</span><span>A Clarity Group company</span></div>
</section>

%(chapter)s
<section class="hpan" id="journey" data-shape="thread" data-alpha=".3">
  <div class="hpan-pin">
    <div class="wrap">
      <div class="shead">
        <h2 data-split>Five moments in a working life. One product behind each.</h2>
        <p class="lede" data-r>Workforce data usually lives in job boards, training providers' inboxes, paper timesheets and payroll spreadsheets. LENIX builds the products that join those steps up.</p>
      </div>
    </div>
    <div class="hpan-track">%(hp)s</div>
    <div class="hpan-bar" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="band" id="products">
  <div class="wrap">
    <div class="shead">
      <h2 data-split>Four products under one umbrella.</h2>
      <p class="lede" data-r>Each one has its own page with what it does, a demo you can use, how it compares with the usual alternatives, and where it is stronger.</p>
    </div>
  </div>
</section>
<section class="pseq" style="--n:%(n)d" aria-label="Products">
  %(marks)s
  <div class="pseq-pin">%(panels)s
    <div class="pseq-vis">%(shots)s</div>
    <div class="pseq-rail" role="group" aria-label="Jump to a product">%(rail)s</div>
  </div>
</section>

<div class="mq" aria-hidden="true" data-shape="field" data-alpha=".4"><div class="mq-t">%(names)s%(names)s</div></div>

%(services)s
<section class="band" id="about">
  <div class="wrap split">
    <div>
      <h2 data-split>A technology company built from the project site up.</h2>
      <p class="lede" data-r>LENIX Pte Ltd is the digital products, data and IT arm of Clarity Group, a Singapore engineering, construction and industrial manpower group. Our products start from problems we see on real sites.</p>
      <div class="cta-row" data-r>%(b3)s%(b4)s</div>
    </div>
    %(facts)s
  </div>
</section>

%(clients)s
%(close)s""" % dict(
        b1=btn("Explore products", "#products"), b2=btn("Talk to us", "#contact", "line"),
        b3=btn("About LENIX", "about.html", "line"), b4=btn("See the platform", "platform.html", "line"),
        chapter=wrap_shape(old.chapter("One line from the first hire to the final payslip."), "thread", ".7"),
        hp=hp, n=n, marks=marks, panels=panels, shots=shots, rail=rail, names=names,
        services=services(), facts=FACTS, clients=clients(), close=close_cta())
    return page("LENIX | Connecting every workforce",
                "LENIX builds the technology that links the workforce together: EZJOB for hiring, Course Atlas for training, BuiltSync for running every project site and Smart Site for securing it.",
                "index.html", main)


FACTS = """<dl class="facts" data-r>
      <div><dt>Company</dt><dd>LENIX Pte Ltd</dd></div>
      <div><dt>Group</dt><dd><a href="https://www.clarity.com.sg/our-business/lenix" target="_blank" rel="noopener">Clarity Group</a></dd></div>
      <div><dt>Based in</dt><dd>Singapore</dd></div>
      <div><dt>Focus</dt><dd>Workforce technology, data and IT</dd></div>
    </dl>"""


# --------------------------------------------------------------------------- product pages
def product_page(i, p):
    nxt = PRODUCTS[(i + 1) % len(PRODUCTS)]
    slug, smart, shape = p["slug"], p["slug"] == "smartsite", SHAPE[p["slug"]]
    href, label = p["demo"]
    links = btn(label, href, "solid", ext=not href.startswith("#"))
    if p["second"]:
        links += btn(p["second"][1], p["second"][0], "line", ext=not p["second"][0].startswith("#"))
    links += btn("Talk to us", "#contact", "line")
    if p.get("note"):
        note = '<p class="note" data-h>%s</p>' % e(p["note"])
    elif slug == "builtsync":
        note = ""
    else:
        note = '<p class="note" data-h>%s is in preview and opens on a test address.</p>' % e(p["name"])

    fn_photos = old.MEDIA.get(slug, {}).get("fn_photos")
    fns = ""
    for k, (fa, fb, fc) in enumerate(p["functions"]):
        ph = ""
        if fn_photos is not None:
            ph = ('<span class="phero"><img src="assets/smartsite/%s.jpg" alt="" loading="lazy"></span>' % fn_photos[k]) if k in fn_photos else "<span></span>"
        fns += "<div><dt>%s<small>%s</small></dt><dd>%s</dd>%s</div>" % (e(fa), e(fb), e(fc), ph)
    ths = "".join('<th scope="col">%s</th>' % e(a) for a in p["alts"])
    rows = "".join('<tr><th scope="row">%s</th><td class="us">%s</td>%s</tr>' % (e(r[0]), e(r[1]), "".join("<td>%s</td>" % e(c) for c in r[2:])) for r in p["rows"])
    pros = "".join("<li><b>%s</b> %s</li>" % (e(a), e(b)) for a, b in p["pros"])

    demos = (old.builtsync_pre() if slug == "builtsync" else "") + old.scene(p) + (old.builtsync_post() if slug == "builtsync" else old.media_live(p))

    main = """<section class="phero" data-shape="%(shape)s" data-pos="right">
  <div class="wrap"><div class="phero-in">
    <nav class="crumbs" aria-label="Breadcrumb" data-h><a href="index.html">LENIX</a> / <a href="index.html#products">Products</a> / %(name)s</nav>
    <div data-h>%(logo)s</div>
    <p class="kind" data-h>%(kind)s</p>
    <h1 data-split="hero">%(h1)s</h1>
    <p class="lede" data-h>%(lede)s</p>
    <div class="cta-row" data-h>%(links)s</div>
    %(note)s
  </div></div>
</section>

%(chapter)s%(demos)s
<div data-shape="field" data-alpha=".16">
<div class="wrap doc">
  <nav class="toc" aria-label="On this page">
    <a href="#what">What it is</a>
    <a href="#functions">What it does</a>
    %(toc_mid)s<a href="#compare">How it compares</a>
    <a href="#verdict">Strengths</a>
    %(toc_end)s
  </nav>
  <div>
    <section class="sec" id="what">
      <h2>What %(name)s is, and the problem it is for</h2>
      <div class="prose">%(intro)s</div>
      %(figure)s
    </section>

    <section class="sec" id="functions">
      <h2>What it does, function by function</h2>
      <dl class="fn%(fn_cls)s">%(fns)s</dl>
      <div class="prose"><p><strong>Who it is for.</strong> %(audience)s</p></div>
    </section>
%(mid)s
    <section class="sec" id="compare">
      <h2>How it compares with the usual alternatives</h2>
      <div class="tbl-wrap" role="region" aria-label="Comparison table" tabindex="0">
        <table class="cmp">
          <thead><tr><th scope="col"><span class="sr">Criterion</span></th><th scope="col" class="us">%(name)s</th>%(ths)s</tr></thead>
          <tbody class="stagger">%(rows)s</tbody>
        </table>
      </div>
      <p class="tbl-note">The comparison is against the typical setup in each category, not a named product. Individual products and agencies differ, so check the ones you are considering.</p>
    </section>

    <section class="sec" id="verdict">
      <h2>Where %(name)s is stronger</h2>
      <div class="verdict solo"><div class="pro"><ul>%(pros)s</ul></div></div>
    </section>
%(end)s
  </div>
</div>
</div>

<div class="wrap" data-shape="%(nshape)s" data-pos="right" data-alpha=".85">
  <a class="nextp" href="%(nslug)s.html" data-cur="Next"><span class="mono">Next product</span><strong>%(nname)s %(arw)s</strong></a>
</div>
%(close)s""" % dict(
        shape=shape, name=e(p["name"]), logo=old.media_logo(p), kind=e(p["kind"]), h1=e(p["h1"]), lede=e(p["lede"]), links=links, note=note,
        chapter=wrap_shape(old.chapter(old.SHOWCASE[slug]["chapter"]), shape, ".45"),
        demos=wrap_shape(demos, "field", ".2"),
        intro="".join("<p>%s</p>" % x for x in p["intro"]), figure=old.media_figure(p),
        fn_cls=" has-photos" if fn_photos is not None else "", fns=fns, audience=e(p["audience"]), ths=ths, rows=rows, pros=pros,
        toc_mid='<a href="#demo">Demo</a>\n    ' if smart else "",
        toc_end='<a href="#rollout">Roll-out</a>\n    <a href="#more">What comes next</a>' if smart else "",
        mid=old.SMARTSITE_DEMO if smart else "", end=old.SMARTSITE_END if smart else "",
        nshape=SHAPE[nxt["slug"]], nslug=nxt["slug"], nname=e(nxt["name"]), arw=ARW,
        close=close_cta("See %s on your own site." % p["name"]))
    scripts = ('<script src="assets/builtsync/demo-data.js"></script>\n<script src="assets/demo.js"></script>\n<script src="assets/p2demo.js"></script>\n'
               if slug == "builtsync" else "")
    return page(p["title"], p["desc"], slug + ".html", main, accent=p["accent"], scripts=scripts)


# --------------------------------------------------------------------------- platform
def platform():
    tiles = "".join(
        '<a class="tile" href="%s.html" style="--c:%s" data-cur="Open" data-r><span class="mono">%s</span><h3>%s</h3><p>%s</p></a>'
        % (p["slug"], p["accent"], e(STAGE[p["slug"]]), e(p["name"]), e(p["home_copy"])) for p in PRODUCTS)
    tiles += ('<a class="tile open" href="#contact" style="--c:var(--text-3)" data-r><span class="mono">Next</span><h3>Your site\'s problem</h3>'
              '<p>New tools start in our Venture Lab, with a site that needs them. Bring us the step that still runs on paper.</p></a>')
    dirs = [("Gate read to attendance", "A Smart Site gate read that also starts the day's attendance in BuiltSync."),
            ("Certificate to gate", "An expired certificate in BuiltSync that turns the Smart Site gate screen red."),
            ("Course to access", "A course found in Course Atlas and completed becomes the authorisation a controlled room checks for.")]
    drows = "".join('<div data-r><h3>%s</h3><p>%s</p><span class="mono">Direction</span></div>' % (e(a), e(b)) for a, b in dirs)
    how = [("Start on site", "Our products start from problems we see on real project sites, not from a feature list."),
           ("Pilot first, then scale", "We start with a small pilot and widen it only when it has proved itself."),
           ("Compare plainly", "Every product page sets the product against the usual alternatives, row by row.")]
    hrows = "".join('<div data-r><span class="mono">%d</span><h3>%s</h3><p>%s</p>%s</div>' % (i + 1, e(a), e(b), ARW) for i, (a, b) in enumerate(how))
    main = """<section class="phero" data-shape="thread" data-pos="right" data-scale=".62">
  <div class="wrap"><div class="phero-in">
    <nav class="crumbs" aria-label="Breadcrumb" data-h><a href="index.html">LENIX</a> / Platform</nav>
    <p class="kind" data-h>The platform</p>
    <h1 data-split="hero">Four products. One working life.</h1>
    <p class="lede" data-h>A worker gets hired, gets trained, shows up on site and gets paid. LENIX builds a product for each of those moments, and designs them to meet.</p>
    <div class="cta-row" data-h>%(b1)s%(b2)s</div>
  </div></div>
</section>

%(chapter)s
<section class="band" id="stack" data-shape="globe" data-alpha=".3">
  <div class="wrap">
    <div class="shead">
      <h2 data-split>Where each product sits.</h2>
      <p class="lede" data-r>Each product stands on its own today, with its own page, demo and comparison. Pick the moment you need first.</p>
    </div>
    <div class="stack">%(tiles)s</div>
  </div>
</section>

<section class="band" id="joins" data-shape="thread" data-alpha=".4">
  <div class="wrap">
    <div class="shead">
      <h2 data-split>Where the products meet.</h2>
      <p class="lede" data-r>Once every worker has one identity, new controls are mostly a matter of rules and screens. These are the joins we are building toward with the sites that need them. They are directions, not products yet.</p>
    </div>
    <div class="dirs">%(drows)s</div>
  </div>
</section>

<section class="band" id="how" data-shape="field" data-alpha=".34">
  <div class="wrap">
    <div class="shead">
      <h2 data-split>How we build.</h2>
      <p class="lede" data-r>The same three habits sit behind every product on this site.</p>
    </div>
    <div class="svc">%(hrows)s</div>
  </div>
</section>
%(close)s""" % dict(b1=btn("See the products", "#stack"), b2=btn("Talk to us", "#contact", "line"),
                    chapter=wrap_shape(old.chapter("Hire. Train. Deploy. Pay. Secure. One thread."), "thread", ".8"),
                    tiles=tiles, drows=drows, hrows=hrows, close=close_cta("Bring us the step that still runs on paper."))
    return page("LENIX Platform | Four products, one working life",
                "How the LENIX products fit together: EZJOB for hiring, Course Atlas for training, BuiltSync for running the site and Smart Site for securing it.",
                "platform.html", main)


# --------------------------------------------------------------------------- about
def about():
    main = """<section class="phero" data-shape="globe" data-pos="right">
  <div class="wrap"><div class="phero-in">
    <nav class="crumbs" aria-label="Breadcrumb" data-h><a href="index.html">LENIX</a> / About</nav>
    <p class="kind" data-h>About LENIX</p>
    <h1 data-split="hero">Built from the project site up.</h1>
    <p class="lede" data-h>LENIX Pte Ltd is the digital products, data and IT arm of Clarity Group, a Singapore engineering, construction and industrial manpower group.</p>
    <div class="cta-row" data-h>%(b1)s%(b2)s</div>
  </div></div>
</section>

%(chapter)s
<section class="band" id="company" data-shape="field" data-alpha=".3">
  <div class="wrap split">
    <div>
      <h2 data-split>A technology company inside a construction group.</h2>
      <p class="lede" data-r>Our products start from problems we see on real sites: the gate log book, the paper timesheet, the certificate that expired without anyone noticing. We build the tool, pilot it, and widen it when it has proved itself.</p>
    </div>
    %(facts)s
  </div>
</section>

%(services)s
%(clients)s
%(close)s""" % dict(b1=btn("See the platform", "platform.html"), b2=btn("Talk to us", "#contact", "line"),
                    chapter=wrap_shape(old.chapter("Technology that links every workforce together."), "globe", ".6"),
                    facts=FACTS, services=services("What the team does."), clients=clients(), close=close_cta())
    return page("About LENIX | The technology arm of Clarity Group",
                "LENIX Pte Ltd is the digital products, data and IT arm of Clarity Group in Singapore.", "about.html", main)


def write(name, text):
    with io.open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote", name, len(text))


if __name__ == "__main__":
    write("index.html", home())
    for i, p in enumerate(PRODUCTS):
        write(p["slug"] + ".html", product_page(i, p))
    write("platform.html", platform())
    write("about.html", about())
