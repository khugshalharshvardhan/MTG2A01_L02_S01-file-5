# Visual refresh

## Spaceport Adventure

The practice game now uses a quiet starfield and curved spaceport deck filling the entire browser, including margins outside the 16:9 play area. New transparent frog, rabbit and squirrel astronauts match the friendly lesson cast. Number badges remain prominent on waiting passengers and occupied pods, including 100. The three counting-game cards have distinct pastel colours. All three docks are built in advance along one persistent 3999px world. The heading stays fixed outside that world. After a set is filled, rockets launch left to right at roughly 440ms intervals. A 3.8-second camera track starts with the first launch, revealing the already-existing next dock and its passengers. No scene is replaced or recreated between sets. Distant scenery and nearby deck rails move at different speeds. Input stays locked until the camera stops and the next dock's narration finishes. There is no round counter, speaker button or Swifty portrait in the game.

Correct docking adds a gentle squash and number glow; wrong drops add a small puff below the number. Each rocket ignites individually before lifting off. Animal selection triggers a short frog croak or playful synthesized rabbit/squirrel chirp, with a cooldown preventing double sounds on taps. Ready chimes, engine ignition, flyby and camera-travel sweeps join the dock, puff and launch effects. These are quiet event cues rather than long loops competing with number narration. Six additional effects are generated locally with `prepare_spaceport.py --audio-only`.

The PPT's nine number sets, two prefills per set, locked first pod, shuffled correct passengers/distractors, same animal within each counting game, any-order placement, number-only correct VO, first-wrong-only VO, initial demonstration with one inactivity repeat, ground exit for distractors and completed-menu badges are preserved. As requested, the visible round structure is replaced by continuous parallax travel. The menu returns once a counting game's three authored sets are complete. The permanent instruction bar is visually removed while its live status remains available to assistive technology. Reduced motion replaces moving guidance with a static highlight and skips camera travel. Narration remains serialized. The full-window backdrop is removed on leaving the game.

The source `1_SPEC/MTG2A01_L02_S01_FINALreview.pptx` was re-read directly for this update (slides 13–16). Slide 14's wrong-drop rule explicitly says first incorrect drop gets VO, subsequent incorrect drops get the same visual feedback without repeating VO, and both distractors and misplaced correct animals receive it. It does not prescribe a three-attempt lock or third-error hint. Following the user's instruction to prefer the PPT if it differs, game passengers remain available after the third wrong drop. First-drag and one 7-second inactivity hand demonstrations follow slide 13. G1–G7's separate third-attempt option lock is retained. Sequential launches override slide 14's original simultaneous launch at the user's explicit request.

Assets and exact image prompts: `1_SPEC/visual_refresh/spaceport_provenance.json`; retained masters: `1_SPEC/visual_refresh/spaceport/`; reproducible exports and synthesized audio: `1_SPEC/prepare_spaceport.py`. The background and pod are native SVG assets. Run the standard builder to refresh `3_BUILD`.

Validation: `1_SPEC/_verify_spaceport.py` passed 119/119 checks across all nine sets with mouse, keyboard and touch input, reverse-order docking, three incorrect drops, narration IDs, idle guidance, individual left-to-right launches, persistent world and title identity, six camera tracks overlapping launches with distinct parallax depths and locked input, menu completion, celebration, full-window backgrounds, reduced-motion progression, effect triggers and scene cleanup. No browser errors. Screenshots and receipts: `5_SCREENSHOTS/spaceport/`, including individual-launch screenshots and `results.json`. `1_SPEC/_verify_spaceport_media.py` previously decoded all nine shipped spaceport sound effects in Chrome without audio stubs; interaction tests shorten VO to keep the run practical. `1_SPEC/_verify_spaceport_background.py` checks seamless stage edges at normal, wide and tall viewport sizes. JavaScript syntax and `git diff --check` passed.

## Explicit third-attempt option lock

G1–G7 now store the terminal answer in the option tray, independently of visual classes. The third wrong tap immediately disables and fades all incorrect options. The correct option becomes selectable once the feedback VO ends. Replay cannot release the terminal lock; a correctly filled blank clears it for the next blank while keeping used options disabled. Disabled buttons also reject direct handler calls and expose `aria-disabled`. The faded style overrides the entrance animation's retained opacity.

Verification: `1_SPEC/_verify_third_attempt.py` passed all 64 checks across every question and blank, including attempts one/two, immediate third-error disabling, visible fading, correct-only selection, replay, handler guards and next-blank reset. No browser errors. Receipt: `5_SCREENSHOTS/third_attempt/results.json`.

