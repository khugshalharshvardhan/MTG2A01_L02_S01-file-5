"""Copy generated masters and export the approved transparent cast for the normal builder."""
from pathlib import Path
from PIL import Image
import json, shutil
HERE=Path(__file__).resolve().parent
OUT=HERE/'visual_refresh/cast_v5';OUT.mkdir(exist_ok=True)
NAMES={'frog_gold':'lesson_friend_gold','frog_teal':'lesson_friend_teal','frog_peach':'lesson_friend_peach','rabbit_cute':'lesson_rabbit_cute','squirrel_cute':'lesson_squirrel_cute','grasshopper_cute':'lesson_grasshopper_cute'}
for a in json.loads((HERE/'visual_refresh/cast_v5_provenance.json').read_text(encoding='utf8'))['assets']:
    master=OUT/(a['key']+'.png')
    if not master.exists():shutil.copy2(a['source'],master)
    im=Image.open(master).convert('RGBA')
    assert im.getextrema()[3][0]==0,'Asset must have real transparency'
    im=im.crop(im.getchannel('A').getbbox());im.thumbnail((1024,1024),Image.Resampling.LANCZOS)
    im.save(HERE/'art_keyed'/(NAMES[a['key']]+'.webp'),'WEBP',quality=94,method=6)
    print(NAMES[a['key']],im.size,flush=True)
