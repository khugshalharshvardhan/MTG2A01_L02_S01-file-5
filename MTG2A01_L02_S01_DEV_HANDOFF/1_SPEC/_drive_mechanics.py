"""Behavioural walk of every interactive screen (QA). Audio is stubbed to end in ~60 ms so the walk
measures the logic, not the clip lengths. Screenshots of each key state go to <outdir>.
    python _drive_mechanics.py <outdir>
"""
import sys, os, time, json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
URL = "http://127.0.0.1:8931/MTG2A01_L02_S01.html"
STUB = """
HTMLMediaElement.prototype.play = function(){ const a = this; setTimeout(()=>{ try{ a.dispatchEvent(new Event('ended')); }catch(e){} }, 60); return Promise.resolve(); };
/* the engine plays VO through Web Audio: every decoded clip becomes 60 ms of silence */
(function(){ const AC = window.AudioContext || window.webkitAudioContext; if(!AC) return;
  AC.prototype.decodeAudioData = function(){ return Promise.resolve(this.createBuffer(1, 1440, 24000)); }; })();
"""
o = webdriver.ChromeOptions()
o.add_argument("--headless=new"); o.add_argument("--window-size=1333,750")
o.add_argument("--autoplay-policy=no-user-gesture-required")
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o)
d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": STUB})
results = []


def shot(name):
    d.save_screenshot(os.path.join(OUT, name + ".png"))


def js(s, *a):
    return d.execute_script(s, *a)


def until(cond, timeout=40, step=0.15):
    t = time.time()
    while time.time() - t < timeout:
        if js("return " + cond):
            return True
        time.sleep(step)
    return False


def ok(name, cond):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)


def go(i):
    d.get(URL + f"?slide={i}")
    time.sleep(0.6)


NAV_ON = "!document.getElementById('navBtn').disabled"
NAV_SHOWN = NAV_ON + " && !document.body.classList.contains('auto-next')"

# ---------- file4 shell: cover play button + the first transition ----------
d.get(URL); time.sleep(0.8)
ok("cover: play button becomes tappable", until("!document.getElementById('sgBtn').disabled", 20))
time.sleep(5.6)
ok("cover: idle pulse after ~5 s", js("return !!document.querySelector('.idle-pulse')"))
shot("SHELL_cover_idle")
js("document.getElementById('sgBtn').click()")
ok("transition Swifty (peek-up) opens after play", until("document.getElementById('phaseGate').classList.contains('show')", 6))
time.sleep(1.2); shot("SHELL_gate_tutorial")
ok("T1 mounts after the transition", until("state.idx===0 && !document.getElementById('phaseGate').classList.contains('show')", 20))

# ---------- teach screens ----------
for i, taps in ((0, 0), (1, 2), (2, 2)):
    go(i)
    for k in range(taps):
        ok(f"T{i+1} tap {k+1} offered", until("!!document.querySelector('.br-frog.tappable')", 60))
        if k == 0:
            shot(f"T{i+1}_tapwait")
        js("document.querySelector('.br-frog.tappable').click()")
    ok(f"T{i+1} आगे shown + enabled at end", until(NAV_SHOWN, 60))
    time.sleep(0.8)
    shot(f"T{i+1}_end")
    ok(f"T{i+1} jumps drawn", js("return document.querySelectorAll('.br-svg .mtg-arc').length") >= 5)
    if i == 2:
        js("document.getElementById('navBtn').click()")
        ok("T3 आगे → guided transition", until("document.getElementById('phaseGate').classList.contains('show')", 8))
        time.sleep(1.0); shot("SHELL_gate_guided")
        ok("guided transition → G1", until("state.idx===3 && !document.getElementById('phaseGate').classList.contains('show')", 25))

# ---------- JUMP_PICK ----------
for i, wrong, right in ((3, 51, 55), (4, 15, 16), (5, 35, 40)):
    go(i)
    ok(f"G{i-2} options live", until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)", 30))
    for k in range(3):
        js(f"[...document.querySelectorAll('.mtg-opt')].find(b=>b.dataset.v=='{wrong}').click()")
        time.sleep(0.3)
        until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)", 20)
        if k == 1:
            pass
    ok(f"G{i-2} WA3 fades the wrong options", js("return document.querySelectorAll('.mtg-opt.faded').length") == 2)
    ok(f"G{i-2} WA3 guides the answer", js(f"return !!document.querySelector('.mtg-opt.guide[data-v=\"{right}\"]')"))
    shot(f"G{i-2}_wa3")
    js(f"document.querySelector('.mtg-opt[data-v=\"{right}\"]').click()")
    ok(f"G{i-2} आगे hidden on a question page", js("return document.body.classList.contains('auto-next')"))
    time.sleep(0.5); shot(f"G{i-2}_correct")
    ok(f"G{i-2} correct → moves on by itself", until(f"state.idx==={i+1}", 25))

