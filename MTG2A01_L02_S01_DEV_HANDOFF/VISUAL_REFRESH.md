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
