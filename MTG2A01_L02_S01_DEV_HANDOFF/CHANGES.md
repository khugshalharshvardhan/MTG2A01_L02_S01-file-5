# CHANGES: MTG2A01_L02_S01 «टप्पू मेंढक की कूद» (skip counting by 2s, 5s and 10s to 100)

**What this build is.** The SME draft (`_v1_factory_build/`) rebuilt to match the review deck
`1_SPEC/MTG2A01_L02_S01_FINALreview.pptx`, which replaces almost the whole lesson. It uses the
draft's engine (`2026.07.16i-r4-unified`, pinned in `4_ENGINE/`) plus four additive modules
for this lesson in `4_ENGINE/mtg_modules.js` / `mtg_styles.css`: `BRIDGE_TEACH`, `JUMP_PICK`,
`SEQ_FILL` and `SPACE_PODS`. Folder structure and layout follow the HI02H11_L02_S05 handoff.
The deck text is kept verbatim in `1_SPEC/_SME_RECOMMENDATIONS.txt`.

**Decisions confirmed with the user (2026-10-30):**
* deck flow only: the old pages are removed, including the 2s/5s chants, the 100-chart and the 30-40-50 pattern on deck slides 19–22;
* the deck's slide 18 «Alternate suggestion» (slider) is skipped;
* all VO is Gemini TTS, voice **Leda** (as in file4);
* new art is generated with Gemini and keyed in-house.

**Flow (12 screens):** landing → T1 2s bridge → T2 5s bridge (2 taps) → T3 10s bridge (camera, 2 taps)
→ G1–G3 «where will the frog land?» → G4–G7 fill the sequence → the «अंतरिक्ष की सैर» game → celebration.

Status: ✅ DONE · ⚑ FLAGGED (built, with a stated difference) · N/C (no change asked)

## Checklist, deck slide by deck slide

