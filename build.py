#!/usr/bin/env python3
"""
Static generator for the Idaho Falls Luxury RV Park redesign prototype.

Run:  python3 build.py            -> builds for GitHub Pages (/iflrv-redesign)
      BASE= python3 build.py      -> builds for a domain root (/)
"""
import os, re, shutil, html

BASE = os.environ.get('BASE', '/iflrv-redesign').rstrip('/')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')
SITE = 'https://zach0589.github.io' + BASE
MEDIA = 'https://idahofallsluxuryrvpark.com'

PHONE = '(208) 881-4562'
PHONE_HREF = 'tel:+12088814562'
EMAIL = 'admin@idahofallsluxuryrvpark.com'
ADDR = '3000 S Yellowstone Hwy, Idaho Falls, ID 83402'
LOGO = '/media/5hylfmfo/ifluxuryrvpark_logohorizontal_whitetext_11-20-23.png'
BOOK = 'https://bookingsus.newbook.cloud/idahofallsluxuryrvpark/index.php'

def u(path):
    """Internal URL, prefixed for whatever root the site is served from."""
    return (BASE + path) if path.startswith('/') else path

ICON_ASSETS = ('water-heater', 'bus-stop', 'lounge.png', 'camper-van', 'barbeque',
               'light-bulb', 'mountain', 'eating.png', 'road.png', 'cityscape',
               'statue-of-liberty', 'telephone', 'mail-2', 'reservation.png',
               'happy-shopper', 'rv-share', 'sprinterland-02')

def asset(path):
    """Internal asset URL with a content hash, so a redeploy can't be served
    from a stale browser/CDN cache (which is exactly what happened when the
    awards CSS changed but browsers kept the old file)."""
    import hashlib
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), path.lstrip('/'))
    try:
        h = hashlib.md5(open(local, 'rb').read()).hexdigest()[:8]
    except OSError:
        return u(path)
    return f'{u(path)}?v={h}'


def img(src, alt, w=1200, cls='', loading='lazy', ratio=None):
    """Responsive image off their Umbraco media pipeline (supports width + webp)."""
    sep = '&' if '?' in src else '?'
    one = f'{MEDIA}{src}{sep}width={w}&format=webp'
    two = f'{MEDIA}{src}{sep}width={w*2}&format=webp'
    c = f' class="{cls}"' if cls else ''
    r = f' style="aspect-ratio:{ratio}"' if ratio else ''
    # NOTE: alt text is mandatory here — every image on the live site ships alt=""
    assert alt, f'missing alt text for {src}'
    # These are line-art icons and wordmarks in the media library, not photographs.
    # Using one as a photo is the single most repeated mistake in this rebuild.
    assert not any(k in src for k in ICON_ASSETS), f'{src} is an icon/logo, not a photograph'
    assert '&#' not in alt and '&mdash;' not in alt, f'alt text must be plain: {alt!r}'
    return (f'<img{c}{r} src="{one}" srcset="{one} 1x, {two} 2x" '
            f'alt="{html.escape(alt)}" loading="{loading}" decoding="async">')

# ---------------------------------------------------------------- navigation
NAV = [
    ('Stay', '/stay/', [
        ('/stay/',          'All Sites &amp; Rates',   'Compare all 59 sites side by side'),
        ('/stay/rv-sites/', 'RV Sites',                'Pull-through &amp; back-in, 36&#39; &times; 80&#39;'),
        ('/stay/casitas/',  'SprinterLand Casitas',    'Covered shelter, heaters, masonry BBQ'),
        ('/stay/extended/', 'Extended &amp; Seasonal', 'Monthly rates and summer-long stays'),
    ]),
    ('Rates', '/rates/', None),
    ('The Park', '/park/amenities/', [
        ('/park/amenities/', 'Amenities',   'Lodge, pickleball, dog park, laundry'),
        ('/park/map/',       'Park Map',    'See exactly where your site sits'),
        ('/park/gallery/#tour', '360&deg; Virtual Tour', 'Walk the roads before you arrive'),
        ('/park/gallery/',   'Photo Gallery', 'Sites, lodge, casitas and the river'),
        ('/park/policies/',  'Policies',    'Cancellation, pets, rig age, check-in'),
    ]),
    ('Explore', '/explore/', [
        ('/explore/#yellowstone', 'Yellowstone &amp; Tetons', 'Drive times from the park gate'),
        ('/explore/#local',       'In Idaho Falls',           'Greenbelt, downtown, the falls'),
        ('/explore/#dining',      'Where to Eat',             'Local favorites minutes away'),
        ('/explore/#july4',       '4th of July',              'The biggest week of our year'),
    ]),
    ('FAQ', '/faq/', None),
    ('About', '/about/', None),
]

def nav_html(active):
    out = []
    for label, href, panel in NAV:
        cur = ' aria-current="page"' if active and active.startswith(href.rstrip('/')) and href != '/' else ''
        if panel:
            pid = 'panel-' + re.sub(r'[^a-z]', '', label.lower())
            links = ''.join(
                f'<li><a href="{u(h)}">{t}<small>{d}</small></a></li>' for h, t, d in panel)
            out.append(
                f'<li class="nav-item has-panel" data-open="false">'
                f'<button class="nav-link" aria-expanded="false" aria-controls="{pid}"{cur}>'
                f'{label}<span class="chev" aria-hidden="true"></span></button>'
                f'<ul class="nav-panel" id="{pid}">{links}</ul></li>')
        else:
            out.append(f'<li class="nav-item"><a class="nav-link" href="{u(href)}"{cur}>{label}</a></li>')
    return ''.join(out)

# ---------------------------------------------------------------- chrome
def header(active):
    return f'''
<div class="site-top">
<div class="utility"><div class="wrap-wide">
  <div class="utility-awards">
    <span>&#9733; Idaho&#39;s Best RV Park &mdash; Statewide</span>
    <span>&#9733; RV Life Best of the Best</span>
  </div>
  <div><a href="{PHONE_HREF}">{PHONE}</a> &middot; Open daily 10am&ndash;6pm</div>
</div></div>
<header class="site-header">
  <div class="wrap-wide">
    <a class="brand" href="{u('/')}" aria-label="Idaho Falls Luxury RV Park &mdash; home">
      <img class="brand-light" src="{MEDIA}{LOGO}?width=420&amp;format=webp"
           alt="Idaho Falls Luxury RV Park" width="210" height="44">
    </a>
    <nav aria-label="Main">
      <ul class="nav">{nav_html(active)}
        <li class="nav-cta"><a class="btn btn-primary btn-sm" href="{u('/rates/')}">Check Availability</a></li>
      </ul>
    </nav>
    <button class="nav-toggle" aria-expanded="false" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
</div>'''

def footer():
    return f'''
<footer class="site-footer" id="site-footer">
  <div class="wrap-wide">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="{MEDIA}{LOGO}?width=440&amp;format=webp"
             alt="Idaho Falls Luxury RV Park" loading="lazy">
        <p>Fifty-nine oversized, fully paved sites on the Snake River &mdash; two miles from
           downtown Idaho Falls and two hours from Yellowstone&#39;s west gate.</p>
        <div class="socials">
          <a href="https://www.facebook.com/idahofallsluxuryrvpark" aria-label="Idaho Falls Luxury RV Park on Facebook">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.96h-1.51c-1.49 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg>
          </a>
          <a href="https://www.instagram.com/idahofallsluxuryrvpark/" aria-label="Idaho Falls Luxury RV Park on Instagram">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.89 2.38 7.15 2.23 8.42 2.18 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.2-4.35-2.62-6.78-6.98-6.98C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 100 12.32 6.16 6.16 0 000-12.32zM12 16a4 4 0 110-8 4 4 0 010 8zm6.41-11.85a1.44 1.44 0 100 2.88 1.44 1.44 0 000-2.88z"/></svg>
          </a>
        </div>
      </div>
      <div>
        <h4>Stay</h4>
        <ul>
          <li><a href="{u('/stay/')}">Compare all sites</a></li>
          <li><a href="{u('/stay/rv-sites/')}">RV sites</a></li>
          <li><a href="{u('/stay/casitas/')}">SprinterLand casitas</a></li>
          <li><a href="{u('/stay/extended/')}">Extended &amp; seasonal</a></li>
          <li><a href="{u('/rates/')}">Rates &amp; availability</a></li>
        </ul>
      </div>
      <div>
        <h4>The Park</h4>
        <ul>
          <li><a href="{u('/park/amenities/')}">Amenities</a></li>
          <li><a href="{u('/park/map/')}">Park map</a></li>
          <li><a href="{u('/park/gallery/#tour')}">360&deg; virtual tour</a></li>
          <li><a href="{u('/park/gallery/')}">Photo gallery</a></li>
          <li><a href="{u('/park/policies/')}">Policies</a></li>
          <li><a href="{u('/faq/')}">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <div class="footer-hours">
          <div><span>Office</span><b>Daily 10am&ndash;6pm</b></div>
          <div><span>Check-in</span><b>1:00 PM</b></div>
          <div><span>Check-out</span><b>11:00 AM</b></div>
        </div>
        <p class="mt2">
          <a href="https://maps.google.com/?q={ADDR.replace(' ', '+')}">{ADDR.replace(', Idaho Falls', '<br>Idaho Falls')}</a><br><br>
          <a href="{PHONE_HREF}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>
      </div>
    </div>
    <div class="footer-bottom">
      <div>&copy; 2026 Idaho Falls Luxury RV Park</div>
      <nav aria-label="Legal">
        <a href="{u('/park/policies/')}">Policies</a>
        <a href="{u('/contact/')}">Contact</a>
        <a href="#top">Back to top</a>
      </nav>
    </div>
  </div>
</footer>
<div class="bookbar">
  <div class="bookbar-price"><strong>Check availability</strong><span>59 sites &middot; on the Snake River</span></div>
  <a class="btn btn-primary" href="{u('/rates/')}">Book</a>
</div>'''

# ---------------------------------------------------------------- layout
def page(slug, title, desc, body, active=None, has_hero=False, jsonld='', og_img=None):
    canonical = SITE + (slug if slug != '/' else '/')
    og = og_img or '/media/cy0lrm2y/droneparknexttoriver.jpg'
    cls = ' class="has-hero"' if has_hero else ''
    ld = f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Idaho Falls Luxury RV Park">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{MEDIA}{og}?width=1200&amp;format=webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f3830">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="{MEDIA}">
<link href="https://fonts.googleapis.com/css2?family=Mohave:wght@400;500;600;700&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('/assets/css/site.css')}">
{ld}
</head>
<body{cls} id="top">
<a class="skip" href="#main">Skip to main content</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="{asset('/assets/js/site.js')}" defer></script>
</body>
</html>'''

def write(slug, content):
    path = OUT + (slug if slug.endswith('/') else slug + '/')
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(content)
    print('  ', slug)

# ---------------------------------------------------------------- components
def booking_widget(compact=False):
    """The single biggest fix: let people search before they leave for NewBook."""
    return f'''
<form class="booking" data-booking-form>
  <div class="booking-grid booking-grid-6">
    <div class="booking-field">
      <label for="arrive{compact}">Arrive</label>
      <input type="date" id="arrive{compact}" name="arrive" required>
    </div>
    <div class="booking-field">
      <label for="depart{compact}">Depart</label>
      <input type="date" id="depart{compact}" name="depart" required>
    </div>
    <div class="booking-field">
      <label for="guests{compact}">Guests</label>
      <select id="guests{compact}" name="adults">
        <option value="2">2 guests</option>
        <option value="1">1 guest</option>
        <option value="3">3 guests</option>
        <option value="4">4 guests</option>
        <option value="5">5 guests</option>
        <option value="6">6+ guests</option>
      </select>
    </div>
    <div class="booking-field">
      <label for="rig{compact}">Rig length</label>
      <select id="rig{compact}" name="rig">
        <option value="">Any length</option>
        <option value="25">Up to 25 ft</option>
        <option value="35">26&ndash;35 ft</option>
        <option value="45">36&ndash;45 ft</option>
        <option value="46">Over 45 ft</option>
      </select>
    </div>
    <div class="booking-field">
      <label for="cat{compact}">Site type</label>
      <select id="cat{compact}" name="category">
        <option value="">All 59 sites</option>
        <option value="pull-through">Pull-through full hookup</option>
        <option value="back-in">Back-in full hookup</option>
        <option value="casita">SprinterLand casita</option>
        <option value="ultimate">Ultimate Pull-In</option>
      </select>
    </div>
    <button class="btn btn-primary" type="submit">Search dates</button>
  </div>
  <p class="booking-note">
    <span aria-hidden="true">&#128274;</span>
    Secure booking through NewBook &middot; free cancellation up to 48 hours before arrival
  </p>
