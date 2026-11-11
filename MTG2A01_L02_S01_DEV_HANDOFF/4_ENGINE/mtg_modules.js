/* =====================================================================================
   [MTG2A01] MTG2A01_L02_S01 «टप्पू मेंढक की कूद» — lesson modules (additive)
   BRIDGE_TEACH · JUMP_PICK · SEQ_FILL · SPACE_PODS
   Registered into the engine's SlideModules; nothing existing is changed. Every module owns its
   audio (state.ownsAudio) and runs on a mount token, so leaving a slide cancels its timeline.
   CSS lives in mtg_styles.css (scoped under .mtg-*, .br-*, .jp-*, .sf-*, .sp-*).
   ===================================================================================== */
let _mtgTok = 0;
const MTG_STOP = "__mtg_stop__";
function mtgToken(){ return ++_mtgTok; }
function mtgAlive(tok){ if(tok !== _mtgTok) throw MTG_STOP; }
function mtgWait(ms, tok){ return new Promise((res, rej)=> setTimeout(()=> (tok === _mtgTok ? res() : rej(MTG_STOP)), ms)); }
function mtgSrc(id){ if(!id) return null; return (CARD.assets && CARD.assets.audio && CARD.assets.audio[id]) || ("assets/Audio/" + id + "." + AUDIO_EXT); }
function mtgText(id){ return (CARD.assets && CARD.assets.audio_text && CARD.assets.audio_text[id]) || ""; }
function mtgSay(id, tok){ return new Promise((res, rej)=> play(mtgSrc(id), ()=> (tok === _mtgTok ? res() : rej(MTG_STOP)))); }
function mtgRun(fn){ fn().catch(e => { if(e !== MTG_STOP) console.error("[mtg]", e); }); }
function mtgEl(tag, cls, html){ const e = document.createElement(tag); if(cls) e.className = cls; if(html != null) e.innerHTML = html; return e; }
/* file4's right / wrong feedback recordings (sfx_fb_*), with the engine's synthesised tone as the
   fallback; the lesson music steps back while they sound, as file4's sfxFile does */
function mtgFx(name, fallback, vol){
  try{
    const a = new Audio((typeof _av === "function") ? _av("assets/Audio/" + name + "." + AUDIO_EXT) : "assets/Audio/" + name + "." + AUDIO_EXT);
    a.volume = (vol != null) ? vol : 0.55;
    if(window.__lessonBgm && window.__lessonBgm.track) window.__lessonBgm.track(a);
    a.play().catch(()=>{ if(fallback) fallback(); });
  }catch(e){ if(fallback) fallback(); }
}
const mtgRight = ()=> mtgFx("sfx_fb_correct", ()=>{ if(typeof sfxCorrect === "function") sfxCorrect(); });
const mtgWrong = ()=> mtgFx("sfx_fb_incorrect", ()=>{ if(typeof sfxWrongSoft === "function") sfxWrongSoft(); });
function mtgImg(key){ return "assets/Images/" + key + ".webp"; }
function mtgOst(t){ const p = $("promptText"); if(p && t != null) p.textContent = t; }
function mtgPulse(el, cls, ms){ if(!el) return; el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); if(ms) setTimeout(()=> el.classList.remove(cls), ms); }
const MTG_SVG = "http://www.w3.org/2000/svg";
/* dotted red jump arc with an arrowhead, from x1 to x2 at baseline y, into an <svg> */
function mtgArc(svg, x1, x2, y, lift, label){
  const g = document.createElementNS(MTG_SVG, "g"); g.setAttribute("class", "mtg-arc");
  const mx = (x1 + x2) / 2, top = y - lift, cy = top - lift * 0.35;
  // the head points along the curve's end tangent; the shaft stops at its base so the dots meet the head
  const tx = x2 - mx, ty = y - cy, tl = Math.hypot(tx, ty) || 1, ux = tx / tl, uy = ty / tl;
  const HL = 20, HW = 11, bx = x2 - ux * HL, by = y - uy * HL;
  const d = `M${x1},${y} Q${mx},${cy} ${bx},${by}`;
  const head = `M${x2},${y} L${bx - uy * HW},${by + ux * HW} L${bx + uy * HW},${by - ux * HW} Z`;
  // a white halo under the red dots and head keeps them readable over grass, water and stones
  [["mtg-arc-halo", d], ["mtg-arc-path", d], ["mtg-arc-head", head]].forEach(([cls, dd])=>{
    const p = document.createElementNS(MTG_SVG, "path");
    p.setAttribute("d", dd); p.setAttribute("class", cls); g.appendChild(p);
  });
  if(label){
    const t = document.createElementNS(MTG_SVG, "text");
    t.setAttribute("x", mx); t.setAttribute("y", top - lift * 0.2 - 6); t.setAttribute("class", "mtg-arc-lbl");
    t.textContent = label; g.appendChild(t);
  }
  svg.appendChild(g);
  requestAnimationFrame(()=> g.classList.add("show"));
  return g;
}
/* hop an absolutely-positioned element from (x1) to (x2) along a parabola (its `left` is the centre) */
function mtgHop(el, x1, x2, lift, ms){
  // Keep the whole sprite within its positioning frame, including its shadow clearance.
  lift = Math.max(0, Math.min(lift, el.offsetTop - 12));
  return new Promise(res=>{
    const t0 = performance.now();
    el.classList.add("hopping");
    (function f(now){
      const k = Math.min(1, (now - t0) / ms);
      const e = k < .5 ? 2*k*k : 1 - Math.pow(-2*k + 2, 2) / 2;
      el.style.left = (x1 + (x2 - x1) * e) + "px";
      el.style.transform = `translate(-50%, ${-Math.sin(Math.PI * k) * lift}px)`;
      if(k < 1) requestAnimationFrame(f); else { el.style.transform = "translate(-50%,0)"; el.classList.remove("hopping"); res(); }
    })(t0);
  });
}
/* our own hand cue (the engine's nudge hand lives in .slide-stage and is hidden by some layers) */
function mtgHand(parent, x, y){ const h = mtgEl("img", "mtg-hand"); h.src = "assets/UI/nudge_hand_new.svg"; h.style.left = x + "px"; h.style.top = y + "px"; parent.appendChild(h); return h; }

