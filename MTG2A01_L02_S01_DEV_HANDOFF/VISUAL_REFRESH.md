# Visual refresh

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
