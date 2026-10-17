# FILMS X — 4K upscale strategy

This is how FILMS X turns 480p Seedance drafts into verified 3840 × 2160 deliveries. It's written from the scripts and logs of the jobs that produced the recent 4K finals: poolside v1 and v2 (24 Sep 2026), the MCBH full song, and both Suede finals (25 Sep 2026).

---

## 1. The rule

**All upscaling runs locally in Topaz Video on this Mac. Never through an API.**
- Atlas and Tencent upscalers (`pipeline/atlas_upscale.py`) were tried once and retired on 15 Sep 2026 at your request. You pay for Topaz, and it looks better.
- We don't pay for Seedance's `-sr` / `-esr` resolutions either. Render at 480p and let Topaz do the lift.

## 2. The recipe that works (current standard)

**One Topaz model pass, then one clean resize, then one high-bitrate encode.**

```
480p source (854×480)
   │  Topaz Rhea 1, scale ×4   ← all the AI enhancement happens here
   ▼
3416×1920
   │  Lanczos resize (plain maths, no AI)
   ▼
3840×2160 UHD  →  HEVC 60 Mbps, Rec.709, 24 fps, original audio copied
```

### Why each choice

| Choice | Why |
|---|---|
| **Rhea 1** (`rhea-1`) | Topaz's newest detail model. It rebuilds skin pores, eyes, braids and fabric weave without the waxy look. In the podcast-01 side-by-side tests (`ads/podcast-01/upscaled/compare-*.png`) it held faces better than Proteus 4 and Iris 2. It's installed locally (`rhea-v1-…-4x` model file), so it runs offline. |
| **×4 in one step** | Rhea is trained as a 4× model, and one pass avoids stacking the artefacts of two AI passes (the old 2× → 4K ladder). 854×480 × 4 = 3416×1920. |
| **Lanczos for the last 12%** | 3416 → 3840 is only a 1.12× stretch. Lanczos is a sharp, neutral resize that adds no invented detail and no AI artefacts. Asking Rhea to hit 3840×2160 directly failed in an early test ("Failed to configure output pad"). ×4 then Lanczos has worked every time since. |
| **Keep 24 fps** | Seedance renders at 24 fps. No frame interpolation, because Apollo and Chronos can warp hands and lips. The old ladder made a 60 fps version, but current deliveries don't. |
| **HEVC 60 Mbps, `hvc1` tag** | Visually lossless for 4K web and social delivery, it plays in QuickTime/Finder and on iPhone, and 30 s comes to about 215 MB. It uses Apple's hardware encoder (`hevc_videotoolbox`). |
| **Rec.709 tags** | Stops players and CapCut shifting the colour or gamma. |
| **Audio `-c:a copy`** | The mixed audio passes through untouched: no re-encoding and no drift. |
| **`+faststart`** | The file starts playing immediately when shared or uploaded. |

## 3. The exact command

This is run through Topaz's own bundled ffmpeg, which contains the `tvai_up` filter. The system doesn't need its own ffmpeg.

```zsh
T="/Applications/Topaz Video.app/Contents"
export TVAI_MODEL_DIR="$T/Resources/models" TVAI_MODEL_DATA_DIR="$T/Resources/models"

"$T/MacOS/ffmpeg" -hide_banner -y -loglevel info -nostats -progress progress.txt \
  -i INPUT-480p.mp4 \
  -map 0:v:0 -map 0:a:0 \
  -vf "tvai_up=model=rhea-1:scale=4:download=0,scale=3840:2160:flags=lanczos,setsar=1" \
  -c:v hevc_videotoolbox -b:v 60M -tag:v hvc1 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a copy -movflags +faststart \
  OUTPUT-TOPAZ-4K.mp4
```

- `TVAI_MODEL_DIR` / `TVAI_MODEL_DATA_DIR` point the filter at the models inside the app. Without them it can't find Rhea.
- `download=0` uses the installed model and never tries to download one mid-job.
- `setsar=1` keeps square pixels, so the 16:9 frame isn't stretched.
- `-progress progress.txt` writes live progress (frame count, speed, `progress=end`) that can be checked without watching the terminal.

Reference implementations: `clients/suede-ai-creators/edit-2026-09-25/upscale_local.py`, `music-videos/mcbh/edit-2026-09-25-v2/upscale_topaz.sh` and `music-videos/poolside-cigar/upscaled/run.sh`.

### Two ways to run it

| Mode | When | How |
|---|---|---|
| **With a ProRes master** (poolside) | Plenty of disk space, and you want a master to re-encode later | Pass 1: Rhea ×4 → ProRes 422 HQ `.mov` (10-bit, `prores_videotoolbox -profile:v 3 -pix_fmt yuv422p10le`). Pass 2: Lanczos → HEVC 60M. Keeps a lossless 3416×1920 master (≈1.9 GB for 30 s). |
| **Streamed** (MCBH, Suede) | Disk is tight or the video is long | The single command above: Rhea → Lanczos → HEVC in one pass, with no intermediate file. |

**Disk check before starting:** the drive is currently at 95% with about 21 GB free. A 30 s ProRes 4× master is about 1.9 GB, so a full song won't fit. Use streamed mode for anything long.

