#!/usr/bin/env python3
"""Follow the Bag: regenerate the rider and his kit in the existing Bolly Eats palette with Seedream 5.0 Pro (fal).
Edits the morning's raspberry/plum sheets (kept for face, shape and design) with our logo files as references.
3-panel 16:9 sheets on light grey. Usage: gen_seedream.py [names...]. Skips existing outputs. Key: FAL_KEY in SEED PORTFOLIO/.env"""
import os, sys, json, concurrent.futures as cf
from pathlib import Path
import fal_client, requests

ROOT = Path(__file__).resolve().parent
for line in (ROOT.parents[1] / ".env").read_text().splitlines():
    if line.startswith("FAL_KEY="): os.environ["FAL_KEY"] = line.split("=", 1)[1].strip()
EDIT = "bytedance/seedream/v5/pro/edit"
BRAND_DIR = ROOT.parent / "bolly-eats" / "brand"
OUT = ROOT / "regen"

PALETTE = ("BOLLY EATS BRAND COLOURS, replacing every raspberry pink and plum from the original: masala maroon #5B1A1F, turmeric "
           "yellow #F4B400, warm cream #FFF4E0, with chilli red #E2462B only as a thin accent. NO raspberry, NO hot pink, NO purple "
           "anywhere. LOGO exactly as in the logo images: three short wavy steam lines above the lowercase words 'bolly eats.' in a "
           "heavy rounded grotesque, spelled b-o-l-l-y e-a-t-s with the full stop. Reproduce the logo exactly; no other text. ")
SHEET = ("ONE 16:9 reference sheet split into THREE equal vertical panels side by side with thin white gutters, seamless warm "
         "light-grey studio background in every panel, soft even 5600K studio light with gentle contact shadows, photoreal, "
         "real material texture. Every panel shows the SAME subject with identical proportions, colours and logo. ")

JOBS = {  # name: ([reference image paths], prompt). Image 1 is always the original sheet being restyled.
 "rider": ([ROOT / "characters/courier-man-purple-jacket-sheet.jpg", BRAND_DIR / "bolly-logo-on-turmeric.png",
            BRAND_DIR / "bolly-logo-on-masala.png"],
   "Restyle the delivery rider from image 1. Keep EXACTLY the same man: same face, medium brown skin, short tidy black hair "
   "with a sharp line-up, light stubble, lean athletic build, friendly relaxed expression. " + PALETTE + "Logos as in images 2 "
   "and 3. WARDROBE: masala maroon #5B1A1F waterproof shell jacket with thin turmeric yellow piping along the shoulders, zip and "
   "cuffs, a small cream logo on the left chest and a larger turmeric logo across the upper back; black tapered technical "
   "trousers, black trainers, fingerless black gloves. HELMET: turmeric yellow cycling helmet with one masala maroon stripe. "
   + SHEET + "PANEL 1 (left): neutral front headshot, no helmet. PANEL 2 (middle): three-quarter headshot wearing the helmet with "
   "the clip fastened, warm smile. PANEL 3 (right): FULL-LENGTH OUTFIT, head to shoes, standing relaxed facing camera, helmet "
   "on, jacket chest logo readable. Pore-level skin texture, natural asymmetry, living eyes with catch-lights."),
 "backpack": ([ROOT / "props/delivery-backpack-raspberry-sheet.jpg", BRAND_DIR / "bolly-logo-on-turmeric.png",
               BRAND_DIR / "bolly-logo-on-masala.png"],
   "Restyle the insulated food delivery backpack from image 1. Keep EXACTLY the same object: a rigid cube-shaped thermal "
   "backpack about 42 cm each side, slightly rounded corners, neat stitched edge seams, top-opening lid zipped around three "
   "sides, padded shoulder straps and chest strap, a thin reflective strip around the base. " + PALETTE + "Logos as in images "
   "2 and 3. NEW COLOURS: matte turmeric yellow #F4B400 water-resistant coated fabric body; masala maroon #5B1A1F zip, pull "
   "tab, straps and edge piping; a large masala maroon logo on each side panel; a cream reflective base strip. " + SHEET +
   "PANEL 1 (left): front three-quarter view, lid closed, side logo readable. PANEL 2 (middle): back view showing the maroon "
   "straps. PANEL 3 (right): three-quarter view with the lid open, silver foil insulated interior, a closed turmeric-and-maroon "
   "Bolly Eats paper food bag sitting inside."),
 "ebike": ([ROOT / "props/cargo-ebike-pink-box-sheet.jpg", BRAND_DIR / "bolly-logo-on-turmeric.png"],
   "Restyle the delivery e-bike from image 1. Keep EXACTLY the same bike: black step-through urban e-bike, matte frame, black "
   "tyres, battery in the down tube, a moulded rear crate over the back wheel with a black elastic cargo strap across the top. "
   + PALETTE + "Logo as in image 2. NEW COLOURS: the rear crate is turmeric yellow #F4B400 with the masala maroon logo on its "
   "back face; a thin masala maroon line along the crate rim. The bike frame stays black. " + SHEET + "PANEL 1 (left): left "
   "side view. PANEL 2 (middle): three-quarter rear view. PANEL 3 (right): straight rear view with the crate logo readable."),
}

def go(name):
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{name}-bolly-palette-v1.jpg"
    if out.exists(): return f"skip {name}"
    refs, prompt = JOBS[name]
    args = {"prompt": prompt, "image_urls": [fal_client.upload_file(str(r)) for r in refs], "image_size": "auto_2K",
            "num_images": 1, "output_format": "jpeg", "enhance_prompt_mode": "standard"}
    h = fal_client.submit(EDIT, arguments=args)
    (OUT / f"{name}-bolly-palette-v1.json").write_text(json.dumps({"endpoint": EDIT, "request_id": h.request_id,
        "refs": [str(r) for r in refs], "input": args}, indent=1))
    res = h.get()
    out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
    return f"DONE {name} -> {out}"

with cf.ThreadPoolExecutor(3) as ex:
    for r in ex.map(go, sys.argv[1:] or list(JOBS)): print(r, flush=True)
