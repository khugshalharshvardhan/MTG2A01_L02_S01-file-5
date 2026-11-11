"""Sample jump bounds on every related activity at two viewport sizes. Audio is simulated."""
from pathlib import Path
import os,json,time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'5_SCREENSHOTS/jump_bounds_fix';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8934/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new')
o.add_argument('--autoplay-policy=no-user-gesture-required')
o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o)
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':"""
HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();
window.__jumpAudit={samples:0,outside:0,headerOverlap:0};
(function sample(){
 const a=document.querySelector('.sf-animal.hopping,.jp-frog.hopping'),log=window.__jumpAudit;
 if(a){
  const frame=a.closest('.sf-stage,.jp-board').getBoundingClientRect(),r=a.getBoundingClientRect();
  const header=document.querySelector('.prompt-band').getBoundingClientRect();
  log.samples++;
  if(r.left<frame.left-2||r.right>frame.right+2||r.top<frame.top-2||r.bottom>frame.bottom+2)log.outside++;
  if(r.top<header.bottom-1)log.headerOverlap++;
 }
 requestAnimationFrame(sample);
})();
"""})
checks=[]
def js(s,*args):return d.execute_script(s,*args)
def wait(s):return WebDriverWait(d,35).until(lambda _:js('return '+s))
def check(name,result):
 checks.append([name,bool(result)]);print(('PASS ' if result else 'FAIL ')+name,flush=True)
try:
 for w,h in [(1333,750),(960,540)]:
  d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
  for idx in range(3,10):
   d.get(URL+'?slide='+str(idx))
   wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
   sid=js('return CARD.slides[state.idx].id')
   answers=js('const a=CARD.slides[state.idx].data;return a.blanks?a.blanks.map(b=>b.answer):[a.answer]')
   for i,answer in enumerate(answers):
    js("[...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled && +b.textContent===arguments[0]).click()",answer)
    if i<len(answers)-1:wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
    else:wait("!document.querySelector('.sf-animal.hopping,.jp-frog.hopping')")
   result=js('return __jumpAudit')
   check(sid+' '+str(w)+'px jumps stay in frame',result['samples']>10 and result['outside']==0)
   check(sid+' '+str(w)+'px jumps clear header',result['headerOverlap']==0)
   if w==1333:d.save_screenshot(str(OUT/(sid+'_landed.png')))
 errors=[x['message'] for x in d.get_log('browser') if x['level']=='SEVERE' and 'favicon' not in x['message']]
 check('no browser errors',not errors)
 for e in errors:print(e,flush=True)
finally:
 d.quit();(OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
if any(not v for _,v in checks):raise SystemExit(1)
print(str(len(checks))+' jump bounds checks passed.',flush=True)
