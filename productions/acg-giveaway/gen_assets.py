#!/usr/bin/env python3
"""ACG Markets $100K Giveaway: character sheet + six location plates on Sume (Seedream 5 Pro, 2K, ~$0.09 each).
Usage: python3 gen_assets.py            -> all 7
       python3 gen_assets.py talent     -> just the named asset(s)
Re-running skips any image already saved, so it never pays twice."""
import json, sys, time, uuid
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets"; OUT.mkdir(exist_ok=True)
for line in (ROOT.parents[1] / ".env").read_text().splitlines():
    if line.startswith("SUME_API_KEY="): KEY = line.split("=", 1)[1].strip()
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
SEEDREAM = "bytedance-seed/seedream-5-pro"

NO_TEXT = "One single continuous photograph, not a collage. No readable text, no logos, no brand names, no watermarks."
LOOK = "Photorealistic, shot on a cinema camera with a 35mm lens, natural London light, high-end commercial colour grade, fine film grain."

ASSETS = {
"talent": ("16:9", """A photorealistic character reference sheet of one man, on a seamless plain warm-grey studio backdrop with soft even light. Exactly three solid equal panels side by side with thin gaps: panel 1 is a front close-up headshot looking into the camera, panel 2 is a side-profile view of his head and shoulders, panel 3 is his full outfit from head to shoes, standing facing the camera with arms relaxed.

The man: Daniel, the confident founder-spokesman of a London trading firm, aged 36, strikingly handsome with model-grade looks. British of mixed Black Caribbean and white heritage, warm light-brown skin, a strong defined jaw, high cheekbones, warm hazel-brown eyes, a neat short boxed beard, short dark curly hair faded at the sides. A relaxed, charismatic half-smile, the look of someone about to share good news. Real skin texture and visible pores, no makeup look.

Outfit, worn the same in all panels: a tailored navy wool overcoat worn open, over a slim charcoal-grey wool suit, a crisp light-blue cotton shirt with the collar open and no tie, polished dark-brown leather Chelsea boots. A slim steel watch on the left wrist. Expensive matte fabrics, sharp modern London tailoring.

He looks identical across all three panels. No text, labels, numbers or watermarks."""),

"talent-v2": ("16:9", """A photorealistic character reference sheet of one man, on a seamless plain warm-grey studio backdrop with soft even light. Exactly three solid equal panels side by side with thin gaps: panel 1 is a front close-up headshot looking into the camera, panel 2 is a side-profile view of his head and shoulders, panel 3 is his full outfit from head to shoes, standing facing the camera with arms relaxed.

The man: a senior London investment banker and managing director, aged 64, a distinguished, strikingly handsome older man with the presence of a veteran fashion model. White British, lightly tanned skin with real lines around the eyes and forehead, a strong jaw, a straight nose, sharp clear blue eyes. Thick, full pure-white hair swept back off his forehead, neatly cut, and a short, trimmed pure-white stubble beard. A self-assured, warm half-smile, the look of a man about to share good news. Real skin texture and visible pores.

Outfit, worn the same in all panels: a fitted heavyweight black cotton crew-neck T-shirt, worn under an open tailored charcoal wool overcoat and an open navy suit jacket, with matching navy suit trousers, polished black leather Chelsea boots and a slim gold dress watch on the left wrist. Expensive matte fabrics, impeccable tailoring with a modern edge.

T-shirt print: image 1 is the company logo. Print this exact logo once, centred on the chest of the black T-shirt, about 22 cm wide, in clean solid white ink. Copy it faithfully: the angular mountain-shaped "A" mark on the left, the serif letters "ACG" on the top line and the letters "MARKETS" below. Spell it exactly "ACG MARKETS", add no other words or graphics. The jackets hang open so the whole logo stays flat, uncreased and fully visible facing the camera in panels 1 and 3.

He looks identical across all three panels. No text anywhere except the T-shirt logo, no labels, numbers or watermarks."""),

"prop-tee-flatlay": ("16:9", """A photorealistic product flat-lay sheet of one black T-shirt, shot from directly overhead on a seamless warm-grey paper background with soft, even studio light and gentle natural shadows. Exactly three solid equal panels side by side with thin gaps: panel 1 is the front of the T-shirt laid perfectly flat and symmetrical, sleeves spread out; panel 2 is the back of the same T-shirt laid flat, completely plain black with no print; panel 3 is a close-up of the chest print showing the fabric texture and the ink.

The T-shirt: a premium heavyweight black cotton crew-neck tee, matte, with a ribbed collar, a straight relaxed fit and clean stitching, neatly pressed with only soft natural folds.

Print: image 1 is the company logo. Print this exact logo once, centred on the chest of the front, about 22 cm wide, in clean solid white screen-print ink. Copy it faithfully: the angular mountain-shaped mark on the left, the serif letters "ACG" on the top line and the letters "MARKETS" below. Spell it exactly "ACG MARKETS", add no other words or graphics. The print is flat, uncreased and fully visible.

The same T-shirt in all three panels. No text anywhere except the logo, no labels, no props, no hangers, no watermarks."""),

"loc-01-tube-carriage-v2": ("16:9", f"""The interior of a modern London Underground train carriage, photographed straight-on from a seat on one side of the carriage at seated eye level, looking directly across the narrow aisle at the facing row of seats, the lens square to them. The facing bench of seats in a busy blue, red and teal patterned moquette fabric fills the lower middle of the frame, and its middle seat, directly opposite the lens and centred in frame, is empty and clearly visible, ready for one passenger to sit facing the camera. Behind the seat backs, a long window shows the black tunnel wall blurring past. A yellow-green vertical grab pole stands in the aisle on the right third of the frame, the sliding doors begin at the right edge, small red safety stickers sit on the white panels. Soft, even cool fluorescent light from the ceiling strips, no hard rays, gentle shadows under the seats, a sliver of grey floor along the bottom edge. Medium-wide 35mm framing, the carriage otherwise empty. {LOOK} {NO_TEXT}"""),

"loc-01-tube-carriage": ("16:9", f"""The interior of a modern London Underground train carriage, seen from a seated passenger's eye level looking across the aisle. A row of seats upholstered in a busy blue, red and teal patterned moquette fabric, yellow-green grab poles, white curved interior panels, small red safety stickers by the doors, dark tunnel blur outside the windows, cool fluorescent ceiling light. The carriage is quiet, with a couple of anonymous commuters out of focus at the far end and the facing seats empty. {LOOK} {NO_TEXT}"""),

"loc-02-escalators": ("16:9", f"""A deep London Underground station escalator shaft, seen from the top looking down the long bank of three parallel escalators. Brushed-steel balustrades, warm bronze uplighter lamps between the escalators, cream tiled tunnel walls and ceiling curving overhead, a few commuters with bags riding up and down in soft focus. Directional signs hang overhead but their writing is blurred and unreadable. Warm, slightly golden station light. {LOOK} {NO_TEXT}"""),

"loc-03-station-exit": ("16:9", f"""A busy central London pavement just outside the street-level entrance of an Underground station on a bright overcast summer day. A wide pale stone pavement, a stainless-steel column with a blue stripe near the entrance, a station wall clad in bold black-and-white geometric tiles, red-brick Victorian buildings and modern glass offices across the road, a red double-decker bus passing in soft focus, tourists and office workers walking past out of focus. Camera at chest height with space in the centre of frame for someone to stop. {LOOK} {NO_TEXT}"""),

"loc-03-station-exit-v2": ("16:9", f"""A busy central London pavement just outside the street-level entrance of an Underground station on a cold, grey winter morning just after rain. The camera stands just inside the station entrance at chest height looking out: the station wall on both edges of frame clad in bold black-and-white geometric tiles, a stainless-steel column with a blue stripe near the entrance, a wide pale stone pavement that is damp and softly reflective. Across the road, red-brick Victorian buildings and modern glass offices, a red double-decker bus passing in soft focus. Office workers and shoppers in dark wool coats, scarves and a few closed umbrellas walk past out of focus. Open space in the centre of the pavement for one person to stop. Soft, even overcast light, no hard sun, no shadows from the sun. {LOOK} {NO_TEXT}"""),

"loc-04-london-lane": ("16:9", f"""A narrow pedestrian street in Covent Garden, London, on a grey winter morning just after rain. Wet stone paving reflecting the light, red-brick and painted Georgian shopfronts with dark wooden window frames, black iron bollards, a bare tree with tiny warm fairy lights at the far end, a few shoppers with umbrellas and coats in soft focus walking away. Camera at head height in the middle of the street looking down its length, a classic 'day in the life' walking shot. {LOOK} {NO_TEXT}"""),

"loc-05-office-lobby": ("16:9", f"""The ground-floor lobby of a modern glass office building in the City of London in the morning. Polished pale stone floor, floor-to-ceiling glass walls, a bank of brushed-steel lift doors with glass panels on the right, a sleek minimal reception desk in the distance, strong warm sunlight slicing in from the left and casting long hard shadows across the floor. Empty of people. Camera at head height looking down the length of the lobby from the revolving entrance. {LOOK} {NO_TEXT}"""),

"loc-06-office-talking-head": ("16:9", f"""The inside of a modern London trading firm's office, framed as a set for a casual seated talking-head interview. In the background, slightly out of focus: a wall of large screens showing abstract green and red market candlestick charts and dark dashboards, open-plan desks with monitors, exposed concrete ceiling with warm pendant lights, a few plants, big windows with soft daylight. An empty modern chair in the left third of the frame for the speaker, shallow depth of field. Calm, premium, tech-forward mood. {LOOK} {NO_TEXT}"""),
}