| # | deck | change asked | status | proof |
|---|---|---|---|---|
| 1 | 1 | lesson name «टप्पू मेंढक की कूद»; «जम्पी» → «टप्पू» everywhere | ✅ | `card.title.hi`, landing VO; no «जम्पी» left in the card |
| 2 | 3 | landing like the right-hand mock: big title, pond scene with the frog jumping over stones, «शुरू करें» | ✅ | `01_landing.png` (`sc_landing.webp`) |
| 3 | 4 | T1: pond, stones 0–10 equally spaced, टप्पू on 0, friend near 10, stones neutral, highlights and arcs revealed during the animation, watch-only | ✅ | `02_T1_BRIDGE_2s.png`; walk: «T1 आगे enabled at end» |
| 4 | 4 | step 1: highlight each character as named; friend waves; deck VO | ✅ | clips `vo_t1_1a/b/c` with `focus` / `wave` |
| 5 | 4 | step 2: glow 0, highlight 1 then 2, one jump 0→2 with a curved trail; deck VO («…दो की संख्या पर…», romanised «ki sankhya» written in Devanagari) | ✅ | `vo_t1_2a…c` + `vo_c_1`, `vo_c_2` drive the dot |
| 6 | 4 | step 3: pause after the question, highlight 3 then 4, jump 2→4, glow 4 | ✅ | `pause_after: 900`, `vo_c_3/4`, `jump [2,4]` |
| 7 | 4 | (missing in the deck) 4→6 | ⚑ | the deck jumps from step 3 to «6 से 8»; a 4→6 step was added on the same pattern: «टप्पू ने फिर दो कदम की छलाँग लगाई और छह पर पहुँच गया!» |
| 8 | 4 | step 4: 6→8, glow 8 | ✅ | `vo_t1_4` |
| 9 | 4 | step 5: 8→10, friend waves on landing | ✅ | `vo_t1_5`, `wave_end` |
| 10 | 4 | step 6: both frogs happy; 2, 4, 6, 8, 10 lit one at a time with the VO; all 5 trails visible | ✅ | `T1_end.png`: 5 arcs, 5 marks |
| 11 | 5 | T2 steps 1–5: 0–30, friend at 30, light dot through 1–5, jumps to 20 with equal arcs and glows; deck VO | ✅ | `03_T2_BRIDGE_5s.png` |
| 12 | 5 | T2 steps 6–9: hand cue on टप्पू, tap enabled after the VO, 20→25 and 25→30 on taps, tap disabled during the jump | ✅ | walk: «T2 tap 1/2 offered»; `T2_tapwait.png` |
| 13 | 5 | T2 steps 10–11: happy bounce; 5…30 highlighted, all six arcs; आगे after the VO | ✅ | `T2_end.png` (6 arcs) |
| 14 | 6 | T3 steps 1–4: 0–50, friend near 50; ten unit spaces lit before the 0→10 jump; jumps to 30 | ✅ | `span` + `jump` on `vo_t3_2b` |
| 15 | 6 | T3 steps 5–8: camera settles on 30–50 and holds; OST «टप्पू पर टैप कीजिए।» / «टप्पू पर फिर टैप कीजिए।»; 30→40, 40→50 on taps; no wrong-answer feedback | ✅ | `04_T3_BRIDGE_10s.png`, `T3_tapwait.png` |
| 16 | 6 | camera note: the pond scrolls as टप्पू moves (frame, heading, bar and nav fixed); zoom out to 0–50 for the recap | ✅ | `cam: "follow"` / `[29,53]` / `"all"`; `T3_end.png` |
| 17 | 7 | G1: frog at 50, options 51 · 55 · 60; 50 glows on «पचास पर है»; OST «सही संख्या पर टैप कीजिए।» | ✅ | `05_G1_JUMP_PICK.png` |
| 18 | 7 | G1 feedback: correct VO + frog 50→55; WA1 wiggle + VO; WA2 «पचास से पाँच कदम आगे देखिए।» + glow the 5 spaces; WA3 fade, pulse 55, hand | ✅ | walk: «G1 WA3 fades…/guides…», `G1_wa3.png`, `G1_correct.png` |
| 19 | 7 notes | G2 (2s): frog at 14, options 15 · 16 · 18, OST «सही! 16», WA2/WA3 lines | ✅ | walk G2 ✓ |
| 20 | 7 notes | G3 (10s): frog at 30, options 35 · 50 · 40, OST «सही! 40», WA2/WA3 lines | ✅ | walk G3 ✓ |
| 21 | 8 | G4: grasshopper hops 30→32→34→36 with VO1–VO4, then the question and the blank; options after the VO | ✅ | `08_G4_SEQ_FILL.png` |
| 22 | 8 | G4 correct: «शाबाश! छत्तीस से दो आगे—अड़तीस!», 38 in the box, sequence highlighted, आगे after feedback; WA1 wiggle + «दो-दो करके गिनिए…» | ✅ | `G4_done.png` |
| 23 | 8 | G4 WA2 «संकेत» popup: screen dimmed, options disabled, line 34–40, animal still at 36, arc 36→38 «+2», glow 38, auto-close (~5 s), then «अगली संख्या क्या होगी?…» | ✅ | `G4_hint.png`; walk: «hint popup opens / closes by itself» |
| 24 | 8 | G4 WA3: fade 40 and 37, glow 38 + hand, no tick before the tap | ⚑ | built. The deck line says «मेंढक…»; the animal on this screen is the grasshopper, so the VO says «टिड्डा दो कदम की छलाँग लगाकर अड़तीस पर पहुँचेगा।» |
| 25 | 9 | G5: 10…16,_,_ options 17–20; one box at a time; used option fades; animal on top jumps on each correct answer | ✅ | `09_G5_SEQ_FILL.png`, `G5_done.png` |
| 26 | 9 | G5 WA2 = number-line hint popup (the deck replaces the +2 arrow) per blank; then «सही संख्या पर टैप कीजिए।»; WA3 lines | ⚑ | built. WA3 says «खरगोश…» where the deck says «मेंढक…» (the animal is the rabbit) |
| 27 | 10 | G6: 55,60,65,_,_ options 66 · 70 · 75 · 80 (per the mock), hint popups 64–70 and 69–75 (+5) | ✅ | `10_G6_SEQ_FILL.png`, `G6_hint.png` |
| 28 | 10 | G6 conflicts | ⚑ | the VO names a **गिलहरी** while the hint text and mock show a rabbit, so a squirrel is used throughout. The second WA3 «…सत्तर पर पहुँचेगी» was changed to «…पचहत्तर पर…» because the answer is 75 |
| 29 | 11 | G7: 50,60,_,80,_,100 options 61 · 70 · 75 · 90; deck VO; WA2 = «साठ/अस्सी से दस आगे गिनिए।» then the +10 popup (grasshopper); WA3; the grasshopper jumps to the filled box; filled numbers disabled | ✅ | `11_G7_SEQ_FILL.png`, `G7_hint.png`, `G7_done.png` |
| 30 | 12–14 | game «अंतरिक्ष की सैर»: menu VO + 3 cards; prefilled pods; drag into pods (any order, checked per pod); round-1 ghost-hand guidance + 7 s inactivity repeat once; correct = number VO + snap + lock; wrong = pod wiggle + smoke, animal returns, VO only on the first wrong per round; round complete = numbers lit L→R, pods fly away, distractors exit, next round loads; after 3 rounds the menu shows a badge; «कमाल!…» after all three | ✅ | `12_GAME_menu.png`, `GAME_round.png`, `GAME_wrongdrop.png`, `GAME_menu_badge.png`; walk: all 9 rounds filled, «GAME all levels → celebration» |
| 31 | 15 | the 9 number sets and distractors exactly as in the table | ✅ | `ROUNDS` in the builder (asserts ≤ 100 and distractors ∉ sequence) |
| 32 | 16 | one cast per level (frog / rabbit / grasshopper); 1 distractor, then 2 in round 3; ground order shuffled; gentle bob, still while dragging; full screen, no instruction bar | ✅ | `CAST`, `shuffle`, `.sp-astro-in` bob paused on `.dragging` |
| 33 | 17 | celebration | N/C | unchanged |
| 34 | 18 | «Alternate suggestion» slider / «simple tap on the patthar» | N/C | skipped, per the user's decision |
| 35 | 19–22 | old pages 3, 5, 6, 17 | ✅ | removed, per the user's decision («deck flow only») |
| 36 | — | old pages not in the deck | ✅ | removed (old 20-page flow → 12 screens) |
| 37 | — | skill code | ⚑ | the draft's card said `MTG2A01_L03_S01`; aligned to the folder and deck: `MTG2A01_L02_S01` / LO `MTG2A01_L02` |

