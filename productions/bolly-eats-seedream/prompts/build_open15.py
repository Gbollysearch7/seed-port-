#!/usr/bin/env python3
"""Follow the Bag, first 15 s as ONE continuous take (kitchen -> through the glass door -> kerb -> ride off).
Seedance 2.0 reference-to-video, 480p, 16:9, 15 s (~$1.35). Writes follow-the-bag-open15.json/.txt for pipeline/atlas_run.py."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODEL = "bytedance/seedance-2.0/reference-to-video"
REFS = [  # (path relative to ROOT, role)
 ("locations/restaurant-kitchen-blue-hour.jpg", "the restaurant: open kitchen, steel pass under amber heat lamps, glass front door"),
 ("locations/high-street-rain-neon-burger-shop-b.jpg", "the wet high street outside the restaurant at blue hour"),
 ("regen/chef-plain-apron-v1.jpg", "the chef: black cap, white t-shirt, plain white apron, black gloves, forearm tattoos"),
 ("regen/rider-bolly-palette-v1.jpg", "the rider: maroon Bolly Eats jacket with turmeric piping, turmeric helmet, black trousers"),
 ("regen/ebike-bag-mount-v1.jpg", "the rider's black e-bike with the turmeric Bolly Eats delivery bag fixed on the rear rack"),
 ("../bolly-eats/assets/brand-bag-grey-v1.png", "the Bolly Eats paper takeaway bag: turmeric front, maroon back and sides"),
 ("../bolly-eats/assets/brand-shakes-grey-v1.png", "the Bolly Eats shake cups and maroon carrier"),
 ("regen/burger-box-fries-v1.jpg", "the Bolly Eats turmeric burger box and fries carton with the maroon logo"),
]
c = [f"@Image{i + 1}" for i in range(len(REFS))]
PROMPT = f"""[REFERENCES]
""" + "\n".join(f"{c[i]} = {r[1]}." for i, r in enumerate(REFS)) + f"""
Character sheets are identity only: one chef, one rider, one single continuous scene, never a collage.

[STYLE]
Photoreal live-action food-delivery commercial, 16:9, London at blue hour just after rain. One continuous take that never cuts:
the camera follows the food from the grill, into the bag, out of the door and onto the bike. Warm amber light inside the kitchen,
cool blue dusk and pink-amber neon reflections outside. Bolly Eats colours are turmeric yellow #F4B400 and masala maroon #5B1A1F;
every logo is three wavy steam lines over the lowercase words 'bolly eats.' exactly as on the packaging in {c[7]}. Fine natural grain, real textures.

[TIMELINE]
0-3 s: macro close-up on the flat-top grill in the kitchen of {c[0]}. A smash-burger patty sizzles with melting cheese. The chef's
black-gloved hand ({c[2]}) slides a steel spatula under it and lifts it onto a toasted bun waiting on the steel pass.
3-5 s: he crowns the burger and sets it into the open turmeric burger box ({c[7]}), then snaps the lid shut. The turmeric fries
carton ({c[7]}), full of golden fries, stands beside it. The camera drifts back, staying on the food.
5-7 s: he puts the burger box and fries into the Bolly Eats paper takeaway bag ({c[5]}), with the two shakes in their carrier
({c[6]}) beside it, folds the top of the bag over and presses a round turmeric steam-mark sticker down with his thumb.
7-9 s: he slides the sealed bag across the pass. The rider ({c[3]}), helmet on, takes it by the handles. The camera follows the
bag as he turns and walks toward the glass front door.
9-11 s: he pushes the glass door open and the camera follows him straight through the open doorway onto the wet pavement of
{c[1]}, neon reflecting in the puddles.
11-13 s: at the kerb stands his e-bike ({c[4]}). He unzips the lid of the turmeric delivery bag fixed on the rear rack, lowers
the paper bag inside and zips it shut.
13-15 s: he swings onto the bike and pushes off down the shining street; the camera rises and follows the turmeric delivery bag
as he rides away.

[CAMERA]
One unbroken gimbal move, no cuts, no dissolves, no wipes: macro at the grill, a gentle pull back along the pass, a follow
through the open door, a low glide at the kerb, then a rising chase behind the bike.

[AUDIO]
Grill sizzle, spatula scrape, box lid snap, paper fold, sticker press, door creak, rain hiss on the street, zip, e-bike whir.
Sound design only, no music, no voices.

[NEGATIVE]
No cuts or scene changes; no on-screen text, captions or subtitles; no other delivery brands (no Uber Eats, no Deliveroo, no
Just Eat, no McDonald's), no green, teal or black-and-white delivery bags; no pink, raspberry or purple branding; no logo on the
chef's apron; no ropes, cords or bungees on the bike bag; exactly one chef and one rider, no customers, no other riders; the
chef stays in the kitchen; faces and outfits match the references; no daylight."""

payload = {"model": MODEL, "prompt": PROMPT, "reference_images": [r[0] for r in REFS], "duration": 15, "resolution": "480p",
           "ratio": "16:9", "generate_audio": True, "watermark": False, "return_last_frame": True}
pack = {"model": MODEL, "production_root": str(ROOT),
        "clips": [{"id": "OPEN-15", "title": "Follow the Bag 0-15 s", "est_cost_usd": round(15 * 0.09, 2), "payload": payload}]}
(HERE / "follow-the-bag-open15.json").write_text(json.dumps(pack, indent=1, ensure_ascii=False))
(HERE / "follow-the-bag-open15.txt").write_text(f"{MODEL} · 480p · 16:9 · 15 s · ~$1.35\n\nREFERENCES (upload order):\n" +
    "\n".join(f"  {c[i]}  {r[0]}" for i, r in enumerate(REFS)) + f"\n\nPROMPT:\n{PROMPT}\n")
missing = [r[0] for r in REFS if not (ROOT / r[0]).exists()]
print("built;", len(PROMPT), "chars;", len(REFS), "refs; missing:", missing or "none")
