#!/usr/bin/env python3
"""SEED PORTFOLIO character sheets: young New York millennials on fal GPT Image 2.5 Sunburst (text-to-image), 16:9.
Three panels per sheet: front close-up, three-quarter close-up (hair + piercings), full-length outfit.
Usage: gen_character_sheets.py [names...]. Skips existing outputs. Key: FAL_KEY in SEED PORTFOLIO/.env"""
import os, sys, json, concurrent.futures as cf
from pathlib import Path
import fal_client, requests

ROOT = Path(__file__).resolve().parent
for line in (ROOT.parents[2] / ".env").read_text().splitlines():
    if line.startswith("FAL_KEY="): os.environ["FAL_KEY"] = line.split("=", 1)[1].strip()
T2I = "openai/gpt-image-2.5/sunburst/text-to-image"
SIZE = {"width": 1824, "height": 1024}

LAYOUT = ("ONE photorealistic CHARACTER REFERENCE SHEET, horizontal 16:9, split into THREE equal vertical panels side by side, "
          "separated by thin white gutters, all three showing the SAME person with an identical face, hair, skin, piercings and "
          "outfit. Every panel uses the same plain light-grey seamless studio backdrop and the same soft, even key light with a "
          "gentle fill, true-to-life skin tones. PANEL 1 (left): front-facing head-and-shoulders close-up portrait, looking straight "
          "into the lens, neutral relaxed expression, sharp detail on eyes, skin texture and every piercing. PANEL 2 (middle): "
          "three-quarter view head-and-shoulders close-up turned to the left, showing the hair from the side and back plus the ear "
          "and facial piercings clearly. PANEL 3 (right): FULL-LENGTH OUTFIT panel, the whole body head to toe, standing naturally "
          "facing camera, feet and shoes fully visible inside the frame, so every garment, layer, accessory and the footwear read "
          "clearly. Real photography, 85mm lens for the close-ups and 50mm for the full length, subtle film grain, natural skin "
          "with pores and slight imperfections, not airbrushed, not a render, not a cartoon. No text, no captions, no labels, no "
          "numbers, no logos or brand names on any clothing, no watermark. ")

JOBS = {
 "jalen-braids": LAYOUT + "THE CHARACTER: Jalen, a 28-year-old Black man from Brooklyn, New York, a young millennial with pop-star "
   "energy and a confident, playful half-smile in his eyes. Rich deep-brown skin, sharp jawline, short neat beard line, thick "
   "brows. HAIR: shoulder-length medium knotless box braids, the ends dipped in honey blonde, half of the braids gathered up into a "
   "high top knot and the rest falling to his shoulders, clean edges. PIERCINGS: a small silver hoop in the left nostril, a "
   "silver eyebrow bar in the right brow, stacked silver hoops and studs up both ears including a helix hoop, a single small "
   "silver ring in the lower lip. JEWELLERY: a layered silver Cuban chain and a thinner silver chain with a small pendant, chunky "
   "silver rings on several fingers, black painted nails. OUTFIT (downtown New York street style, 2026): an oversized cropped "
   "cherry-red leather bomber jacket worn open, over a faded vintage-washed oversized black graphic band tee with an abstract "
   "cracked print (no readable words), very baggy light-wash carpenter jeans with a hammer loop, stacked at the ankle, chunky "
   "grey-and-cream retro running sneakers, a black nylon crossbody sling bag worn across the chest, white crew socks.",
 "nova-colour": LAYOUT + "THE CHARACTER: Nova, a 27-year-old mixed-race (Black and Puerto Rican) woman from the Lower East Side, New "
   "York, a young millennial with bold pop-star attitude, a knowing smirk and bright eyes. Warm golden-brown skin with natural "
   "freckles across the nose, full brows, glossy lips, a sharp graphic electric-blue winged eyeliner. HAIR: vivid two-tone dyed "
   "hair, hot bubblegum pink at the crown blending into lilac-lavender lengths, chin-length shaggy wolf cut with curtain bangs, "
   "soft natural texture, dark roots just showing. PIERCINGS: a silver septum ring, a silver labret stud under the lower lip, a "
   "silver ring in the left eyebrow, both ears filled with silver hoops and studs including an industrial bar across the upper "
   "right ear and a conch hoop. JEWELLERY: a silver choker chain with a tiny padlock, layered thin silver necklaces, stacked "
   "silver rings, long almond nails in chrome lilac. OUTFIT (downtown New York street style, 2026): a cropped black leather moto "
   "jacket with silver zips worn open, over a fitted cropped baby tee in pastel baby-pink with a small abstract heart graphic "
   "(no words), a low-slung pair of very wide-leg dark indigo baggy jeans with a silver studded belt, black chunky platform boots, "
   "a tiny lilac quilted shoulder bag on a silver chain strap, tinted lilac oval sunglasses pushed up into her hair in the "
   "full-length panel only.",
 "priya-gloss": LAYOUT + "THE CHARACTER: Priya, a 29-year-old Indian-American woman from Jackson Heights, Queens, New York, a young "
   "millennial with warm, sharp-witted pop energy and a wide, mischievous grin. Medium-brown skin with a natural glow, strong arched "
   "brows, glossy brown lips, soft bronze shimmer on the lids, a tiny gold bindi-style face gem between the brows. HAIR: long, glossy "
   "jet-black hair with chunky money-piece face-framing streaks dyed bright cherry red, worn in a high sleek ponytail with two loose "
   "front strands. PIERCINGS: a small gold hoop in the left nostril, a gold septum clicker, gold huggie hoops and studs stacked up both "
   "ears including a gold chain cuff on the right helix. JEWELLERY: layered thin gold necklaces, a stack of thin gold bangles on one "
   "wrist, gold rings, short square nails in glossy cherry red. OUTFIT (downtown New York street style, 2026): an oversized vintage "
   "mustard-yellow suede trucker jacket worn open, a fitted black ribbed cropped halter top, low-rise khaki parachute cargo pants "
   "with toggle hems, white chunky leather sneakers, a small black leather baguette bag on a short strap.",
 "theo-bleach": LAYOUT + "THE CHARACTER: Theo, a 27-year-old Korean-American man from Flushing, Queens, New York, a young millennial "
   "with laid-back pop-idol cool and a dry, amused look. Light warm-toned skin, clean-shaven, defined cheekbones, monolid eyes. HAIR: "
   "a textured bleached platinum-silver crop with a slightly messy fringe falling over the forehead and dark roots just growing in. "
   "PIERCINGS: a silver eyebrow ring in the left brow, a silver bridge bar across the top of the nose, a snake-bite pair of small silver "
   "studs at both corners under the lower lip, both ears stacked with silver hoops and a dangling silver cross earring on the left. "
   "JEWELLERY: a silver ball-chain necklace with a small dog tag, silver rings, chipped black nail polish. OUTFIT (downtown New York "
   "street style, 2026): an oversized forest-green knitted cardigan with chunky buttons, worn open over a white oversized tank top, "
   "baggy black denim jorts to just below the knee, white knee-high tube socks with two green stripes, black leather loafers with "
   "chunky soles, a black canvas tote bag on one shoulder.",
}

