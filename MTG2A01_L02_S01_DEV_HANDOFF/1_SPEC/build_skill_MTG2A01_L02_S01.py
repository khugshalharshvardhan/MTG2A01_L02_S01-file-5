"""Build MTG2A01_L02_S01 — «टप्पू मेंढक की कूद» (G2 · skip counting by 2s, 5s and 10s to 100).

ENGINE (r3): the HI02H11_L02_S05 handoff's engine, `4_ENGINE/lesson_template.html` (2026.08.04b-r4-unified
with its shell set: peek-up transition Swifty + whoosh, play/next button sounds, the cover's waiting /
idle-pulse play button and drifting stars, nudge_hand_new, lesson music, the lip-synced celebration
Swifty from celebration_kit/). This lesson's modules (`mtg_modules.js` / `mtg_styles.css`) are
injected into it at build time; the template itself is never edited. This script is the single
choke-point that regenerates 3_BUILD/.

Content is the SME deck 1_SPEC/MTG2A01_L02_S01_FINALreview.pptx applied in full; CHANGES.md maps
every ask to its row.

    PYTHONUTF8=1 python 1_SPEC/build_skill_MTG2A01_L02_S01.py
"""
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "4_ENGINE")
OUT = os.path.join(ROOT, "3_BUILD")
CODE = "MTG2A01_L02_S01"
AUDIO_EXT = "ogg"
KIT_AUDIO = os.path.join(HERE, "kit_audio")      # copied unchanged from HI02H11_L02_S05 (sfx, music, transition VO)
CEL_KIT = os.path.join(ROOT, "celebration_kit")


# --------------------------------------------------------------------------------------
# ENGINE GUARD — pins the bundle-local engine (no MT factory canon ships on this machine)
# --------------------------------------------------------------------------------------
def require_current_engine():
    expect = "2026.08.04b-r4-unified"
    need = ["lesson_template.html", "mtg_modules.js", "mtg_styles.css", "mtg_cover.js", "mtg_cover.css"]
    for n in need:
        if not os.path.isfile(os.path.join(ENGINE, n)):
            sys.exit(f"ENGINE GUARD: 4_ENGINE/{n} missing — refusing to build.")
    src = open(os.path.join(ENGINE, "lesson_template.html"), encoding="utf-8").read()
    if f'ENGINE_VERSION = "{expect}"' not in src:
        sys.exit(f"ENGINE GUARD: lesson_template.html is not {expect} — refusing to build.")
    sha = {n: hashlib.sha256(open(os.path.join(ENGINE, n), "rb").read()).hexdigest()[:12] for n in need}
    print(f"  engine {expect}  " + "  ".join(f"{k} {v}" for k, v in sha.items()))
    return src


# --------------------------------------------------------------------------------------
# NUMBER WORDS (spoken numbers stay Hindi; shown numerals are Arabic — engine NUMERAL POLICY)
# --------------------------------------------------------------------------------------
HI_NUM = ("शून्य एक दो तीन चार पाँच छह सात आठ नौ दस ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह "
          "उन्नीस बीस इक्कीस बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस तीस इकतीस बत्तीस "
          "तैंतीस चौंतीस पैंतीस छत्तीस सैंतीस अड़तीस उनतालीस चालीस इकतालीस बयालीस तैंतालीस चवालीस "
          "पैंतालीस छियालीस सैंतालीस अड़तालीस उनचास पचास इक्यावन बावन तिरपन चौवन पचपन छप्पन सत्तावन "
          "अट्ठावन उनसठ साठ इकसठ बासठ तिरसठ चौंसठ पैंसठ छियासठ सड़सठ अड़सठ उनहत्तर सत्तर इकहत्तर "
          "बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उन्यासी अस्सी इक्यासी बयासी तिरासी "
          "चौरासी पचासी छियासी सत्तासी अट्ठासी नवासी नब्बे इक्यानवे बानवे तिरानवे चौरानवे पचानवे "
          "छियानवे सत्तानवे अट्ठानवे निन्यानवे सौ").split()
assert len(HI_NUM) == 101


VO = {}          # audio id -> exact Hindi line (shown == spoken)


def vo(vid, text):
    if vid in VO and VO[vid] != text:
        raise SystemExit(f"VO id {vid} reused with different text")
    VO[vid] = text
    return vid


def cnt(n):
    """counting word inside a chant: «एक,» — one clip per number, reused everywhere"""
    return vo(f"vo_c_{n}", HI_NUM[n] + ",")


def say(n):
    """game: «पच्चीस!» after a correct drop"""
    return vo(f"vo_g_n_{n}", HI_NUM[n] + "!")


# --------------------------------------------------------------------------------------
# TEACH SCREENS — BRIDGE_TEACH. A step = one deck row: caption (shown), clip list (spoken),
# each clip with the actions that fire as it starts. Verbatim from deck slides 4–6.
# --------------------------------------------------------------------------------------
def clip(vid, text=None, **act):
    if text is not None:
        vo(vid, text)
    return {"vo": vid, **act}


