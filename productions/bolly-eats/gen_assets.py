#!/usr/bin/env python3
"""Bolly Eats "Peace, delivered" spot: location, prop and branded asset sheets on fal GPT Image 2.5 Sunburst.
Assets only, never storyboard frames: these sheets plus the shot prompt go to Seedance.
Branded assets use the edit endpoint with the rendered logo / bag / shake references from brand/ (render_brand.py).
Usage: gen_assets.py [names...]. Skips existing outputs. Key: FAL_KEY in SEED PORTFOLIO/.env"""
import os, sys, json, concurrent.futures as cf
from pathlib import Path
import fal_client, requests

ROOT = Path(__file__).resolve().parent
for line in (ROOT.parents[1] / ".env").read_text().splitlines():
    if line.startswith("FAL_KEY="): os.environ["FAL_KEY"] = line.split("=", 1)[1].strip()
T2I, EDIT = "openai/gpt-image-2.5/sunburst/text-to-image", "openai/gpt-image-2.5/sunburst/edit"
WIDE = {"width": 1824, "height": 1024}
B = ROOT / "brand"

PHOTO = ("Real photography, true-to-life colour, subtle film grain, natural imperfections, believable and lived-in, not a render, "
         "not a cartoon. No people, no hands, no watermark. ")
SHEET = ("ONE photorealistic PRODUCTION REFERENCE SHEET, horizontal 16:9, split into THREE equal vertical panels side by side with thin "
         "white gutters, all three showing the SAME object or place with identical design, materials and colours. ")
BRAND = ("BRAND: Bolly Eats, a cheeky Indian food delivery brand. Colours: masala maroon #5B1A1F, turmeric yellow #F4B400, chilli red "
         "#E2462B, rose pink #E8889A, warm cream #FFF4E0. The logo is EXACTLY as in image 1: three wavy steam lines above the lowercase "
         "words 'bolly eats.' in a heavy rounded grotesque, spelled b-o-l-l-y e-a-t-s with the full stop. Reproduce the logo exactly, "
         "never invent other text. ")