</form>'''

def cta_band(img_src, alt, heading, text, primary=('Check availability', '/rates/')):
    return f'''
<section class="section cta-band">
  {img(img_src, alt, 1800, loading='lazy')}
  <div class="wrap">
    <h2>{heading}</h2>
    <p class="lede">{text}</p>
    <div class="cta-actions">
      <a class="btn btn-primary btn-lg" href="{u(primary[1])}">{primary[0]}</a>
      <a class="btn btn-ghost-light btn-lg" href="{PHONE_HREF}">Call {PHONE}</a>
    </div>
  </div>
</section>'''

def crumbs(items):
    """Visual breadcrumbs plus the matching BreadcrumbList, emitted together so
    the two can never drift apart."""
    import json
    parts, el = [], []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            parts.append(f'<a href="{u(href)}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>' if i else label)
        node = {'@type': 'ListItem', 'position': i + 1,
                'name': html.unescape(re.sub('<[^>]+>', '', label))}
        if href:
            node['item'] = SITE + href
        el.append(node)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                     'itemListElement': el})
    return ('<div class="crumbs"><div class="wrap">'
            + '<span aria-hidden="true">/</span>'.join(parts) + '</div></div>'
            + f'<script type="application/ld+json">{ld}</script>')

def page_hero(img_src, alt, eyebrow, h1, sub):
    return f'''
<section class="hero hero-page">
  <div class="hero-media">{img(img_src, alt, 1800, loading='eager')}</div>
  <div class="hero-inner"><div class="wrap">
    <span class="eyebrow" style="color:#7fd4bd">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="hero-sub mb0">{sub}</p>
  </div></div>
</section>'''

def acc(items, group=None, start=0):
    """items = [(id, question, answer_html)]"""
    out = []
    if group:
        out.append(f'<h3>{group}</h3>')
    out.append('<div class="acc">')
    for i, (aid, q, a) in enumerate(items):
        out.append(f'''<div class="acc-item">
  <h4 style="margin:0"><button class="acc-btn" id="{aid}" aria-expanded="false" aria-controls="p-{aid}">
    <span>{q}</span><span class="acc-icon" aria-hidden="true"></span></button></h4>
  <div class="acc-panel" id="p-{aid}" role="region" aria-labelledby="{aid}">
    <div class="acc-panel-inner">{a}</div>
  </div>
</div>''')
    out.append('</div>')
    return ''.join(out)

PROTO = lambda t: f'<div class="proto"><div>{t}</div></div>'

# ================================================================ HOME
DRIVE = [
    ('Downtown Idaho Falls', '2 miles', '5 min'),
    ('I-15, Exit 116', '2 miles', '5 min'),
    ('Yellowstone &mdash; West Entrance', '110 miles', '2 hrs'),
    ('Grand Teton National Park', '70&ndash;100 miles', '1.5&ndash;2 hrs'),
    ('Jackson Hole', 'Under 100 miles', '~2 hrs'),
    ('Salt Lake City', '215 miles', '3.5&ndash;4 hrs'),
]

SITE_CARDS = [
    ('/stay/rv-sites/', '/media/120ohllo/idaho-falls-luxury-rv-park-idaho-falls-id-20220929-001.jpg',
     'A motorhome and tow vehicle on a paved, landscaped pull-through site',
     'Pull-Through Full Hookup', '32 sites',
     "Pull in, level up, and never unhitch. 36&#39; &times; 80&#39; of paved pad with 50/30-amp power, water, sewer and a hotspot of your own.",
     ['36&#39; &times; 80&#39; paved &amp; level', '50 &amp; 30 amp full hookup', 'Fire pit + artisan picnic table']),
    ('/stay/rv-sites/', '/media/kwcbbwkw/3-1-1.png',
     'A travel trailer with its awning out and camp chairs set up on a paved site',
     'Back-In Full Hookup', '26 sites',
     'The same oversized paved footprint as our pull-throughs, angled to open your patio side toward the green space.',
     ['36&#39; &times; 80&#39; paved &amp; level', '50 &amp; 30 amp full hookup', 'Patio side faces open lawn']),
    ('/stay/casitas/', '/media/yunlwroj/dsc00664.jpg',
     'A camper van parked beside its SprinterLand casita shelter and fire pit',
     'SprinterLand Casita', '10 sites',
     'Your own covered outdoor room: ceiling heaters, party lights, two Adirondack chairs and a masonry charcoal BBQ.',
     ['3-sided shelter w/ privacy walls', 'Electric ceiling heaters', 'Masonry charcoal barbecue']),
    ('/stay/casitas/#ultimate', '/media/2hbfonwd/ultimate-pull-in.jpg',
     'The Ultimate Pull-In site, a large grassy site with a custom shelter beside open space',
     'The Ultimate Pull-In', '1 site',
     "The owner&#39;s favorite. One large grassy site backing onto open space, with a custom masonry BBQ under its own shelter.",
     ['One-of-a-kind site', 'Grassy, adjacent to open space', 'Custom masonry BBQ']),
]

def home():
    cards = ''
    for href, src, alt, name, count, blurb, feats in SITE_CARDS:
        cards += f'''
<article class="card">
  <div class="card-media">{img(src, alt, 720)}</div>
  <div class="card-body">
    <div class="tag-row"><span class="tag">{count}</span></div>
    <h3>{name}</h3>
    <p>{blurb}</p>
    <ul class="features mt1" style="gap:.45rem;font-size:.88rem">
      {''.join(f'<li>{f}</li>' for f in feats)}
    </ul>
    <div class="card-foot">
      <a class="btn btn-outline btn-sm" href="{u(href)}">See this site type</a>
    </div>
  </div>
</article>'''

    rows = ''.join(
        f'<tr><th scope="row">{n}</th><td>{m}</td><td>{t}</td></tr>' for n, m, t in DRIVE)

    ld = '''{"@context":"https://schema.org","@type":"Campground","name":"Idaho Falls Luxury RV Park",
"description":"Fifty-nine oversized, fully paved full-hookup RV sites on the Snake River in Idaho Falls, Idaho.",
"address":{"@type":"PostalAddress","streetAddress":"3000 S Yellowstone Hwy","addressLocality":"Idaho Falls","addressRegion":"ID","postalCode":"83402","addressCountry":"US"},
"telephone":"+1-208-881-4562","email":"admin@idahofallsluxuryrvpark.com",
"url":"''' + SITE + '''/","petsAllowed":true,
"amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Full hookups","value":true},
{"@type":"LocationFeatureSpecification","name":"High-speed Wi-Fi","value":true},
{"@type":"LocationFeatureSpecification","name":"Dog park","value":true},
{"@type":"LocationFeatureSpecification","name":"Pickleball courts","value":true},
{"@type":"LocationFeatureSpecification","name":"Laundry","value":true}]}'''

    body = f'''
<section class="hero">
  <div class="hero-media">
    <!-- The still is the video's own first frame, so when the loop fades in
         nothing on screen moves. It is also the only thing phones, reduced-motion
         and Save-Data visitors ever download. -->
    <img class="hero-still"
         src="{asset('/assets/video/hero-1400.jpg')}"
         srcset="{asset('/assets/video/hero-900.jpg')} 900w, {asset('/assets/video/hero-1400.jpg')} 1400w, {asset('/assets/video/hero-1600.jpg')} 1600w"
         sizes="100vw" width="1600" height="900" fetchpriority="high" decoding="async"
         alt="The Snake River and the Greenbelt trail running past the RV park">
    <video class="hero-video" muted loop playsinline preload="none"
           data-src="{asset('/assets/video/hero.mp4')}" aria-hidden="true" tabindex="-1"></video>
    <button class="hero-motion" type="button" data-motion hidden>
      <span class="hero-motion-ico" aria-hidden="true"></span><span data-motion-label>Pause</span>
    </button>
  </div>
  <div class="hero-inner"><div class="wrap">
    <span class="eyebrow">Idaho Falls, Idaho &middot; On the Snake River</span>
    <h1>The largest paved sites in East Idaho</h1>
    <p class="hero-sub">Fifty-nine oversized, fully paved full-hookup sites &mdash; two miles from downtown,
      two hours from Yellowstone, and a gate away from fourteen miles of riverside trail.</p>
    <div data-bookbar-anchor>{booking_widget()}</div>
  </div></div>
</section>

<section class="section-sm" style="background:var(--sand)">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b>59</b><span>Paved sites</span></div>
      <div class="stat"><b>36&times;80</b><span>Feet per site</span></div>
      <div class="stat"><b>50<span style="font-size:1.3rem">amp</span></b><span>Full hookups</span></div>
      <div class="stat"><b>2<span style="font-size:1.3rem">mi</span></b><span>To downtown</span></div>
      <div class="stat"><b>14<span style="font-size:1.3rem">mi</span></b><span>Greenbelt at the gate</span></div>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap">
    <p class="eyebrow center">Recognized</p>
    <div class="awards">
      <figure>{img('/media/li4hq32r/img_3424.png', "Idaho's Best of 2025 statewide winner badge", 420)}</figure>
      <figure>{img('/media/ettnarzb/img_3425.png', "Idaho's Best of 2025 Eastern Idaho winner badge", 420)}</figure>
      <figure class="awards-wide">{img('/media/3rcjp3ob/best-of-the-best-2025.png', 'RV Life Best of the Best campground 2025 winner badge', 420)}</figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Choose your site</span>
      <h2>Four ways to stay</h2>
      <p class="lede">Every site is paved, level and fully serviced. What changes is how much
        outdoor room comes with it &mdash; and whether you ever have to back up.</p>
    </div>
    <div class="grid g4">{cards}</div>
    <p class="center mt3">
      <a class="btn btn-dark btn-lg" href="{u('/stay/')}">Compare all four side by side</a>
      <a class="btn btn-outline btn-lg" href="{u('/park/gallery/#tour')}" style="margin-left:.6rem">Take the 360&deg; tour</a>
    </p>
  </div>
</section>

<section class="section section-deep">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Basecamp</span>
        <h2>Close to everything worth driving to</h2>
        <p class="lede" style="color:rgba(255,255,255,.88)">Idaho Falls is the closest real city to
          Yellowstone&#39;s west gate &mdash; which means full hookups, a grocery run and a hot tiled
          shower at the end of a park day, instead of a gravel pad in a gateway town.</p>
        <div class="compare-wrap mt2" style="background:transparent;border-color:rgba(255,255,255,.2)">
          <table class="compare" style="min-width:0;color:rgba(255,255,255,.85)">
            <caption class="sr">Driving distances and times from Idaho Falls Luxury RV Park</caption>
            <thead><tr>
              <th scope="col" style="background:rgba(255,255,255,.08);color:#fff;border-bottom-color:rgba(255,255,255,.2)">Destination</th>
              <th scope="col" style="background:rgba(255,255,255,.08);color:#fff;border-bottom-color:rgba(255,255,255,.2)">Distance</th>
              <th scope="col" style="background:rgba(255,255,255,.08);color:#fff;border-bottom-color:rgba(255,255,255,.2)">Drive</th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        <p class="mt2"><a class="btn btn-ghost-light" href="{u('/explore/')}">Plan your trip from here</a></p>
      </div>
      <div class="split-media">{img('/media/xn3bssaz/dronesunset.jpg',
        'Sunset over the RV park and the Snake River valley', 1000)}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split reverse">
      <div class="split-media">{img('/media/vxxccmwh/19.jpg',
        'The lodge lounge with leather seating, rugs and a stone fireplace', 1000)}</div>
      <div>
        <span class="eyebrow">The park</span>
        <h2>Built by a homebuilder, not a developer</h2>
        <p class="lede">Randy Sebastian spent three decades building high-end homes in Portland before
          turning that standard loose on an RV park. It shows in the details you notice on day two.</p>
        <ul class="features mt2">
          <li>Five private bathrooms &mdash; full tile showers, heated floors</li>
          <li>The region&#39;s largest outdoor community fireplace</li>
          <li>Two regulation pickleball courts and a fenced dog park</li>
          <li>Site-specific Wi-Fi &mdash; your own hotspot, not a shared signal</li>
          <li>Camp store, two 24-hour laundry rooms, beach cruisers for the Greenbelt</li>
          <li>Gated property with guest-only access codes</li>
        </ul>
        <p class="mt2"><a class="btn btn-outline" href="{u('/park/amenities/')}">All amenities</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="split">
      <div class="split-media">{img('/media/12cbkpnp/sunriselandscape.jpg',
        'The park and the Snake River from the air at sunrise', 1000)}</div>
      <div>
        <span class="eyebrow">Our story</span>
        <h2>It started as a drive-in theater</h2>
        <p>The Sky-Vu Drive-In opened here in 1950 and brought families together beside the Snake
          River for decades. When the Teichert and Sebastian families found it &mdash; closed ten years,
          equipment stripped &mdash; they saw the same thing the theater&#39;s owners had.</p>
        <p>Ground broke in 2021. The park opened in May 2023. It has since been named
          Idaho&#39;s Best RV Park.</p>
        <p class="mt2"><a class="btn btn-outline" href="{u('/about/')}">Read the full story</a></p>
      </div>
    </div>
  </div>
