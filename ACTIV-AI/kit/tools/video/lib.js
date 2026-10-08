// Bibliotecă comună pentru animațiile ACTIV AI (randare deterministă: window.render(t))
const PAL = {
  night: '#0F1720', slate: '#1B2733', petrol: '#0E7C86', violet: '#6E56CF', ocru: '#E2A62B',
  tigla: '#B9583A', var: '#F3EFE6', ceata: '#A9B4C0', zid: '#F5F1EA', red: '#E5484D'
};
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const inv = (a, b, x) => clamp((x - a) / (b - a));
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeIn = t => t * t * t;
const easeInOut = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const smooth = (a, b, x) => { const t = inv(a, b, x); return t * t * (3 - 2 * t); };
function rng(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; }; }
function hexToRgb(h) { if (h.startsWith('rgb')) return h.match(/[\d.]+/g).slice(0, 3).map(Number); h = h.replace('#', '');return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
function mix(c1, c2, t) { const a = hexToRgb(c1), b = hexToRgb(c2); return `rgb(${Math.round(lerp(a[0], b[0], t))},${Math.round(lerp(a[1], b[1], t))},${Math.round(lerp(a[2], b[2], t))})`; }
function rgba(h, a) { const c = hexToRgb(h); return `rgba(${c[0]},${c[1]},${c[2]},${a})`; }

function setupCanvas(W = 1920, H = 1080) {
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  c.style.position = 'fixed'; c.style.left = '0'; c.style.top = '0';
  document.body.style.margin = '0'; document.body.style.background = '#000'; document.body.style.overflow = 'hidden';
  document.body.appendChild(c); return c.getContext('2d');
}

function text(ctx, s, x, y, o = {}) {
  ctx.save();
  ctx.globalAlpha = o.alpha == null ? 1 : o.alpha;
  ctx.fillStyle = o.color || PAL.var;
  ctx.font = `${o.weight || 400} ${o.size || 40}px ${o.family || 'Inter'}`;
  ctx.textAlign = o.align || 'left'; ctx.textBaseline = o.base || 'alphabetic';
  if (o.shadow) { ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = o.shadow; ctx.shadowOffsetY = 2; }
  if (o.maxW) {
    const words = s.split(' '); let line = '', yy = y; const lh = o.lh || (o.size || 40) * 1.3; const lines = [];
    for (const w of words) { const test = line ? line + ' ' + w : w; if (ctx.measureText(test).width > o.maxW && line) { lines.push(line); line = w; } else line = test; }
    if (line) lines.push(line);
    for (const l of lines) { ctx.fillText(l, x, yy); yy += lh; }
    ctx.restore(); return lines.length;
  }
  ctx.fillText(s, x, y); ctx.restore(); return 1;
}
function serif(ctx, s, x, y, o = {}) { return text(ctx, s, x, y, Object.assign({ family: 'Noto Serif', weight: 700 }, o)); }

function footer(ctx, W, H, code, light) {
  ctx.save();
  const col = light ? 'rgba(15,23,32,.75)' : 'rgba(169,180,192,.9)';
  text(ctx, 'ACTIV AI · Sibiul meu · Artefact-model generat cu AI', 40, H - 28, { size: 20, color: col });
  text(ctx, code + ' · #SibiulMeu', W - 40, H - 28, { size: 20, color: light ? 'rgba(15,23,32,.75)' : PAL.ocru, align: 'right', weight: 600 });
  ctx.restore();
}
function chip(ctx, label, x, y, color) {
  ctx.save(); ctx.font = '700 20px Inter'; const w = ctx.measureText(label).width + 36;
  ctx.fillStyle = color; roundRect(ctx, x, y, w, 40, 20); ctx.fill();
  ctx.fillStyle = PAL.night; ctx.textBaseline = 'middle'; ctx.fillText(label, x + 18, y + 21); ctx.restore(); return w;
}
function roundRect(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }

// Lucarnă „ochi” (pleoapă) – open: 0..1 (clipire), glow: lumină la geam
function eye(ctx, x, y, w, roof, o = {}) {
  const h = w * 0.42, open = o.open == null ? 1 : o.open;
  ctx.save(); ctx.translate(x, y);
  ctx.fillStyle = roof; // pleoapa
  ctx.beginPath(); ctx.moveTo(-w / 2 - w * .25, h * .25); ctx.quadraticCurveTo(0, -h * 1.15, w / 2 + w * .25, h * .25); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = 'rgba(0,0,0,.25)'; ctx.lineWidth = Math.max(1, w * .04); ctx.stroke();
  // fanta
  const sh = h * .55 * open + 0.6;
  ctx.fillStyle = o.glow ? mix('#2a1d10', '#FFD27A', o.glow) : '#1a1410';
  ctx.beginPath(); ctx.ellipse(0, h * .05, w * .36, sh / 2, 0, Math.PI, 0); ctx.lineTo(w * .36, h * .05); ctx.closePath(); ctx.fill();
  if (o.glow && o.glow > .05) { ctx.globalAlpha = o.glow * .35; ctx.fillStyle = '#FFD27A'; ctx.beginPath(); ctx.ellipse(0, h * .05, w * .7, h * .6, 0, 0, Math.PI * 2); ctx.fill(); }
  ctx.restore();
}

// Rând de case cu acoperișuri abrupte și „ochi”
function houses(ctx, o) {
  const r = rng(o.seed || 7); const { y0, W } = o; let x = o.x0 == null ? -40 : o.x0;
  const out = [];
  while (x < W + 60) {
    const w = 120 + r() * 150, wallH = (o.wallH || 150) * (0.8 + r() * .5), roofH = w * (0.75 + r() * .35);
    const wallC = o.walls[Math.floor(r() * o.walls.length)], roofC = o.roofs[Math.floor(r() * o.roofs.length)];
    out.push({ x, w, wallH, roofH, wallC, roofC, r1: r(), r2: r(), r3: r() });
    x += w - 2;
  }
  for (const hs of out) {
    const { x, w, wallH, roofH } = hs, base = y0;
    ctx.fillStyle = o.tint ? mix(hs.wallC, o.tint, o.tintAmt) : hs.wallC;
    ctx.fillRect(x, base - wallH, w, wallH + 400);
    // ferestre
    const cols = Math.max(2, Math.floor(w / 55)), rows = Math.max(1, Math.floor(wallH / 70));
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
      const wx = x + (i + .5) * w / cols - 11, wy = base - wallH + 26 + j * 66;
      const lit = o.night && ((hs.r1 * 13 + i * 7 + j * 3) % 10) / 10 < o.night * 0.75;
      ctx.fillStyle = lit ? '#FFD27A' : (o.winC || 'rgba(20,24,30,.55)');
      ctx.fillRect(wx, wy, 22, 34);
    }
    // acoperiș
    const rc = o.tint ? mix(hs.roofC, o.tint, o.tintAmt) : hs.roofC;
    ctx.fillStyle = rc;
    ctx.beginPath(); ctx.moveTo(x - 6, base - wallH); ctx.lineTo(x + w / 2, base - wallH - roofH); ctx.lineTo(x + w + 6, base - wallH); ctx.closePath(); ctx.fill();
    // zăpadă
    if (o.snow > 0) {
      ctx.fillStyle = rgba('#FFFFFF', .92);
      const sh = roofH * .22 * o.snow;
      ctx.beginPath(); ctx.moveTo(x + w / 2, base - wallH - roofH - 2);
      ctx.lineTo(x + w / 2 + (w / 2) * (sh / roofH) * 2.2, base - wallH - roofH + sh * 2.2);
      ctx.quadraticCurveTo(x + w / 2, base - wallH - roofH + sh * 1.4, x + w / 2 - (w / 2) * (sh / roofH) * 2.2, base - wallH - roofH + sh * 2.2);
      ctx.closePath(); ctx.fill();
      ctx.fillRect(x - 6, base - wallH - 4, w + 12, 6 * o.snow);
    }
    // ochi
    const nEyes = w > 190 ? 2 : 1;
    for (let k = 0; k < nEyes; k++) {
      const ex = x + w / 2 + (nEyes === 2 ? (k ? 1 : -1) * w * .17 : 0), ey = base - wallH - roofH * (nEyes === 2 ? .3 : .45);
      const blinkPhase = ((o.t || 0) * 0.37 + hs.r2 * 9 + k * 3.1) % 6;
      const open = blinkPhase < 0.18 ? Math.abs(blinkPhase - 0.09) / 0.09 : 1;
      eye(ctx, ex, ey, w * .2, mix(rc, '#000000', .18), { open, glow: o.night ? o.night * (hs.r3 > .4 ? 1 : .2) : 0 });
    }
  }
  return out;
}