## Cover, continuous expansion and cute cast — v5

The cover title is now one line with no subtitle. The reference round Play button is hidden while the landing VO runs and becomes visible only when the existing audio gate releases it. Tappu performs a small anticipation/hop/landing cycle with a timed splash, while the gold companion gives a separate gentle reaction. Reduced motion shows a still scene.

The long-number scenes now interpolate unit spacing, leaf and label positions, jump-arc geometry, minor-label opacity and camera position on one requestAnimationFrame timeline. Expansion takes 950ms; recap contraction follows the camera cue duration. Arc nodes are retained rather than destroyed and rebuilt. The frog's feet share the camera anchor, so its on-screen size and baseline remain stable. Leaving the slide cancels the pending transition through the normal mount token.

Three distinct gold, teal and peach frog companions replace mirrored copies of Tappu. T1/T2/T3 have separate friends; G2/G3 use the gold and teal frogs, mirrored to face the jump direction. New round, friendly rabbit, squirrel and grasshopper sprites are shared by the sequence scenes and their hints. The space-game cast and mechanics remain unchanged.

New artwork was made with the built-in image-generation tool. Exact prompts and original generated paths: `1_SPEC/visual_refresh/cast_v5_provenance.json`. Selected masters: `1_SPEC/visual_refresh/cast_v5/`. Exported project assets: `1_SPEC/art_keyed/lesson_friend_*.webp` and `lesson_*_cute.webp`, prepared with `1_SPEC/prepare_cast_v5.py` and copied by the standard builder.

Current checks: `python -X utf8 1_SPEC/_verify_cast_motion_v5.py` and `python -X utf8 1_SPEC/_drive_mechanics.py 5_SCREENSHOTS/cast_motion_v5_regression`. The first check simulates a three-second landing VO and verifies that Play stays hidden until its actual end event; it also samples intermediate layout frames, stable arcs, clipping, sprite loading, mirroring and reduced motion at two viewport sizes. Evidence: `5_SCREENSHOTS/cast_motion_v5/`.

Final verification: 44/44 focused checks and 84/84 full lesson regression checks passed. No browser console errors. Expansion was sampled over approximately 950ms and recap contraction over approximately 700ms at both viewport sizes. The space-game implementation and its nine-round configuration remain unchanged.

## File9 cover and SME read-along follow-up

The current cover uses File9's 1040 × 574 art-card frame, 8px white border, 40px radius and shadow. Its original round gold and grey play SVGs are copied without modification, rendered at 140 × 140 with the same 30px bottom inset. The lesson's existing disabled/start/audio gates are retained, with File9-style ready pop and idle pulse.

Pond artwork fills the entire cover. A white sky veil supports the dark navy/green, two-line Devanagari display title. The locally bundled Yatra One font and SIL OFL license are in `1_SPEC/fonts/` and copied to `3_BUILD/assets/Fonts/`; source: https://github.com/google/fonts/tree/main/ofl/yatraone. Title entry, sequential jump trails, grounded frog breathing, water rings and small water glints animate the cover. Reduced-motion mode shows a still composition with the title visible.

The added “ध्वनि चालू” effects controls are removed from every screen. Narration replay and the previously added quiet foley remain available as before.

T1–T3 now display every original authored narration clip as it is spoken. Complete explanations are preserved; counting clips build a separate read-along word strip. The caption panel replaces the short equations introduced in v4. The pond is 320 design pixels high, preserving space for the longest explanation, counting strip and Next button without overlaps. No narration files or space-game mechanics were changed.

Current QA: `python -X utf8 1_SPEC/_verify_cover_sme.py`, followed by `python -X utf8 1_SPEC/_drive_mechanics.py 5_SCREENSHOTS/cover_sme_regression` with `MTG_TEST_URL` set to the local preview. Evidence is saved in `5_SCREENSHOTS/cover_sme/` and `cover_sme_regression/`. The older v4 verifier's expected cover frame, caption and removed-control checks have been brought up to date.

Final results: 64/64 cover/SME checks and 84/84 full-lesson regression checks passed, with no browser console or missing-resource errors. All authored audio-text metadata remains unchanged. File9's two play-button SVGs match their source hashes. The local preview server uses a larger request queue to handle simultaneous browser asset loads.

## Lesson v4 — pond layout, lesson animals and File9 options (2026-11-12)

The cover and T1–T3 use `sc_pond_v4.webp`, an open-water background without edge foliage or flowers. The picture meets the container's inner top and side edges; the heading sits over the sky. A separate footer holds one short prompt or counting equation and the navigation. Full spoken explanations are retained. Enlarged resting pads support the frogs at a shared feet baseline.

