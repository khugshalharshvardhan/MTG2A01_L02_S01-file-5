"""Interaction refinement acceptance checks. Uses short silent audio; visual timing is real."""
from pathlib import Path
import json,time,os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'5_SCREENSHOTS/interaction_refinement';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8934/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required')
o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o);d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':1333,'height':750,'deviceScaleFactor':1,'mobile':False})
STUB="""HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();
window.__arcs=[];window.__segments=[];let last='';
(function frame(){
 document.querySelectorAll('.mtg-arc[data-animating="true"]').forEach(g=>{const t=+g.dataset.progress;if(t>.05&&t<.95)__arcs.push({t,d:g.querySelector('.mtg-arc-path').getAttribute('d'),head:g.querySelector('.mtg-arc-head').getAttribute('d')});});
 const line=[...document.querySelectorAll('.jp-nl .nl-seg.lit')].map(p=>p.getAttribute('d')).join('|');
 if(line!==last){__segments.push({time:performance.now(),line});last=line;}
 requestAnimationFrame(frame);
})();"""
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB})
checks=[]
def js(s,*args):
 for q in ["document.querySelectorAll('.sp-pod","document.querySelector('.sp-pod","document.querySelectorAll('.walker","document.querySelector('.walker","document.querySelector('.sp-ground"]:
  s=s.replace(q,q.replace('document.','current.'))
 return d.execute_script("const current=document.querySelector('.sp-scene.active')||document;"+s,*args)
def wait(s,seconds=40):return WebDriverWait(d,seconds,poll_frequency=.05).until(lambda _:js('return '+s))
def ok(name,value):
 checks.append([name,bool(value)]);print(('PASS ' if value else 'FAIL ')+name,flush=True)