## Changed beyond the deck (each with its reason)

* **Layout follows file4** (as you instructed): stage background token `--bg:#F2F7FA` (the draft used the older warm `#FAF7F1`).
* **T1 heading «दो-दो की गिनती»**: the T2/T3 mocks have headings and the T1 mock shows an empty card, so T1 got one too, for consistency.
* **Question screens enable आगे after the correct feedback** (deck slide 8 says this for G4), instead of the engine's auto-advance.
* **Game**: the mock's home button is left out (the deck says the menu returns only after 3 rounds). The ghost-hand guidance runs on round 1 of **each** level. A small Swiftie sits in the corner and the audio button replays the current line.
* **Landing VO** reworded only for the rename: «…टप्पू मेंढक के साथ…».
* **Celebration audio**: `sfx_correct` was requested by the draft but never shipped (404). It is now copied from the kit (HI02H11_L02_S05), not synthesised.

## Verification

* **Behavioural walk** (`1_SPEC/_drive_mechanics.py`, audio stubbed): **74 pass · 0 FAIL**, 0 console errors.
  It covers every tap on टप्पू, every WA1/WA2/WA3 rung on G1–G7 (including popup open and close), all 9 game rounds
  (including a wrong drop) and the hand-off to the celebration. Proof is in `5_SCREENSHOTS/_drive/`.
* **Receipt** (`verify_bundle.py 3_BUILD --delivery`), verbatim: `17 pass · 5 FAIL · 4 warn`
  * FAIL engine `2026.07.16i` vs `2026.08.04b`: the draft arrived on 07.16i and no Maths factory canon exists on this machine (same situation as MTG1A04). Porting the engine is a separate job.
  * FAIL review PPT / page shots: these are produced in `2_BUILT_REVIEW_DECK/` and `5_SCREENSHOTS/` (file4 structure), not inside `3_BUILD/` where the receipt looks.
  * FAIL dist / dist freshness: there is no dist step for this structure. `3_BUILD` is **13 MB** (real MP3s, WebP sprites and pruned UI; it was 39 MB). The rest is kit Swiftie animations, which are left untouched. For comparison, file4's `3_BUILD` is 89 MB.
  * WARN «PICK dominates»: the checker does not recognise `SPACE_PODS` (a drag/produce game). WARN `vo_pt_mastery`: there is no gate before the celebration, by design. The two content-sync WARNs are expected because there is no canon engine.
