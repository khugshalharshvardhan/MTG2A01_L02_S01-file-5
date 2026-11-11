"""Check the sequence activity artwork and every hint after the character update."""
from pathlib import Path
import os,json,time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'5_SCREENSHOTS/sequence_cast_refresh'
OUT.mkdir(exist_ok=True)
URL=os.environ.get('MTG_TEST_URL','http://127.0.0.1:8934/MTG2A01_L02_S01.html')
o=webdriver.ChromeOptions();o.add_argument('--headless=new')
o.add_argument('--autoplay-policy=no-user-gesture-required')
o.set_capability('goog:loggingPrefs',{'browser':'ALL'})
d=webdriver.Chrome(options=o)
d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':1333,'height':750,'deviceScaleFactor':1,'mobile':False})
d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':"""
HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>a.dispatchEvent(new Event('ended')),60);return Promise.resolve();};
(function(){const A=window.AudioContext||window.webkitAudioContext;if(A)A.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();
"""})
checks=[]
def js(s,*args):return d.execute_script(s,*args)
def wait(s):return WebDriverWait(d,35).until(lambda _:js('return '+s))
def check(name,value):
    checks.append([name,bool(value)]);print(('PASS ' if value else 'FAIL ')+name,flush=True)
def shot(name):d.save_screenshot(str(OUT/(name+'.png')))
try:
    for idx,expected in [(6,'sp_grasshopper_v3'),(7,'sp_rabbit'),(8,'sp_squirrel'),(9,'sp_grasshopper_v3')]:
        d.get(URL+'?slide='+str(idx))
        wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
        wait("document.querySelector('.sf-animal').complete")
        sid=js('return CARD.slides[state.idx].id')
        blanks=js('return CARD.slides[state.idx].data.blanks.map(b=>b.answer)')
        check(sid+' uses requested character',js("return document.querySelector('.sf-animal').src.endsWith(arguments[0]+'.webp')",expected))
        check(sid+' character loads',js("return document.querySelector('.sf-animal').naturalWidth>0"))
        check(sid+' character clears number boxes',js("const a=document.querySelector('.sf-animal').getBoundingClientRect(),b=document.querySelector('.sf-strip').getBoundingClientRect();return a.bottom<=b.top+1"))
        shot(sid+'_question')
        for bi,answer in enumerate(blanks):
            wrong=js("return [...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled && +b.textContent!==arguments[0])",answer)
            js('arguments[0].click()',wrong)
            wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
            js('arguments[0].click()',wrong)
            wait("!!document.querySelector('.sf-hint-ov.show')")
            wait("document.querySelector('.sf-hint-animal').complete")
            check(sid+' blank '+str(bi+1)+' hint uses matching character',js("const a=document.querySelector('.sf-hint-animal');return a.src.endsWith(arguments[0]+'.webp')&&a.naturalWidth>0",expected))
            shot(sid+'_hint_'+str(bi+1))
            wait("!document.querySelector('.sf-hint-ov')")
            wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
            js("[...document.querySelectorAll('.mtg-opt')].find(b=>!b.disabled && +b.textContent===arguments[0]).click()",answer)
            if bi<len(blanks)-1:
                wait("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)")
            else:
                WebDriverWait(d,15).until(lambda _:js("return CARD.slides[state.idx].id!==arguments[0] || document.querySelectorAll('.sf-box.filled').length>=arguments[1]",sid,len(blanks)))
        check(sid+' sequence completes',True)
    errors=[x['message'] for x in d.get_log('browser') if x['level']=='SEVERE' and 'favicon' not in x['message']]
    check('no browser errors',not errors)
    for error in errors:print(error,flush=True)
finally:
    d.quit()
    (OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
if any(not v for _,v in checks):raise SystemExit(1)
print(str(len(checks))+' character and hint checks passed.',flush=True)
