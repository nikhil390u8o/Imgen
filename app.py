from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import random

app = Flask(__name__)

# Super-safe font that always works on Render
def get_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold", size)
    except:
        return ImageFont.load_default()

@app.route('/')
def home():
    return '<h1>Imgen Logo Generator</h1><p><a href="/logo">Default</a> | /logo?text=ANY+TEXT</p>'

@app.route('/logo')
def logo():
    text = request.args.get('text', 'AS MASTI WORLD').upper()
    if len(text) > 30:
        text = text[:27] + "..."

    # Base image
    img = Image.new('RGB', (1080, 1080), (10, 0, 30))
    draw = ImageDraw.Draw(img)

    # Lightning background
    for _ in range(80):
        x1 = random.randint(0, 1080)
        y1 = random.randint(0, 1080)
        x2 = x1 + random.randint(-300, 300)
        y2 = y1 + random.randint(-300, 300)
        draw.line((x1,y1,x2,y2), fill=(160, 0, 255), width=random.randint(3,9))
    img = img.filter(ImageFilter.GaussianBlur(5))

    # Scattered background text (fixed for new Pillow)
    bg_font = get_font(90)
    for _ in range(12):
        layer = Image.new('RGBA', (1080,1080), (0,0,0,0))
        d = ImageDraw.Draw(layer)
        bbox = d.textbbox((0,0), text, font=bg_font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = random.randint(-400, 1080 - w)
        y = random.randint(-400, 1080 - h)
        angle = random.randint(-50, 50)
        d.text((0,0), text, font=bg_font, fill=(180,100,255,50))
        layer = layer.rotate(angle, expand=True)
        img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'), (x,y))

    # Main text size
    font_size = 180
    font = get_font(font_size)
    while draw.textbbox((0,0), text, font=font)[2] > 950 and font_size > 70:
        font_size -= 10
        font = get_font(font_size)

    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (1080 - w) // 2
    y = 380

    # Black outline
    for dx in range(-14, 15):
        for dy in range(-14, 15):
            draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0))

    # Purple glow
    glow = Image.new('RGBA', (1080,1080), (0,0,0,0))
    g = ImageDraw.Draw(glow)
    for i in range(50, 0, -5):
        g.text((x, y), text, font=get_font(font_size + i), fill=(200,0,255,20))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    img.paste(glow, (0,0), glow)

    # White text on top
    draw.text((x, y), text, font=font, fill=(255,255,255))

    # Send image
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