T1 = {   # deck slide 4 — 2s, 0..10
    "lo": 0, "hi": 10, "step": 2, "friend_at": 10, "heading": "दो-दो की गिनती",
    "steps": [
        {"cap": "यह है टप्पू मेंढक। उसका दोस्त पुल के उस पार है। टप्पू दो-दो कदम की छलाँग लगाकर अपने दोस्त से मिलने जाएगा। आइए, उसके साथ गिनते हैं!",
         "clips": [clip("vo_t1_1a", "यह है टप्पू मेंढक।", focus="tappu"),
                   clip("vo_t1_1b", "उसका दोस्त पुल के उस पार है।", focus="friend", wave=True),
                   clip("vo_t1_1c", "टप्पू दो-दो कदम की छलाँग लगाकर अपने दोस्त से मिलने जाएगा। आइए, उसके साथ गिनते हैं!")]},
        {"cap": "टप्पू शून्य पर है। आइए, यहाँ से दो कदम आगे गिनते हैं—एक, दो। टप्पू दो कदम की छलाँग लगाकर दो की संख्या पर पहुँच गया!",
         "clips": [clip("vo_t1_2a", "टप्पू शून्य पर है।", glow=0),
                   clip("vo_t1_2b", "आइए, यहाँ से दो कदम आगे गिनते हैं—"),
                   {"vo": cnt(1), "dot": 1}, {"vo": cnt(2), "dot": 2},
                   clip("vo_t1_2c", "टप्पू दो कदम की छलाँग लगाकर दो की संख्या पर पहुँच गया!", jump=[0, 2])]},
        {"cap": "अब टप्पू दो पर है। वह दो कदम की छलाँग लगाकर कहाँ पहुँचेगा? आइए, दो से आगे दो कदम गिनते हैं—तीन, चार। टप्पू चार पर पहुँच गया!",
         "clips": [clip("vo_t1_3a", "अब टप्पू दो पर है। वह दो कदम की छलाँग लगाकर कहाँ पहुँचेगा?", pause_after=900),
                   clip("vo_t1_3b", "आइए, दो से आगे दो कदम गिनते हैं—"),
                   {"vo": cnt(3), "dot": 3}, {"vo": cnt(4), "dot": 4},
                   clip("vo_t1_3c", "टप्पू चार पर पहुँच गया!", jump=[2, 4])]},
        # ⚑ the deck skips 4→6 (it goes from step 3 straight to «6 से 8»); added on step 4's pattern
        {"cap": "टप्पू ने फिर दो कदम की छलाँग लगाई और छह पर पहुँच गया!",
         "clips": [clip("vo_t1_4x", "टप्पू ने फिर दो कदम की छलाँग लगाई और छह पर पहुँच गया!", jump=[4, 6])]},
        {"cap": "टप्पू ने फिर दो कदम की छलाँग लगाई और आठ पर पहुँच गया!",
         "clips": [clip("vo_t1_4", "टप्पू ने फिर दो कदम की छलाँग लगाई और आठ पर पहुँच गया!", jump=[6, 8])]},
        {"cap": "दो कदम की एक और छलाँग—दस! टप्पू अपने दोस्त से मिल गया!",
         "clips": [clip("vo_t1_5", "दो कदम की एक और छलाँग—दस! टप्पू अपने दोस्त से मिल गया!", jump=[8, 10], wave_end=True)]},
        {"cap": "टप्पू अपने दोस्त से मिल गया! हमने दो-दो की गिनती करके उसे पुल पार कराया—दो, चार, छह, आठ, दस!",
         "clips": [clip("vo_t1_6a", "टप्पू अपने दोस्त से मिल गया!", happy=True),
                   clip("vo_t1_6b", "हमने दो-दो की गिनती करके उसे पुल पार कराया—")]
                  + [{"vo": cnt(n), "mark": n} for n in (2, 4, 6, 8, 10)]},
    ],
}

T2 = {   # deck slide 5 — 5s, 0..30, camera (as T3), two child taps
    "lo": 0, "hi": 30, "step": 5, "friend_at": 30, "heading": "पाँच-पाँच की गिनती", "camera": True,
    "steps": [
        {"cap": "टप्पू का एक और दोस्त पुल के उस पार इंतज़ार कर रहा है। इस बार टप्पू पाँच-पाँच कदम की छलाँग लगाकर उससे मिलने जाएगा। आइए, टप्पू के साथ गिनते हैं!",
         "clips": [clip("vo_t2_1", "टप्पू का एक और दोस्त पुल के उस पार इंतज़ार कर रहा है। इस बार टप्पू पाँच-पाँच कदम की छलाँग लगाकर उससे मिलने जाएगा। आइए, टप्पू के साथ गिनते हैं!", wave=True, glow_end=0, cam="all")]},
        {"cap": "टप्पू शून्य पर है। यहाँ से पाँच कदम आगे गिनते हैं—एक, दो, तीन, चार, पाँच। टप्पू पाँच पर पहुँच गया!",
         "clips": [clip("vo_t2_2a", "टप्पू शून्य पर है। यहाँ से पाँच कदम आगे गिनते हैं—", cam="follow")]
                  + [{"vo": cnt(n), "dot": n} for n in (1, 2, 3, 4, 5)]
                  + [clip("vo_t2_2b", "टप्पू पाँच पर पहुँच गया!", jump=[0, 5])]},
        {"cap": "टप्पू पाँच से पाँच कदम आगे कूदकर दस पर पहुँच गया!",
         "clips": [clip("vo_t2_3", "टप्पू पाँच से पाँच कदम आगे कूदकर दस पर पहुँच गया!", jump=[5, 10])]},
        {"cap": "फिर पाँच कदम की छलाँग लगाई और पंद्रह पर पहुँच गया!",
         "clips": [clip("vo_t2_4", "फिर पाँच कदम की छलाँग लगाई और पंद्रह पर पहुँच गया!", jump=[10, 15])]},
        {"cap": "एक और पाँच कदम की छलाँग! अब टप्पू बीस पर है।",
         "clips": [clip("vo_t2_5", "एक और पाँच कदम की छलाँग! अब टप्पू बीस पर है।", jump=[15, 20], pause_after=700)]},
        {"cap": "अब आप टप्पू पर टैप कीजिए। वह पाँच कदम आगे कूदेगा!",
         "clips": [clip("vo_t2_6", "अब आप टप्पू पर टैप कीजिए। वह पाँच कदम आगे कूदेगा!", cam=[19, 31], tapcue=True)]},
        {"cap": "देखिए! टप्पू पच्चीस पर पहुँच गया!", "wait_tap": True,
         "clips": [clip("vo_t2_7", "देखिए! टप्पू पच्चीस पर पहुँच गया!", jump=[20, 25])]},
        {"cap": "टप्पू पर फिर टैप कीजिए।",
         "clips": [clip("vo_t2_8", "टप्पू पर फिर टैप कीजिए।", wave=True)]},
        {"cap": "पाँच कदम की एक और छलाँग लगाकर टप्पू तीस पर पहुँच गया!", "wait_tap": True,
         "clips": [clip("vo_t2_9", "पाँच कदम की एक और छलाँग लगाकर टप्पू तीस पर पहुँच गया!", jump=[25, 30])]},
        {"cap": "वाह! टप्पू अपने दोस्त से मिल गया!",
         "clips": [clip("vo_met", "वाह! टप्पू अपने दोस्त से मिल गया!", happy=True, cam="all")]},
        {"cap": "पाँच, दस, पंद्रह, बीस, पच्चीस, तीस! ऐसे हम पाँच-पाँच करके गिनते हैं।",
         "clips": [{"vo": cnt(n), "mark": n} for n in (5, 10, 15, 20, 25, 30)]
                  + [clip("vo_t2_11", "ऐसे हम पाँच-पाँच करके गिनते हैं।")]},
    ],
}

