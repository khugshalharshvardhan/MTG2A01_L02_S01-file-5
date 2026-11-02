#!/usr/bin/env bash
# Regenerates 3_BUILD/ from 1_SPEC/ + 4_ENGINE/. Needs Pillow and ffmpeg.
set -e
cd "$(dirname "$0")"
PYTHONUTF8=1 python 1_SPEC/build_skill_MTG2A01_L02_S01.py