## 4. Where it sits in the workflow

1. **Render at 480p** in Seedance (cheap drafts, identity checks).
2. **Pick and edit at 480p:** cuts, grade and sound in CapCut or a local assembly. Upscale **after** the edit, so Topaz only processes frames that will be used.
3. **Always upscale from the original 480p frames.** Never upscale footage that has already been enlarged; that doubles the artefacts (MCBH v2 rule).
4. **Topaz last for the picture.** Subtitles, end cards and logos go on **after** Topaz, on the 4K finishing master, so text stays razor-sharp and isn't "enhanced" into mush. The Suede finals keep a caption-free `FINISHING-MASTER-4K.mp4` and a separate `FINAL-4K.mp4` with yellow subtitles.
5. **Verify** (section 5) before calling anything delivered.
6. Copy the final to `~/Downloads` when you want it to hand.

## 5. Verification: nothing is "done" until it passes

Using Topaz's bundled `ffprobe` and the local ffmpeg (from `imageio_ffmpeg`):

| Check | Pass condition |
|---|---|
| Frame size | exactly **3840 × 2160**, SAR 1:1 |
| Frame rate | **24/1**, same as the source |
| Frame count | identical to the source (e.g. 768 frames for 32 s, 4,093 for MCBH). Nothing dropped or duplicated (`dup_frames=0`, `drop_frames=0`) |
| Duration | matches the source to within a frame |
| Full decode | every frame decodes without error |
| Black frames | none introduced (the 480p edit's intentional black is noted separately) |
| Audio sync | correlation between source and output audio at zero offset **> 0.995** (Suede office v2: 0.99983; MCBH: 0.99981) |
| Audio level | sample peak < 1.0 (no clipping); loudness and true peak recorded (Suede v2: −17.6 LUFS, −1.9 dBTP) |
| Colour tags | `bt709` primaries, transfer and matrix. If missing, re-tag with a stream copy (`-c copy -bsf:v hevc_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`) with **no re-encode** (`finalize_topaz.py`) |
| Eyes on it | a key-frame contact sheet plus a native-resolution face crop, inspected for waxy skin, halos, flicker or text damage |

Results are written next to the file as `*-QA.json` / `COMPLETE.json`, so every delivery has a receipt.

## 6. Speed on this Mac (Topaz on Apple Silicon)

| Job | Length | Rhea time | Notes |
|---|---|---|---|
| Poolside v1 | 16 s | 5 min 41 s | + 14 s HEVC encode (ProRes mode) |
| Poolside v2 | 30 s | 11 min | + 18 s encode at 1.7× real time |
| Suede office v2 | 32 s | 11 min 14 s | streamed, about 1.1 fps, 0.047× real time |

Rule of thumb: **about 20–22 minutes of Topaz per minute of 480p footage.** Run it in the background and check `progress.txt`.

## 7. Log hygiene

Topaz writes your **login tokens** (`TopazAuthManager … auth_studio / refresh_studio`) into ffmpeg's log output. The current scripts filter those lines out before saving (`redact_topaz_log.py`, and the filter inside `upscale_local.py`). **One older log still contains them: `ads/podcast-01/upscaled/topaz-ladder.log`.** Delete or redact it before that folder is shared. The same log shows the Topaz licence re-login date as **5 Oct 2026**. Renew before then or the filter will stop working.

## 8. History: what we tried and why we moved on

| Stage | Method | Outcome |
|---|---|---|
| 1 | Atlas/Tencent API upscaler ladder, 1080p → 2K → 4K (`atlas_upscale.py`) | Cost per clip and softer faces. **Retired 15 Sep 2026: never use an API.** |
| 2 | Topaz ladder (`topaz_upscale.sh`): Proteus 4 ×2 → Proteus 4 to 3840×2160 → optional Apollo 8 at 60 fps | Worked, but two AI passes compound artefacts, and 60 fps interpolation risks warped hands and lips. Kept for reference. |
| 3 | Side-by-side tests on podcast-01: Proteus vs Rhea vs Iris 2, 1-second clips with face crops | Rhea won on skin and eyes. |
| 4 | **Rhea 1 ×4 → Lanczos → HEVC 60M, 24 fps, Rec.709, audio copied, full QA** | **Current standard.** Used for poolside v1/v2, MCBH and both Suede finals, all verified at 3840×2160. |

## 9. Quick checklist

- [ ] Edit is locked at 480p; the source is the original 480p render or the 480p edit export
- [ ] Enough free disk space, otherwise use streamed mode
- [ ] Topaz licence valid (re-login due 5 Oct 2026)
- [ ] Run Rhea ×4 → Lanczos 3840×2160 → HEVC 60M, Rec.709, `-c:a copy`, `+faststart`
- [ ] Redact auth lines from the log
- [ ] QA: 3840×2160 · 24 fps · same frame count · full decode · no new black frames · audio correlation > 0.995 · bt709 tags
- [ ] Contact sheet and face crop checked by eye
- [ ] Subtitles and cards added after Topaz on the 4K master
- [ ] Final copied to `~/Downloads` if wanted
