from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import random

app = Flask(__name__)

# Pre-load fonts (with fallbacks)
def get_font(size):
    font_paths = [
        "fonts/impact.ttf", "fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "impact.ttf", "arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

@app.route('/')
def home():
    return "<h1>Imgen Logo Maker</h1><p>Use: /logo?text=YOUR+TEXT</p>"

@app.route('/logo')
def logo():
    text = request.args.get('text', 'AS MASTI WORLD').upper().strip()
    if len(text) > 30:
        text = text[:27] + "..."

    # Base image
    img = Image.new('RGB', (1080, 1080), (10, 0, 30))
    draw = ImageDraw.Draw(img)

    # 1. Background lightning pattern (procedural)
    for _ in range(80):
        x1 = random.randint(0, 1080)
        y1 = random.randint(0, 1080)
        x2 = x1 + random.randint(-200, 200)
        y2 = y1 + random.randint(-200, 200)
        draw.line((x1, y1, x2, y2), fill=(100, 0, 200, 180), width=random.randint(2, 6))
    
    # Blur for glow effect
    img = img.filter(ImageFilter.GaussianBlur(3))

    # 2. Scattered background text (repeated, semi-transparent)
    bg_font = get_font(80)
    for _ in range(12):
        angle = random.randint(-40, 40)
        temp = Image.new('RGBA', (1080, 1080), (0,0,0,0))
        tdraw = ImageDraw.Draw(temp)
        tw, th = tdraw.textsize(text, font=bg_font)
        x = random.randint(0, 1080 - tw)
        y = random.randint(0, 1080 - th)
        tdraw.text((x, y), text, font=bg_font, fill=(180, 100, 255, 40))
        temp = temp.rotate(angle, expand=False)
        img.paste(temp, (0, 0), temp)

    # 3. Main glowing text
    main_font_size = 180
    font = get_font(main_font_size)
    while True:
        w, h = draw.textsize(text, font=font)
        if w <= 950 or main_font_size <= 80:
            break
        main_font_size -= 10
        font = get_font(main_font_size)

    x = (1080 - w) // 2
    y = (1080 - h) // 2 - 50

    # Black outline (multiple passes)
    outline = 12
    for dx in range(-outline, outline+1):
        for dy in range(-outline, outline+1):
            if abs(dx) + abs(dy) < outline*1.5:
                draw.text((x+dx, y+dy), text, font=font, fill=(0, 0, 0))

    # Purple glow (soft)
    glow = Image.new('RGBA', (1080, 1080), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(30, 0, -2):
        gdraw.text((x, y), text, font=get_font(main_font_size + i), fill=(180, 0, 255, 15))
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    img.paste(glow, (0,0), glow)

    # Main white text
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # Final neon border glow
    border = Image.new('RGBA', (1080, 1080), (0,0,0,0))
    bdraw = ImageDraw.Draw(border)
    for i in range(20):
        bdraw.text((x, y), text, font=get_font(main_font_size + 20), fill=(200, 0, 255, 20))
    border = border.filter(ImageFilter.GaussianBlur(20))
    img.paste(border, (0,0), border)

    # Save
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
