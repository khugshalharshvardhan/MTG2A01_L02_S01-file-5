"""Visual and input regression checks for the refreshed lesson. Audio timing is stubbed.
Serve 3_BUILD on port 8931, then run: python -X utf8 1_SPEC/_verify_visual_refresh.py
"""
from pathlib import Path
import json, time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'5_SCREENSHOTS/visual_refresh'
OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8931/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions()
o.add_argument('--headless=new')
o.add_argument('--autoplay-policy=no-user-gesture-required')
o.set_capability('goog:loggingPrefs', {'browser':'ALL'})
d=webdriver.Chrome(options=o)
checks=[]
def js(code,*args): return d.execute_script(code,*args)
def wait(code): return WebDriverWait(d,40).until(lambda _:js('return '+code))
def check(name,result):
    checks.append([name,bool(result)])
    print(('PASS ' if result else 'FAIL ')+name,flush=True)
def shot(name): d.save_screenshot(str(OUT/(name+'.png')))
def metrics(w,h,dpr=1):
    d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':dpr,'mobile':False})
def go(slide):
    d.get(URL+('?slide='+str(slide) if slide is not None else ''))
def pair():
    return js("""const R=CARD.slides[10].data.levels[0].rounds[0];
    const i=[...document.querySelectorAll('.sp-pod')].findIndex(p=>!p.classList.contains('filled'));
    const p=document.querySelectorAll('.sp-pod')[i];
    const w=[...document.querySelectorAll('.sp-astro.walker:not(.snapped)')].find(w=>+w.dataset.n===R.seq[i]);
    return [w,p];""")
