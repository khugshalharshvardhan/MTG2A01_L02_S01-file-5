"""File9 cover, full SME read-along text and motion QA. Narration is simulated."""
from pathlib import Path
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'5_SCREENSHOTS/cover_sme';OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8942/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required')
o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o);checks=[]
def js(s,*a):return d.execute_script(s,*a)
def wait(s,t=60):return WebDriverWait(d,t,poll_frequency=.05).until(lambda _:js('return '+s))
def check(n,v):checks.append([n,bool(v)]);print(('PASS ' if v else 'FAIL ')+n,flush=True)
def go(i=None):d.get(URL+('' if i is None else '?slide='+str(i)))
def shot(n):d.save_screenshot(str(OUT/(n+'.png')))
STUB="""
HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),100);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,14400,24000));};})();
window.__captions=[];window.__audit={samples:0,outside:0};
new MutationObserver(()=>{const c=document.querySelector('.br-cap');if(c&&c.dataset.clip&&c.dataset.clip!==window.__lastCaption){window.__lastCaption=c.dataset.clip;const text=c.querySelector('.br-caption-text'),current=c.querySelector('.br-count-word.current'),r=text.getBoundingClientRect(),nav=document.getElementById('navBtn').getBoundingClientRect();window.__captions.push({clip:c.dataset.clip,text:text.textContent,count:current?current.textContent:'',clear:r.bottom<nav.top-8});}}).observe(document,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['data-clip']});
(function sample(){const f=document.querySelector('.br-frog.hopping');if(f){const r=f.getBoundingClientRect(),p=f.closest('.br-view').getBoundingClientRect();__audit.samples++;if(r.left<p.left-2||r.right>p.right+2||r.top<p.top-2||r.bottom>p.bottom+2)__audit.outside++;}requestAnimationFrame(sample);})();
"""
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':STUB})
try:
 for w,h in [(1333,750),(960,540)]:
  d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
  go();wait("document.querySelector('.fc-card.fc-ready')&&window.__ltReady&&!document.getElementById('sgBtn').disabled")
  time.sleep(.8)
  check(f'{w}: exact File9 frame dimensions and border',js("const c=document.querySelector('.fc-card');return c.offsetWidth===1040&&c.offsetHeight===574&&getComputedStyle(c).borderTopWidth==='8px'&&getComputedStyle(c).borderRadius==='40px'"))
  check(f'{w}: artwork fills the complete frame',js("const p=document.querySelector('.fc-pond').getBoundingClientRect(),c=document.querySelector('.fc-card'),r=c.getBoundingClientRect(),s=r.width/c.offsetWidth;return Math.abs(p.width-c.clientWidth*s)<2&&Math.abs(p.height-c.clientHeight*s)<2"))
  check(f'{w}: animated frogs align with their own pads',js("return [...document.querySelectorAll('.fc-frog,.fc-friend')].every(f=>{const l=[...document.querySelectorAll('.fc-leaf')].find(l=>Math.abs(l.offsetLeft-f.offsetLeft)<1),a=f.getBoundingClientRect(),b=l.getBoundingClientRect();return Math.abs((a.left+a.right-b.left-b.right)/2)<3&&a.bottom<=b.bottom&&a.width<b.width;})"))
  check(f'{w}: exact 140px round play art',js("const b=document.getElementById('sgBtn'),i=b.querySelector('.fc-play-ready');return b.offsetWidth===140&&b.offsetHeight===140&&i.complete&&i.naturalWidth>0&&i.src.endsWith('/btn-play-round.svg')&&getComputedStyle(b).bottom==='30px'"))
  check(f'{w}: local Yatra title font loaded',js("return document.fonts.check('64px \"Yatra One\"')&&getComputedStyle(document.querySelector('.fc-title-line')).fontFamily.includes('Yatra One')"))
  check(f'{w}: cover subtitle removed',js("return !document.querySelector('.sg-sub')"))
  check(f'{w}: cover has animated frog and water',js("return getComputedStyle(document.querySelector('.fc-frog')).animationName==='fcFrogHello'&&document.querySelectorAll('.fc-water-ring').length===4&&document.querySelectorAll('.fc-mote').length===5"))
  check(f'{w}: sound-effects toggle removed from cover',js("return !document.querySelector('.mtg-sound-toggle')"))
  shot(f'{w}_cover')
  wait("document.getElementById('sgBtn').classList.contains('idle-pulse')",12)
  check(f'{w}: reference idle play pulse',js("return getComputedStyle(document.getElementById('sgBtn')).animationName==='fcPlayPulse'"))
  for idx,taps in [(0,0),(1,2),(2,2)]:
   go(idx);first=js('return CARD.slides[arguments[0]].data.steps[0].clips[0].vo',idx)
   wait("document.querySelector('.br-cap')&&document.querySelector('.br-cap').dataset.clip==='"+first+"'")
   shot(f'{w}_T{idx+1}_intro')
   for _ in range(taps):
    wait("document.querySelector('.br-frog.tappable')");js("document.querySelector('.br-frog.tappable').click()")
   wait("!document.getElementById('navBtn').disabled",100)
   check(f'{w}: T{idx+1} every SME narration clip has visible exact text',js("const s=CARD.slides[arguments[0]],want=[...new Set(s.data.steps.flatMap(x=>x.clips.map(c=>c.vo)))];return want.every(id=>__captions.some(c=>c.clip===id&&(c.text===CARD.assets.audio_text[id]||c.count===CARD.assets.audio_text[id])))",idx))
   check(f'{w}: T{idx+1} all caption text clears navigation',js('return __captions.length>0&&__captions.every(c=>c.clear)'))
   check(f'{w}: T{idx+1} all hops remain in the picture',js('return __audit.samples>0&&__audit.outside===0'))
   check(f'{w}: T{idx+1} counting strip keeps spoken numbers',js("return document.querySelector('.br-count-strip').children.length>=5"))
   check(f'{w}: T{idx+1} sound-effects toggle removed',js("return !document.querySelector('.mtg-sound-toggle')"))
   (OUT/f'{w}_T{idx+1}_caption_log.json').write_text(json.dumps(js('return __captions'),ensure_ascii=False,indent=2),encoding='utf8')
   shot(f'{w}_T{idx+1}_recap')
  for idx in range(3,10):
   go(idx);wait("document.querySelector('.mtg-opt')")
   check(f'{w}: G{idx-2} sound-effects toggle removed',js("return !document.querySelector('.mtg-sound-toggle')"))
 d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
 go();wait("document.querySelector('.fc-card.fc-ready')&&window.__ltReady")
 check('reduced-motion cover is still and title remains visible',js("return getComputedStyle(document.querySelector('.fc-frog')).animationName==='none'&&getComputedStyle(document.querySelector('.fc-title-line')).opacity==='1'"))
 shot('reduced_motion_cover')
 errors=[e for e in d.get_log('browser') if e['level']=='SEVERE']
 (OUT/'browser_errors.json').write_text(json.dumps(errors,indent=2),encoding='utf8')
 check('no browser errors or missing assets',not errors)
finally:
 (OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf8');d.quit()
if any(not result for _,result in checks):sys.exit(1)