All teaching number labels use a fixed 46 × 40 design-pixel box; only the font size changes between landing numbers and skipped numbers. T2/T3 use a close view for each jump and a milestone overview for the recap, keeping the frog at a readable size. Unit labels and pads are hidden only in the milestone overview; the close view preserves the unit spacing used to demonstrate each jump.

G1–G3 centre the number line and option tray vertically. G1–G7 use new natural frog, rabbit, squirrel and grasshopper sprites; main scenes and hint popups use the same animals. The space game's astronaut sprites, level data and `SPACE_PODS` implementation are unchanged.

Options follow File9's `jl-opt` design: white face, grey ledge, spring entrance, lateral wrong-answer shake, green correct feedback, and a three-pulse green hint. Third-attempt guidance disables and fades all incorrect choices, leaving the answer for the child to select. Used sequence options disappear and the remaining choices are restored for the next blank. The exact File9 correct, wrong and tap sound files are retained in `1_SPEC/interaction_audio/`.

Original synthesised hop, croak and water-landing sounds play independently of narration. A sound-effects toggle is available on the cover and lesson screens. Leaving an activity stops its foley; reduced motion still provides the audio cue without playing the flight or splash animation.

Artwork was made with the built-in image-generation tool. Prompts and original generated paths are in `1_SPEC/visual_refresh/lesson_v4_provenance.json`; copied masters are retained in `1_SPEC/visual_refresh/lesson_v4/`. Project assets are in `1_SPEC/art_keyed/lesson_*.webp` and `sc_pond_v4.webp`. `prepare_lesson_v4.py` performs alpha-bound trimming, export and deterministic sound preparation. Normal builds use the retained project assets and need no image API or File9 checkout.

Rebuild and review from the handoff directory:

```powershell
python -X utf8 1_SPEC/build_skill_MTG2A01_L02_S01.py
python -X utf8 1_SPEC/_serve_preview.py 8942
# In another terminal:
$env:MTG_TEST_URL='http://127.0.0.1:8942/MTG2A01_L02_S01.html'
python -X utf8 1_SPEC/_verify_lesson_v4.py
python -X utf8 1_SPEC/_verify_lesson_v4.py --real-audio
python -X utf8 1_SPEC/_drive_mechanics.py 5_SCREENSHOTS/lesson_v4_regression
```

The lesson v4 checks cover both 1333 × 750 and 960 × 540 layouts, equal number boxes, grounded cover frogs, frame-by-frame hop bounds, readable long-sequence characters, keyboard frog taps, every guided blank's third-attempt lock, File9 feedback requests, sound muting and reduced motion. Interaction tests simulate narration; the separate audio check decodes all seven new effects in Chrome. Screenshots and receipts live in `5_SCREENSHOTS/lesson_v4/` and `lesson_v4_regression/`.

Final verification: 115/115 lesson layout and interaction checks, 14/14 sound-control placement checks (`--controls`), 84/84 full-lesson regression checks, and all seven sound effects decoded successfully. No browser console errors. Source/generated JavaScript syntax and `git diff --check` passed.

The lesson now uses a generated opaque pond backdrop, independent of the counting camera, and original vector space scenery. Original assets are retained.

## Source files

- `4_ENGINE/mtg_modules.js`: viewport scenery and shared drag/tap/keyboard grading.
- `4_ENGINE/mtg_styles.css`: background, labels, selection/focus states and reduced motion.
- `4_ENGINE/mtg_cover.css` / `mtg_cover.js`: lighter title treatment and new pond.
- `1_SPEC/build_skill_MTG2A01_L02_S01.py`: SVG copying, up to 1024px sprite exports, pond preload.
- `1_SPEC/visual_refresh/`: original generated master and complete generation prompt.

## Artwork

The pond was generated with the built-in image_gen tool. The exact prompt and source are recorded in `1_SPEC/visual_refresh/provenance.json`. It is 2172 x 724 pixels, exported as quality-94 WebP without enlargement. The space background is SVG geometry and gradients and scales without raster pixelation. Raster characters and the pond still have finite resolution at extreme zoom.

## Verification

Serve `3_BUILD` on port 8931 and run:

```powershell
python -X utf8 1_SPEC/_verify_visual_refresh.py
python -X utf8 1_SPEC/_drive_mechanics.py 5_SCREENSHOTS/visual_refresh_regression
```

The added checks exercise mouse, touch and keyboard selection, matching and wrong placement, fixed pond height during recap, Full HD at 2x density, a smaller landscape viewport, and reduced motion. Audio is stubbed, so real-audio timing still needs listening. New screenshots are saved separately in `5_SCREENSHOTS/visual_refresh` and `visual_refresh_regression`.