/* =====================================================================================
   BRIDGE_TEACH — टप्पू crosses the stone bridge (deck slides 4–6)
   data: lo, hi, step, friend_at, heading, camera?, steps[{cap, wait_tap?, clips[{vo, …actions}]}]
   ===================================================================================== */
SlideModules.BRIDGE_TEACH = { mount(host, slide){
  const d = slide.data, tok = mtgToken();
  state.ownsAudio = true;
  const card = host.closest(".tut-card");
  if(card){ card.classList.add("br-card"); const tp = card.querySelector(".tut-prompt"); if(tp) tp.textContent = d.heading || ""; }
  // The scenery belongs to the viewport; only stones, labels and characters follow the camera.
  /* the scene bleeds to the frame's inner edges: measure the frame rather than assume its width */
  const _bleedL = card ? Math.max(0, host.offsetLeft - card.clientLeft) : 30;
  const VIEW_W = (card && card.clientWidth) ? card.clientWidth : 1113;
  const VIEW_H = 282, FEET_Y = 194;
  const span = d.hi - d.lo, START_SPACE = 110, END_SPACE = 190;
  const U = d.camera ? 80 : (VIEW_W - START_SPACE - END_SPACE) / span;
  const RW = Math.min(U * .88, 76), RH = RW * 52 / 160;
  const WORLD_W = d.camera ? START_SPACE + span * U + END_SPACE : VIEW_W;
  const X = n => START_SPACE + (n - d.lo) * U;
  const ROCK_TOP = FEET_Y - 3, STONE_Y = FEET_Y - 2, NUM_Y = FEET_Y + 32;
  const LOTUS = "assets/Images/prop_lotus.svg";

  const wrap = mtgEl("div", "br-wrap");
  const view = mtgEl("div", "br-view"); view.style.height = VIEW_H + "px"; view.style.width = VIEW_W + "px";
  const world = mtgEl("div", "br-world"); world.style.width = WORLD_W + "px"; world.style.height = VIEW_H + "px";
  const stones = {}, nums = {};
  for(let n = d.lo; n <= d.hi; n++){
    const big = (n % d.step === 0);
    const s = mtgEl("div", "br-rock" + (big ? " key" : ""));
    s.style.cssText = `left:${X(n)}px;top:${ROCK_TOP}px;width:${RW}px;height:${RH}px`;
    const im = mtgEl("img"); im.src = LOTUS; im.alt = ""; s.appendChild(im);
    world.appendChild(s); stones[n] = s;
    const lb = mtgEl("div", "br-num" + (big ? " big" : ""), String(n));
    lb.style.left = X(n) + "px"; lb.style.top = NUM_Y + "px";
    if(!big && U < 30) lb.style.fontSize = Math.max(12, U * 0.52) + "px";
    world.appendChild(lb); nums[n] = lb;
  }
  const svg = document.createElementNS(MTG_SVG, "svg"); svg.setAttribute("class", "br-svg");
  svg.setAttribute("width", WORLD_W); svg.setAttribute("height", VIEW_H); world.appendChild(svg);
  const dot = mtgEl("div", "br-dot"); dot.style.top = (ROCK_TOP + RH * 0.3) + "px"; world.appendChild(dot);
  // Distinct landing and resting leaves leave room for both frogs at the far end.
  const FW = Math.min(70, U * .86), FH = FW * 579 / 477;
  const FRW = FW, FRH = FRW * 574 / 551, friendX = X(d.hi) + 110;
  const rest = mtgEl("img", "br-rest-leaf"); rest.src = LOTUS; rest.alt = "";
  rest.style.cssText = "left:"+friendX+"px;top:"+(FEET_Y-3)+"px;width:110px;height:36px";
  world.appendChild(rest);
  const friend = mtgEl("img", "br-friend"); friend.src = mtgImg("chr_friend");
  friend.alt = "टप्पू का दोस्त";
  friend.style.cssText = "left:"+friendX+"px;top:"+(FEET_Y-FRH)+"px;width:"+FRW+"px";
  world.appendChild(friend);
  const frog = mtgEl("img", "br-frog"); frog.src = mtgImg("chr_tappu"); frog.alt = "टप्पू";
  frog.style.width = FW + "px"; frog.style.top = (FEET_Y-FH) + "px";
  let at = d.lo; frog.style.left = X(at) + "px"; world.appendChild(frog);
  view.appendChild(world); wrap.appendChild(view);
  const cap = mtgEl("div", "br-cap"); wrap.appendChild(cap);
  wrap.style.margin = `0 0 0 ${-_bleedL}px`; wrap.style.width = VIEW_W + "px";
  host.appendChild(wrap);

  // Scale, translation and labels share one animation clock anchored at the feet.
  let cam = d.camera ? "all" : null, cameraFrame = 0, cameraFinish = null;
  let camera = {x:0,z:1};
  const reduceMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  function paintCamera(x,z){
    camera={x,z}; world.style.setProperty("--z",z);
    world.classList.toggle("zoomed",z<.48);
    world.style.transform="translate("+(-x)+"px,"+(FEET_Y*(1-z))+"px) scale("+z+")";
  }
  function cameraTo(x,z,ms=700){
    if(cameraFrame) cancelAnimationFrame(cameraFrame);
    if(cameraFinish) cameraFinish();
    const from={...camera}, start=performance.now();
    world.dataset.cameraMoving="true";
    return new Promise(resolve=>{
      cameraFinish=resolve;
      function tick(now){
        if(tok!==_mtgTok){cameraFrame=0;cameraFinish=null;resolve();return;}
        const t=ms&&!reduceMotion()?Math.min(1,(now-start)/ms):1, ease=t*t*(3-2*t);
        paintCamera(from.x+(x-from.x)*ease,from.z+(z-from.z)*ease);
        if(t<1) cameraFrame=requestAnimationFrame(tick);
        else{cameraFrame=0;cameraFinish=null;world.dataset.cameraMoving="false";resolve();}
      }
      tick(start);
    });
  }
  function rangeCamera(a,b,ms=700){
    const left=Math.max(0,X(Math.max(d.lo,a))-80);
    const right=b>=d.hi?WORLD_W:Math.min(WORLD_W,X(b)+80);
    const z=Math.min(1,VIEW_W/(right-left));
    const x=Math.max(0,Math.min(WORLD_W*z-VIEW_W,(left+right)*z/2-VIEW_W/2));
    return cameraTo(x,z,ms);
  }
  function applyCam(mode,ms=700){
    if(!d.camera)return Promise.resolve();
    cam=mode;
    if(mode==="all")return cameraTo(0,VIEW_W/WORLD_W,ms);
    if(Array.isArray(mode))return rangeCamera(mode[0],mode[1],ms);
    return rangeCamera(at,Math.min(d.hi,at+d.step),ms);
  }
  paintCamera(0,d.camera?VIEW_W/WORLD_W:1);

  const glow = n => { mtgPulse(stones[n], "glow", 1400); mtgPulse(nums[n], "glow", 1400); };
  const mark = n => { stones[n].classList.add("mark"); nums[n].classList.add("mark"); mtgPulse(nums[n], "pop", 600); };
  const clearLit = () => Object.values(stones).forEach(s => s.classList.remove("lit"));
  async function jump(a, b){
    clearLit(); dot.classList.remove("show");
    if(cam==="follow") await rangeCamera(a,b,420);
    const lift=Math.max(12,Math.min(62,FEET_Y-FH-22));
    view.dataset.jumpActive="true";
    mtgArc(svg,X(a),X(b),STONE_Y-2,lift);
    await mtgHop(frog,X(a),X(b),lift,950);
    view.dataset.jumpActive="false";
    at=b;view.dataset.landedAt=String(at);mark(b);glow(b);
  }
  async function spanLight(a, b){ for(let n = a + 1; n <= b; n++){ stones[n].classList.add("lit"); await mtgWait(85, tok); } }
  async function runClip(c){
    mtgAlive(tok);
    if(c.cam) await applyCam(c.cam);
    if(c.focus) mtgPulse(c.focus === "friend" ? friend : frog, "focus", 1600);
    if(c.wave) mtgPulse(friend, "wave", 1400);
    if(c.glow != null) glow(c.glow);
    if(c.dot != null){ dot.style.left = X(c.dot) + "px"; dot.classList.add("show"); stones[c.dot].classList.add("lit"); mtgPulse(nums[c.dot], "pop", 500); }
    if(c.mark != null) mark(c.mark);
    if(c.happy){ mtgPulse(frog, "bounce", 900); mtgPulse(friend, "bounce", 900); }
    const voDone = mtgSay(c.vo, tok);
    if(c.jump){ await mtgWait(250, tok); if(c.span) await spanLight(c.jump[0], c.span[1]); await jump(c.jump[0], c.jump[1]); }
    await voDone;
    if(c.wave_end) mtgPulse(friend, "wave", 1400);
    if(c.glow_end != null) glow(c.glow_end);
    if(c.pause_after) await mtgWait(c.pause_after, tok);
  }
  function waitTap(){
    return new Promise((res, rej)=>{
      frog.classList.add("tappable");
      let hand = mtgHand(world, X(at) + 6, FEET_Y - FH * .55);
      const again = setInterval(()=>{ if(tok !== _mtgTok){ clearInterval(again); return; } if(!hand){ hand = mtgHand(world, X(at) + 6, FEET_Y - FH * .55); setTimeout(()=>{ if(hand){ hand.remove(); hand = null; } }, 1800); } }, 6000);
      setTimeout(()=>{ if(hand){ hand.remove(); hand = null; } }, 1800);
      frog.onclick = ()=>{
        if(tok !== _mtgTok) return rej(MTG_STOP);
        frog.onclick = null; frog.classList.remove("tappable"); clearInterval(again);
        if(hand){ hand.remove(); hand = null; }
        sfxTap(); SwiftPAL.emit("teach_tap", { slide_id: slide.id, at });
        res();
      };
    });
  }
  let done = false, lastStep = null;
  state.replayAudio = ()=>{ if(!done || !lastStep) return; mtgRun(async()=>{ for(const c of lastStep.clips) await mtgSay(c.vo, tok); }); };
  mtgRun(async()=>{
    await mtgWait(350, tok);
    for(const st of d.steps){
      if(st.wait_tap) await waitTap();
      cap.textContent = st.cap; mtgPulse(cap, "in", 400);
      lastStep = st;
      for(const c of st.clips) await runClip(c);
      await mtgWait(250, tok);
    }
    done = true;
    SwiftPAL.emit("teach_done", { slide_id: slide.id });
    setNavActive(true);
  });
}};

