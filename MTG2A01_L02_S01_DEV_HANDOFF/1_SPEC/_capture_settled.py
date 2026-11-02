"""Play-order screenshots of every screen in its settled/question state (audio stubbed). QA only.
    python _capture_settled.py <outdir>"""
import sys, os, time
from selenium import webdriver
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
URL = "http://127.0.0.1:8931/MTG2A01_L02_S01.html"
o = webdriver.ChromeOptions(); o.add_argument("--headless=new"); o.add_argument("--window-size=1333,750"); o.add_argument("--autoplay-policy=no-user-gesture-required")
d = webdriver.Chrome(options=o)
d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source":
    "HTMLMediaElement.prototype.play=function(){const a=this;setTimeout(()=>{try{a.dispatchEvent(new Event('ended'))}catch(e){}},60);return Promise.resolve();};"
    "(function(){const AC=window.AudioContext||window.webkitAudioContext;if(AC)AC.prototype.decodeAudioData=function(){return Promise.resolve(this.createBuffer(1,1440,24000));};})();"})
def until(c, t=40):
    s = time.time()
    while time.time() - s < t:
        if d.execute_script("return " + c): return
        time.sleep(0.15)
d.get(URL); time.sleep(4); d.save_screenshot(os.path.join(OUT, "01_landing.png"))
names = ["02_T1_BRIDGE_2s", "03_T2_BRIDGE_5s", "04_T3_BRIDGE_10s", "05_G1_JUMP_PICK", "06_G2_JUMP_PICK", "07_G3_JUMP_PICK",
         "08_G4_SEQ_FILL", "09_G5_SEQ_FILL", "10_G6_SEQ_FILL", "11_G7_SEQ_FILL", "12_GAME_menu", "13_CELEBRATION"]
for i, n in enumerate(names):
    d.get(URL + f"?slide={i}"); time.sleep(0.6)
    if i < 3: until("!!document.querySelector('.br-frog.tappable') || !document.getElementById('navBtn').disabled"); time.sleep(1.4)
    elif i < 10: until("[...document.querySelectorAll('.mtg-opt')].some(b=>!b.disabled)"); time.sleep(0.8)
    else: time.sleep(4.5)
    d.save_screenshot(os.path.join(OUT, n + ".png"))
d.quit()
