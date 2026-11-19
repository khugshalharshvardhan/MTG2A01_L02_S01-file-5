"""Nov 19 review corrections. Silent audio shortens narration; visual timing stays real."""
from pathlib import Path
import json,time,re,subprocess
P=Path(__file__).resolve().parents[1]
scope={'__file__':str(P/'1_SPEC/_verify_interaction_refinement.py')}
exec((P/'1_SPEC/_verify_interaction_refinement.py').read_text(encoding='utf-8').split('\ntry:\n')[0],scope)
d=scope['d'];js=scope['js'];wait=scope['wait'];live=scope['live'];go=scope['go'];click=scope['click']
out=P/'5_SCREENSHOTS/nov19_corrections';out.mkdir(exist_ok=True);checks=[]
def check(name,value):
 checks.append([name,bool(value)]);print(('PASS ' if value else 'FAIL ')+name,flush=True)
def shot(name):d.save_screenshot(str(out/(name+'.png')))
try:
 for width,height in [(1333,750),(960,540)]:
  d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False})
  for page in [1,2]:
   d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
   go(page);wait("document.querySelector('.br-frog.tappable')&&document.querySelector('.mtg-hand')")
   check(f'{width} T{page+1}: compact hand fingertip targets Tappu',js("const f=document.querySelector('.br-frog'),h=document.querySelector('.mtg-hand'),a=f.getBoundingClientRect(),b=h.getBoundingClientRect(),s=a.width/f.offsetWidth;const x=b.left+20*s,y=b.top+4*s;return h.offsetWidth===54&&h.offsetHeight===68&&Math.abs(x-(a.left+a.width/2))<2*s&&y>a.top&&y<a.bottom"))
   shot(f'{width}_T{page+1}_hand')
   for _ in range(2):
    wait("document.querySelector('.br-frog.tappable')");js("document.querySelector('.br-frog.tappable').click()")
   wait("!document.getElementById('navBtn').disabled")
   check(f'{width} T{page+1}: zero labels the beginning of the completed curves',js("const z=[...document.querySelectorAll('.br-num')].find(e=>e.textContent==='0'),r=z.getBoundingClientRect(),v=document.querySelector('.br-view').getBoundingClientRect(),style=getComputedStyle(z);return z.classList.contains('mark')&&style.visibility==='visible'&&style.opacity==='1'&&r.left>=v.left&&r.right<=v.right"))
   shot(f'{width}_T{page+1}_zero')
 for page in [3,4,5]:
  go(page);live()
  check(f'G{page-2}: first and subsequent completed numbers are equally bold without gold',js("const a=CARD.slides[state.idx].data.prior.map(n=>[...document.querySelectorAll('.nl-lbl')].find(e=>+e.textContent===n));return a.every(e=>e.classList.contains('landed')&&+getComputedStyle(e).fontWeight>=800&&getComputedStyle(e).backgroundColor==='rgba(0, 0, 0, 0)'&&getComputedStyle(e).boxShadow==='none')&&new Set(a.map(e=>getComputedStyle(e).fontSize)).size===1"))
  shot(f'G{page-2}_bold_no_glow')
  if page==3:
   click(51);time.sleep(.2);live();click(51)
   wait("document.querySelector('.nl-lbl.glow')")
   check('G1: destination glows temporarily during second-attempt hint',js("return [...document.querySelectorAll('.nl-lbl.glow')].some(e=>e.textContent==='55'&&getComputedStyle(e).boxShadow!=='none')"))
   wait("!document.querySelector('.nl-lbl.glow')")
   check('G1: glow clears without removing historical bold numbers',js("return [...document.querySelectorAll('.nl-lbl.landed')].length===3&&[...document.querySelectorAll('.nl-lbl.landed')].every(e=>getComputedStyle(e).boxShadow==='none')"))
 go(10);wait("document.querySelector('.sp-card')&&[...document.querySelectorAll('.sp-card img')].every(e=>e.complete&&e.naturalWidth>0)")
 d.execute_async_script("const done=arguments[0];document.fonts.ready.then(()=>done(true))")
 shot('open_ship_menu')
 source=(P/'1_SPEC/art_keyed/spaceport_pod.svg').read_text(encoding='utf-8')
 built=(P/'3_BUILD/assets/Images/spaceport_pod.svg').read_text(encoding='utf-8')
 check('ship source and exported artwork have no glass canopy or reflection',source==built and 'id="glass"' not in source and 'M48 142V79' not in source and 'M66 63' not in source)
 js("document.querySelector('.sp-card').click()");wait("document.querySelector('.sp-root[data-playable=\"true\"][data-narrating=\"false\"]')")
 js("""const cfg=CARD.slides[10].data.levels[0].rounds[0],p=[...document.querySelectorAll('.sp-pod')].find(p=>!p.classList.contains('filled')),n=cfg.seq[+p.dataset.i],w=[...document.querySelectorAll('.walker')].find(w=>+w.dataset.n===n);w.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));p.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));""")
 check('open ship still seats and locks the correct astronaut',js("return document.querySelectorAll('.sp-pod.filled').length===3&&document.querySelectorAll('.walker.snapped').length===1"))
 time.sleep(.5);shot('open_ship_seated')
 errors=[e for e in d.get_log('browser') if e['level']=='SEVERE' and 'favicon' not in e['message']]
 check('no browser errors',not errors)
 for attrs,s in re.findall(r'<script\b([^>]*)>(.*?)</script>',(P/'3_BUILD/MTG2A01_L02_S01.html').read_text(encoding='utf-8'),re.S|re.I):
  if not s.strip():continue
  if 'application/json' in attrs:json.loads(s)
  else:
   r=subprocess.run(['node','--check'],input=s,encoding='utf-8',capture_output=True);assert r.returncode==0,r.stderr
 check('built JavaScript and embedded JSON are valid',True)
finally:
 d.quit();(out/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(f'{sum(v for _,v in checks)}/{len(checks)} checks passed',flush=True)
if any(not v for _,v in checks):raise SystemExit(1)