def go(i):d.get(URL+'?slide='+str(i))
def live():wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
def click(n):js("document.querySelector('.mtg-opt[data-v=\"'+arguments[0]+'\"]').click()",n)
def shot(name):d.save_screenshot(str(OUT/(name+'.png')))
try:
 for i in range(3):
  go(i);wait("document.querySelectorAll('.br-num').length>0")
  ok(f'T{i+1} initial numbers have equal size and weight',js("const a=[...document.querySelectorAll('.br-num')].map(e=>{const s=getComputedStyle(e);return s.fontSize+':'+s.fontWeight});return new Set(a).size===1&&!document.querySelector('.br-num.mark')"))
  ok(f'T{i+1} pad centres align with equal consecutive spacing',js("const r=[...document.querySelectorAll('.br-rock')].map(e=>[parseFloat(e.style.left),parseFloat(e.style.top)+parseFloat(e.style.height)/2]);const dx=r[1][0]-r[0][0];return r.every((v,k)=>Math.abs(v[1]-r[0][1])<1&&(!k||Math.abs(v[0]-r[k-1][0]-dx)<1))"))
  for _ in range(2 if i else 0):
   wait("document.querySelector('.br-frog.tappable')",65);js("document.querySelector('.br-frog.tappable').click()")
  wait("!document.getElementById('navBtn').disabled",65);time.sleep(.8)
  ok(f'T{i+1} all visited labels retain equal emphasis',js("const d=CARD.slides[state.idx].data;const a=[...document.querySelectorAll('.br-num.mark')];const styles=a.map(e=>{const s=getComputedStyle(e);return s.fontSize+':'+s.fontWeight});return a.length===(d.hi-d.lo)/d.step+1&&new Set(styles).size===1&&[...document.querySelectorAll('.br-num:not(.mark)')].every(e=>!e.classList.contains('big'))"))
  ok(f'T{i+1} pads return to their resting position and size',js("return [...document.querySelectorAll('.br-rock')].every(e=>{const m=new DOMMatrix(getComputedStyle(e).transform);return Math.abs(m.a-1)<.001&&Math.abs(m.d-1)<.001&&Math.abs(m.e+e.getBoundingClientRect().width/(parseFloat(getComputedStyle(document.querySelector('.br-world')).getPropertyValue('--z'))||1)/2)<1})"))
  ok(f'T{i+1} arrow grows through ascent and descent',js("const a=__arcs;return a.some(v=>v.t<.4)&&a.some(v=>v.t>.6)&&a.every(v=>v.d.includes(' Q')&&!v.d.includes('NaN'))"))
  ok(f'T{i+1} recap number labels do not overlap',js("const a=[...document.querySelectorAll('.br-num')].map(e=>e.getBoundingClientRect());return a.every((r,k)=>!k||r.left>=a[k-1].right-.5)"))
  shot('teaching_'+str(i+1))
 for i in [3,4,5]:
  go(i);live()
  ok(f'G{i-2} future labels remain uniform',js("const d=CARD.slides[state.idx].data;const a=[...document.querySelectorAll('.nl-lbl:not(.landed)')].map(e=>{const s=getComputedStyle(e);return s.fontSize+':'+s.fontWeight});return new Set(a).size===1&&!document.querySelector('.nl-lbl.landed')?.textContent.includes(String(d.answer))"))
  data=js("return CARD.slides[state.idx].data");wrong=next(n for n in data['options'] if n!=data['answer'])
  click(wrong);time.sleep(.15);live();click(wrong)
  wait("document.querySelector('.nl-seg.lit')",10)
  ok(f'G{i-2} golden hint matches axis thickness',js("return getComputedStyle(document.querySelector('.nl-seg.lit')).strokeWidth===getComputedStyle(document.querySelector('.nl-axis')).strokeWidth"))
  live()
  samples=js("return __segments.filter(s=>s.line)")
  ok(f'G{i-2} one unit at a time for approximately one second',len(samples)==data['answer']-data['at'] and all('|' not in s['line'] for s in samples) and all(850<samples[k+1]['time']-samples[k]['time']<1250 for k in range(len(samples)-1)))
  click(data['answer']);wait("document.querySelector('.jp-frog.hopping')")
  # Capture the complete landing state atomically, before the automatic departure.
  landing=wait("(()=>{const a=[...document.querySelectorAll('.nl-lbl.landed')];return a.some(e=>+e.textContent==="+str(data['answer'])+")?a.map(e=>({n:+e.textContent,size:getComputedStyle(e).fontSize,weight:getComputedStyle(e).fontWeight})):false})()")
  expected=set(data['prior']+[data['answer']])
  ok(f'G{i-2} landing becomes bold while earlier landings remain',expected.issubset({x['n'] for x in landing}) and len({x['size']+':'+x['weight'] for x in landing})==1)
 for i in range(6,10):
  go(i);live();data=js("return CARD.slides[state.idx].data")
  for bi,bl in enumerate(data['blanks']):
   wrong=next(n for n in data['options'] if n!=bl['answer'] and n not in [b['answer'] for b in data['blanks'][:bi]])
   click(wrong);time.sleep(.15);live();click(wrong)
   wait("document.querySelector('.sf-hint-ov.show')",10)
   ok(f'G{i-2} blank {bi+1} starts with a completed preceding jump',js("const arcs=[...document.querySelectorAll('.sf-hint .mtg-arc')];const labels=[...document.querySelectorAll('.sf-hint .nl-lbl')];return arcs.length===1&&arcs[0].dataset.progress==='1.000'&&labels.some(e=>+e.textContent===arguments[0])&&labels.some(e=>+e.textContent===arguments[1]&&e.classList.contains('landed'))",bl['from']-bl['step'],bl['from']))
   wait("document.querySelectorAll('.sf-hint .mtg-arc').length===2");time.sleep(.3)
   ok(f'G{i-2} blank {bi+1} next arrow animates on the curve',js("const a=document.querySelectorAll('.sf-hint .mtg-arc')[1];return +a.dataset.progress>0&&+a.dataset.progress<1&&a.querySelector('.mtg-arc-path').getAttribute('d').includes(' Q')"))
   time.sleep(.7);shot(f'G{i-2}_hint_{bi+1}')
   wait("!document.querySelector('.sf-hint-ov')",12);live();click(bl['answer']);time.sleep(.4)
   ok(f'G{i-2} blank {bi+1} used option leaves no empty slot',js("const cells=[...document.querySelectorAll('.mtg-opt:not(.used)')],r=cells.map(c=>c.getBoundingClientRect());return getComputedStyle(document.querySelector('.mtg-opt.used')).display==='none'&&r.every((v,k)=>!k||Math.abs(v.left-r[k-1].right-parseFloat(getComputedStyle(document.querySelector('.mtg-opts')).gap)*parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--scale')))<2)"))
   if bi+1<len(data['blanks']):live()
 go(10);wait("document.querySelectorAll('.sp-card').length===3");shot('space_menu')
 ok('playful space artwork loads',js("return getComputedStyle(document.querySelector('.sp-cosmos')).backgroundImage.includes('sc_space_playful.svg')"))
 js("document.querySelector('.sp-card').click()");wait("document.querySelector('.sp-ground')")
 first=js("return [...document.querySelectorAll('.walker')].map(w=>parseFloat(w.style.left))");time.sleep(.3)
 second=js("return [...document.querySelectorAll('.walker')].map(w=>parseFloat(w.style.left))")
 ok('animals enter across the screen',any(abs(a-b)>30 for a,b in zip(first,second)))
 wait("document.querySelector('.sp-ground').dataset.entering==='false'");time.sleep(.5)
 first=js("return [...document.querySelectorAll('.walker')].map(w=>parseFloat(w.style.left))");time.sleep(.7)
 second=js("return [...document.querySelectorAll('.walker')].map(w=>parseFloat(w.style.left))")
 ok('correct animals and distractors move gently',all(abs(a-b)>.1 for a,b in zip(first,second)))
 w=js("return document.querySelector('.walker')")
 js("arguments[0].dispatchEvent(new MouseEvent('mousedown',{bubbles:true,clientX:400,clientY:550}))",w);time.sleep(.1)
 first=js("return [...document.querySelectorAll('.walker')].map(w=>w.style.left)");time.sleep(.4)
 ok('animal positions and bob pause during a drag',first==js("return [...document.querySelectorAll('.walker')].map(w=>w.style.left)") and js("return getComputedStyle(document.querySelector('.walker .sp-astro-in')).animationPlayState==='paused'"))
 js("document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX:10,clientY:400}))")
 shot('space_round')
 d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
 go(10);wait("document.querySelector('.sp-card')");js("document.querySelector('.sp-card').click()");wait("document.querySelector('.walker')");time.sleep(.2)
 first=js("return [...document.querySelectorAll('.walker')].map(w=>w.style.left)");time.sleep(.4)
 ok('reduced motion keeps animals still and immediately available',first==js("return [...document.querySelectorAll('.walker')].map(w=>w.style.left)") and js("return document.querySelector('.sp-ground').dataset.entering==='false'"))
 errs=[e['message'] for e in d.get_log('browser') if e['level']=='SEVERE' and 'favicon' not in e['message']]
 ok('no browser errors',not errs)
 if errs:print(errs[:5])
finally:
 d.quit();(OUT/'acceptance_results.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
 print(f'{sum(v for _,v in checks)}/{len(checks)} checks passed',flush=True)

if any(not v for _,v in checks):raise SystemExit(1)