/* =====================================================================================
   number line used by JUMP_PICK and the SEQ_FILL hint popup
   ===================================================================================== */
function mtgNumberLine(o){
  // o: lo, hi, width, height, baseY, every (label step), bigEvery
  const U = (o.width - 80) / (o.hi - o.lo), X = n => 40 + (n - o.lo) * U;
  const root = mtgEl("div", "nl " + (o.cls || "")); root.style.width = o.width + "px"; root.style.height = o.height + "px";
  const svg = document.createElementNS(MTG_SVG, "svg"); svg.setAttribute("width", o.width); svg.setAttribute("height", o.height); svg.setAttribute("class", "nl-svg");
  const ln = document.createElementNS(MTG_SVG, "path"); ln.setAttribute("class", "nl-axis");
  ln.setAttribute("d", `M10,${o.baseY} H${o.width - 10} M22,${o.baseY - 9} L8,${o.baseY} L22,${o.baseY + 9} M${o.width - 22},${o.baseY - 9} L${o.width - 8},${o.baseY} L${o.width - 22},${o.baseY + 9}`);
  if(o.noArrows) ln.setAttribute("d", `M${X(o.lo)},${o.baseY} H${X(o.hi)}`);
  svg.appendChild(ln);
  const segs = {}, labels = {};
  for(let n = o.lo; n <= o.hi; n++){
    const big = o.bigEvery && n % o.bigEvery === 0;
    if(o.dots){ const c = document.createElementNS(MTG_SVG, "circle"); c.setAttribute("cx", X(n)); c.setAttribute("cy", o.baseY); c.setAttribute("r", 7); c.setAttribute("class", "nl-dotpt"); svg.appendChild(c); }
    else { const t = document.createElementNS(MTG_SVG, "path"); t.setAttribute("d", `M${X(n)},${o.baseY - (big ? 15 : 10)} V${o.baseY + (big ? 15 : 10)}`); t.setAttribute("class", "nl-tick" + (big ? " big" : "")); svg.appendChild(t); }
    if(n < o.hi){ const s = document.createElementNS(MTG_SVG, "path"); s.setAttribute("d", `M${X(n)},${o.baseY} H${X(n + 1)}`); s.setAttribute("class", "nl-seg"); svg.appendChild(s); segs[n] = s; }
    if(!o.every || n % o.every === 0 || n === o.lo || n === o.hi){
      const l = mtgEl("div", "nl-lbl" + (big ? " big" : ""), String(n)); l.style.left = X(n) + "px"; l.style.top = (o.baseY + 18) + "px"; root.appendChild(l); labels[n] = l;
    }
  }
  root.appendChild(svg);
  return { root, svg, X, U, segs, labels,
    glow(n, ms){ const l = labels[n]; if(l) mtgPulse(l, "glow", ms || 1600); },
    hold(n){ const l = labels[n]; if(l) l.classList.add("glow-hold"); },
    async walk(a, b, tok){ for(let n = a; n < b; n++){ segs[n] && segs[n].classList.add("lit"); await mtgWait(Math.max(90, 520 / (b - a)), tok); } },
    unwalk(){ Object.values(segs).forEach(s => s.classList.remove("lit")); } };
}

