"""Read-only browser QA of lesson v4. Outputs new receipts/screenshots, never rebuilds.
Audio is simulated for interaction checks; use --real-audio for file decoding checks.
"""
from pathlib import Path
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'5_SCREENSHOTS/lesson_v4';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8941/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required')
o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o)
checks=[]
def js(s,*a):return d.execute_script(s,*a)
def wait(s,timeout=45):return WebDriverWait(d,timeout).until(lambda _:js('return '+s))
def check(n,v):checks.append([n,bool(v)]);print(('PASS ' if v else 'FAIL ')+n,flush=True)
def shot(n):d.save_screenshot(str(OUT/(n+'.png')))
def go(i=None):d.get(URL+('' if i is None else '?slide='+str(i)))
def metrics(w,h):d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
STUB="""
window.__foley=[];
HTMLMediaElement.prototype.play=function(){window.__foley.push(this.src);const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();
window.__audit={samples:0,outside:0};
(function sample(){const f=document.querySelector('.br-frog.hopping,.jp-frog.hopping,.sf-animal.hopping');if(f){const p=f.closest('.br-view,.jp-board,.sf-stage').getBoundingClientRect(),r=f.getBoundingClientRect();window.__audit.samples++;if(r.top<p.top-2||r.bottom>p.bottom+2||r.left<p.left-2||r.right>p.right+2)window.__audit.outside++;}requestAnimationFrame(sample);})();
"""
try:
 if '--real-audio' in sys.argv:
  metrics(1333,750);go(3)
  wait("document.querySelector('.mtg-opt')")
  result=d.execute_async_script("""const done=arguments[arguments.length-1],ac=new AudioContext();Promise.all(['sfx_ref_correct','sfx_ref_wrong','sfx_ref_tap','sfx_frog_hop','sfx_frog_croak','sfx_animal_hop','sfx_water_land'].map(async k=>{const r=await fetch('assets/Audio/'+k+'.ogg');if(!r.ok)throw Error(k);const b=await ac.decodeAudioData(await r.arrayBuffer());return [k,b.duration];})).then(done).catch(e=>done({error:String(e)}));""")
  check('all seven effects decode as real audio',isinstance(result,list) and len(result)==7 and all(x[1]>0 for x in result))
  (OUT/'audio_metadata.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 elif '--controls' in sys.argv:
  d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB})
  for w,h in [(1333,750),(960,540)]:
   metrics(w,h)
   for idx in range(3,10):
    go(idx);wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)");time.sleep(.75)
    sid=js('return CARD.slides[state.idx].id')
    check(f'{w}: {sid} removed sound control stays absent',js("return !document.querySelector('.mtg-sound-toggle')"))
    shot(f'{w}_{sid}')
 else:
  d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB})
  for w,h in [(1333,750),(960,540)]:
   metrics(w,h);go();wait("document.querySelector('.fc-pond') && window.__ltReady && !document.getElementById('sgBtn').disabled && [...document.querySelectorAll('.fc-pond img')].every(i=>i.complete&&i.naturalWidth>0)")
   check(f'{w}: cover artwork fills reference frame',js("const p=document.querySelector('.fc-pond').getBoundingClientRect(),c=document.querySelector('.fc-card'),r=c.getBoundingClientRect(),s=r.width/c.offsetWidth;return Math.abs(p.width-c.clientWidth*s)<2&&Math.abs(p.top-r.top-8*s)<2"))
   check(f'{w}: frogs supported by enlarged leaves',js("const s=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--scale'));return [...document.querySelectorAll('.fc-frog,.fc-friend')].every(f=>{const leaf=[...document.querySelectorAll('.fc-leaf')].find(l=>Math.abs(l.offsetLeft-f.offsetLeft)<1),r=f.getBoundingClientRect(),b=leaf.getBoundingClientRect();return b.width>r.width&&r.bottom>=b.top&&r.bottom<b.bottom;})"))
   shot(f'{w}_cover')
   for idx,taps in [(0,0),(1,2),(2,2)]:
    go(idx);wait("document.querySelector('.br-frog')")
    check(f'{w}: T{idx+1} full bleed picture',js("const p=document.querySelector('.br-view').getBoundingClientRect(),c=document.querySelector('.br-card').getBoundingClientRect(),s=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--scale'));return Math.abs(p.left-c.left-10*s)<2&&Math.abs(p.right-c.right+10*s)<2&&Math.abs(p.top-c.top-10*s)<2"))
    check(f'{w}: T{idx+1} equal number containers',js("const a=[...document.querySelectorAll('.br-num')];return new Set(a.map(x=>x.offsetWidth+','+x.offsetHeight)).size===1"))
    for k in range(taps):
     wait("document.querySelector('.br-frog.tappable')")
     check(f'{w}: T{idx+1} hop {k+1} stays readable',js("return document.querySelector('.br-frog').getBoundingClientRect().width/(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--scale')))>=90"))
     shot(f'{w}_T{idx+1}_tap{k+1}')
     frog=d.find_element('css selector','.br-frog.tappable');frog.send_keys(Keys.ENTER)
    wait("!document.getElementById('navBtn').disabled",75)
    check(f'{w}: T{idx+1} finishes with authored text',js("const c=document.querySelector('.br-cap');return c.textContent.includes(CARD.assets.audio_text[c.dataset.clip])"))
    check(f'{w}: T{idx+1} every hop frame inside picture',js('return __audit.samples>0&&__audit.outside===0'))
    check(f'{w}: T{idx+1} hop, croak and water sounds',js("return ['sfx_frog_hop','sfx_frog_croak','sfx_water_land'].every(n=>__foley.some(x=>x.includes(n)))"))
    shot(f'{w}_T{idx+1}_recap')
   for idx in range(3,10):
    go(idx);wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)");time.sleep(.75)
    sid=js('return CARD.slides[state.idx].id')
    check(f'{w}: {sid} natural animal loaded',js("const a=document.querySelector('.jp-frog,.sf-animal');return a.src.includes('/lesson_')&&a.complete&&a.naturalWidth>0"))
    if idx<6:
     check(f'{w}: {sid} activity vertically centred',js("const h=document.getElementById('slideHost').getBoundingClientRect(),a=document.querySelector('.jp-board').getBoundingClientRect(),b=document.querySelector('.mtg-opts').getBoundingClientRect();return Math.abs((a.top+b.bottom)/2-(h.top+h.bottom)/2)<12"))
    shot(f'{w}_{sid}')
    answers=js('const a=CARD.slides[state.idx].data;return a.blanks?a.blanks.map(b=>b.answer):[a.answer]')
    for bi,answer in enumerate(answers):
     for attempt in range(3):
      wrong=js("return [...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled&&+b.dataset.v!==arguments[0]).dataset.v",answer)
      js("[...document.querySelectorAll('.mtg-opt')].find(b=>b.dataset.v===arguments[0]).click()",wrong)
      wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
     check(f'{w}: {sid} blank {bi+1} third-attempt lock',js("const a=[...document.querySelectorAll('.mtg-opt')].filter(b=>!b.classList.contains('used'));return a.filter(b=>!b.disabled).length===1&&a.filter(b=>b.disabled).every(b=>b.classList.contains('faded'))"))
     js("[...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled&&+b.dataset.v===arguments[0]).click()",answer)
     if bi<len(answers)-1:wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
     else:wait(f"state.idx!=={idx}")
    check(f'{w}: {sid} all hop frames inside activity',js('return __audit.samples>0&&__audit.outside===0'))
    check(f'{w}: {sid} File9 feedback audio requested',js("return ['sfx_ref_correct','sfx_ref_wrong','sfx_ref_tap'].every(n=>__foley.some(x=>x.includes(n)))"))
   go(0);wait("document.querySelector('.br-frog')")
   check(f'{w}: effects toggle remains removed',js("return !document.querySelector('.mtg-sound-toggle')"))
  # No game code/art changes, but confirm the same cast and round plan remain available.
  go(10);wait("document.querySelectorAll('.sp-card').length===3")
  check('space game keeps three astronaut casts and nine rounds',js("return CARD.slides[10].data.levels.every(x=>x.cast.startsWith('sp_')&&x.rounds.length===3)"))
  shot('space_game_unchanged')
  d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
  go(2)
  for _ in range(2):
   wait("document.querySelector('.br-frog.tappable')");js("document.querySelector('.br-frog.tappable').click()")
  wait("!document.getElementById('navBtn').disabled")
  check('reduced motion completes long sequence without flight effects',js("return !document.querySelector('.hopping,.br-splash,.mtg-hop-shadow')&&document.querySelector('.br-view').dataset.landedAt==='50'"))
  errors=[x for x in d.get_log('browser') if x['level']=='SEVERE']
  (OUT/'browser_errors.json').write_text(json.dumps(errors,indent=2),encoding='utf8')
  check('no browser console errors',not errors)
finally:
 (OUT/('real_audio_results.json' if '--real-audio' in sys.argv else 'controls_results.json' if '--controls' in sys.argv else 'results.json')).write_text(json.dumps(checks,indent=2),encoding='utf8')
 d.quit()
if any(not ok for _,ok in checks):sys.exit(1)
