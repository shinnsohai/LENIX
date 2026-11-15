/* LENIX interactions: smooth scroll, page veil, text reveals, navigation, cursor, magnetic buttons,
   the pinned product sequence and the horizontal journey. Needs gsap, ScrollTrigger and (optionally) Lenis.
   If gsap is missing the page stays fully readable: nothing is hidden until html.gsap is set. */
(function(){
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches;
  function $$(sel, ctx){ return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  var veil = document.querySelector('.veil');
  function dropVeil(){ root.classList.remove('enter', 'first'); if (veil) veil.style.display = 'none'; }

  if (!window.gsap || !window.ScrollTrigger){ dropVeil(); return; }
  gsap.registerPlugin(ScrollTrigger);
  root.classList.add('gsap');

  /* ---------- smooth scroll ---------- */
  var lenis = null;
  if (!reduce && window.Lenis){
    try {
      lenis = new Lenis({lerp: 0.11, wheelMultiplier: 1});
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function(t){ lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
      $$('dialog, .tbl-wrap, .mmenu').forEach(function(el){ el.setAttribute('data-lenis-prevent', ''); });
    } catch (err) { lenis = null; }
  }
  function scrollToY(target, offset){
    if (lenis) lenis.scrollTo(target, {offset: offset || 0, duration: 1.3});
    else if (typeof target === 'number') window.scrollTo({top: target, behavior: reduce ? 'auto' : 'smooth'});
    else window.scrollTo({top: target.getBoundingClientRect().top + window.scrollY + (offset || 0), behavior: reduce ? 'auto' : 'smooth'});
  }

  /* ---------- words that rise into place ---------- */
  function split(el){
    var words = [];
    if (!el.getAttribute('aria-label')) el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    (function walk(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(ch){
        if (ch.nodeType === 3){
          var frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(function(tok){
            if (!tok) return;
            if (/^\s+$/.test(tok)){ frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span'), i = document.createElement('span');
            w.className = 'w'; i.className = 'wi'; i.textContent = tok; w.setAttribute('aria-hidden', 'true');
            w.appendChild(i); frag.appendChild(w); words.push(i);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1 && ch.tagName !== 'BR') walk(ch);
      });
    })(el);
    el.classList.add('is-split');
    return words;
  }
  var heroWords = [];
  $$('[data-split]').forEach(function(el){
    if (reduce){ el.classList.add('is-split'); return; }
    var words = split(el);
    gsap.set(words, {yPercent: 115});
    if (el.getAttribute('data-split') === 'hero'){ heroWords = heroWords.concat(words); return; }
    ScrollTrigger.create({trigger: el, start: 'top 90%', once: true, onEnter: function(){
      gsap.to(words, {yPercent: 0, duration: 1.15, ease: 'expo.out', stagger: 0.04});
    }});
  });
  var heroBits = $$('[data-h]');
  if (reduce) gsap.set($$('[data-r],[data-h]'), {opacity: 1});
  else {
    gsap.set('[data-r]', {y: 34});
    ScrollTrigger.batch('[data-r]', {start: 'top 92%', once: true, onEnter: function(batch){
      gsap.to(batch, {opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: 0.08, overwrite: true});
    }});
  }
  function intro(){
    if (reduce) return;
    gsap.to(heroWords, {yPercent: 0, duration: 1.3, ease: 'expo.out', stagger: 0.07});
    gsap.fromTo(heroBits, {opacity: 0, y: 26}, {opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: 0.09, delay: 0.25});
  }

  /* ---------- page veil: a count on the first visit, a wipe between pages ---------- */
  if (veil && root.classList.contains('enter')){
    var count = veil.querySelector('b');
    var lift = function(){
      gsap.to(veil, {yPercent: -100, duration: 0.7, ease: 'expo.inOut', onComplete: dropVeil});
      gsap.delayedCall(0.2, intro);
    };
    if (root.classList.contains('first') && count){
      var o = {v: 0};
      gsap.to(o, {v: 100, duration: 1.15, ease: 'power2.inOut', onUpdate: function(){ count.textContent = Math.round(o.v); }, onComplete: lift});
    } else lift();
  } else { dropVeil(); intro(); }

  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
    var href = a.getAttribute('href');
    if (a.target === '_blank' || a.hasAttribute('download') || /^(mailto:|tel:)/.test(href)) return;
    var url; try { url = new URL(a.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.hash){
      var t = document.getElementById(url.hash.slice(1));
      if (t){ e.preventDefault(); scrollToY(t, -84); history.replaceState(null, '', url.hash); }
      return;
    }
    if (reduce || !veil || /\/demo\//.test(url.pathname)) return;
    e.preventDefault();
    $$('b, img', veil).forEach(function(n){ n.style.display = 'none'; });
    veil.style.display = 'grid';
    gsap.fromTo(veil, {yPercent: 100, opacity: 1, visibility: 'visible'}, {yPercent: 0, duration: 0.6, ease: 'expo.inOut', onComplete: function(){ location.href = a.href; }});
  });
  window.addEventListener('pageshow', function(e){ if (e.persisted && veil){ veil.style.display = 'none'; } });

  /* ---------- navigation ---------- */
  var nav = document.getElementById('nav'), lastY = window.scrollY;
  function onScroll(){
    var y = window.scrollY;
    if (nav){
      nav.classList.toggle('is-solid', y > 30);
      if (y > 500 && y > lastY + 4) nav.classList.add('is-up');
      else if (y < lastY - 4 || y <= 500) nav.classList.remove('is-up');
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, {passive: true}); onScroll();
  $$('.nav-dd').forEach(function(dd){
    var b = dd.querySelector('button');
    b.addEventListener('click', function(e){ e.stopPropagation(); var open = dd.classList.toggle('open'); b.setAttribute('aria-expanded', open); });
    document.addEventListener('click', function(){ dd.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); });
    dd.addEventListener('keydown', function(e){ if (e.key === 'Escape'){ dd.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); b.focus(); } });
  });

  /* ---------- cursor follower and magnetic buttons ---------- */
  if (fine && !reduce){
    var cur = document.querySelector('.cur');
    if (cur){
      var cx = gsap.quickTo(cur, 'x', {duration: 0.35, ease: 'power3'}), cy = gsap.quickTo(cur, 'y', {duration: 0.35, ease: 'power3'});
      var label = cur.querySelector('span');
      window.addEventListener('pointermove', function(e){ cx(e.clientX); cy(e.clientY); }, {passive: true});
      document.addEventListener('pointerover', function(e){
        var t = e.target.closest ? e.target : null; if (!t) return;
        var lab = t.closest('[data-cur]'), link = t.closest('a, button, label, input, [role="button"], .hs');
        cur.classList.toggle('is-label', !!lab);
        cur.classList.toggle('is-link', !lab && !!link);
        if (lab) label.textContent = lab.getAttribute('data-cur');
      });
    }
    $$('.mag').forEach(function(el){
      var mx = gsap.quickTo(el, 'x', {duration: 0.5, ease: 'power3'}), my = gsap.quickTo(el, 'y', {duration: 0.5, ease: 'power3'});
      el.addEventListener('pointermove', function(e){
        var r = el.getBoundingClientRect();
        mx((e.clientX - r.left - r.width / 2) * 0.28); my((e.clientY - r.top - r.height / 2) * 0.4);
      });
      el.addEventListener('pointerleave', function(){ gsap.to(el, {x: 0, y: 0, duration: 0.9, ease: 'elastic.out(1, 0.45)'}); });
    });
    var vis = document.querySelector('.pseq-vis');
    if (vis) window.addEventListener('pointermove', function(e){
      vis.style.setProperty('--ry', (-11 + (e.clientX / window.innerWidth - 0.5) * 12).toFixed(2) + 'deg');
      vis.style.setProperty('--rx', (5 - (e.clientY / window.innerHeight - 0.5) * 9).toFixed(2) + 'deg');
    }, {passive: true});
  }

  var mm = gsap.matchMedia();

  /* ---------- product sequence: one product takes the screen at a time ---------- */
  var pseq = document.querySelector('.pseq');
  if (pseq){
    var pps = $$('.pp', pseq), shots = $$('.pseq-vis a', pseq), rail = $$('.pseq-rail button', pseq), n = pps.length, now = -1;
    var show = function(i){
      if (i === now) return; now = i;
      pps.forEach(function(p, k){ p.classList.toggle('on', k === i); });
      shots.forEach(function(p, k){ p.classList.toggle('on', k === i); });
      rail.forEach(function(p, k){ p.classList.toggle('on', k === i); p.setAttribute('aria-pressed', k === i); });
    };
    show(0);
    mm.add('(min-width: 901px)', function(){
      var st = ScrollTrigger.create({trigger: pseq, start: 'top top', end: 'bottom bottom',
        onUpdate: function(self){ show(Math.min(n - 1, Math.floor(self.progress * n * 0.999))); }});
      var go = function(e){ var i = rail.indexOf(e.currentTarget); scrollToY(st.start + (st.end - st.start) * (i + 0.35) / n); };
      rail.forEach(function(b){ b.addEventListener('click', go); });
      return function(){ rail.forEach(function(b){ b.removeEventListener('click', go); }); };
    });
  }

  /* ---------- journey: vertical scroll becomes sideways travel ---------- */
  var hpan = document.querySelector('.hpan');
  if (hpan){
    mm.add('(min-width: 901px)', function(){
      var track = hpan.querySelector('.hpan-track');
      gsap.to(track, {x: function(){ return -Math.max(0, track.scrollWidth - window.innerWidth); }, ease: 'none',
        scrollTrigger: {trigger: hpan, start: 'top top', end: 'bottom bottom', scrub: reduce ? true : 0.5, invalidateOnRefresh: true,
          onUpdate: function(self){ hpan.style.setProperty('--hp', self.progress.toFixed(3)); }}});
    });
  }

  /* ---------- Singapore time in the hero ---------- */
  var clock = document.querySelector('.js-clock');
  if (clock){
    var fmt; try { fmt = new Intl.DateTimeFormat('en-GB', {timeZone: 'Asia/Singapore', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false}); } catch (err) {}
    var tick = function(){ if (fmt) clock.textContent = 'SGT ' + fmt.format(new Date()); };
    tick(); setInterval(tick, 1000);
  }

  window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ ScrollTrigger.refresh(); });
})();
