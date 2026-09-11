# Idaho Falls Luxury RV Park — UX redesign prototype

A working rebuild of [idahofallsluxuryrvpark.com](https://idahofallsluxuryrvpark.com/),
built to demonstrate a set of specific UX fixes rather than to replace the site wholesale.

**Live preview:** https://zach0589.github.io/iflrv-redesign/

Brand colors (`#237d68` / `#195446`), typefaces (Mohave + Noto Sans) and all photography
are the park's own, read straight off the live site, so the comparison is about structure
and flow rather than a change of look.

---

## What this fixes

### 1. You can now find out what it costs and whether there's room
The live site has no rates anywhere and no date picker — the only path is a **Book Now**
button that drops you into NewBook cold, with no dates, no rig length and no site type.
On the current homepage that button sits directly beneath the words *"Call or message to
book now."*

Here, a search widget (dates, rig length, site type) leads every key page and carries the
guest's search into the booking engine. A sticky booking bar follows on mobile.

### 2. Four products, and the nav only admitted three
Site types were scattered across four sibling pages with no way to compare them — and the
**Penthouse Apartment** appeared exactly once on the whole site, buried in the cancellation
policy, with no page selling it.

`/stay/` is now a hub with all four types in one comparison table.

### 3. The mega-nav was leaking into every page
Every page's DOM opened with four orphaned `<h3>`s from the nav panel — so **no page had an
`<h1>`**, and screen reader users heard the same four attraction headings before every page's
actual content. Nav is now a real `<nav>` with list markup; every page has exactly one H1.

### 4. Accessibility
All 26 images on the live homepage ship `alt=""`, including the logo. Every image here has
real alt text (verified in the build: `assert alt`). Also added: visible focus states,
`prefers-reduced-motion`, keyboard-operable dropdowns and accordions, and an ARIA-wired
lightbox. The autoplaying, control-stripped YouTube hero — a third-party iframe as the LCP
element on mobile — is replaced with a responsive image.

### 5. The park map exists and nobody sees it
`/media/gnabpzdm/park-map-6-10-24-opt.jpg` has been sitting in the media library while
*Virtual Tour & Site Map* ships a fixed `height="800"` iframe and no map at all. It's now a
pan-and-zoom viewer with a site-type legend. The 360° tour holds a 16:10 ratio at every
width and degrades to two working links.

### 6. Policies are readable at the moment they matter
~20 sections of flat prose became accordions grouped by decision stage — *Before you book*
(cancellation, pets, rig age), *Arriving & leaving*, *While you're here*.

### 7. The FAQ was the best content on the site and nobody landed on it
Its trip-planning answers (Yellowstone West Entrance, Tetons, Jackson, SLC) are promoted to
the homepage and to a new `/explore/` page — replacing *Things to Do*, which is currently a
nav parent pointing at a page with no content on it.

### 8. SEO and metadata
The live homepage has an empty `<meta name="description">` and empty `og:description`, and
`sitemap.xml` returns 404. Every page here has a real description and OG tags; the build
emits `sitemap.xml` and `robots.txt`, plus `Campground` and `FAQPage` JSON-LD.

---

## ⚑ Things that need your real data

Every one of these is flagged in the amber boxes in the UI. Nothing here invents a number.

| What | Where |
|---|---|
| **Nightly + seasonal rates** — published nowhere on the live site | `RATES` in `build.py` |
| **NewBook deep-link parameter names** — installs differ; wrong keys fail silently | `PARAMS` in `assets/js/site.js` |
| **Winter office hours** — footer says "TBD (check Google)", About says 10am–6pm daily | `footer()` in `build.py` |
| **Speed limit conflict** — Policies says 5 mph, Extended Stay rules say 7.5 mph | pick one |
| **Penthouse Apartment** — has a cancellation policy but no page | needs a page |
| **Restaurant recommendations** — the live "Bars & Restaurants" page is empty | `/explore/#dining` |
| **4th of July details** — the live page is empty | `/explore/#july4` |
| **Contact form backend** — currently `mailto:`; the live site has no form at all | `contact()` |

## Build

```bash
python3 build.py          # -> docs/, pathed for GitHub Pages (/iflrv-redesign)
BASE= python3 build.py    # -> docs/, pathed for a domain root (/)
```

No dependencies, no build toolchain — plain Python 3 emitting static HTML.

- `build.py` — content and page templates
- `assets/css/site.css`, `assets/js/site.js` — hand-written, no framework
- `docs/` — generated output (committed, since GitHub Pages serves it)

Images are referenced from the live site's Umbraco media pipeline, which supports
`?width=&format=webp`, so every image gets a responsive `srcset` for free. If the live
site's media moves, the images here go with it.
