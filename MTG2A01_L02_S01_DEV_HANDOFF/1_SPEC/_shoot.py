"""Headless capture of chosen slides after a wait (QA only).
    python _shoot.py <outdir> <slide>:<seconds>[:js] ...
`js` (optional) runs in the page before the shot (e.g. to tap something)."""
import sys, time, os
from selenium import webdriver

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
o = webdriver.ChromeOptions()
o.add_argument("--headless=new"); o.add_argument("--window-size=1333,750")
o.add_argument("--autoplay-policy=no-user-gesture-required")
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o)
for spec in sys.argv[2:]:
    parts = spec.split(":", 2)
    s, secs = parts[0], float(parts[1])
    js = parts[2] if len(parts) > 2 else None
    url = "http://127.0.0.1:8931/MTG2A01_L02_S01.html" + ("" if s == "land" else f"?slide={s}")
    d.get(url)
    if js:
        time.sleep(1.0)
        for step in js.split(";;"):
            if step.startswith("wait"):
                time.sleep(float(step[4:])); continue
            d.execute_script(step)
    time.sleep(secs)
    name = f"{s}_{str(secs).replace('.', '_')}" + ("_js" if js else "")
    d.save_screenshot(os.path.join(out, name + ".png"))
    errs = [l["message"] for l in d.get_log("browser") if l["level"] in ("SEVERE",)]
    print(name, "errors:", errs[:4])
d.quit()
