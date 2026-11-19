#!/usr/bin/env python3
"""ACG giveaway audio for the CapCut edit, via ElevenLabs.
- Speech-to-speech: re-voice each dialogue shot (banker -> George; the tube clip also -> Alice for the announcer),
  background noise removed so the clean voice sits over the original ambience.
- Music: 68 s instrumental theme.
- SFX: phone-graphic pop and end-card hit.
Re-running skips files that already exist."""
import os, sys
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
for line in (HERE.parents[2] / ".env").read_text().splitlines():
    if line.startswith("ELEVENLABS_API_KEY="):
        KEY = line.split("=", 1)[1].strip().strip('"')
H = {"xi-api-key": KEY}
ORIG, STS, MUSIC = HERE / "original", HERE / "sts", HERE / "music"
for d in (STS, MUSIC): d.mkdir(exist_ok=True)

GEORGE, ALICE = "JBFqnCBsd6RMkjVDRZzb", "Xb7hH8MSUJpSbSDYk0k2"
JOBS = [  # (source clip, voice id, output name)
    ("ACG-S1-TRAIN-15", GEORGE, "S1-train-banker-george"),
    ("ACG-S1-TRAIN-15", ALICE, "S1-train-announcer-alice"),
    ("ACG-S3-EXIT-8", GEORGE, "S3-exit-banker-george"),
    ("ACG-S4-LANE-12", GEORGE, "S4-lane-banker-george"),
    ("ACG-S6-OFFICE-20", GEORGE, "S6-office-banker-george"),
]


def save(path, r):
    if not r.ok:
        sys.exit(f"{path.name}: {r.status_code} {r.text[:600]}")
    path.write_bytes(r.content)
    print("OK  ", path.relative_to(HERE), flush=True)


def sts(src, voice, name):
    out = STS / f"{name}.mp3"
    if out.exists():
        return print("skip", out.name)
    with open(ORIG / f"{src}.m4a", "rb") as f:
        r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{voice}?output_format=mp3_44100_128", headers=H,
                          files={"audio": (f"{src}.m4a", f, "audio/mp4")},
                          data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true",
                                "voice_settings": '{"stability": 0.5, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": true}'},
                          timeout=300)
    save(out, r)


THEME = ("Premium, modern fintech brand film score for a 68-second London giveaway announcement. Instrumental only, no vocals. "
         "Opens light and curious with soft muted piano plucks and a gentle ticking pulse, like a city morning commute. "
         "From about 15 seconds a warm sub bass and crisp, minimal electronic drums build an upbeat, confident groove at 110 BPM, "
         "with airy synth pads and subtle shimmering arpeggios suggesting markets and momentum. "
         "Around 45 seconds it opens up into an optimistic, uplifting lift, then settles to a clean, satisfying resolve at the end "
         "suited to a logo end card. Polished, understated and expensive, leaving plenty of space for a speaking voice on top.")

SFX = [
    ("sfx-graphic-pop", "A clean, modern UI notification pop with a short soft airy whoosh, for a sleek phone graphic appearing on screen, crisp and premium", 1.5),
    ("sfx-endcard-hit", "A deep, polished cinematic logo hit with a soft sub boom and a bright shimmering tail, premium fintech brand end card", 3.0),
]


def music():
    out = MUSIC / "acg-theme-68s.mp3"
    if out.exists():
        return print("skip", out.name)
    r = requests.post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", headers=H,
                      json={"prompt": THEME, "music_length_ms": 68000, "force_instrumental": True}, timeout=600)
    save(out, r)


def sfx(name, text, secs):
    out = MUSIC / f"{name}.mp3"
    if out.exists():
        return print("skip", out.name)
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers=H,
                      json={"text": text, "duration_seconds": secs, "prompt_influence": 0.5}, timeout=120)
    save(out, r)


for j in JOBS:
    sts(*j)
music()
for s in SFX:
    sfx(*s)
