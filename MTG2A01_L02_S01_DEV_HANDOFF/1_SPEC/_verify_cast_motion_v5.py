"""Cover VO gating, continuous layout morphs and distinct cute cast. Audio is simulated."""
from pathlib import Path
import json,os,sys,time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'5_SCREENSHOTS/cast_motion_v5';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8942/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required');o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o);checks=[]
def js(s,*a):return d.execute_script(s,*a)
def wait(s,t=60):return WebDriverWait(d,t,poll_frequency=.05).until(lambda _:js('return '+s))
def check(n,v):checks.append([n,bool(v)]);print(('PASS ' if v else 'FAIL ')+n,flush=True)
def go(i=None):d.get(URL+('' if i is None else '?slide='+str(i)))
def shot(n):d.save_screenshot(str(OUT/(n+'.png')))
STUB="""
const landingBuffers=new WeakSet(),fetch0=window.fetch;window.fetch=async function(...args){const r=await fetch0.apply(this,args),u=String(args[0]);if(u.includes('/vo_landing.')){const f=r.arrayBuffer.bind(r);r.arrayBuffer=async()=>{const b=await f();landingBuffers.add(b);return b;};}return r;};
HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),this.src.includes('/vo_landing.')?3000:60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(data){const b=this.createBuffer(1,landingBuffers.has(data)?72000:1440,24000);b.__landing=landingBuffers.has(data);return Promise.resolve(b);};const start=AudioBufferSourceNode.prototype.start;AudioBufferSourceNode.prototype.start=function(...a){if(this.buffer&&this.buffer.__landing){window.__landingStarted=performance.now();this.addEventListener('ended',()=>window.__landingEnded=performance.now());}return start.apply(this,a);};})();
window.__morph={expanded:[],compact:[]};window.__bounds={samples:0,outside:0};
(function sample(){const w=document.querySelector('.br-world'),f=document.querySelector('.br-frog');if(w&&f){const r=f.getBoundingClientRect(),p=f.closest('.br-view').getBoundingClientRect();if(w.dataset.layoutMoving==='true'){const n=document.querySelector('.br-num.big'),leaf=document.querySelector('.br-rock.key');window.__morph[w.dataset.layoutTarget].push({t:performance.now(),u:+w.dataset.unitSpacing,opacity:+w.style.getPropertyValue('--minor-opacity'),arcs:w.querySelectorAll('.mtg-arc').length,aligned:Math.abs(n.offsetLeft-leaf.offsetLeft)<1});}if(f.classList.contains('hopping')||w.dataset.layoutMoving==='true'){__bounds.samples++;if(r.left<p.left-2||r.right>p.right+2||r.top<p.top-2||r.bottom>p.bottom+2)__bounds.outside++;}}requestAnimationFrame(sample);})();
"""
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB})
try:
 for w,h in [(1333,750),(960,540)]:
  d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
  go();wait('window.__landingStarted')
  check(f'{w}: Play hidden while landing VO runs',js("const b=document.getElementById('sgBtn');return b.disabled&&getComputedStyle(b).visibility==='hidden'"))
  check(f'{w}: subtitle removed and title one line',js("const t=document.querySelector('.fc-title-line');return !document.querySelector('.sg-sub')&&document.querySelectorAll('.fc-title-line').length===1&&getComputedStyle(t).whiteSpace==='nowrap'&&t.scrollWidth<=t.clientWidth"))
  shot(f'{w}_cover_during_vo')
  wait("window.__landingEnded&&!document.getElementById('sgBtn').disabled")
  check(f'{w}: Play appears after VO completion',js("const b=document.getElementById('sgBtn');return getComputedStyle(b).visibility==='visible'&&getComputedStyle(b).opacity==='1'"))
  check(f'{w}: distinct cover frogs and lively motion',js("const a=document.querySelector('.fc-frog'),b=document.querySelector('.fc-friend');return a.src!==b.src&&b.complete&&b.naturalWidth>0&&getComputedStyle(a).animationName==='fcFrogHello'&&document.querySelector('.fc-cover-splash')"))
  time.sleep(.7);shot(f'{w}_cover')
  for idx in [1,2]:
   go(idx);wait("document.querySelector('.br-frog.tappable')")
   check(f'{w}: T{idx+1} compact view expands through intermediate spacing',js("const a=__morph.expanded;return a.length>=8&&new Set(a.map(x=>x.u)).size>=8&&a.at(-1).t-a[0].t>600&&a.every(x=>x.aligned)&&a.some(x=>x.opacity>.1&&x.opacity<.9)"))
   shot(f'{w}_T{idx+1}_expanded')
   for _ in range(2):
    wait("document.querySelector('.br-frog.tappable')");js("document.querySelector('.br-frog.tappable').click()")
   wait("!document.getElementById('navBtn').disabled")
   check(f'{w}: T{idx+1} recap contracts smoothly with existing arcs',js("const a=__morph.compact;return a.length>=8&&a[0].t<a.at(-1).t-450&&new Set(a.map(x=>x.arcs)).size===1&&a[0].arcs>=5&&a.every(x=>x.aligned)"))
   check(f'{w}: T{idx+1} no frame clipping during morph or hop',js('return __bounds.samples>0&&__bounds.outside===0'))
   check(f'{w}: T{idx+1} distinct friend loaded',js("return document.querySelector('.br-friend').src.includes(CARD.slides[state.idx].data.friend)&&document.querySelector('.br-friend').naturalWidth>0"))
   shot(f'{w}_T{idx+1}_recap');(OUT/f'{w}_T{idx+1}_frames.json').write_text(json.dumps(js('return __morph')),encoding='utf8')
  for idx in range(3,10):
   go(idx);wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
   a=js("const a=document.querySelector('.jp-frog,.sf-animal');return {src:a.src,loaded:a.complete&&a.naturalWidth>0}")
   check(f'{w}: G{idx-2} intended cute cast loaded',a['loaded'] and ('lesson_friend_' in a['src'] if idx in [4,5] else '_cute.webp' in a['src'] if idx>=6 else 'lesson_frog.webp' in a['src']))
   if idx in [4,5]:check(f'{w}: G{idx-2} mirrored frog stays centred',js("const a=document.querySelector('.jp-frog'),n=a.closest('.nl'),r=a.getBoundingClientRect(),b=n.getBoundingClientRect(),s=b.width/n.offsetWidth;return Math.abs((r.left+r.right)/2-(b.left+a.offsetLeft*s))<2"))
   time.sleep(.7);shot(f'{w}_G{idx-2}')
 d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
 go(2)
 for _ in range(2):wait("document.querySelector('.br-frog.tappable')");js("document.querySelector('.br-frog.tappable').click()")
 wait("!document.getElementById('navBtn').disabled")
 check('reduced motion skips the layout and flight animation',js("return __morph.expanded.length===0&&!document.querySelector('.hopping')&&document.querySelector('.br-world').dataset.layoutMoving==='false'"))
 errors=[x for x in d.get_log('browser') if x['level']=='SEVERE'];(OUT/'browser_errors.json').write_text(json.dumps(errors,indent=2),encoding='utf8');check('no browser errors',not errors)
finally:
 (OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf8');d.quit()
if any(not x[1] for x in checks):sys.exit(1)
