/* =====================================================================================
   FROG COVER — file4's cover choreography (the train arrives, its smoke gathers into a cloud, the
   title is written on the cloud with sfx_pop and lands with pop + bell, and only then the greeting,
   with the play button grey until it ends), told with टप्पू: he hops in over the pond stones and
   each hop's splash puff rises into the cloud, then the title is written on it.
   Uses file4's engine hook: defining window.landingTrainReady makes the engine hold the greeting
   (and keep the play button in .sg-waiting) until we call it ready; __ltReady also releases the
   lesson warm-up. Card: CARD.landing_hero = { kind:"frog_cover" } (the engine draws nothing for it).
   ===================================================================================== */
(function frogCover(){
  const hero = CARD.landing_hero;
  if(!hero || hero.kind !== "frog_cover") return;
  window.__ltReady = false;
  window.__ltWaiters = [];
  const ready = ()=>{ if(window.__ltReady) return; window.__ltReady = true;
    const w = window.__ltWaiters.splice(0); w.forEach(f => { try{ f(); }catch(e){} }); };
  window.landingTrainReady = (fn)=>{ if(window.__ltReady) fn(); else window.__ltWaiters.push(fn); };
  const onCover = ()=>{ const g = document.getElementById("startGate"); return !g || !g.classList.contains("hidden"); };
  const tone = (f, ty, d, v)=>{ try{ if(typeof _tone === "function") _tone(f, ty, d, v); }catch(e){} };
  const sfxHop = ()=>{ if(onCover()) tone([380, 560], "sine", 0.14, 0.05); };
  const sfxTitle = ()=>{ if(onCover()) mtgFx("sfx_pop", ()=> tone([620, 980], "sine", 0.16, 0.12), 1.0); };
  const sfxTitleLand = ()=>{ if(!onCover()) return; mtgFx("sfx_pop", null, 1.0); tone([1047, 1319, 1568, 2093], "triangle", 0.62, 0.10); };
  // the cloud: a soft body, a white core behind the words, puffs round the top and the ends
  const PUFFS = [[70,96,92],[150,52,112],[250,26,128],[360,20,132],[468,30,124],[560,62,104],[620,104,76],
                 [24,118,64],[118,124,70],[230,128,74],[350,130,76],[470,128,72],[574,122,66]];
  function build(){
    const card = document.querySelector("#startGate .sg-card"), ttl = $("sgTitle"), heroEl = $("sgHero");
    if(!card || !ttl || !heroEl) return null;
    card.classList.add("fc-card");
    const text = ttl.textContent;
    ttl.textContent = "";
    ttl.classList.add("fc-title");
    const cloud = mtgEl("div", "fc-cloud");
    cloud.appendChild(mtgEl("i", "fc-body"));
    PUFFS.forEach(([x, y, d])=>{ const p = mtgEl("i", "fc-puff");
      p.style.cssText = `left:${x - d/2}px;top:${y - d/2}px;width:${d}px;height:${d}px`;
      p.dataset.cx = x; p.dataset.cy = y; cloud.appendChild(p); });
    cloud.appendChild(mtgEl("i", "fc-core"));
    const word = mtgEl("span", "fc-word", text);
    ttl.appendChild(cloud); ttl.appendChild(word);
    heroEl.innerHTML = "";
    heroEl.classList.add("fc-hero");
    const pond = mtgEl("div", "fc-pond");
    [120, 250, 380, 510, 640].forEach(x => { const s = mtgEl("i", "fc-stone"); s.style.left = x + "px"; pond.appendChild(s); });
    ["l", "r"].forEach(side => { const r = mtgEl("img", "fc-reeds " + side); r.src = mtgImg("prop_reeds"); pond.appendChild(r); });
    const frog = mtgEl("img", "fc-frog"); frog.src = mtgImg("chr_tappu");
    pond.appendChild(frog); heroEl.appendChild(pond);
    return { cloud, word, frog };
  }
  function run(){
    const B = build(); if(!B){ ready(); return; }
    const { cloud, word, frog } = B;
    const LAND = 380;                                         // the middle stone
    const settle = ()=>{ cloud.classList.add("fc-settled"); word.classList.add("fc-static"); frog.style.left = LAND + "px"; };
    const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if(reduce || typeof frog.animate !== "function"){ settle(); ready(); return; }
    const puffs = [...cloud.querySelectorAll(".fc-puff")], fills = [...cloud.querySelectorAll(".fc-body,.fc-core")];
    const path = [880, 640, 510, LAND];
    frog.style.left = path[0] + "px";
    let k = 0;
    const launch = (x)=>{                                     // puffs leave the splash and swell into place
      const sc = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
      const cr = cloud.getBoundingClientRect(), pr = frog.parentNode.getBoundingClientRect();
      const fx = (pr.left - cr.left) / sc + x, fy = (pr.top - cr.top) / sc + 70;
      const take = puffs.splice(0, k >= path.length - 2 ? puffs.length : 4);
      take.forEach((p, i)=>{
        const dx = fx - +p.dataset.cx, dy = fy - +p.dataset.cy;
        p.animate([{ opacity:0, transform:`translate3d(${dx}px,${dy}px,0) scale(.15)` },
                   { opacity:1, offset:.25, transform:`translate3d(${dx * .6}px,${dy * .55 - 30}px,0) scale(.4)` },
                   { opacity:1, transform:"translate3d(0,0,0) scale(1)" }],
                  { duration:1100, delay:i * 90, easing:"cubic-bezier(.3,.1,.25,1)", fill:"both" });
      });
    };
    const writeTitle = ()=>{
      fills.forEach(f => f.animate([{ opacity:0 }, { opacity:1 }], { duration:700, easing:"ease-in-out", fill:"both" }));
      setTimeout(()=>{
        sfxTitle();
        const wa = word.animate([{ clipPath:"inset(-40% 100% -40% 0)" }, { clipPath:"inset(-40% 0% -40% 0)" }],
                                { duration:1300, easing:"cubic-bezier(.42,0,.32,1)", fill:"forwards" });
        let fin = false;
        const done = ()=>{ if(fin) return; fin = true; sfxTitleLand(); mtgPulse(frog, "fc-cheer", 900); setTimeout(ready, 300); };
        wa.onfinish = done; setTimeout(done, 1900);
      }, 650);
    };
    const hopNext = ()=>{
      if(k >= path.length - 1){ writeTitle(); return; }
      const a = path[k], b = path[k + 1];
      sfxHop();
      mtgHop(frog, a, b, 70, 560).then(()=>{ launch(b); mtgPulse(frog, "fc-squash", 260); k++; setTimeout(hopNext, 160); });
    };
    setTimeout(hopNext, 450);
    setTimeout(()=>{ if(!window.__ltReady){ settle(); ready(); } }, 9000);   // never strand the cover
  }
  // build now (boot() writes the title right after this script), but start the hops only once the
  // engine's loading screen has gone (body.loaded) — as file4's train sets off when the cover is seen
  setTimeout(()=>{
    const t0 = Date.now();
    (function wait(){
      if(document.body.classList.contains("loaded") || Date.now() - t0 > 8000){ setTimeout(run, 350); return; }
      setTimeout(wait, 100);
    })();
  }, 0);
})();
