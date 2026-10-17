#!/usr/bin/env python3
"""Builds the-last-fry-30s-v2.txt and .json: Seedance 2.5 reference-to-video, 480p, 16:9, one clip per shot.
Every clip prompt is self-contained (Seedance sees only the prompt and its references), cites references as @ImageN in
submission order, uses the house template [REFERENCES][CHARACTERS][LOOK][TIMELINE][CAMERA][AUDIO][NEGATIVE], and keeps
~2 s of handle at each end of the beat (FILMS X edit-length rule). Also builds one 15 s multi-shot Mini test of S01-S05."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODEL = "bytedance/seedance-2.5/reference-to-video"
MINI = "bytedance/seedance-2.0-mini/reference-to-video"
SETTINGS = {"resolution": "480p", "ratio": "16:9", "generate_audio": True, "watermark": False, "return_last_frame": True}
RATE = {MODEL: 0.134, MINI: 0.0113}  # $/s at 480p: Atlas list price; Mini measured on FILMS X (15 s = $0.169)

REFS = {  # id: (path relative to production root, what it controls)
 "ROOM": ("assets/living-room-master-16x9-v1.png", "the living room master view: geometry, furniture, blue-hour light"),
 "ROOM3": ("assets/living-room-34-bluehour-cushion-v1.png", "the same living room from three other three-quarter angles"),
 "JALEN": ("characters/jalen-braids/jalen-braids-indoor-v2.png", "Jalen: face, braids, piercings, indoor outfit"),
 "THEO": ("characters/theo-bleach/theo-bleach-indoor-v2.png", "Theo: face, platinum hair, piercings, indoor outfit"),
 "NOVA": ("characters/nova-colour/nova-colour-indoor-v2.png", "Nova: face, pink-lilac hair, piercings, indoor outfit"),
 "PRIYA": ("characters/priya-gloss/priya-gloss-indoor-v2.png", "Priya: face, ponytail with red streaks, gold piercings, indoor outfit"),
 "FRY": ("assets/fry-box-plain-grey-v1.png", "the original plain white takeaway box with a thin red stripe and ONE straight-cut fry"),
 "PHONE": ("assets/phone-place-order-grey-v1.png", "Priya's phone showing the Bolly Eats 'Your basket' screen with the yellow Place order button"),
 "PHONE2": ("assets/brand-phone-order-grey-v1.png", "the same phone showing the Bolly Eats 'Order confirmed' screen"),
 "BAG": ("assets/brand-bag-grey-v1.png", "the Bolly Eats delivery bag (turmeric front, maroon back and sides)"),
 "PACK": ("assets/brand-packaging-grey-v1.png", "Bolly Eats food packaging: maroon meal box, turmeric bowl, full fries box, naan sleeve"),
 "SHAKES": ("assets/brand-shakes-grey-v1.png", "the two Bolly Eats shakes (mango, rose) and their maroon carrier"),
 "FEAST": ("assets/feast-v1.png", "the delivered Indian feast: dishes and how they sit on the coffee table"),
}

CAST = {
 "JALEN": "Jalen, Black man, 28: shoulder-length box braids with honey-blonde ends tied half-up in a top knot, short beard, silver "
          "nose hoop, lip ring, eyebrow bar and stacked ear hoops, layered silver chains, black nail polish; faded oversized black "
          "graphic tee with a grey cracked print, baggy light-wash carpenter jeans, chunky grey-and-cream sneakers.",
 "THEO": "Theo, Korean-American man, 27: messy bleached platinum crop with dark roots, silver bridge bar between the eyes, eyebrow "
         "ring, two studs under the lower lip, silver hoops and a cross earring, ball-chain dog tag; open forest-green chunky "
         "cardigan over a white ribbed tank, baggy black denim jorts, white knee socks with green stripes, black chunky loafers.",
 "NOVA": "Nova, mixed-race woman, 27: shaggy pink-to-lilac wolf cut with curtain bangs and dark roots, freckles, electric-blue "
         "winged liner, silver septum ring, labret stud, eyebrow ring and ear hoops, silver padlock choker; cropped baby-pink tee "
         "with a pink heart, very wide dark indigo jeans with a silver studded belt, black platform boots.",
 "PRIYA": "Priya, Indian-American woman, 29: long black hair in a high sleek ponytail with cherry-red face-framing streaks, gold "
          "septum ring, nose hoop and ear stack with a chain cuff, tiny gold forehead gem, layered gold necklaces and bangles; black "
          "ribbed cropped halter top, khaki parachute cargo pants, white chunky sneakers.",
}
SEATS = ("Fixed for the whole film: Jalen sits on the LEFT end of the oatmeal boucle sofa; Nova sits on the RIGHT end "
         "of the sofa; Theo sits cross-legged on the round rust-velvet floor cushion on the near side of the coffee table, facing "
         "the sofa; Priya sits apart in the brown leather armchair in the front-left corner by the windows. The plain white fry box "
         "starts in the centre of the coffee table. The green front door is at the back right, down the short hallway.")
LOOK = ("Photoreal live-action comedy commercial, 16:9. Brooklyn walk-up living room exactly as @{ROOM}{ROOM3_CITE}: exposed "
        "brick, black sash windows with fire escape, worn oak floor, patterned red-and-navy rug, oatmeal boucle sofa with mustard, "
        "rose, black-and-white checkered and red kilim cushions and a cream knit throw, chunky reclaimed-oak coffee table, brown "
        "leather armchair, round rust-velvet floor cushion, plants, string lights, framed posters. BLUE HOUR, about 7:30 pm, the "
        "same in every shot: deep cobalt dusk and the lit Manhattan skyline through the windows, warm 2700K table lamps, string "
        "lights and a candle inside, warm-and-cool contrast. Fine natural grain, soft halation on practicals, real skin texture. "
        "The friends play a silly fight over one fry with total action-movie seriousness, and nobody speaks.")
NEG = ("NEGATIVE: no dialogue, no talking, no lip movement as speech; no music; no on-screen text, captions, subtitles, chat "
       "bubbles, title cards or UI overlays; no split screen, no collage, no multi-panel layout, never show the reference sheets "
       "themselves; no extra people, no duplicate characters, nobody else enters; no jackets, coats, bags or sunglasses on the "
       "cast; no daylight, no sunset sun, no golden-hour sunlight; no McDonald's or any other real fast-food brand, no golden "
       "arches, no logos except the lowercase 'bolly eats.' marks exactly as referenced; the original fry box stays plain and "
       "unbranded; faces, skin tones, hair colours and outfits never change from the references.")

def cite(ids):
    return {r: f"@Image{i + 1}" for i, r in enumerate(ids)}

def build(shot, model=MODEL):
    ids = shot["refs"]
    c = cite(ids)
    look = LOOK.replace("@{ROOM}", c["ROOM"]).replace("{ROOM3_CITE}", f" and {c['ROOM3']}" if "ROOM3" in c else "")
    ref_lines = "\n".join(f"{c[r]} = {REFS[r][1]}." for r in ids)
    who = [k for k in CAST if k in ids]
    chars = "\n".join(f"{c[k]}: {CAST[k]}" for k in who) if who else "No people in this shot."
    n = len(who)
    count = (f"Exactly {n} {'person' if n == 1 else 'people'} in frame: " + ", ".join(k.title() for k in who) + "."
             if who and not shot.get("partial") else shot.get("count", ""))
    body = "\n\n".join(x for x in [
        f"[REFERENCES]\n{ref_lines}\nUse each character sheet as identity only: one person per sheet, in one single continuous scene.",
        f"[CHARACTERS]\n{chars}\n{count}".strip(),
        "[LOOK]\n" + look,
        "[BLOCKING]\n" + SEATS if who else "",
        "[TIMELINE]\n" + shot["timeline"].format(**c),
        "[CAMERA]\n" + shot["camera"],
        "[AUDIO]\n" + shot["audio"] + " Sound design only, no music, no voices.",
        NEG + (" " + shot["neg"] if shot.get("neg") else ""),
    ] if x)
    payload = {"model": model, "prompt": body, "reference_images": [REFS[r][0] for r in ids], "duration": shot["dur"], **SETTINGS}
    return body, payload

SHOTS = [
 {"id": "S01", "title": "THE LAST FRY", "edit": "00:00-00:03", "beat": 3, "dur": 7, "refs": ["ROOM", "FRY", "JALEN"], "partial": True,
  "count": "Only Jalen's right hand and forearm appear; no faces.",
  "timeline": "0-2 s (handle): close three-quarter top-down view of the plain white box with its thin red stripe ({FRY}) in the "
              "centre of the oak coffee table, ONE golden straight-cut fry lying alone inside, candle glow on the wood, sofa "
              "cushions soft and out of focus behind. Stillness.\n2-5 s (the beat): Jalen's right hand ({JALEN}: silver rings, "
              "black nails, black tee sleeve) slides in slowly from frame left, fingers stretching toward the fry like it is "
              "treasure.\n5-7 s (handle): his fingertips hover two centimetres above the fry and tremble slightly. They never "
              "touch it. Box and fry do not move.",
  "camera": "Locked-off top-down three-quarter angle, 50mm, shallow depth of field, a very slow push-in across the whole clip.",
  "audio": "Quiet room tone, faint city hum through the windows, a tiny paper creak."},
 {"id": "S02", "title": "THE BLOCK", "edit": "00:03-00:06", "beat": 3, "dur": 7, "refs": ["ROOM", "ROOM3", "JALEN", "THEO", "NOVA", "PRIYA", "FRY"],
  "timeline": "0-2 s (handle): wide master. Jalen leans forward from the left end of the sofa, right arm reaching over the coffee "
              "table toward the fry box ({FRY}). Theo on the floor cushion opposite him watches, very still. Nova on the right "
              "end of the sofa holds her breath. Priya sits back in the leather armchair, calm.\n2-5 s (the beat): Theo's left "
              "hand shoots across the table and grips Jalen's right wrist an inch before the fry. Jalen freezes, looks down at the "
              "grip, then slowly up into Theo's eyes. Theo stares back, deadly serious.\n5-7 s (handle): the wrist stays held "
              "above the box. Nova's eyes slide from the two men to the unguarded box. Priya glances down at her phone in her lap.",
  "camera": "Static wide three-quarter master from the window corner, 24mm, matching the framing of the room reference. Everyone, "
            "the table and the box read clearly.",
  "audio": "Room tone; one sharp skin-on-skin grab sound at 2 s; a cushion creak."},
 {"id": "S03", "title": "THE THIEF", "edit": "00:06-00:08", "beat": 2, "dur": 6, "refs": ["ROOM", "JALEN", "THEO", "NOVA", "FRY"],
  "timeline": "0-2 s (handle): table-level medium shot on Nova at the right end of the sofa, the fry box ({FRY}) on the table in "
              "front of her; at frame left, Theo's hand still grips Jalen's wrist.\n2-4 s (the beat): Nova slides the box toward "
              "herself across the tabletop with her right hand, slowly, fifteen centimetres. The single fry stays inside.\n4-6 s "
              "(handle): the paper scrapes. Jalen and Theo turn their heads to her at the same moment, Theo lets go of the wrist, "
              "the two men share a quick allied glance and then glare at Nova. She freezes, hand still on the box, caught.",
  "camera": "Table-height medium shot, 35mm, slight push toward Nova's guilty face in the last two seconds.",
  "audio": "A drawn-out paper-on-wood scrape, then sudden silence."},
 {"id": "S04", "title": "THE RIDICULOUS BATTLE", "edit": "00:08-00:12", "beat": 4, "dur": 8, "refs": ["ROOM", "ROOM3", "JALEN", "THEO", "NOVA", "FRY"],
  "timeline": "Three quick cuts, one continuous fight.\n0-2 s (handle): Nova lets go of the box, it sits upright on the table. Jalen "
              "grabs the checkered cushion from the sofa, Theo snatches the mustard cushion.\n2-3.5 s (cut A): Jalen hurls the "
              "checkered cushion at Theo; Theo blocks it with the mustard cushion held like a shield, a soft thump, a small "
              "recoil, both faces dead serious.\n3.5-5 s (cut B): Nova dives full length along the sofa toward the box, arm "
              "outstretched, and lands face-first in the cushions just short of it, the box untouched.\n5-6 s (cut C): low "
              "close-up over the table: Jalen's and Theo's right hands race toward the box from opposite sides and stop a few "
              "centimetres apart, a frozen standoff.\n6-8 s (handle): hold the standoff, the fry still alone in the upright box.",
  "camera": "Handheld action energy, 24-35mm, punchy cuts at 2 s, 3.5 s and 5 s, always from the window side of the room.",
  "audio": "Cushion whooshes and soft thumps, sofa springs, effort breaths, no voices."},
 {"id": "S05", "title": "THE SMART MOVE", "edit": "00:12-00:15", "beat": 3, "dur": 7, "refs": ["ROOM", "PRIYA", "PHONE", "PHONE2"],
  "partial": True, "count": "Priya is the only person in focus; the fight behind her is a soft blur of movement.",
  "timeline": "0-2 s (handle): over-the-shoulder close shot of Priya in the leather armchair, holding her phone in her left hand. "
              "The screen shows the Bolly Eats 'Your basket' screen exactly as {PHONE}, with the big yellow Place order button. "
              "Behind her, out of focus, cushions fly.\n2-5 s (the beat): she taps Place order once with her right index finger. "
              "The screen changes to the 'Order confirmed' screen exactly as {PHONE2}. A small satisfied smile.\n5-7 s (handle): "
              "she keeps reading, calm, while the blurred fight continues behind her.",
  "camera": "Over-the-shoulder 50mm, shallow focus on the phone and Priya's profile, gentle handheld.",
  "audio": "One soft phone tap, a quiet confirmation chime, muffled thumps of the fight behind.",
  "neg": "The phone screen shows only the two referenced Bolly Eats screens; no other apps, no notifications, no keyboard."},
 {"id": "S06", "title": "LATER: THE INTERRUPTION", "edit": "00:15-00:18", "beat": 3, "dur": 7, "refs": ["ROOM", "JALEN", "THEO", "NOVA", "PRIYA", "FRY"],
  "timeline": "0-2 s (handle): the same wide master, some time later. Cushions are scattered on the rug. Jalen is slumped on the "
              "left of the sofa, Theo sprawled on his floor cushion, both breathing hard but still eyeing the box ({FRY}), the "
              "fry still inside. Nova is crouched at the right end of the sofa, ready for one more try. Priya sits calmly in the "
              "armchair, her phone face-down on the armrest.\n2-4 s (the beat): a doorbell rings from the hallway. All three "
              "fighters freeze and turn their heads toward the green front door.\n4-7 s (handle): Priya stands up and walks "
              "calmly past them toward the hallway.",
  "camera": "Static wide three-quarter master from the window corner, 24mm, the same framing as S02.",
  "audio": "Heavy breathing, one clear apartment doorbell at 2 s, then room tone.",
  "neg": "The 'Later' caption is added in the edit; never write it in the video."},
 {"id": "S07", "title": "THE ENTRANCE", "edit": "00:18-00:20", "beat": 2, "dur": 6, "refs": ["ROOM", "PRIYA", "JALEN", "NOVA", "THEO", "BAG"],
  "timeline": "0-2 s (handle): table-height medium shot. Priya walks back in from the hallway holding exactly two full Bolly "
              "Eats bags ({BAG}), one in each hand by the paper handles, turmeric fronts with the 'bolly eats.' logo facing the "
              "camera.\n2-4 s (the beat): she sets both bags down on a clear part of the oak coffee table; their bases touch the "
              "wood before she lets go. Behind her, out of focus, Jalen, Nova and Theo lean in hopefully.\n4-6 s (handle): the "
              "two closed bags stand on the table; Priya's hands are free.",
  "camera": "Table-height 35mm, slow push toward the bags as they land.",
  "audio": "Paper bag rustle and handle creak, a soft thud as the bags land."},
 {"id": "S08", "title": "THE FEAST REVEAL", "edit": "00:20-00:23", "beat": 3, "dur": 7, "refs": ["ROOM", "FEAST", "PACK", "SHAKES", "FRY"],
  "partial": True, "count": "No people and no hands in this shot.",
  "timeline": "0-2 s (handle): the feast already unpacked on the oak coffee table, matching {FEAST}: a turmeric bowl of butter "
              "chicken with a swirl of cream and coriander, a maroon box of lamb biryani with fried onions, four golden samosas "
              "with green and tamarind dips, garlic naan in a kraft sleeve, a full turmeric box of crinkle-cut masala fries, and "
              "the mango and rose shakes in their maroon carrier ({SHAKES}). Packaging as {PACK}. Soft steam rising.\n2-5 s (the "
              "beat): the camera glides slowly sideways across the food, mouth-watering.\n5-7 s (handle): settle on the whole "
              "spread; at the near corner of the table the plain white fry box ({FRY}) still holds its single fry.",
  "camera": "Table-level 50mm lateral slider move, shallow depth of field, the oatmeal sofa soft behind.",
  "audio": "Gentle paper and lid rustles, faint steam, room tone."},
 {"id": "S09", "title": "PEACE", "edit": "00:23-00:25", "beat": 2, "dur": 6, "refs": ["ROOM", "JALEN", "THEO", "NOVA", "PRIYA", "FEAST", "FRY"],
  "timeline": "0-2 s (handle): the same wide master. All four eat around the feast; cushions still on the rug. The plain white fry "
              "box ({FRY}) sits at the table corner nearest Priya's armchair.\n2-4 s (the beat): Jalen passes Theo a napkin and "
              "Theo nods thanks; Nova bites a samosa and her shoulders drop, happy.\n4-6 s (handle): everyone is absorbed in the "
              "food. Priya, hands free, smiles to herself.",
  "camera": "Static wide three-quarter master from the window corner, 24mm, the same framing as S02 and S06.",
  "audio": "Soft eating sounds, paper rustle, a contented sigh, room tone."},
 {"id": "S10", "title": "THE WINNER", "edit": "00:25-00:27", "beat": 2, "dur": 6, "refs": ["ROOM", "PRIYA", "FRY"],
  "partial": True, "count": "Priya in focus; the other three are soft, out-of-focus shapes eating in the background.",
  "timeline": "0-2 s (handle): medium close-up of Priya in the armchair. The plain white box ({FRY}) is within reach of her right "
              "hand, the single straight-cut fry inside. She glances left and right: the others are busy eating.\n2-4 s (the "
              "beat): she pinches the fry with her right hand, lifts it out cleanly and eats it. The box is now empty.\n4-6 s "
              "(handle): she chews, a tiny victorious smile, not looking at the camera.",
  "camera": "Static medium close-up, 50mm, background soft.",
  "audio": "One crisp, isolated crunch, then room tone."},
]

MINI_TEST = {"id": "TEST-15", "title": "FIRST 15 SECONDS, ONE MULTI-SHOT TAKE", "edit": "00:00-00:15", "beat": 15, "dur": 15,
  "refs": ["ROOM", "ROOM3", "JALEN", "THEO", "NOVA", "PRIYA", "FRY", "PHONE", "PHONE2"],
  "timeline": "Five shots with hard cuts, one continuous story.\n0-3 s: close top-down three-quarter view of the plain white fry box "
              "({FRY}) alone in the centre of the oak coffee table with ONE straight-cut fry inside; Jalen's ringed right hand "
              "slides in from frame left and hovers above it without touching.\n3-6 s: static wide master from the window corner. "
              "Theo, on the floor cushion opposite, grips Jalen's wrist across the table an inch before the fry; they lock eyes, "
              "deadly serious. Nova watches from the right end of the sofa; Priya sits calmly in the armchair.\n6-8 s: "
              "table-level medium shot: Nova quietly slides the box toward herself; both men snap their heads to her and glare; "
              "she freezes, caught.\n8-12 s: quick handheld action cuts: Jalen throws the checkered cushion, Theo blocks it with "
              "the mustard cushion; Nova dives along the sofa and lands short of the box; Jalen's and Theo's hands race for the "
              "box and stop in a standoff. The box stays upright, the fry untouched.\n12-15 s: over-the-shoulder close shot of "
              "Priya in the armchair: her phone shows the Bolly Eats 'Your basket' screen ({PHONE}); she taps the yellow Place "
              "order button and it changes to 'Order confirmed' ({PHONE2}); a small satisfied smile while the fight blurs behind her.",
  "camera": "Cuts at 3, 6, 8 and 12 s. Every angle is taken from the window side of the room; the wide shot matches the room reference framing.",
  "audio": "Room tone, a grab sound, a paper scrape, cushion thumps and effort breaths, one soft phone tap and chime."}

SHARED = """BOLLY EATS · THE LAST FRY · 30-SECOND AD · PROMPT PACK v2
Built by prompts/build_pack_v2.py (edit the script, not this file). Replaces v1.