T3 = {   # deck slide 6 — 10s, 0..50, camera, two child taps
    "lo": 0, "hi": 50, "step": 10, "friend_at": 50, "heading": "दस-दस की गिनती", "camera": True,
    "steps": [
        {"cap": "टप्पू का एक और दोस्त पुल के उस पार है। इस बार टप्पू दस-दस कदम की छलाँग लगाकर उससे मिलने जाएगा। आइए, उसके साथ गिनते हैं!",
         "clips": [clip("vo_t3_1", "टप्पू का एक और दोस्त पुल के उस पार है। इस बार टप्पू दस-दस कदम की छलाँग लगाकर उससे मिलने जाएगा। आइए, उसके साथ गिनते हैं!", wave=True, cam="all")]},
        {"cap": "टप्पू शून्य पर है। वह दस कदम की छलाँग लगाकर दस पर पहुँच गया!",
         "clips": [clip("vo_t3_2a", "टप्पू शून्य पर है।", glow=0, cam="follow"),
                   clip("vo_t3_2b", "वह दस कदम की छलाँग लगाकर दस पर पहुँच गया!", span=[0, 10], jump=[0, 10])]},
        {"cap": "फिर दस कदम की छलाँग लगाई और बीस पर पहुँच गया!",
         "clips": [clip("vo_t3_3", "फिर दस कदम की छलाँग लगाई और बीस पर पहुँच गया!", jump=[10, 20])]},
        {"cap": "एक और दस कदम की छलाँग! अब टप्पू तीस पर है।",
         "clips": [clip("vo_t3_4", "एक और दस कदम की छलाँग! अब टप्पू तीस पर है।", jump=[20, 30], pause_after=700)]},
        {"cap": "टप्पू पर टैप कीजिए।",       # OST (the VO is longer)
         "clips": [clip("vo_t3_5", "अब आप टप्पू पर टैप कीजिए। वह दस कदम आगे कूदेगा!", cam=[29, 51], tapcue=True)]},
        {"cap": "देखिए! टप्पू चालीस पर पहुँच गया!", "wait_tap": True,
         "clips": [clip("vo_t3_6", "देखिए! टप्पू चालीस पर पहुँच गया!", jump=[30, 40])]},
        {"cap": "टप्पू पर फिर टैप कीजिए।",
         "clips": [{"vo": "vo_t2_8", "wave": True}]},
        {"cap": "दस कदम की एक और छलाँग लगाकर टप्पू पचास पर पहुँच गया!", "wait_tap": True,
         "clips": [clip("vo_t3_8", "दस कदम की एक और छलाँग लगाकर टप्पू पचास पर पहुँच गया!", jump=[40, 50])]},
        {"cap": "वाह! टप्पू अपने दोस्त से मिल गया! हमने दस-दस करके गिना—दस, बीस, तीस, चालीस, पचास!",
         "clips": [{"vo": "vo_met", "happy": True, "cam": "all"},
                   clip("vo_t3_9b", "हमने दस-दस करके गिना—")]
                  + [{"vo": cnt(n), "mark": n} for n in (10, 20, 30, 40, 50)]},
    ],
}


# --------------------------------------------------------------------------------------
# GUIDED Q1–Q3 — JUMP_PICK (deck slide 7 + its notes)
# --------------------------------------------------------------------------------------
def jump_pick(qid, lo, hi, prior, at, step, options, ans, q_clips, wa1, wa2, wa3, correct, correct_ost):
    return {
        "lo": lo, "hi": hi, "prior": prior, "at": at, "step": step, "options": options, "answer": ans,
        "q": q_clips, "ost": "सही संख्या पर टैप कीजिए।",
        "wa1": wa1, "wa2": wa2, "wa3": wa3, "correct": correct, "correct_ost": correct_ost,
    }


Q1 = jump_pick(
    "q1", 40, 65, [40, 45, 50], 50, 5, [51, 55, 60], 55,
    [clip("vo_q1_a", "मेंढक को आगे जाना है।"), clip("vo_q1_b", "वह पचास पर है।", glow=50),
     clip("vo_q1_c", "पाँच कदम की छलाँग लगाकर वह किस संख्या पर पहुँचेगा? सही संख्या पर टैप कीजिए।")],
    {"vo": vo("vo_q1_wa1", "मेंढक पचास पर है। पाँच कदम आगे कहाँ पहुँचेगा? सही संख्या पर टैप कीजिए।"), "ost": "सही संख्या पर टैप कीजिए।"},
    {"vo": vo("vo_q1_wa2", "पचास से पाँच कदम आगे देखिए।"), "ost": "पचास से पाँच कदम आगे देखिए।"},
    {"vo": vo("vo_q1_wa3", "मेंढक पाँच कदम की छलाँग लगाकर पचपन पर पहुँचेगा।"), "ost": "मेंढक पाँच कदम की छलाँग लगाकर पचपन पर पहुँचेगा।"},
    vo("vo_q1_ok", "शाबाश! पाँच कदम आगे - पचपन!"), "शाबाश! 55")

Q2 = jump_pick(
    "q2", 8, 20, [10, 12, 14], 14, 2, [15, 16, 18], 16,
    [clip("vo_q2_a", "मेंढक चौदह पर है।", glow=14),
     clip("vo_q2_b", "दो कदम आगे कहाँ पहुँचेगा? सही संख्या पर टैप कीजिए।")],
    {"replay_q": True, "ost": "सही संख्या पर टैप कीजिए।"},
    {"vo": vo("vo_q2_wa2", "चौदह से दो कदम आगे देखिए।"), "ost": "चौदह से दो कदम आगे देखिए।"},
    {"vo": vo("vo_q2_wa3", "मेंढक दो कदम की छलाँग लगाकर सोलह पर पहुँचेगा।"), "ost": "मेंढक दो कदम की छलाँग लगाकर सोलह पर पहुँचेगा।"},
    vo("vo_q2_ok", "शाबाश! दो कदम आगे—सोलह!"), "सही! 16")