</section>

{cta_band('/media/2g2dxrsl/dronesummer-updated.jpg',
  'Aerial view of the park in full summer with RVs on every site',
  'Your site is waiting',
  'Check live availability, pick your pad, and book in about ninety seconds.')}
'''
    return page('/', 'Idaho Falls RV Park | Full-Hookup Sites on the Snake River',
                "59 oversized paved 50-amp full-hookup RV sites on the Snake River. Two miles from downtown "
                "Idaho Falls, two hours from Yellowstone. Check dates and rates.",
                body, active='/', has_hero=True, jsonld=ld)

# ================================================================ STAY HUB
COMPARE_ROWS = [
    ('How many',        ['32 sites', '26 sites', '10 sites', '1 site']),
    ('Pad size',        ['36&#39; &times; 80&#39;', '36&#39; &times; 80&#39;', '36&#39; &times; 80&#39;', 'Large grassy site']),
    ('Surface',         ['Paved &amp; level', 'Paved &amp; level', 'Paved &amp; level', 'Grass with paved patio']),
    ('Park &amp; go',   ['<span class="yes">Pull-through</span>', 'Back-in',
                         'Back-in', '<span class="yes">Pull-in</span>']),
    ('Electric',        ['50 &amp; 30 amp', '50 &amp; 30 amp', '50 &amp; 30 amp', '50 &amp; 30 amp']),
    ('Water &amp; sewer', ['<span class="yes">Yes</span>'] * 4),
    ('Site-specific Wi-Fi', ['<span class="yes">Yes</span>'] * 4),
    ('Fire pit',        ['<span class="yes">Yes</span>'] * 4),
    ('Artisan picnic table', ['<span class="yes">Yes</span>'] * 4),
    ('Covered shelter', ['<span class="no">&mdash;</span>', '<span class="no">&mdash;</span>',
                         '<span class="yes">3-sided casita</span>', '<span class="yes">Open-air</span>']),
    ('Ceiling heaters', ['<span class="no">&mdash;</span>', '<span class="no">&mdash;</span>',
                         '<span class="yes">Yes</span>', '<span class="yes">Yes</span>']),
    ('Masonry charcoal BBQ', ['<span class="no">&mdash;</span>', '<span class="no">&mdash;</span>',
                              '<span class="yes">Yes</span>', '<span class="yes">Custom-built</span>']),
    ('Second patio',    ['<span class="no">&mdash;</span>', '<span class="no">&mdash;</span>',
                         '<span class="yes">Yes</span>', '<span class="yes">Yes</span>']),
    ('Adirondack chairs', ['<span class="no">&mdash;</span>', '<span class="no">&mdash;</span>',
                           '<span class="yes">Two</span>', '<span class="yes">Two</span>']),
    ('Best for',        ['Big rigs, one-nighters', 'Longer stays, patio life',
                         'Vans, teardrops, anyone who lives outside', 'A splurge you remember']),
]
COMPARE_COLS = ['Pull-Through', 'Back-In', 'SprinterLand Casita', 'Ultimate Pull-In']
RATE_NOTE = ('<b>Rates are not published anywhere on the current site.</b> Drop your real nightly '
             'and seasonal numbers into <code>RATES</code> in <code>build.py</code> and they will '
             'appear here, on every site-type page and in the comparison table. '
             'Nothing on this page invents a price.')

def stay():
    head = ''.join(f'<th scope="col">{c}</th>' for c in COMPARE_COLS)
    rows = ''
    for label, cells in COMPARE_ROWS:
        rows += f'<tr><th scope="row">{label}</th>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
    rows += ('<tr><th scope="row">From</th>' +
             ''.join('<td><span class="card-price">$&mdash;</span><small class="muted"> / night</small></td>'
                     for _ in COMPARE_COLS) + '</tr>')
    rows += ('<tr><th scope="row"></th>' +
             ''.join(f'<td><a class="btn btn-primary btn-sm" href="{u("/rates/")}">Check dates</a></td>'
                     for _ in COMPARE_COLS) + '</tr>')

    body = crumbs([('Home', '/'), ('Stay', None)]) + f'''
{page_hero('/media/2g2dxrsl/dronesummer-updated.jpg',
  'Aerial view of the park showing pull-through and back-in site rows',
  'Stay', 'All 59 sites, compared',
  'Same hookups, same paved pads, same 36-by-80 footprint. The difference is how much outdoor room comes with it.')}

<section class="section-sm" style="background:var(--sand)">
  <div class="wrap" data-bookbar-anchor>{booking_widget(compact=2)}</div>
</section>

<section class="section">
  <div class="wrap-wide">
    <div class="section-head">
      <span class="eyebrow">Side by side</span>
      <h2>Pick the site, then pick the dates</h2>
      <p>The current site makes you read four separate pages and guess. Here it is in one table.</p>
    </div>
    {PROTO(RATE_NOTE)}
    <div class="compare-wrap mt2">
      <table class="compare">
        <caption class="sr">Comparison of the four site types at Idaho Falls Luxury RV Park</caption>
        <thead><tr><th scope="col"><span class="sr">Feature</span></th>{head}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="small muted mt2">All 59 sites are paved, level and full-hookup. The 10 SprinterLand casita
      sites are part of the 59 &mdash; they are back-in sites with a casita shelter added.</p>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Staying a while?</span>
      <h2>Extended and seasonal stays</h2>
      <p class="lede">A limited number of sites carry a discounted monthly rate, and a handful of
        seasonal spots run Memorial Day through Labor Day.</p>
    </div>
    <p class="center"><a class="btn btn-dark btn-lg" href="{u('/stay/extended/')}">Extended &amp; seasonal stays</a></p>
  </div>
</section>

{cta_band('/media/dronesunrise.jpg'.replace('/media/', '/media/f3pk4rhy/'),
  'Sunrise over the RV park with mist on the river',
  'Ready when you are', 'Live availability, real-time pricing, and a booking that takes about ninety seconds.')}
'''
    return page('/stay/', 'Compare All 59 RV Sites | Idaho Falls Luxury RV Park',
                'Compare all 59 sites side by side — pull-through, back-in, SprinterLand casita and the '
                'Ultimate Pull-In. Pad sizes, hookups and what each one includes.',
                body, active='/stay', has_hero=True,
                og_img='/media/2g2dxrsl/dronesummer-updated.jpg')

# ================================================================ RV SITES
def rv_sites():
    body = crumbs([('Home', '/'), ('Stay', '/stay/'), ('RV Sites', None)]) + f'''
{page_hero('/media/eslbo5ci/idaho-falls-luxury-rv-park-idaho-falls-id-20220929-016.jpg',
  'A motorhome pulling into a paved site at the park',
  'RV Sites', 'Pull-through &amp; back-in',
  '58 of our 59 sites, every one of them 36 by 80 feet of paved, level, fully serviced pad.')}

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">32 sites</span>
        <h2>Pull-through full hookup</h2>
        <p class="lede">Arrive late, pull straight in, level up and stay hitched. Built for Class A
          motorhomes, fifth wheels and oversized rigs &mdash; roads and pads are paved end to end,
          so there is no gravel to wrestle in the dark.</p>
        <ul class="features mt2">
          <li>36&#39; &times; 80&#39; paved, level pad</li>
          <li>50-amp and 30-amp service, water and sewer at the site</li>
          <li>Site-specific high-speed Wi-Fi &mdash; your own hotspot</li>
          <li>Fire pit and a custom artisan picnic table</li>
          <li>Clear sky access for Starlink and satellite TV</li>
        </ul>
        <p class="mt2"><a class="btn btn-primary" href="{u('/rates/')}">Check availability</a></p>
      </div>
      <div class="split-media">{img('/media/fgwolhjr/dji_0104.jpg',
        'Rows of paved full-hookup sites seen from the air', 1000)}</div>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="split reverse">
      <div>
        <span class="eyebrow">26 sites</span>
        <h2>Back-in full hookup</h2>
        <p class="lede">The identical 36-by-80 paved footprint and the identical hookups &mdash;
          angled so your patio side and awning open toward the open lawn rather than your neighbor&#39;s
          slide-out.</p>
        <ul class="features mt2">
          <li>36&#39; &times; 80&#39; paved, level pad</li>
          <li>50-amp and 30-amp service, water and sewer at the site</li>
          <li>Patio side oriented to the green space</li>
          <li>Fire pit and a custom artisan picnic table</li>
        </ul>
        <p class="mt2"><a class="btn btn-primary" href="{u('/rates/')}">Check availability</a></p>
      </div>
      <div class="split-media">{img('/media/30ppmizv/idaho-falls-luxury-rv-park-20230519-008-1.jpg',
        'A fifth wheel parked on a site beside open lawn', 1000)}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Good to know</span>
      <h2>The answers people call about</h2>
    </div>
    <div class="grid g3">
      <div class="card"><div class="card-body">
        <h3>Will my rig fit?</h3>
        <p>Sites are 36&#39; &times; 80&#39;, which handles oversized Class A motorhomes, fifth wheels
          and travel trailers with room for a tow vehicle. Two vehicles per site, and both must fit on the pad.</p></div></div>
      <div class="card"><div class="card-body">
        <h3>Will Starlink work?</h3>
        <p>Yes. Every site has clear sky access with no major obstructions, so Starlink and satellite
          TV set up without hunting for a window.</p></div></div>
      <div class="card"><div class="card-body">
        <h3>Can I have a fire?</h3>
        <p>Every site includes a fire pit, and campfires are allowed whenever local fire restrictions
          permit. Firewood is in the camp store, and we will deliver it to your site.</p></div></div>
    </div>
    <p class="center mt3"><a class="btn btn-outline" href="{u('/faq/')}">Read all FAQs</a></p>
  </div>
</section>

{cta_band('/media/uybnzgyf/dji_0055.jpg',
  'RVs parked on paved sites beside open lawn',
  'Book a pull-through', 'Check live availability for your dates and rig length.')}
'''
    return page('/stay/rv-sites/', 'Pull-Through &amp; Back-In RV Sites | Idaho Falls Luxury RV Park',
                '58 paved, level 36x80ft full-hookup sites with 50-amp service, water, sewer and private '
                'Wi-Fi. Pull-through and back-in, built for oversized rigs.',
                body, active='/stay', has_hero=True,
                og_img='/media/f3hlpx5h/idaho-falls-luxury-rv-park-20230519-038-scaled-1.jpg')

# ================================================================ CASITAS
def casitas():
    feats = [
        ('Shelter', 'A cozy 3-sided outdoor shelter with 5-foot privacy walls, to keep the weather off.',
         '/media/2eafmd2d/casita-back-in-2.jpg', 'Inside a casita shelter, with privacy walls and Adirondack chairs'),
        ('Heating', 'Built-in electric ceiling heaters take the chill off mornings and evenings.',
         '/media/irjnazpz/fallcasita57aiedit.png', 'A casita shelter and fire pit in autumn'),
        ('Seating', 'Two Adirondack chairs for stretching your legs out and doing nothing in particular.',
         '/media/dkxpsbza/casita-back-in.jpg', 'Two Adirondack chairs under a casita shelter'),
        ('Grilling', 'A masonry charcoal barbecue built into the shelter. Charcoal is in the camp store.',
         '/media/tsckx5wy/fallcasita57charcuterie.png', 'A charcuterie board laid out at a casita'),
    ]
    cards = ''.join(f'''
<article class="card">
  <div class="card-media">{img(s, a, 700)}</div>
  <div class="card-body"><h3>{t}</h3><p>{d}</p></div>
</article>''' for t, d, s, a in feats)

    body = crumbs([('Home', '/'), ('Stay', '/stay/'), ('SprinterLand Casitas', None)]) + f'''
{page_hero('/media/ldiedk2y/sprinterland-opt.jpg',
  'A SprinterLand casita shelter beside a paved site',
  'SprinterLand', 'Ten sites with an outdoor room attached',
  'Built for adventure vans and teardrops — and for anyone who would rather live outside the rig than inside it.')}

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What it is</span>
      <h2>A casita on your site</h2>
      <p class="lede">Ten of our 59 sites are anchored by a casita &mdash; a built structure that turns
        a parking pad into an outdoor living room. A firepit and a separate patio with a picnic table
        finish it off.</p>
    </div>
    <div class="grid g4">{cards}</div>
  </div>
</section>