JOBS = {
 # name: (endpoint, [reference images], prompt)
 "living-room": (T2I, [], SHEET + "THE LOCATION: a lived-in young creatives' apartment living room in a Brooklyn, New York pre-war "
   "walk-up, late evening, warm practical lamp light mixed with a cool blue city glow from the windows. Exposed red brick wall, tall "
   "sash windows with a fire escape outside, worn oak floorboards, a large patterned vintage rug. A big slouchy oatmeal boucle "
   "three-seat sofa covered in mismatched cushions (mustard velvet, rose pink, a checkered one, a fringed kilim cushion) and a thrown "
   "knit blanket. In front of it a low, wide, chunky oak coffee table, mostly clear apart from a candle, two remote controls and a "
   "magazine, with room for food to be spread across it. Plants, a record player on a sideboard, string lights, framed gig posters "
   "with no readable text. The apartment front door is a painted deep-green panelled door with a brass knob, a chain lock and a "
   "peephole, a coat hook with jackets beside it, reached by a short hallway visible from the sofa. PANEL 1 (left): wide establishing "
   "view of the whole room from a corner at standing eye height, showing the sofa, the coffee table and the front door in the "
   "background. PANEL 2 (middle): closer view of the sofa, cushions and coffee table, from where a seated friend opposite would see "
   "them. PANEL 3 (right): the front door and short hallway seen from the sofa, door closed, warm hallway light. Completely empty of "
   "people. " + PHOTO),
 "fry-box": (EDIT, [B / "bolly-logo-on-turmeric.png"], SHEET + BRAND + "THE PROP, the hero of the film: an open Bolly Eats "
   "takeaway fries box, a sturdy turmeric-yellow #F4B400 paperboard scoop box with the masala-maroon logo from image 1 printed on the "
   "front, lightly grease-spotted and slightly crumpled from being passed around. It is ALMOST EMPTY: just a few crumbs of red "
   "masala seasoning on the bottom and ONE single golden crinkle-cut masala fry left, dusted with red chilli spice, lying alone "
   "inside. Sitting on a warm oak coffee table. PANEL 1 (left): front three-quarter view at table height, logo readable. PANEL 2 "
   "(middle): looking straight down into the box, the lone fry sharp in focus. PANEL 3 (right): extreme close-up macro of the single "
   "fry with its spice texture, shallow depth of field. Moody warm evening lamp light. " + PHOTO),
 "smartphone": (T2I, [], SHEET + "THE PROP: a modern unbranded smartphone with thin flat edges, rounded corners and a matte "
   "graphite-grey aluminium frame, a triple camera bump on the back, NO logo anywhere on it, in a clear slim case with a small "
   "lilac-and-pink sticker on the back (abstract star shapes, no text). PANEL 1 (left): front view, the screen on and showing a plain "
   "warm cream #FFF4E0 blank screen. PANEL 2 (middle): back view showing the camera bump and the sticker. PANEL 3 (right): edge-on "
   "three-quarter view lying on an oak coffee table beside a knit blanket. Soft warm studio light, clean grey seamless background for "
   "panels 1 and 2. " + PHOTO),
 "delivery-bags": (EDIT, [B / "bolly-logo-on-turmeric.png", B / "ref-bag-design.png"], SHEET + BRAND + "THE ASSET: the Bolly Eats "
   "paper delivery bag, built EXACTLY to the design in image 2: heavy kraft-board bag, turmeric-yellow #F4B400 front with the logo, "
   "'Food with drama.' under it and a masala-maroon band at the bottom reading 'HOT · FAST · FILMI'; masala-maroon gusset sides "
   "with 'bolly eats.' running vertically; masala-maroon back reading 'Every meal deserves an entrance.' with a cream round 'sealed "
   "for' sticker; twisted brown kraft paper handles. The bag is full and heavy, the top folded and closed with a small turmeric "
   "sticker. PANEL 1 (left): one bag front view, standing on a wooden floor. PANEL 2 (middle): the same bag back view. PANEL 3 "
   "(right): TWO full bags side by side on a doorstep doormat outside a deep-green apartment door, three-quarter view. Copy the "
   "text from image 2 exactly. " + PHOTO),
 "feast": (EDIT, [B / "bolly-logo-on-turmeric.png", B / "ref-shake-carrier-design.png", B / "ref-shake-cups-design.png"], SHEET + BRAND
   + "THE ASSET: a delivered Bolly Eats feast to share, spread across a chunky oak coffee table. Several open takeaway containers: "
   "masala-maroon #5B1A1F and turmeric-yellow #F4B400 paperboard boxes and bowls, each with the logo from image 1, holding rich, "
   "steaming, glossy, appetising Indian food: a bowl of orange butter chicken with a swirl of cream and coriander, a box of fluffy "
   "saffron lamb biryani with fried onions and a lemon wedge, four golden crispy samosas with green chutney and tamarind dips, "
   "blistered garlic naan torn open in a paper sleeve, a full box of crinkle-cut masala fries dusted with red chilli spice. The two "
   "milkshakes stand in the shake carrier from image 2, cups built exactly like image 3: a turmeric mango masala shake and a rose "
   "falooda shake, clear dome lids, wide straws. Steam rising, condensation on the cups, a few napkins, the empty fold-down paper "
   "bag to one side. PANEL 1 (left): overhead top-down 'everything on the table' hero view of the whole feast. PANEL 2 (middle): low "
   "three-quarter table-level view, food in the foreground with an empty oatmeal sofa and cushions softly out of focus behind. PANEL 3 "
   "(right): close-up of the butter chicken and torn naan, sauce glossy, steam visible. Warm evening lamp light, mouth-watering "
   "food-commercial styling but natural, not plastic. " + PHOTO),
}