EDIT = "openai/gpt-image-2.5/sunburst/edit"
KEEP = ("Recreate image 1 EXACTLY: the same person with the identical face, skin, hair, piercings, jewellery and nails, the same "
        "three-panel layout, the same light-grey studio backdrop, lighting, framing and poses. ONE CHANGE ONLY, the INDOOR LOOK for a "
        "night in at a friend's apartment: ")
INDOOR = {  # name: (v1 sheet to edit from, indoor wardrobe change)
 "jalen-braids": ("jalen-braids-sheet-v1.png", "the red leather bomber jacket and the crossbody sling bag are removed. He wears the "
   "same faded oversized black graphic tee with the abstract cracked print, now fully visible with the sleeves showing his forearms, "
   "the same baggy light-wash carpenter jeans, white crew socks and the same chunky grey-and-cream sneakers. Piercings: exactly ONE "
   "silver bar in his right eyebrow only, the left eyebrow has no piercing, in every panel."),
 "nova-colour": ("nova-colour-sheet-v1.png", "the black leather moto jacket, the lilac shoulder bag and the sunglasses are removed. "
   "She wears the same fitted cropped pastel baby-pink baby tee with the small heart graphic, now fully visible including her bare "
   "arms, the same low-slung very wide-leg dark indigo jeans with the silver studded belt, and the same black chunky platform boots."),
 "priya-gloss": ("priya-gloss-sheet-v1.png", "the mustard-yellow suede jacket and the black shoulder bag are removed. She wears the "
   "same fitted black ribbed cropped halter top, now fully visible with her bare shoulders and arms and gold bangles, the same "
   "low-rise khaki parachute cargo pants with toggle hems and the same white chunky sneakers."),
 "theo-bleach": ("theo-bleach-sheet-v1.png", "the black tote bag is removed. He keeps the same oversized forest-green knitted "
   "cardigan worn open over the white tank top, the same baggy black denim jorts, white knee-high striped tube socks and black "
   "chunky loafers."),
}

def go_indoor(name):
    src, change = INDOOR[name]
    out_dir = ROOT / name
    out = out_dir / f"{name}-indoor-v2.png"
    if out.exists(): return f"skip {name} indoor"
    args = {"prompt": KEEP + change + " No text, no captions, no logos, no watermark.", "image_size": SIZE, "quality": "high",
            "num_images": 1, "output_format": "png", "image_urls": [fal_client.upload_file(str(out_dir / src))]}
    handle = fal_client.submit(EDIT, arguments=args)
    (out_dir / f"{name}-indoor-v2.json").write_text(json.dumps({"endpoint": EDIT, "request_id": handle.request_id, "source": src, "input": args}, indent=1))
    res = handle.get()
    out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
    return f"DONE {name} indoor -> {out}"

if sys.argv[1:2] == ["indoor"]:
    with cf.ThreadPoolExecutor(4) as ex:
        for r in ex.map(go_indoor, sys.argv[2:] or list(INDOOR)): print(r, flush=True)
    sys.exit()

def go(name):
    out_dir = ROOT / name; out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{name}-sheet-v1.png"
    if out.exists(): return f"skip {name}"
    args = {"prompt": JOBS[name], "image_size": SIZE, "quality": "high", "num_images": 1, "output_format": "png"}
    handle = fal_client.submit(T2I, arguments=args)
    (out_dir / f"{name}-sheet-v1.json").write_text(json.dumps({"endpoint": T2I, "request_id": handle.request_id, "input": args}, indent=1))
    res = handle.get()
    out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
    return f"DONE {name} -> {out}"

names = sys.argv[1:] or list(JOBS)
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(go, names): print(r, flush=True)
