#!/usr/bin/env python3
"""Zeichnet die Warnsymbole (DDS) und das Vorschaubild der Mod (PNG). Benötigt Pillow.

    python3 werkzeuge/erzeuge_grafiken.py
"""

import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WURZEL = Path(__file__).resolve().parent.parent
SYMBOL_GROESSE = 64
UEBERABTASTUNG = 4

FARBEN = {
    "kritisch": (196, 40, 40),
    "warnung": (222, 160, 30),
    "tipp": (52, 150, 72),
}


def schreibe_dds(bild, pfad):
    """Unkomprimiertes 32-Bit-DDS (A8R8G8B8) ohne Mipmaps, das jede Paradox-Engine liest."""
    bild = bild.convert("RGBA")
    breite, hoehe = bild.size
    kopf = struct.pack(
        "<4sIIIIIII44xIIIIIIIIIIIII",
        b"DDS ",
        124,                          # Größe des Kopfes
        0x1 | 0x2 | 0x4 | 0x8 | 0x1000,  # CAPS | HEIGHT | WIDTH | PITCH | PIXELFORMAT
        hoehe,
        breite,
        breite * 4,                   # Bytes je Zeile
        0,                            # Tiefe
        0,                            # Mipmaps
        32,                           # Größe des Pixelformats
        0x1 | 0x40,                   # ALPHAPIXELS | RGB
        0,                            # FourCC
        32,                           # Bits je Pixel
        0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000,
        0x1000,                       # CAPS: TEXTURE
        0, 0, 0, 0,
    )
    r, g, b, a = bild.split()
    daten = Image.merge("RGBA", (b, g, r, a)).tobytes()
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_bytes(kopf + daten)
    print(f"  {pfad.relative_to(WURZEL)}")


def symbol(art):
    """Runde Plakette in der Farbe der Stufe mit „!“ (Problem) oder „i“ (Tipp)."""
    g = SYMBOL_GROESSE * UEBERABTASTUNG
    bild = Image.new("RGBA", (g, g), (0, 0, 0, 0))
    z = ImageDraw.Draw(bild)
    rand = g * 0.04
    z.ellipse((rand, rand, g - rand, g - rand), fill=(30, 26, 22, 255))
    innen = g * 0.10
    z.ellipse((innen, innen, g - innen, g - innen), fill=FARBEN[art] + (255,))
    weiss = (250, 246, 236, 255)
    mitte = g / 2
    halb = g * 0.065
    if art == "tipp":
        z.ellipse((mitte - halb * 1.2, g * 0.24, mitte + halb * 1.2, g * 0.24 + halb * 2.4), fill=weiss)
        z.rounded_rectangle((mitte - halb, g * 0.42, mitte + halb, g * 0.76), radius=halb * 0.5, fill=weiss)
    else:
        z.rounded_rectangle((mitte - halb, g * 0.22, mitte + halb, g * 0.60), radius=halb * 0.5, fill=weiss)
        z.ellipse((mitte - halb * 1.2, g * 0.66, mitte + halb * 1.2, g * 0.66 + halb * 2.4), fill=weiss)
    return bild.resize((SYMBOL_GROESSE, SYMBOL_GROESSE), Image.LANCZOS)


def schrift(datei, groesse):
    """Systemschrift mit Umlauten; sonst die eingebaute Schrift von Pillow."""
    for ordner in ("/usr/share/fonts/truetype/dejavu", "C:/Windows/Fonts", "/Library/Fonts"):
        pfad = Path(ordner) / datei
        if pfad.exists():
            return ImageFont.truetype(str(pfad), groesse)
    return ImageFont.load_default(size=groesse)


def vorschaubild():
    breite = hoehe = 512
    bild = Image.new("RGB", (breite, hoehe), (28, 34, 52))
    z = ImageDraw.Draw(bild)
    for y in range(hoehe):
        t = y / hoehe
        z.line((0, y, breite, y), fill=(int(28 + 20 * t), int(34 + 14 * t), int(52 - 10 * t)))
    z.rectangle((24, 24, breite - 24, hoehe - 24), outline=(196, 164, 92), width=6)
    for i, art in enumerate(("kritisch", "warnung", "tipp")):
        s = symbol(art).resize((112, 112), Image.LANCZOS)
        bild.paste(s, (72 + i * 132, 96), s)
    gold = (232, 204, 128)
    titel = schrift("DejaVuSerif-Bold.ttf", 72)
    unter = schrift("DejaVuSans.ttf", 30)
    z.text((breite / 2, 320), "BERATER", font=titel, fill=gold, anchor="mm")
    z.text((breite / 2, 400), "Live-Ratschläge für Victoria 3", font=unter, fill=(220, 220, 228), anchor="mm")
    bild.save(WURZEL / "thumbnail.png")
    print("  thumbnail.png")


def main():
    print("Schreibe Grafiken:")
    for art in FARBEN:
        schreibe_dds(symbol(art), WURZEL / f"gfx/interface/icons/berater/berater_{art}.dds")
    vorschaubild()


if __name__ == "__main__":
    main()