STUB="""HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();"""
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB+"window.__pondAudit={samples:0,outside:0,anchorErrors:0,cameraFrames:0};\n(function frame(){\n const v=document.querySelector('.br-view'), f=document.querySelector('.br-frog'), w=document.querySelector('.br-world'),a=window.__pondAudit;\n if(v&&f&&w){\n  if(f.classList.contains('hopping')){\n   a.samples++;const r=f.getBoundingClientRect(),b=v.getBoundingClientRect();\n   if(r.left<b.left-2||r.right>b.right+2||r.top<b.top-2||r.bottom>b.bottom+2)a.outside++;\n  }\n  if(w.dataset.cameraMoving==='true'){\n   a.cameraFrames++;const m=new DOMMatrix(getComputedStyle(w).transform);\n   if(Math.abs(m.f+194*m.a-194)>.2)a.anchorErrors++;\n  }\n }\n requestAnimationFrame(frame);\n})();"})
try:
    metrics(1333,750)
    go(None)
    wait("document.body.classList.contains('loaded') && !document.getElementById('sgBtn').disabled")
    time.sleep(1)
    check('cover uses new pond',js("return getComputedStyle(document.querySelector('.fc-pond')).backgroundImage.includes('sc_pond_v2')"))
    check('cover has two distinct resting frogs',js("const f=document.querySelector('.fc-frog').getBoundingClientRect(),g=document.querySelector('.fc-friend').getBoundingClientRect();return f.right<g.left && document.querySelectorAll('.fc-leaf').length===5"))
    check('cover has a labelled Start button',js("return document.getElementById('sgBtn').textContent.includes('\\u0936\\u0941\\u0930\\u0942')"))
    check('Start label is visible at a readable size',js("const b=document.getElementById('sgBtn');return parseFloat(getComputedStyle(b).fontSize)>=24 && b.getBoundingClientRect().width>=200"))
    shot('01_cover')
    go(0)
    wait("document.querySelector('.br-view')")
    check('pond background belongs to viewport, not camera world',js("return getComputedStyle(document.querySelector('.br-view')).backgroundImage.includes('sc_pond_v2') && !document.querySelector('.br-world .br-pond')"))
    wait("!document.getElementById('navBtn').disabled")
    check('pond does not overlap teaching heading',js("const t=document.querySelector('.br-card .tut-prompt').getBoundingClientRect(),v=document.querySelector('.br-view').getBoundingClientRect();return v.top>=t.bottom-1"))
    check('2s hops stay inside pond on every sampled frame',js("return __pondAudit.samples>30 && __pondAudit.outside===0"))
    check('both frogs have separate space at final landing',js("const a=document.querySelector('.br-frog').getBoundingClientRect(),b=document.querySelector('.br-friend').getBoundingClientRect();return b.left-a.right>20"))
    check('friend rests on its own lotus leaf',js("const a=document.querySelector('.br-friend').getBoundingClientRect(),b=document.querySelector('.br-rest-leaf').getBoundingClientRect();return Math.abs(a.bottom-b.top)<8 && a.left>=b.left && a.right<=b.right"))
    check('all numbered resting places are lotus leaves',js("return [...document.querySelectorAll('.br-rock img')].every(i=>i.src.includes('prop_lotus.svg'))"))
    check('landing numbers are larger than skipped numbers',js("return parseFloat(getComputedStyle(document.querySelector('.br-num.big')).fontSize)>parseFloat(getComputedStyle(document.querySelector('.br-num:not(.big)')).fontSize)*1.2"))
    shot('02_pond_2s')
    go(1)
    wait("!!document.querySelector('.br-frog.tappable')")
    js("document.querySelector('.br-frog.tappable').click()")
    wait("!!document.querySelector('.br-frog.tappable')")
    js("document.querySelector('.br-frog.tappable').click()")
    wait("!document.getElementById('navBtn').disabled")
    check('5s hops stay inside pond on every sampled frame',js("return __pondAudit.samples>30 && __pondAudit.outside===0"))
    check('5s zoom keeps the resting baseline steady',js("return __pondAudit.cameraFrames>20 && __pondAudit.anchorErrors===0"))
    shot('02b_pond_5s')

    go(2)
    wait("!!document.querySelector('.br-frog.tappable')")
    time.sleep(1.2)
    before=js("return document.querySelector('.br-view').getBoundingClientRect().height")
    shot('03_pond_10s_follow')
    for i in range(2):
        js("document.querySelector('.br-frog.tappable').click()")
        if i==0: wait("!!document.querySelector('.br-frog.tappable')")
    wait("!document.getElementById('navBtn').disabled")
    time.sleep(1.3)
    check('pond retains height through full-line recap',abs(before-js("return document.querySelector('.br-view').getBoundingClientRect().height"))<1)
    check('10s hops stay inside pond on every sampled frame',js("return __pondAudit.samples>30 && __pondAudit.outside===0"))
    check('10s zoom keeps the resting baseline steady',js("return __pondAudit.cameraFrames>20 && __pondAudit.anchorErrors===0"))
    check('10s frogs remain separated after recap',js("const a=document.querySelector('.br-frog').getBoundingClientRect(),b=document.querySelector('.br-friend').getBoundingClientRect();return b.left>a.right"))
    shot('04_pond_10s_recap')
    go(6)
    wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
    shot('05_sequence')
    go(10)
    wait("document.querySelectorAll('.sp-card').length===3")
    check('space uses scalable SVG',js("return getComputedStyle(document.querySelector('.sp-root')).backgroundImage.includes('sc_space_v2.svg')"))
    shot('06_space_menu')
    js("document.querySelector('.sp-card').click()")
    wait("document.querySelectorAll('.sp-pod').length===5")
    time.sleep(2)
    check('Hindi instructions intact',js("return document.querySelector('.sp-status').textContent.includes('\\u091c\\u093e\\u0928\\u0935\\u0930') && !document.querySelector('.sp-status').textContent.includes('???')"))
    shot('07_space_round')
    w,p=pair()
    wrong=js("return [...document.querySelectorAll('.sp-pod:not(.filled)')].find(p=>p!==arguments[0])",p)
    w.send_keys(Keys.ENTER);wrong.click();time.sleep(.8)
    check('wrong tap leaves pod empty and animal available',js("return !arguments[0].classList.contains('filled') && !arguments[1].classList.contains('snapped')",wrong,w))
    # Exercise real mouse input through the engine's onTap hook, not an onclick shortcut.
    ActionChains(d).move_to_element(w).click().perform()
    check('mouse tap selects animal',js("return arguments[0].getAttribute('aria-pressed')==='true'",w))
    shot('08_space_selected')
    p.click()
    time.sleep(.8)
    check('mouse tap fills matching pod',js("return arguments[0].classList.contains('filled') && arguments[1].classList.contains('snapped')",p,w))
    w,p=pair()
    w.send_keys(Keys.ENTER)
    check('keyboard selects animal',js("return arguments[0].getAttribute('aria-pressed')==='true'",w))
    p.send_keys(Keys.SPACE)
    time.sleep(.8)
    check('keyboard fills matching pod',js("return arguments[0].classList.contains('filled')",p))
    w,p=pair()
    # Exercise a touchstart/touchend pair; the engine suppresses native clicks on touchstart.
    js("""const w=arguments[0],r=w.getBoundingClientRect(),t=new Touch({identifier:1,target:w,clientX:r.x+r.width/2,clientY:r.y+r.height/2});
    w.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,cancelable:true,touches:[t],changedTouches:[t]}));
    w.dispatchEvent(new TouchEvent('touchend',{bubbles:true,cancelable:true,touches:[],changedTouches:[t]}));""",w)
    check('touch tap selects animal',js("return arguments[0].getAttribute('aria-pressed')==='true'",w))
    p.click();time.sleep(.8)
    check('touch-selected animal can fill matching pod',js("return arguments[0].classList.contains('filled')",p))
    # Confirm rendered assets load at a high-density desktop size.
    metrics(1920,1080,2);time.sleep(.5)
    check('full-HD stage fits viewport',js("const r=document.getElementById('stage').getBoundingClientRect();return r.width<=innerWidth+1 && r.height<=innerHeight+1"))
    check('visible images loaded',js("return [...document.querySelectorAll('.sp-root img')].every(i=>i.complete&&i.naturalWidth>0)"))
    shot('09_space_fullhd_2x')
    metrics(960,540);time.sleep(.5)
    check('small landscape stage fits viewport',js("const r=document.getElementById('stage').getBoundingClientRect();return r.width<=innerWidth+1 && r.height<=innerHeight+1"))
    shot('10_space_small')
    d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
    check('reduced motion stops floating animals',js("return [...document.querySelectorAll('.sp-astro-in')].every(e=>getComputedStyle(e).animationName==='none')"))
    errors=[x['message'] for x in d.get_log('browser') if x['level']=='SEVERE' and 'favicon' not in x['message']]
    check('no browser errors',not errors)
    for error in errors:print(error,flush=True)
finally:
    d.quit()
    (OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
if any(not result for _,result in checks): raise SystemExit(1)
print(str(len(checks))+' visual/input checks passed.',flush=True)
