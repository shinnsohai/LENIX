/* BuiltSync Phase 1 interactive demo.
   A plain-JavaScript port of the demo on the Clarity site (DemoShowcase.jsx), driven by the same data:
   every screen is an image with tap targets ("hotspots", in % of the image) that jump to another screen. */
(function(){
  var D = window.BUILTSYNC_DEMO, root = document.getElementById('demo');
  if (!D || !root) return;

  var UI = {
    en: { play: 'Play tour', pause: 'Pause tour', tryIt: 'Try it:', tap: 'tap', click: 'click', areas: 'the highlighted areas.',
          hl1: 'Highlight tappable areas', hl2: 'Highlight clickable areas', scroll: 'Scroll', enlarge: 'Enlarge screen',
          prev: 'Previous screen', next: 'Next screen', modules: 'Modules', lang: 'Language', close: 'Close' },
    zh: { play: '播放演示', pause: '暂停演示', tryIt: '试一试：', tap: '点击', click: '点击', areas: '高亮区域。',
          hl1: '高亮可点击区域', hl2: '高亮可点击区域', scroll: '向下滑动', enlarge: '放大',
          prev: '上一屏', next: '下一屏', modules: '模块', lang: '语言', close: '关闭' }
  };
  var st = { tab: 'app', cur: { app: 'app-home', admin: 'adm-dashboard' }, hints: true, playing: false, lang: 'en' };
  var timer = 0, focusKey = '';

  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function L(o, k){ return (st.lang === 'zh' && o[k + 'Zh']) || o[k] || ''; }
  function srcOf(s){ return (st.lang === 'zh' && s.imageZh) || s.image; }
  function spots(s){ return (st.lang === 'zh' && s.hotspotsZh) || s.hotspots || []; }

  function prep(group){
    var screens = group.screens, byId = {}, known = [];
    screens.forEach(function(s){ byId[s.id] = s; });
    group.modules.forEach(function(m){ known.push(m.id); });
    var mods = group.modules.slice();
    screens.forEach(function(s){ if (known.indexOf(s.module) < 0){ known.push(s.module); mods.push({ id: s.module, label: s.module, description: '' }); } });
    mods = mods.filter(function(m){ return screens.some(function(s){ return s.module === m.id; }); });
    var ordered = [];
    mods.forEach(function(m){ screens.forEach(function(s){ if (s.module === m.id) ordered.push(s); }); });
    return { group: group, screens: screens, byId: byId, modules: mods, ordered: ordered };
  }
  var V = { app: prep(D.app), admin: prep(D.admin) };

  function view(){ return V[st.tab]; }
  function screen(){ var v = view(); return v.byId[st.cur[st.tab]] || v.ordered[0]; }
  function index(){ var v = view(), s = screen(); return v.ordered.indexOf(s); }

  var ZOOM = '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.5 2H14v4.5M6.5 14H2V9.5M14 2L9 7M2 14l5-5"/></svg>';
  var ARR = '<svg width="14" height="12" viewBox="0 0 12 10" fill="none" aria-hidden="true"><path d="M0.8 5h10M7.1 1.4 10.9 5l-3.8 3.6" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function hotspotHtml(s){
    return spots(s).map(function(h, i){
      return '<button type="button" class="hs' + (st.hints ? ' show' : '') + '" data-act="go" data-arg="' + esc(h.goto) + '" data-k="hs' + i + '"' +
        ' aria-label="' + esc(h.label || 'Open') + '" title="' + esc(h.label || '') + '"' +
        ' style="left:' + h.x + '%;top:' + h.y + '%;width:' + h.w + '%;height:' + h.h + '%"></button>';
    }).join('');
  }

  function render(){
    var ui = UI[st.lang], v = view(), s = screen(), idx = index();
    var isApp = st.tab === 'app';
    var inModule = v.screens.filter(function(x){ return x.module === s.module; });
    var mod = v.modules.filter(function(m){ return m.id === s.module; })[0] || {};
    var langAttr = st.lang === 'zh' ? ' lang="zh-CN"' : '';

    var tabs = ['app', 'admin'].map(function(id){
      return '<button type="button" role="tab" data-act="tab" data-arg="' + id + '" data-k="tab-' + id + '" aria-selected="' + (st.tab === id) + '">' + esc(L(D[id], 'title')) + '</button>';
    }).join('');
    var langs = [['en', 'EN'], ['zh', '中文']].map(function(l){
      return '<button type="button" data-act="lang" data-arg="' + l[0] + '" data-k="lang-' + l[0] + '" aria-pressed="' + (st.lang === l[0]) + '">' + l[1] + '</button>';
    }).join('');
    var mods = v.modules.map(function(m){
      var on = m.id === s.module, desc = L(m, 'description');
      return '<button type="button" role="tab" class="mod' + (on ? ' on' : '') + '" data-act="mod" data-arg="' + esc(m.id) + '" data-k="mod-' + esc(m.id) + '" aria-selected="' + on + '">' +
        '<b>' + esc(L(m, 'label')) + '</b>' + (on && desc ? '<span>' + esc(desc) + '</span>' : '') + '</button>';
    }).join('');

    var img = '<img src="' + esc(srcOf(s)) + '" alt="' + esc(L(s, 'title')) + '" width="' + s.width + '" height="' + s.height + '" draggable="false">';
    var device;
    if (isApp){
      var tall = s.width && s.height && s.height / s.width > 844 / 390 + 0.02;
      device = '<div class="phone-f"><div class="phone-s"><div class="phone-scroll" tabindex="0"><div class="screen">' + img + hotspotHtml(s) + '</div></div>' +
        (tall ? '<span class="scroll-tip">' + ui.scroll + ' ↓</span>' : '') + '</div>' +
        '<button type="button" class="zoom-btn" data-act="zoom" data-k="zoom" aria-label="' + ui.enlarge + '">' + ZOOM + '</button></div>';
    } else {
      device = '<div class="browser-f"><div class="browser-bar"><span class="dots"><i></i><i></i><i></i></span><span class="browser-title">BuiltSync Admin Console</span>' +
        '<button type="button" class="zoom-btn" data-act="zoom" data-k="zoom" aria-label="' + ui.enlarge + '">' + ZOOM + '</button></div>' +
        '<div class="browser-scroll" tabindex="0"><div class="screen">' + img + hotspotHtml(s) + '</div></div></div>';
    }

    var side = '<div class="cap"' + langAttr + '><span class="cap-k">' + esc(L(mod, 'label') || s.module) + ' · ' + (inModule.indexOf(s) + 1) + '/' + inModule.length + '</span>' +
      '<h3>' + esc(L(s, 'title')) + '</h3><p>' + esc(L(s, 'caption')) + '</p>' +
      (spots(s).length ? '<p class="cap-try"><b>' + ui.tryIt + '</b> ' + (isApp ? ui.tap : ui.click) + ' ' + ui.areas + '</p>' : '') + '</div>' +
      '<div class="demo-ctl">' +
        '<button type="button" class="round" data-act="step" data-arg="-1" data-k="prev" aria-label="' + ui.prev + '"><span style="display:inline-block;rotate:180deg">' + ARR + '</span></button>' +
        '<span class="count">' + (idx + 1) + ' / ' + v.ordered.length + '</span>' +
        '<button type="button" class="round" data-act="step" data-arg="1" data-k="next" aria-label="' + ui.next + '">' + ARR + '</button>' +
        '<button type="button" class="pill solid sm" data-act="play" data-k="play" aria-pressed="' + st.playing + '">' + (st.playing ? ui.pause : ui.play) + '</button>' +
      '</div>' +
      '<label class="demo-hint"><input type="checkbox" data-act="hints" data-k="hints"' + (st.hints ? ' checked' : '') + '> ' + (isApp ? ui.hl1 : ui.hl2) + '</label>';

    root.innerHTML =
      '<div class="demo-top"><div class="seg" role="tablist" aria-label="Demo">' + tabs + '</div>' +
        '<div class="demo-top-r"><div class="seg sm" role="group" aria-label="' + ui.lang + '">' + langs + '</div>' +
        '<p class="demo-blurb"' + langAttr + '>' + esc(L(v.group, 'blurb')) + '</p></div></div>' +
      '<div class="demo-grid ' + (isApp ? 'is-app' : 'is-admin') + '">' +
        '<div class="demo-mods" role="tablist" aria-label="' + ui.modules + '">' + mods + '</div>' +
        '<div class="demo-device">' + device + '</div>' +
        '<div class="demo-side">' + side + '</div>' +
      '</div>' +
      '<p class="note demo-note"' + langAttr + '>' + esc(L(D, 'demoNote')) + '</p>';

    if (focusKey){
      var f = root.querySelector('[data-k="' + focusKey + '"]');
      if (f) f.focus({ preventScroll: true });
      focusKey = '';
    }
    /* warm the neighbouring screens so a tap feels instant */
    var warm = [v.ordered[(idx + 1) % v.ordered.length], v.ordered[(idx - 1 + v.ordered.length) % v.ordered.length]];
    spots(s).forEach(function(h){ if (v.byId[h.goto]) warm.push(v.byId[h.goto]); });
    warm.forEach(function(w){ if (w){ var im = new Image(); im.src = srcOf(w); } });
  }

  function stopPlay(){ st.playing = false; clearInterval(timer); }
  function step(d){
    var v = view(), n = v.ordered.length;
    st.cur[st.tab] = v.ordered[(index() + d + n) % n].id;
  }

  /* lightbox: a native <dialog>, so Escape and focus trapping come from the browser */
  var dlg = document.createElement('dialog');
  dlg.className = 'demo-zoom';
  dlg.addEventListener('click', function(e){ if (e.target === dlg || e.target.closest('[data-close]')) dlg.close(); });
  document.body.appendChild(dlg);
  function zoom(){
    var s = screen();
    dlg.innerHTML = '<button type="button" class="round" data-close aria-label="' + UI[st.lang].close + '">×</button>' +
      '<img class="' + (st.tab === 'app' ? 'is-app' : 'is-admin') + '" src="' + esc(srcOf(s)) + '" alt="' + esc(L(s, 'title')) + '">';
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  }

  root.addEventListener('click', function(e){
    var b = e.target.closest('[data-act]');
    if (!b || !root.contains(b) || b.tagName === 'INPUT') return;
    var act = b.getAttribute('data-act'), arg = b.getAttribute('data-arg');
    focusKey = b.getAttribute('data-k') || '';
    if (act === 'zoom'){ zoom(); return; }
    if (act === 'play'){
      st.playing = !st.playing;
      clearInterval(timer);
      if (st.playing) timer = setInterval(function(){ step(1); render(); }, 4200);
    } else {
      stopPlay();
      if (act === 'tab') st.tab = arg;
      else if (act === 'lang') st.lang = arg;
      else if (act === 'go') { st.cur[st.tab] = arg; focusKey = ''; }
      else if (act === 'step') step(+arg);
      else if (act === 'mod'){
        var first = view().screens.filter(function(x){ return x.module === arg; })[0];
        if (first) st.cur[st.tab] = first.id;
      }
    }
    render();
  });
  root.addEventListener('change', function(e){
    if (e.target.getAttribute('data-act') === 'hints'){ st.hints = e.target.checked; focusKey = 'hints'; render(); }
  });
  root.addEventListener('keydown', function(e){
    if (e.target.tagName === 'INPUT') return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft'){
      stopPlay(); step(e.key === 'ArrowRight' ? 1 : -1);
      focusKey = (document.activeElement && document.activeElement.getAttribute('data-k')) || '';
      render();
    }
  });

  /* "See it in the app / console" buttons elsewhere on the page jump the demo to a screen */
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-demo-go]');
    if (!b) return;
    var id = b.getAttribute('data-demo-go'), t = id.indexOf('adm-') === 0 ? 'admin' : 'app';
    stopPlay(); st.tab = t; st.cur[t] = id; render();
    root.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  });

  render();
})();

