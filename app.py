from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import random

app = Flask(__name__)

# Super safe font – works everywhere, no file needed
def get_font(size=100):
    try:
        # Try common system fonts first
        return ImageFont.truetype("DejaVuSans-Bold", size)
    except:
        try:
            return ImageFont.truetype("Arial", size)
        except:
            # Final fallback – always works
            return ImageFont.load_default(size=size)

@app.route('/')
def home():
    return "<h1>Imgen Logo Generator</h1><p><a href='/logo'>Default Logo</a> | /logo?text=YOUR+TEXT</p>"

@app.route('/logo')
def logo():
    text = request.args.get('text', 'AS MASTI WORLD').upper()
    if len(text) > 25:
        text = text[:22] + "..."

    # Create base image
    img = Image.new('RGB', (1080, 1080), (10, 0, 30))
    draw = ImageDraw.Draw(img)

    # Lightning background
    for _ in range(70):
        x1, y1 = random.randint(0,1080), random.randint(0,1080)
        x2, y2 = x1 + random.randint(-250,250), y1 + random.randint(-250,250)
        draw.line((x1,y1,x2,y2), fill=(140,0,255,180), width=random.randint(3,7))
    img = img.filter(ImageFilter.GaussianBlur(4))

    # Scattered background text
    for _ in range(10):
        temp = Image.new('RGBA', img.size, (0,0,0,0))
        d = ImageDraw.Draw(temp)
        f = get_font(90)
        w, h = d.textsize(text, font=f)
        x = random.randint(-200, 1080-w)
        y = random.randint(-200, 1080-h)
        angle = random.randint(-45,45)
        d.text((0,0), text, font=f, fill=(180,100,255,50))
        temp = temp.rotate(angle, expand=1)
        img.paste(temp, (x,y), temp)

    # Main text with glow
    font_size = 180
    font = get_font(font_size)
    while font.getsize(text)[0] > 950 and font_size > 60:
        font_size -= 10
        font = get_font(font_size)

    w, h = font.getsize(text)
    x = (1080 - w) // 2
    y = (1080 - h) // 2 - 50

    # Black outline
    for dx in range(-10,11):
        for dy in range(-10,11):
            draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0))

    # Purple glow
    glow = Image.new('RGBA', img.size, (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(40,0,-3):
        gdraw.text((x,y), text, font=get_font(font_size + i), fill=(200,0,255,20))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img.paste(glow, glow)

    # Main white text
    draw.text((x,y), text, font=font, fill=(255,255,255))

    # Save & send
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