Q3 = jump_pick(
    "q3", 10, 55, [10, 20, 30], 30, 10, [35, 50, 40], 40,
    [clip("vo_q3_a", "मेंढक तीस पर है।", glow=30),
     clip("vo_q3_b", "दस कदम आगे कहाँ पहुँचेगा? सही संख्या पर टैप कीजिए।")],
    {"replay_q": True, "ost": "सही संख्या पर टैप कीजिए।"},
    {"vo": vo("vo_q3_wa2", "तीस से दस कदम आगे देखिए।"), "ost": "तीस से दस कदम आगे देखिए।"},
    {"vo": vo("vo_q3_wa3", "मेंढक दस कदम की छलाँग लगाकर चालीस पर पहुँचेगा।"), "ost": "मेंढक दस कदम की छलाँग लगाकर चालीस पर पहुँचेगा।"},
    vo("vo_q3_ok", "शाबाश! दस कदम आगे—चालीस!"), "सही! 40")


# --------------------------------------------------------------------------------------
# Q4–Q7 — SEQ_FILL (deck slides 8–11). One ladder per blank: WA1 wiggle, WA2 number-line hint
# popup, WA3 fade the rest + pulse/hand on the answer.
# --------------------------------------------------------------------------------------
def blank(ans, frm, step, correct, wa1, hint, wa3, pre_hint=None, after_hint=None, wa1_ost=None):
    return {"answer": ans, "from": frm, "step": step, "correct": correct,
            "wa1": wa1, "wa1_ost": wa1_ost, "pre_hint": pre_hint, "hint": hint,
            "hint_range": [frm - 1, frm + step + (1 if step == 2 else 0)] if step < 10 else [frm, frm + 10],
            "after_hint": after_hint, "wa3": wa3}


Q4 = {   # deck slide 8 — grasshopper hops 30→36, then «?»
    "seq": [30, 32, 34, 36, None], "options": [40, 37, 38], "animal": "chr_grasshopper",
    "intro": [clip("vo_q4_1", "टिड्डा तीस पर है। आइए, उसके साथ दो-दो करके गिनते हैं।", reveal=0),
              clip("vo_q4_2", "बत्तीस…", reveal=1, hop=1),
              clip("vo_q4_3", "चौंतीस…", reveal=2, hop=2),
              clip("vo_q4_4", "छत्तीस!", reveal=3, hop=3)],
    "q": [clip("vo_q4_5", "अगली छलाँग में टिड्डा कहाँ पहुँचेगा? सही संख्या पर टैप कीजिए।", reveal_blank=True)],
    "ost": "अगली सही संख्या पर टैप कीजिए।",
    "blanks": [blank(38, 36, 2, vo("vo_q4_ok", "शाबाश! छत्तीस से दो आगे—अड़तीस!"),
                     vo("vo_q4_wa1", "दो-दो करके गिनिए। अगली सही संख्या पर टैप कीजिए।"),
                     vo("vo_q4_hint", "छत्तीस से दो कदम आगे देखिए।"),
                     # ⚑ deck says «मेंढक»; the animal on this screen is the grasshopper
                     vo("vo_q4_wa3", "टिड्डा दो कदम की छलाँग लगाकर अड़तीस पर पहुँचेगा।"),
                     after_hint=vo("vo_q4_after", "अगली संख्या क्या होगी? सही संख्या पर टैप कीजिए।"),
                     wa1_ost="दो-दो करके गिनिए। अगली सही संख्या पर टैप कीजिए।")],
}
Q4["blanks"][0]["hint_range"] = [34, 40]
Q4["blanks"][0]["after_hint_ost"] = "अगली सही संख्या पर टैप कीजिए।"

Q5 = {   # deck slide 9 — rabbit, 10…16, __, __
    "seq": [10, 12, 14, 16, None, None], "options": [17, 18, 19, 20], "animal": "chr_rabbit",
    "q": [clip("vo_q5_q", "खरगोश दो-दो करके गिन रहा है। उसकी गिनती में दो संख्याएँ छूट गई हैं। सही संख्याओं पर टैप करके गिनती पूरी कीजिए।")],
    "ost": "दो-दो करके गिनिए। सही संख्या पर टैप कीजिए।",
    "blanks": [
        blank(18, 16, 2, vo("vo_q5_ok1", "सही! सोलह से दो आगे—अठारह!"),
              vo("vo_q5_wa1", "दो-दो करके गिनिए। खाली जगह के लिए सही संख्या पर टैप कीजिए।"),
              vo("vo_q5_hint1", "सोलह से दो कदम आगे देखिए।"),
              vo("vo_q5_wa3a", "खरगोश दो कदम की छलाँग लगाकर अठारह पर पहुँचेगा।"),   # ⚑ deck: «मेंढक»
              after_hint=vo("vo_after_tap", "सही संख्या पर टैप कीजिए।"), wa1_ost="सही संख्या पर टैप कीजिए।"),
        blank(20, 18, 2, vo("vo_q5_ok2", "शाबाश! अठारह से दो आगे—बीस!"),
              "vo_q5_wa1", vo("vo_q5_hint2", "अठारह से दो कदम आगे देखिए।"),
              vo("vo_q5_wa3b", "खरगोश दो कदम की छलाँग लगाकर बीस पर पहुँचेगा।"),      # ⚑ deck: «मेंढक»
              after_hint="vo_after_tap", wa1_ost="सही संख्या पर टैप कीजिए।"),
    ],
}
Q5["blanks"][0]["hint_range"] = [14, 20]
Q5["blanks"][1]["hint_range"] = [16, 22]