// Turn cu acoperiș piramidal și turnulețe (siluetă generică)
function tower(ctx, x, base, w, h, o = {}) {
  ctx.save();
  const wall = o.wall || '#E9DCC3', roof = o.roof || '#5B3A2E';
  ctx.fillStyle = o.tint ? mix(wall, o.tint, o.tintAmt) : wall;
  ctx.fillRect(x - w / 2, base - h, w, h + 400);
  ctx.fillStyle = 'rgba(0,0,0,.18)'; ctx.fillRect(x + w * .18, base - h, w * .32, h + 400);
  // ferestre / ceas
  ctx.fillStyle = 'rgba(20,24,30,.7)';
  for (let i = 0; i < 4; i++) { ctx.fillRect(x - 8, base - h + 70 + i * (h - 140) / 4, 16, 34); }
  if (o.clock) { ctx.fillStyle = '#F3EFE6'; ctx.beginPath(); ctx.arc(x, base - h + 40, w * .18, 0, 7); ctx.fill(); ctx.strokeStyle = '#333'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, base - h + 40); ctx.lineTo(x, base - h + 40 - w * .13); ctx.moveTo(x, base - h + 40); ctx.lineTo(x + w * .09, base - h + 40); ctx.stroke(); }
  const rc = o.tint ? mix(roof, o.tint, o.tintAmt) : roof;
  ctx.fillStyle = rc;
  const rh = o.roofH || w * 1.8;
  ctx.beginPath(); ctx.moveTo(x - w / 2 - 8, base - h); ctx.lineTo(x, base - h - rh); ctx.lineTo(x + w / 2 + 8, base - h); ctx.closePath(); ctx.fill();
  // turnulețe de colț
  for (const s of [-1, 1]) {
    const tx = x + s * (w / 2 + 2);
    ctx.fillStyle = rc; ctx.beginPath(); ctx.moveTo(tx - 12, base - h); ctx.lineTo(tx, base - h - rh * .32); ctx.lineTo(tx + 12, base - h); ctx.closePath(); ctx.fill();
  }
  if (o.snow > 0) { ctx.fillStyle = 'rgba(255,255,255,.9)'; ctx.beginPath(); ctx.moveTo(x, base - h - rh); ctx.lineTo(x + 14 * o.snow, base - h - rh + 40 * o.snow); ctx.lineTo(x - 14 * o.snow, base - h - rh + 40 * o.snow); ctx.closePath(); ctx.fill(); }
  ctx.restore();
}

