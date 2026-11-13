"""Decode the shipped Opus effects in Chrome without audio stubs."""
import json,sys
from pathlib import Path
from selenium import webdriver
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required')
d=webdriver.Chrome(options=o)
try:
 d.get('http://127.0.0.1:8942/MTG2A01_L02_S01.html?slide=10')
 r=d.execute_async_script("""const done=arguments[0];(async()=>{const c=new AudioContext(),out=[];for(const n of ['dock','puff','launch','rabbit','squirrel','ready','ignite','flyby','travel']){const r=await fetch('assets/Audio/sfx_space_'+n+'.ogg'),b=await c.decodeAudioData(await r.arrayBuffer());out.push({effect:n,duration:b.duration,peak:Math.max(...b.getChannelData(0).map(Math.abs))});}await c.close();return out;})().then(done).catch(e=>done({error:String(e)}));""")
 print(json.dumps(r,indent=2));assert isinstance(r,list) and len(r)==9 and all(.15<x['duration']<1.6 and .01<x['peak']<.95 for x in r)
 (Path(__file__).resolve().parents[1]/'5_SCREENSHOTS/spaceport/media.json').write_text(json.dumps(r,indent=2))
finally:d.quit()