import base64
SEEDREAM55, SUNBURST = "bytedance-seed/seedream-5.5", "openai/gpt-image-2.5-sunburst"

def data_uri(path):
    import io
    from PIL import Image
    im = Image.open(ROOT / path).convert("RGB"); im.thumbnail((1600, 1600))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# per-asset overrides: model, local reference images (sent as data URIs), extra body params
CFG = {
    "talent-v2": {"refs": ["logo/acg-logo-white.png"]},
    "prop-tee-flatlay": {"refs": ["logo/acg-logo-white.png"]},
    "prop-tee-flatlay-v2": {"model": SUNBURST, "refs": ["logo/acgm-logo-green.png"], "extra": {"quality": "high"}},
    "talent-v3": {"model": SEEDREAM55, "refs": ["assets/talent-v2.png", "assets/prop-tee-flatlay-v2.png"]},
}

ASSETS["prop-tee-flatlay-v2"] = ("16:9", """Create a photorealistic product flat-lay sheet of one black T-shirt. Image 1 is the exact company logo to print on it.

Layout: exactly three solid equal panels side by side with thin gaps, all shot from directly overhead on a seamless warm-grey paper background with soft, even studio light and gentle natural shadows. Panel 1: the front of the T-shirt laid perfectly flat and symmetrical, sleeves spread out. Panel 2: the back of the same T-shirt laid flat, completely plain black with no print. Panel 3: a straight-on close-up of the chest print showing the cotton texture and the ink.

T-shirt: a premium heavyweight black cotton crew-neck tee, matte, ribbed collar, straight relaxed fit, clean stitching, neatly pressed with only soft natural folds.

Print: reproduce the logo from image 1 exactly, with the same shapes, proportions and spacing: the small pointed peak chevron on top, the large angular "M" mountain zigzag below it, and the word "ACGM" in bold geometric sans-serif capitals underneath. Print it once, centred horizontally on the chest of the front, about 12 cm wide, in solid brand teal-green ink (#2EC4AA) as a clean screen print. Spell exactly "ACGM", add no other words, outlines, circles or graphics. The print is flat, sharp, uncreased and fully visible.

The same T-shirt in all three panels. No text anywhere except the logo, no labels, no props, no hangers, no watermarks.""")

