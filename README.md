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

### 4. Every photo actually shows what the caption says
The first build assigned images by filename, and the filenames lie. A rendered
contact sheet of the whole media library caught roughly **30 of 61 wrong**:
`lounge.png` is line art rather than the lodge, the pull-through card was showing
pickleball, the laundry card was showing the lodge exterior, the bathroom card was
showing a bike rack, and the Yellowstone card was showing fireworks. Every image
is now checked by eye against its alt text.

### 5. Accessibility
All 26 images on the live homepage ship `alt=""`, including the logo. Every image here has
real alt text (verified in the build: `assert alt`). Also added: visible focus states,
`prefers-reduced-motion`, keyboard-operable dropdowns and accordions, and an ARIA-wired
lightbox, and collapsed accordion panels leave the tab order and the accessibility
tree entirely (a 0-height `overflow:hidden` panel does not).

### The hero video
The live site keeps its motion by autoplaying a YouTube iframe with the controls
stripped (`6YqvRm1ACf0`, `autoplay=1&loop=1&mute=1&controls=0`). That makes a
third-party iframe the LCP element on mobile, pulls the player bundle in before the
hero can paint, gives nobody a way to stop the motion, and ignores
`prefers-reduced-motion`.

This keeps the motion and drops all of that:

- The same footage, cut to the stretch that actually shows the sites and **crossfaded into a
  seamless 6.8s loop**, self-hosted as a 1.9MB H.264 MP4 — no third party at all.
  (VP9/WebM came out *larger* at matched quality, so it isn't shipped.)
- The still behind it is **the video's own first frame** at three widths, so when
  the loop fades in nothing on screen moves.
- The video is `preload="none"` and its source is attached by JS only when it's
  actually wanted. **Phones, `prefers-reduced-motion` and `Save-Data`/2G visitors
  never fetch the 1.9MB** — they get a 63–126KB still instead.
- A real pause control, and the loop stops decoding once it scrolls out of view.

Re-encoding from the YouTube copy is lossy twice over. Hand over the original
export and the same pipeline yields a visibly better file at the same size.

### 6. The park map exists and nobody sees it
`/media/gnabpzdm/park-map-6-10-24-opt.jpg` has been sitting in the media library while
*Virtual Tour & Site Map* ships a fixed `height="800"` iframe and no map at all. It's now a
pan-and-zoom viewer with a site-type legend. The 360° tour holds a 16:10 ratio at every
width and degrades to two working links.

### 7. Policies are readable at the moment they matter
~20 sections of flat prose became accordions grouped by decision stage — *Before you book*
(cancellation, pets, rig age), *Arriving & leaving*, *While you're here*.

### 8. The FAQ was the best content on the site and nobody landed on it
Its trip-planning answers (Yellowstone West Entrance, Tetons, Jackson, SLC) are promoted to
the homepage and to a new `/explore/` page — replacing *Things to Do*, which is currently a
nav parent pointing at a page with no content on it.

### 9. SEO and metadata
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
| **Contact form backend** — currently composes a `mailto:`; the live site has no form at all | `contact()` |
| **Yellowstone / Teton photography** — the library has none, so `/explore/` reuses park shots | `/explore/` |

## Verified, not assumed

Checked on every build: one `<h1>` per page, zero empty `alt` attributes, balanced
tags, no broken `aria-controls`/`label for`/duplicate IDs, no broken internal links,
and all 61 media URLs returning 200. A browser-driven test suite additionally
asserts the accordion open/close contract, that the booking form collects every
field the deep link expects, and that the hero video plays on desktop while never
attaching its source on a narrow viewport.

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