GREY = ("STUDIO: every panel on the same plain light-grey seamless studio backdrop and grey floor, soft even key light with a gentle "
        "fill and a soft contact shadow, product-catalogue clarity, nothing else in frame. ")
A = ROOT / "assets"
JOBS.update({
 "brand-bag-grey": (EDIT, [B / "bolly-logo-on-turmeric.png", B / "ref-bag-design.png"], SHEET + BRAND + GREY + "THE ASSET: the Bolly "
   "Eats paper delivery bag, built EXACTLY to the design in image 2: heavy kraft-board bag, turmeric-yellow #F4B400 front with the "
   "logo, 'Food with drama.' under it and a masala-maroon band at the bottom reading 'HOT · FAST · FILMI'; masala-maroon gusset sides "
   "with 'bolly eats.' running vertically; masala-maroon back reading 'Every meal deserves an entrance.' with a cream round 'sealed for' "
   "sticker; twisted brown kraft paper handles standing up. The bag is full, top folded once and closed with a small round turmeric "
   "sticker. PANEL 1 (left): front view. PANEL 2 (middle): back view. PANEL 3 (right): three-quarter view showing the front and one "
   "gusset side. Copy the text from image 2 exactly, no other text. " + PHOTO),
 "brand-packaging-grey": (EDIT, [B / "bolly-logo-on-turmeric.png"], SHEET + BRAND + GREY + "THE ASSET: the Bolly Eats food packaging "
   "set, all closed and new, each piece printed with the logo from image 1: a masala-maroon #5B1A1F rectangular paperboard meal box with "
   "a fold-over tuck lid, a turmeric-yellow #F4B400 round paper soup-style bowl with a fitted lid, a turmeric-yellow fries scoop box "
   "full of crinkle-cut masala fries dusted with red chilli spice, a kraft paper naan sleeve, a stack of cream napkins with the logo in "
   "masala. PANEL 1 (left): the whole set grouped together, three-quarter view. PANEL 2 (middle): the meal box and round bowl front on, "
   "logos readable. PANEL 3 (right): the full fries box front on, logo readable. " + PHOTO),
 "brand-shakes-grey": (EDIT, [B / "bolly-logo-on-turmeric.png", B / "ref-shake-cups-design.png", B / "ref-shake-carrier-design.png"],
   SHEET + BRAND + GREY + "THE ASSET: the two Bolly Eats milkshakes and their carrier, built EXACTLY to images 2 and 3. Cups: tapered "
   "paper cups with clear dome lids and wide straws; the Mango Masala Shake in a turmeric-yellow cup with a chilli-red straw, a creamy "
   "pale mango-yellow shake visible under the dome; the Rose Falooda Shake in a rose-pink #E8889A cup with a masala-maroon straw, a "
   "pink shake visible under the dome; each cup with the masala logo and a masala band reading 'SHAKE IT, HERO'. Carrier: a "
   "masala-maroon recycled-board two-cup carrier with a fold-up turmeric handle. Light condensation on the cups. PANEL 1 (left): both "
   "cups side by side, front view. PANEL 2 (middle): both cups standing in the carrier, three-quarter view. PANEL 3 (right): the carrier "
   "with cups from directly above. Copy the text from images 2 and 3 exactly, no other text. " + PHOTO),
 "brand-phone-order-grey": (EDIT, [B / "order-confirmation-screen.png", A / "smartphone-v1.png"], SHEET + GREY + "THE ASSET: the "
   "smartphone from image 2 (unbranded graphite-grey phone, thin flat edges, clear slim case, the lilac-and-pink star sticker on the "
   "back, NO logo anywhere) with its screen ON and displaying EXACTLY the app screen in image 1, the Bolly Eats 'Order confirmed' screen: "
   "masala-maroon top with the yellow steam marks and 'bolly eats.' logo, a yellow tick circle, 'Order confirmed', 'Your feast is on its "
   "way.', then the cream lower half with 'ARRIVING IN 25 min', the four-step tracker and the order list. Reproduce the screen layout, "
   "colours and words exactly, bright and legible, with a faint natural screen reflection. PANEL 1 (left): phone standing upright, "
   "screen straight to camera. PANEL 2 (middle): phone propped on a small stand at a slight three-quarter angle, screen still readable. PANEL 3 (right): "
   "phone lying flat, seen from above at an angle, screen glowing. " + PHOTO),
 "phone-place-order-grey": (EDIT, [B / "order-cart-screen.png", A / "smartphone-v1.png"], SHEET + GREY + "THE ASSET: the "
   "smartphone from image 2 (unbranded graphite-grey phone, thin flat edges, clear slim case, the lilac-and-pink star sticker on the "
   "back, NO logo anywhere) with its screen ON and displaying EXACTLY the app screen in image 1, the Bolly Eats 'Your basket' screen: "
   "masala-maroon top with the yellow steam marks, 'bolly eats.' logo, 'Your basket' and 'Feast for four · 7 items', then the cream "
   "lower half with the seven items and their minus/plus buttons, 'DELIVER TO Home · about 25 min' and the big turmeric 'Place order' "
   "button at the bottom. The screen fills the whole display edge to edge, no clock or status bar added. Reproduce the screen layout, "
   "colours and words exactly, bright and legible, with a faint natural screen reflection. PANEL 1 (left): phone standing upright, "
   "screen straight to camera. PANEL 2 (middle): phone propped on a small stand at a slight three-quarter angle, screen still "
   "readable. PANEL 3 (right): the back of the phone, showing the camera bump and star sticker. " + PHOTO),
 "fry-box-plain-grey": (T2I, [], SHEET + GREY + "THE PROP, the hero of the film: an open takeaway fries box from an anonymous "
   "takeaway, completely UNBRANDED: plain white paperboard scoop box with a simple thin red stripe around the top edge, NO logo, NO "
   "words, NO lettering or symbols anywhere on it. Lightly grease-spotted and a little crumpled from being passed around. It is ALMOST "
   "EMPTY: a few crumbs of salt and seasoning on the bottom and ONE single golden straight-cut fry left, lying alone inside. PANEL 1 "
   "(left): front three-quarter view at table height. PANEL 2 (middle): looking straight down into the box, the lone fry sharp in focus. "
   "PANEL 3 (right): close-up of the single fry inside the box, shallow depth of field. " + PHOTO),
 "living-room-34-bluehour": (EDIT, [A / "living-room-v1.png"], SHEET + "THE LOCATION: EXACTLY the same Brooklyn, New York pre-war "
   "walk-up living room as image 1, keep every design element identical: exposed red brick wall, tall black sash windows with the fire "
   "escape outside, worn oak floorboards, the big patterned vintage rug, the slouchy oatmeal boucle three-seat sofa with its mismatched "
   "cushions (mustard velvet, rose pink, black-and-white checkered, red fringed kilim) and knit throw, the low chunky reclaimed-oak "
   "coffee table with a candle, two remotes and a magazine, the framed gig posters, plants, string lights, the record player and vinyl "
   "shelf, and the deep-green panelled front door with brass knob at the end of the short hallway. TIME OF DAY, locked for every panel: "
   "BLUE HOUR just after sunset, about 7:30 pm. Through the windows a deep cobalt-blue dusk sky over Brooklyn rooftops and water towers, "
   "lit apartment windows across the street and a soft glow of the Manhattan skyline in the distance. Inside, warm 2700K practical light "
   "from the table lamps, string lights and candle, pools of amber light on the sofa and table, the cool blue window light rimming the "
   "edges of the room: cinematic warm-and-cool contrast, cosy, ready for a night in. ALL THREE PANELS ARE THREE-QUARTER VIEWS at "
   "standing eye height, 24-28mm lens: PANEL 1 (left): three-quarter view from the window corner looking across the coffee table to the "
   "sofa, with the hallway and green front door visible in the background. PANEL 2 (middle): three-quarter view from the hallway end "
   "looking back across the sofa and coffee table toward the brick wall and the blue-hour windows. PANEL 3 (right): three-quarter view "
   "from behind one end of the sofa looking down across the cushions to the coffee table and the open floor in front of it. Completely "
   "empty of people. Framed posters show only abstract images, no readable text. " + PHOTO),
})
CUSHION = ("ADD ONE NEW ITEM: a large round floor cushion someone can sit on, about 70 cm across and 20 cm thick, in rust-terracotta "
           "velvet with a deep tufted button in the centre and piped edges, lying flat on the rug on the near side of the coffee table, "
           "directly opposite the middle of the sofa, so a person sitting on it would face the sofa across the table. ")