* **Not verified by machine:** real-audio timing (headless Chrome does not decode the clips). Before release, a person should play the 3 teach screens with sound and confirm each jump lands on its spoken number.

## Assets

* **VO:** 154 clips, Gemini TTS, voice Leda; sources in `1_SPEC/vo_src_wav/`, shipped as MP3 (mono 48k).
* **EAR-CHECK** (generated through the fallback ladder; listen to these before release): `vo_c_3`, `vo_c_5`, `vo_c_30`,
  `vo_q4_ok`, `vo_q7_pre1`, `vo_g_n_61`, `vo_g_n_65`, `vo_g_n_67`, `vo_g_n_69`, `vo_g_n_70`, `vo_g_n_75`.
  These are placeholder-quality TTS, as file4's were. `1_SPEC/VO_RECORDING_LIST.md` lists all 154 lines for a human recording.
* **Art (Gemini, keyed by `1_SPEC/key_art.py`):** टप्पू, the friend frog, grasshopper, rabbit, squirrel, reeds, the pod, 3 astronauts,
  the space background and the landing scene. Raw renders are in `1_SPEC/game_art_src/`. The generator left its chroma background opaque,
  so the in-house keyer removes it and turns the magenta seen through the glass domes into light-blue glass. The pond, stones,
  number lines, arcs and smoke are drawn in CSS/SVG.

## Observations: noticed, NOT changed

* The celebration line «शाबाश! तुमने कूद-कूद कर गिनती सीख ली!» is in the *tum* register, while every deck line uses *aap* (कीजिए). It was kept as the deck left it.
* The guided-practice WA3 lines on deck slides 7–9 say «मेंढक» even where the screen animal is not a frog. Only the screens with a different animal were changed (rows 24, 26 and 28).
* Deck slide 9's WA2 text still lists the old «arrow +2» animation next to the instruction to use the number line. The number line was used.
* The phase-gate lines «चलिए, साथ में करें!» / «अब आपकी बारी!» come from the engine and were not reviewed in the deck.

---

# ROUND 3: file4's shell (user request, 2026-10-30)

> "take all swifty animations (transitions), buttons, their sfx, hand nudge and all from this file [HI02H11_L02_S05]
> … when the play button will appear, when any button will be inactive / active … extract all the things from this file and implement"

**How:** the lesson now runs on **file4's engine itself**, `4_ENGINE/lesson_template.html` (`2026.08.04b-r4-unified`, the
S05 copy with its shell, confetti and train set), instead of the draft's `2026.07.16i`. Our four modules are injected
into it at build time and the template is never edited, so every shell behaviour below is file4's own code, not a copy.
The old engine is kept in `4_ENGINE/_old_engine_2026.07.16i/`.