/* option tray shared by JUMP_PICK and SEQ_FILL */
function mtgOptions(host, values, onPick){
  const row = mtgEl("div", "mtg-opts");
  const cells = values.map(v=>{
    const b = mtgEl("button", "mtg-opt", String(v)); b.type = "button"; b.dataset.v = v; b.disabled = true;
    b.onclick = ()=> onPick(v, b);
    row.appendChild(b); return b;
  });
  host.appendChild(row);
  return { row, cells,
    enable(on){ cells.forEach(c => { if(!c.classList.contains("used") && !c.classList.contains("faded")) c.disabled = !on; }); },
    wiggle(b){ mtgPulse(b, "wiggle", 600); } };
}
/* WA3: fade + disable everything except the answer, pulse it, hand cue — no tick before the tap */
function mtgGuideTo(opts, answer){
  let target = null;
  opts.cells.forEach(c=>{
    if(+c.dataset.v === answer && !c.classList.contains("used")){ target = c; c.classList.add("guide"); }
    else if(!c.classList.contains("used")){ c.classList.add("faded"); c.disabled = true; }
  });
  if(target) pointNudgeAt(target, true);
  return target;
}

/* =====================================================================================
   JUMP_PICK — guided Q1–Q3 (deck slide 7): where will the frog land?
   ===================================================================================== */
SlideModules.JUMP_PICK = { mount(host, slide){
  const d = slide.data, tok = mtgToken();
  state.ownsAudio = true;
  const board = mtgEl("div", "jp-board");
  const span = d.hi - d.lo;
  const nl = mtgNumberLine({ lo: d.lo, hi: d.hi, width: 1000, height: 200, baseY: 140,
    every: span > 30 ? 5 : 1, bigEvery: span > 30 ? 10 : (d.step >= 5 ? 5 : 2), cls: "jp-nl" });
  board.appendChild(nl.root);
  for(let i = 0; i + 1 < d.prior.length; i++) mtgArc(nl.svg, nl.X(d.prior[i]), nl.X(d.prior[i + 1]), 136, Math.min(70, 26 + (d.prior[i + 1] - d.prior[i]) * nl.U * 0.25));
  const frog = mtgEl("img", "jp-frog"); frog.src = mtgImg("chr_tappu"); frog.style.left = nl.X(d.at) + "px";
  nl.root.appendChild(frog);
  host.appendChild(board);
  let tries = 0, busy = true, solved = false;
  const opts = mtgOptions(host, d.options, (v, b)=> pick(v, b));
  const playQ = async()=>{ for(const c of d.q){ mtgAlive(tok); if(c.glow != null) nl.glow(c.glow, 1800); await mtgSay(c.vo, tok); } };
  state.replayAudio = ()=>{ if(busy || solved) return; busy = true; opts.enable(false); mtgRun(async()=>{ await playQ(); busy = false; opts.enable(true); }); };
  function pick(v, b){
    if(busy || solved) return;
    sfxTap();
    if(v === d.answer){
      solved = true; busy = true; opts.enable(false); stopNudge();
      b.classList.remove("guide"); b.classList.add("right");
      SwiftPAL.emit("jump_pick_correct", { slide_id: slide.id, attempts: tries + 1 });
      mtgOst(d.correct_ost);
      mtgRun(async()=>{
        mtgRight(); confettiCannon(); setSwMood("celebrate");
        const voDone = mtgSay(d.correct, tok);
        const lift = Math.max(0, Math.min(44, frog.offsetTop - 12, 30 + (d.answer - d.at) * nl.U * 0.25));
        mtgArc(nl.svg, nl.X(d.at), nl.X(d.answer), 136, lift);
        await mtgHop(frog, nl.X(d.at), nl.X(d.answer), lift, 900);
        nl.hold(d.answer);
        await voDone;
        setNavActive(true);
      });
      return;
    }
    tries++; state.attempts = tries; busy = true; opts.enable(false);
    opts.wiggle(b); mtgWrong(); setSwMood("tryagain");
    SwiftPAL.emit("jump_pick_wrong", { slide_id: slide.id, attempt: tries, picked: v });
    mtgRun(async()=>{
      await mtgWait(450, tok);
      if(tries === 1){ mtgOst(d.wa1.ost); if(d.wa1.replay_q) await playQ(); else await mtgSay(d.wa1.vo, tok); }
      else if(tries === 2){ mtgOst(d.wa2.ost); state.hintUsed = true;
        const voDone = mtgSay(d.wa2.vo, tok); await mtgWait(300, tok); await nl.walk(d.at, d.answer, tok); await voDone; await mtgWait(500, tok); nl.unwalk(); }
      else { mtgOst(d.wa3.ost); state.scaffoldLevel = 3; await mtgSay(d.wa3.vo, tok); mtgGuideTo(opts, d.answer); }
      busy = false; opts.enable(true);
      if(tries >= 3) opts.cells.forEach(c => { if(c.classList.contains("faded")) c.disabled = true; });
    });
  }
  mtgRun(async()=>{ await mtgWait(400, tok); await playQ(); busy = false; opts.enable(true); });
}};