ASSETS["talent-v3"] = ("16:9", """A photorealistic character reference sheet of one man. Image 1 shows the man: keep his exact face, bone structure, blue eyes, thick swept-back pure-white hair and short white stubble beard, unchanged and instantly recognisable. Image 2 shows the exact black T-shirt he wears, with the teal-green ACGM logo on the chest.

Layout: exactly three solid equal panels side by side with thin gaps, on a seamless plain warm-grey studio backdrop with soft even light. Panel 1: a front close-up from the chest up looking into the camera. Panel 2: a side-profile view of his head and shoulders. Panel 3: his full outfit from head to shoes, standing facing the camera with arms relaxed.

He is a senior London investment banker, aged 64, distinguished and strikingly handsome, with real skin texture, fine lines and visible pores. A self-assured, warm half-smile.

Outfit, the same in all panels: the black crew-neck T-shirt from image 2, with its teal-green ACGM logo copied exactly (the small peak chevron, the angular "M" mountain zigzag and the word "ACGM" below), centred on the chest. Over it, an open tailored navy suit jacket and an open charcoal wool overcoat, both pushed back so the whole logo stays fully visible, flat and uncovered in panels 1 and 3. Matching navy suit trousers, polished black leather Chelsea boots, a slim gold dress watch on the left wrist.

He looks identical across all three panels. No text anywhere except the T-shirt logo, no labels, numbers or watermarks.""")


