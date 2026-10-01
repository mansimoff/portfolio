#!/usr/bin/env python3
"""
make_placeholder.py — генерирует картинку-заглушку с подписью, пока нет
реального фото/скана сертификата. Держит макет аккуратным, не "битой иконкой".

Использование:
    python scripts/make_placeholder.py static/assets/projects/new.jpg "New Project" 800 600
    python scripts/make_placeholder.py static/assets/certificates/it-2.jpg "IT course" 500 500
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

path, label = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 800
h = int(sys.argv[4]) if len(sys.argv) > 4 else 600

img = Image.new("RGB", (w, h), "#e6ddd0")
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, w - 1, h - 1], outline="#7a2e3a", width=3)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(14, w // 22))
except OSError:
    font = ImageFont.load_default()
text = f"TODO: {label}"
bbox = draw.textbbox((0, 0), text, font=font)
draw.text(((w - (bbox[2] - bbox[0])) / 2, (h - (bbox[3] - bbox[1])) / 2), text, fill="#7a2e3a", font=font)

Path(path).parent.mkdir(parents=True, exist_ok=True)
img.save(path, quality=85)
print(f"OK: {path}")
