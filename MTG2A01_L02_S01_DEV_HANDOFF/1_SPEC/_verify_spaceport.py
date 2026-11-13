"""Spaceport interaction regression. VO is shortened; decoded clip IDs are recorded."""
from pathlib import Path
import json,time,sys,os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'5_SCREENSHOTS/spaceport';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8942/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required');o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o);checks=[]
def js(s,*a):
 for q in ["document.querySelectorAll('.sp-pod",'document.querySelectorAll(".sp-pod',"document.querySelector('.sp-pod",'document.querySelector(".sp-pod',"document.querySelectorAll('.sp-astro.walker",'document.querySelectorAll(".sp-astro.walker',"document.querySelectorAll('.sp-badge"]:
  s=s.replace(q,q.replace('document.','current.'))
 return d.execute_script("const current=document.querySelector('.sp-scene.active')||document;"+s,*a)
def wait(s,t=40):return WebDriverWait(d,t,poll_frequency=.08).until(lambda _:js('return '+s))
def check(n,v):checks.append([n,bool(v)]);print(('PASS ' if v else 'FAIL ')+n,flush=True)
def shot(n):d.save_screenshot(str(OUT/(n+'.png')))
STUB="""
window.__voices=[];window.__launches=[];window.__ghosts=0;window.__sfx=[];window.__pan=[];const launched=new WeakSet();
const tagged=new WeakMap(),f0=window.fetch;window.fetch=async function(...a){const r=await f0.apply(this,a),u=String(a[0]),f=r.arrayBuffer.bind(r);r.arrayBuffer=async()=>{const b=await f();tagged.set(b,u);return b;};return r;};
HTMLMediaElement.prototype.play=function(){const a=this;if(a.src.includes('sfx_'))__sfx.push(a.src);setTimeout(()=>a.dispatchEvent(new Event('ended')),120);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(data){const b=this.createBuffer(1,4320,24000);b.__url=tagged.get(data)||'';return Promise.resolve(b);};const start=AudioBufferSourceNode.prototype.start;AudioBufferSourceNode.prototype.start=function(...a){if(this.buffer&&this.buffer.__url.includes('/vo_'))__voices.push(this.buffer.__url);return start.apply(this,a);};})();
new MutationObserver(ms=>{for(const m of ms){if(m.type==='attributes'&&m.target.matches('.sp-pod.fly')&&!launched.has(m.target)){launched.add(m.target);__launches.push({t:performance.now(),index:+m.target.dataset.i,count:m.target.closest('.sp-scene').querySelectorAll('.sp-pod.fly').length});}for(const n of m.addedNodes)if(n.nodeType===1&&n.matches('.sp-astro.ghost'))__ghosts++;}}).observe(document,{subtree:true,childList:true,attributes:true,attributeFilter:['class']});
(function sample(){const r=document.querySelector('.sp-root[data-travelling="true"]'),s=document.querySelector('.sp-world'),c=document.querySelector('.sp-cosmos'),n=document.querySelector('.sp-rails'),h=document.querySelector('.sp-fixed-title');if(r&&s&&c&&n&&h)__pan.push({x:new DOMMatrix(getComputedStyle(s).transform).m41,far:new DOMMatrix(getComputedStyle(c).transform).m41,near:new DOMMatrix(getComputedStyle(n).transform).m41,inert:s.querySelector('.active').inert,scenes:s.children.length,heading:h.getBoundingClientRect().left,launches:s.querySelectorAll('.active .fly').length});requestAnimationFrame(sample);})();
"""
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB})
READY="document.querySelector('.sp-root[data-playable=\"true\"][data-narrating=\"false\"]')&&!document.querySelector('.sp-pod.fly')&&!document.body.classList.contains('vo-lock')"
DRAG="""
const tile=arguments[0],zone=arguments[1],s=tile.getBoundingClientRect(),t=zone.getBoundingClientRect();
const sx=s.left+s.width/2,sy=s.top+s.height/2,tx=t.left+t.width/2,ty=t.top+t.height/2;
tile.dispatchEvent(new MouseEvent('mousedown',{bubbles:true,clientX:sx,clientY:sy}));
document.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:(sx+tx)/2,clientY:(sy+ty)/2}));
document.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:tx,clientY:ty}));
document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX:tx,clientY:ty}));
"""
try:
 d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':1333,'height':750,'deviceScaleFactor':1,'mobile':False})
 d.get(URL+'?slide=10');wait("document.querySelectorAll('.sp-card').length===3");time.sleep(1);shot('menu')
 check('menu: three distinct astronaut animals loaded',js("const a=[...document.querySelectorAll('.sp-card-animal')];return new Set(a.map(x=>x.src)).size===3&&a.every(x=>x.complete&&x.naturalWidth>0)"))
 check('speaker, Swifty and round counter removed',js("return !document.querySelector('.sp-audio,.sp-swiftie,.sp-round')"))
 for lv in range(3):
  js("document.querySelectorAll('.sp-card')[arguments[0]].click()",lv)
  wait("document.querySelector('.sp-world')");js("window.__world=document.querySelector('.sp-world');window.__heading=document.querySelector('.sp-fixed-title');window.__headingX=__heading.getBoundingClientRect().left")
  for rnd in range(3):
   label=f'L{lv+1} R{rnd+1}'
   wait(f"document.querySelector('.sp-root[data-set=\"{rnd}\"]')&&{READY}");time.sleep(.4)
   cfg=js('return CARD.slides[10].data.levels[arguments[0]].rounds[arguments[1]]',lv,rnd)
   launches_before=js('return __launches.length')
   pan_before=js('return __pan.length')
   check(label+': five pods, exact prefills locked',js("const p=[...document.querySelectorAll('.sp-pod')];return p.length===5&&p[0].classList.contains('locked')&&p.filter(x=>x.classList.contains('filled')).length===arguments[0]",len(cfg['prefilled'])))
   check(label+': same persistent world and fixed heading',js("return document.querySelector('.sp-world')===__world&&document.querySelector('.sp-fixed-title')===__heading&&__world.children.length===3&&__world.querySelectorAll('.sp-pod').length===15&&Math.abs(__heading.getBoundingClientRect().left-__headingX)<1"))
   check(label+': pods inside stage, readable equal badges',js("const p=[...document.querySelectorAll('.sp-pod')],s=document.getElementById('stage').getBoundingClientRect(),b=[...document.querySelectorAll('.sp-badge,.sp-podnum')];return p.every(x=>{const r=x.getBoundingClientRect();return r.left>=s.left&&r.right<=s.right})&&b.every(x=>x.offsetWidth>=64&&x.scrollWidth<=x.clientWidth)"))
   shot(label.replace(' ','_'))
   if rnd==0:
    check(label+': initial ghost demonstration',js('return __ghosts>=arguments[0]',lv+1))
   if lv==0 and rnd==0:
    start=js('return __ghosts');time.sleep(7.5)
    check('idle: demonstration repeats once',js('return __ghosts===arguments[0]+1',start));time.sleep(7.5)
    check('idle: no third demonstration',js('return __ghosts===arguments[0]+1',start))
    for attempt in range(3):
     wait(READY);time.sleep(.1)
     tile=js("return [...document.querySelectorAll('.sp-astro.walker')].find(x=>arguments[0].includes(+x.dataset.n))",cfg['distractors'])
     pod=js("return document.querySelector('.sp-pod:not(.filled)')")
     js(DRAG,tile,pod);time.sleep(.45);wait(READY)
     check(f'wrong {attempt+1}: no pod filled and passenger returns',js("return document.querySelectorAll('.sp-pod.filled').length===2&&!arguments[0].classList.contains('snapped')",tile))
    wrongvo=js('return CARD.slides[10].data.levels[0].wrong')
    check('wrong VO only once per round',js('return __voices.filter(x=>x.includes(arguments[0]+".")).length===1',wrongvo))
    check('PPT: third wrong drop keeps retries and all unsnapped passengers available',js("return [...document.querySelectorAll('.sp-astro.walker:not(.snapped)')].every(x=>x.getAttribute('aria-disabled')!=='true'&&getComputedStyle(x).pointerEvents!=='none')"))
    shot('wrong_return')
   for target in reversed([i for i in range(5) if i not in cfg['prefilled']]):
    wait(READY);time.sleep(.12)
    n=cfg['seq'][target];tile=js("return [...document.querySelectorAll('.sp-astro.walker:not(.snapped)')].find(x=>+x.dataset.n===arguments[0])",n);pod=js('return document.querySelectorAll(".sp-pod")[arguments[0]]',target)
    before=js('return __voices.length')
    if lv==1:
     js("arguments[0].dispatchEvent(new KeyboardEvent('keydown',{key:' ',bubbles:true}));arguments[1].dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}))",tile,pod)
    elif lv==2:
     js("const a=arguments[0],z=arguments[1],s=a.getBoundingClientRect(),t=z.getBoundingClientRect();const touch=(x,y)=>new Touch({identifier:1,target:a,clientX:x,clientY:y});const emit=(el,type,p)=>el.dispatchEvent(new TouchEvent(type,{bubbles:true,cancelable:true,touches:type==='touchend'?[]:[p],changedTouches:[p]}));emit(a,'touchstart',touch(s.left+s.width/2,s.top+s.height/2));emit(document,'touchmove',touch(t.left+t.width/2,t.top+t.height/2));emit(document,'touchend',touch(t.left+t.width/2,t.top+t.height/2));",tile,pod)
    else:js(DRAG,tile,pod)
    check(label+f': any-order docking {n}',js("return arguments[0].classList.contains('filled')&&arguments[1].classList.contains('snapped')",pod,tile))
    time.sleep(.7)
    check(label+f': correct narration says only {n}',js('return __voices.slice(arguments[0]).some(x=>x.includes("vo_g_n_"+arguments[1]+"."))',before,n))
   shot(label.replace(' ','_')+'_full')
   wait(f"__launches.length>{launches_before}");time.sleep(.55);shot(label.replace(' ','_')+'_individual_launch')
   wait(f"__launches.length>={launches_before+5}")
   check(label+': rockets launch individually left to right',js('const a=__launches.slice(-5);return a.every((x,i)=>x.index===i&&x.count===i+1&&(i===0||x.t-a[i-1].t>=350))'))
   shot(label.replace(' ','_')+'_launch')
   if rnd<2:
    wait("document.querySelector('.sp-root[data-travelling=\"true\"]')");time.sleep(.5);shot(label.replace(' ','_')+'_parallax')
    check(label+': camera tracks while launching, with fixed heading and locked input',js('return __pan.slice(arguments[0]).some(p=>p.x<-20&&p.x>-2650&&p.near<p.far&&p.inert&&p.scenes===3&&p.launches>0&&p.launches<5&&Math.abs(p.heading-__headingX)<1)',pan_before))
  if lv<2:
   wait(f"document.querySelectorAll('.sp-card')[{lv}]&&document.querySelectorAll('.sp-card')[{lv}].classList.contains('done')")
   check(f'L{lv+1}: completed menu card faded and disabled',js('const c=document.querySelectorAll(".sp-card")[arguments[0]];return c.disabled&&!!c.querySelector(".sp-card-badge")',lv));shot('menu_done_'+str(lv))
 wait("CARD.slides[state.idx].type==='CELEBRATION'");check('nine rounds reach celebration',True)
 check('background removed after game',js("return !document.querySelector('.sp-universe')&&!document.body.classList.contains('mtg-game')"))
 check('all creature and spaceship cues triggered',js("return ['frog_croak','space_rabbit','space_squirrel','space_ready','space_ignite','space_flyby','space_travel','space_launch'].every(n=>__sfx.some(x=>x.includes('sfx_'+n+'.')))"))
 d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':960,'height':540,'deviceScaleFactor':1,'mobile':False})
 d.get(URL+'?slide=10');wait("document.querySelector('.sp-card')");time.sleep(.6);shot('960_menu');js("document.querySelector('.sp-card').click()");wait(READY);time.sleep(.4);shot('960_round')
 check('960: all five pods fit stage',js('const s=document.getElementById("stage").getBoundingClientRect();return [...document.querySelectorAll(".sp-pod")].every(x=>{const r=x.getBoundingClientRect();return r.left>=s.left-1&&r.right<=s.right+1})'))
 for w,h in [(1600,750),(1000,900)]:
  d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False});time.sleep(.3);shot(f'{w}_{h}_full_background')
  check(f'{w}x{h}: background fills letterbox margins',js("const b=document.querySelector('.sp-universe').getBoundingClientRect();return b.width===innerWidth&&b.height===innerHeight&&getComputedStyle(document.querySelector('.sp-root')).backgroundColor==='rgba(0, 0, 0, 0)'"))
 d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
 d.get(URL+'?slide=10');wait("document.querySelector('.sp-card')");js("document.querySelector('.sp-card').click()");wait(READY);time.sleep(.4)
 check('reduced motion: static hint replaces moving ghost',js('return __ghosts===0'))
 for _ in range(3):
  wait(READY)
  tile,pod=js("const p=[...document.querySelectorAll('.sp-pod')].find(x=>!x.classList.contains('filled')),n=CARD.slides[10].data.levels[0].rounds[0].seq[+p.dataset.i];return [[...document.querySelectorAll('.sp-astro.walker')].find(x=>+x.dataset.n===n),p]")
  js(DRAG,tile,pod);time.sleep(.4)
 wait(f"document.querySelector('.sp-root[data-set=\"1\"]')&&{READY}")
 check('reduced motion: next dock accessible after staggered launches',js("return getComputedStyle(document.querySelector('.sp-world')).transitionDuration==='0s'&&document.querySelectorAll('.sp-pod.filled').length===2"))
 errors=[e for e in d.get_log('browser') if e['level']=='SEVERE' and 'favicon' not in e['message']];check('no browser errors',not errors);(OUT/'browser_errors.json').write_text(json.dumps(errors,indent=2))
finally:
 (OUT/'camera_launch_events.json').write_text(json.dumps(js('return {launches:__launches,pan:__pan}'),indent=2))
 (OUT/'results.json').write_text(json.dumps(checks,indent=2));d.quit()
print(f'{sum(v for _,v in checks)} passed / {len(checks)} checks',flush=True)
if any(not v for _,v in checks):sys.exit(1)
