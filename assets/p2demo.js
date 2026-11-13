/* BuiltSync Phase 2 guided demo.
   The real prototype (demo/builtsync-phase2/) runs in an iframe on this site. The buttons above it
   drive the prototype by clicking its own controls, so the visitor is taken to each module and can
   then carry on using it freely. */
(function(){
  var box = document.getElementById('p2demo');
  if (!box) return;
  var frameBox = box.querySelector('.p2-frame');
  var cap = box.querySelector('.p2-cap');
  var frame = null, ready = false, current = 0, timers = [];

  /* [label, caption, taps in the worker app, sidebar item in the admin console] */
  var MODS = [
    ['Overview', 'The worker\'s Work Center beside the admin dashboard: one record, two faces.', ['Work'], 'Dashboard'],
    ['Check-in', 'The worker signs in on site inside the geofence. The admin\'s daily attendance summary updates to match.', ['Check-in'], 'Attendance'],
    ['Payslips', 'The worker opens a payslip to confirm or dispute. The admin sees which are confirmed, waiting or disputed.', ['Work', 'Payslips'], 'Payroll'],
    ['Leave', 'The worker applies against their balance. The admin approves from a month calendar.', ['Work', 'Leave'], 'Leave'],
    ['Certificates', 'The worker\'s skill passport beside the admin\'s certificate list, with expiring and expired items flagged.', ['Work', 'Skill Passport'], 'Certificates'],
    ['Claims', 'New in Phase 2: the worker submits an expense claim and the admin approves or rejects it.', ['Work', 'Claims'], 'Claim review'],
    ['Permit to work', 'New in Phase 2: permits to work raised, reviewed and tracked in the console.', ['Work'], 'Permit to Work'],
    ['Site chat', 'New in Phase 2: site group chat with a Kanban board for issues raised from the field.', ['Work'], 'Site chat & Kanban'],
    ['Training', 'New in Phase 2: training booked and tracked for each worker.', ['Work'], 'Training hub']
  ];

  var mods = box.querySelector('.p2-mods');
  mods.innerHTML = MODS.map(function(m, i){
    return '<button type="button" class="mod' + (i === 0 ? ' on' : '') + '" data-p2-mod="' + i + '" aria-pressed="' + (i === 0) + '"><b>' + m[0] + '</b></button>';
  }).join('');
  cap.textContent = MODS[0][1];

  function doc(){ return frame && frame.contentDocument; }
  function clickText(rootId, text){
    var d = doc(), root = d && d.getElementById(rootId), best = null;
    if (!root) return false;
    Array.prototype.forEach.call(root.querySelectorAll('*'), function(el){
      if (el.children.length > 3) return;
      if ((el.textContent || '').replace(/\s+/g, ' ').trim() === text) best = el;
    });
    if (!best) return false;
    (best.closest('button,a,[data-a],[data-act],[data-nav],[role=button]') || best).click();
    return true;
  }
  function press(sel){
    var d = doc(), b = d && d.querySelector(sel);
    if (b && b.getAttribute('aria-pressed') !== 'true') b.click();
  }
  function run(i){
    current = i;
    Array.prototype.forEach.call(mods.children, function(b, k){
      b.classList.toggle('on', k === i); b.setAttribute('aria-pressed', k === i);
    });
    cap.textContent = MODS[i][1];
    if (!ready) return;
    timers.forEach(clearTimeout); timers = [];
    press('[data-lang="en"]');                       /* the guide drives the English labels */
    var steps = MODS[i][2].map(function(t){ return ['worker', t]; });
    steps.push(['admin', MODS[i][3]]);
    steps.forEach(function(s, k){
      timers.push(setTimeout(function(){ clickText(s[0], s[1]); }, 120 + k * 260));
    });
  }
  function setView(v){
    Array.prototype.forEach.call(box.querySelectorAll('[data-p2-view]'), function(b){
      b.setAttribute('aria-pressed', b.getAttribute('data-p2-view') === v);
    });
    if (ready) press('[data-v="' + v + '"]');
  }
  function start(){
    if (frame) return;
    frame = document.createElement('iframe');
    frame.title = 'BuiltSync Phase 2 prototype';
    frame.src = box.getAttribute('data-src');
    frame.addEventListener('load', function(){
      ready = true;
      setTimeout(function(){
        press('[data-lang="en"]');
        var pressed = box.querySelector('[data-p2-view][aria-pressed="true"]');
        setView(pressed ? pressed.getAttribute('data-p2-view') : (frame.clientWidth >= 1180 ? 'both' : 'app'));
        run(current);
      }, 500);
    });
    frameBox.innerHTML = '';
    frameBox.classList.add('is-live');
    frameBox.appendChild(frame);
  }

  box.addEventListener('click', function(e){
    var b = e.target.closest('[data-p2-mod],[data-p2-view],[data-p2-start]');
    if (!b) return;
    if (b.hasAttribute('data-p2-start')){ start(); return; }
    if (!frame) start();
    if (b.hasAttribute('data-p2-view')) setView(b.getAttribute('data-p2-view'));
    else run(+b.getAttribute('data-p2-mod'));
  });
  /* pick the view that fits before the prototype loads */
  var fit = frameBox.clientWidth >= 1180 ? 'both' : 'app';
  Array.prototype.forEach.call(box.querySelectorAll('[data-p2-view]'), function(b){
    b.setAttribute('aria-pressed', b.getAttribute('data-p2-view') === fit);
  });
})();