<section class="section section-deep">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Why SprinterLand</span>
        <h2>For the nights between boondocks</h2>
        <p class="lede" style="color:rgba(255,255,255,.88)">Adventurers love getting off the beaten
          path. But eventually a hot shower is required, clothes need washing, and a work project
          needs real bandwidth.</p>
        <p>SprinterLand is the stop where you refresh and regroup &mdash; five private tiled bathrooms
          with heated floors, two 24-hour laundry rooms, and Wi-Fi that belongs to your site alone.</p>
        <ul class="features light mt2">
          <li>Sized for adventure vans and small teardrop trailers</li>
          <li>Full hookups, same as every other site</li>
          <li>Inside a gated park two miles from downtown</li>
        </ul>
      </div>
      <div class="split-media">{img('/media/2f4jr1ka/dsc00665.jpg',
        'A Sprinter van parked at its site beside the picnic table', 1000)}</div>
    </div>
  </div>
</section>

<section class="section" id="ultimate">
  <div class="wrap">
    <div class="split reverse">
      <div>
        <span class="eyebrow">One site only</span>
        <h2>The Ultimate Pull-In</h2>
        <p class="lede">The owner&#39;s favorite site in the park. Pull your motorhome in &mdash; no
          backing, no spotting &mdash; and step out into an open-air shelter with a custom-built
          masonry BBQ, two Adirondack chairs, ceiling heaters and party lights.</p>
        <p>It is a large grassy site adjacent to open space, with its own patio, picnic table and a
          firepit close by. There is exactly one, so it goes early.</p>
        <p class="mt2"><a class="btn btn-primary" href="{u('/rates/')}">Check if it&#39;s open</a></p>
      </div>
      <div class="split-media">{img('/media/qlbhvwn3/ultimate-pull-in-opt.jpg',
        'The Ultimate Pull-In site with its custom shelter and masonry barbecue', 1000)}</div>
    </div>
  </div>
</section>

{cta_band('/media/pzioqoyq/iflrv-04.jpg',
  'The SprinterLand sign hanging under a casita shelter',
  'Ten casitas. That&#39;s it.', 'Check which dates still have one open.')}
'''
    return page('/stay/casitas/', 'SprinterLand Casita Sites | Idaho Falls Luxury RV Park',
                'Ten premium sites with a private casita shelter — ceiling heaters, masonry charcoal BBQ, '
                'Adirondack chairs and a second patio. Built for adventure vans.',
                body, active='/stay', has_hero=True, og_img='/media/ldiedk2y/sprinterland-opt.jpg')

# ================================================================ EXTENDED
EXT_RULES = [
    ('rule-clean', 'Keeping your site', 'Each site must be kept clean and tidy. Lawn ornaments are not '
     'permitted. If trash of any kind is found on site when you leave, a $50 cleaning fee is charged. '
     'For fire safety, cigarette butts found on site result in a verbal warning, then termination of the stay. '
     'Trash may not be piled in your fire pit &mdash; all trash goes to the appropriate receptacles.'),
    ('rule-audit', 'Site audits', 'Sites are audited every 30&ndash;31 days to confirm they are being kept '
     'clean and tidy. Failing an audit may bring additional charges. If problems are not resolved, you will '
     'have 7 days to leave the property.'),
    ('rule-age', 'RV age and condition', 'All RVs must be 10 years old or newer, and must be in good '
     'external condition regardless of age.'),
    ('rule-skirt', 'Skirting and storage', 'Any insulation material used at the base of the RV must be '
     'covered or hidden by skirting &mdash; ask park staff for clarification. No straw or hay, due to pests '
     'and rodents. No permanent structures, and no storage of boxes or bins around the RV.'),
    ('rule-veh', 'Vehicles', 'Vehicles must fit on your site, two maximum. Guests of campers park at the '
     'bath house or lodge parking spots, not on the roads. The speed limit is 7.5 MPH &mdash; after three '
     'warnings you will be asked to leave. This is for the safety of every guest.'),
    ('rule-pets', 'Pets', 'No pet enclosures, and no excessive barking or noise. Always pick up after your '
     'pet anywhere in the park, including on your own site.'),
]

def extended():
    body = crumbs([('Home', '/'), ('Stay', '/stay/'), ('Extended &amp; Seasonal', None)]) + f'''
{page_hero('/media/ujwlgfbg/dronesummer.jpg',
  'The park from above in mid-summer with RVs on nearly every site',
  'Extended &amp; Seasonal', 'Stay a month. Stay the summer.',
  'A limited number of sites carry a discounted monthly rate, and a handful of seasonal spots run Memorial Day through Labor Day.')}

<section class="section">
  <div class="wrap">
    <div class="grid g2">
      <div>
        <span class="eyebrow">Monthly</span>
        <h2>Extended stay</h2>
        <p class="lede">A limited number of sites are available for extended stays at a discounted
          monthly rate, subject to availability and the season.</p>
        <p>Extended stays require a signed agreement, and the park rules below apply on top of the
          standard park policies. Extended stays are non-refundable.</p>
        {PROTO('<b>Monthly rate not published on the current site.</b> Add it to <code>RATES</code> in <code>build.py</code>.')}
      </div>
      <div>
        <span class="eyebrow">Memorial Day &rarr; Labor Day</span>
        <h2>Seasonal stay</h2>
        <p class="lede">Book one of a limited number of seasonal spots and get three months of prime
          outdoor season from a single basecamp.</p>
        <p>Jackson Hole, the Grand Tetons, Yellowstone, Island Park, Craters of the Moon, Sun Valley
          and the Frank Church Wilderness are all day trips from the gate.</p>
        <p class="mt2">
          <a class="btn btn-primary" href="{PHONE_HREF}">Call {PHONE}</a>
          <a class="btn btn-outline" href="{u('/contact/')}" style="margin-left:.5rem">Request a site</a>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Before you commit</span>
      <h2>Extended stay rules</h2>
      <p>These apply in addition to the standard <a href="{u('/park/policies/')}">park policies</a>.
        We put them here, before you book, rather than at the gate.</p>
    </div>
    {acc([(i, t, f'<p>{d}</p>') for i, t, d in EXT_RULES])}
  </div>
</section>

{cta_band('/media/lukjjem2/dronesunrise4.jpg',
  'Sunrise over the park and river',
  'Seasonal spots are limited', 'Call the office and we will walk you through what is still open.',
  primary=('Call the office', '/contact/'))}
'''
    return page('/stay/extended/', 'Extended &amp; Seasonal RV Stays | Idaho Falls Luxury RV Park',
                'Discounted monthly rates on a limited number of sites, plus seasonal spots from Memorial '
                'Day to Labor Day. Rules and requirements stated up front.',
                body, active='/stay', has_hero=True, og_img='/media/ujwlgfbg/dronesummer.jpg')

# ================================================================ RATES
# ⚑ Real nightly rates are published nowhere on the current site. Fill these in
#    and every price on the prototype updates. Deliberately left blank rather
#    than invented.
RATES = [
    ('Pull-Through Full Hookup', None, None, None),
    ('Back-In Full Hookup',      None, None, None),
    ('SprinterLand Casita',      None, None, None),
    ('The Ultimate Pull-In',     None, None, None),
]
FEES = [
    ('Booking transaction fee', '$10', 'Non-refundable, charged on every reservation.'),
    ('Early check-in (before 1 PM)', '$25', 'By prior approval only &mdash; a previous guest is often still in the site.'),
    ('Late check-out (after 11 AM)', '$25', 'Arrange with the office before your departure day.'),
]

def rates():
    def cell(v):
        return f'<span class="card-price">{v}</span>' if v else '<span class="card-price">$&mdash;</span>'
    rows = ''.join(
        f'<tr><th scope="row">{n}</th><td>{cell(a)}</td><td>{cell(b)}</td><td>{cell(c)}</td></tr>'
        for n, a, b, c in RATES)
    fees = ''.join(
        f'<tr><th scope="row">{n}</th><td><b>{amt}</b></td><td>{note}</td></tr>' for n, amt, note in FEES)

    body = crumbs([('Home', '/'), ('Rates &amp; Availability', None)]) + f'''
{page_hero('/media/dripxrjd/dronesunrise3.jpg',
  'Aerial view of the park at sunrise beside the Snake River',
  'Rates &amp; Availability', 'What it costs, before you click away',
  'Dates, rig length and site type — searched here, carried into the booking engine.')}

<section class="section-sm" style="background:var(--sand)">
  <div class="wrap" data-bookbar-anchor>{booking_widget(compact=3)}</div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Nightly rates</span>
      <h2>Rates by site type and season</h2>
      <p>Rates move with the season &mdash; July is not October. Live pricing for your exact dates
        comes back from the booking engine above.</p>
    </div>
    {PROTO(RATE_NOTE)}
    <div class="compare-wrap mt2">
      <table class="compare">
        <caption class="sr">Nightly rates by site type and season</caption>
        <thead><tr>
          <th scope="col">Site type</th>
          <th scope="col">Peak<br><small class="muted" style="font-weight:400">Jun&ndash;Aug</small></th>
          <th scope="col">Shoulder<br><small class="muted" style="font-weight:400">Apr&ndash;May, Sep&ndash;Oct</small></th>
          <th scope="col">Winter<br><small class="muted" style="font-weight:400">Nov&ndash;Mar</small></th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="grid g2">
      <div>
        <span class="eyebrow">Included</span>
        <h2>What every rate covers</h2>
        <ul class="features mt2">
          <li>Full hookups &mdash; 50 &amp; 30 amp, water, sewer</li>
          <li>Site-specific high-speed Wi-Fi</li>
          <li>Fire pit and custom artisan picnic table</li>
          <li>Five private bathrooms, tiled showers, heated floors</li>
          <li>Two 24-hour laundry rooms (credit-card machines)</li>
          <li>Two pickleball courts and the fenced dog park</li>
          <li>Direct access to 14 miles of Greenbelt trail</li>
          <li>Gated entry with a guest-only access code</li>
        </ul>
      </div>
      <div>
        <span class="eyebrow">Fees</span>
        <h2>The extras, stated plainly</h2>
        <div class="compare-wrap mt2">
          <table class="compare" style="min-width:0">
            <caption class="sr">Additional fees</caption>
            <tbody>{fees}</tbody>
          </table>
        </div>
        <div class="callout mt2">
          <h4>Cancellation</h4>
          <p class="mb0">Cancel more than <b>48 hours</b> before arrival for a full refund, less the $10
            transaction fee. Holiday weekends and the Penthouse run longer windows &mdash;
            <a href="{u('/park/policies/#cancellation')}">see the full policy</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

{cta_band('/media/2g2dxrsl/dronesummer-updated.jpg',
  'The park in full summer from the air',
  'Search your dates', 'Live availability across all 59 sites.')}
