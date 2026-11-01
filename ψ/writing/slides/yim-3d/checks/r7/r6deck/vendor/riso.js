/* Rikyu Riso: a risograph print pass for three.js slide scenes. slide-kit/riso/riso.js, v1.0.0, 2026-11-01.
 * Written by Osaa (Oracle AI) for Rikyu Labs. Vanilla classic script, no build step: load three r169 as a classic
 * script first (window.THREE, e.g. three.iife.js), then this file. It defines window.RikyuRiso.
 *
 * What it does. Your scene is rendered into an "ink separation" target: R = ink 1 (kuro), G = ink 2 (sabi),
 * B = ink 3 (moss), where 1 = no ink. One full-screen pass prints it like a risograph: each ink has its own
 * threshold curve, its own Bayer lattice offset and its own misregistration; inks multiply on shiro paper;
 * solid ink has speckle and drum starve; an optional flood ink fills the whole sheet (a sabi page).
 * Words are knocked out: no ink is printed within `pad` px of any box you pass to knockout().
 *
 * Moire rule (why the canvas is sized the way it is). The canvas backing store is always sized to the device
 * pixels the stage covers on screen, the canvas is a fixed layer outside any CSS transform (see place()),
 * and the dither cell is a whole number of device pixels:
 *   cell = max(2, round(cellAt1920 * devicePxPerStagePx)).  1920 wide at dpr 1 -> 4, 1280 -> 3, 3840 -> 8.
 * The browser never resamples the dots, so the dots cannot beat against the screen grid. Only a projector or
 * capture box that rescales the whole output can still add moire; a bigger cell is the remedy there.
 *
 * Credits. Ordered-dither threshold idea after niccolofanton/dithering-shader (MIT, Copyright (c) 2023-2024
 * Niccolo Fanton; original dither pattern by Klems, shadertoy.com/view/ltSSzW). This file computes an 8x8 Bayer
 * value by bit interleave instead of the repo's 4x4 table; ink separation, paper, knockout, flood and
 * misregistration are ours (Rikyu Labs, MIT).
 */
