#!/usr/bin/env python3
"""v3 opening (00-15 s) of Bolly Eats 'The Last Fry': the polite offer, the wrist grab, the box slides away from Nova,
the cushion fight, the cat eats the fry, the stomach growl. One 15 s multi-shot take on Seedance 2.5, 480p, 16:9.
Reuses the v2 references, cast, look and negatives; adds the cat and the seating fixes from the Mini test.
Writes the-last-fry-v3-open15.txt and .json (pipeline/atlas_run.py <json> OPEN-15 runs it)."""
import json
import build_pack_v2 as v2

v2.REFS["CAT"] = ("assets/cat-grey-v1.png", "the apartment's cat: a chunky ginger tabby with a white chest and white paws")
v2.SEATS = ("Fixed for the whole film. Jalen sits on the LEFT end of the oatmeal boucle sofa. Nova SITS on the RIGHT end of the "
            "sofa, she never stands. Theo sits cross-legged ON THE ROUND RUST-VELVET FLOOR CUSHION on the near side of the coffee "
            "table, facing the sofa and facing Jalen across the table; Theo is NEVER on the sofa. Priya sits apart in the brown "
            "leather armchair in the front-left corner by the windows. The plain white fry box is on the coffee table between "
            "them. The green front door is at the back right, down the short hallway.")
v2.NEG += (" No magazines, books or printed paper with writing on the table. The only food on screen is the single fry; the cat "
           "is the only animal.")

OPEN = {"id": "OPEN-15", "title": "THE POLITE OFFER TO THE STOMACH GROWL", "edit": "00:00-00:15", "beat": 15, "dur": 15,
 "refs": ["ROOM", "ROOM3", "JALEN", "THEO", "NOVA", "PRIYA", "FRY", "CAT"],
 "timeline": "Six shots joined by hard cuts, one continuous scene, no time jumps.\n"
  "0-3 s, THE POLITE OFFER: static wide master from the window corner. Dinner is over: a few crumpled napkins on the coffee "
  "table. Theo, on the floor cushion, slides the plain white fry box ({FRY}) with its ONE straight-cut fry into the middle of "
  "the table and opens both palms: anyone? Jalen, Nova and Priya each raise a hand and politely wave it away with gracious "
  "smiles. A beat of awkward stillness.\n"
  "3-5 s, THE GRAB: close shot over the table. Jalen's ringed right hand darts at the box; Theo's hand clamps Jalen's wrist an "
  "inch from the fry. Cut to the two of them locking eyes across the table, deadly serious.\n"
  "5-7 s, IT GETS AWAY: medium shot. Nova lunges from her seat on the right of the sofa and stretches for the box; just as her "
  "fingertips arrive, Theo slides the box away across the tabletop and she grabs empty air.\n"
  "7-10 s, PILLOW WAR: handheld wide. Total chaos: Jalen swings the black-and-white checkered cushion at Theo, Theo blocks with "
  "the mustard cushion, Nova hurls the rose cushion, cushions bounce and fly. Priya, in the armchair, leans calmly out of the way "
  "of a stray cushion without looking up. The fry box stays upright on the table, the fry still inside.\n"
  "10-12.5 s, THE CAT: low table-level shot. The ginger tabby cat ({CAT}) hops up onto the coffee table, strolls to the box, "
  "sniffs, takes the single fry in its mouth and eats it. In the background the three fighters freeze mid-swing; a cushion "
  "drops to the floor.\n"
  "12.5-15 s, THE GROWL: static wide master again. Total stillness. All four stare at the cat as it licks its lips and sits "
  "down smugly on the table next to the empty box. A long, loud stomach growl; the friends slowly look down at their bellies, "
  "then at each other.",
 "camera": "Cuts at 3, 5, 7, 10 and 12.5 s. Every angle is from the window side of the room. Both wide shots match the framing "
           "of the room reference @Image1. Close and table-level shots use 35-50mm with shallow depth of field.",
 "audio": "Room tone; a paper slide; a sharp wrist-grab; a squeak of the box sliding away; cushion whooshes, thumps and sofa "
          "springs; a soft cat landing and tiny crunch; dead silence; then one long, loud stomach growl."}

body, payload = v2.build(OPEN, v2.MODEL)
cost = round(OPEN["dur"] * v2.RATE[v2.MODEL], 2)
pack = {"model": v2.MODEL, "settings": v2.SETTINGS, "production_root": str(v2.ROOT),
        "clips": [{"id": OPEN["id"], "title": OPEN["title"], "edit": OPEN["edit"], "est_cost_usd": cost, "payload": payload}]}
(v2.HERE / "the-last-fry-v3-open15.json").write_text(json.dumps(pack, indent=1, ensure_ascii=False))
(v2.HERE / "the-last-fry-v3-open15.txt").write_text(
    f"BOLLY EATS · THE LAST FRY · v3 OPENING · {OPEN['title']}\nSeedance 2.5 reference-to-video · 480p · 16:9 · 15 s · ~${cost}\n"
    "Story change from v2: the polite offer starts the fight and the CAT eats the fry, so v2's S10 ending (Priya eats it) is void.\n\n"
    "REFERENCE FILES (upload in this order):\n" +
    "\n".join(f"  @Image{i + 1}  {v2.REFS[r][0]}" for i, r in enumerate(OPEN["refs"])) + f"\n\nPROMPT:\n{body}\n")
print("built v3 open15:", len(body), "chars,", len(payload["reference_images"]), "refs, ~$", cost)