Q6 = {   # deck slide 10 — squirrel (the VO's गिलहरी), 55,60,65,__,__
    "seq": [55, 60, 65, None, None], "options": [66, 70, 75, 80], "animal": "chr_squirrel",
    "q": [clip("vo_q6_q", "गिलहरी पाँच-पाँच करके आगे गिन रही है। उसकी गिनती पूरी करने में मदद कीजिए। खाली जगहों के लिए सही संख्याओं पर टैप कीजिए।")],
    "ost": "पाँच-पाँच करके गिनती पूरी कीजिए।",
    "blanks": [
        blank(70, 65, 5, vo("vo_q6_ok1", "सही! पैंसठ के बाद पाँच आगे गिनने पर सत्तर आता है।"),
              vo("vo_q6_wa1", "पाँच-पाँच करके गिनिए। सही संख्या पर टैप कीजिए।"),
              vo("vo_q6_hint1", "पैंसठ से पाँच कदम आगे देखिए।"),
              vo("vo_q6_wa3a", "पाँच कदम की छलाँग लगाकर सत्तर पर पहुँचेगा।"),
              after_hint="vo_after_tap", wa1_ost="पाँच-पाँच करके गिनिए। सही संख्या पर टैप कीजिए।"),
        blank(75, 70, 5, vo("vo_q6_ok2", "शाबाश! सत्तर से पाँच आगे गिनने पर पचहत्तर आता है। गिलहरी की गिनती पूरी हो गई!"),
              "vo_q6_wa1", vo("vo_q6_hint2", "सत्तर से पाँच कदम आगे देखिए।"),
              # ⚑ deck: «…सत्तर पर पहुँचेगी» — the answer is 75
              vo("vo_q6_wa3b", "गिलहरी पाँच कदम की छलाँग लगाकर पचहत्तर पर पहुँचेगी।"),
              after_hint="vo_after_tap", wa1_ost="पाँच-पाँच करके गिनिए। सही संख्या पर टैप कीजिए।"),
    ],
}
Q6["blanks"][0]["hint_range"] = [64, 70]
Q6["blanks"][1]["hint_range"] = [69, 75]

Q7 = {   # deck slide 11 — grasshopper, 50,60,__,80,__,100
    "seq": [50, 60, None, 80, None, 100], "options": [61, 70, 75, 90], "animal": "chr_grasshopper",
    "q": [clip("vo_q7_q", "दस-दस करके गिनिए। खाली जगह के लिए सही संख्या पर टैप कीजिए।")],
    "ost": "सही संख्या पर टैप कीजिए।",
    "blanks": [
        blank(70, 60, 10, vo("vo_q7_ok1", "सही! साठ से दस आगे—सत्तर!"),
              vo("vo_q7_wa1", "दस-दस करके गिनिए। सही संख्या पर टैप कीजिए।"),
              vo("vo_q7_hint1", "साठ से दस कदम आगे देखिए।"),
              vo("vo_q7_wa3a", "टिड्डा दस कदम की छलाँग लगाकर सत्तर पर पहुँचेगा।"),
              pre_hint=vo("vo_q7_pre1", "साठ से दस आगे गिनिए।"),
              after_hint="vo_after_tap", wa1_ost="दस-दस करके गिनिए। सही संख्या पर टैप कीजिए।"),
        blank(90, 80, 10, vo("vo_q7_ok2", "शाबाश! अस्सी से दस आगे—नब्बे!"),
              "vo_q7_wa1", vo("vo_q7_hint2", "अस्सी से दस कदम आगे देखिए।"),
              vo("vo_q7_wa3b", "टिड्डा दस कदम की छलाँग लगाकर नब्बे पर पहुँचेगा।"),
              pre_hint=vo("vo_q7_pre2", "अस्सी से दस आगे गिनिए।"),
              after_hint="vo_after_tap", wa1_ost="दस-दस करके गिनिए। सही संख्या पर टैप कीजिए।"),
    ],
}


# --------------------------------------------------------------------------------------
# INDEPENDENT GAME — SPACE_PODS «अंतरिक्ष की सैर» (deck slides 12–16, number sets = slide 15)
# --------------------------------------------------------------------------------------
STEP_WORD = {2: "दो-दो", 5: "पाँच-पाँच", 10: "दस-दस"}
ROUNDS = {   # (start, prefilled pod indexes, distractors) — slide 15 table
    2: [(23, [0, 2], [26]), (42, [0, 4], [45]), (61, [0, 1], [66, 68])],
    5: [(25, [0, 4], [36]), (40, [0, 2], [52]), (65, [0, 1], [76, 84])],
    10: [(30, [0, 1], [55]), (50, [0, 2], [75]), (60, [0, 4], [85, 95])],
}
CAST = {2: "sp_frog", 5: "sp_rabbit", 10: "sp_squirrel"}   # the user's game art (1_SPEC/art_user_src/game *.png)
LEVEL_DONE = {
    2: "वाह! दो-दो की गिनती से सभी यान उड़ गए! अब दूसरी गिनती चुनिए।",
    5: "वाह! पाँच-पाँच की गिनती से सभी यान उड़ गए! अब दूसरी गिनती चुनिए।",
    10: "वाह! दस-दस की गिनती से सभी यान उड़ गए! अब दूसरी गिनती चुनिए।",
}


def game():
    levels = []
    for step in (2, 5, 10):
        rounds = []
        for r, (start, pre, extra) in enumerate(ROUNDS[step]):
            seq = [start + i * step for i in range(5)]
            assert seq[-1] <= 100 and not set(extra) & set(seq)
            for n in seq:
                say(n)
            rounds.append({
                "seq": seq, "prefilled": pre, "distractors": extra,
                "vo": vo(f"vo_g_r_{step}_{r+1}",
                         f"कुछ साथी यानों में बैठ गए हैं। {HI_NUM[start]} से {STEP_WORD[step]} करके गिनिए और खाली यानों में सही साथियों को बिठाइए!"),
            })
        levels.append({
            "step": step, "label": f"{STEP_WORD[step]} की गिनती", "cast": CAST[step], "rounds": rounds,
            "wrong": vo(f"vo_g_wrong_{step}", f"अरे! {STEP_WORD[step]} करके गिनिए। फिर कोशिश कीजिए!"),
            "done": vo(f"vo_g_done_{step}", LEVEL_DONE[step]),
        })
    return {
        "title": "अंतरिक्ष की सैर", "levels": levels,
        "menu_vo": vo("vo_g_menu", "अंतरिक्ष की सैर के लिए यात्री तैयार हैं! सही संख्या वाले यात्रियों को खाली यानों में बिठाइए। पहले चुनिए—दो-दो, पाँच-पाँच या दस-दस की गिनती।"),
        "guide_vo": vo("vo_g_guide", "सही साथी को खींचकर खाली यान में बिठाइए।"),
        "round_done_vo": vo("vo_g_round_done", "शाबाश! गिनती पूरी हुई। साथियो, उड़ान भरिए!"),
        "all_done_vo": vo("vo_g_all_done", "कमाल! आपने दो-दो, पाँच-पाँच और दस-दस करके गिनती पूरी कर ली!"),
        "inactivity_ms": 7000,
        # badge = number patch on each astronaut's chest, as fractions of the sprite (measured)
        "badge": {"sp_frog": [0.51, 0.62], "sp_rabbit": [0.52, 0.68], "sp_squirrel": [0.70, 0.62]},   # on each suit's chest star
        # rider = [helmet centre x, helmet top y] as sprite fractions (measured), to sit the helmet in a pod's dome
        "rider": {"sp_frog": [0.48, 0.02], "sp_rabbit": [0.48, 0.15], "sp_squirrel": [0.57, 0.08]},
    }