# ---------- SEQ_FILL ----------
for i, plan in ((6, [(38, 40)]), (7, [(18, 17), (20, 19)]), (8, [(70, 66), (75, 80)]), (9, [(70, 61), (90, 75)])):
    go(i)
    ok(f"G{i-2} options live", until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)", 40))
    if i == 6:
        shot("G4_question")
    for bi, (right, wrong) in enumerate(plan):
        js(f"document.querySelector('.mtg-opt[data-v=\"{wrong}\"]').click()")       # WA1
        time.sleep(0.3); until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)", 20)
        js(f"document.querySelector('.mtg-opt[data-v=\"{wrong}\"]').click()")       # WA2 → hint popup
        ok(f"G{i-2} blank {bi+1} hint popup opens", until("!!document.querySelector('.sf-hint-ov.show')", 10))
        time.sleep(1.8)
        if bi == 0:
            shot(f"G{i-2}_hint")
        ok(f"G{i-2} blank {bi+1} hint closes by itself", until("!document.querySelector('.sf-hint-ov')", 12))
        until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)", 20)
        js(f"document.querySelector('.mtg-opt[data-v=\"{wrong}\"]').click()")       # WA3
        time.sleep(0.3); until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)", 20)
        ok(f"G{i-2} blank {bi+1} WA3 guides {right}", js(f"return !!document.querySelector('.mtg-opt.guide[data-v=\"{right}\"]')"))
        js(f"document.querySelector('.mtg-opt[data-v=\"{right}\"]').click()")
        time.sleep(0.4)
        until(f"document.querySelector('.mtg-opt[data-v=\"{right}\"]').classList.contains('used')", 10)
        until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled) || " + NAV_ON, 20)
    time.sleep(0.3); shot(f"G{i-2}_done")
    if i == 9:
        ok("G7 → practice transition before the game", until("document.getElementById('phaseGate').classList.contains('show')", 25))
        time.sleep(1.0); shot("SHELL_gate_practice")
        ok("G7 → game mounts after the transition", until("state.idx===10 && !document.getElementById('phaseGate').classList.contains('show')", 25))
    else:
        ok(f"G{i-2} all blanks filled → moves on by itself", until(f"state.idx==={i+1}", 25))

# ---------- SPACE_PODS ----------
go(10)
time.sleep(1.0); shot("GAME_menu")
DRAG = """
const [tile, pod] = arguments;
const r = tile.getBoundingClientRect(), p = pod.getBoundingClientRect();
const sx = r.left + r.width/2, sy = r.top + r.height/2, tx = p.left + p.width/2, ty = p.top + p.height/2;
tile.dispatchEvent(new MouseEvent('mousedown', {bubbles:true, clientX:sx, clientY:sy}));
document.dispatchEvent(new MouseEvent('mousemove', {bubbles:true, clientX:(sx+tx)/2, clientY:(sy+ty)/2}));
document.dispatchEvent(new MouseEvent('mousemove', {bubbles:true, clientX:tx, clientY:ty}));
document.dispatchEvent(new MouseEvent('mouseup', {bubbles:true, clientX:tx, clientY:ty}));
"""
for lv in range(3):
    js(f"document.querySelectorAll('.sp-card')[{lv}].click()")
    for rnd in range(3):
        ok(f"GAME L{lv+1} R{rnd+1} pods shown", until(f"document.querySelectorAll('.sp-pod').length===5 && !document.querySelector('.sp-pod.fly') && document.querySelectorAll('.sp-pod.filled').length===CARD.slides[10].data.levels[{lv}].rounds[{rnd}].prefilled.length && [...document.querySelectorAll('.sp-podnum')][0].textContent==String(CARD.slides[10].data.levels[{lv}].rounds[{rnd}].seq[0])", 30))
        time.sleep(0.5)
        if lv == 0 and rnd == 0:
            shot("GAME_round")
        # one wrong drop: a distractor (or a correct animal on the wrong pod)
        seq = js("return [...document.querySelectorAll('.sp-pod')].map(p=>p.classList.contains('filled'))")
        empty = [k for k, f in enumerate(seq) if not f]
        walkers = js("return [...document.querySelectorAll('.sp-astro.walker:not(.snapped)')].map(w=>+w.dataset.n)")
        need = js("return arguments[0]", None)
        if rnd == 0:
            pod = js(f"return document.querySelectorAll('.sp-pod')[{empty[0]}]")
            wrong = js(f"return [...document.querySelectorAll('.sp-astro.walker')].find(w=>!w.classList.contains('snapped'))")
            js(DRAG, wrong, pod)   # may or may not be right — the next loop fixes everything
            time.sleep(0.25)
            if lv == 0:
                shot("GAME_wrongdrop")
        # fill the rest correctly
        for _ in range(8):
            pods = js("return [...document.querySelectorAll('.sp-pod')]")
            target = js("""
              const pods=[...document.querySelectorAll('.sp-pod')];
              const lvl = arguments[0];
              return pods.findIndex(p=>!p.classList.contains('filled'));""", lv)
            if target < 0:
                break
            n = js("""
              const card = CARD.slides[10].data.levels[arguments[0]].rounds[arguments[1]];
              return card.seq[arguments[2]];""", lv, rnd, target)
            tile = js(f"return [...document.querySelectorAll('.sp-astro.walker')].find(w=>+w.dataset.n==={n} && !w.classList.contains('snapped'))")
            js(DRAG, tile, pods[target])
            time.sleep(0.3)
        ok(f"GAME L{lv+1} R{rnd+1} all pods filled", js("return [...document.querySelectorAll('.sp-pod')].every(p=>p.classList.contains('filled'))"))
        if lv == 0 and rnd == 0:
            time.sleep(0.4); shot("GAME_roundfull")
    ok(f"GAME L{lv+1} back to menu with badge", until(f"!!document.querySelectorAll('.sp-card')[{lv}] && document.querySelectorAll('.sp-card')[{lv}].classList.contains('done')", 30))
    if lv == 0:
        time.sleep(0.5); shot("GAME_menu_badge")
ok("GAME all levels → celebration", until("CARD.slides[state.idx].type==='CELEBRATION'", 30))
time.sleep(2); shot("CEL")
errs = [l["message"] for l in d.get_log("browser") if l["level"] == "SEVERE" and "favicon" not in l["message"]]
ok("no console errors", not errs)
for e in errs[:10]:
    print("  ", e)
d.quit()
print(f"\n{sum(1 for _, v in results if v)} pass · {sum(1 for _, v in results if not v)} FAIL")
json.dump(results, open(os.path.join(OUT, "_results.json"), "w"), indent=1)