## Completed checks

- 84 / 84 lesson regression checks passed.
- 31 / 31 visual and input checks passed.
- No browser console errors on the isolated preview server.
- All three inline JavaScript blocks passed Node syntax checks; git diff --check passed.

Final preview: http://127.0.0.1:8934/MTG2A01_L02_S01.html (while the local server is running).

The final checks used MTG_TEST_URL pointing to port 8934 to avoid other local servers and concurrent request limits. They use simulated audio playback, not a real-audio timing review.

## Pond adventure follow-up

Implemented the selected Pond adventure cover with two frogs on separate lotus leaves and a labelled Start button. Added a reusable vector lotus leaf (1_SPEC/art_keyed/prop_lotus.svg), replaced numbered stone rests with leaves, and reserved 110 design pixels between the final landing and the friend.

Jump height is bounded by the available headroom. The camera frames the complete next jump before take-off and interpolates position, scale and label sizing on one animation clock around the feet baseline. Landing numbers use 30px type and skipped numbers 22px at the displayed scale.

Final results: 84 lesson regression checks and 31 visual/input checks passed. The added checks sample every animation frame for clipping and baseline drift across the 2s, 5s and 10s scenes, check frog separation and lotus support, and verify a readable Start label. Audio remains simulated for these automated checks.

## Sequence character update (pages 7-10)

G4 and G7 use the new transparent astronaut grasshopper (assets/Images/sp_grasshopper_v2.webp). G5 reuses the game rabbit (sp_rabbit.webp), and G6 reuses the game squirrel (sp_squirrel.webp). Main activity and hint art share the same character mapping.

Only the grasshopper was generated, using the built-in image_gen tool and the existing game cast as style references. Master: 1_SPEC/visual_refresh/grasshopper_astronaut_v2.png. Exact prompt: 1_SPEC/visual_refresh/grasshopper_provenance.json. The trimmed alpha source is 1_SPEC/art_keyed/sp_grasshopper_v2.png and is exported by the normal builder.

All 24 targeted checks passed, covering character loading, clearance above number boxes, all seven hints, completion of all four sequences, and no browser console errors. Evidence: 5_SCREENSHOTS/sequence_cast_refresh/results.json. Audio was simulated.

### Grasshopper leg correction

The current grasshopper is sp_grasshopper_v3.webp: one green hind leg on the left and one on the right. The suit, face, helmet and central boots are preserved. Both grasshopper activities and all their hints use this revision. Master: 1_SPEC/visual_refresh/grasshopper_astronaut_v3.png; exact image-edit prompt: 1_SPEC/visual_refresh/grasshopper_legs_provenance.json. All 24 character and hint checks passed again, with no browser errors.

## Sequence and number-line jump bounds fix

The sequence sprites previously started at the top edge of their frame and jumped upward by 70px. The sequence layout now reserves 64px of headroom, keeps 12px above the number strip, and uses a 44px hop. The shared hop helper also limits height to the actual available headroom. Frog number-line jumps use the same safe height for both the sprite and its drawn arc. Characters remain fully visible instead of being hidden by clipping.

All 29 frame-by-frame bounds/header checks passed across G1-G7 at 1333x750 and 960x540. All 24 sequence character, answer and hint checks also passed; no browser errors. Sources: 4_ENGINE/mtg_modules.js and mtg_styles.css. Test: 1_SPEC/_verify_jump_bounds.py; evidence: 5_SCREENSHOTS/jump_bounds_fix/results.json. Audio playback was simulated.

## Tappu jump animation

Frog hops now use a short crouch, a feet-anchored stretch and gentle tilt during flight, and a soft landing squash. A ground shadow stays under the frog; pond take-off and landing trigger short-lived water ripples and tiny droplets, while the supporting lily pad dips and settles. Number-line frog hops share the body motion; other characters retain their existing hop.

The hop keeps its original total duration and destination. Headroom accounts for sprite deformation. Transient effects are noninteractive and removed after playback; leaving a slide also cancels an unfinished hop. Reduced-motion mode moves directly to the destination and suppresses the added effects. No new sounds interrupt the narration.

Verification: 37 visual/input checks and 29 jump-boundary checks passed, including every sampled frog frame, all three motion phases, cleanup, reduced motion, two viewport sizes and no browser errors. Audio was simulated. A mid-flight review screenshot is saved locally as 5_SCREENSHOTS/visual_refresh/tappu_in_flight.png.
