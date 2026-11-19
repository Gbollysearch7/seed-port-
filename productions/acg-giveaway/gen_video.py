#!/usr/bin/env python3
"""ACG Markets giveaway clips: Seedance 2.5 reference-to-video via the Sume Video Router (480p 16:9, native audio, 30 s about $3.08).
Usage: gen_video.py [prompt-name, default acg-01-30]. Submits once, saves the job id, polls, downloads the mp4.
Re-running resumes the saved job instead of paying again."""
import json, os, sys, time, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"')

import requests

NAME = sys.argv[1] if len(sys.argv) > 1 else "acg-01-30"
# @image1, @image2 ... in this order; public Sume URLs saved by gen_assets.py
REF_ORDER = {
    "acg-01-30": ["talent-v3", "prop-tee-flatlay-v2", "loc-01-tube-carriage-v2", "loc-02-escalators", "loc-03-station-exit-v2"],
    "acg-01-15-s2": ["talent-v3", "prop-tee-flatlay-v2", "loc-01-tube-carriage-v2", "file:blocking/sc01-tube.png", "loc-02-escalators"],
    "acg-s1-train-15": ["talent-v3", "prop-tee-flatlay-v2", "loc-01-tube-carriage-v2", "file:blocking/sc01-tube.png"],
    "acg-s2-escalator-6": ["talent-v3", "loc-02-escalators", "file:blocking/sc02-escalator.png"],
    "acg-s3-exit-8": ["talent-v3", "prop-tee-flatlay-v2", "loc-03-station-exit-v2", "file:blocking/sc03-station-exit.png"],
    "acg-s4-lane-12": ["talent-v3", "prop-tee-flatlay-v2", "loc-04-london-lane", "file:blocking/sc04-lane.png"],
    "acg-s5-lobby-6": ["talent-v3", "loc-05-office-lobby", "file:blocking/sc05-lobby.png"],
    "acg-s6-office-20": ["talent-v3", "prop-tee-flatlay-v2", "loc-06-office-talking-head", "file:blocking/sc06-talking-head.png"],
}
DURATION = {"acg-01-30": 30, "acg-01-15-s2": 15, "acg-s1-train-15": 15, "acg-s2-escalator-6": 6, "acg-s3-exit-8": 8, "acg-s4-lane-12": 12, "acg-s5-lobby-6": 6, "acg-s6-office-20": 20}
MODEL = {"acg-01-15-s2": "seedance-2"}


def ref_url(n):
    if n.startswith("file:"):  # local image sent inline as a data URI
        import base64, io
        from PIL import Image
        im = Image.open(HERE / n[5:]).convert("RGB"); im.thumbnail((1600, 1600))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return json.loads((A / f"{n}.json").read_text())["url"]

OUT = HERE / "video" / NAME.upper(); OUT.mkdir(parents=True, exist_ok=True)
A = HERE / "assets"
H = {"Authorization": f"Bearer {os.environ['SUME_API_KEY']}", "Content-Type": "application/json"}
JOB = OUT / "job.json"

if JOB.exists():
    job = json.loads(JOB.read_text())
else:
    refs = [ref_url(n) for n in REF_ORDER[NAME]]
    for u in refs:
        if u.startswith("http"):
            requests.head(u, timeout=30, allow_redirects=True).raise_for_status()
    body = {"model": MODEL.get(NAME, "seedance-2.5"), "prompt": (HERE / "prompts" / f"{NAME}.txt").read_text(), "duration": DURATION[NAME],
            "resolution": "480p", "aspect_ratio": "16:9", "generate_audio": True, "reference_image_urls": refs}
    r = requests.post("https://api.sume.com/v1/video-router/generate", json=body, headers={**H, "Idempotency-Key": str(uuid.uuid4())}, timeout=120)
    if not r.ok:
        sys.exit(f"Submit failed {r.status_code}: {r.text[:800]}")
    job = r.json()["data"]
    JOB.write_text(json.dumps({**job, "request": {**body, "reference_image_urls": REF_ORDER[NAME]}}, indent=1))
print("job", job["request_id"], flush=True)

while True:
    s = requests.get(job["status_url"], headers=H, timeout=60).json()["data"]
    st = (s.get("job") or s).get("status")
    print(time.strftime("%H:%M:%S"), st, flush=True)
    if st in ("succeeded", "completed", "failed", "canceled", "cancelled"):
        break
    time.sleep(20)

res = requests.get(job["result_url"], headers=H, timeout=60).json()
(OUT / "result.json").write_text(json.dumps(res, indent=1))
url = next((v for v in json.dumps(res).split('"') if v.startswith("http") and ".mp4" in v), None)
if url:
    (OUT / f"{NAME.upper()}-480p.mp4").write_bytes(requests.get(url, timeout=600).content)
    print("DONE", OUT / f"{NAME.upper()}-480p.mp4")
else:
    print("no mp4 url:", json.dumps(res)[:800])
