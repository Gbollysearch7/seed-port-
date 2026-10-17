#!/usr/bin/env python3
"""Bolly Eats blocking diagram: top-down floor plan of the Brooklyn living room with the four friends, the master camera and
the delivery move. Rendered from SVG to blocking-plan.png (1920x1080). Geometry follows assets/living-room-34-bluehour-v1.png:
windows on the west wall, brick wall with posters to the north, hallway and green front door at the north-east."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
CHROME = str(Path.home() / ".cache/puppeteer/chrome/mac_arm-146.0.7680.76/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
MASALA, TURMERIC, CHILLI, ROSE, CREAM, INK, OAK, RUG = "#5B1A1F", "#F4B400", "#E2462B", "#E8889A", "#FFF4E0", "#3A0F14", "#B88A5A", "#E9C9B0"

def person(x, y, face_deg, color, initial, name, name_dy=66):
    # circle + facing wedge; face_deg 0 = facing up (north), clockwise
    return (f'<g transform="translate({x},{y})"><g transform="rotate({face_deg})"><path d="M0,-58 L-20,-30 L20,-30 Z" fill="{color}"/></g>'
            f'<circle r="34" fill="{color}" stroke="{INK}" stroke-width="4"/>'
            f'<text y="12" text-anchor="middle" font-size="34" font-weight="800" fill="{INK}">{initial}</text></g>'
            f'<text x="{x}" y="{y + name_dy}" text-anchor="middle" font-size="26" font-weight="800" fill="{INK}">{name}</text>')

SVG = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080" font-family="DM Sans, sans-serif">
 <rect width="1920" height="1080" fill="{CREAM}"/>

 <!-- room shell -->
 <g transform="translate(90,220)">
  <rect x="0" y="0" width="1100" height="780" fill="#FBEBD3" stroke="{INK}" stroke-width="10"/>
  <rect x="0" y="-12" width="880" height="24" fill="#A4523A"/>
  <text x="440" y="-26" text-anchor="middle" font-size="20" font-weight="700" fill="{INK}" letter-spacing="2">BRICK WALL · POSTERS · RECORD SHELF</text>
  <rect x="-14" y="110" width="28" height="200" fill="#6D8FC7"/><rect x="-14" y="400" width="28" height="200" fill="#6D8FC7"/>
  <text x="-40" y="360" font-size="20" font-weight="700" fill="{INK}" letter-spacing="2" transform="rotate(-90,-40,360)" text-anchor="middle">WINDOWS · FIRE ESCAPE · BLUE-HOUR SKY</text>
  <rect x="880" y="-150" width="220" height="162" fill="#FBEBD3" stroke="{INK}" stroke-width="10"/>
  <rect x="930" y="-162" width="120" height="24" fill="#2F4A3A"/>
  <text x="990" y="-176" text-anchor="middle" font-size="20" font-weight="700" fill="{INK}" letter-spacing="2">GREEN FRONT DOOR</text>
  <text x="990" y="-60" text-anchor="middle" font-size="20" fill="{INK}">hallway</text>

  <rect x="150" y="150" width="760" height="540" rx="6" fill="{RUG}" stroke="#C99877" stroke-width="4" stroke-dasharray="14 8"/>
  <rect x="250" y="60" width="560" height="200" rx="34" fill="#E8DCC6" stroke="{INK}" stroke-width="5"/>
  <rect x="250" y="60" width="560" height="44" rx="20" fill="#D9CBB1" stroke="{INK}" stroke-width="3"/>
  <text x="530" y="90" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}" letter-spacing="2">SOFA</text>
  <rect x="60" y="560" width="130" height="130" rx="22" fill="#7A4A32" stroke="{INK}" stroke-width="5"/>
  <text x="125" y="676" text-anchor="middle" font-size="15" font-weight="700" fill="{CREAM}">ARMCHAIR</text>
  <rect x="360" y="320" width="340" height="190" rx="8" fill="{OAK}" stroke="{INK}" stroke-width="5"/>
  <text x="530" y="492" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}" letter-spacing="2">COFFEE TABLE</text>
  <rect x="512" y="388" width="36" height="36" fill="#FFFFFF" stroke="{CHILLI}" stroke-width="4"/>
  <text x="562" y="413" font-size="20" font-weight="700" fill="{CHILLI}">the last fry</text>
  <circle cx="700" cy="600" r="54" fill="#B5532E" stroke="{INK}" stroke-width="5"/>
  <text x="770" y="606" font-size="18" fill="{INK}">floor cushion</text>

  {person(380, 150, 165, TURMERIC, "J", "Jalen", 95)}
  {person(690, 150, 195, ROSE, "N", "Nova", 95)}
  {person(700, 600, -25, "#7FA88C", "T", "Theo", 88)}
  {person(125, 600, 60, "#C9A27A", "P", "Priya", -48)}

  <path d="M200,590 C320,530 820,530 905,420 C960,320 960,120 975,-20" fill="none" stroke="{CHILLI}" stroke-width="6" stroke-dasharray="16 10"/>
  <path d="M978,-36 l-18,26 l26,4 Z" fill="{CHILLI}"/>
  <text x="925" y="297" text-anchor="end" font-size="18" font-weight="700" fill="{CHILLI}">Priya → door (S06), back with the bags (S07)</text>

  <g transform="translate(60,730) rotate(45)">
   <path d="M0,0 L-150,-420 M0,0 L150,-420" stroke="{MASALA}" stroke-width="3" stroke-dasharray="6 8" fill="none" opacity="0.6"/>
   <rect x="-30" y="-20" width="60" height="44" rx="8" fill="{MASALA}"/>
   <path d="M-14,-20 L-24,-40 L24,-40 L14,-20 Z" fill="{MASALA}"/>
  </g>
  <text x="10" y="820" font-size="20" font-weight="800" fill="{MASALA}">CAM A · master 3/4 · 24mm, from the window corner</text>
 </g>

 <g transform="translate(1290,96)">
  <text x="0" y="0" font-family="Bricolage Grotesque, sans-serif" font-size="58" font-weight="800" fill="{INK}" letter-spacing="-1.5">Blocking</text>
  <text x="0" y="58" font-family="Bricolage Grotesque, sans-serif" font-size="40" font-weight="800" fill="{INK}">the living room, top-down</text>
  <text x="0" y="100" font-size="22" fill="{INK}">Blue hour, about 7:30 pm · Bolly Eats "Peace, delivered"</text>
  <text x="0" y="190" font-family="Bricolage Grotesque, sans-serif" font-size="34" font-weight="800" fill="{INK}">Who sits where</text>
  <g font-size="23" fill="{INK}">
   <circle cx="20" cy="236" r="16" fill="{TURMERIC}" stroke="{INK}" stroke-width="3"/><text x="50" y="244"><tspan font-weight="800">Jalen</tspan> · sofa left · claims the fry</text>
   <circle cx="20" cy="286" r="16" fill="{ROSE}" stroke="{INK}" stroke-width="3"/><text x="50" y="294"><tspan font-weight="800">Nova</tspan> · sofa right · steals the box</text>
   <circle cx="20" cy="336" r="16" fill="#7FA88C" stroke="{INK}" stroke-width="3"/><text x="50" y="344"><tspan font-weight="800">Theo</tspan> · floor cushion · blocks Jalen</text>
   <circle cx="20" cy="386" r="16" fill="#C9A27A" stroke="{INK}" stroke-width="3"/><text x="50" y="394"><tspan font-weight="800">Priya</tspan> · armchair · orders, wins</text>
  </g>
  <text x="0" y="480" font-family="Bricolage Grotesque, sans-serif" font-size="34" font-weight="800" fill="{INK}">Why this works</text>
  <g font-size="22" fill="{INK}">
   <text x="0" y="524">The fry sits dead centre between the three fighters.</text>
   <text x="0" y="560">Theo faces Jalen across the table: he can catch</text>
   <text x="0" y="590">Jalen's wrist without anyone standing up.</text>
   <text x="0" y="626">Priya sits apart, out of the fight, phone in hand,</text>
   <text x="0" y="656">and nearest the fry box at the end (S09–S10).</text>
   <text x="0" y="692">Wedges show which way each person faces.</text>
  </g>
 </g>
</svg>"""

HTML = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
        'opsz,wght@12..96,800&family=DM+Sans:wght@400;700;800&display=swap" rel="stylesheet"><style>html,body{margin:0}</style>'
        f'</head><body>{SVG}</body></html>')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.set_content(HTML, wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(OUT / "blocking-plan.png"))
    b.close()
print("rendered", OUT / "blocking-plan.png")