CFG["banker-options"] = {"model": SEEDREAM55, "refs": ["assets/prop-tee-flatlay-v2.png"]}
ASSETS["banker-options"] = ("4:3", """A photorealistic casting reference sheet of three very different senior investment bankers, on a seamless plain warm-grey studio backdrop with soft even light. The sheet is a clean grid of exactly nine equal panels, in 3 rows and 3 columns with thin gaps. Each row is one man. Column 1 is a close-up of his face from the chest up looking at the camera, column 2 is a side view of his head and shoulders in profile, column 3 is his full outfit from head to toe with his shoes visible, standing facing the camera with arms relaxed.

Row 1: a white British managing director, aged 62, with the looks of a veteran male model. A long lean face, a strong square jaw, clean-shaven, light grey eyes, short pure silver-white hair neatly side-parted, a calm, confident, slightly amused expression.
Row 2: a Black British senior partner, aged 60, strikingly handsome. Deep brown skin, high cheekbones, warm dark-brown eyes, closely cropped pure-white hair and a neat, short pure-white full beard, a broad, charismatic smile.
Row 3: an Italian-British banker, aged 66, a distinguished silver fox. Warm olive skin, a strong Roman nose, dark brown eyes behind slim tortoiseshell glasses, thick pure-white hair swept back to just above the collar, a trimmed white beard, a knowing, relaxed half-smile.

The three men must not resemble each other: different face shapes, skin tones, hair and beards. All are very handsome, with real skin texture, fine lines and visible pores.

All three wear the same outfit: the black crew-neck T-shirt from image 1 with its teal-green ACGM logo copied exactly (the small peak chevron, the angular "M" mountain zigzag and the word "ACGM" below), centred on the chest; an open tailored navy suit jacket and an open charcoal wool overcoat, both pushed back so the whole logo is visible in columns 1 and 3; matching navy suit trousers, polished black leather Chelsea boots and a slim gold dress watch.

Each man looks identical across his three panels. No text anywhere except the T-shirt logo, no labels, numbers or watermarks.""")


CFG["storyboard-sheet"] = {"model": SEEDREAM55, "refs": ["assets/talent-v3.png", "assets/prop-tee-flatlay-v2.png",
    "assets/loc-01-tube-carriage-v2.png", "assets/loc-02-escalators.png", "assets/loc-03-station-exit-v2.png",
    "assets/loc-04-london-lane.png", "assets/loc-05-office-lobby.png", "assets/loc-06-office-talking-head.png"]}
ASSETS["storyboard-sheet"] = ("16:9", """A clean, professional film storyboard presentation page for an advertising shoot, white page with a thin black outer border, flat graphic layout like a slide.

Top centre: the bold black sans-serif title "ACG Markets $100K Giveaway".

Below it, a grid of exactly six equal 16:9 photographic panels in 2 rows of 3, each with a thin grey border, and directly under each panel a white rounded caption box with a thin grey border containing short black text. Bottom of the page: small text "Page 1" centred and "Private and Confidential internal use only." at the bottom right.

The same man appears in every panel: the white-haired banker from image 1, aged 64, thick swept-back pure-white hair, short white beard, wearing the black T-shirt from image 2 with its teal-green ACGM logo on the chest, an open navy jacket and an open charcoal overcoat. Photorealistic cinematic stills, natural London winter light, realistic people around him.

Panel 1 (top left), the Underground carriage from image 3: he sits in the centre of the patterned blue-red bench facing camera, leaning forward and talking, a passenger in earbuds two seats away. Caption: "1. TUBE: whip pan to talent. Are we recording? Good. Announcer: next station, ACG Markets."
Panel 2 (top middle), the escalator shaft from image 4: high angle down the moving escalators full of commuters, he rides up the middle one. Caption: "2. ESCALATOR: B-roll of talent leaving the station."
Panel 3 (top right), the station entrance from image 5: he stands by the blue-striped column holding a glowing phone, commuters passing. Caption: "3. STATION EXIT: So here it is. ACG Markets is live. Follow me."
Panel 4 (bottom left), the wet Covent Garden lane from image 6: side tracking shot of him walking and talking to camera past lit shopfronts, shoppers with umbrellas. Caption: "4. COVENT GARDEN: walk and talk. We're giving away $100,000."
Panel 5 (bottom middle), the glass office lobby from image 7: he strides out of a brushed-steel lift toward camera, low sun shadows on the stone floor. Caption: "5. LOBBY: into the office, out of the lift."
Panel 6 (bottom right), the trading office from image 8: casual seated talking head, market chart screens behind him, he counts on his fingers. Caption: "6. TALKING HEAD: explains how to enter and the prizes."

All text spelled exactly as written, crisp and legible. The six panels are photographs; everything else is a clean flat white layout.""")


