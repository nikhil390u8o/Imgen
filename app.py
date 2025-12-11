from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/logo')
def logo():
    text = request.args.get('text', 'AS MASTI WORLD')

    # Create image
    img = Image.new("RGB", (1080, 1080), "#2a0134")
    draw = ImageDraw.Draw(img)

    # Load font
    font = ImageFont.truetype("bold.ttf", 150)

    # Draw
    draw.text((100, 400), text, font=font, fill="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

# Render binds to PORT environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
