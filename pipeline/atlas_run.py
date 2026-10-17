#!/usr/bin/env python3
"""Run one clip from a prompt-pack JSON on Atlas Cloud (Seedance reference-to-video).
Usage: atlas_run.py <pack.json> <clip id | mini_test> [out_dir]
Uploads the clip's reference images, submits, writes the job ID to out_dir/job.json straight away (so a run can be cancelled),
polls, downloads <id>-480p.mp4 and saves the result JSON with Atlas's billed price. Key: ATLAS_CLOUD_API_KEY in SEED PORTFOLIO/.env"""
import sys, json, time, requests
from pathlib import Path

BASE = "https://api.atlascloud.ai/api/v1"
ENV = Path(__file__).resolve().parents[1] / ".env"
KEY = next(l.split("=", 1)[1].strip() for l in ENV.read_text().splitlines() if l.startswith("ATLAS_CLOUD_API_KEY="))
H = {"Authorization": f"Bearer {KEY}"}

pack_path, clip_id = Path(sys.argv[1]).resolve(), sys.argv[2]
pack = json.loads(pack_path.read_text())
clip = pack["mini_test"] if clip_id == "mini_test" else next(c for c in pack["clips"] if c["id"] == clip_id)
root = Path(pack["production_root"])
name = clip["id"]
out = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else root / "video" / name
out.mkdir(parents=True, exist_ok=True)

payload = dict(clip["payload"])
urls = []
for rel in payload["reference_images"]:
    with open(root / rel, "rb") as f:
        r = requests.post(f"{BASE}/model/uploadMedia", headers=H, files={"file": f}, timeout=120)
    r.raise_for_status()
    d = r.json().get("data", r.json())
    urls.append(d.get("download_url") or d.get("url"))
    print("  uploaded", rel, flush=True)
payload["reference_images"] = urls
if not urls:  # text-to-video: no references
    payload.pop("reference_images")
(out / "payload.json").write_text(json.dumps(payload, indent=1))

def submit():
    r = requests.post(f"{BASE}/model/generateVideo", headers={**H, "Content-Type": "application/json"}, json=payload, timeout=120)
    if r.status_code >= 400:
        sys.exit(f"submit failed {r.status_code}: {r.text[:400]}")
    job = r.json().get("data", r.json())
    jobs = json.loads((out / "job.json").read_text()) if (out / "job.json").exists() else {"attempts": []}
    jobs.setdefault("attempts", []).append({"id": job.get("id"), "model": payload["model"], "submitted": time.time()})
    jobs["id"] = job.get("id")
    (out / "job.json").write_text(json.dumps(jobs, indent=1))
    print(f"  submitted {payload['model']} {payload['duration']}s {payload['resolution']} {payload['ratio']} id={job.get('id')}", flush=True)
    return job

# Freshly uploaded references can fail instantly with "still being prepared" (no tokens billed): wait and resubmit.
time.sleep(10)
job, t0, tries = submit(), time.time(), 0
while True:
    time.sleep(6)
    try:
        j = requests.get(f"{BASE}/model/prediction/{job['id']}", headers=H, timeout=60).json().get("data")
    except Exception as e:
        print("  poll retry", type(e).__name__, flush=True); continue
    if j["status"] == "completed":
        break
    if j["status"] == "failed":
        (out / "result.json").write_text(json.dumps(j, indent=1))
        if "still being prepared" in str(j.get("error")) and not j.get("total_tokens") and tries < 5:
            tries += 1
            print(f"  refs not ready, retry {tries}/5 in 20s (nothing billed)", flush=True)
            time.sleep(20); job, t0 = submit(), time.time(); continue
        sys.exit(f"  failed: {j.get('error')}")
    if int(time.time() - t0) % 30 < 6:
        print(f"  ... {int(time.time() - t0)}s {j['status']}", flush=True)

(out / "result.json").write_text(json.dumps(j, indent=1))
video = out / f"{name}-480p.mp4"
video.write_bytes(requests.get(j["outputs"][0], timeout=300).content)
print(f"DONE {video}  price={j.get('price')}  took {int(time.time() - t0)}s")