| # | from file4 | status | proof |
|---|---|---|---|
| R3-1 | **Transition Swifty:** the peek-up talking Swifty (`peeking_talk_up.webp`), blurred stage, soft `sfx_whoosh`, headline wiped in when Swifty says it (`CARD.gate.title_cue_ms`), 12 s watchdog, आगे off while it is up. Before T1, before G1 and before the game | ✅ | `SHELL_gate_tutorial/guided/practice.png`; walk: «transition opens / next slide mounts» ×3 |
| R3-2 | **Transition VO:** file4's recorded `vo_pt_*` clips (the same three lines as ours), so its measured cues (3370 / 3520 / 940 ms) apply unchanged | ✅ | `1_SPEC/kit_audio/` |
| R3-3 | **Cover play button:** file4's drawn ▶ (`play_btn.svg`), grey and disabled (`sg-waiting`, `play_btn_disabled.svg`) while the greeting speaks, `idle-pulse` only after 5 s idle, `sfx_play_button` on press; drifting stars + tap-burst (`startnew_bg_plain` + `bgdeco_*`) | ✅ | `SHELL_cover_idle.png`; walk: «play button becomes tappable», «idle pulse after ~5 s» |
| R3-4 | **Next button:** file4's arrow-only → pill (52 px arrow), `sfx_next_button` on press; while it pulses, every other animation stops (`nav-live`) | ✅ | `T1_end.png` |
| R3-5 | **When the buttons are on/off (file4's rule):** teach pages show → only after their VO/animation ends. From the first question on (`auto_advance_from: 3`, file4 hard-codes 5), the button is **hidden** (`auto-next`) and a solved page **moves on by itself** after the correct feedback, with file4's 5.2 s fail-safe that brings the button back | ✅ | walk: «T1–T3 आगे shown + enabled at end», «G1–G7 आगे hidden», «correct → moves on by itself» |
| R3-6 | **Hand nudge:** `nudge_hand_new.svg` with file4's `nudgeMove` bob, on Tappu's tap cue, on the WA3 answer and as the game's ghost-drag hand. The WA3 hand is an *earned* hand (`pointNudgeAt(el, true)`), which is file4's phase rule | ✅ | `G1_wa3.png`, `GAME_wrongdrop.png` |
| R3-7 | **Header Swifty:** file4's round head (`sw_head_*`) that changes expression (talking / celebrate / hint / try-again) | ✅ | every question screenshot |
| R3-8 | **Feedback sounds:** file4's recordings `sfx_fb_correct` / `sfx_fb_incorrect` on every right/wrong answer and drop (the synthesised tones are the fallback) | ✅ | `mtgRight()` / `mtgWrong()` in `mtg_modules.js` |
| R3-9 | **Correct-answer confetti:** file4's (FLN kit recipe 7, whole-window), replacing the side cannons | ✅ | `G1_correct.png` |
| R3-10 | **Lesson music:** `bgm_lesson.ogg` starts on the play-button tap, plays at 0.30, ducks under SFX/VO | ✅ | file4's BGM code, unchanged |
| R3-11 | **Celebration Swifty:** file4's celebration kit; she jumps on «शाबाश», then lip-syncs **our** line (track measured from `vo_well_done` by the kit's `make_lipsync.py`); `sfx_celebrate`; arrow-only end button | ✅ | `13_CELEBRATION.png`; build log «lip-sync from vo_well_done (3611 ms)» |

**Changed in our modules to fit file4's engine:** hand art and earned-hand flag, feedback sounds, the game's Swifty
(file4's round head) and replay button (file4's header audio-chip graphic). The full-screen game hides `#swBuddy` / `#navBtn`.

**Removed from file4 because this lesson has no train or runner:** at build time the runner warm-up is switched off,
and the train whistle and chug are dropped from the sound pre-load list. The train art is not shipped.

**Audio format:** now `.ogg` like file4 (its engine hard-codes `.ogg` for SFX and music). Our 151 VO clips are Opus 40k mono.

**Verification:** walk `1_SPEC/_drive_mechanics.py`: **84 pass · 0 FAIL**, 0 console errors (it now also covers the cover,
the three transitions and the button rule). Receipt, verbatim: `16 pass · 5 FAIL · 4 warn`. The stale-engine FAIL is
**gone**. The new «start_mascot.png / start_btn.png missing» is the checker's fixed list: neither file is referenced
by this page, and file4 does not ship them either. The other FAILs are as before (review deck and shots live in
`2_BUILT_REVIEW_DECK/` and `5_SCREENSHOTS/`; there is no dist step). Bundle 17.5 MB; the growth is file4's music (2.4 MB),
celebration sheets and transition art.

**⚑ One conflict for you to decide:** deck slide 8 says «Enable Next after the feedback finishes» on the question
pages. file4's rule (R3-5) moves a solved page on by itself, with no button. I followed your instruction to use file4's
button behaviour. To go back to the deck's version, set `auto_advance_from` to `99` in the builder and rebuild.

**EAR-CHECK (new):** the three `vo_pt_*` transition clips are file4's recordings. Confirm they say exactly
«ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!» / «बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!» / «वाह! अब आपकी बारी।»

---

# ROUND 3b: file4's title-page entrance (user request, 2026-10-30)

> "https://github.com/khugshalharshvardhan/HI02H11_L02_S05_DEV_HANDOFF-file4- — extract all the swift transitions, confetti,
> title page start animation, celebration screen animation, layout and other standard things"

