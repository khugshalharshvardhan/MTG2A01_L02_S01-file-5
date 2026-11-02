"""Key the chroma background out of the generated art (gen_objects left it opaque).
Border-connected pixels near the corner colour -> transparent. Enclosed pockets of that colour ->
transparent (characters) or a light glass tint (sp_* domes). Then autocrop.
    python key_art.py 1_SPEC/game_art_src 1_SPEC/art_keyed
"""
import sys, os, glob
from collections import deque
from PIL import Image

def key(path, out):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = im.load()
    corners = [px[3, 3], px[w-4, 3], px[3, h-4], px[w-4, h-4]]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
    def d(c): return ((c[0]-bg[0])**2 + (c[1]-bg[1])**2 + (c[2]-bg[2])**2) ** .5
    TOL, TOL_IN = 95, 70
    magenta = bg[0] > bg[1] + 80 and bg[2] > bg[1] + 40
    seen = bytearray(w*h); dq = deque()
    for x in range(w):
        for y in (0, h-1): dq.append((x, y))
    for y in range(h):
        for x in (0, w-1): dq.append((x, y))
    while dq:
        x, y = dq.popleft(); i = y*w+x
        if seen[i]: continue
        seen[i] = 1
        c0 = px[x, y]
        hue_bg = magenta and c0[0] - c0[1] > 35 and c0[2] - c0[1] > 12
        if c0[3] and d(c0) > TOL and not hue_bg: continue
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny*w+nx]: dq.append((nx, ny))
    glass = os.path.basename(path).startswith("sp_")
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            if c[3] and d(c) <= TOL_IN:
                px[x, y] = (214, 236, 255, 70) if glass else (0, 0, 0, 0)
            elif glass and c[3] and bg[0] > bg[1] + 80 and c[0] - c[1] > 35 and c[2] - c[1] > 12:
                # magenta seen through the glass dome -> light-blue glass, keep the highlight's lightness
                L = (c[0] + c[1] + c[2]) / 3
                t = min(1, max(0, (L - 120) / 135))
                px[x, y] = (int(200 + 45*t), int(228 + 25*t), 255, int(55 + 120*t*t))
    # soften the 1px fringe left by the flood
    bb = im.getchannel("A").getbbox()
    im.crop(bb).save(out)
    print(os.path.basename(path), "bg", bg, "->", im.crop(bb).size)

src, dst = sys.argv[1], sys.argv[2]
for p in sorted(glob.glob(os.path.join(src, "*.png"))):
    key(p, os.path.join(dst, os.path.basename(p)))