# --------------------------------------------------------------------------------------
# CARD
# --------------------------------------------------------------------------------------
def slide(sid, phase, typ, prompt, data, audio=None):
    return {"id": sid, "phase": phase, "eis": "iconic", "type": typ, "prompt_hi": prompt,
            "audio": audio or {}, "data": data}


def build_card():
    vo("vo_landing", "नमस्ते! आज हम टप्पू मेंढक के साथ कूद-कूद कर गिनती करेंगे — दो-दो, पाँच-पाँच और दस-दस की कूद!")
    vo("vo_pt_tutorial", "ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!")
    vo("vo_pt_guided", "बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!")
    vo("vo_pt_practice", "वाह! अब आपकी बारी।")
    vo("vo_well_done", "शाबाश! तुमने कूद-कूद कर गिनती सीख ली!")

    slides = [
        slide("T1", "tutorial", "BRIDGE_TEACH", "", T1),
        slide("T2", "tutorial", "BRIDGE_TEACH", "", T2),
        slide("T3", "tutorial", "BRIDGE_TEACH", "", T3),
        slide("G1", "guided", "JUMP_PICK", Q1["ost"], Q1),
        slide("G2", "guided", "JUMP_PICK", Q2["ost"], Q2),
        slide("G3", "guided", "JUMP_PICK", Q3["ost"], Q3),
        slide("G4", "guided", "SEQ_FILL", Q4["ost"], Q4),
        slide("G5", "guided", "SEQ_FILL", Q5["ost"], Q5),
        slide("G6", "guided", "SEQ_FILL", Q6["ost"], Q6),
        slide("G7", "guided", "SEQ_FILL", Q7["ost"], Q7),
        slide("GAME", "practice", "SPACE_PODS", "", game()),
        {"id": "CEL", "phase": "mastery", "eis": "enactive", "type": "CELEBRATION",
         "prompt_hi": "शाबाश! तुमने कूद-कूद कर गिनती सीख ली!",
         "audio": {"prompt": "vo_well_done", "sfx": "sfx_celebrate"}, "data": {}},
    ]
    # voice roles as metadata (the modules own their audio; the engine's auto-chain is skipped, so
    # these only document which clip is the prompt / hint / reveal for QA and the receipt)
    for s in slides:
        d, t = s["data"], s["type"]
        if t == "BRIDGE_TEACH":
            s["audio"] = {"prompt": d["steps"][0]["clips"][0]["vo"]}
        elif t == "JUMP_PICK":
            s["audio"] = {"prompt": d["q"][0]["vo"], "hint": d["wa2"]["vo"], "reveal": d["wa3"]["vo"], "correct": d["correct"]}
        elif t == "SEQ_FILL":
            s["audio"] = {"prompt": (d.get("intro") or d["q"])[0]["vo"], "hint": d["blanks"][0]["hint"],
                          "reveal": d["blanks"][0]["wa3"], "correct": d["blanks"][-1]["correct"]}
        elif t == "SPACE_PODS":
            s["audio"] = {"prompt": d["menu_vo"]}
    phases = {}
    for s in slides:
        phases[s["phase"]] = phases.get(s["phase"], 0) + 1
    return {
        "version": "0.2",
        "skill_code": CODE, "lo_code": "MTG2A01_L02", "grade": "G2", "attribute": "A01",
        "skill_type": "CORE", "part_label": "",
        "title": {"hi": "टप्पू मेंढक की कूद", "en": "Skip counting by 2s, 5s and 10s (to 100)"},
        "subtitle_hi": "दो-दो, पाँच-पाँच, दस-दस की कूद",
        "skill_description_hi": "दो-दो, पाँच-पाँच और दस-दस की कूद लगाकर सौ तक संख्या-क्रम पूरा करना।",
        "theme": "toybox",
        "landing_audio": "vo_landing",
        # file4-style cover: टप्पू hops in, the cloud gathers, the title is written on it (mtg_cover.js)
        "landing_hero": {"kind": "frog_cover"},
        # --- file4's shell, configured as HI02H11_L02_S05 configures it ---
        "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided", "practice": "vo_pt_practice"},
        "ui_sfx": {"play": "sfx_play_button", "next": "sfx_next_button"},
        # the transition clips are file4's recordings of the same three lines, so its measured cues hold:
        # where «चलिए, शुरू करें!» / «चलिए, साथ में करें!» / «अब आपकी बारी!» starts inside each clip
        "gate": {"title_cue_ms": {"tutorial": 3370, "guided": 3520, "practice": 940}},
        # file4's button rule: teach pages keep आगे; from the first question on, a solved page moves
        # on by itself with the button hidden (file4 hard-codes index 5; here it is the card's call)
        "auto_advance_from": 3,
        "phase_distribution": phases,
        "scaffold_rules": {"nudge_timeout_ms": {"guided": 6000, "practice": 8000},
                           "max_attempts": 3, "hint_levels": 3, "hand_on_attempt": 3,
                           "hand_on_hint3": True, "lock_after_hint3": True,
                           "reveal_on_attempt": None, "silent_on_late_correct": True},
        "signals_expected": ["slide_entered", "slide_completed", "teach_done", "jump_pick_correct",
                             "seq_fill_correct", "space_round_done", "lesson_completed"],
        "slides": slides,
        "assets": {
            "audio_ext": AUDIO_EXT, "img_ext": "webp",
            "audio": {k: f"assets/Audio/{k}.{AUDIO_EXT}" for k in list(VO) + [i for i in KIT_IDS if i not in VO]},
            "audio_text": dict(VO),
        },
    }