'''
    return page('/rates/', 'Rates &amp; Availability | Idaho Falls Luxury RV Park',
                'Nightly rates by site type and season, what every rate includes, the fee schedule and the '
                'cancellation policy. Check live availability for your dates.',
                body, active='/rates', has_hero=True, og_img='/media/cvcdxegg/iflrv-11.jpg')

# ================================================================ AMENITIES
AMENITIES = [
    ('Full hookups', '/media/kwcbbwkw/3-1-1.png', 'A travel trailer set up on a full-hookup site with its awning out', 'Water, sewer and 50/30-amp electric at every site',
     'Every one of the 59 sites has water, sewer and both 50-amp and 30-amp electric right at the pad, '
     'so nothing runs off your tanks and nothing runs out mid-stay.'),
    ('Site-specific Wi-Fi', '/media/pr4lkbqp/wifi.jpg', 'A guest working on a laptop at the park', 'Your own hotspot, not a shared park signal',
     'Each site gets its own dedicated high-speed Wi-Fi hotspot. Stream, video call, push a work project '
     'over the line &mdash; without competing with 58 other rigs for bandwidth.'),
    ('Private bathrooms', '/media/qcrgezpe/21.jpg', 'A private bathroom with a fully tiled shower', 'Five of them, full tile, heated floors',
     'Five private bathrooms, each with a fully tiled shower and heated floors. An extra sink and toilet '
     'sit in the lodge, plus a powder bath.'),
    ('The lodge &amp; fireplace', '/media/qcxgwjfm/18-1.png', 'Guests gathered around the outdoor community fireplace', 'Plus the region&#39;s largest outdoor fireplace',
     'A welcoming check-in lodge with a lounge to work or gather in, and outside it the largest outdoor '
     'community fireplace in the region &mdash; the default meeting point once it cools off.'),
    ('Snake River &amp; Greenbelt', '/media/lbemwskp/dronesnakeriverdam.jpg', 'The Snake River seen from above beside the park', 'Fourteen paved miles, straight off the property',
     'The park opens directly onto the Idaho Falls River Walk &mdash; fourteen paved miles along the Snake '
     'River for walking, running and riding. Fishing, kayaking and paddle boarding start at the same gate.'),
    ('Pickleball', '/media/kx0d405i/iflrv-08.jpg', 'The two pickleball courts at the park', 'Two regulation courts, equipment provided',
     'Two dedicated regulation courts, first-come first-served, with equipment available so you do not '
     'have to travel with paddles.'),
    ('Dog park', '/media/hpfnwnlu/9.jpg', 'The fenced dog park with dogs running off leash', 'Fenced, off-leash, no breed or size restrictions',
     'A fenced dog park for off-leash play, and the Greenbelt right outside for longer runs. Well-behaved '
     'dogs of all sizes and breeds are welcome; leashes everywhere except the dog park.'),
    ('Laundry', '/media/lbodjrcc/1-1-scaled-1.jpg', 'Washers and dryers in the on-site laundry room', 'Two rooms, open 24 hours, card-operated',
     'Two on-site laundry rooms with five washers and five dryers between them, available around the '
     'clock and operated by credit card.'),
    ('Camp store', '/media/0znjvnro/camp-store-opt.jpg', 'Shelves of supplies and souvenirs in the camp store', 'Essentials, souvenirs, ice and firewood delivered',
     'Last-minute essentials, local products and fun souvenirs. Ice and firewood are available, and we '
     'will deliver them to your site.'),
    ('Playground &amp; lawn', '/media/sallnm0f/dsc00831.jpg', 'Children playing on the playground', 'Swings, a climbing structure and room to run',
     'Swings, a small climbing structure and a large open lawn for frisbee or catch, with safe paved '
     'roads throughout the park.'),
    ('Beach cruisers', '/media/rfjan1ng/idaho-falls-luxury-rv-park-20230519-016-scaled.jpg', 'A rack of yellow beach cruiser bikes available to guests', 'Ride the Greenbelt straight from the park',
     'A rack of beach cruisers sits by the lodge for riding the Greenbelt or heading into town. '
     'Ask at the office for current availability and terms.'),
    ('Gated &amp; secure', '/media/cqhp0zsx/img_6459-1.jpg', 'The gated entrance to the park', 'Access codes issued to registered guests only',
     'The property is gated, and entry codes go to registered guests only. Quiet hours are observed.'),
]

def amenities():
    cards = ''.join(f'''
<article class="card">
  <div class="card-media">{img(s, alt, 700)}</div>
  <div class="card-body"><h3>{t}</h3><p class="small" style="color:var(--green-dk);font-weight:600;margin-bottom:.5rem">{sub}</p><p>{d}</p></div>
</article>''' for t, s, alt, sub, d in AMENITIES)

    body = crumbs([('Home', '/'), ('The Park', None), ('Amenities', None)]) + f'''
{page_hero('/media/nbkpdav5/drone2.jpg',
  'Aerial view of the park showing the lodge, courts and open lawn',
  'The Park', 'Everything that comes with the site',
  'A homebuilder&#39;s standards applied to an RV park — which mostly shows up in the things you notice on day two.')}

<section class="section">
  <div class="wrap-wide">
    <div class="grid g3">{cards}</div>
    {PROTO('<b>The bikes are not complimentary</b> &mdash; but your live FAQ says they are '
           '(&ldquo;Do you provide bikes for guests? Yes. Complimentary beach cruiser bikes&hellip;&rdquo;), '
           'and that wording is what this rebuild originally inherited. Worth correcting on the live site '
           'too. Tell me the actual terms &mdash; rental fee, deposit, guests-only &mdash; and I will state '
           'them here rather than leaving it vague.')}
  </div>
</section>

<section class="section section-deep">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Also on site</span>
      <h2>Storage, next door</h2>
      <p class="lede" style="color:rgba(255,255,255,.88)">Eagle Rock Storage sits immediately next to
        the park &mdash; fully fenced, gated, and set up for RVs, boats, trailers and vehicles. Useful
        if you are seasonal, or local, or just do not want to tow it home.</p>
    </div>
    <p class="center"><a class="btn btn-ghost-light" href="https://eaglerockstorageif.com" rel="noopener">Eagle Rock Storage</a></p>
  </div>
</section>

{cta_band('/media/lusm24um/dsc00756.jpg',
  'Guests and bikes outside an RV at the park',
  'See it for yourself', 'Take the 360&deg; virtual tour, or just book the dates.',
  primary=('Virtual tour &amp; gallery', '/park/gallery/'))}
'''
    return page('/park/amenities/', 'Amenities | Idaho Falls Luxury RV Park',
                'Full hookups, private Wi-Fi per site, five tiled bathrooms with heated floors, two '
                'pickleball courts, a fenced dog park, 24-hour laundry and Greenbelt access.',
                body, active='/park', has_hero=True, og_img='/media/nbkpdav5/drone2.jpg')

# ================================================================ PARK MAP
def park_map():
    legend = [
        ('#237d68', 'Pull-through full hookup', '32 sites &middot; 36&#39; &times; 80&#39; &middot; drive straight in'),
        ('#b08d36', 'Back-in full hookup', '26 sites &middot; 36&#39; &times; 80&#39; &middot; patio faces the lawn'),
        ('#3f7fbf', 'SprinterLand casita', '10 sites &middot; covered shelter, heaters, BBQ'),
        ('#9a4f9e', 'The Ultimate Pull-In', '1 site &middot; grassy, adjacent to open space'),
    ]
    items = ''.join(f'''
<div class="legend-item">
  <span class="legend-key" style="background:{c}" aria-hidden="true"></span>
  <div><b>{t}</b><span>{d}</span></div>
</div>''' for c, t, d in legend)

    body = crumbs([('Home', '/'), ('The Park', None), ('Park Map', None)]) + f'''
<section class="section-sm" style="padding-top:clamp(2rem,5vw,3.5rem)">
  <div class="wrap">
    <span class="eyebrow">Park map</span>
    <h1>See exactly where your site sits</h1>
    <p class="lede" style="max-width:60ch">Drag to pan, use the buttons to zoom. Sixty-plus acres of the
      old Sky-Vu Drive-In, laid out so the river side stays open.</p>
  </div>
</section>

<section style="padding-bottom:clamp(3rem,7vw,5rem)">
  <div class="wrap-wide">
    <div class="mapbox">
      <div class="mapbox-frame">
        {img('/media/gnabpzdm/park-map-6-10-24-opt.jpg',
             'Site map of Idaho Falls Luxury RV Park showing numbered sites, the lodge, pickleball courts, dog park and river frontage',
             1800, loading='eager')}
      </div>
      <div class="mapbox-tools">
        <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
        <button type="button" data-zoom="out" aria-label="Zoom out">&minus;</button>
        <button type="button" data-zoom-reset aria-label="Reset zoom" style="font-size:.95rem">&#8634;</button>
      </div>
    </div>

    <div class="legend">{items}</div>

    {PROTO('<b>This map is already in your media library</b> at '
           '<code>/media/gnabpzdm/park-map-6-10-24-opt.jpg</code> &mdash; the live site never shows it. '
           'Making individual sites clickable (tap site 14 &rarr; see its type and book it) needs one pass '
           'mapping site numbers to coordinates; the viewer and legend here are the rest of that feature.')}

    <div class="grid g2 mt3">
      <div class="callout">
        <h4>Prefer to walk it?</h4>
        <p class="mb0">The 360&deg; virtual tour lets you move through the park site by site before you
          arrive. <a href="{u('/park/gallery/#tour')}">Take the tour</a>.</p>
      </div>
      <div class="callout">
        <h4>Not sure which site to pick?</h4>
        <p class="mb0">Call the office and we will put you somewhere that fits your rig and your plans.
          <a href="{PHONE_HREF}">{PHONE}</a></p>
      </div>
    </div>
  </div>
</section>

{cta_band('/media/fgwolhjr/dji_0104.jpg',
  'The park and the Snake River from the air',
  'Found your spot?', 'Check which sites are open on your dates.')}
'''
    return page('/park/map/', 'Park Map | Idaho Falls Luxury RV Park',
                'A zoomable site map — see where the pull-through, back-in and SprinterLand casita sites '
                'sit relative to the lodge, the river and the amenities.',
                body, active='/park', og_img='/media/gnabpzdm/park-map-6-10-24-opt.jpg')

# ================================================================ GALLERY
GALLERY = [
    ('/media/cy0lrm2y/droneparknexttoriver.jpg', 'The park alongside the Snake River from the air'),
    ('/media/xn3bssaz/dronesunset.jpg', 'Sunset from above the park'),
    ('/media/0ivgvqeu/iflrv-14.jpg', 'A rainbow arcing over the RV sites'),
    ('/media/vxxccmwh/19.jpg', 'The lodge lounge with leather seating and a stone fireplace'),
    ('/media/qcxgwjfm/18-1.png', 'Guests gathered around the outdoor community fireplace'),
    ('/media/ejujv3c2/iflrv-13.jpg', 'The lodge with RVs parked outside'),
    ('/media/va4dcxhk/iflrv-02.jpg', 'The lodge exterior and its stone chimney'),
    ('/media/trtdpu3f/idaho-falls-luxury-rv-park-20230520-047-scaled.jpg', 'Inside the check-in lodge'),
    ('/media/0znjvnro/camp-store-opt.jpg', 'Inside the camp store'),
    ('/media/ed0cytiu/dsc00767.jpg', 'Bundles of firewood for sale at the park'),
    ('/media/lbodjrcc/1-1-scaled-1.jpg', 'The on-site laundry room'),
    ('/media/qcrgezpe/21.jpg', 'A private bathroom with a fully tiled shower'),
    ('/media/ldiedk2y/sprinterland-opt.jpg', 'A casita shelter beside a paved site'),
    ('/media/2eafmd2d/casita-back-in-2.jpg', 'Inside a casita, with privacy walls and Adirondack chairs'),
    ('/media/pzioqoyq/iflrv-04.jpg', 'The SprinterLand sign hanging under a casita shelter'),
    ('/media/tsckx5wy/fallcasita57charcuterie.png', 'A charcuterie board laid out at a casita'),
    ('/media/2hbfonwd/ultimate-pull-in.jpg', 'The Ultimate Pull-In shelter, picnic table and fire pit'),
    ('/media/tuqnbdu5/iflrv-05.jpg', 'A fire pit on the open lawn'),
    ('/media/l2efwnz2/img_0329-scaled-1.jpeg', 'One of the custom artisan picnic tables'),
    ('/media/kx0d405i/iflrv-08.jpg', 'The pickleball courts'),
    ('/media/hpfnwnlu/9.jpg', 'The fenced dog park'),
    ('/media/sallnm0f/dsc00831.jpg', 'Children playing on the playground'),
    ('/media/rfjan1ng/idaho-falls-luxury-rv-park-20230519-016-scaled.jpg', 'Beach cruiser bikes available to guests'),
    ('/media/ogwabbyu/img_0357-scaled-1.jpg', 'The gate onto the Idaho Falls Greenbelt trail'),
    ('/media/lbemwskp/dronesnakeriverdam.jpg', 'The Snake River and dam from the air'),
    ('/media/pgnf21pp/mws-still-01-1.png', 'The waterfalls on the Snake River in downtown Idaho Falls'),
    ('/media/cgdhnbvl/dronefall.png', 'The park from above in autumn'),
    ('/media/12cbkpnp/sunriselandscape.jpg', 'Sunrise over the park and river'),
    ('/media/3ybavy0p/iflrv-15.jpg', 'Sunset colour over the park'),
    ('/media/cqhp0zsx/img_6459-1.jpg', 'The gated entrance to the park'),
]

def gallery():
    figs = ''.join(f'<figure>{img(s, a, 700)}</figure>' for s, a in GALLERY)
    body = crumbs([('Home', '/'), ('The Park', None), ('Gallery &amp; Tour', None)]) + f'''
<section class="section-sm" style="padding-top:clamp(2rem,5vw,3.5rem)">
  <div class="wrap">
    <span class="eyebrow">Gallery &amp; virtual tour</span>
    <h1>Walk the park before you book it</h1>
    <p class="lede" style="max-width:62ch">The 360&deg; tour puts you on the roads; the photographs
      show you what the light does here.</p>
  </div>
</section>

<section class="section-sm" id="tour">
  <div class="wrap-wide">
    <h2>360&deg; virtual tour</h2>
    <p class="lede" style="max-width:60ch;margin-bottom:1.5rem">Move through the park site by site,
      at your own pace, before you ever pull in the gate.</p>
    <div style="position:relative;border-radius:var(--r);overflow:hidden;border:1px solid var(--line);background:var(--sand-2)">
      <div style="position:relative;padding-top:62%">
        <iframe src="https://360.campgroundviews.com/h/IdahoFallsLuxuryRVResort"
                title="360-degree virtual tour of Idaho Falls Luxury RV Park"
                loading="lazy" allow="fullscreen" allowfullscreen
                style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
      </div>
    </div>
    <p class="small muted mt1">Tour not loading? <a href="https://360.campgroundviews.com/h/IdahoFallsLuxuryRVResort" rel="noopener">Open it in a new tab</a>,
      or <a href="{u('/park/map/')}">view the park map</a> instead.</p>
    {PROTO('The live site ships this tour as a fixed <code>height="800"</code> iframe with no fallback, '
           'which is unusable on a phone. Here it holds a 16:10 aspect ratio at every width and degrades '
           'to two working links.')}
  </div>
