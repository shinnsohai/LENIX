/* LENIX 3D scene.
   One cloud of points sits behind every page. As the visitor scrolls, the cloud flows into the shape
   named by the nearest [data-shape] marker: a linked globe, a thread, a building under construction,
   a skill passport, a course calendar, a site with reader rings, and the X from the logo.
   The pointer acts like a reader: points near it light up and lean away. */
import * as THREE from './vendor/three.module.min.js';

(function(){
  var canvas = document.getElementById('gl');
  if (!canvas) return;
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var small = Math.min(window.innerWidth, window.innerHeight) < 700;
  var N = small ? 7000 : 16000;

  var renderer;
  try {
    renderer = new THREE.WebGLRenderer({canvas: canvas, antialias: false, alpha: true, powerPreference: 'high-performance', preserveDrawingBuffer: /[?&]shot/.test(location.search)});
  } catch (err) { root.classList.add('no-gl'); return; }
  renderer.setClearColor(0x000000, 0);

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50);
  camera.position.set(0, 0, 7);
  var HALF_H = Math.tan(16 * Math.PI / 180) * 7;

  /* ---------- deterministic random ---------- */
  var seed = 20261;
  function rnd(){ seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }
  function jit(a){ return (rnd() - 0.5) * a; }

  /* ---------- shape helpers ---------- */
  function fromSegs(segs, n, out, off, j){
    var total = 0, i, s;
    var len = segs.map(function(s){ var l = Math.hypot(s[3]-s[0], s[4]-s[1], s[5]-s[2]) * (s[6] || 1); total += l; return l; });
    for (i = 0; i < n; i++){
      var r = rnd() * total, k = 0;
      while (k < len.length - 1 && r > len[k]){ r -= len[k]; k++; }
      s = segs[k]; var t = rnd(), o = (off + i) * 3;
      out[o]   = s[0] + (s[3]-s[0]) * t + jit(j);
      out[o+1] = s[1] + (s[4]-s[1]) * t + jit(j);
      out[o+2] = s[2] + (s[5]-s[2]) * t + jit(j);
    }
  }
  function rect(x0, y0, x1, y1, z){ return [[x0,y0,z,x1,y0,z],[x1,y0,z,x1,y1,z],[x1,y1,z,x0,y1,z],[x0,y1,z,x0,y0,z]]; }
  function rectXZ(x0, z0, x1, z1, y){ return [[x0,y,z0,x1,y,z0],[x1,y,z0,x1,y,z1],[x1,y,z1,x0,y,z1],[x0,y,z1,x0,y,z0]]; }
  function ring(cx, cy, cz, r, plane, n){
    var segs = [], i;
    for (i = 0; i < n; i++){
      var a = i / n * Math.PI * 2, b = (i + 1) / n * Math.PI * 2;
      if (plane === 'xz') segs.push([cx + Math.cos(a)*r, cy, cz + Math.sin(a)*r, cx + Math.cos(b)*r, cy, cz + Math.sin(b)*r]);
      else segs.push([cx + Math.cos(a)*r, cy + Math.sin(a)*r, cz, cx + Math.cos(b)*r, cy + Math.sin(b)*r, cz]);
    }
    return segs;
  }
  function put(out, i, x, y, z){ out[i*3] = x; out[i*3+1] = y; out[i*3+2] = z; }

  var SHAPES = {
    globe: function(out){
      var R = 1.55, i, a = Math.floor(N * 0.6), b = Math.floor(N * 0.84);
      for (i = 0; i < a; i++){
        var y = 1 - (i / (a - 1)) * 2, rad = Math.sqrt(1 - y * y), th = i * 2.399963;
        put(out, i, Math.cos(th) * rad * R, y * R, Math.sin(th) * rad * R);
      }
      for (i = a; i < b; i++){
        var ang = rnd() * Math.PI * 2;
        if (rnd() < 0.5){ var lat = (Math.floor(rnd() * 7) - 3) * 0.42, cr = Math.cos(lat) * R; put(out, i, Math.cos(ang) * cr, Math.sin(lat) * R, Math.sin(ang) * cr); }
        else { var lon = Math.floor(rnd() * 8) * Math.PI / 8; put(out, i, Math.cos(ang) * Math.cos(lon) * R, Math.sin(ang) * R, Math.cos(ang) * Math.sin(lon) * R); }
      }
      var arcs = [], k;
      for (k = 0; k < 16; k++){
        var p = new THREE.Vector3(jit(2), jit(2), jit(2)).normalize(), q = new THREE.Vector3(jit(2), jit(2), jit(2)).normalize();
        arcs.push([p, q]);
      }
      var v = new THREE.Vector3();
      for (i = b; i < N; i++){
        var arc = arcs[i % arcs.length], t = rnd();
        v.copy(arc[0]).lerp(arc[1], t).normalize().multiplyScalar(R * (1 + 0.34 * Math.sin(Math.PI * t)));
        put(out, i, v.x, v.y, v.z);
      }
    },
    thread: function(out){
      var i, nodes = [-2.28, 0, 2.28], a = Math.floor(N * 0.84);
      for (i = 0; i < a; i++){
        var s = i % 9, x = (rnd() * 2 - 1) * 3.5, env = Math.abs(Math.sin(x * 1.378)), ph = s * 0.698;
        put(out, i, x, Math.sin(x * 1.5 + ph) * 0.62 * env + jit(0.02), Math.cos(x * 1.2 + ph * 1.7) * 0.55 * env + jit(0.02));
      }
      for (i = a; i < N; i++){
        var c = nodes[i % 3], d = new THREE.Vector3(jit(2), jit(2), jit(2)).normalize().multiplyScalar(0.16 + rnd() * 0.04);
        put(out, i, c + d.x, d.y, d.z);
      }
    },
    tower: function(out){
      var segs = [], y, w = 0.68, d = 0.5;
      for (y = -1.5; y <= 1.31; y += 0.4) segs = segs.concat(rectXZ(-w, -d, w, d, y));
      [[-w,-d],[w,-d],[w,d],[-w,d],[0,-d],[0,d]].forEach(function(c){ segs.push([c[0], -1.5, c[1], c[0], 1.3, c[1]]); });
      segs.push([1.2, -1.5, -0.2, 1.2, 1.95, -0.2, 1.6], [-1.0, 1.95, -0.2, 2.0, 1.95, -0.2, 1.6], [1.2, 2.25, -0.2, -1.0, 1.95, -0.2], [1.2, 2.25, -0.2, 2.0, 1.95, -0.2],
                [-0.55, 1.95, -0.2, -0.55, 1.45, -0.2]);
      segs = segs.concat(rect(-0.68, 1.3, -0.42, 1.45, -0.2));
      var g; for (g = -2; g <= 2.01; g += 0.5){ segs.push([g, -1.5, -1.4, g, -1.5, 1.4, 0.35], [-2, -1.5, g * 0.7, 2, -1.5, g * 0.7, 0.35]); }
      fromSegs(segs, N, out, 0, 0.014);
    },
    card: function(out){
      var segs = [], i, a = Math.floor(N * 0.56);
      segs = segs.concat(rect(-1.35, -0.85, 1.35, 0.85, 0)).map(function(s){ s[6] = 1.6; return s; });
      segs = segs.concat(rect(-1.17, -0.71, 1.53, 0.99, -0.4));
      segs = segs.concat(ring(-0.78, 0.22, 0, 0.36, 'xy', 28));
      segs.push([-1.1, -0.36, 0, -0.46, -0.36, 0], [-1.1, -0.54, 0, -0.66, -0.54, 0]);
      [0.5, 0.2, -0.1, -0.4].forEach(function(y){ segs = segs.concat(rect(-0.1, y - 0.07, 1.05, y + 0.07, 0)); });
      segs = segs.concat(ring(0.92, -0.6, 0, 0.13, 'xy', 18));
      segs.push([0.86, -0.6, 0, 0.91, -0.65, 0, 2], [0.91, -0.65, 0, 0.99, -0.55, 0, 2]);
      fromSegs(segs, a, out, 0, 0.012);
      var fills = [[0.5, 1.0], [0.2, 0.72], [-0.1, 0.9], [-0.4, 0.55]], b = Math.floor(N * 0.82);
      for (i = a; i < b; i++){ var f = fills[i % 4]; put(out, i, -0.1 + rnd() * 1.15 * f[1], f[0] + jit(0.12), jit(0.02)); }
      for (i = b; i < N; i++){ var r = Math.sqrt(rnd()) * 0.34, th = rnd() * 6.283; put(out, i, -0.78 + Math.cos(th) * r, 0.22 + Math.sin(th) * r, jit(0.02)); }
    },
    calendar: function(out){
      var segs = [], c, r, cell = 0.36, gap = 0.07, x0 = -(7 * cell + 6 * gap) / 2, y0 = 0.72, on = {}, list = [1, 3, 8, 9, 12, 16, 18, 22, 23, 27, 31];
      list.forEach(function(k){ on[k] = 1; });
      for (r = 0; r < 5; r++) for (c = 0; c < 7; c++){
        var x = x0 + c * (cell + gap), y = y0 - r * (cell + gap), z = on[r * 7 + c] ? 0.34 : 0;
        segs = segs.concat(rect(x, y - cell, x + cell, y, z));
        if (z) [[x, y], [x + cell, y], [x, y - cell], [x + cell, y - cell]].forEach(function(p){ segs.push([p[0], p[1], 0, p[0], p[1], z]); });
      }
      segs = segs.concat(rect(x0, y0 + 0.14, -x0, y0 + 0.36, 0));
      var a = Math.floor(N * 0.62), i;
      fromSegs(segs, a, out, 0, 0.01);
      for (i = a; i < N; i++){
        if (i % 9 === 0){ put(out, i, x0 + rnd() * -2 * x0, y0 + 0.14 + rnd() * 0.22, jit(0.02)); continue; }
        var k = list[i % list.length], cc = k % 7, rr = Math.floor(k / 7);
        put(out, i, x0 + cc * (cell + gap) + rnd() * cell, y0 - rr * (cell + gap) - rnd() * cell, 0.34 + jit(0.02));
      }
    },
    site: function(out){
      var segs = [], g, y = -0.7;
      for (g = -2.25; g <= 2.26; g += 0.5){ segs.push([g, y, -2.25, g, y, 2.25, 0.3], [-2.25, y, g, 2.25, y, g, 0.3]); }
      segs = segs.concat(rectXZ(-1.9, -1.5, 1.9, 1.5, y), rectXZ(-1.9, -1.5, 1.9, 1.5, y + 0.16));
      var bw = 0.55, bd = 0.38, by;
      for (by = 0; by <= 1.21; by += 0.3) segs = segs.concat(rectXZ(-bw, -bd, bw, bd, y + by));
      [[-bw,-bd],[bw,-bd],[bw,bd],[-bw,bd]].forEach(function(c){ segs.push([c[0], y, c[1], c[0], y + 1.2, c[1]]); });
      [[-1.9, 0.2], [0.3, 1.5], [1.35, -0.85], [-0.9, -1.0]].forEach(function(p){
        segs.push([p[0], y, p[1], p[0], y + 0.55, p[1], 2.4]);
        [0.22, 0.45, 0.7].forEach(function(r, k){ segs = segs.concat(ring(p[0], y + 0.03, p[1], r, 'xz', 22).map(function(s){ s[6] = 1.5 - k * 0.3; return s; })); });
      });
      fromSegs(segs, N, out, 0, 0.012);
    },
    xmark: function(out){
      var i, L = 1.55, T = 0.27, c = Math.SQRT1_2;
      for (i = 0; i < N; i++){
        var u = (rnd() * 2 - 1) * L, v = (rnd() * 2 - 1) * T, flip = i % 2 ? 1 : -1;
        var x = (u - v * flip) * c, y = (u * flip + v) * c, z = jit(0.12);
        if (x > 0.25 && y > 0.25){
          var q = 0.17, far = Math.min(1, (x + y - 0.5) / 1.9);
          x = Math.round(x / q) * q + jit(0.1) * (1 - far); y = Math.round(y / q) * q + jit(0.1) * (1 - far);
          if (rnd() < far * 0.75){ x += rnd() * 0.9; y += rnd() * 0.9; z += jit(0.6); }
        }
        put(out, i, x, y, z);
      }
    },
    field: function(out){
      var i;
      for (i = 0; i < N; i++){
        var x = (rnd() * 2 - 1) * 4.6, z = (rnd() * 2 - 1) * 2.6;
        put(out, i, x, Math.sin(x * 1.15) * Math.cos(z * 1.3) * 0.3 - 0.5, z);
      }
    }
  };
  /* how each shape is held: c = colours (dark theme), spin = keeps turning, tilt = lean toward the viewer */
  var LOOK = {
    globe:    {c: ['#27d3ff', '#8a5cff'], spin: 1, tilt: 0.28, scale: 0.84},
    thread:   {c: ['#27d3ff', '#ff3d9a'], spin: 0, tilt: 0.1,  scale: 1},
    tower:    {c: ['#8a5cff', '#27d3ff'], spin: 1, tilt: 0.18, scale: 0.92},
    card:     {c: ['#27d3ff', '#4a7dff'], spin: 0, tilt: -0.08, scale: 1},
    calendar: {c: ['#ff3d9a', '#8a5cff'], spin: 0, tilt: -0.5, scale: 1},
    site:     {c: ['#ff8a1f', '#ffd166'], spin: 1, tilt: 0.52, scale: 1},
    xmark:    {c: ['#27d3ff', '#ff3d9a'], spin: 0, tilt: 0,    scale: 1},
    field:    {c: ['#4a7dff', '#8a5cff'], spin: 0, tilt: 0.34, scale: 1}
  };
  var cache = {};
  function shape(name){
    if (!SHAPES[name]) name = 'globe';
    if (!cache[name]){ seed = 20261 + name.length * 977; var a = new Float32Array(N * 3); SHAPES[name](a); cache[name] = a; }
    return cache[name];
  }

  /* ---------- points ---------- */
  var cur = new Float32Array(N * 3), seeds = new Float32Array(N), rate = new Float32Array(N), i;
  for (i = 0; i < N; i++){ seeds[i] = Math.random(); rate[i] = 0.022 + Math.random() * 0.075; }
  var geo = new THREE.BufferGeometry();
  var posAttr = new THREE.BufferAttribute(cur, 3); posAttr.setUsage(THREE.DynamicDrawUsage);
  geo.setAttribute('position', posAttr);
  geo.setAttribute('aSeed', new THREE.BufferAttribute(seeds, 1));
  geo.boundingSphere = new THREE.Sphere(new THREE.Vector3(), 20);

  var uni = {
    uTime: {value: 0}, uSize: {value: small ? 30 : 34}, uPx: {value: 1}, uStir: {value: 0},
    uMouse: {value: new THREE.Vector3(0, 0, 0)}, uAlpha: {value: 0}, uLight: {value: 0},
    uC1: {value: new THREE.Color('#27d3ff')}, uC2: {value: new THREE.Color('#8a5cff')}
  };
  var mat = new THREE.ShaderMaterial({
    uniforms: uni, transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: [
      'attribute float aSeed;',
      'uniform float uTime, uSize, uPx, uStir; uniform vec3 uMouse;',
      'varying float vMix; varying float vGlow;',
      'void main(){',
      '  vec3 p = position; float t = uTime;',
      '  p += vec3(sin(t*.7 + aSeed*40.), cos(t*.6 + aSeed*31.), sin(t*.5 + aSeed*17.)) * (.012 + uStir*.13);',
      '  vec4 w = modelMatrix * vec4(p, 1.);',
      '  vec2 d = w.xy - uMouse.xy; float f = smoothstep(.95, 0., length(d)) * uMouse.z;',
      '  w.xy += normalize(d + 1e-4) * f * .2; w.z += f * .3;',
      '  vGlow = f;',
      '  vec4 mv = viewMatrix * w;',
      '  gl_Position = projectionMatrix * mv;',
      '  float tw = .72 + .28 * sin(t*1.7 + aSeed*90.);',
      '  gl_PointSize = uSize * uPx * (.55 + aSeed*.95) * tw * (1. + f*1.5) / -mv.z;',
      '  vMix = clamp(position.y*.32 + .5 + (aSeed - .5)*.5, 0., 1.);',
      '}'].join('\n'),
    fragmentShader: [
      'precision mediump float;',
      'uniform vec3 uC1, uC2; uniform float uAlpha, uLight;',
      'varying float vMix; varying float vGlow;',
      'void main(){',
      '  float d = length(gl_PointCoord - .5); float a = smoothstep(.5, .12, d);',
      '  if (a < .01) discard;',
      '  vec3 col = mix(uC1, uC2, vMix);',
      '  col = mix(col, mix(vec3(1.), col*.55, uLight), vGlow*.65);',
      '  gl_FragColor = vec4(col, a * uAlpha * (.5 + vGlow*.5 + uLight*.25));',
      '}'].join('\n')
  });
  var cloud = new THREE.Points(geo, mat);
  cloud.frustumCulled = false;
  cloud.rotation.order = 'XYZ';
  scene.add(cloud);

  /* ---------- state ---------- */
  var marks = [], target = shape('globe'), active = null;
  var goal = {x: 0, y: 0, scale: 1, alpha: 0.9, tilt: 0.28, spin: 1, c1: new THREE.Color(), c2: new THREE.Color()};
  var pose = {x: 0, y: 0, scale: 1, alpha: 0, tilt: 0.28, angle: 0};
  var aspect = 1, light = false, pointer = {x: 0, y: 0, on: 0, px: 0, py: 0}, started = false;

  function collect(){ marks = Array.prototype.slice.call(document.querySelectorAll('[data-shape]')); }
  function setTheme(){
    light = root.getAttribute('data-theme') === 'light';
    mat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
    mat.needsUpdate = true;
    uni.uLight.value = light ? 1 : 0;
    if (active) apply(active, true);
  }
  function apply(el, keepShape){
    active = el;
    var name = el.getAttribute('data-shape'), look = LOOK[name] || LOOK.globe;
    if (!keepShape){ target = shape(name); uni.uStir.value = reduce ? 0 : 1; }
    var c1 = el.getAttribute('data-c1') || look.c[0], c2 = el.getAttribute('data-c2') || look.c[1];
    goal.c1.set(c1); goal.c2.set(c2);
    if (light){ goal.c1.multiplyScalar(0.62); goal.c2.multiplyScalar(0.62); }
    var pos = el.getAttribute('data-pos') || 'center', narrow = aspect < 1;
    var halfW = HALF_H * aspect;
    goal.x = narrow ? 0 : pos === 'right' ? halfW * 0.5 : pos === 'left' ? -halfW * 0.5 : 0;
    goal.y = narrow ? (pos !== 'center' ? 0.55 : 0) : (+el.getAttribute('data-y') || 0);
    goal.scale = (+el.getAttribute('data-scale') || 1) * look.scale * (narrow ? Math.max(0.5, aspect * 1.05) : Math.min(1, aspect / 1.35));
    var al = el.getAttribute('data-alpha');
    goal.alpha = (al === null ? 0.9 : +al) * (narrow && pos !== 'center' ? 0.5 : 1);
    goal.tilt = look.tilt; goal.spin = look.spin;
  }
  function pick(){
    var vh = window.innerHeight, best = null, k;
    for (k = 0; k < marks.length; k++){
      var el = marks[k];
      if (!el.getClientRects().length) continue;
      if (el.getBoundingClientRect().top <= vh * 0.62) best = el; else if (best) break;
      if (!best) best = el;
    }
    if (best && best !== active) apply(best);
  }
  function resize(){
    var w = window.innerWidth, h = window.innerHeight, dpr = Math.min(window.devicePixelRatio || 1, 1.75);
    renderer.setPixelRatio(dpr); renderer.setSize(w, h, false);
    aspect = w / h; camera.aspect = aspect; camera.updateProjectionMatrix();
    uni.uPx.value = h / 900 * dpr;
    if (active) apply(active, true);
  }

  window.addEventListener('pointermove', function(e){
    if (e.pointerType === 'touch') return;
    pointer.x = (e.clientX / window.innerWidth) * 2 - 1; pointer.y = -((e.clientY / window.innerHeight) * 2 - 1); pointer.on = 1;
  }, {passive: true});
  root.addEventListener('mouseleave', function(){ pointer.on = 0; });
  window.addEventListener('resize', resize);
  new MutationObserver(setTheme).observe(root, {attributes: true, attributeFilter: ['data-theme']});

  var last = performance.now(), running = true, tmp = new THREE.Color();
  function frame(now){
    if (!running) return;
    requestAnimationFrame(frame);
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    var k = dt * 60, n3 = N * 3, j;
    pick();
    if (reduce){ cur.set(target); }
    else for (j = 0; j < n3; j++){ var r = rate[(j / 3) | 0] * k; cur[j] += (target[j] - cur[j]) * (r > 1 ? 1 : r); }
    posAttr.needsUpdate = true;

    if (!reduce) uni.uTime.value += dt;
    uni.uStir.value *= Math.pow(0.04, dt);
    var e = 1 - Math.pow(0.02, dt);
    pose.x += (goal.x - pose.x) * e; pose.y += (goal.y - pose.y) * e;
    pose.scale += (goal.scale - pose.scale) * e; pose.tilt += (goal.tilt - pose.tilt) * e;
    pose.alpha += (goal.alpha - pose.alpha) * e * 0.8;
    if (goal.spin && !reduce) pose.angle += dt * 0.16;
    else { var home = Math.round(pose.angle / (Math.PI * 2)) * Math.PI * 2; pose.angle += (home - pose.angle) * e * 0.8; }
    pointer.px += (pointer.x - pointer.px) * 0.06; pointer.py += (pointer.y - pointer.py) * 0.06;
    var sway = goal.spin || reduce ? 0 : Math.sin(uni.uTime.value * 0.35) * 0.16;
    cloud.rotation.set(pose.tilt - pointer.py * 0.14, pose.angle + sway + pointer.px * 0.22, 0);
    cloud.position.set(pose.x, pose.y, 0);
    cloud.scale.setScalar(pose.scale);
    uni.uAlpha.value = pose.alpha * (light ? 0.85 : 1);
    uni.uC1.value.lerp(tmp.copy(goal.c1), e); uni.uC2.value.lerp(tmp.copy(goal.c2), e);
    var m = uni.uMouse.value;
    m.x = pointer.px * HALF_H * aspect; m.y = pointer.py * HALF_H; m.z += ((reduce ? 0 : pointer.on) - m.z) * 0.08;
    renderer.render(scene, camera);
    if (!started){ started = true; root.classList.add('gl-on'); }
  }
  document.addEventListener('visibilitychange', function(){
    running = !document.hidden;
    if (running){ last = performance.now(); requestAnimationFrame(frame); }
  });

  collect(); resize(); setTheme();
  /* start scattered, then gather into the first shape */
  for (i = 0; i < N * 3; i++) cur[i] = (Math.random() - 0.5) * (i % 3 === 2 ? 6 : 12);
  pick();
  requestAnimationFrame(frame);
  window.LXScene = {refresh: collect};
})();
