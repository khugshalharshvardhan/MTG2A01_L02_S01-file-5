"""Visual receipt for full-window spaceport at wide and tall aspect ratios."""
from pathlib import Path
import time,json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
OUT=Path(__file__).resolve().parents[1]/'5_SCREENSHOTS/spaceport'
o=webdriver.ChromeOptions();o.add_argument('--headless=new');o.add_argument('--autoplay-policy=no-user-gesture-required')
d=webdriver.Chrome(options=o);results=[]
try:
 for w,h in [(1333,750),(1600,750),(1000,900)]:
  d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':False})
  d.get('http://127.0.0.1:8942/MTG2A01_L02_S01.html?slide=10')
  WebDriverWait(d,30).until(lambda _:d.execute_script('return document.querySelectorAll(".sp-card-animal").length===3&&[...document.querySelectorAll(".sp-card-animal")].every(x=>x.complete)'))
  time.sleep(.7);p=OUT/f'{w}_{h}_background_final.png';d.save_screenshot(str(p))
  # A single backdrop must paint both sides of the playable stage boundary.
  stage=d.execute_script('const r=document.getElementById("stage").getBoundingClientRect();return {x:r.left,y:r.top}')
  im=Image.open(p).convert('RGB')
  if stage['x']>5:
   x=round(stage['x']);a=im.getpixel((x-2,h-6));b=im.getpixel((x+2,h-6))
  elif stage['y']>5:
   y=round(stage['y']);a=im.getpixel((12,y-2));b=im.getpixel((12,y+2))
  else:a=b=(0,0,0)
  delta=max(abs(x-y) for x,y in zip(a,b));assert delta<15,(w,h,a,b)
  # The SVG must also paint its full width when the parallax overscan stretches it.
  svg=d.execute_async_script("const done=arguments[0];fetch('assets/Images/spaceport_bg.svg').then(r=>r.text()).then(done)")
  assert 'preserveAspectRatio="none"' in svg
  results.append({'width':w,'height':h,'stage_edge_colour_delta':delta,'passed':True})
 print(json.dumps(results,indent=2));(OUT/'background_final.json').write_text(json.dumps(results,indent=2))
finally:d.quit()
