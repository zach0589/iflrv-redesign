/* =============================================================
   Idaho Falls Luxury RV Park — redesign prototype
   ============================================================= */
(function () {
  'use strict';

  var FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

  /* Keep Tab inside an open overlay. aria-modal alone does not do this. */
  function trapFocus(container) {
    function onKey(e) {
      if (e.key !== 'Tab') return;
      var items = [].slice.call(container.querySelectorAll(FOCUSABLE))
        .filter(function (el) { return el.offsetParent !== null || el === document.activeElement; });
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    container.addEventListener('keydown', onKey);
    return function () { container.removeEventListener('keydown', onKey); };
  }

  /* -----------------------------------------------------------
     BOOKING DEEP LINK

     The live site sends every visitor to the NewBook booking
     engine with no context at all — no dates, no rig length, no
     site type. This rebuilds that handoff so the search the guest
     performs on the marketing site carries into the booking engine.

     ⚑ BEFORE LAUNCH: confirm these query-string parameter names
     against your actual NewBook account. NewBook installs differ,
     and the wrong key names are silently ignored (the guest just
     lands on a blank search). Ask your NewBook rep for the
     "online booking deep link" spec, then update PARAMS below.
     Everything else on the page already works.
  ----------------------------------------------------------- */
  var BOOKING_BASE = 'https://bookingsus.newbook.cloud/idahofallsluxuryrvpark/index.php';
  var PARAMS = {
    arrive:    'period_from',      // ⚑ verify
    depart:    'period_to',        // ⚑ verify
    adults:    'adults',           // ⚑ verify
    children:  'children',         // ⚑ verify
    rig:       'equipment_length', // ⚑ verify — was previously collected and thrown away
    category:  'category_id'       // ⚑ verify — maps to site-type IDs in NewBook
  };

  function bookingUrl(data) {
    var qs = [];
    Object.keys(data).forEach(function (k) {
      var key = PARAMS[k];
      if (key && data[k]) qs.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[k]));
    });
    return BOOKING_BASE + (qs.length ? '?' + qs.join('&') : '');
  }

  /* Availability search form(s) */
  document.querySelectorAll('[data-booking-form]').forEach(function (form) {
    var arrive = form.querySelector('[name="arrive"]');
    var depart = form.querySelector('[name="depart"]');

    // sensible defaults: tonight → tomorrow, and never let depart precede arrive
    var today = new Date();
    var iso = function (d) {
      // NOT toISOString(): that returns the UTC date, which is already tomorrow
      // from ~6pm Mountain Time and would refuse a same-night arrival.
      return d.getFullYear() + '-' +
        String(d.getMonth() + 1).padStart(2, '0') + '-' +
        String(d.getDate()).padStart(2, '0');
    };
    if (arrive) {
      arrive.min = iso(today);
      arrive.addEventListener('change', function () {
        if (!depart) return;
        var next = new Date(arrive.value);
        next.setDate(next.getDate() + 1);
        depart.min = iso(next);
        if (!depart.value || depart.value <= arrive.value) depart.value = iso(next);
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      window.open(bookingUrl({
        arrive: fd.get('arrive'),
        depart: fd.get('depart'),
        adults: fd.get('adults'),
        children: fd.get('children'),
        rig: fd.get('rig'),
        category: fd.get('category')
      }), '_blank', 'noopener');
    });
  });

  /* -----------------------------------------------------------
     Hero video.

     The live site autoplays a YouTube iframe with controls stripped: it
     becomes the LCP element on mobile, pulls in the player bundle before the
     hero can finish painting, offers no way to stop the motion, and ignores
     prefers-reduced-motion.

     This keeps the motion and drops all of that. The still paints first and is
     the video's own opening frame, so the fade-in is invisible. The 3MB loop is
     only ever fetched when it is actually wanted -- never on a phone, never
     under reduced-motion, never on a metered connection -- and there is a real
     pause control.
  ----------------------------------------------------------- */
  (function () {
    var video = document.querySelector('.hero-video');
    if (!video) return;

    var toggle = document.querySelector('[data-motion]');
    var label = document.querySelector('[data-motion-label]');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    // width alone let a large phone in landscape (>860px) pull the 4.4MB loop.
    // A fine pointer additionally excludes phones and tablets.
    var wide = window.matchMedia('(min-width: 861px) and (pointer: fine)');
    var conn = navigator.connection || {};
    var thrifty = conn.saveData === true || /^(slow-)?2g$/.test(conn.effectiveType || '');

    if (!wide.matches || reduced.matches || thrifty) return;  // still image only

    video.src = video.dataset.src;
    video.load();

    video.addEventListener('canplay', function () {
      var p = video.play();
      if (p && p.catch) p.catch(function () { /* autoplay refused: keep the still */ });
    }, { once: true });

    video.addEventListener('playing', function () {
      video.classList.add('is-playing');
      if (toggle) toggle.hidden = false;
    }, { once: true });

    if (toggle) {
      toggle.addEventListener('click', function () {
        var paused = video.paused;
        if (paused) { video.play(); } else { video.pause(); }
        toggle.classList.toggle('is-paused', !paused);
        if (label) label.textContent = paused ? 'Pause' : 'Play';
        toggle.setAttribute('aria-label', (paused ? 'Pause' : 'Play') + ' the background video');
      });
    }

    // stop decoding while the hero is off screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        if (!toggle || !toggle.classList.contains('is-paused')) {
          e[0].isIntersecting ? video.play().catch(function () {}) : video.pause();
        }
      }, { threshold: 0.05 }).observe(video);
    }
  })();

  /* -----------------------------------------------------------
     Contact form — composes a mailto so the prototype has no backend.
     On the real site, point this at your form handler or CRM.
  ----------------------------------------------------------- */
  document.querySelectorAll('[data-mailto-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var body = [];
      fd.forEach(function (v, k) { if (v) body.push(k.toUpperCase() + ': ' + v); });
      window.location.href = 'mailto:' + form.dataset.to +
        '?subject=' + encodeURIComponent('Website enquiry — ' + (fd.get('topic') || 'General')) +
        '&body=' + encodeURIComponent(body.join('\n\n'));
    });
  });

  /* -----------------------------------------------------------
     Header: transparent over hero, solid once scrolled
  ----------------------------------------------------------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* -----------------------------------------------------------
     Navigation — accessible dropdowns (hover on desktop,
     tap/click everywhere, Escape closes, focus is tracked)
  ----------------------------------------------------------- */
  var desktop = window.matchMedia('(min-width:1041px)');

  document.querySelectorAll('.nav-item.has-panel').forEach(function (item) {
    var btn = item.querySelector('.nav-link');
    var close = function () { item.dataset.open = 'false'; btn.setAttribute('aria-expanded', 'false'); };
    var open  = function () { item.dataset.open = 'true';  btn.setAttribute('aria-expanded', 'true'); };

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = item.dataset.open === 'true';
      document.querySelectorAll('.nav-item.has-panel').forEach(function (o) {
        o.dataset.open = 'false';
        o.querySelector('.nav-link').setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) open();
    });

    item.addEventListener('mouseenter', function () { if (desktop.matches) open(); });
    item.addEventListener('mouseleave', function () { if (desktop.matches) close(); });
    item.addEventListener('focusout', function (e) {
      if (desktop.matches && !item.contains(e.relatedTarget)) close();
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.nav-item.has-panel').forEach(function (o) {
      o.dataset.open = 'false';
      o.querySelector('.nav-link').setAttribute('aria-expanded', 'false');
    });
    if (document.body.classList.contains('nav-open')) {
      setDrawer(false);
      if (toggle) toggle.focus();
    }
  });

  document.addEventListener('click', function (e) {
    if (!desktop.matches || e.target.closest('.nav-item.has-panel')) return;
    document.querySelectorAll('.nav-item.has-panel').forEach(function (o) {
      o.dataset.open = 'false';
      o.querySelector('.nav-link').setAttribute('aria-expanded', 'false');
    });
  });

  var toggle = document.querySelector('.nav-toggle');
  var navList = document.querySelector('.nav');
  var releaseNav = null;

  function setDrawer(open) {
    document.body.classList.toggle('nav-open', open);
    if (!toggle) return;
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (releaseNav) { releaseNav(); releaseNav = null; }
    if (open && navList) {
      releaseNav = trapFocus(navList);
      var first = navList.querySelector(FOCUSABLE);
      if (first) first.focus();
    }
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      setDrawer(!document.body.classList.contains('nav-open'));
    });
  }

  /* -----------------------------------------------------------
     Accordions — used for Policies and the FAQ.
     Height is animated explicitly so the panel can be measured
     and so deep links (#anchor) can open the right item.
  ----------------------------------------------------------- */
  document.querySelectorAll('.acc-btn').forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    panel.style.height = '0px';

    btn.addEventListener('click', function () {
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
      // .is-open drives visibility, which keeps a collapsed panel's links out
      // of the tab order and out of the accessibility tree
      panel.classList.toggle('is-open', !isOpen);
      if (isOpen) {
        panel.style.height = panel.firstElementChild.offsetHeight + 'px';
        requestAnimationFrame(function () { panel.style.height = '0px'; });
      } else {
        panel.style.height = panel.firstElementChild.offsetHeight + 'px';
      }
    });

    // Once open, release the fixed height so late reflow (webfonts, text
    // resizing, injected content) can't clip the answer.
    panel.addEventListener('transitionend', function (e) {
      if (e.propertyName === 'height' && panel.classList.contains('is-open')) {
        panel.style.height = 'auto';
      }
    });
  });

  // keep an open panel correctly sized when the viewport reflows
  window.addEventListener('resize', function () {
    document.querySelectorAll('.acc-btn[aria-expanded="true"]').forEach(function (btn) {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (panel) panel.style.height = 'auto';
    });
  });

  // open + scroll to an accordion item linked directly (e.g. /park/policies/#pets)
  function openFromHash() {
    if (!location.hash) return;
    var target = document.querySelector(location.hash);
    if (!target) return;
    var btn = target.matches('.acc-btn') ? target : target.querySelector('.acc-btn');
    if (btn && btn.getAttribute('aria-expanded') !== 'true') btn.click();
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);

  /* -----------------------------------------------------------
     Sticky mobile booking bar — appears once the hero widget
     has scrolled away, so the CTA is never more than a thumb away
  ----------------------------------------------------------- */
  var bar = document.querySelector('.bookbar');
  var anchor = document.querySelector('[data-bookbar-anchor]');
  if (bar) {
    if (anchor && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        bar.classList.toggle('show', !entries[0].isIntersecting);
      }, { rootMargin: '-80px 0px 0px 0px' }).observe(anchor);
    } else {
      bar.classList.add('show');
    }
  }

  /* -----------------------------------------------------------
     Park map — pan and zoom.
     The live site has this map sitting unused in the media
     library while the "Virtual Tour & Site Map" page ships an
     800px iframe and no map at all.
  ----------------------------------------------------------- */
  document.querySelectorAll('.mapbox').forEach(function (box) {
    var frame = box.querySelector('.mapbox-frame');
    var img = frame.querySelector('img');
    var scale = 1;

    function apply() {
      img.style.width = (scale * 100) + '%';
    }
    box.querySelectorAll('[data-zoom]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var step = btn.dataset.zoom === 'in' ? 0.35 : -0.35;
        scale = Math.min(3.5, Math.max(1, scale + step));
        apply();
      });
    });
    box.querySelectorAll('[data-zoom-reset]').forEach(function (btn) {
      btn.addEventListener('click', function () { scale = 1; apply(); frame.scrollTo(0, 0); });
    });

    // keyboard panning — the zoom buttons were operable but the panned map
    // itself was pointer-only
    frame.setAttribute('tabindex', '0');
    frame.setAttribute('role', 'application');
    frame.setAttribute('aria-label', 'Park map. Use the arrow keys to pan, plus and minus to zoom.');
    frame.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 240 : 80, handled = true;
      switch (e.key) {
        case 'ArrowLeft':  frame.scrollLeft -= step; break;
        case 'ArrowRight': frame.scrollLeft += step; break;
        case 'ArrowUp':    frame.scrollTop  -= step; break;
        case 'ArrowDown':  frame.scrollTop  += step; break;
        case '+': case '=': scale = Math.min(3.5, scale + 0.35); apply(); break;
        case '-': case '_': scale = Math.max(1, scale - 0.35); apply(); break;
        case 'Home': scale = 1; apply(); frame.scrollTo(0, 0); break;
        default: handled = false;
      }
      if (handled) e.preventDefault();
    });

    // click-drag panning
    var down = false, sx = 0, sy = 0, sl = 0, st = 0;
    frame.addEventListener('pointerdown', function (e) {
      down = true; sx = e.clientX; sy = e.clientY; sl = frame.scrollLeft; st = frame.scrollTop;
      frame.classList.add('dragging'); frame.setPointerCapture(e.pointerId);
    });
    frame.addEventListener('pointermove', function (e) {
      if (!down) return;
      frame.scrollLeft = sl - (e.clientX - sx);
      frame.scrollTop = st - (e.clientY - sy);
    });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      frame.addEventListener(ev, function () { down = false; frame.classList.remove('dragging'); });
    });
  });

  /* -----------------------------------------------------------
     Birdeye review feed.

     Third-party review widgets are heavy and they are not worth a single
     millisecond of the initial render, so this mounts the iframe only once the
     section is near the viewport. The curated quotes above it are server-
     rendered, so the page still shows proof if this never loads at all.
  ----------------------------------------------------------- */
  document.querySelectorAll('[data-birdeye]').forEach(function (mount) {
    var src = mount.dataset.src;
    if (!src) return;  // not configured yet — leave the placeholder visible

    var mounted = false;
    function load() {
      if (mounted) return;
      mounted = true;
      var frame = document.createElement('iframe');
      frame.src = src;
      frame.title = mount.dataset.label || 'Guest reviews';
      frame.loading = 'lazy';
      frame.height = mount.dataset.height || 520;
      frame.setAttribute('scrolling', 'no');
      mount.textContent = '';
      mount.appendChild(frame);
    }

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (e) {
        if (e[0].isIntersecting) { load(); io.disconnect(); }
      }, { rootMargin: '400px' });
      io.observe(mount);
    } else {
      load();
    }
  });

  /* -----------------------------------------------------------
     Gallery lightbox — minimal, keyboard dismissable
  ----------------------------------------------------------- */
  var figures = document.querySelectorAll('.gallery figure');
  if (figures.length) {
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Photo viewer');
    box.hidden = true;
    box.innerHTML = '<button class="lightbox-close" aria-label="Close photo viewer">&times;</button><img alt="">';
    document.body.appendChild(box);

    var shown = box.querySelector('img');
    var opener = null;
    var releaseBox = null;

    figures.forEach(function (fig) {
      var img = fig.querySelector('img');
      var btn = document.createElement('button');
      btn.className = 'sr';
      btn.textContent = 'View larger: ' + (img.alt || 'photo');
      fig.appendChild(btn);

      var show = function () {
        opener = document.activeElement;
        if (releaseBox) releaseBox();
        releaseBox = trapFocus(box);
        shown.src = img.src.replace(/width=\d+/, 'width=1600');
        shown.alt = img.alt;
        box.hidden = false;
        document.body.style.overflow = 'hidden';
        box.querySelector('.lightbox-close').focus();
      };
      img.addEventListener('click', show);
      btn.addEventListener('click', show);
    });

    var hide = function () {
      if (releaseBox) { releaseBox(); releaseBox = null; }
      box.hidden = true;
      document.body.style.overflow = '';
      if (opener) opener.focus();
    };
    box.addEventListener('click', function (e) { if (e.target !== shown) hide(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) hide(); });
  }
})();