/* =====================================================================================
   SEQ_FILL — Q4–Q7 (deck slides 8–11): fill the missing numbers, one blank at a time.
   WA1 wiggle + VO · WA2 number-line hint popup «संकेत» · WA3 fade the rest, pulse + hand.
   ===================================================================================== */
SlideModules.SEQ_FILL = { mount(host, slide){
  const d = slide.data, tok = mtgToken();
  state.ownsAudio = true;
  const stage = mtgEl("div", "sf-stage");
  const strip = mtgEl("div", "sf-strip");
  const boxes = d.seq.map((n, i)=>{
    const b = mtgEl("div", "sf-box" + (n == null ? " blank" : ""), n == null ? "?" : String(n));
    if(d.intro) b.classList.add("hidden");
    strip.appendChild(b); return b;
  });
  const animal = mtgEl("img", "sf-animal"); animal.src = mtgImg(d.animal);
  stage.appendChild(animal); stage.appendChild(strip); host.appendChild(stage);
  const blanks = d.seq.map((n, i) => n == null ? i : -1).filter(i => i >= 0);
  let bi = 0, tries = 0, busy = true;
  const opts = mtgOptions(host, d.options, (v, b)=> pick(v, b));
  if(d.intro) opts.row.classList.add("hidden");
  // animal sits on the last filled box to the left of the active blank (Q4 starts on box 0)
  const boxX = i => boxes[i].offsetLeft + boxes[i].offsetWidth / 2;
  let animalAt = 0;
  function seatAnimal(i){ animalAt = i; animal.style.left = boxX(i) + "px"; }
  const lastFilledBefore = i => { for(let k = i - 1; k >= 0; k--) if(d.seq[k] != null || boxes[k].classList.contains("filled")) return k; return 0; };
  function activate(){ boxes.forEach(b => b.classList.remove("active")); if(bi < blanks.length) boxes[blanks[bi]].classList.add("active"); }
  async function hopTo(i){ const x1 = boxX(animalAt), x2 = boxX(i); await mtgHop(animal, x1, x2, 44, 650); animalAt = i; }
  const playQ = async()=>{ for(const c of d.q){ mtgAlive(tok); if(c.reveal_blank) boxes.forEach(b => b.classList.remove("hidden")); await mtgSay(c.vo, tok); } };
  state.replayAudio = ()=>{ if(busy || bi >= blanks.length) return; busy = true; opts.enable(false); mtgRun(async()=>{ await playQ(); busy = false; opts.enable(true); }); };

  async function hintPopup(bl){
    const ov = mtgEl("div", "sf-hint-ov"), card = mtgEl("div", "sf-hint");
    card.appendChild(mtgEl("div", "sf-hint-title", "संकेत"));
    const [a, z] = bl.hint_range;
    const nl = mtgNumberLine({ lo: a, hi: z, width: 760, height: 190, baseY: 128, dots: true, noArrows: false, cls: "sf-hint-nl" });
    const pet = mtgEl("img", "sf-hint-animal"); pet.src = mtgImg(d.animal); pet.style.left = nl.X(bl.from) + "px";
    nl.root.appendChild(pet);
    card.appendChild(nl.root);
    card.appendChild(mtgEl("div", "sf-hint-cap", mtgText(bl.hint)));
    ov.appendChild(card); $("stage").appendChild(ov);
    requestAnimationFrame(()=> ov.classList.add("show"));
    const opened = Date.now();
    const voDone = mtgSay(bl.hint, tok);
    await mtgWait(700, tok);
    mtgArc(nl.svg, nl.X(bl.from), nl.X(bl.answer), 124, Math.min(80, 34 + (bl.answer - bl.from) * nl.U * 0.18), "+" + bl.step);
    await mtgWait(900, tok);
    nl.hold(bl.answer);
    await voDone;
    await mtgWait(Math.max(900, 5000 - (Date.now() - opened)), tok);   // deck: the popup stays ~5 s
    ov.classList.remove("show"); setTimeout(()=> ov.remove(), 300);
  }
  // a hint popup is outside the slide host — make sure leaving the slide removes it
  const killOv = ()=> document.querySelectorAll(".sf-hint-ov").forEach(o => o.remove());
  $("navBtn").addEventListener("click", killOv, { once: true });

  function pick(v, b){
    if(busy || bi >= blanks.length) return;
    const bl = d.blanks[bi], idx = blanks[bi];
    sfxTap();
    if(v === bl.answer){
      busy = true; opts.enable(false); stopNudge();
      b.classList.remove("guide"); b.classList.add("used");
      SwiftPAL.emit("seq_fill_correct", { slide_id: slide.id, blank: bi, attempts: tries + 1 });
      mtgRun(async()=>{
        mtgRight(); confettiCannon(); setSwMood("celebrate"); mtgOst(mtgText(bl.correct));
        const box = boxes[idx]; box.textContent = String(v); box.classList.remove("blank", "active"); box.classList.add("filled");
        mtgPulse(box, "glow", 1500);
        const voDone = mtgSay(bl.correct, tok);
        await hopTo(idx);
        await voDone;
        bi++; tries = 0; state.attempts = 0;
        opts.cells.forEach(c => c.classList.remove("faded", "guide"));
        if(bi >= blanks.length){
          boxes.forEach((bx, k)=> setTimeout(()=> mtgPulse(bx, "glow", 900), k * 140));
          setNavActive(true);
          killOv();
        } else { activate(); mtgOst(slide.data.ost); busy = false; opts.enable(true); }
      });
      return;
    }
    tries++; state.attempts = tries; busy = true; opts.enable(false);
    opts.wiggle(b); mtgWrong(); setSwMood("tryagain");
    SwiftPAL.emit("seq_fill_wrong", { slide_id: slide.id, blank: bi, attempt: tries, picked: v });
    mtgRun(async()=>{
      await mtgWait(450, tok);
      if(tries === 1){ mtgOst(bl.wa1_ost || d.ost); await mtgSay(bl.wa1, tok); }
      else if(tries === 2){
        state.hintUsed = true;
        if(bl.pre_hint){ mtgOst(mtgText(bl.pre_hint)); await mtgSay(bl.pre_hint, tok); }
        mtgOst(mtgText(bl.hint));
        await hintPopup(bl);
        mtgOst(bl.after_hint_ost || mtgText(bl.after_hint) || d.ost);
        if(bl.after_hint) await mtgSay(bl.after_hint, tok);
      } else { mtgOst(mtgText(bl.wa3)); state.scaffoldLevel = 3; await mtgSay(bl.wa3, tok); mtgGuideTo(opts, bl.answer); }
      busy = false; opts.enable(true);
      if(tries >= 3) opts.cells.forEach(c => { if(c.classList.contains("faded")) c.disabled = true; });
    });
  }

  mtgRun(async()=>{
    await mtgWait(60, tok);
    seatAnimal(d.intro ? 0 : lastFilledBefore(blanks[0]));
    await mtgWait(350, tok);
    if(d.intro){
      for(const c of d.intro){
        mtgAlive(tok);
        if(c.reveal != null){ boxes[c.reveal].classList.remove("hidden"); mtgPulse(boxes[c.reveal], "glow", 700); }
        const voDone = mtgSay(c.vo, tok);
        if(c.hop) await hopTo(c.hop);
        await voDone;
      }
    }
    activate();
    await playQ();
    opts.row.classList.remove("hidden");
    busy = false; opts.enable(true);
  });
}};

