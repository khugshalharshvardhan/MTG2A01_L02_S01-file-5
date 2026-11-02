# MTG2A01_L02_S01: «टप्पू मेंढक की कूद» (skip counting by 2s, 5s and 10s to 100)

The SME's first draft rebuilt to match the review deck in `1_SPEC/`.
**Read `CHANGES.md` first.** It lists every deck ask with its status.

## Run

```bash
cd 3_BUILD && python -m http.server 8931
# open http://127.0.0.1:8931/MTG2A01_L02_S01.html  (over http, not as a file)
# Shell (Swifty transitions, play/next buttons + sounds, hand nudge, music, celebration) is file4's engine — see CHANGES.md «ROUND 3».
# QA jump: ?slide=N  (0 = T1 … 10 = game, 11 = celebration)
```

## Rebuild

```bash
./_rebuild.sh        # = PYTHONUTF8=1 python 1_SPEC/build_skill_MTG2A01_L02_S01.py
```

All content lives in `1_SPEC/build_skill_MTG2A01_L02_S01.py`: the VO lines, the 12 screens, the game's
number sets and the timeline actions. The builder regenerates everything in `3_BUILD/`:
the card and a single HTML (file4's engine `4_ENGINE/lesson_template.html` + this lesson's modules), Opus .ogg from the WAV sources, file4's kit audio (`1_SPEC/kit_audio/`), the celebration kit,
WebP sprites, and only the UI files the engine references. **Never hand-edit `3_BUILD/`.**
Needs Python with Pillow, and `ffmpeg` (with libopus) on PATH.

## Voice-over

```bash
export GEMINI_KEY=...                       # environment only; never commit it
python <swiftpal-game-revise>/scripts/build/gen_tts.py 3_BUILD/card.json --voice Leda --ext ogg
# then move the new 3_BUILD/assets/Audio/<id>.ogg (WAV content) to 1_SPEC/vo_src_wav/<id>.wav and rebuild
```

For a human re-record, `1_SPEC/VO_RECORDING_LIST.md` has every id and line. Drop each WAV into `1_SPEC/vo_src_wav/` and rebuild.

## Folders

| | |
|---|---|
| `1_SPEC/` | SME deck + verbatim notes, the builder, art/VO sources, keyer, QA drivers |
| `2_BUILT_REVIEW_DECK/` | review deck of this build (one slide per screen) |
| `3_BUILD/` | the lesson (HTML + card.json + assets): the deliverable |
| `4_ENGINE/` | **file4's engine** `lesson_template.html` (`2026.08.04b-r4-unified`) + `mtg_modules.js` / `mtg_styles.css` + file4's `ui_kit/` and `kit_images/`; old engine in `_old_engine_2026.07.16i/` |
| `celebration_kit/` | file4's lip-synced celebration Swifty |
| `5_SCREENSHOTS/` | every screen in play order; `_drive/` = behavioural-walk states |
| `_v1_factory_build/` | the SME's original draft, kept for reference |

## Modules added for this lesson (`4_ENGINE/mtg_modules.js`)

* `BRIDGE_TEACH`: टप्पू crosses the stone bridge. Steps are clip lists, and each clip fires actions as it starts:
  `focus`, `wave`, `glow`, `dot`, `jump`, `span`, `mark`, `happy`, `cam`, `tapcue`, `pause_after`, plus `wait_tap` on a step.
* `JUMP_PICK`: the frog on a number line and three options, with the WA1/WA2/WA3 ladder.
* `SEQ_FILL`: fill the blanks one at a time, with the «संकेत» number-line hint popup on WA2.
* `SPACE_PODS`: the full-screen «अंतरिक्ष की सैर» drag game (menu → 3 levels × 3 rounds).

## QA

```bash
PYTHONUTF8=1 python 1_SPEC/_drive_mechanics.py 5_SCREENSHOTS/_drive   # 84 checks (incl. cover, transitions, button rule), audio stubbed
PYTHONUTF8=1 python 1_SPEC/_capture_settled.py 5_SCREENSHOTS          # play-order screenshots
```
Both expect the build served on port 8931.