MODEL AND SETTINGS (every clip)
Seedance 2.5 reference-to-video on Atlas Cloud ({model}), resolution 480p, ratio 16:9, generate_audio true, watermark false,
return_last_frame true. Upscale picked takes locally with Topaz Rhea (pipeline/upscale_rhea_4k.sh); never pay for -sr/-esr.

WHAT CHANGED FROM v1
- Room: the Brooklyn blue-hour apartment (assets/living-room-master-16x9-v1.png + the 3-angle cushion sheet). v1's sunny loft
  (teal sofa, cream armchair, late-afternoon light) is retired; the cast sheets, feast sheet and blocking were all made for this room.
- No start frames. References are the locked asset sheets only (house rule: never storyboard frames), cited @Image1..N in order.
- Blocking re-mapped to this room (blocking/blocking-plan.png): Jalen sofa-left, Nova sofa-right, Theo on the rust floor
  cushion opposite (so his wrist-grab works across the table), Priya apart in the leather armchair. Roles unchanged.
- Each clip prompt is complete on its own and uses the [REFERENCES][CHARACTERS][LOOK][BLOCKING][TIMELINE][CAMERA][AUDIO]
  [NEGATIVE] template with second stamps, which Seedance follows more closely than prose.
- Durations include ~2 s of handle before and after each beat, so every cut has trimming room.
- Phone shots use the generated phone sheets that already carry the Bolly Eats screens; replace the screen in post only if the
  480p lettering drifts.
