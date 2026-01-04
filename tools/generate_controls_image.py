from PIL import Image, ImageDraw, ImageFont

# Canvas
WIDTH, HEIGHT = 900, 600
img = Image.new("RGB", (WIDTH, HEIGHT), "#1e1e1e")
draw = ImageDraw.Draw(img)

# Fonts (fallback-safe)
try:
    title_font = ImageFont.truetype("arial.ttf", 40)
    header_font = ImageFont.truetype("arial.ttf", 26)
    text_font = ImageFont.truetype("arial.ttf", 22)
except:
    title_font = header_font = text_font = ImageFont.load_default()

# Helpers
def draw_text(x, y, text, font, fill="#ffffff"):
    draw.text((x, y), text, font=font, fill=fill)

def draw_row(y, key, action):
    draw_text(80, y, key, text_font, "#a6e22e")
    draw_text(260, y, action, text_font)

# Title
draw_text(80, 40, "Game Controls", title_font)

# Sections
draw_text(80, 110, "Movement & Camera", header_font)
draw_row(150, "W / A / S / D", "Move")
draw_row(180, "Mouse / Trackpad", "Look around")
draw_row(210, "Space", "Jump")

draw_text(80, 270, "Block Selection", header_font)
draw_row(310, "1", "Grass")
draw_row(340, "2", "Dirt")
draw_row(370, "3", "Brick")
draw_row(400, "4", "Wood")
draw_row(430, "5", "Stone")

draw_text(520, 110, "Actions", header_font)
draw_text(520, 150, "Left Click", text_font, "#a6e22e")
draw_text(680, 150, "Place block", text_font)
draw_text(520, 180, "Right Click", text_font, "#a6e22e")
draw_text(680, 180, "Destroy block", text_font)

draw_text(520, 270, "Save System", header_font)
draw_text(520, 310, "Shift + S", text_font, "#a6e22e")
draw_text(680, 310, "Save game", text_font)
draw_text(520, 340, "Shift + L", text_font, "#a6e22e")
draw_text(680, 340, "Load game", text_font)

# Save
img.save("assets/controls.png")
print("controls.png generated")
