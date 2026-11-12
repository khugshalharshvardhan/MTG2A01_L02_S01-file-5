"""Prepare the approved generated art and quiet interaction audio, without API calls.
Run once before the normal lesson builder. Original generated masters are retained.
"""
from pathlib import Path
from PIL import Image
import json, shutil, math, random, struct, subprocess, wave

HERE = Path(__file__).resolve().parent
ART = HERE / 'art_keyed'
MASTER = HERE / 'visual_refresh' / 'lesson_v4'
SOUNDS = HERE / 'interaction_audio'

def main():
    MASTER.mkdir(exist_ok=True)
    SOUNDS.mkdir(exist_ok=True)
    manifest = json.loads((HERE/'visual_refresh/lesson_v4_provenance.json').read_text(encoding='utf8'))
    sizes = {}
    for asset in manifest['assets']:
        key = asset['key']
        master = MASTER / (key + '.png')
        if not master.exists():
            shutil.copy2(asset['source'], master)
        im = Image.open(master).convert('RGBA')
        if asset['transparent']:
            assert im.getextrema()[3][0] == 0, 'Sprite must have real transparency'
            im = im.crop(im.getchannel('A').getbbox())
        im.thumbnail((2172, 1024) if key == 'pond' else (1024,1024), Image.Resampling.LANCZOS)
        name = 'sc_pond_v4' if key == 'pond' else 'lesson_' + key
        im.save(ART/(name+'.webp'), 'WEBP', quality=94, method=6)
        sizes[name] = list(im.size)
    (MASTER/'sizes.json').write_text(json.dumps(sizes,indent=2),encoding='utf8')
    ref = Path(r'F:\CG Game\FLN\HI02H04_L03_S02 (File9 Hindi)\assets\sfx')
    for source, dest in [('sfx_correct','sfx_ref_correct'),('sfx_wrong','sfx_ref_wrong'),('sfx_tap','sfx_ref_tap')]:
        if (ref/(source+'.ogg')).exists():
            shutil.copy2(ref/(source+'.ogg'), SOUNDS/(dest+'.ogg'))
        else:
            assert (SOUNDS/(dest+'.ogg')).exists(), 'File9 feedback source is missing'
    # Original synthesised foley: soft spring, short croak and a filtered splash.
    # Seeded noise makes this preparation deterministic. No narration is modified.
    sr = 24000
    rng = random.Random(25)
    def render(name, duration, sample):
        wav = SOUNDS/(name+'.wav')
        with wave.open(str(wav),'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes(b''.join(struct.pack('<h', int(max(-.95,min(.95,sample(i/sr)))*32767)) for i in range(int(duration*sr))))
        subprocess.run([shutil.which('ffmpeg'),'-y','-loglevel','error','-i',str(wav),'-c:a','libopus','-b:a','48k',str(SOUNDS/(name+'.ogg'))],check=True)
    render('sfx_frog_hop',.28,lambda t: .38*math.sin(2*math.pi*(420*t+700*t*t))*math.sin(math.pi*t/.28)**2)
    render('sfx_frog_croak',.25,lambda t: .3*(math.sin(2*math.pi*190*t)+.3*math.sin(2*math.pi*380*t))*max(0,math.sin(2*math.pi*16*t))*math.sin(math.pi*t/.25)**2)
    render('sfx_animal_hop',.20,lambda t: .3*math.sin(2*math.pi*(280*t+900*t*t))*math.sin(math.pi*t/.20)**2)
    smooth = [0.0]
    def water(t):
        smooth[0] = .78*smooth[0] + .22*(rng.random()*2-1)
        return .65*smooth[0]*math.sin(math.pi*t/.32)**2 + .09*math.sin(2*math.pi*(800*t-500*t*t))*math.exp(-15*t)
    render('sfx_water_land',.32,water)
    print('Prepared 5 original illustrations and 7 interaction sounds.')

if __name__ == '__main__':
    main()