- Audio: sound design only. Music is scored in the edit (music in prompts can trip Seedance's audio copyright block).
- Negatives ban competitor fast-food marks by name (Seedance once put golden arches on generic cups), on-screen text,
  collages of the reference sheets, extra people and daylight.
- Dropped the v1 instruction about Jalen's eyebrow (the sheet is accepted as it is).

EDIT PLAN (final 30 s)
S01 0-3 · S02 3-6 · S03 6-8 · S04 8-12 · S05 12-15 · S06 15-18 (add 'Later...' in the edit) · S07 18-20 · S08 20-23 ·
S09 23-25 · S10 25-27 · S11 27-30 = brand/brand-card-16x9.png held 3 s (no generation; optional VO 'Bolly Eats. Peace, delivered.').
"""

def main():
    txt = [SHARED.format(model=MODEL)]
    out = {"model": MODEL, "settings": SETTINGS, "production_root": str(ROOT), "clips": [], "mini_test": None}
    total = 0
    for s in SHOTS:
        body, payload = build(s)
        cost = round(s["dur"] * RATE[MODEL], 2); total += s["dur"]
        txt.append(f"\n{'=' * 100}\n{s['id']} · {s['title']} · edit {s['edit']} ({s['beat']} s beat) · generate {s['dur']} s · "
                   f"~${cost:.2f}\nREFERENCE FILES (upload in this order):\n" +
                   "\n".join(f"  @Image{i + 1}  {REFS[r][0]}" for i, r in enumerate(s["refs"])) + f"\n\nPROMPT:\n{body}\n")
        out["clips"].append({"id": s["id"], "title": s["title"], "edit": s["edit"], "est_cost_usd": cost, "payload": payload})
    body, payload = build(MINI_TEST, MINI)
    out["mini_test"] = {"id": MINI_TEST["id"], "est_cost_usd": round(15 * RATE[MINI], 2), "payload": payload}
    txt.append(f"\n{'=' * 100}\nTOTAL to generate S01-S10 once on Seedance 2.5 at 480p: {total} s ≈ ${total * RATE[MODEL]:.2f}\n")
    txt.append(f"\n{'=' * 100}\nTEST · {MINI_TEST['title']} · Seedance 2.0 Mini ({MINI}), 480p 16:9, 15 s · "
               f"~${15 * RATE[MINI]:.2f}\nREFERENCE FILES:\n" +
               "\n".join(f"  @Image{i + 1}  {REFS[r][0]}" for i, r in enumerate(MINI_TEST["refs"])) + f"\n\nPROMPT:\n{body}\n")
    (HERE / "the-last-fry-30s-v2.txt").write_text("".join(txt))
    (HERE / "the-last-fry-30s-v2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    missing = [p for p, _ in REFS.values() if not (ROOT / p).exists()]
    print("built v2;", len(SHOTS), "clips,", total, "s; missing refs:", missing or "none")

if __name__ == "__main__":
    main()
