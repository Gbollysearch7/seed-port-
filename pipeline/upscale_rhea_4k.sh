#!/bin/zsh
# SEED PORTFOLIO - local Topaz Rhea 4K upscale (never API). Recipe from FILMS X UPSCALE-STRATEGY.md:
#   480p source -> Topaz Rhea 1 x4 -> Lanczos to UHD -> HEVC 60 Mbps, Rec.709, source fps kept, audio copied, +faststart
# Usage: upscale_rhea_4k.sh <input.mp4> [more inputs...]
# Output: <input dir>/upscaled/<name>-RHEA-4K.mp4 (+ <name>-progress.txt, <name>-topaz.log with auth lines redacted)
# Landscape -> 3840x2160, portrait -> 2160x3840. Upscale the locked 480p edit, never footage that was already enlarged.
set -e
set -o pipefail
(( $# )) || { echo "usage: ${0:t} <input.mp4> [more inputs...]"; exit 1; }
T='/Applications/Topaz Video.app/Contents'
export TVAI_MODEL_DIR="$T/Resources/models" TVAI_MODEL_DATA_DIR="$T/Resources/models"
FF="$T/MacOS/ffmpeg"; FP="$T/MacOS/ffprobe"
log(){ echo "[$(date +%H:%M:%S)] $*"; }
for IN in "$@"; do
  IN="${IN:A}"; NAME="${IN:t:r}"; OUT="${IN:h}/upscaled"; mkdir -p "$OUT"
  read W H <<< "$("$FP" -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$IN" | tr x ' ')"
  if (( H > W )); then TW=2160 TH=3840; else TW=3840 TH=2160; fi
  AMAP=(); "$FP" -v error -select_streams a:0 -show_entries stream=index -of csv=p=0 "$IN" | grep -q . && AMAP=(-map 0:a:0 -c:a copy)
  log "Rhea x4 -> ${TW}x${TH}  <- $IN (${W}x${H})"
  "$FF" -hide_banner -y -loglevel info -nostats -progress "$OUT/$NAME-progress.txt" \
    -i "$IN" -map 0:v:0 $AMAP \
    -vf "tvai_up=model=rhea-1:scale=4:download=0,scale=${TW}:${TH}:flags=lanczos,setsar=1" \
    -c:v hevc_videotoolbox -b:v 60M -tag:v hvc1 -pix_fmt yuv420p \
    -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
    -movflags +faststart "$OUT/$NAME-RHEA-4K.mp4" 2>&1 \
    | grep -viE --line-buffered 'topazauthmanager|auth_studio|refresh_studio|username_studio|access_token|refresh_token|authorization' > "$OUT/$NAME-topaz.log" || true
  [[ -s "$OUT/$NAME-RHEA-4K.mp4" ]] && grep -q 'progress=end' "$OUT/$NAME-progress.txt" || { log "FAILED $NAME - see $OUT/$NAME-topaz.log"; exit 1; }
  log "done -> $OUT/$NAME-RHEA-4K.mp4  ($("$FP" -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -of csv=p=0 "$OUT/$NAME-RHEA-4K.mp4"))"
done
log "ALL DONE"