(function (root) {
  'use strict';
  const VERSION = '1.0.0';
  const MAXB = 64;                        // knockout boxes per frame

  // resolve any CSS colour (hex, var() already resolved, oklch, color-mix) to sRGB 0..1 via a 1px canvas
  const probe = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  function rgb(value) {
    if (!value) throw new Error('RikyuRiso: empty colour');
    probe.clearRect(0, 0, 1, 1); probe.fillStyle = '#000'; probe.fillStyle = value.trim();
    probe.fillRect(0, 0, 1, 1); const d = probe.getImageData(0, 0, 1, 1).data;
    return [d[0] / 255, d[1] / 255, d[2] / 255];
  }
  function token(styles, name) {
    const v = styles.getPropertyValue(name).trim();
    if (!v) throw new Error('RikyuRiso: missing token ' + name + ' (load riso.css after the Rikyu tokens)');
    return rgb(v);
  }

  /* Ink vector convention, used everywhere: [ink1, ink2, ink3] = how much of each ink the lit face carries,
   * 0..1. [0.22,0,0] = a kuro block, [0,0.5,0] = a sabi block, [0.1,0.4,0] = sabi overprinted with a little kuro.
   * Shadowed faces print darker automatically. Use INK.* for the house blocks. */
  const INK = { kuro: [0.22, 0, 0], kuroLight: [0.08, 0, 0], sabi: [0, 0.52, 0], moss: [0, 0, 0.62], mossLight: [0, 0, 0.16], none: [0, 0, 0] };

  function create(o) {
    const T = root.THREE;
    if (!T || !T.WebGLRenderer) throw new Error('RikyuRiso: three.js r169 (window.THREE) is required');
    o = o || {};
    const W = o.width || 1920, H = o.height || 1080;
    const canvas = o.canvas, stage = o.stage || canvas.parentElement;
    const styles = getComputedStyle(o.tokens || document.documentElement);
    const paper = token(styles, '--riso-paper');
    const inks = ['--riso-ink-1', '--riso-ink-2', '--riso-ink-3'].map(n => token(styles, n));
    const flood = token(styles, '--riso-flood');
    // density > 1 deepens a light ink so a 50% dither still reads from the back of a room; hue is kept
    const density = o.density || [1, 1.6, 1.15];
    const printed = inks.map((c, k) => c.map((v, j) => Math.min(1, paper[j] * Math.pow(v / paper[j], density[k]))));
    const cellAt1920 = o.cell || 4;
    const misStage = o.misregistration || [[0, 0], [2, -1], [-1, 2]];   // stage px, rounded to device px
    const lattice = o.lattice || [[0, 0], [3, 5], [5, 2]];               // Bayer offsets in cells
    const curve = o.thresholds || [[0.06, 0.92], [0.04, 0.82], [0.05, 0.88]];
    const forced = o.forceOutput || null;    // {w,h}: debug only, e.g. the moire negative control

    const renderer = new T.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: 'high-performance', preserveDrawingBuffer: !!o.preserveDrawingBuffer });
    const gl = renderer.getContext(); if (!gl) throw new Error('RikyuRiso: no WebGL');
    renderer.setPixelRatio(1);
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap;

    // ---------- scene: orthographic isometric camera, one sun, a ground that only takes ink in shadow ----------
    const scene = new T.Scene(); scene.background = new T.Color(1, 1, 1);
    const camera = new T.OrthographicCamera(-W / 2, W / 2, H / 2, -H / 2, 1, 8000);
    // r169 Lambert = colour / PI * irradiance, so both lights carry PI and a lit face comes out near 1
    scene.add(new T.AmbientLight(0xffffff, 0.28 * Math.PI));
    const sun = new T.DirectionalLight(0xffffff, 0.92 * Math.PI); sun.castShadow = true;
    sun.shadow.mapSize.set(o.shadowSize || 2048, o.shadowSize || 2048);
    Object.assign(sun.shadow.camera, { left: -1600, right: 1600, top: 1600, bottom: -1600, near: 10, far: 6000 });
    sun.shadow.bias = -0.0006; sun.shadow.normalBias = 1.5; sun.shadow.radius = 2;
    scene.add(sun); scene.add(sun.target);
    const ground = new T.Mesh(new T.PlaneGeometry(12000, 12000),
      new T.MeshLambertMaterial({ color: new T.Color(0.62, 0, 0), emissive: new T.Color(0.40, 1, 1) }));
    ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

    function pose(p, cam) {               // {az, el, zoom, target:[x,z]} -> camera
      cam = cam || camera; const az = p.az ?? Math.PI / 4, el = p.el ?? 0.58, D = 2600, tx = (p.target || [0, 0])[0], tz = (p.target || [0, 0])[1];
      cam.position.set(tx + Math.cos(el) * Math.cos(az) * D, Math.sin(el) * D, tz + Math.cos(el) * Math.sin(az) * D);
      cam.zoom = p.zoom || 1; cam.lookAt(tx, 0, tz); cam.updateProjectionMatrix(); cam.updateMatrixWorld(); return cam;
    }
    function poseCamera(p) { return pose(p, camera.clone()); }
    pose(o.pose || {});
    function sunAt(az, el) { el = el ?? 0.75; sun.position.set(Math.cos(az) * Math.cos(el) * 2200, Math.sin(el) * 2200, Math.sin(az) * Math.cos(el) * 2200); sun.target.position.set(0, 0, 0); }
    sunAt(-0.95);

    // stage pixel (y down) -> point on the ground, for a given camera pose. Orthographic, so the map is affine:
    // groundMap(cam) returns a fast function built from three rays.
    const ray = new T.Raycaster(), plane = new T.Plane(new T.Vector3(0, 1, 0), 0);
    function onGround(sx, sy, cam) {
      ray.setFromCamera(new T.Vector2(sx / (W / 2) - 1, 1 - sy / (H / 2)), cam || camera);
      const v = new T.Vector3(); ray.ray.intersectPlane(plane, v); return v;
    }
    function groundMap(cam) {
      const a = onGround(0, 0, cam), b = onGround(1000, 0, cam), c = onGround(0, 1000, cam);
      const ux = (b.x - a.x) / 1000, uz = (b.z - a.z) / 1000, vx = (c.x - a.x) / 1000, vz = (c.z - a.z) / 1000;
      return (sx, sy) => ({ x: a.x + ux * sx + vx * sy, z: a.z + uz * sx + vz * sy });
    }

    // ---------- blocks: one InstancedMesh, per-instance ink, separation shading ----------
    function sepMaterial() {
      const m = new T.MeshLambertMaterial({ color: 0xffffff });
      m.onBeforeCompile = sh => {
        sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute vec3 aInk;\nvarying vec3 vInk;')
          .replace('#include <begin_vertex>', '#include <begin_vertex>\n  vInk = aInk;');
        sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vInk;')
          .replace('#include <opaque_fragment>',
            'float shade = clamp(outgoingLight.r, 0., 1.);\n' +
            'vec3 used = step(vec3(.0005), vInk);\n' +
            'gl_FragColor = vec4(1. - used * (1. - (1. - vInk) * shade), 1.);');
      };
      return m;
    }
    const box = new T.BoxGeometry(1, 1, 1); box.translate(0, 0.5, 0);   // origin at the bottom face
    const dummy = new T.Object3D();
    function blocks(n) {
      const g = box.clone(); const ink = new T.InstancedBufferAttribute(new Float32Array(n * 3), 3);
      ink.setUsage(T.DynamicDrawUsage); g.setAttribute('aInk', ink);
      const mesh = new T.InstancedMesh(g, sepMaterial(), n);
      mesh.instanceMatrix.setUsage(T.DynamicDrawUsage); mesh.castShadow = true; mesh.receiveShadow = true; mesh.frustumCulled = false;
      scene.add(mesh);
      return {
        mesh, count: n,
        // p = {x, z, y (base height), w, h, d, ry, ink:[k,s,m]}; sizes in world units (about stage px at zoom 1)
        set(i, p) {
          const w = Math.max(p.w, 1e-3), h = Math.max(p.h, 1e-3), d = Math.max(p.d ?? p.w, 1e-3);
          dummy.position.set(p.x, p.y || 0, p.z); dummy.rotation.set(0, p.ry || 0, 0); dummy.scale.set(w, h, d);
          dummy.updateMatrix(); mesh.setMatrixAt(i, dummy.matrix);
          const k = p.ink || INK.kuro; ink.setXYZ(i, k[0], k[1], k[2]);
        },
        hide(i) { dummy.position.set(0, -10, 0); dummy.scale.set(1e-3, 1e-3, 1e-3); dummy.updateMatrix(); mesh.setMatrixAt(i, dummy.matrix); },
        commit() { mesh.instanceMatrix.needsUpdate = true; ink.needsUpdate = true; },
      };
    }

    // ---------- print pass ----------
    const quadMat = new T.ShaderMaterial({
      depthTest: false, depthWrite: false,
      uniforms: {
        tSep: { value: null }, uRes: { value: new T.Vector2() }, uSep: { value: new T.Vector2() }, uCell: { value: 4 }, uScale: { value: 1 },
        uMis: { value: [new T.Vector2(), new T.Vector2(), new T.Vector2()] }, uLat: { value: lattice.map(v => new T.Vector2(...v)) },
        uLo: { value: new T.Vector3(...curve.map(c => c[0])) }, uHi: { value: new T.Vector3(...curve.map(c => c[1])) },
        uInk1: { value: new T.Vector3(...printed[0]) }, uInk2: { value: new T.Vector3(...printed[1]) }, uInk3: { value: new T.Vector3(...printed[2]) },
        uPaper: { value: new T.Vector3(...paper) }, uFloodInk: { value: new T.Vector3(...flood) }, uFlood: { value: 0 },
        uGrain: { value: o.grain === false ? 0 : 1 }, uMask: { value: 1 }, uPad: { value: 40 },
        uBox: { value: Array.from({ length: MAXB }, () => new T.Vector4(-9, -9, -9, -9)) }, uNB: { value: 0 },
      },
      vertexShader: 'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}',
      fragmentShader: `precision highp float;
varying vec2 vUv;
uniform sampler2D tSep; uniform vec2 uRes, uSep; uniform float uCell, uScale, uFlood, uGrain, uMask, uPad;
uniform vec2 uMis[3]; uniform vec2 uLat[3]; uniform vec3 uLo, uHi, uInk1, uInk2, uInk3, uPaper, uFloodInk;
uniform vec4 uBox[${MAXB}]; uniform int uNB;
float hh(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float vn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hh(i),hh(i+vec2(1,0)),f.x),mix(hh(i+vec2(0,1)),hh(i+vec2(1,1)),f.x),f.y);}
// 8x8 Bayer threshold by bit interleave: 2x2 core m(x,y) = (2x + 3y) mod 4
float bayer8(vec2 p){p=mod(floor(p),8.);float v=0.,w=16.;
  for(int i=0;i<3;i++){vec2 b=mod(p,2.);v+=w*mod(2.*b.x+3.*b.y,4.);p=floor(p/2.);w/=4.;}
  return (v+.5)/64.;}
// knockout: 1 = free paper, 0 = inside or within uPad of a word box (boxes in stage px, y down)
float clearAt(vec2 sp){ if(uMask<.5) return 1.; float m=1.;
  for(int i=0;i<${MAXB};i++){ if(i>=uNB) break; vec4 b=uBox[i];
    float d=length(max(vec2(b.x-sp.x, b.y-sp.y), max(vec2(0.), vec2(sp.x-b.z, sp.y-b.w))));
    m=min(m, smoothstep(0., uPad, d)); }
  return m; }
float ink(vec3 sep, int ch, vec2 f, vec2 lat, float lo, float hi, float clr){
  float v = ch==0 ? sep.r : ch==1 ? sep.g : sep.b;
  float d = clamp(((1.-v)-lo)/(hi-lo),0.,1.) * clr;
  float on = step(bayer8(floor(f/uCell)+lat), d) * step(.001, d);
  float hole = uGrain * step(.965, hh(floor(f/max(1.,floor(uCell/3.)))+float(ch)*7.1));
  float starve = mix(1., .88+.12*vn(f/uScale*vec2(.012,.11)+float(ch)*13.), uGrain);
  return on*(1.-hole)*starve; }
// f is a device pixel with y down; texel (cx, cy) of the separation is cell (cx, cy) counted from the top left
vec3 sampleSep(vec2 f){ vec2 cell=floor(f/uCell); return texture2D(tSep, vec2((cell.x+.5)/uSep.x, 1.-(cell.y+.5)/uSep.y)).rgb; }
float plate(int ch, vec2 frag, vec2 mis, vec2 lat, float lo, float hi){
  vec2 f=frag+mis; vec2 c=(floor(f/uCell)+.5)*uCell;
  return ink(sampleSep(f), ch, f, lat, lo, hi, clearAt(c/uScale)); }
void main(){
  vec2 frag = vec2(floor(vUv.x*uRes.x), uRes.y-1.-floor(vUv.y*uRes.y));   // device pixel, y down
  float k = plate(0, frag, uMis[0], uLat[0], uLo.x, uHi.x);
  float s = plate(1, frag, uMis[1], uLat[1], uLo.y, uHi.y);
  float m = plate(2, frag, uMis[2], uLat[2], uLo.z, uHi.z);
  // flood ink: a whole-sheet solid that fills in by dither as uFlood goes 0 -> 1
  float fl = step(bayer8(floor(frag/uCell)+vec2(6.,1.)), uFlood*1.02) * step(.001,uFlood);
  fl *= mix(1., .9+.1*vn(frag/uScale*vec2(.01,.09)+31.), uGrain);
  vec2 sp = frag/uScale;
  float fib = vn(vec2(sp.x*.6, sp.y*.04))*.5 + vn(sp*.02)*.5;
  vec3 paper = uPaper*(1.-uGrain*((fib-.5)*.025+(hh(frag)-.5)*.02));
  vec3 c = paper * mix(vec3(1.), uFloodInk/uPaper, fl);
  c *= mix(vec3(1.), uInk2/uPaper, s) * mix(vec3(1.), uInk3/uPaper, m) * mix(vec3(1.), uInk1/uPaper, k*.97);
  vec2 q=vUv-.5; c *= 1.-dot(q,q)*.08*uGrain;
  gl_FragColor = vec4(c,1.);
}`,
    });
    const quad = new T.Mesh(new T.PlaneGeometry(2, 2), quadMat);
    const qScene = new T.Scene(); qScene.add(quad); const qCam = new T.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    let sep = null, outW = 0, outH = 0, cell = 4, scale = 1;
    function resize() {
      // device pixels the stage covers: the canvas backing store matches them 1:1 (the moire rule)
      const r = stage.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
      const w = forced ? forced.w : Math.max(2, Math.round(r.width * dpr)), h = forced ? forced.h : Math.max(2, Math.round(w * H / W));
      if (w === outW && h === outH && sep) { place(r, dpr); return info(); }
      outW = w; outH = h; scale = outW / W;
      cell = Math.max(2, Math.round(cellAt1920 * scale));
      renderer.setSize(outW, outH, false);
      place(r, dpr);
      if (sep) sep.dispose();
      const sw = Math.ceil(outW / cell) + 1, sh = Math.ceil(outH / cell) + 1;
      sep = new T.WebGLRenderTarget(sw, sh, { minFilter: T.NearestFilter, magFilter: T.NearestFilter });
      quadMat.uniforms.tSep.value = sep.texture;
      quadMat.uniforms.uRes.value.set(outW, outH); quadMat.uniforms.uSep.value.set(sw, sh);
      quadMat.uniforms.uCell.value = cell; quadMat.uniforms.uScale.value = scale; quadMat.uniforms.uPad.value = 40;
      misStage.forEach((v, k) => quadMat.uniforms.uMis.value[k].set(Math.round(v[0] * scale), Math.round(v[1] * scale)));
      return info();
    }
    // The canvas must not sit inside a CSS-transformed element: Chrome filters a transformed canvas even at an exact
    // 1:1 size (measured 2026-11-01 at 1280x720: dots came out 2 px plus a grey edge pixel). So the canvas is a fixed
    // layer under the stage, sized in CSS px to outW / dpr and placed on the stage's whole-device-pixel origin.
    function place(r, dpr) {
      if (o.place === false) return;
      const cs = canvas.style; cs.position = 'fixed'; cs.zIndex = '0'; cs.pointerEvents = 'none';
      cs.left = Math.round(r.left * dpr) / dpr + 'px'; cs.top = Math.round(r.top * dpr) / dpr + 'px';
      cs.width = (forced ? r.width : outW / dpr) + 'px'; cs.height = (forced ? r.height : outH / dpr) + 'px';
    }
    function info() { return { outW, outH, cell, scale, canvasW: canvas.width, canvasH: canvas.height, version: VERSION }; }

    // knockout boxes in stage px: [{l,t,r,b}] (pad applies to all, default 40)
    function knockout(boxes, pad) {
      const u = quadMat.uniforms; const n = Math.min(MAXB, boxes.length);
      for (let i = 0; i < MAXB; i++) { const b = boxes[i]; if (i < n) u.uBox.value[i].set(b.l, b.t, b.r, b.b); else u.uBox.value[i].set(-9, -9, -9, -9); }
      u.uNB.value = n; if (pad != null) u.uPad.value = pad * 1;   // pad in stage px
      if (boxes.length > MAXB) console.warn('RikyuRiso: ' + boxes.length + ' knockout boxes, only ' + MAXB + ' used');
    }
    // measure word boxes under root (stage px). The stage may be CSS-scaled; we divide the scale out.
    function measureKnockout(rootEl, selector) {
      const sr = stage.getBoundingClientRect(), sc = sr.width / W;
      return [...rootEl.querySelectorAll(selector || 'h1,h2,h3,p,li,.label,.num,svg text')].filter(e => e.getClientRects().length).map(e => {
        const b = e.getBoundingClientRect(); return { l: (b.left - sr.left) / sc, t: (b.top - sr.top) / sc, r: (b.right - sr.left) / sc, b: (b.bottom - sr.top) / sc };
      });
    }

    // one frame: scene -> separation (cell resolution) -> print (device resolution)
    // slip 0..1 moves inks 2 and 3 out of register (use it during a page change); flood 0..1 fills the sheet
    function render(opt) {
      opt = opt || {}; if (!sep) resize();
      const u = quadMat.uniforms, sl = opt.slip || 0;
      u.uMis.value[1].set(Math.round((misStage[1][0] + sl * 3) * scale), Math.round((misStage[1][1] + sl) * scale));
      u.uMis.value[2].set(Math.round((misStage[2][0] - sl) * scale), Math.round((misStage[2][1] - sl * 3) * scale));
      u.uFlood.value = opt.flood || 0; u.uMask.value = opt.mask === false ? 0 : 1;
      // the separation covers (sw*cell) x (sh*cell) device px from the top left, so one texel is one cell exactly
      const sw = u.uSep.value.x, sh = u.uSep.value.y;
      camera.setViewOffset(outW, outH, 0, 0, sw * cell, sh * cell);
      renderer.setRenderTarget(sep); renderer.render(scene, camera);
      camera.clearViewOffset();
      renderer.setRenderTarget(null); renderer.render(qScene, qCam);
    }

    resize();
    return {
      THREE: T, renderer, scene, camera, sun, ground, blocks, pose, poseCamera, sunAt, onGround, groundMap,
      knockout, measureKnockout, render, resize, info, INK,
      rendererName() { const e = gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER); },
    };
  }

  /* ---------- formation helpers: pure functions, world units, centred on (0,0); add your anchor ---------- */
  const rnd = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
  const formations = {
    // a block field: `count` cells on a cols-wide grid, a few cells skipped so it does not read as a spreadsheet.
    // pick(n, seed) chooses n distinct indexes (the "17 of 211" moment).
    field({ count, cols, spacing }) {
      const rows = Math.ceil(count / cols) + 1, total = cols * rows, cells = [];
      for (let i = 0; i < total && cells.length < count; i++) {
        const c = i % cols, r = Math.floor(i / cols);
        if ((c + r * 7) % 16 === 5 && cells.length + (total - i) > count) continue;
        cells.push({ dx: (c - (cols - 1) / 2) * spacing, dz: (r - (Math.ceil(count / cols) - 1) / 2) * spacing, c, r });
      }
      return cells;
    },
    pick(n, of, seed) { const s = new Set(); let k = 0; while (s.size < Math.min(n, of)) s.add(Math.floor(rnd(k++ + (seed || 900), 4) * of)); return s; },
    // a stack: n slabs on top of a base, each a little smaller, swaying with t (the bottleneck tower)
    stack({ n, base, slab, width, shrink, t }) {
      let y = base; const out = [];
      for (let k = 0; k < n; k++) { const sway = Math.sin((t || 0) * 1.1 + k * 0.5) * k * 1.6;
        out.push({ dx: sway + k * 2.2, dz: -k * 1.4, y, w: width - k * (shrink ?? 2), h: slab, ry: Math.sin((t || 0) * 0.7 + k) * 0.09 }); y += slab; }
      return out;
    },
    // a ring: n points on an ellipse (rx along world x, rz along world z), turning with phase
    ring({ n, rx, rz, phase }) {
      return Array.from({ length: n }, (_, k) => { const a = -Math.PI / 2 + k * Math.PI * 2 / n + (phase || 0);
        return { dx: Math.cos(a) * rx, dz: Math.sin(a) * (rz ?? rx), a }; });
    },
    rnd,
  };
  const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
  const back = x => { x = Math.max(0, Math.min(1, x)); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

  root.RikyuRiso = { VERSION, create, formations, INK, ease, back, rgb };
})(window);
