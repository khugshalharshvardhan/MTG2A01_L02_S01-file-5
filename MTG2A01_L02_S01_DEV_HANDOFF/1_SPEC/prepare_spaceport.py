"""Retain generated masters and export transparent spaceport cast; no API required."""
from pathlib import Path
from PIL import Image
import json,shutil,math,random,struct,wave,subprocess,sys
HERE=Path(__file__).resolve().parent
OUT=HERE/'visual_refresh/spaceport';OUT.mkdir(exist_ok=True)
for a in ([] if '--audio-only' in sys.argv else json.loads((HERE/'visual_refresh/spaceport_provenance.json').read_text(encoding='utf8'))['assets']):
    master=OUT/(a['key']+'.png')
    if not master.exists():shutil.copy2(a['source'],master)
    im=Image.open(master).convert('RGBA');assert im.getextrema()[3][0]==0
    im=im.crop(im.getchannel('A').getbbox());im.thumbnail((1024,1024),Image.Resampling.LANCZOS)
    im.save(HERE/'art_keyed'/('spaceport_'+a['key']+'.webp'),'WEBP',quality=94,method=6)
    print(a['key'],im.size,flush=True)
audio=HERE/'interaction_audio';rng=random.Random(36);sr=24000
def render(name,duration,fn):
    src=audio/(name+'.wav')
    with wave.open(str(src),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h',int(max(-.9,min(.9,fn(i/sr)))*32767)) for i in range(int(sr*duration))))
    subprocess.run([shutil.which('ffmpeg'),'-y','-loglevel','error','-i',str(src),'-c:a','libopus','-b:a','48k',str(audio/(name+'.ogg'))],check=True)
render('sfx_space_dock',.22,lambda t:.24*math.sin(2*math.pi*(560*t+800*t*t))*math.sin(math.pi*t/.22)**2)
smooth=[0.0]
def noise(t,d):
    smooth[0]=smooth[0]*.8+.2*(rng.random()*2-1)
    return smooth[0]*math.sin(math.pi*t/d)**2
render('sfx_space_puff',.25,lambda t:noise(t,.25)*.7)
render('sfx_space_launch',.85,lambda t:noise(t,.85)*.65+.08*math.sin(2*math.pi*(65*t+65*t*t))*math.sin(math.pi*t/.85)**2)

# Playful synthesized creature chirps (rabbits are quiet in nature), soft sci-fi
# cues and engine sweeps. No speech or long loops competing with number VO.
def chirp(t,d,base,rate):
    env=math.sin(math.pi*t/d)**2
    pulse=max(0,math.sin(2*math.pi*rate*t))**2
    return .32*env*pulse*math.sin(2*math.pi*(base*t+100*t*t)+1.4*math.sin(2*math.pi*22*t))
render('sfx_space_rabbit',.38,lambda t:chirp(t,.38,820,7))
render('sfx_space_squirrel',.42,lambda t:chirp(t,.42,1250,11))
render('sfx_space_ready',.48,lambda t:.18*math.sin(math.pi*t/.48)**2*(math.sin(2*math.pi*(523 if t<.16 else 659 if t<.32 else 784)*t)))
render('sfx_space_ignite',.38,lambda t:noise(t,.38)*.7+.09*math.sin(2*math.pi*(55*t+100*t*t))*math.sin(math.pi*t/.38)**2)
render('sfx_space_flyby',1.05,lambda t:noise(t,1.05)*.7+.11*math.sin(2*math.pi*(320*t-110*t*t))*math.sin(math.pi*t/1.05)**2)
render('sfx_space_travel',1.5,lambda t:noise(t,1.5)*.5+.07*math.sin(2*math.pi*(140*t+100*t*t))*math.sin(math.pi*t/1.5)**2)