FFMPEG = shutil.which("ffmpeg")
# file4's fixed clips, shipped unchanged: button / feedback / transition sounds, the lesson music and the
# three recorded transition lines (same words as ours, so CARD.gate.title_cue_ms is file4's measurement)
KIT_IDS = ["sfx_celebrate", "sfx_correct", "sfx_wrong", "sfx_tap", "sfx_pop", "sfx_fb_correct",
           "sfx_fb_incorrect", "sfx_play_button", "sfx_next_button", "sfx_whoosh", "bgm_lesson",
           "vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice"]
KIT_VO = {"vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice"}


def _stale(src, dst):
    return not os.path.isfile(dst) or os.path.getmtime(dst) < os.path.getmtime(src)


def _closing_tag_guard(name, txt, bad):
    # a literal closing tag anywhere in injected source (even in a comment) ends the host element
    if bad in txt:
        sys.exit(f"X  {name} contains a literal {bad} — write it as '</sty' + 'le>' / '</scr' + 'ipt>'")


def assets(html, card):
    """3_BUILD/assets is GENERATED: our VO as Opus .ogg (mono) from the TTS WAVs, file4's kit audio
    unchanged, WebP sprites, and only the UI files the page asks for."""
    from PIL import Image
    import subprocess
    aud = os.path.join(OUT, "assets", "Audio"); img = os.path.join(OUT, "assets", "Images"); ui = os.path.join(OUT, "assets", "UI")
    for p in (aud, img, ui):
        os.makedirs(p, exist_ok=True)
    wav = os.path.join(HERE, "vo_src_wav")
    want = set()
    for k in VO:
        if k in KIT_VO:
            continue
        src, dst = os.path.join(wav, k + ".wav"), os.path.join(aud, f"{k}.{AUDIO_EXT}")
        want.add(os.path.basename(dst))
        if os.path.isfile(src) and _stale(src, dst):
            if not FFMPEG:
                sys.exit("ffmpeg not on PATH — needed to encode the VO")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-ac", "1",
                            "-codec:a", "libopus", "-b:a", "40k", "-f", "ogg", dst], check=True)
    for k in KIT_IDS:
        src, dst = os.path.join(KIT_AUDIO, k + ".ogg"), os.path.join(aud, k + ".ogg")
        want.add(k + ".ogg")
        if _stale(src, dst):
            shutil.copy2(src, dst)
    for f in os.listdir(aud):
        if f not in want:
            os.remove(os.path.join(aud, f))
    keyed = os.path.join(HERE, "art_keyed")
    for f in os.listdir(keyed):
        src = os.path.join(keyed, f)
        dst = os.path.join(img, f if f.endswith(".svg") else os.path.splitext(f)[0] + ".webp")
        if f.endswith((".webp", ".svg")):
            if _stale(src, dst):
                shutil.copy2(src, dst)
        elif f.endswith(".png"):
            im = Image.open(src).convert("RGBA")
            im.thumbnail((1024, 1024), Image.LANCZOS)
            if _stale(src, dst) or Image.open(dst).size != im.size:
                im.save(dst, "WEBP", quality=94, method=6)
    # file4's drawn play button (and its grey "waiting" twin) live in assets/Images in that engine
    kimg = os.path.join(ENGINE, "kit_images")
    for f in os.listdir(kimg):
        if _stale(os.path.join(kimg, f), os.path.join(img, f)):
            shutil.copy2(os.path.join(kimg, f), os.path.join(img, f))
    # UI: a file the page names, plus the expression heads the engine assembles ("sw_head_" + expr)
    kit = os.path.join(ENGINE, "ui_kit")
    keep = {f for f in os.listdir(kit) if os.path.isfile(os.path.join(kit, f))
            and (f in html or f.startswith("sw_head_"))}
    for f in keep:
        if _stale(os.path.join(kit, f), os.path.join(ui, f)):
            shutil.copy2(os.path.join(kit, f), os.path.join(ui, f))
    for f in os.listdir(ui):
        if os.path.isfile(os.path.join(ui, f)) and f not in keep:
            os.remove(os.path.join(ui, f))
    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"  assets: {len(os.listdir(aud))} audio · {len(os.listdir(img))} images · {len(keep)} UI"
          f" (+ celebration sheets) · bundle {size/1e6:.1f} MB")


# ---------------------------------------------------------------- the celebration Swifty (file4 r85)
def celebration_anim(card):
    """file4's lip-synced celebration: the kit's three sheets copied unchanged, the lip-sync track
    measured from OUR celebration line by the kit's own make_lipsync.py."""
    import filecmp, tempfile, subprocess
    cel = [x for x in card["slides"] if x["type"] == "CELEBRATION"]
    vo_id = cel and (cel[0].get("audio") or {}).get("prompt")
    vo_path = vo_id and os.path.join(OUT, "assets", "Audio", f"{vo_id}.{AUDIO_EXT}")
    if not (os.path.isdir(CEL_KIT) and vo_path and os.path.isfile(vo_path)):
        print("  !!  celebration Swifty skipped (kit or %s missing)" % vo_id)
        return None
    meta = json.load(open(os.path.join(CEL_KIT, "sheets", "cel_meta.json"), encoding="utf-8"))
    cel_dir = os.path.join(OUT, "assets", "UI", "celebration")
    os.makedirs(cel_dir, exist_ok=True)
    for sheet in (meta["shabaash"]["src"], meta["talk"]["src"], meta["idle"]["src"]):
        a, b = os.path.join(CEL_KIT, "sheets", sheet), os.path.join(cel_dir, sheet)
        if not (os.path.isfile(b) and filecmp.cmp(a, b, shallow=False)):
            shutil.copy2(a, b)
    out = os.path.join(tempfile.gettempdir(), f"cel_track_{CODE}.json")
    subprocess.run([sys.executable, os.path.join(CEL_KIT, "make_lipsync.py"), vo_path, "--json", out],
                   check=True, capture_output=True)
    track = json.load(open(out, encoding="utf-8"))
    if "1" not in track["bits"]:
        sys.exit("X  the celebration VO measured silent - no lip-sync track")
    print(f"  celebration Swifty: lip-sync from {vo_id} ({track['ms']} ms)")
    return {"base": "assets/UI/celebration/", "vo": vo_id, "meta": meta, "track": track}