The GitHub repo is the **same commit (556bd40)** as the local file4 ported in Round 3, with no local changes. So the
transitions, confetti, celebration Swifty, buttons, button sounds, hand nudge, music and button on/off rules were
already in. The one thing still missing was the **title-page entrance**. file4 draws it only for its train cover
(`landing_hero.kind = "matra_train"`), so it could not come across as-is.

| # | from file4's cover | here | status |
|---|---|---|---|
| R3b-1 | the cover card: translucent white with an inset white border, 536 px tall, title at the top (`.lt-cloud-card`) | `.fc-card`, same values | ✅ |
| R3b-2 | the train rolls in from the right and parks | टप्पू hops in from the right over the pond stones (3 hops, squash on landing), starting when the loading screen has gone, as the train does | ✅ |
| R3b-3 | its smoke leaves the chimney and gathers into a cloud (13 puffs round a soft body and a white core, file4's puff gradient) | each hop's splash sends puffs up into the same 13-puff cloud | ✅ |
| R3b-4 | the title is written on the cloud (soft-edged reveal, left to right) with `sfx_pop`; when it lands, pop + bell | same reveal, same sounds | ✅ |
| R3b-5 | the greeting waits for the title; the ▶ stays hidden/grey (`sg-waiting`) until the greeting ends; 9 s fail-safe | file4's own engine hook (`window.landingTrainReady` / `__ltReady`), so its gating is unchanged | ✅ |
| R3b-6 | no subtitle on the cover | subtitle line hidden | ✅ |

Code: `4_ENGINE/mtg_cover.js` + `mtg_cover.css` (injected with the lesson modules), card `landing_hero: {kind:"frog_cover"}`.
Proof: `5_SCREENSHOTS/01_landing.png` (the settled cover; measured pond bottom 371 px, ▶ top 391 px, no overlap). The walk is
**84 pass · 0 FAIL**, 0 console errors. One run crashed inside Chrome/Selenium; the rerun was clean.

**Not ported, and why:** file4's train itself, its whistle and its chug are train art and train sounds. The frog
gets a soft synthesised "hop" tone instead (no frog SFX recording exists in the kit).

---

# ROUND 4: the user's pond, frog and rock art (2026-11-02)

> "i've added image of pond and frog and rock in my assets-image folder i want the same layout of pond and frog apply this"
> (with a mock: pond across the screen, a row of rocks in the water, टप्पू on the left, the friend waving on the right)

| # | change | where | status |
|---|---|---|---|
| R4-1 | `pond.png` → `sc_pond` (1600×533 WebP). On the teaching screens it is drawn as a **9-slice**: the two banks keep their shape and only the water stretches, so one pond serves 0–10, 0–30 and the wide scrolling 0–50 world | `BRIDGE_TEACH` | ✅ |
| R4-2 | `frog and rock.png` split into `chr_tappu` (the darker frog), `chr_friend` (the yellow frog) and `prop_rock` | `1_SPEC/art_keyed/` | ✅ |
| R4-3 | every number is one of the user's rocks in the water, its number below on the water (navy with a white halo); the lit / marked / glow states are drawn on the rock itself | `BRIDGE_TEACH` | ✅ |
| R4-4 | टप्पू sits on rock 0 (deck: "directly on the stone marked 0") and hops rock to rock; the friend stands on the far bank | `BRIDGE_TEACH` | ✅ |
| R4-5 | the scene is sized from the frame's real width (it was a fixed 1113 px, which clipped the far bank and the friend in this engine) | `BRIDGE_TEACH` | ✅ |
| R4-6 | the user's टप्पू also on G1–G3 (it replaces the generated frog everywhere) and on the cover, whose pond is now the user's pond with five of the user's rocks | `JUMP_PICK`, `mtg_cover.js` | ✅ |

Sources: the user's two files moved from `3_BUILD/assets/Images/` to `1_SPEC/art_user_src/` (the build regenerates
`3_BUILD`, so assets live in `1_SPEC` and are copied in). The generated frogs they replace are kept in
`1_SPEC/art_keyed_r2_generated/`. Walk: **84 pass · 0 FAIL**, 0 console errors. Screens: `5_SCREENSHOTS/02–04`, `01_landing.png`.

