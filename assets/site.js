/* LENIX site behaviour. Loaded at the end of <body> on every page. */
(function(){
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $$(sel, ctx){ return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function clamp(v){ return v < 0 ? 0 : v > 1 ? 1 : v; }

  /* ---------- theme ---------- */
  function setTheme(t, save){
    root.setAttribute('data-theme', t);
    if (save){ try { localStorage.setItem('lenix-theme', t); } catch (e) {} }
    var next = t === 'light' ? 'dark' : 'light';
    $$('.js-theme').forEach(function(b){
      b.setAttribute('aria-label', 'Switch to ' + next + ' theme');
      var label = b.querySelector('.js-theme-label');
      if (label) label.textContent = next === 'light' ? 'Light theme' : 'Dark theme';
    });
  }
  setTheme(root.getAttribute('data-theme') === 'light' ? 'light' : 'dark', false);
  $$('.js-theme').forEach(function(b){
    b.addEventListener('click', function(){
      setTheme(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light', true);
    });
  });

  /* ---------- menus (hero burger and top bar burger) ---------- */
  $$('.js-burger').forEach(function(burger){
    var menu = document.getElementById(burger.getAttribute('aria-controls'));
    if (!menu) return;
    function isOpen(){ return menu.classList.contains('open'); }
    function set(open){
      menu.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
    burger.addEventListener('click', function(e){ e.stopPropagation(); set(!isOpen()); });
    menu.addEventListener('click', function(e){ if (e.target.closest('a')) set(false); });
    document.addEventListener('click', function(e){
      if (isOpen() && !menu.contains(e.target) && !burger.contains(e.target)) set(false);
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && isOpen()){ set(false); burger.focus(); }
    });
  });

  /* ---------- scroll-linked state ---------- */
  var hero = document.querySelector('.hero');
  var topbar = document.getElementById('topbar');
  var linked = reduce ? [] : $$('[data-scroll]');
  var hasProgress = !!document.querySelector('.progress');
  var tocLinks = $$('.toc a');
  var tocSecs = tocLinks.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); });
  var ticking = false;
  var pending = [];
  var pins = reduce ? [] : $$('[data-pin]');
  pins.forEach(function(el){
    if (!el.hasAttribute('data-scene')) return;
    el._scene = {
      steps: $$('.scene-steps li', el),
      count: el.querySelector('.scene-count'),
      imgs: $$('.stage img', el),
      idx: -2
    };
  });

  function update(){
    ticking = false;
    var vh = window.innerHeight, y = window.scrollY;

    if (hero){
      var hh = hero.offsetHeight;
      if (!reduce && y <= hh) hero.style.setProperty('--hs', clamp(y / hh).toFixed(3));
      if (topbar){
        var hide = y < hh * 0.72;
        topbar.classList.toggle('is-hidden', hide);
        if (hide) topbar.setAttribute('inert', ''); else topbar.removeAttribute('inert');
      }
    }

    /* each [data-scroll] gets --p: 0 as its top enters the lower viewport, 1 once it has passed through */
    linked.forEach(function(el){
      var r = el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      var span = el.hasAttribute('data-steps') ? Math.max(vh * 0.45, r.height * 0.8) : r.height + vh * 0.25;
      var p = clamp((vh * 0.85 - r.top) / span);
      el.style.setProperty('--p', p.toFixed(3));
      var steps = el.children, n = steps.length;
      if (el.hasAttribute('data-steps')){
        for (var i = 0; i < n; i++) steps[i].classList.toggle('on', p >= i / n + 0.03);
      }
    });

    /* pinned chapters and scenes: --p is progress through the pinned distance */
    var wide = window.innerWidth > 900;
    pins.forEach(function(el){
      var r = el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      var total = r.height - vh;
      var p = total > 0 ? clamp(-r.top / total) : 1;
      el.style.setProperty('--p', p.toFixed(3));
      var sc = el._scene;
      if (!sc) return;
      if (!wide){
        if (sc.idx !== -1){
          sc.idx = -1; el.removeAttribute('data-step');
          sc.imgs.forEach(function(im, i){ im.style.transform = ''; im.classList.toggle('on', i === 0); });
        }
        return;
      }
      var n = sc.steps.length, idx = Math.min(n - 1, Math.floor(p * n * 0.999));
      if (idx === sc.idx) return;
      sc.idx = idx;
      el.setAttribute('data-step', idx);
      sc.steps.forEach(function(s, i){ s.classList.toggle('on', i === idx); });
      if (sc.count) sc.count.textContent = (idx + 1) + ' / ' + n;
      if (sc.imgs.length){
        /* data-img picks which real screen is showing; the others fade out */
        var attr = sc.steps[idx].getAttribute('data-img');
        var k = attr === null ? 0 : +attr;            /* -1 means no picture for this step */
        sc.imgs.forEach(function(im, i){ im.classList.toggle('on', i === k); });
        sc.img = sc.imgs[k] || sc.imgs[0];
        /* data-focus="x,y,scale": centre that point of the image, without showing past its edges */
        var f = (sc.steps[idx].getAttribute('data-focus') || '0.5,0.5,1').split(',').map(Number);
        var s = f[2] || 1;
        var tx = Math.max((1 - s) * 100, Math.min(0, (0.5 - f[0] * s) * 100));
        var ty = Math.max((1 - s) * 100, Math.min(0, (0.5 - f[1] * s) * 100));
        sc.img.style.transform = 'translate(' + tx.toFixed(2) + '%,' + ty.toFixed(2) + '%) scale(' + s + ')';
      }
    });

    if (pending.length){
      pending = pending.filter(function(el){
        var r = el.getBoundingClientRect();
        if (r.top < vh * 0.86 && r.bottom > 0){ el.classList.add('in'); return false; }
        return true;
      });
    }

    if (hasProgress){
      var max = root.scrollHeight - vh;
      root.style.setProperty('--read', max > 0 ? clamp(y / max).toFixed(4) : '0');
    }

    if (tocLinks.length){
      var cur = 0;
      for (var j = 0; j < tocSecs.length; j++){
        if (tocSecs[j] && tocSecs[j].getBoundingClientRect().top < vh * 0.38) cur = j;
      }
      tocLinks.forEach(function(a, k){
        a.classList.toggle('on', k === cur);
        if (k === cur) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    }
  }
  function onScroll(){ if (!ticking){ ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);

  /* ---------- reveals that happen once, on entry ---------- */
  /* Checked in the scroll loop, not with IntersectionObserver: a fully clipped
     element reports no intersection, so the clip-path wipe would never start. */
  if (!reduce){
    root.classList.add('motion');
    $$('.stagger').forEach(function(list){
      Array.prototype.forEach.call(list.children, function(c, i){ c.style.setProperty('--i', Math.min(i, 8)); });
    });
    pending = $$('.wipe, .stagger');
  }
  update();

  /* ---------- live demos: an app is loaded into the page only when the visitor asks for it ---------- */
  $$('.js-embed').forEach(function(btn){
    btn.addEventListener('click', function(){
      var box = btn.closest('.embed'), f = document.createElement('iframe');
      f.src = btn.getAttribute('data-src');
      f.title = btn.getAttribute('data-title') || 'Live demo';
      box.innerHTML = '';
      box.classList.add('is-live');
      box.appendChild(f);
      f.focus();
    });
  });

  /* ---------- Smart Site demo dashboard: illustrative data only ---------- */
  var dash = document.getElementById('dash');
  if (dash){
    var TOTAL = 1200;
    var range = dash.querySelector('input[type=range]');
    var out = dash.querySelector('output');
    var btn = dash.querySelector('.js-muster');
    var muster = 0, raf = 0;
    var put = function(sel, v){
      $$(sel, dash).forEach(function(n){ n.textContent = typeof v === 'number' ? v.toLocaleString('en-SG') : v; });
    };
    var render = function(){
      var t = +range.value, mins = 420 + t * 30;
      var hh = Math.floor(mins / 60);
      out.textContent = (hh < 10 ? '0' : '') + hh + ':' + (mins % 60 ? '30' : '00');
      var entries = Math.round(TOTAL * clamp((t + 1) / 3));
      var exits = Math.round(TOTAL * clamp((t - 19) / 5));
      var on = entries - exits;
      var early = t <= 1, late = t >= 20;
      var share = { yard: early ? 0.7 : 0.04, gate: early ? 0.2 : (late ? 0.15 : 0.03), store: early ? 0.02 : 0.06, room: early ? 0 : 0.05 };
      var waiting = muster >= 1 ? Math.min(3, on) : 0;
      var atMuster = muster >= 1 ? on - waiting : Math.round(on * muster);
      var rest = muster >= 1 ? 0 : on - atMuster;
      var used = 0;
      ['yard', 'gate', 'store', 'room'].forEach(function(z){
        var v = Math.round(rest * share[z]); used += v; put('[data-z="' + z + '"]', v);
      });
      put('[data-z="building"]', rest - used);
      put('[data-z="muster"]', atMuster);
      put('[data-k="on"]', on); put('[data-k="in"]', entries); put('[data-k="out"]', exits); put('[data-k="muster"]', atMuster);
      put('[data-k="await"]', muster >= 1 ? waiting + ' awaiting confirmation' : (muster > 0 ? 'Drill in progress' : 'No drill running'));
    };
    var stop = function(){ cancelAnimationFrame(raf); muster = 0; btn.textContent = 'Start muster drill'; };
    range.addEventListener('input', function(){ stop(); render(); });
    btn.addEventListener('click', function(){
      if (muster > 0){ stop(); render(); return; }
      btn.textContent = 'Reset';
      if (reduce){ muster = 1; render(); return; }
      var t0 = performance.now();
      var step = function(now){
        muster = Math.max(0.001, clamp((now - t0) / 2600));
        render();
        if (muster < 1) raf = requestAnimationFrame(step);
      };
      raf = requestAnimationFrame(step);
    });
    render();
  }

  /* ---------- hero background video: two copies cross-fade at the loop point ---------- */
  var A = document.getElementById('bgVideoA'), B = document.getElementById('bgVideoB');
  if (A && B){
    if (reduce){
      A.removeAttribute('autoplay'); A.pause(); B.pause();
      try { A.currentTime = 0; } catch (e) {}
    } else {
      var FADE = 0.9, cur = A, nxt = B, swapping = false;
      var play = function(v){ var p = v.play(); if (p && p.catch) p.catch(function(){}); };
      play(A);
      var tick = function(){
        if (swapping || !cur.duration) return;
        if (cur.duration - cur.currentTime > FADE) return;
        swapping = true;
        var out = cur;
        try { nxt.currentTime = 0; } catch (e) {}
        play(nxt);
        nxt.classList.add('is-active'); out.classList.remove('is-active');
        cur = nxt; nxt = out;
        setTimeout(function(){ out.pause(); try { out.currentTime = 0; } catch (e) {} swapping = false; }, FADE * 1000 + 100);
      };
      A.addEventListener('timeupdate', tick);
      B.addEventListener('timeupdate', tick);
    }
  }
})();