def inject_celebration(html):
    css = open(os.path.join(CEL_KIT, "swiftie_celebration.css"), encoding="utf-8").read()
    js = open(os.path.join(CEL_KIT, "swiftie_celebration.js"), encoding="utf-8").read()
    wrap = open(os.path.join(HERE, "cel_wrap.js"), encoding="utf-8").read()
    i = html.index("</head>")
    html = html[:i] + '<style id="swcKitCss">\n' + css + "</style>\n" + html[i:]
    i = html.rindex("</body>")
    return html[:i] + '<script id="swcKit">\n' + js + "\n" + wrap + "</script>\n" + html[i:]


def compile_html(tmpl, card):
    import re
    mods = (open(os.path.join(ENGINE, "mtg_modules.js"), encoding="utf-8").read() + chr(10)
            + open(os.path.join(ENGINE, "mtg_cover.js"), encoding="utf-8").read())
    css = (open(os.path.join(ENGINE, "mtg_styles.css"), encoding="utf-8").read() + chr(10)
           + open(os.path.join(ENGINE, "mtg_cover.css"), encoding="utf-8").read())
    _closing_tag_guard("mtg_modules.js", mods, "</script>")
    _closing_tag_guard("mtg_styles.css", css, "</style>")
    html = tmpl
    # the card
    tag = re.compile(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', re.S)
    if not tag.search(html):
        sys.exit("X  cardData tag not found in the template")
    html = tag.sub(lambda m: m.group(1) + "\n" + json.dumps(card, ensure_ascii=False, indent=1) + "\n" + m.group(3), html, count=1)
    html = re.sub(r"<title>.*?</title>", f"<title>SwiftPAL · {CODE} · {card['title']['hi']}</title>", html, count=1, flags=re.S)
    # the template's head preloads are its sample card's pictures — preload OUR cover instead
    html, n = re.subn(r'(?:<link rel="preload" as="image"[^>]*>)+',
                      '<link rel="preload" as="image" fetchpriority="high" href="assets/Images/chr_tappu.webp"><link rel="preload" as="image" href="assets/Images/sc_pond_v2.webp">', html, count=1)
    # this lesson's styles, after every engine style; its modules, before boot()
    i = html.index("</head>")
    html = html[:i] + '<style id="mtgStyles">\n' + css + "\n</style>\n" + html[i:]
    j = html.rindex("\nboot();")
    html = html[:j] + "\n/* ===== [MTG2A01] lesson modules (4_ENGINE/mtg_modules.js) ===== */\n" + mods + "\n" + html[j:]
    # file4 hard-codes where pages start moving on by themselves; read it from the card
    a = "const AUTO_ADVANCE_FROM = 5;"
    if a not in html:
        sys.exit("X  AUTO_ADVANCE_FROM not found")
    html = html.replace(a, "const AUTO_ADVANCE_FROM = (CARD.auto_advance_from != null ? CARD.auto_advance_from : 5);")
    # file4's runner game is not in this lesson: its background warm-up must not fetch files we do not ship
    a = "(function warmRunner(){"
    if a not in html:
        sys.exit("X  warmRunner not found")
    html = html.replace(a, a + " return;   /* [MTG2A01] no runner game in this lesson */", 1)
    # file4 pre-loads its train's whistle and chug; this lesson has no train
    for x, y in (('window.__coverSfx = ["sfx_whistle", "sfx_train_move", "sfx_pop"];', 'window.__coverSfx = ["sfx_pop"];'),
                 ('window.__lessonSfx = ["sfx_whistle", "sfx_train_move", "sfx_pop", "sfx_fb_correct", "sfx_fb_incorrect"];',
                  'window.__lessonSfx = ["sfx_pop", "sfx_fb_correct", "sfx_fb_incorrect"];'),
                 ('window.__coverSfx || ["sfx_whistle", "sfx_train_move", "sfx_pop"]', 'window.__coverSfx || ["sfx_pop"]')):
        if x not in html:
            sys.exit("X  sfx warm list not found: " + x[:40])
        html = html.replace(x, y)
    for ph in ("__MR_AUDIO_V_STAMP__", "__MR_ART_V_STAMP__", "__MR_ART_LIST__"):
        html = html.replace(ph, "")
    return html


def stamp(html):
    for ph, sub in (("__AUDIO_V_STAMP__", "Audio"), ("__IMG_V_STAMP__", "Images")):
        h = hashlib.sha1()
        d = os.path.join(OUT, "assets", sub)
        for f in sorted(os.listdir(d)):
            h.update(f.encode("utf-8")); h.update(open(os.path.join(d, f), "rb").read())
        html = html.replace(ph, h.hexdigest()[:12])
    return html


def main():
    tmpl = require_current_engine()
    card = build_card()
    os.makedirs(OUT, exist_ok=True)
    html = compile_html(tmpl, card)
    assets(html, card)                      # audio first: the celebration track is measured off it
    ea = celebration_anim(card)
    if ea:
        card["end_anim"] = ea
        html = compile_html(tmpl, card)
        html = inject_celebration(html)
    html = stamp(html)
    open(os.path.join(OUT, f"{CODE}.html"), "w", encoding="utf-8").write(html)
    with open(os.path.join(OUT, "card.json"), "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=1)
    for stale in ("app.js", "style.css"):    # the r2 split engine, superseded by the single-file template
        p = os.path.join(OUT, stale)
        if os.path.isfile(p):
            os.remove(p)

    # VO recording list (for a human re-record; Gemini TTS fills assets/Audio meanwhile)
    with open(os.path.join(HERE, "VO_RECORDING_LIST.md"), "w", encoding="utf-8") as f:
        f.write(f"# VO recording list — {CODE}\n\n{len(VO)} clips. File = `3_BUILD/assets/Audio/<id>.{AUDIO_EXT}`. "
                "The three `vo_pt_*` transition lines are file4's recordings and are not re-recorded here.\n\n| id | line |\n|---|---|\n")
        for k, v in VO.items():
            f.write(f"| `{k}` | {v} |\n")
    missing = [k for k in VO if not os.path.isfile(os.path.join(OUT, "assets", "Audio", f"{k}.{AUDIO_EXT}"))]
    print(f"  built {CODE}.html · {len(card['slides'])} slides · {len(VO)} VO ids ({len(missing)} not yet recorded)")


if __name__ == "__main__":
    main()