/* =====================================================================================
   SPACE_PODS — independent game «अंतरिक्ष की सैर» (deck slides 12–16)
   Menu (2s / 5s / 10s) → 3 rounds each → back to the menu with a badge → all 3 done → next slide.
   ===================================================================================== */
SlideModules.SPACE_PODS = { mount(host, slide){
  const g = slide.data, tok = mtgToken();
  state.ownsAudio = true;
  $("stage").classList.add("mtg-game"); document.body.classList.add("mtg-game");
  const root = mtgEl("div", "sp-root"); $("stage").appendChild(root);
  const done = new Set();
  let curVo = g.menu_vo;
  /* file4's own header audio chip graphic, cloned so the game's replay button matches it */
  const audioBtn = mtgEl("button", "sp-audio", ($("audioChip") && $("audioChip").innerHTML) || "🔊"); audioBtn.type = "button"; audioBtn.setAttribute("aria-label", "फिर सुनिए");
  audioBtn.onclick = ()=>{ state.audioReplays++; play(mtgSrc(curVo), ()=>{}); };
  const buddy = mtgEl("div", "sp-swiftie", `<img src="assets/UI/sw_head_talking.webp" alt="">`);
  const scene = mtgEl("div", "sp-scene");
  root.appendChild(scene); root.appendChild(audioBtn); root.appendChild(buddy);
  const say = (id)=>{ curVo = id; return mtgSay(id, tok); };
  const badgeAt = (cast)=> g.badge[cast] || [0.5, 0.65];
  function astronaut(cast, n, cls){
    const a = mtgEl("div", "sp-astro " + (cls || ""));
    const inner = mtgEl("div", "sp-astro-in");
    const im = mtgEl("img"); im.src = mtgImg(cast); im.draggable = false;
    const [bx, by] = badgeAt(cast);
    const bd = mtgEl("div", "sp-badge", String(n)); bd.style.left = (bx * 100) + "%"; bd.style.top = (by * 100) + "%";
    inner.appendChild(im); inner.appendChild(bd); a.appendChild(inner); a.dataset.n = n;
    return a;
  }
  /* an animal riding in a pod: shown through a window cut to the glass dome, so nothing pokes out of it;
     the helmet is centred in the dome (CARD rider = [helmet centre x, helmet top y] as sprite fractions) */
  function rider(cast, cls){
    const w = mtgEl("div", "sp-dome");
    const im = mtgEl("img", cls); im.src = mtgImg(cast); im.draggable = false; im.alt = "";
    const [cx, top] = (g.rider && g.rider[cast]) || [0.5, 0.05];
    im.style.transform = `translate(${-cx * 100}%, ${-top * 100}%)`;
    w.appendChild(im); return w;
  }
  function seat(pod, cast, n){
    pod.classList.add("filled");
    pod.insertBefore(rider(cast, "sp-seated"), pod.firstChild);
    const nb = mtgEl("div", "sp-podnum", String(n)); pod.appendChild(nb);
    return nb;
  }
  function puff(pod){
    for(let i = 0; i < 7; i++){
      const p = mtgEl("span", "sp-puff");
      const ang = (i / 7) * Math.PI * 2;
      p.style.setProperty("--dx", Math.cos(ang) * 70 + "px"); p.style.setProperty("--dy", Math.sin(ang) * 46 + "px");
      p.style.animationDelay = (i * 25) + "ms";
      pod.appendChild(p); setTimeout(()=> p.remove(), 900);
    }
  }
  const shuffle = arr => { const a = arr.slice(); for(let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  // ---------------- MENU ----------------
  function menu(){
    scene.innerHTML = "";
    scene.appendChild(mtgEl("div", "sp-title big", "★ " + g.title + " ★"));
    const row = mtgEl("div", "sp-menu");
    g.levels.forEach((L, i)=>{
      const c = mtgEl("button", "sp-card c" + i + (done.has(i) ? " done" : "")); c.type = "button";
      const art = mtgEl("div", "sp-card-art");
      const pod = mtgEl("img", "sp-card-pod"); pod.src = mtgImg("sp_pod");
      art.appendChild(rider(L.cast, "sp-card-animal")); art.appendChild(pod);
      c.appendChild(art);
      c.appendChild(mtgEl("div", "sp-card-lbl", L.label));
      c.appendChild(mtgEl("div", "sp-card-play", done.has(i) ? "✔" : "▶"));
      if(done.has(i)) c.appendChild(mtgEl("div", "sp-card-badge", "★"));
      c.onclick = ()=>{ if(done.has(i) || tok !== _mtgTok) return; sfxTap(); stopAudio(); runLevel(i); };
      row.appendChild(c);
    });
    scene.appendChild(row);
  }

  // ---------------- ROUND ----------------
  function round(L, r){
    return new Promise((resolve, reject)=>{
      const R = L.rounds[r];
      scene.innerHTML = "";
      scene.appendChild(mtgEl("div", "sp-title", "★ " + L.label + " ★"));
      const pods = mtgEl("div", "sp-pods");
      const podEls = R.seq.map((n, i)=>{
        const p = mtgEl("div", "sp-pod dd-zone"); p.dataset.i = i;
        const im = mtgEl("img", "sp-pod-img"); im.src = mtgImg("sp_pod"); im.draggable = false;
        p.appendChild(im); pods.appendChild(p); return p;
      });
      const nums = [];
      R.prefilled.forEach(i => { nums[i] = seat(podEls[i], L.cast, R.seq[i]); podEls[i].classList.add("locked"); });
      scene.appendChild(pods);
      const ground = mtgEl("div", "sp-ground");
      const pool = shuffle(R.seq.filter((n, i) => !R.prefilled.includes(i)).concat(R.distractors));
      const W = 1333 - 300, x0 = 230, gap = W / pool.length;
      const walkers = pool.map((n, k)=>{
        const a = astronaut(L.cast, n, "walker"); a.style.left = (x0 + gap * k + gap / 2 - 75) + "px";
        ground.appendChild(a); return a;
      });
      scene.appendChild(ground);
      let wrongSaid = false, finished = false, idleT = null, guidedOnce = false, busyVo = false;
      let selected = null, tapLocked = false;
      const status = mtgEl("div", "sp-status", "जानवर चुनिए, फिर खाली यान चुनिए।");
      status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
      scene.appendChild(status);
      const roundLabel = mtgEl("div", "sp-round", "दौर " + (r + 1) + " / " + L.rounds.length);
      scene.appendChild(roundLabel);
      function clearSelection(){
        if(selected){ selected.classList.remove("selected"); selected.setAttribute("aria-pressed", "false"); }
        selected = null;
        podEls.forEach(p => p.classList.remove("select-target"));
      }
      const needed = () => podEls.filter(p => !p.classList.contains("filled"));
      function ghost(){
        const target = needed()[0]; if(!target || finished) return;
        const n = R.seq[+target.dataset.i];
        const src = walkers.find(w => +w.dataset.n === n && !w.classList.contains("snapped"));
        if(!src) return;
        target.classList.add("cue");
        const gh = astronaut(L.cast, n, "ghost");
        const sr = src.getBoundingClientRect(), tr = target.getBoundingClientRect(), rr = root.getBoundingClientRect();
        const sc = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
        const sx = (sr.left - rr.left) / sc, sy = (sr.top - rr.top) / sc;
        const tx = (tr.left - rr.left + tr.width / 2) / sc - 65, ty = (tr.top - rr.top) / sc;
        gh.style.left = sx + "px"; gh.style.top = sy + "px";
        const hand = mtgEl("img", "sp-ghost-hand"); hand.src = "assets/UI/nudge_hand_new.svg"; gh.appendChild(hand);
        root.appendChild(gh);
        gh.animate([{ left: sx + "px", top: sy + "px", opacity: 0 }, { opacity: .75, offset: .15 }, { left: tx + "px", top: (ty - 10) + "px", opacity: .75, offset: .85 }, { left: tx + "px", top: (ty - 10) + "px", opacity: 0 }],
          { duration: 2200, easing: "ease-in-out" }).onfinish = ()=>{ gh.remove(); target.classList.remove("cue"); };
      }
      function armIdle(){
        clearTimeout(idleT);
        if(r !== 0 || guidedOnce || finished) return;
        idleT = setTimeout(()=>{
          if(tok !== _mtgTok || finished) return;
          guidedOnce = true;            // inactivity repeat happens once (separate from wrong attempts)
          ghost(); if(!busyVo) say(g.guide_vo).catch(()=>{});
        }, g.inactivity_ms);
      }
      function gradeDrop(zone, tile){
          if(zone.classList.contains("filled") || tile.classList.contains("snapped")) return;
          clearSelection();
          if(tok !== _mtgTok || finished) return;
          clearTimeout(idleT);
          const i = +zone.dataset.i, n = +tile.dataset.n;
          if(R.seq[i] === n){
            tile.classList.add("snapped");
            tile.tabIndex = -1; tile.setAttribute("aria-disabled", "true");
            zone.tabIndex = -1; zone.setAttribute("aria-disabled", "true");
            zone.setAttribute("aria-label", String(n) + ", भरा हुआ यान");
            status.textContent = "सही! " + n;
            mtgRight();
            nums[i] = seat(zone, L.cast, n);
            mtgPulse(nums[i], "glow", 1200); mtgPulse(zone, "snap", 600);
            busyVo = true; say(`vo_g_n_${n}`).then(()=>{ busyVo = false; }).catch(()=>{});
            SwiftPAL.emit("space_drop_correct", { slide_id: slide.id, step: L.step, round: r + 1, n });
            if(!needed().length) complete(); else armIdle();
          } else {
            status.textContent = "फिर कोशिश कीजिए।";
            mtgWrong();
            mtgPulse(zone, "wiggle", 650); puff(zone);
            SwiftPAL.emit("space_drop_wrong", { slide_id: slide.id, step: L.step, round: r + 1, n, pod: i });
            if(!wrongSaid){ wrongSaid = true; busyVo = true; say(L.wrong).then(()=>{ busyVo = false; }).catch(()=>{}); }
            armIdle();
          }
      }
      const keyActivate = fn => e => {
        if(e.key === "Enter" || e.key === " "){ e.preventDefault(); fn(); }
      };
      podEls.forEach((p, i) => {
        const filled = p.classList.contains("filled");
        p.setAttribute("role", "button"); p.tabIndex = filled ? -1 : 0;
        p.setAttribute("aria-disabled", String(filled));
        p.setAttribute("aria-label", filled ? String(R.seq[i]) + ", भरा हुआ यान" : "खाली यान " + (i + 1));
        const activate = () => {
          if(!selected || finished || tapLocked || busyVo || p.classList.contains("filled")) return;
          tapLocked = true; gradeDrop(p, selected);
          setTimeout(() => { tapLocked = false; }, 650);
        };
        p.onclick = activate; p.onkeydown = keyActivate(activate);
      });
      walkers.forEach(w=>{
        w.setAttribute("role", "button"); w.setAttribute("aria-pressed", "false"); w.tabIndex = 0;
        w.setAttribute("aria-label", String(w.dataset.n) + ", जानवर चुनिए");
        const select = () => {
          if(finished || busyVo || w.classList.contains("snapped")) return;
          const wasSelected = selected === w; clearSelection();
          if(!wasSelected){
            selected = w; w.classList.add("selected"); w.setAttribute("aria-pressed", "true");
            needed().forEach(p => p.classList.add("select-target"));
            status.textContent = w.dataset.n + " चुना। अब खाली यान चुनिए।";
            armIdle();
          }
        };
        // The engine distinguishes taps from drags for mouse and touch, including preventDefault.
        makeDraggable(w, gradeDrop, {onTap:select, onPick:clearSelection});
        w.onkeydown = keyActivate(select);
        w.addEventListener("mousedown", ()=> clearTimeout(idleT)); w.addEventListener("touchstart", ()=> clearTimeout(idleT), { passive: true });
      });
      async function complete(){
        finished = true; clearTimeout(idleT);
        try{
          await mtgWait(700, tok);
          SwiftPAL.emit("space_round_done", { slide_id: slide.id, step: L.step, round: r + 1 });
          const voDone = say(g.round_done_vo);
          for(let i = 0; i < 5; i++){ mtgPulse(nums[i], "glow", 700); await mtgWait(260, tok); }
          confettiCannon();
          podEls.forEach((p, i)=> setTimeout(()=> p.classList.add("fly"), 150 + i * 90));
          walkers.filter(w => !w.classList.contains("snapped")).forEach(w => w.classList.add("leave"));
          await voDone; await mtgWait(900, tok);
          resolve();
        } catch(e){ reject(e); }
      }
      mtgRun(async()=>{
        await mtgWait(300, tok);
        mtgPulse(nums[0], "glow", 1600);     // the first number glows as it is mentioned
        busyVo = true; await say(R.vo); busyVo = false;
        if(r === 0){ ghost(); busyVo = true; await say(g.guide_vo); busyVo = false; }
        armIdle();
      });
    });
  }

  async function runLevel(i){
    const L = g.levels[i];
    try{
      for(let r = 0; r < L.rounds.length; r++) await round(L, r);
    } catch(e){ if(e !== MTG_STOP) console.error(e); return; }
    done.add(i);
    menu();
    mtgRun(async()=>{
      if(done.size < g.levels.length){ await say(L.done); return; }
      await say(g.all_done_vo);
      await mtgWait(600, tok);
      root.remove();
      $("stage").classList.remove("mtg-game"); document.body.classList.remove("mtg-game");
      completeSlide(true);
    });
  }

  menu();
  mtgRun(async()=>{ await mtgWait(400, tok); await say(g.menu_vo); });
}};
/* leaving the game by any other route (dev jump) must not strand the full-screen layer */
(function(){ const _m = mountSlide; window.mountSlide = mountSlide = function(i){
  _mtgTok++;
  if(CARD.slides[i] && CARD.slides[i].type !== "SPACE_PODS"){ document.querySelectorAll(".sp-root, .sf-hint-ov").forEach(e => e.remove()); $("stage").classList.remove("mtg-game"); document.body.classList.remove("mtg-game"); }
  return _m(i);
}; })();
