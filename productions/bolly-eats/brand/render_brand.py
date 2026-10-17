#!/usr/bin/env python3
"""Bolly Eats brand graphics rendered from HTML (exact type and colours, no AI).
Source of truth: the Bolly Eats Branding canvas https://claude.ai/artifact/QrVPY2WRx9GyE2Z8Z8YbPt
Usage: render_brand.py [artboard_dir]  (artboard_dir holds the canvas's Bag.dc.html / Holder.dc.html for the reference renders)"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
CHROME = str(Path.home() / ".cache/puppeteer/chrome/mac_arm-146.0.7680.76/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800'
         '&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">')
MASALA, TURMERIC, CHILLI, ROSE, CREAM, INK, SAND = "#5B1A1F", "#F4B400", "#E2462B", "#E8889A", "#FFF4E0", "#3A0F14", "#F2D9B8"

def steam(color, w=96, sw=5):
    return (f'<svg width="{w}" height="{w//2}" viewBox="0 0 96 48" fill="none" stroke="{color}" stroke-width="{sw}" '
            'stroke-linecap="round"><path d="M18 44c-8-8 8-14 0-22s8-14 0-20"/><path d="M48 44c-8-8 8-14 0-22s8-14 0-20"/>'
            '<path d="M78 44c-8-8 8-14 0-22s8-14 0-20"/></svg>')

def page(body, bg="transparent"):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>html,body{{margin:0;background:{bg}}}'
            ".h{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-0.05em;line-height:.82}"
            f"*{{box-sizing:border-box}}body{{font-family:'DM Sans',sans-serif;color:{INK}}}</style></head><body>{body}</body></html>")

def logo(fg, accent):
    return (f'<div style="width:1600px;height:900px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px">'
            f'{steam(accent, 240, 5)}<div class="h" style="font-size:300px;color:{fg};text-align:center">bolly<br>'
            f'<span style="color:{accent}">eats.</span></div></div>')

ORDER_ITEMS = [("Butter chicken", "1"), ("Lamb biryani", "1"), ("Vegetable samosas", "4"), ("Garlic naan", "2"),
               ("Masala fries", "1"), ("Mango Masala Shake", "1"), ("Rose Falooda Shake", "1")]
order_rows = "".join(f'<div style="display:flex;justify-content:space-between;padding:26px 0;border-bottom:2px solid #EAD8BC;font-size:40px">'
                     f'<span>{n}</span><span style="font-weight:700">×{q}</span></div>' for n, q in ORDER_ITEMS)
steps = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:16px;width:220px">'
                f'<div style="width:56px;height:56px;border-radius:50%;background:{TURMERIC if i < 2 else "#EAD8BC"};'
                f'border:6px solid {MASALA if i < 2 else "#EAD8BC"}"></div><div style="font-size:30px;font-weight:{700 if i < 2 else 500};'
                f'text-align:center">{s}</div></div>' for i, s in enumerate(["Confirmed", "Cooking", "On the way", "Delivered"]))
ORDER = (f'<div style="width:1080px;height:2340px;background:{CREAM};display:flex;flex-direction:column">'
         f'<div style="background:{MASALA};color:{CREAM};padding:170px 80px 90px;display:flex;flex-direction:column;align-items:center;gap:30px">'
         f'{steam(TURMERIC, 150, 5)}<div class="h" style="font-size:120px;text-align:center">bolly <span style="color:{TURMERIC}">eats.</span></div>'
         f'<div style="margin-top:50px;width:170px;height:170px;border-radius:50%;background:{TURMERIC};display:flex;align-items:center;justify-content:center">'
         f'<svg width="96" height="96" viewBox="0 0 24 24" fill="none" stroke="{MASALA}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>'
         f'<div class="h" style="font-size:96px;letter-spacing:-0.03em;line-height:1">Order confirmed</div>'
         f'<div style="font-size:42px;color:{SAND};text-align:center">Your feast is on its way.</div></div>'
         f'<div style="padding:70px 80px 0;display:flex;flex-direction:column;gap:50px;flex-grow:1">'
         f'<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-size:36px;font-weight:700;letter-spacing:.16em;text-transform:uppercase">Arriving in</span>'
         f'<span class="h" style="font-size:110px;color:{CHILLI};letter-spacing:-0.03em">25 min</span></div>'
         f'<div style="display:flex;justify-content:space-between">{steps}</div>'
         f'<div><div style="font-size:30px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;margin-bottom:10px">Your order</div>{order_rows}</div></div>'
         f'<div style="margin:0 80px 110px;background:{MASALA};color:{CREAM};border-radius:999px;padding:40px;text-align:center;font-size:42px;font-weight:700">Track your rider</div></div>')

CART_ITEMS = ORDER_ITEMS
cart_rows = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:24px 0;border-bottom:2px solid #EAD8BC;font-size:40px">'
                    f'<span>{n}</span><span style="display:flex;align-items:center;gap:22px;font-weight:700">'
                    f'<span style="width:56px;height:56px;border-radius:50%;border:3px solid {MASALA};display:flex;align-items:center;justify-content:center;font-size:36px">−</span>{q}'
                    f'<span style="width:56px;height:56px;border-radius:50%;background:{MASALA};color:{CREAM};display:flex;align-items:center;justify-content:center;font-size:36px">+</span></span></div>'
                    for n, q in CART_ITEMS)
CART = (f'<div style="width:1080px;height:2340px;background:{CREAM};display:flex;flex-direction:column">'
        f'<div style="background:{MASALA};color:{CREAM};padding:150px 80px 70px;display:flex;flex-direction:column;gap:26px">'
        f'<div style="display:flex;align-items:center;gap:20px">{steam(TURMERIC, 90, 6)}<div class="h" style="font-size:72px">bolly <span style="color:{TURMERIC}">eats.</span></div></div>'
        f'<div class="h" style="font-size:110px;letter-spacing:-0.03em;line-height:1;margin-top:30px">Your basket</div>'
        f'<div style="font-size:40px;color:{SAND}">Feast for four · 7 items</div></div>'
        f'<div style="padding:50px 80px 0;flex-grow:1">{cart_rows}'
        f'<div style="display:flex;justify-content:space-between;margin-top:50px;font-size:38px"><span style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:30px">Deliver to</span><span>Home · about 25 min</span></div></div>'
        f'<div style="margin:0 80px 110px;background:{TURMERIC};color:{MASALA};border-radius:999px;padding:46px;text-align:center" class="h"><span style="font-size:64px;letter-spacing:-0.02em">Place order</span></div></div>')

def card(w, h, logo_px, line_px):
    return (f'<div style="width:{w}px;height:{h}px;background:{MASALA};color:{CREAM};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{line_px}px">'
            f'{steam(TURMERIC, int(logo_px * 0.9), 5)}<div class="h" style="font-size:{logo_px}px;text-align:center">bolly<br><span style="color:{TURMERIC}">eats.</span></div>'
            f'<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:500;font-size:{line_px}px;letter-spacing:-0.01em">Peace, delivered.</div>'
            f'<div style="background:{TURMERIC};color:{MASALA};border-radius:999px;padding:{line_px*0.45:.0f}px {line_px*1.1:.0f}px;font-weight:700;font-size:{line_px*0.6:.0f}px">'
            f'Order now on the Bolly Eats app</div></div>')

def artboard(path):
    src = Path(path).read_text()
    helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
    body = re.search(r"<x-dc>(.*?)</x-dc>", src, re.S).group(1).replace(re.search(r"<helmet>.*?</helmet>", src, re.S).group(0), "")
    return f'<!doctype html><html><head><meta charset="utf-8">{helmet}</head><body>{body}</body></html>'

JOBS = {  # name: (html, width, height, transparent)
    "bolly-logo-masala": (page(logo(MASALA, CHILLI)), 1600, 900, True),
    "bolly-logo-on-masala": (page(logo(CREAM, TURMERIC), MASALA), 1600, 900, False),
    "bolly-logo-on-turmeric": (page(logo(MASALA, MASALA), TURMERIC), 1600, 900, False),
    "order-confirmation-screen": (page(ORDER, CREAM), 1080, 2340, False),
    "order-cart-screen": (page(CART, CREAM), 1080, 2340, False),
    "brand-card-16x9": (page(card(1920, 1080, 230, 64), MASALA), 1920, 1080, False),
    "brand-card-9x16": (page(card(1080, 1920, 250, 62), MASALA), 1080, 1920, False),
}
if len(sys.argv) > 1:
    d = Path(sys.argv[1])
    JOBS["ref-bag-design"] = (artboard(d / "Bag.dc.html"), 1200, 1100, False)
    JOBS["ref-shake-carrier-design"] = (artboard(d / "Holder.dc.html"), 1200, 900, False)
    JOBS["ref-shake-cups-design"] = (artboard(d / "Shake.dc.html"), 1000, 900, False)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    for name, (html, w, h, clear) in JOBS.items():
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.set_content(html, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(OUT / f"{name}.png"), omit_background=clear)
        pg.close()
        print("rendered", name)
    b.close()