</section>

<section class="section">
  <div class="wrap-wide">
    <h2>Photo gallery</h2>
    <p class="lede" style="max-width:60ch;margin-bottom:2rem">The sites, the lodge, the casitas
      and the river, in daylight and at the hour that sells the place.</p>
    <div class="gallery">{figs}</div>
  </div>
</section>

{cta_band('/media/ujwlgfbg/dronesummer.jpg',
  'The park from the air in summer',
  'Seen enough?', 'Check availability for your dates.')}
'''
    return page('/park/gallery/', 'Gallery &amp; 360&deg; Virtual Tour | Idaho Falls Luxury RV Park',
                'Photos of the sites, lodge, casitas and river frontage at Idaho Falls Luxury RV Park, plus a '
                '360-degree virtual tour you can walk through before you book.',
                body, active='/park', og_img='/media/xa1hraq3/iflrv-01.jpg')

# ================================================================ POLICIES
P_BOOK = [
    ('cancellation', 'Cancellation &amp; refunds',
     '<p>Cancel <b>more than 48 hours</b> before your arrival date for a full refund, less the '
     'non-refundable $10 transaction fee. Inside 48 hours there is no refund.</p>'
     '<ul><li><b>Memorial Day &amp; Labor Day:</b> cancel 7 days prior for a full refund, less the $10 fee.</li>'
     '<li><b>4th of July:</b> cancel 30 days prior for a full refund, less the $10 fee.</li>'
     '<li><b>Penthouse Apartment:</b> cancel 7 days prior for a full refund, less the $10 fee.</li>'
     '<li><b>Extended stays:</b> no refunds.</li></ul>'),
    ('pets', 'Pets',
     '<p>Well-behaved dogs of all sizes and breeds are welcome, and there is a fenced off-leash dog park. '
     'Because of our insurance requirements, a few rules are firm:</p>'
     '<ul><li>No exotic or oversized pets.</li>'
     '<li>Pets may never be left unattended &mdash; weather and power outages make that genuinely dangerous.</li>'
     '<li>All pets must be up to date on vaccinations.</li>'
     '<li>Leashed at all times outside the dog park.</li>'
     '<li>Not permitted in the lodge, laundromat or bathrooms.</li>'
     '<li>Always clean up. Failure to clean up, or excessive barking, will result in being asked to '
     'leave without a refund.</li></ul>'),
    ('rvs', 'RVs, rigs &amp; tents',
     '<p>This is an RV-only park &mdash; we do not offer tent camping. Sites are 36&#39; &times; 80&#39; '
     'and handle oversized Class A motorhomes, fifth wheels and travel trailers.</p>'
     '<p>For <b>extended stays</b>, all RVs must be 10 years old or newer and in good external condition '
     'regardless of age.</p>'),
    ('prohibited', 'Fireworks, firearms &amp; drones',
     '<p>Fireworks and firearms are strictly prohibited. Fireworks includes sparklers, smoke bombs, '
     'aerials and firecrackers. Firearms includes air soft, BB and pellet guns. If these are seen outside '
     'your RV you will be asked to leave immediately without a refund.</p>'
     '<p>Drones are not permitted in the park, and may not be flown over people or RVs.</p>'),
    ('visitors', 'Visitors',
     '<p>Only registered guests may enter the park. Visitors must stop at the office for a parking pass '
     'and may not bring pets. Day visitors depart by 10:00 PM; overnight visitors by 11:00 AM. We reserve '
     'the right to limit the number of visitors to a site, and the registered guest is responsible for '
     'their visitors following park rules. Please check with the office before inviting anyone.</p>'),
]
P_ARRIVE = [
    ('checkin', 'Check-in &amp; check-out',
     '<p>Check-in is <b>1:00 PM</b> mountain time; check-out is <b>11:00 AM</b>.</p>'
     '<p>Arrivals before 1:00 PM are subject to a $25 early check-in fee, and early check-in is not '
     'permitted without prior approval &mdash; often a previous guest is still in the site. We do not have '
     'a waiting area, so please make arrangements if you will be in the area early. Departures after '
     '11:00 AM are charged a $25 late check-out fee.</p>'
     '<p>Late check-ins are fine at any hour, but contact the park for instructions &mdash; you will need '
     'a code for the secured entrance gate.</p>'),
    ('sites', 'Your site assignment',
     '<p>You are assigned a specific site. If you would like to move, check with staff first and we will '
     'do our best &mdash; reservations and maintenance sometimes make it impossible. Please ask before '
     'moving.</p>'),
    ('parking', 'Parking &amp; vehicles',
     '<p>A nightly registration covers one RV and one vehicle per site. Park only on your reserved site; '
     'using more than one site brings additional charges, and parking on the grass is prohibited and may '
     'incur damage fines. Extra vehicles park by the lodge or the laundromat &mdash; never on the streets.</p>'
     '<p>Additional trailers and boats can be accommodated if they fit on your site; an additional charge '
     'may apply. ATVs, dirt bikes, motorcycles and golf carts may be used only to get to and from your site.</p>'),
    ('speed', 'Speed limit',
     '<p>The park speed limit is <b>5 mph</b>. Exceeding it brings a warning; repeated warnings mean we '
     'will ask you to leave. Safety is the priority &mdash; there are children and pets on these roads.</p>'),
    ('power', 'Electrical use',
     '<p>You are responsible for knowing how many amps you are drawing. Going over the 50 amps provided '
     'will trip your breaker. Tell the office about any electrical issue so maintenance can handle it &mdash; '
     'guests are not permitted to diagnose our pedestals, per insurance and safety requirements.</p>'),
]
P_STAY = [
    ('fires', 'Campfires &amp; grills',
     '<p>Campfires belong in the designated fire rings or the big fireplace outside the lodge. Firewood '
     'bundles are for sale and we will deliver them. SprinterLand casita sites include a charcoal '
     'barbecue &mdash; charcoal only, available at the lodge store.</p>'
     '<p>Please do not put BBQ grills on the wooden picnic tables; use the stone fire pit.</p>'),
    ('quiet', 'Quiet hours',
     '<p>Quiet time is <b>10:00 PM to 7:00 AM</b>.</p>'),
    ('kids', 'Children',
     '<p>Children must be supervised by an adult. Bicycles, scooters and skateboards are not allowed on '
     'the main entrance road without a parent, for their safety and our arriving guests&#39;. The great '
     'lawn and pickleball courts close at dark, and children may not use the restrooms unaccompanied.</p>'),
    ('facilities', 'Restrooms &amp; laundry',
     '<p>Restrooms are open 24/7 apart from a short daily cleaning closure; children need adult supervision '
     'in the bathrooms and showers. Each site has a dumping station for gray and black water &mdash; do not '
     'empty cassette-style holding tanks in the bathrooms.</p>'
     '<p>Laundry is open 24 hours: 2 washers and dryers in the main lodge, 3 in the laundromat building, '
     'card reader payment with instructions posted. Please do not leave laundry unattended; we are not '
     'responsible for accidents or theft.</p>'),
    ('pickle', 'Pickleball courts',
     '<p>Open from 8:00 AM until dusk. Please limit play to an hour if others are waiting. Paddles and '
     'balls are available to rent at the lodge.</p>'),
    ('tidy', 'Keeping the park looking right',
     '<p>No storage under or around your RV or picnic table. Rugs larger than 3&#39; &times; 2&#39; are not '
     'allowed on the grass &mdash; they kill it &mdash; but your concrete patio is fair game. Clotheslines '
     'are not permitted. Please do not use paint or other staining materials outdoors.</p>'
     '<p>Washing an RV or vehicle is permitted with one bucket and a sponge; hose washing is not.</p>'
     '<p>Please walk the main roads, sidewalks and designated paths rather than cutting between sites.</p>'),
    ('trash', 'Trash &amp; recycling',
     '<p>Tie bags closed and put them fully inside the dumpster. No motor oil, cooking oil, wires, '
     'furniture, mattresses or hazardous waste &mdash; disposal fees will be charged. We do not have '
     'recycling on site yet. We are working on it.</p>'),
    ('smoking', 'Smoking, vaping &amp; drugs',
     '<p>The lodge, laundry facilities and all bathrooms are non-smoking. Smoking tobacco and vaping are '
     'limited to your own site &mdash; please be courteous with smoke and do not litter.</p>'
     '<p>All Idaho state drug laws apply, and no public intoxication is tolerated.</p>'),
    ('repairs', 'Repairs',
     '<p>RV and vehicle repairs are not permitted in the park. We are glad to recommend a local mobile RV '
     'repair service that will come to your site.</p>'),
    ('damage', 'Damage &amp; vandalism',
     '<p>Damage, vandalism or excessive cleanup at your site may result in additional charges based on the '
     'extent of the damage.</p>'),
    ('weather', 'Severe weather',
     '<p>Seek shelter in the bathrooms or the laundry room &mdash; shelter areas are posted. Bring your '
     'pets with you; please do not leave them in the RV during a severe weather warning.</p>'),
    ('safety', 'Safety &amp; emergencies',
     '<p>Extended stay guests are required to complete an emergency contact form. That information stays '
     'private and is used only if we need to reach someone in an emergency or if it is sought by law '
     'enforcement. We never give personal information to anyone else.</p>'
     '<p>If you see anything concerning, tell the office. (No soliciting is allowed.) If you need to call '
     '911 and time allows, call the office too, so maintenance can escort emergency personnel to your site.</p>'),
]

def policies():
    body = crumbs([('Home', '/'), ('The Park', None), ('Policies', None)]) + f'''
<section class="section-sm" style="padding-top:clamp(2rem,5vw,3.5rem)">
  <div class="wrap">
    <span class="eyebrow">Park policies</span>
    <h1>The rules, in the order you need them</h1>
    <p class="lede" style="max-width:64ch">Grouped by when they actually matter &mdash; what could change
      your mind before booking, what to know on arrival day, and what keeps the place pleasant once you
      are settled.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="acc-group">
      {acc(P_BOOK, group='Before you book &mdash; the deal-breakers')}
    </div>
    <div class="acc-group">
      {acc(P_ARRIVE, group='Arriving &amp; leaving')}
    </div>
    <div class="acc-group">
      {acc(P_STAY, group='While you&#39;re here')}
    </div>

    {PROTO('<b>Two things to reconcile before this goes live.</b> The current site states a <b>5 mph</b> '
           'park speed limit on Park Policies and <b>7.5 mph</b> in the Extended Stay rules &mdash; this page '
           'uses 5 mph, but pick one. And the <b>Penthouse Apartment</b> appears in your cancellation policy '
           'with no page anywhere selling it; it needs one.')}

    <div class="callout mt3">
      <h4>Staying a month or longer?</h4>
      <p class="mb0">Extended stays carry additional rules on top of everything above &mdash;
        <a href="{u('/stay/extended/')}">read them here</a> before you book.</p>
    </div>
  </div>
</section>

{cta_band('/media/dokcru1q/tempimagesjkrtz-1.jpg',
  'The park entrance sign lit at dusk',
  'Questions we did not answer?', 'The office picks up.',
  primary=('Contact us', '/contact/'))}
'''
    return page('/park/policies/', 'Park Policies | Idaho Falls Luxury RV Park',
                'Cancellation windows, pet rules, check-in and check-out, parking and quiet hours — grouped '
                'by when they matter, from before you book to while you are here.',
                body, active='/park', og_img='/media/30ppmizv/idaho-falls-luxury-rv-park-20230519-008-1.jpg')

# ================================================================ EXPLORE
def explore():
    rows = ''.join(f'<tr><th scope="row">{n}</th><td>{m}</td><td>{t}</td></tr>' for n, m, t in DRIVE)
    trips = [
        ('Yellowstone National Park', '/media/fgwolhjr/dji_0104.jpg',
         "The park from the air, two hours from Yellowstone's west entrance",
         'About 2 hours north on Highway 20 to the West Entrance. Idaho Falls is the closest major city '
         'to that gate, which is why so many people base here instead of fighting for a pad in a gateway town.'),
        ('Grand Teton &amp; Jackson Hole', '/media/ugoembul/grandtargheeskiresort-1024x699.jpg',
         'The Teton range rising behind a ski resort',
         '90 minutes to two hours east, depending on your route and where in the park you are headed. '
         'Jackson Hole sits just beyond it, under 100 miles out.'),
        ('Craters of the Moon', '/media/a5jfwhee/cratersofthemoon-1024x684.jpg',
         'The volcanic landscape of Craters of the Moon National Monument',
         'A lava field the Apollo astronauts trained on, roughly 90 minutes west. Strange, stark, and '
         'completely unlike everything else within a day of here.'),
        ('Island Park &amp; Sun Valley', '/media/12cbkpnp/sunriselandscape.jpg',
         'Sunrise over eastern Idaho from above the park',
         'Island Park sits between here and Yellowstone&#39;s west side; Sun Valley is a longer but very '
         'worthwhile run west. Both are comfortable day trips from a seasonal site.'),
    ]
    cards = ''.join(f'''
