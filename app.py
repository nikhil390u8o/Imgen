from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import random

app = Flask(__name__)

# Safe font – works everywhere without any file
def get_font(size=100):
    try:
        return ImageFont.truetype("DejaVuSans-Bold", size)
    except:
        try:
            return ImageFont.truetype("Arial", size)
        except:
            return ImageFont.load_default()

@app.route('/')
def home():
    return '<h1>Imgen Logo Generator</h1><p><a href="/logo">Default Logo</a> | /logo?text=YOUR+TEXT</p>'

@app.route('/logo')
def logo():
    text = request.args.get('text', 'AS MASTI WORLD').upper()
    if len(text) > 30:
        text = text[:27] + "..."

    img = Image.new('RGB', (1080, 1080), (10, 0, 30))
    draw = ImageDraw.Draw(img)

    # Lightning background
    for _ in range(70):
        x1 = random.randint(0, 1080)
        y1 = random.randint(0, 1080)
        x2 = x1 + random.randint(-300, 300)
        y2 = y1 + random.randint(-300, 300)
        draw.line((x1,y1,x2,y2), fill=(150, 0, 255), width=random.randint(3,8))
    img = img.filter(ImageFilter.GaussianBlur(5))

    # Scattered background text (FIXED: using textbbox instead of textsize)
    bg_font = get_font(90)
    for _ in range(12):
        temp = Image.new('RGBA', (1080,1080), (0,0,0,0))
        tdraw = ImageDraw.Draw(temp)
        bbox = tdraw.textbbox((0,0), text, font=bg_font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = random.randint(-300, 1080 - w)
        y = random.randint(-300, 1080 - h)
        angle = random.randint(-45, 45)
        tdraw.text((0,0), text, font=bg_font, fill=(180,100,255,45))
        temp = temp.rotate(angle, expand=True)
        img.paste(temp, (x,y), temp)

    # Main text
    font_size = 180
    font = get_font(font_size)
    while True:
        bbox = draw.textbbox((0,0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= 950 or font_size <= 80:
            break
        font_size -= 10
        font = get_font(font_size)

    x = (1080 - w) // 2
    y = 380

    # Black outline
    for dx in range(-12, 13):
        for dy in range(-12, 13):
            draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0))

    # Purple glow
    glow = Image.new('RGBA', (1080,1080), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(40, 0, -4):
        gf = get_font(font_size + i)
        gdraw.text((x, y), text, font=gf, fill=(200, 0, 255, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(20))
    img.paste(glow, (0,0), glow)

    # White main text
    draw.text((x, y), text, font=font, fill=(255,255,255))

    # Output
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
