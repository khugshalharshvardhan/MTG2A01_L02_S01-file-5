"""Verify terminal option locking and reset for every guided question/blank."""
from pathlib import Path
import json,os,sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'5_SCREENSHOTS/third_attempt';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8942/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required');o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o);checks=[]
def js(s,*a):return d.execute_script(s,*a)
def wait(s):return WebDriverWait(d,40,poll_frequency=.1).until(lambda _:js('return '+s))
def check(n,v):checks.append([n,bool(v)]);print(('PASS ' if v else 'FAIL ')+n,flush=True)
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':"""
HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();
"""})
READY="[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)"
try:
 for idx in range(3,10):
  d.get(URL+'?slide='+str(idx));wait(READY)
  answers=js('const a=CARD.slides[state.idx].data;return a.blanks?a.blanks.map(b=>b.answer):[a.answer]')
  for bi,answer in enumerate(answers):
   label=f'G{idx-2} blank {bi+1}'
   for attempt in range(3):
    wrong=js("return [...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled&&+b.dataset.v!==arguments[0]).dataset.v",answer)
    js("[...document.querySelectorAll('.mtg-opt')].find(b=>b.dataset.v===arguments[0]).click()",wrong)
    if attempt==2:
     check(label+' locks wrong choices immediately on third error',js("return [...document.querySelectorAll('.mtg-opt')].filter(b=>+b.dataset.v!==arguments[0]).every(b=>b.disabled)",answer))
    wait(READY)
    if attempt<2:check(label+f' attempt {attempt+1} keeps remaining choices available',js("return [...document.querySelectorAll('.mtg-opt')].filter(b=>!b.classList.contains('used')).every(b=>!b.disabled)"))
   check(label+' only correct answer enabled and wrong choices visibly disabled',js("const a=[...document.querySelectorAll('.mtg-opt')].filter(b=>!b.classList.contains('used'));return a.filter(b=>!b.disabled).length===1&&a.find(b=>!b.disabled).dataset.v===String(arguments[0])&&a.filter(b=>b.disabled).every(b=>b.getAttribute('aria-disabled')==='true'&&+getComputedStyle(b).opacity<=.46&&getComputedStyle(b).pointerEvents==='none')",answer))
   js("document.getElementById('audioChip').click()");wait(READY)
   check(label+' replay preserves correct-only selection',js("const a=[...document.querySelectorAll('.mtg-opt')].filter(b=>!b.disabled);return a.length===1&&+a[0].dataset.v===arguments[0]",answer))
   check(label+' disabled handler cannot submit another wrong answer',js("const n=state.attempts;[...document.querySelectorAll('.mtg-opt')].find(b=>b.disabled&&!b.classList.contains('used')).onclick();return state.attempts===n"))
   if idx in [3,7]:d.save_screenshot(str(OUT/(label.replace(' ','_')+'.png')))
   js("[...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled&&+b.dataset.v===arguments[0]).click()",answer)
   if bi<len(answers)-1:
    wait(READY);check(label+' next blank releases lock but keeps used choices disabled',js("return [...document.querySelectorAll('.mtg-opt')].filter(b=>!b.disabled).length>1&&[...document.querySelectorAll('.mtg-opt.used')].every(b=>b.disabled)"))
   else:wait(f'state.idx!=={idx}')
 errors=[e for e in d.get_log('browser') if e['level']=='SEVERE'];(OUT/'browser_errors.json').write_text(json.dumps(errors,indent=2),encoding='utf8');check('no browser errors',not errors)
finally:
 (OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf8');d.quit()
if any(not x[1] for x in checks):sys.exit(1)