JOBS.update({
 "living-room-master-16x9": (EDIT, [A / "living-room-34-bluehour-v1.png"], "ONE single photorealistic location photograph, NOT a "
   "sheet, NO panels, NO gutters, horizontal 16:9 full frame. EXACTLY the same Brooklyn, New York walk-up living room as image 1, same "
   "furniture, rug, brick, posters, plants, windows and the same locked BLUE HOUR lighting: deep cobalt dusk and the Manhattan skyline "
   "through the windows, warm 2700K lamps, string lights and candle inside. CAMERA: the three-quarter master view of the LEFT panel of "
   "image 1, standing eye height from the window corner, 24mm lens, looking diagonally across the coffee table to the sofa, with the "
   "short hallway and the deep-green front door visible in the background right, the windows on the left edge of frame. " + CUSHION +
   "The cushion is clearly visible in the foreground right of the coffee table. Completely empty of people. Framed posters show only "
   "abstract images, no readable text. " + PHOTO),
 "living-room-34-bluehour-cushion": (EDIT, [A / "living-room-34-bluehour-v1.png"], "Recreate image 1 EXACTLY: the same three-panel "
   "sheet with the same three three-quarter camera views, the same room, furniture, rug, posters and the same locked BLUE HOUR lighting. "
   + CUSHION + "Show it in every panel where that spot is in view, consistently placed and identical in each. Change nothing else. "
   "Completely empty of people. Framed posters show only abstract images, no readable text. " + PHOTO),
})
JOBS.update({
 "cat-grey": (T2I, [], SHEET + GREY + "THE CHARACTER: the apartment's cat, a chunky, confident ginger tabby with bold orange-and-cream "
   "stripes, a white chest and white front paws, bright green eyes, a slightly smug expression and long white whiskers. A real "
   "domestic cat, healthy and well-fed, natural fur texture. PANEL 1 (left): sitting upright facing camera. PANEL 2 (middle): side "
   "profile standing, full body and tail visible. PANEL 3 (right): crouched low, nose forward, sniffing something on the floor. "
   + PHOTO.replace("No people, no hands, ", "No people, no hands, no collar, ")),
})

def go(name):
    out_dir = ROOT / "assets"; out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{name}-v1.png"
    if out.exists(): return f"skip {name}"
    endpoint, refs, prompt = JOBS[name]
    args = {"prompt": prompt, "image_size": WIDE, "quality": "high", "num_images": 1, "output_format": "png"}
    if refs: args["image_urls"] = [fal_client.upload_file(str(r)) for r in refs]
    handle = fal_client.submit(endpoint, arguments=args)
    (out_dir / f"{name}-v1.json").write_text(json.dumps({"endpoint": endpoint, "request_id": handle.request_id,
                                                         "refs": [str(r) for r in refs], "input": args}, indent=1))
    res = handle.get()
    out.write_bytes(requests.get(res["images"][0]["url"], timeout=300).content)
    return f"DONE {name}"

names = sys.argv[1:] or list(JOBS)
with cf.ThreadPoolExecutor(5) as ex:
    for r in ex.map(go, names): print(r, flush=True)