CFG["storyboard-sheet-v2"] = {**CFG["storyboard-sheet"], "refs": ["assets/banker-row1-crop.png"] + CFG["storyboard-sheet"]["refs"][1:]}
ASSETS["storyboard-sheet-v2"] = ("16:9", """A clean, professional film storyboard presentation page for an advertising shoot, white page with a thin black outer border, flat graphic layout like a slide.

Top centre: the bold black sans-serif title "ACG Markets $100K Giveaway".

Below it, a grid of exactly six equal 16:9 photographic panels in 2 rows of 3, each with a thin grey border, and directly under each panel a white rounded caption box with a thin grey border containing short black text. Bottom of the page: small text "Page 1" centred and "Private and Confidential internal use only." at the bottom right.

The same man appears in every panel: the British managing director from image 1, aged 62, a long lean face, strong square jaw, clean-shaven, light grey eyes, short pure silver-white hair neatly side-parted; keep his exact face from image 1. He wears the black T-shirt from image 2 with its teal-green ACGM logo on the chest, an open navy jacket and an open charcoal overcoat. Photorealistic cinematic stills, natural London winter light, realistic people around him.

Panel 1 (top left), the Underground carriage from image 3: he is genuinely seated in the centre seat of the patterned blue-red bench facing camera: his hips are right back in the seat, his back rests against the seat back, his thighs lie on the seat cushion which visibly compresses under his weight, his knees bend at a right angle with both feet flat on the carriage floor, his hands loosely clasped between his knees, the bench clearly continuing on both sides of him; he leans slightly forward, talking. A passenger in earbuds sits on the same bench two seats away. Caption: "1. TUBE: whip pan to talent. Are we recording? Good. Announcer: next station, ACG Markets."
Panel 2 (top middle), the escalator shaft from image 4: high angle down the moving escalators full of commuters, he rides up the middle one. Caption: "2. ESCALATOR: B-roll of talent leaving the station."
Panel 3 (top right), the station entrance from image 5: he stands by the blue-striped column holding a glowing phone, commuters passing. Caption: "3. STATION EXIT: So here it is. ACG Markets is live. Follow me."
Panel 4 (bottom left), the wet Covent Garden lane from image 6: side tracking shot of him walking and talking to camera past lit shopfronts, shoppers with umbrellas. Caption: "4. COVENT GARDEN: walk and talk. We're giving away $100,000."
Panel 5 (bottom middle), the glass office lobby from image 7: he strides out of a brushed-steel lift toward camera, low sun shadows on the stone floor. Caption: "5. LOBBY: into the office, out of the lift."
Panel 6 (bottom right), the trading office from image 8: casual seated talking head, market chart screens behind him, he counts on his fingers. Caption: "6. TALKING HEAD: explains how to enter and the prizes."

All text spelled exactly as written, crisp and legible. The six panels are photographs; everything else is a clean flat white layout.""")


def generate(name, aspect, prompt):
    png = OUT / f"{name}.png"
    if png.exists():
        print("skip", png.name, flush=True); return
    cfg = CFG.get(name, {})
    body = {"model": cfg.get("model", SEEDREAM), "prompt": prompt, "aspect_ratio": aspect, "resolution": "2K", "output_format": "png", **cfg.get("extra", {})}
    if cfg.get("refs"):
        body["input_references"] = [{"type": "image_url", "image_url": {"url": data_uri(r)}} for r in cfg["refs"]]
    r = requests.post("https://api.sume.com/v1/images", json=body, headers={**H, "Idempotency-Key": str(uuid.uuid4())}, timeout=120)
    if r.status_code not in (200, 202):
        raise SystemExit(f"{name}: {r.status_code} {r.text[:800]}")
    res = r.json()
    if r.status_code == 202:
        job = res["data"]
        while True:
            s = requests.get(job["status_url"], headers=H, timeout=60).json()["data"]
            st = (s.get("job") or s).get("status")
            print(time.strftime("%H:%M:%S"), name, st, flush=True)
            if st in ("succeeded", "completed", "failed", "canceled", "cancelled"): break
            time.sleep(10)
        res = requests.get(job["result_url"], headers=H, timeout=60).json()
    url = next((v for v in json.dumps(res).split('"') if v.startswith("http") and ("media.sume.com" in v or v.split("?")[0].endswith((".png", ".jpg", ".jpeg", ".webp")))), None)
    if not url:
        raise SystemExit(f"{name}: no image url: {json.dumps(res)[:800]}")
    png.write_bytes(requests.get(url, timeout=300).content)
    saved = {**body, "input_references": cfg.get("refs", [])}
    png.with_suffix(".json").write_text(json.dumps({"url": url, "request": saved, "response": res}, indent=1))
    print("OK  ", png.name, flush=True)


for n in (sys.argv[1:] or ASSETS):
    generate(n, *ASSETS[n])