## ROUND 5 — re-audit against the shared deck (Drive copy of MTG2A01_L02_S01_FINALreview.pptx, byte-identical to 1_SPEC's)
Every VO line, OST, option set, hint range and game number set was compared with the deck, slide by slide. One mismatch was found and fixed:
- **G4 WA1:** the deck says «दो-दो करके गिनिए। अगली सही संख्या पर टैप कीजिए।» is both VO **and** OST. The screen kept the shorter question OST. It now shows the full line (`wa1_ost`).

The known, deliberate deviations still stand: #7 (the 4→6 jump), #24 and #26 (टिड्डा/खरगोश in place of «मेंढक»), and #28 (the G6 squirrel; पचहत्तर). Deck slide 18's slider was skipped by the user, and slides 19–22 are old-draft pages that the deck flow removed. Walk: 84 pass · 0 FAIL.

- **R5-2:** the yellow caption box was removed from the three teaching screens (`.br-cap` loses its background, border and shadow), so the text stands on its own and no longer pushes into the → button. The question pages never used it.
- **R5-3:** the jump arrows are bolder and readable over grass and water: thicker red dots, a white halo under them, and a larger arrowhead that points along the curve with a white edge, as in the deck. This changes every arc, on the teaching screens, G1–G3 and the hint popups.
- **R5-4:** टप्पू's friend is mirrored to face टप्पू across the pond on all three teaching screens (`.br-friend` uses `scale:-1 1`; it is centred with `translate` so the flip does not move it). The friend appears nowhere else.
- **R5-5:** the 5s screen (0–30) now has the 10s screen's camera: it opens zoomed out, follows टप्पू as he jumps, settles on 19–31 for the two taps, and zooms out for the recap. Both camera screens use the 2s screen's spacing (80 px a step, up from 46), so the rocks are large. टप्पू is never wider than one step, so he sits on a single rock. For the 30–50 taps the view zooms out just far enough to fit the range; the whole scene scales together and the numbers grow back to stay readable. The zoomed views are centred vertically.
- **R5-6:** the "tap me" pulse on टप्पू used `mtgPulseBig` (`transform:scale`), which replaced his `translate(-50%)` centring, so while pulsing he slid half his width right onto the next rock. His pulse now keeps the centring (`brFrogPulse`, scale 1.06). Measured: 0 px off the rock centre during the pulse on both tap screens. The same bug moved glowing number-line labels on G1–G7 and the hint popups (`.nl-lbl.glow`), which now use `mtgPulseCx`.
- **R5-7:** in the space game, the animals waiting on the ground now float side to side (±14 px) with a light lift and lean, on a 3.6 s cycle, staggered so they do not move in step. They still hold still while being dragged (deck: "keep their positions stable during dragging"). Measured in the live game: about 22 px of side-to-side travel at the test window size.
- **R5-8 (replaces R5-7):** the waiting animals now travel right and left across the ground (±60 px, a 6 s cycle, with a light lift and lean). They all move in step, so the gaps between them never close. Checked at both extremes: they stay inside the scene and clear of Swifty. They still hold still while dragged. Walk: 84 pass · 0 FAIL.
- **R5-9:** the space game (page 11) now uses the user's art: «game frog» for 2s, «game rabbit» for 5s, and «game Squirrel» in place of the grasshopper for 10s. The art shows on the ground, in the pods and on the menu cards. Each number badge sits on the suit's chest star, at measured positions frog [0.51,0.62], rabbit [0.52,0.68] and squirrel [0.70,0.62]. Sources moved to `1_SPEC/art_user_src/`; cropped copies are in `1_SPEC/art_keyed/sp_*.png`; the old generated astronauts are kept in `1_SPEC/art_keyed_r2_generated/`. The grasshopper on G4/G7 is unchanged (game only).
- **R5-10:** animals riding in a rocket (the menu cards, seated pods and the take-off flight) are shown through a window cut to the glass dome (`.sp-dome`, measured on sp_pod: glass x 84..307, hull at y 136), so no head or ear pokes out of the rocket. Each helmet is centred in the dome from measured sprite points (`rider`: frog [0.48,0.02], rabbit [0.48,0.15], squirrel [0.57,0.08]) and sized to about 60% of the glass, so the face stays clear of the hull and the seat back.