function mountains(ctx, W, y, col, seed = 3, amp = 120) {
  const r = rng(seed); ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(0, y + 200);
  let x = 0; ctx.lineTo(0, y);
  while (x <= W) { x += 60 + r() * 120; ctx.lineTo(x, y - r() * amp); }
  ctx.lineTo(W, y + 400); ctx.lineTo(0, y + 400); ctx.closePath(); ctx.fill();
}

// Cer în funcție de ora zilei (0..1, 0.5 = amiază) și sezon
function sky(ctx, W, H, day, season) {
  // day: 0 miezul nopții, .25 răsărit, .5 amiază, .75 apus
  const sun = Math.sin((day - .25) * Math.PI * 2); // -1..1
  const light = clamp((sun + .25) / 1.0);
  const dusk = clamp(1 - Math.abs(sun) * 3.5) * (sun > -0.3 ? 1 : 0);
  const topDay = ['#7FB8E6', '#5EA8E8', '#8FB3CF', '#A8BCD0'][season], botDay = ['#CFE8F5', '#BFE3FA', '#E8D6B8', '#E6ECF1'][season];
  const top = mix(mix('#0A1020', topDay, light), '#3B2A5A', dusk * .5);
  const bot = mix(mix('#16223A', botDay, light), '#F2A65A', dusk * .85);
  const g = ctx.createLinearGradient(0, 0, 0, H * .75); g.addColorStop(0, top); g.addColorStop(1, bot);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  return { light, dusk, sun };
}
function stars(ctx, W, H, a, seed = 11) {
  if (a <= 0) return; const r = rng(seed); ctx.fillStyle = `rgba(255,255,255,${a})`;
  for (let i = 0; i < 160; i++) { const s = r() * 2 + .4; ctx.fillRect(r() * W, r() * H * .55, s, s); }
}
window.READY = false;