<article class="card">
  <div class="card-media">{img(s, a, 700)}</div>
  <div class="card-body"><h3>{t}</h3><p>{d}</p></div>
</article>''' for t, s, a, d in trips)

    body = crumbs([('Home', '/'), ('Explore', None)]) + f'''
{page_hero('/media/f3pk4rhy/dronesunrise.jpg',
  'Sunrise over the Snake River valley with mountains beyond',
  'Explore', 'Gateway to adventure, with full hookups',
  'Idaho Falls is the practical basecamp for everything in this corner of the country — and a good few days on its own.')}

<section class="section" id="yellowstone">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Drive times</span>
        <h2>From our gate to the gates</h2>
        <p class="lede">Every number below is measured from the park, not from &ldquo;the Idaho Falls
          area.&rdquo; Plan your days off these.</p>
        <div class="compare-wrap mt2">
          <table class="compare" style="min-width:0">
            <caption class="sr">Driving distances and times from Idaho Falls Luxury RV Park</caption>
            <thead><tr><th scope="col">Destination</th><th scope="col">Distance</th><th scope="col">Drive</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </div>
      <div class="split-media">{img('/media/cmrdvlne/dronesunrise.jpg',
        'The park and river from above at first light', 1000)}</div>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap-wide">
    <div class="section-head center">
      <span class="eyebrow">Day trips</span>
      <h2>What is within a tank of fuel</h2>
    </div>
    <div class="grid g4">{cards}</div>
    {PROTO('<b>These four cards reuse park photography.</b> Your media library has no Yellowstone or '
           'Teton imagery in it, and nothing here pretends otherwise &mdash; licensed shots of the west '
           'entrance, the Tetons and Jackson would make this the strongest page on the site, because it '
           'is the search everyone actually runs.')}
  </div>
</section>

<section class="section" id="local">
  <div class="wrap">
    <div class="split reverse">
      <div>
        <span class="eyebrow">In town</span>
        <h2>Two miles to downtown, zero to the trail</h2>
        <p class="lede">The Greenbelt starts at our fence &mdash; fourteen paved miles along the Snake
          River, which you can walk, run or ride on one of our beach cruisers.</p>
        <p>Follow it and you reach the waterfalls the city is named for, the River Walk, and a downtown
          with museums, a zoo, a farmers market and enough restaurants to fill a week. The river itself
          is open for fishing, kayaking and paddle boarding.</p>
        <ul class="features mt2">
          <li>Idaho Falls River Walk and the falls themselves</li>
          <li>Museum of Idaho and the Idaho Falls Zoo</li>
          <li>Farmers market and downtown festivals in season</li>
          <li>Melaleuca Field &mdash; minor league baseball on a summer night</li>
        </ul>
      </div>
      <div class="split-media">{img('/media/pgnf21pp/mws-still-01-1.png',
        'The waterfalls on the Snake River in downtown Idaho Falls', 1000)}</div>
    </div>
  </div>
</section>

<section class="section section-sand" id="dining">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Where to eat</span>
      <h2>Dinner is five minutes away</h2>
      <p class="lede">Downtown Idaho Falls is two miles out, and DoorDash and the other delivery services
        come straight to the park if you would rather not move.</p>
    </div>
    {PROTO('<b>This section needs your actual recommendations.</b> The live site has a '
           '&ldquo;Bars &amp; Restaurants&rdquo; item in the navigation pointing at a page with no content '
           'on it &mdash; and a short list of places you genuinely send guests to is one of the most-read '
           'things an RV park can publish.')}
  </div>
</section>

<section class="section" id="july4">
  <div class="wrap">
    <div class="split">
      <div class="split-media">{img('/media/zrmhig1f/fireworks-in-sky-2022-10-31-23-48-55-utc.jpg',
        'Fireworks bursting over a night sky', 1000)}</div>
      <div>
        <span class="eyebrow">The big week</span>
        <h2>4th of July in Idaho Falls</h2>
        <p class="lede">Idaho Falls puts its fireworks up over the Snake River, and the park fills
          months in advance for the holiday week.</p>
        <p>Book early &mdash; and note that the holiday carries its own cancellation window: cancel 30
          days prior for a refund, less the $10 transaction fee.</p>
        {PROTO('Add this year&#39;s event details, times and road closures '
               'before publishing. The live site&#39;s 4th of July page is currently empty.')}
        <p class="mt2"><a class="btn btn-primary" href="{u('/rates/')}">Check July availability</a></p>
      </div>
    </div>
  </div>
</section>

{cta_band('/media/xn3bssaz/dronesunset.jpg',
  'Sunset over the park',
  'Make this your basecamp', 'One site, a dozen day trips, and a hot shower waiting at the end of each one.')}
'''
    return page('/explore/', 'Things to Do &amp; Drive Times | Idaho Falls Luxury RV Park',
                "Drive times from the park gate to Yellowstone's west entrance, Grand Teton, Jackson Hole "
                "and Craters of the Moon, plus the Greenbelt and downtown Idaho Falls.",
                body, active='/explore', has_hero=True, og_img='/media/f3pk4rhy/dronesunrise.jpg')

# ================================================================ FAQ
FAQ = [
 ('Location &amp; trip planning', [
  ('q1', 'What are the best things to do in Idaho Falls?',
   'Idaho Falls is known as the Gateway to Adventure and offers year-round activities. Visitors enjoy a '
   'vibrant downtown, museums, a zoo, outdoor festivals, and the scenic Snake River Greenbelt. The area is '
   'also a popular base for day trips including hiking, fishing, skiing, boating and visiting nearby '
   'national parks.'),
  ('q2', 'Is the park located on the Snake River?',
   'Yes. The park is located directly on the Snake River, with direct access to the Greenbelt Trail &mdash; '
   'a paved 10-mile walking and biking path &mdash; and is just 2 miles from downtown Idaho Falls.'),
  ('q3', 'How close is the park to Interstate 15?',
   'Within 2 miles. Guests come in from Exit 116, which makes it a convenient stop for travelers heading '
   'north or south.'),
  ('q4', 'How far is Idaho Falls from Yellowstone National Park?',
   "Approximately 110 miles from Yellowstone's West Entrance, about a 2-hour drive north on Highway 20. "
   "Idaho Falls is the closest major city to that entrance."),
  ('q5', 'Is Idaho Falls a good base camp for visiting Yellowstone?',
   'Yes. It offers full hookups, dining, shopping and easy highway access, while avoiding the congestion '
   'found in the smaller gateway towns.'),
  ('q6', 'How far is Grand Teton National Park?',
   'Roughly 70&ndash;100 miles, or about 1.5 to 2 hours depending on your route and destination within the park.'),
  ('q7', 'How far is Jackson Hole?',
   'Under 100 miles, typically about a 2-hour drive depending on traffic and route.'),
  ('q8', 'How far is Salt Lake City?',
   'Approximately 215 miles south, about a 3.5- to 4-hour drive via Interstate 15.'),
  ('q9', 'Are there waterfalls in Idaho Falls?',
   'Yes. The city is named for the waterfalls along the Snake River downtown, which are a central feature '
   'of the River Walk and Greenbelt.'),
 ]),
 ('RV sites &amp; hookups', [
  ('q10', 'What does full hook-up mean?',
   'A full hook-up site includes water, electric and sewer connections at your site, so you can use all '
   'your RV systems without relying on onboard tanks.'),
  ('q11', 'Do your RV sites have full hookups?',
   'Yes. All sites include full hookups with 30-amp and 50-amp electric service, water, sewer and '
   'site-specific high-speed Wi-Fi. Each site also includes a custom artisan picnic table.'),
  ('q12', 'What size RVs can you accommodate?',
   'Sites are 36&#39; &times; 80&#39; and are designed for large Class A motorhomes, fifth wheels and travel '
   'trailers, including oversized rigs. Roads and pads are paved and level for easy setup.'),
  ('q13', 'Do you have pull-through sites?',
   'Yes &mdash; 32 of our 59 sites are pull-through, ideal for larger rigs and for easy arrival and departure.'),
  ('q14', 'Are the sites paved and level?',
   'Yes. All roads and RV pads throughout the park are fully paved and level.'),
  ('q15', 'Do you offer premium sites?',
   'Yes. Our SprinterLand casita sites are premium sites that include a second patio, a covered shelter, '
   'outdoor heaters and a charcoal grill.'),
  ('q16', 'Will satellite TV or Starlink work?',
   'Yes. All sites have clear sky access with no major obstructions, making satellite TV and Starlink easy to use.'),
 ]),
 ('Park amenities', [
  ('q17', 'Do you have private bathrooms and showers?',
   'Yes. Five private bathrooms, each with a tiled shower and heated floors for year-round comfort.'),
  ('q18', 'Do you have laundry facilities?',
   'Yes. Two on-site laundry rooms available 24 hours a day. Machines are operated by credit card.'),
  ('q19', 'Is there Wi-Fi?',
   'Yes. All sites include site-specific high-speed Wi-Fi suitable for streaming and remote work &mdash; '
   'your own hotspot rather than a shared park signal.'),
  ('q20', 'Do you have a camp store?',
   'Yes. It stocks essential supplies and unique local products. Ice and firewood are available, and we '
   'deliver them to your site.'),
  ('q21', 'Can DoorDash deliver to the park?',
   'Yes. DoorDash and other food delivery services deliver directly to the park.'),
  ('q22', 'Do you have pickleball courts?',
   'Yes. Two regulation courts available to guests first-come, first-served. Paddles and balls can be '
   'rented at the lodge.'),
  ('q23', 'Do you provide bikes?',
   'Yes. Beach cruiser bikes are available for the Greenbelt or for riding into the city. '
   'Ask at the office for current availability and terms.'),
  ('q24', 'Do you offer RV or boat storage?',
   'Yes. Eagle Rock Storage offers secure RV, boat, vehicle and general storage right next door to the '
   'park &mdash; fully fenced with gated access. Learn more at '
   '<a href="https://eaglerockstorageif.com" rel="noopener">eaglerockstorageif.com</a>.'),
 ]),
 ('Pets &amp; families', [
  ('q25', 'Is the park pet-friendly?',
   'Yes. Well-behaved dogs are welcome, and there is a fenced dog park for off-leash play.'),
  ('q26', 'Are there breed or size restrictions for dogs?',
   'No. Well-behaved dogs of all sizes and breeds are welcome. Pets must be leashed outside the dog park, '
   'and may not be left unattended. See the full '
   '<a href="' + '{PETS}' + '">pet policy</a> for the insurance requirements.'),
  ('q27', 'Is the park family-friendly?',
   'Yes. There is a playground, open lawn space, bikes and safe paved roads throughout.'),
  ('q28', 'Do you have a playground?',
   'Yes &mdash; swings, a small climbing structure, and a large lawn for frisbee or catch.'),
 ]),
 ('Stays &amp; policies', [
  ('q29', 'Are you open year-round?',
   'Yes, including through the winter months.'),
  ('q30', 'Do you allow extended or long-term stays?',
   'Yes, subject to availability and seasonal guidelines. A limited number of sites carry a discounted '
   'monthly rate. See <a href="' + '{EXT}' + '">extended &amp; seasonal stays</a>.'),
  ('q31', 'Do you offer winter hookups?',
   'Yes. The park is designed for year-round operation and utilities are maintained for winter conditions.'),
  ('q32', 'Can I have a campfire at my site?',
   'Yes. Each site includes a fire pit, and campfires are allowed when local fire restrictions permit.'),
  ('q33', 'Is the park gated and secure?',
   'Yes. The property is gated and access codes are provided to registered guests only.'),
  ('q34', 'Is the park quiet at night?',
   'Yes. Quiet hours run 10:00 PM to 7:00 AM.'),
  ('q35', 'Do you allow tent camping?',
   'No. This is an RV-only park and we do not offer tent camping.'),
 ]),
 ('About the park', [
  ('q36', 'How long have you been open?',
   'The park officially opened in May 2023, after construction began in 2021 on the site of the old '
   'Sky-Vu Drive-In Theater.'),
  ('q37', 'Have you won any awards?',
   "Yes &mdash; the park has been recognized as Idaho's Best RV Park (statewide) and has received RV Life's "
   "Best of the Best awards."),
 ]),
]

def faq():
    import json
    groups, qa = '', []
    for title, items in FAQ:
        fixed = []
        for i, q, a in items:
            a = a.replace('{PETS}', u('/park/policies/#pets')).replace('{EXT}', u('/stay/extended/'))
            fixed.append((i, q, f'<p>{a}</p>'))
            # strip tags AND decode entities — raw &mdash;/&#39; in JSON-LD is
            # what search engines would read back out verbatim
            clean = lambda t: html.unescape(re.sub('<[^>]+>', '', t)).strip()
            qa.append({'@type': 'Question', 'name': clean(q),
                       'acceptedAnswer': {'@type': 'Answer', 'text': clean(a)}})
        groups += f'<div class="acc-group">{acc(fixed, group=title)}</div>'

    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': qa})

    body = crumbs([('Home', '/'), ('FAQ', None)]) + f'''
<section class="section-sm" style="padding-top:clamp(2rem,5vw,3.5rem)">
  <div class="wrap">
    <span class="eyebrow">Frequently asked questions</span>
    <h1>Everything people call to ask</h1>
    <p class="lede" style="max-width:62ch">If it is not here, the office picks up:
      <a href="{PHONE_HREF}">{PHONE}</a>.</p>
  </div>
</section>
<section class="section" style="padding-top:0"><div class="wrap">{groups}</div></section>
{cta_band('/media/uybnzgyf/dji_0055.jpg',
  'RVs parked on paved sites beside open lawn',
  'Answered?', 'Check availability for your dates.')}
'''
    return page('/faq/', 'Frequently Asked Questions | Idaho Falls Luxury RV Park',
                'Drive times to Yellowstone and the Tetons, hookups and rig sizes, Wi-Fi and Starlink, pets, '
                'laundry, extended stays and more — answered.',
                body, active='/faq', jsonld=ld,
                og_img='/media/12cbkpnp/sunriselandscape.jpg')

# ================================================================ ABOUT
def about():
    body = crumbs([('Home', '/'), ('About', None)]) + f'''
{page_hero('/media/12cbkpnp/sunriselandscape.jpg',
  'The park and the Snake River from the air at sunrise',
  'Our story', 'It started as a drive-in theater',
  'Two families, one closed movie screen beside the Snake River, and a stubborn idea about what an RV park could be.')}

<section class="section">
  <div class="wrap">
    <div class="prose">
      <p class="lede">Idaho Falls Luxury RV Park begins with family. Zach and Kristina Teichert,
        longtime East Idaho residents, have always cherished having family around. Randy and Julie
        Sebastian share a passion for RV travel and made the trip out regularly to see Zach, Kristina
        and their grandson.</p>
      <p>Those trips kept turning up the same problem: the RV parks along the way were a disappointment.
        On one of them &mdash; heading through Yellowstone &mdash; the idea of building a genuinely
        remarkable RV park took hold.</p>
      <p>Randy had spent more than three decades as the owner of Renaissance Homes, building high-end
        houses in Portland. The proposition was simple and slightly unreasonable: take the standards
        that go into a custom home and apply them, without compromise, to an RV park.</p>

      <h2>The Sky-Vu Drive-In</h2>
      <p>The search for a site ended somewhere unexpected. The Sky-Vu Drive-In Theater opened in Idaho
        Falls in 1950 and spent decades as a local institution, bringing families together beside the
        Snake River. By the time they found it, it had been closed for ten years and stripped of its
        equipment.</p>
      <p>They saw the canvas rather than the ruin. Building here was never only about a high-quality
        RV destination &mdash; it was about honoring what the old drive-in had done for the better part
        of a century.</p>
      <p>Construction began in 2021. The park opened in May 2023.</p>

      <h2>What came out of it</h2>
      <p>Fifty-nine sites, every one paved and level at 36 by 80 feet &mdash; the largest RV spaces in
        East Idaho. Direct access to the Snake River and the Greenbelt. Two pickleball courts, a dog
        park, a playground, site-specific Wi-Fi, and the region&#39;s largest outdoor community
        fireplace.</p>
      <p>Since opening, the park has been named Idaho&#39;s Best RV Park statewide and has taken RV
        Life&#39;s Best of the Best awards.</p>
      <p>We would like you to be part of the story &mdash; one about family, legacy, and the pursuit of
        somewhere that luxury and camping genuinely overlap.</p>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b>1950</b><span>Sky-Vu opens</span></div>
      <div class="stat"><b>2021</b><span>Ground breaks</span></div>
      <div class="stat"><b>2023</b><span>Park opens</span></div>
      <div class="stat"><b>59</b><span>Sites</span></div>
    </div>
  </div>
</section>

{cta_band('/media/ejujv3c2/iflrv-13.jpg', 'The lodge with RVs parked outside',
  'Come be part of it', 'Check availability for your dates.')}
'''
    return page('/about/', 'Our Story | Idaho Falls Luxury RV Park',
                'Two families, a Portland homebuilder and the closed Sky-Vu Drive-In Theater — how the park '
                "came to be, and what opened on the old theater site in May 2023.",
                body, active='/about', has_hero=True, og_img='/media/12cbkpnp/sunriselandscape.jpg')

# ================================================================ CONTACT
def contact():
    body = crumbs([('Home', '/'), ('Contact', None)]) + f'''
<section class="section-sm" style="padding-top:clamp(2rem,5vw,3.5rem)">
  <div class="wrap">
    <span class="eyebrow">Contact</span>
    <h1>Talk to the office</h1>
    <p class="lede" style="max-width:60ch">For anything the booking engine cannot do &mdash; seasonal
      sites, group bookings, a rig you are not sure will fit.</p>
  </div>
</section>

<section class="section" style="padding-top:1rem">
  <div class="wrap">
    <div class="grid g2">
      <div>
        <h2>Reach us</h2>
        <div class="compare-wrap mt2">
          <table class="compare" style="min-width:0">
            <caption class="sr">Contact details and hours</caption>
            <tbody>
              <tr><th scope="row">Phone</th><td><a href="{PHONE_HREF}"><b>{PHONE}</b></a></td></tr>
              <tr><th scope="row">Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
              <tr><th scope="row">Address</th><td>3000 S Yellowstone Hwy<br>Idaho Falls, ID 83402</td></tr>
              <tr><th scope="row">Office hours</th><td>Daily 10:00 AM &ndash; 6:00 PM</td></tr>
              <tr><th scope="row">Check-in</th><td>1:00 PM</td></tr>
              <tr><th scope="row">Check-out</th><td>11:00 AM</td></tr>
            </tbody>
          </table>
        </div>
        {PROTO('<b>Winter hours.</b> The live site&#39;s footer says &ldquo;TBD (check Google for winter '
               'hours)&rdquo; while its About page lists 10am&ndash;6pm daily. Sending guests to Google to '
               'find your own hours costs you calls &mdash; publish the winter hours here and the footer '
               'picks them up everywhere.')}
        <div class="callout mt2">
          <h4>Arriving after hours?</h4>
          <p class="mb0">Late check-ins are welcome at any hour, but call ahead &mdash; you will need a
            code for the secured entrance gate.</p>
        </div>
      </div>

      <div>
        <h2>Send a message</h2>
        <form class="booking" style="box-shadow:none;border:1px solid var(--line);padding:1.5rem"
              data-mailto-form data-to="{EMAIL}">
          <div style="display:grid;gap:1rem">
            <div class="booking-field"><label for="cname">Name</label>
              <input type="text" id="cname" name="name" required autocomplete="name"></div>
            <div class="booking-field"><label for="cemail">Email</label>
              <input type="email" id="cemail" name="email" required autocomplete="email"></div>
            <div class="booking-field"><label for="cphone">Phone</label>
              <input type="tel" id="cphone" name="phone" autocomplete="tel"></div>
            <div class="booking-field"><label for="crig">Rig type &amp; length</label>
              <input type="text" id="crig" name="rig" placeholder="e.g. 42&#39; Class A + tow"></div>
            <div class="booking-field"><label for="cwhat">What can we help with?</label>
              <select id="cwhat" name="topic">
                <option>A reservation question</option>
                <option>Extended or seasonal stay</option>
                <option>Group booking</option>
                <option>Will my rig fit?</option>
                <option>Something else</option>
              </select></div>
            <div class="booking-field"><label for="cmsg">Message</label>
              <textarea id="cmsg" name="message" rows="5" required
                style="font-family:var(--b);font-size:.97rem;padding:.72em .85em;border:1.5px solid var(--line);border-radius:var(--r-sm)"></textarea></div>
            <button class="btn btn-primary btn-block" type="submit">Send message</button>
          </div>
        </form>
        {PROTO('This form posts to <code>mailto:</code> so the prototype has no backend. On the real site, '
               'point it at your form handler or CRM. <b>The current site has no contact form at all</b> '
               '&mdash; only a phone number and an email address, which loses every visitor who is not '
               'ready to call.')}
      </div>
    </div>
  </div>
</section>

<section class="section-sm" style="padding-bottom:clamp(3rem,7vw,5rem)">
  <div class="wrap-wide">
    <h2 class="sr">Map and directions</h2>
    <div style="position:relative;padding-top:42%;border-radius:var(--r);overflow:hidden;border:1px solid var(--line)">
      <iframe title="Map showing Idaho Falls Luxury RV Park at 3000 S Yellowstone Hwy, Idaho Falls, Idaho"
        src="https://www.google.com/maps?q=Idaho+Falls+Luxury+RV+Park,+3000+S+Yellowstone+Hwy,+Idaho+Falls,+ID+83402&output=embed"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
    </div>
    <p class="small muted mt1">Coming off I-15? Take <b>Exit 116</b> &mdash; the park is within 2 miles.
      <a href="https://maps.google.com/?q=Idaho+Falls+Luxury+RV+Park,+3000+S+Yellowstone+Hwy,+Idaho+Falls,+ID+83402">Open in Google Maps</a></p>
  </div>
</section>
'''
    return page('/contact/', 'Contact &amp; Directions | Idaho Falls Luxury RV Park',
                'Phone, email, office hours and directions to 3000 S Yellowstone Hwy, Idaho Falls — plus a '
                'form for seasonal stays, group bookings and rig questions.',
                body, active='/contact', og_img='/media/cy0lrm2y/droneparknexttoriver.jpg')

# ================================================================ 404
def notfound():
    body = f'''
<section class="section" style="padding-block:clamp(5rem,14vw,9rem);text-align:center">
  <div class="wrap">
    <span class="eyebrow">404</span>
    <h1>That road doesn&#39;t go through</h1>
    <p class="lede" style="max-width:46ch;margin-inline:auto">The page you were after has moved on.
      Here is where most people are headed.</p>
    <div class="cta-actions" style="margin-top:2.5rem">
      <a class="btn btn-primary btn-lg" href="{u('/rates/')}">Check availability</a>
      <a class="btn btn-outline btn-lg" href="{u('/stay/')}">Compare sites</a>
      <a class="btn btn-outline btn-lg" href="{u('/faq/')}">FAQ</a>
    </div>
  </div>
</section>'''
    return page('/404.html', 'Page Not Found | Idaho Falls Luxury RV Park',
                'That page could not be found. Jump to availability, the site comparison or the FAQ for '
                'Idaho Falls Luxury RV Park.', body)

# ================================================================ BUILD
PAGES = [
    ('/',                 home),
    ('/stay/',            stay),
    ('/stay/rv-sites/',   rv_sites),
    ('/stay/casitas/',    casitas),
    ('/stay/extended/',   extended),
    ('/rates/',           rates),
    ('/park/amenities/',  amenities),
    ('/park/map/',        park_map),
    ('/park/gallery/',    gallery),
    ('/park/policies/',   policies),
    ('/explore/',         explore),
    ('/faq/',             faq),
    ('/about/',           about),
    ('/contact/',         contact),
]

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree('assets', os.path.join(OUT, 'assets'))
    open(os.path.join(OUT, '.nojekyll'), 'w').close()

    print('Building ->', OUT, '(base:', (BASE or '/') + ')')
    for slug, fn in PAGES:
        write(slug, fn())

    with open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(notfound())
    print('   /404.html')

    urls = ''.join(
        f'<url><loc>{SITE}{s}</loc><changefreq>monthly</changefreq>'
        f'<priority>{"1.0" if s == "/" else "0.8"}</priority></url>\n' for s, _ in PAGES)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    print('   /sitemap.xml, /robots.txt  (the live site returns 404 for sitemap.xml)')
    print('\nDone.', len(PAGES) + 1, 'pages.')

if __name__ == '__main__':
    main()
