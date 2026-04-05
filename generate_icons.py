#!/usr/bin/env python3
"""
High-quality game-style icon generator for BookQuest
Uses supersampling (1024x1024) with downscaling to 256x256 for anti-aliasing
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math
import os

OUTPUT_DIR = "/sessions/relaxed-nice-bell/mnt/건우독서앱/icons/"
RENDER_SIZE = 1024
FINAL_SIZE = 256
SCALE = RENDER_SIZE // FINAL_SIZE

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_image():
    """Create a new transparent RGBA image at render size"""
    return Image.new('RGBA', (RENDER_SIZE, RENDER_SIZE), (0, 0, 0, 0))

def composite_layer(base, layer, opacity=255):
    """Composite a layer onto base with opacity"""
    if opacity < 255:
        layer.putalpha(int(layer.getchannel('A').getextrema()[1] * opacity / 255))
    return Image.alpha_composite(base, layer)

def apply_blur(img, radius):
    """Apply Gaussian blur to an image"""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))

def downscale(img):
    """Downscale from RENDER_SIZE to FINAL_SIZE with LANCZOS"""
    return img.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)

def save_icon(img, filename):
    """Save icon and downscale"""
    final = downscale(img)
    final.save(os.path.join(OUTPUT_DIR, filename), 'PNG')
    print(f"✓ {filename}")

def draw_circle(draw, center, radius, fill, outline=None, width=1):
    """Draw a circle"""
    x, y = center
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=fill, outline=outline, width=width)

def draw_arc_points(center, radius, start_angle, end_angle, steps=20):
    """Generate points along an arc"""
    points = []
    x, y = center
    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        px = x + radius * math.cos(math.radians(angle))
        py = y + radius * math.sin(math.radians(angle))
        points.append((px, py))
    return points

# ============================================================================
# HAT ITEMS (1-13)
# ============================================================================

def create_shop_crown():
    """Golden crown with 5 peaks, red/blue/green jewels"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Base gold shape (darker gold)
    base_color = (218, 165, 32)
    draw.ellipse([cx-200, cy-50, cx+200, cy+100], fill=(180, 130, 20))
    draw.polygon([
        (cx-200, cy+50),
        (cx-150, cy-80),
        (cx-80, cy-100),
        (cx, cy-140),
        (cx+80, cy-100),
        (cx+150, cy-80),
        (cx+200, cy+50)
    ], fill=base_color)

    # Gold rim
    draw.ellipse([cx-210, cy+50, cx+210, cy+120], fill=(218, 165, 32), outline=(139, 105, 20), width=4*SCALE)

    # 5 crown peaks with highlights
    peak_positions = [
        (cx-150, cy-120),
        (cx-75, cy-180),
        (cx, cy-200),
        (cx+75, cy-180),
        (cx+150, cy-120)
    ]

    for i, (px, py) in enumerate(peak_positions):
        # Peak shadow
        draw.polygon([(px-30, py), (px, py-80), (px+20, py)], fill=(150, 100, 10))
        # Peak highlight
        draw.polygon([(px-20, py), (px-5, py-60), (px+10, py)], fill=(255, 215, 100))

    # Jewels (ruby, sapphire, emerald, sapphire, ruby)
    jewel_colors = [(200, 20, 20), (30, 100, 200), (20, 150, 50), (30, 100, 200), (200, 20, 20)]
    jewel_x_offsets = [-100, -50, 0, 50, 100]

    for offset, color in zip(jewel_x_offsets, jewel_colors):
        jx, jy = cx + offset, cy + 20
        # Jewel body
        draw.ellipse([jx-25, jy-25, jx+25, jy+25], fill=color, outline=(255, 255, 200), width=2*SCALE)
        # Jewel highlight
        draw.ellipse([jx-15, jy-15, jx-5, jy-5], fill=(255, 255, 255), outline=None)

    # Shine streak
    draw.polygon([
        (cx-80, cy-150),
        (cx-60, cy-170),
        (cx+60, cy-100),
        (cx+40, cy-80)
    ], fill=(255, 255, 200, 150))

    save_icon(img, 'shop-crown.png')

def create_deco_hat_pirate():
    """Black tricorn hat with gold trim and skull emblem"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Tricorn hat (3 points)
    hat_color = (30, 20, 20)
    draw.polygon([
        (cx-220, cy+80),
        (cx, cy-180),
        (cx+220, cy+80),
        (cx+100, cy+150),
        (cx-100, cy+150)
    ], fill=hat_color)

    # Gold trim
    draw.polygon([
        (cx-220, cy+80),
        (cx, cy-160),
        (cx+220, cy+80)
    ], fill=None, outline=(218, 165, 32), width=8*SCALE)

    # Skull emblem (center front)
    skull_x, skull_y = cx, cy + 20
    # Skull main
    draw.ellipse([skull_x-40, skull_y-40, skull_x+40, skull_y+40], fill=(200, 200, 200))
    # Eyes
    draw.ellipse([skull_x-25, skull_y-20, skull_x-10, skull_y-5], fill=(50, 50, 50))
    draw.ellipse([skull_x+10, skull_y-20, skull_x+25, skull_y-5], fill=(50, 50, 50))
    # Nose
    draw.polygon([(skull_x-10, skull_y), (skull_x+10, skull_y), (skull_x, skull_y+15)], fill=(50, 50, 50))

    # Crossbones
    draw.line([(skull_x-60, skull_y+30), (skull_x+60, skull_y+50)], fill=(200, 200, 200), width=8*SCALE)
    draw.line([(skull_x-60, skull_y+50), (skull_x+60, skull_y+30)], fill=(200, 200, 200), width=8*SCALE)

    save_icon(img, 'deco-hat-pirate.png')

def create_deco_hat_crown():
    """Ornate royal crown with fur trim"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Fur trim base (white fluffy)
    draw.ellipse([cx-220, cy+60, cx+220, cy+180], fill=(240, 240, 240))
    # Fur texture (irregular bumps)
    for i in range(-5, 6):
        x_pos = cx + i * 70
        draw.ellipse([x_pos-40, cy+40, x_pos+40, cy+100], fill=(250, 250, 250), outline=(220, 220, 220), width=2*SCALE)

    # Gold band
    draw.ellipse([cx-200, cy+50, cx+200, cy+140], fill=(218, 165, 32), outline=(139, 105, 20), width=4*SCALE)

    # Crown peaks (7 ornate peaks)
    for i in range(7):
        angle = i * (math.pi / 3)
        peak_x = cx + 180 * math.cos(angle)
        peak_y = cy - 180 * math.sin(angle)

        # Peak base
        draw.polygon([
            (cx + 140 * math.cos(angle), cy - 140 * math.sin(angle)),
            (peak_x, peak_y),
            (cx + 120 * math.cos(angle + 0.3), cy - 120 * math.sin(angle + 0.3))
        ], fill=(218, 165, 32))

        # Peak highlight
        draw.polygon([
            (cx + 145 * math.cos(angle), cy - 145 * math.sin(angle)),
            (peak_x - 10, peak_y + 15),
            (cx + 125 * math.cos(angle + 0.3), cy - 125 * math.sin(angle + 0.3))
        ], fill=(255, 215, 100))

        # Jewel at peak
        draw.ellipse([peak_x-20, peak_y-20, peak_x+20, peak_y+20], fill=(200, 20, 20), outline=(255, 200, 100), width=2*SCALE)

    # Center jewel (largest)
    draw.ellipse([cx-35, cy-220, cx+35, cy-150], fill=(100, 150, 255), outline=(255, 200, 100), width=3*SCALE)

    save_icon(img, 'deco-hat-crown.png')

def create_deco_hat_santa():
    """Red santa hat with white fur trim"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # White fur trim
    draw.ellipse([cx-180, cy+80, cx+180, cy+160], fill=(255, 255, 255))
    # Fur bumps
    for i in range(-4, 5):
        x_pos = cx + i * 80
        draw.circle((x_pos, cy+100), 35, fill=(250, 250, 250))

    # Red hat cone
    draw.polygon([
        (cx-170, cy+80),
        (cx+170, cy+80),
        (cx+80, cy-180),
        (cx-80, cy-180)
    ], fill=(220, 20, 20))

    # Red highlight stripe
    draw.polygon([
        (cx-160, cy+80),
        (cx-80, cy-170),
        (cx+60, cy-140),
        (cx+150, cy+80)
    ], fill=(255, 100, 100))

    # White pompom at top
    pom_x, pom_y = cx - 30, cy - 200
    draw.ellipse([pom_x-40, pom_y-40, pom_x+40, pom_y+40], fill=(255, 255, 255))
    # Pompom highlight
    draw.ellipse([pom_x-25, pom_y-25, pom_x-5, pom_y-5], fill=(255, 255, 255), outline=None)

    # Gold trim band
    draw.ellipse([cx-180, cy+75, cx+180, cy+125], fill=None, outline=(218, 165, 32), width=6*SCALE)

    save_icon(img, 'deco-hat-santa.png')

def create_deco_hat_wizard():
    """Tall purple wizard hat with stars and moon"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Hat cone (purple)
    draw.polygon([
        (cx-140, cy+100),
        (cx+140, cy+100),
        (cx+40, cy-250),
        (cx-40, cy-250)
    ], fill=(100, 50, 150))

    # Highlight stripe
    draw.polygon([
        (cx-130, cy+100),
        (cx-30, cy-240),
        (cx+50, cy-200),
        (cx+120, cy+100)
    ], fill=(150, 100, 200))

    # Gold band at base
    draw.ellipse([cx-145, cy+95, cx+145, cy+145], fill=(218, 165, 32), outline=(139, 105, 20), width=4*SCALE)

    # Stars scattered on hat
    star_positions = [(cx-60, cy-50), (cx+70, cy-120), (cx-40, cy-180), (cx+50, cy-230)]
    for sx, sy in star_positions:
        # 5-pointed star
        star_points = []
        for i in range(10):
            angle = i * math.pi / 5
            r = 30 if i % 2 == 0 else 15
            star_points.append((sx + r * math.cos(angle), sy + r * math.sin(angle)))
        draw.polygon(star_points, fill=(255, 255, 0), outline=(218, 165, 32), width=2*SCALE)

    # Crescent moon emblem
    moon_x, moon_y = cx + 80, cy - 100
    draw.ellipse([moon_x-35, moon_y-35, moon_x+35, moon_y+35], fill=(255, 255, 100))
    draw.ellipse([moon_x-25, moon_y-25, moon_x+40, moon_y+25], fill=(100, 50, 150))

    # Bent tip
    draw.polygon([(cx-30, cy-250), (cx+30, cy-250), (cx+50, cy-280), (cx-50, cy-280)], fill=(100, 50, 150))

    save_icon(img, 'deco-hat-wizard.png')

def create_deco_hat_ninja_band():
    """Dark blue headband with metal plate"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Headband (dark blue fabric)
    draw.ellipse([cx-180, cy-60, cx+180, cy+80], fill=(30, 50, 100))
    draw.ellipse([cx-160, cy-40, cx+160, cy+60], fill=(50, 80, 130))

    # Fabric wrinkles
    for i in range(-3, 4):
        x_pos = cx + i * 100
        draw.line([(x_pos, cy-50), (x_pos+20, cy-30), (x_pos, cy+50)], fill=(25, 40, 80), width=4*SCALE)

    # Metal plate (center)
    plate_size = 80
    draw.rectangle([cx-plate_size, cy-plate_size, cx+plate_size, cy+plate_size], fill=(180, 180, 180), outline=(100, 100, 100), width=4*SCALE)
    # Metal shine
    draw.rectangle([cx-plate_size+10, cy-plate_size+10, cx+plate_size-40, cy+plate_size-40], fill=(220, 220, 220))

    # Clan symbol (simple circle design)
    draw.ellipse([cx-30, cy-30, cx+30, cy+30], fill=(200, 50, 50), outline=(255, 255, 255), width=3*SCALE)
    draw.circle((cx, cy), 15, fill=(255, 255, 255))

    # Flowing tail ribbons
    ribbon_color = (30, 50, 100)
    draw.polygon([(cx-120, cy+60), (cx-180, cy+200), (cx-140, cy+180)], fill=ribbon_color)
    draw.polygon([(cx+120, cy+60), (cx+180, cy+200), (cx+140, cy+180)], fill=ribbon_color)

    save_icon(img, 'deco-hat-ninja-band.png')

def create_deco_hat_angel_halo():
    """Golden halo with soft glow"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 - 100

    # Glow layer (blurred)
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-150, cy-20, cx+150, cy+20], fill=(255, 215, 0, 100))
    glow = apply_blur(glow, 25)
    img = composite_layer(img, glow, 200)

    # Main halo ring (bright gold)
    draw.ellipse([cx-140, cy-15, cx+140, cy+15], fill=(255, 215, 0), outline=(218, 165, 32), width=6*SCALE)
    draw.ellipse([cx-120, cy-10, cx+120, cy+10], fill=None, outline=(255, 255, 200), width=3*SCALE)

    # Sparkles around halo
    for i in range(8):
        angle = i * math.pi / 4
        sx = cx + 170 * math.cos(angle)
        sy = cy + 170 * math.sin(angle)
        draw.ellipse([sx-8, sy-8, sx+8, sy+8], fill=(255, 255, 200))

    save_icon(img, 'deco-hat-angel-halo.png')

def create_deco_hat_devil_horn():
    """Two curved red horns with fire glow"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 - 80

    # Left horn
    horn_points_l = draw_arc_points((cx-80, cy), 100, 180, 360, 15)
    draw.line(horn_points_l, fill=(150, 20, 20), width=30*SCALE)
    draw.line(horn_points_l, fill=(200, 50, 50), width=20*SCALE)
    draw.circle((horn_points_l[-1]), 25, fill=(100, 10, 10))

    # Right horn
    horn_points_r = draw_arc_points((cx+80, cy), 100, 0, 180, 15)
    draw.line(horn_points_r, fill=(150, 20, 20), width=30*SCALE)
    draw.line(horn_points_r, fill=(200, 50, 50), width=20*SCALE)
    draw.circle((horn_points_r[-1]), 25, fill=(100, 10, 10))

    # Fire glow at base
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-120, cy-50, cx+120, cy+150], fill=(255, 100, 0, 80))
    glow = apply_blur(glow, 30)
    img = composite_layer(img, glow, 150)

    save_icon(img, 'deco-hat-devil-horn.png')

def create_deco_hat_cat_ear():
    """Two triangular cat ears"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 - 120

    # Left ear
    draw.polygon([
        (cx-100, cy+100),
        (cx-80, cy-100),
        (cx-40, cy+80)
    ], fill=(80, 60, 60))

    # Left ear inner (pink)
    draw.polygon([
        (cx-90, cy+70),
        (cx-75, cy-60),
        (cx-55, cy+65)
    ], fill=(200, 150, 150))

    # Right ear
    draw.polygon([
        (cx+100, cy+100),
        (cx+80, cy-100),
        (cx+40, cy+80)
    ], fill=(80, 60, 60))

    # Right ear inner (pink)
    draw.polygon([
        (cx+90, cy+70),
        (cx+75, cy-60),
        (cx+55, cy+65)
    ], fill=(200, 150, 150))

    # Fur texture lines
    for i in range(5):
        y_pos = cy - 100 + i * 40
        draw.line([(cx-80, y_pos), (cx-50, y_pos)], fill=(150, 100, 100), width=2*SCALE)
        draw.line([(cx+80, y_pos), (cx+50, y_pos)], fill=(150, 100, 100), width=2*SCALE)

    save_icon(img, 'deco-hat-cat-ear.png')

def create_deco_hat_bunny_ear():
    """Tall floppy white bunny ears"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 - 150

    # Left ear (large ellipse)
    draw.ellipse([cx-120, cy-200, cx-40, cy+80], fill=(250, 250, 250), outline=(200, 200, 200), width=3*SCALE)

    # Left ear inner (pink)
    draw.ellipse([cx-110, cy-180, cx-60, cy+50], fill=(255, 200, 220))

    # Right ear (large ellipse)
    draw.ellipse([cx+40, cy-200, cx+120, cy+80], fill=(250, 250, 250), outline=(200, 200, 200), width=3*SCALE)

    # Right ear inner (pink)
    draw.ellipse([cx+60, cy-180, cx+110, cy+50], fill=(255, 200, 220))

    # Fur texture
    for i in range(8):
        y_offset = cy - 150 + i * 40
        draw.line([(cx-105, y_offset), (cx-70, y_offset)], fill=(230, 230, 230), width=2*SCALE)
        draw.line([(cx+70, y_offset), (cx+105, y_offset)], fill=(230, 230, 230), width=2*SCALE)

    save_icon(img, 'deco-hat-bunny-ear.png')

def create_deco_hat_unicorn_horn():
    """Rainbow spiral horn with sparkles"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 - 100

    # Gradient horn sections (rainbow)
    colors = [(255, 0, 150), (255, 100, 0), (255, 255, 0), (0, 200, 150), (100, 150, 255)]

    for i, color in enumerate(colors):
        y_top = cy - 200 + i * 40
        y_bot = y_top + 50
        # Create tapering triangle
        width_top = 40 - i * 5
        width_bot = 30 - i * 5
        draw.polygon([
            (cx - width_top, y_top),
            (cx + width_top, y_top),
            (cx + width_bot, y_bot),
            (cx - width_bot, y_bot)
        ], fill=color)

    # Spiral effect
    for i in range(12):
        angle = i * 30
        x_off = 20 * math.cos(math.radians(angle))
        y_off = i * 15
        draw.line([(cx - 15 + x_off, cy - 200 + y_off), (cx + 15 + x_off, cy - 200 + y_off)], fill=(200, 200, 200, 150), width=2*SCALE)

    # Sparkles
    for i in range(6):
        sx = cx + 60 * math.cos(math.radians(i * 60))
        sy = cy - 150 + 50 * math.sin(math.radians(i * 60))
        draw.polygon([
            (sx, sy-15),
            (sx+12, sy),
            (sx, sy+15),
            (sx-12, sy)
        ], fill=(255, 255, 200))

    save_icon(img, 'deco-hat-unicorn-horn.png')

def create_deco_hat_party():
    """Colorful cone party hat"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Striped cone
    stripe_colors = [(255, 50, 50), (50, 100, 255), (50, 200, 50), (255, 255, 0)]

    for i, color in enumerate(stripe_colors):
        width_top = 160 - i * 5
        width_bot = 80 - i * 5
        draw.polygon([
            (cx - width_top, cy + 100),
            (cx + width_top, cy + 100),
            (cx + width_bot, cy - 200),
            (cx - width_bot, cy - 200)
        ], fill=color)

        # Stripe lines
        if i < 3:
            next_width_top = 160 - (i + 1) * 5
            draw.polygon([
                (cx - next_width_top, cy + 100),
                (cx + next_width_top, cy + 100),
                (cx + width_bot, cy - 200),
                (cx - width_bot, cy - 200)
            ], fill=None, outline=(255, 255, 255), width=3*SCALE)

    # Pompom at top
    pom_x, pom_y = cx, cy - 210
    for j in range(3):
        for k in range(-1, 2):
            pom_bx = pom_x + k * 20
            pom_by = pom_y - j * 20
            draw.ellipse([pom_bx-12, pom_by-12, pom_bx+12, pom_by+12], fill=(255, 100, 200))

    save_icon(img, 'deco-hat-party.png')

def create_deco_hat_laurel():
    """Green leaf laurel wreath"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Wreath circle
    for i in range(24):
        angle = i * 15
        leaf_x = cx + 140 * math.cos(math.radians(angle))
        leaf_y = cy + 140 * math.sin(math.radians(angle))

        # Leaf shape
        leaf_angle = angle + 90
        lx = math.cos(math.radians(leaf_angle))
        ly = math.sin(math.radians(leaf_angle))

        leaf_points = [
            (leaf_x, leaf_y),
            (leaf_x + 30*lx, leaf_y + 30*ly),
            (leaf_x + 15*lx - 20*math.cos(math.radians(leaf_angle)), leaf_y + 15*ly - 20*math.sin(math.radians(leaf_angle)))
        ]
        draw.polygon(leaf_points, fill=(50, 150, 50))

    # Golden berries
    for i in range(0, 24, 3):
        angle = i * 15
        berry_x = cx + 100 * math.cos(math.radians(angle))
        berry_y = cy + 100 * math.sin(math.radians(angle))
        draw.ellipse([berry_x-12, berry_y-12, berry_x+12, berry_y+12], fill=(218, 165, 32))
        draw.ellipse([berry_x-6, berry_y-6, berry_x+6, berry_y+6], fill=(255, 215, 100))

    save_icon(img, 'deco-hat-laurel.png')

# ============================================================================
# FACE ITEMS (14-26)
# ============================================================================

def create_shop_glasses():
    """Round nerdy glasses"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left lens
    left_x, right_x = cx - 110, cx + 110
    lens_y = cy
    lens_size = 70

    draw.ellipse([left_x-lens_size, lens_y-lens_size, left_x+lens_size, lens_y+lens_size],
                 fill=(80, 80, 100), outline=(40, 40, 50), width=6*SCALE)

    # Right lens
    draw.ellipse([right_x-lens_size, lens_y-lens_size, right_x+lens_size, lens_y+lens_size],
                 fill=(80, 80, 100), outline=(40, 40, 50), width=6*SCALE)

    # Bridge
    draw.rectangle([left_x+lens_size-10, lens_y-20, right_x-lens_size+10, lens_y+20],
                   fill=(40, 40, 50))

    # Lens reflections
    draw.ellipse([left_x-30, lens_y-30, left_x+10, lens_y-10], fill=(180, 200, 220), outline=None)
    draw.ellipse([right_x-10, lens_y-30, right_x+30, lens_y-10], fill=(180, 200, 220), outline=None)

    save_icon(img, 'shop-glasses.png')

def create_deco_face_sunglasses():
    """Sleek aviator sunglasses"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left lens (teardrop shape)
    left_x = cx - 100
    pts_l = draw_arc_points((left_x, cy), 65, -30, 30, 10)
    pts_l += draw_arc_points((left_x, cy), 50, 30, -30, 10)
    draw.polygon(pts_l, fill=(30, 80, 150), outline=(150, 180, 200), width=5*SCALE)

    # Right lens
    right_x = cx + 100
    pts_r = draw_arc_points((right_x, cy), 65, 150, 210, 10)
    pts_r += draw_arc_points((right_x, cy), 50, 210, 150, 10)
    draw.polygon(pts_r, fill=(30, 80, 150), outline=(150, 180, 200), width=5*SCALE)

    # Gold bridge
    draw.polygon([(left_x+65, cy-15), (right_x-65, cy-15), (right_x-65, cy+15), (left_x+65, cy+15)],
                 fill=(218, 165, 32), outline=(139, 105, 20), width=3*SCALE)

    # Lens shine
    draw.polygon([(left_x-20, cy-40), (left_x+20, cy-35), (left_x, cy-20)], fill=(100, 180, 255, 150))
    draw.polygon([(right_x-20, cy-40), (right_x+20, cy-35), (right_x, cy-20)], fill=(100, 180, 255, 150))

    save_icon(img, 'deco-face-sunglasses.png')

def create_deco_face_heart_glasses():
    """Pink/red heart-shaped frames"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left heart
    hx, hy = cx - 90, cy
    # Heart outline (simplified)
    draw.ellipse([hx-50, hy-60, hx-10, hy-10], fill=(200, 50, 100))
    draw.ellipse([hx+10, hy-60, hx+50, hy-10], fill=(200, 50, 100))
    draw.polygon([(hx-50, hy-10), (hx+50, hy-10), (hx, hy+70)], fill=(200, 50, 100))

    # Right heart
    hx2 = cx + 90
    draw.ellipse([hx2-50, hy-60, hx2-10, hy-10], fill=(200, 50, 100))
    draw.ellipse([hx2+10, hy-60, hx2+50, hy-10], fill=(200, 50, 100))
    draw.polygon([(hx2-50, hy-10), (hx2+50, hy-10), (hx2, hy+70)], fill=(200, 50, 100))

    # Bridge
    draw.rectangle([cx-30, cy-35, cx+30, cy+15], fill=(200, 50, 100))

    # Rose tint lenses
    draw.polygon([(hx-40, hy-50), (hx+40, hy-50), (hx+30, hy+50), (hx-30, hy+50)], fill=(255, 150, 180, 200))
    draw.polygon([(hx2-40, hy-50), (hx2+40, hy-50), (hx2+30, hy+50), (hx2-30, hy+50)], fill=(255, 150, 180, 200))

    save_icon(img, 'deco-face-heart-glasses.png')

def create_deco_face_star_glasses():
    """Yellow star-shaped frames"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left star
    star_x = cx - 90
    for p in range(10):
        angle = p * math.pi / 5
        r = 70 if p % 2 == 0 else 35
        if p == 0:
            points_l = [(star_x + r * math.cos(angle), cy + r * math.sin(angle))]
        else:
            points_l.append((star_x + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points_l, fill=(255, 215, 0), outline=(200, 150, 0), width=5*SCALE)

    # Right star
    star_x2 = cx + 90
    points_r = []
    for p in range(10):
        angle = p * math.pi / 5
        r = 70 if p % 2 == 0 else 35
        points_r.append((star_x2 + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points_r, fill=(255, 215, 0), outline=(200, 150, 0), width=5*SCALE)

    # Bridge
    draw.rectangle([cx-25, cy-20, cx+25, cy+20], fill=(255, 215, 0), outline=(200, 150, 0), width=3*SCALE)

    # Golden sparkle lenses
    draw.polygon([(star_x-50, cy-50), (star_x+50, cy-50), (star_x+40, cy+50), (star_x-40, cy+50)], fill=(255, 255, 150, 200))
    draw.polygon([(star_x2-50, cy-50), (star_x2+50, cy-50), (star_x2+40, cy+50), (star_x2-40, cy+50)], fill=(255, 255, 150, 200))

    save_icon(img, 'deco-face-star-glasses.png')

def create_deco_face_3d_glasses():
    """Red/cyan 3D glasses"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left lens (red)
    left_x = cx - 90
    draw.rectangle([left_x-50, cy-50, left_x+50, cy+50], fill=(200, 50, 50), outline=(100, 20, 20), width=5*SCALE)
    draw.rectangle([left_x-40, cy-40, left_x+40, cy+40], fill=(255, 100, 100, 200))

    # Right lens (cyan)
    right_x = cx + 90
    draw.rectangle([right_x-50, cy-50, right_x+50, cy+50], fill=(50, 150, 200), outline=(20, 100, 150), width=5*SCALE)
    draw.rectangle([right_x-40, cy-40, right_x+40, cy+40], fill=(100, 200, 255, 200))

    # White frame bridge
    draw.rectangle([left_x+45, cy-30, right_x-45, cy+30], fill=(200, 200, 200), outline=(100, 100, 100), width=3*SCALE)

    save_icon(img, 'deco-face-3d-glasses.png')

def create_deco_face_monocle():
    """Golden monocle"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main circle lens
    lens_x = cx - 40
    draw.ellipse([lens_x-70, cy-70, lens_x+70, cy+70], fill=(200, 200, 220), outline=(218, 165, 32), width=8*SCALE)

    # Inner lens shine
    draw.ellipse([lens_x-50, cy-50, lens_x-10, cy-10], fill=(255, 255, 255, 150))

    # Golden frame detail
    draw.ellipse([lens_x-60, cy-60, lens_x+60, cy+60], fill=None, outline=(218, 165, 32), width=4*SCALE)

    # Chain hanging down
    chain_x = lens_x + 50
    chain_points = [(chain_x, cy+70)]
    for i in range(6):
        chain_y = cy + 70 + i * 40
        chain_x_off = chain_x + 15 * math.cos(i * 0.5)
        chain_points.append((chain_x_off, chain_y))
    draw.line(chain_points, fill=(218, 165, 32), width=4*SCALE)

    # Chain links
    for i in range(len(chain_points)-1):
        draw.ellipse([chain_points[i][0]-6, chain_points[i][1]-6,
                     chain_points[i][0]+6, chain_points[i][1]+6],
                     fill=(218, 165, 32), outline=(139, 105, 20), width=2*SCALE)

    save_icon(img, 'deco-face-monocle.png')

def create_deco_face_vr_goggle():
    """Futuristic VR headset"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main visor shape
    visor_x = cx
    draw.rectangle([visor_x-100, cy-50, visor_x+100, cy+80], fill=(40, 40, 50), outline=(100, 100, 120), width=4*SCALE)

    # Left screen
    draw.rectangle([visor_x-90, cy-40, visor_x-20, cy+70], fill=(30, 60, 100), outline=(0, 150, 255), width=3*SCALE)

    # Right screen
    draw.rectangle([visor_x+20, cy-40, visor_x+90, cy+70], fill=(30, 60, 100), outline=(0, 150, 255), width=3*SCALE)

    # Blue LED strips
    for y_off in [-30, 0, 30]:
        draw.line([(visor_x-80, cy+y_off), (visor_x+80, cy+y_off)], fill=(0, 150, 255), width=4*SCALE)

    # Glow effect
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.rectangle([visor_x-100, cy-50, visor_x+100, cy+80], fill=(0, 150, 255, 80))
    glow = apply_blur(glow, 20)
    img = composite_layer(img, glow, 150)

    save_icon(img, 'deco-face-vr-goggle.png')

def create_deco_face_steampunk():
    """Brass goggles with gears"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left goggle
    left_x = cx - 80
    draw.ellipse([left_x-55, cy-55, left_x+55, cy+55], fill=(180, 120, 80), outline=(100, 70, 40), width=6*SCALE)
    draw.ellipse([left_x-40, cy-40, left_x+40, cy+40], fill=(200, 180, 160, 200))

    # Right goggle
    right_x = cx + 80
    draw.ellipse([right_x-55, cy-55, right_x+55, cy+55], fill=(180, 120, 80), outline=(100, 70, 40), width=6*SCALE)
    draw.ellipse([right_x-40, cy-40, right_x+40, cy+40], fill=(200, 180, 160, 200))

    # Bridge (leather)
    draw.rectangle([left_x+50, cy-30, right_x-50, cy+30], fill=(100, 70, 40), outline=(70, 50, 30), width=3*SCALE)

    # Gears on left
    for i in range(8):
        angle = i * 45
        gx = left_x - 70 + 40 * math.cos(math.radians(angle))
        gy = cy + 40 * math.sin(math.radians(angle))
        draw.ellipse([gx-12, gy-12, gx+12, gy+12], fill=(150, 100, 60), outline=(100, 70, 40), width=2*SCALE)

    # Gears on right
    for i in range(8):
        angle = i * 45
        gx = right_x + 70 + 40 * math.cos(math.radians(angle))
        gy = cy + 40 * math.sin(math.radians(angle))
        draw.ellipse([gx-12, gy-12, gx+12, gy+12], fill=(150, 100, 60), outline=(100, 70, 40), width=2*SCALE)

    # Leather strap
    strap_pts = [(left_x-30, cy+60), (right_x+30, cy+60), (right_x+25, cy+90), (left_x-25, cy+90)]
    draw.polygon(strap_pts, fill=(80, 50, 30))

    save_icon(img, 'deco-face-steampunk.png')

def create_deco_face_rainbow_glasses():
    """Rainbow spectrum lenses"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left lens (red to violet)
    left_x = cx - 85
    lens_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

    for i, color in enumerate(lens_colors):
        segment_w = 160 // 7
        draw.rectangle([left_x - 80 + i*segment_w, cy-60, left_x - 80 + (i+1)*segment_w, cy+60],
                      fill=color, outline=None)
    draw.rectangle([left_x-80, cy-60, left_x+80, cy+60], fill=None, outline=(50, 50, 50), width=5*SCALE)

    # Right lens (same gradient)
    right_x = cx + 85
    for i, color in enumerate(lens_colors):
        segment_w = 160 // 7
        draw.rectangle([right_x - 80 + i*segment_w, cy-60, right_x - 80 + (i+1)*segment_w, cy+60],
                      fill=color, outline=None)
    draw.rectangle([right_x-80, cy-60, right_x+80, cy+60], fill=None, outline=(50, 50, 50), width=5*SCALE)

    # Black frame bridge
    draw.rectangle([left_x+75, cy-35, right_x-75, cy+35], fill=(50, 50, 50), outline=(30, 30, 30), width=3*SCALE)

    save_icon(img, 'deco-face-rainbow-glasses.png')

def create_deco_face_half_mask():
    """White phantom mask"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Mask shape (right side)
    mask_pts = [
        (cx-50, cy-80),
        (cx+80, cy-60),
        (cx+100, cy+20),
        (cx+60, cy+100),
        (cx-50, cy+80)
    ]
    draw.polygon(mask_pts, fill=(230, 230, 230), outline=(100, 100, 100), width=4*SCALE)

    # Eye hole
    draw.ellipse([cx+20, cy-50, cx+70, cy], fill=(0, 0, 0, 200))

    # Gold trim
    draw.polygon(mask_pts, fill=None, outline=(218, 165, 32), width=6*SCALE)

    # Elegant curve details
    draw.arc([cx+40, cy-30, cx+100, cy+30], 0, 180, fill=(218, 165, 32), width=3*SCALE)

    save_icon(img, 'deco-face-half-mask.png')

def create_deco_face_tiger_paint():
    """Tiger stripe face paint"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left side stripes (orange/black)
    stripe_positions = [
        (cx-80, cy-60),
        (cx-85, cy),
        (cx-75, cy+60)
    ]

    for sx, sy in stripe_positions:
        # Orange stripe
        draw.rectangle([sx-25, sy-15, sx+30, sy+15], fill=(255, 140, 0))
        # Black outline
        draw.rectangle([sx-25, sy-15, sx+30, sy+15], fill=None, outline=(50, 30, 0), width=3*SCALE)

    # Right side stripes
    stripe_positions_r = [
        (cx+80, cy-60),
        (cx+85, cy),
        (cx+75, cy+60)
    ]

    for sx, sy in stripe_positions_r:
        draw.rectangle([sx-25, sy-15, sx+30, sy+15], fill=(255, 140, 0))
        draw.rectangle([sx-25, sy-15, sx+30, sy+15], fill=None, outline=(50, 30, 0), width=3*SCALE)

    # Nose mark
    nose_pts = [(cx-20, cy), (cx+20, cy), (cx+15, cy+25), (cx-15, cy+25)]
    draw.polygon(nose_pts, fill=(50, 30, 0))

    save_icon(img, 'deco-face-tiger-paint.png')

def create_deco_face_war_paint():
    """Bold red war paint"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Horizontal red stripes across face
    stripe_h = 30
    stripe_colors = [(200, 0, 0), (0, 0, 0), (200, 0, 0), (0, 0, 0)]

    for i, color in enumerate(stripe_colors):
        y_top = cy - 80 + i * stripe_h
        draw.rectangle([cx-150, y_top, cx+150, y_top+stripe_h], fill=color)

    # Vertical accent lines
    for x_off in [-60, -20, 20, 60]:
        draw.line([(cx+x_off, cy-100), (cx+x_off, cy+100)], fill=(0, 0, 0), width=8*SCALE)

    save_icon(img, 'deco-face-war-paint.png')

def create_deco_face_star_sticker():
    """Golden star cheek sticker"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 + 60

    # Main star
    star_points = []
    for i in range(10):
        angle = i * math.pi / 5
        r = 50 if i % 2 == 0 else 25
        star_points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(star_points, fill=(255, 215, 0), outline=(218, 165, 32), width=4*SCALE)

    # Highlight (3D effect)
    for i in [0, 2, 4]:
        angle = i * math.pi / 5
        r = 35
        hx = cx + r * math.cos(angle)
        hy = cy + r * math.sin(angle)
        draw.ellipse([hx-10, hy-10, hx+10, hy+10], fill=(255, 255, 255))

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.polygon(star_points, fill=(255, 215, 0, 100))
    glow = apply_blur(glow, 15)
    img = composite_layer(img, glow, 150)

    save_icon(img, 'deco-face-star-sticker.png')

print("\n=== HAT ITEMS (1-13) ===")
create_shop_crown()
create_deco_hat_pirate()
create_deco_hat_crown()
create_deco_hat_santa()
create_deco_hat_wizard()
create_deco_hat_ninja_band()
create_deco_hat_angel_halo()
create_deco_hat_devil_horn()
create_deco_hat_cat_ear()
create_deco_hat_bunny_ear()
create_deco_hat_unicorn_horn()
create_deco_hat_party()
create_deco_hat_laurel()

print("\n=== FACE ITEMS (14-26) ===")
create_shop_glasses()
create_deco_face_sunglasses()
create_deco_face_heart_glasses()
create_deco_face_star_glasses()
create_deco_face_3d_glasses()
create_deco_face_monocle()
create_deco_face_vr_goggle()
create_deco_face_steampunk()
create_deco_face_rainbow_glasses()
create_deco_face_half_mask()
create_deco_face_tiger_paint()
create_deco_face_war_paint()
create_deco_face_star_sticker()

# ============================================================================
# PET ITEMS (27-38)
# ============================================================================

def create_deco_pet_mini_dragon():
    """Cute red dragon"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Body (red round)
    draw.ellipse([cx-80, cy-60, cx+80, cy+100], fill=(220, 50, 50), outline=(150, 20, 20), width=4*SCALE)

    # Head
    draw.ellipse([cx-50, cy-100, cx+50, cy-20], fill=(220, 50, 50), outline=(150, 20, 20), width=4*SCALE)

    # Eyes (big)
    draw.ellipse([cx-30, cy-70, cx-10, cy-50], fill=(0, 0, 0))
    draw.ellipse([cx+10, cy-70, cx+30, cy-50], fill=(0, 0, 0))
    draw.circle((cx-20, cy-60), 5, fill=(255, 255, 255))
    draw.circle((cx+20, cy-60), 5, fill=(255, 255, 255))

    # Horns
    draw.polygon([(cx-25, cy-100), (cx-35, cy-140), (cx-15, cy-110)], fill=(100, 20, 20))
    draw.polygon([(cx+25, cy-100), (cx+35, cy-140), (cx+15, cy-110)], fill=(100, 20, 20))

    # Small wings
    draw.polygon([(cx-80, cy), (cx-130, cy-40), (cx-100, cy+20)], fill=(180, 30, 30))
    draw.polygon([(cx+80, cy), (cx+130, cy-40), (cx+100, cy+20)], fill=(180, 30, 30))

    # Flame breath
    flame_pts = [(cx-10, cy-20), (cx+10, cy-20), (cx+15, cy-50), (cx-15, cy-50)]
    draw.polygon(flame_pts, fill=(255, 150, 0))
    flame_pts2 = [(cx-5, cy-25), (cx+5, cy-25), (cx+10, cy-45), (cx-10, cy-45)]
    draw.polygon(flame_pts2, fill=(255, 200, 0))

    # Tail
    draw.line([(cx+60, cy+60), (cx+120, cy+80), (cx+140, cy), (cx+100, cy-40)], fill=(220, 50, 50), width=20*SCALE)

    save_icon(img, 'deco-pet-mini-dragon.png')

def create_deco_pet_kitty():
    """Orange tabby kitten"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Body (sitting)
    draw.ellipse([cx-70, cy-20, cx+70, cy+120], fill=(255, 120, 30), outline=(180, 80, 20), width=4*SCALE)

    # Head
    draw.ellipse([cx-60, cy-90, cx+60, cy+20], fill=(255, 120, 30), outline=(180, 80, 20), width=4*SCALE)

    # Ears
    draw.polygon([(cx-50, cy-90), (cx-35, cy-140), (cx-30, cy-80)], fill=(255, 120, 30))
    draw.polygon([(cx+50, cy-90), (cx+35, cy-140), (cx+30, cy-80)], fill=(255, 120, 30))
    # Ear inner
    draw.polygon([(cx-45, cy-100), (cx-37, cy-125), (cx-35, cy-90)], fill=(255, 180, 100))
    draw.polygon([(cx+45, cy-100), (cx+37, cy-125), (cx+35, cy-90)], fill=(255, 180, 100))

    # Eyes (big green)
    draw.ellipse([cx-35, cy-50, cx-10, cy-25], fill=(50, 180, 50), outline=(0, 100, 0), width=2*SCALE)
    draw.ellipse([cx+10, cy-50, cx+35, cy-25], fill=(50, 180, 50), outline=(0, 100, 0), width=2*SCALE)
    # Pupils
    draw.ellipse([cx-25, cy-45, cx-15, cy-30], fill=(0, 0, 0))
    draw.ellipse([cx+15, cy-45, cx+25, cy-30], fill=(0, 0, 0))

    # Nose
    draw.polygon([(cx-5, cy-20), (cx+5, cy-20), (cx, cy-10)], fill=(255, 100, 100))

    # Whiskers
    draw.line([(cx-60, cy-15), (cx-100, cy-20)], fill=(200, 80, 20), width=2*SCALE)
    draw.line([(cx-60, cy-5), (cx-100, cy)], fill=(200, 80, 20), width=2*SCALE)
    draw.line([(cx+60, cy-15), (cx+100, cy-20)], fill=(200, 80, 20), width=2*SCALE)
    draw.line([(cx+60, cy-5), (cx+100, cy)], fill=(200, 80, 20), width=2*SCALE)

    # Tail (curled)
    tail_pts = [(cx+70, cy+100), (cx+130, cy+120), (cx+150, cy+40), (cx+120, cy)]
    draw.line(tail_pts, fill=(255, 120, 30), width=20*SCALE)

    # Striped tabby
    for i in range(3):
        y_pos = cy + i * 40
        draw.line([(cx-40, y_pos), (cx-20, y_pos)], fill=(180, 80, 20), width=3*SCALE)
        draw.line([(cx+20, y_pos), (cx+40, y_pos)], fill=(180, 80, 20), width=3*SCALE)

    save_icon(img, 'deco-pet-kitty.png')

def create_deco_pet_ghost():
    """Cute white ghost"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Body (rounded top, wavy bottom)
    draw.ellipse([cx-80, cy-80, cx+80, cy+80], fill=(250, 250, 250), outline=(200, 200, 200), width=4*SCALE)

    # Wavy bottom (scalloped)
    for i in range(7):
        x_pos = cx - 70 + i * 20
        draw.ellipse([x_pos-15, cy+60, x_pos+15, cy+100], fill=(250, 250, 250))

    # Eyes (big and round)
    draw.ellipse([cx-40, cy-20, cx-10, cy+10], fill=(50, 50, 50))
    draw.ellipse([cx+10, cy-20, cx+40, cy+10], fill=(50, 50, 50))
    # Eye highlights
    draw.circle((cx-25, cy-10), 8, fill=(150, 150, 150))
    draw.circle((cx+25, cy-10), 8, fill=(150, 150, 150))

    # Mouth (happy)
    draw.ellipse([cx-25, cy+20, cx+25, cy+45], fill=(255, 150, 150), outline=(200, 100, 100), width=2*SCALE)

    # Rosy cheeks
    draw.ellipse([cx-60, cy, cx-30, cy+30], fill=(255, 150, 150, 150))
    draw.ellipse([cx+30, cy, cx+60, cy+30], fill=(255, 150, 150, 150))

    save_icon(img, 'deco-pet-ghost.png')

def create_deco_pet_robot():
    """Small silver robot"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Body (square)
    draw.rectangle([cx-60, cy-20, cx+60, cy+100], fill=(200, 200, 200), outline=(100, 100, 100), width=4*SCALE)

    # Head (square)
    draw.rectangle([cx-50, cy-80, cx+50, cy-20], fill=(200, 200, 200), outline=(100, 100, 100), width=4*SCALE)

    # Antenna
    draw.line([(cx, cy-80), (cx-20, cy-120)], fill=(100, 100, 100), width=5*SCALE)
    draw.circle((cx-20, cy-120), 8, fill=(255, 100, 100))

    # LED eyes (red)
    draw.ellipse([cx-30, cy-60, cx-10, cy-40], fill=(255, 100, 100), outline=(150, 50, 50), width=2*SCALE)
    draw.ellipse([cx+10, cy-60, cx+30, cy-40], fill=(255, 100, 100), outline=(150, 50, 50), width=2*SCALE)

    # Mouth (speaker grille)
    for i in range(3):
        y_pos = cy - 25 + i * 10
        draw.line([(cx-20, y_pos), (cx+20, y_pos)], fill=(100, 100, 100), width=3*SCALE)

    # Claw hands
    draw.polygon([(cx-60, cy+30), (cx-100, cy+10), (cx-95, cy+40)], fill=(180, 180, 180), outline=(100, 100, 100), width=2*SCALE)
    draw.polygon([(cx+60, cy+30), (cx+100, cy+10), (cx+95, cy+40)], fill=(180, 180, 180), outline=(100, 100, 100), width=2*SCALE)

    # Panel line
    draw.line([(cx-60, cy+25), (cx+60, cy+25)], fill=(150, 150, 150), width=3*SCALE)

    save_icon(img, 'deco-pet-robot.png')

def create_deco_pet_star():
    """Happy yellow star"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Star shape
    star_points = []
    for i in range(10):
        angle = i * math.pi / 5
        r = 80 if i % 2 == 0 else 40
        star_points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(star_points, fill=(255, 255, 0), outline=(200, 200, 0), width=4*SCALE)

    # Eyes
    draw.ellipse([cx-35, cy-30, cx-15, cy-10], fill=(0, 0, 0))
    draw.ellipse([cx+15, cy-30, cx+35, cy-10], fill=(0, 0, 0))
    draw.circle((cx-25, cy-20), 5, fill=(255, 255, 255))
    draw.circle((cx+25, cy-20), 5, fill=(255, 255, 255))

    # Smile
    draw.arc([cx-30, cy, cx+30, cy+50], 0, 180, fill=(0, 0, 0), width=5*SCALE)

    # Tiny arms
    draw.line([(cx-80, cy), (cx-120, cy-20)], fill=(255, 255, 0), width=8*SCALE)
    draw.line([(cx+80, cy), (cx+120, cy-20)], fill=(255, 255, 0), width=8*SCALE)

    # Tiny legs
    draw.line([(cx-40, cy+70), (cx-40, cy+110)], fill=(255, 255, 0), width=8*SCALE)
    draw.line([(cx+40, cy+70), (cx+40, cy+110)], fill=(255, 255, 0), width=8*SCALE)

    save_icon(img, 'deco-pet-star.png')

def create_deco_pet_slime():
    """Green translucent slime"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main blob (wobbly)
    blob_pts = [
        (cx-70, cy+60),
        (cx-50, cy-40),
        (cx, cy-80),
        (cx+60, cy-30),
        (cx+80, cy+50),
        (cx+50, cy+100),
        (cx-30, cy+110)
    ]
    draw.polygon(blob_pts, fill=(100, 200, 100, 200), outline=(50, 150, 50), width=4*SCALE)

    # Shine highlight
    shine_pts = [(cx-40, cy-20), (cx+20, cy-40), (cx-10, cy+20)]
    draw.polygon(shine_pts, fill=(200, 255, 200, 150))

    # Eyes
    draw.ellipse([cx-30, cy-20, cx-5, cy+5], fill=(0, 0, 0))
    draw.ellipse([cx+5, cy-20, cx+30, cy+5], fill=(0, 0, 0))
    draw.circle((cx-17, cy-10), 6, fill=(100, 255, 100))
    draw.circle((cx+17, cy-10), 6, fill=(100, 255, 100))

    # Mouth (happy)
    draw.arc([cx-20, cy+10, cx+20, cy+40], 0, 180, fill=(50, 150, 50), width=4*SCALE)

    save_icon(img, 'deco-pet-slime.png')

def create_deco_pet_phoenix():
    """Tiny fire bird"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Body (red/orange)
    draw.ellipse([cx-40, cy+20, cx+40, cy+90], fill=(255, 100, 20), outline=(200, 60, 10), width=3*SCALE)

    # Head
    draw.ellipse([cx-35, cy-30, cx+35, cy+30], fill=(255, 100, 20), outline=(200, 60, 10), width=3*SCALE)

    # Eyes (fierce tiny)
    draw.ellipse([cx-20, cy-10, cx-5, cy+5], fill=(0, 0, 0))
    draw.ellipse([cx+5, cy-10, cx+20, cy+5], fill=(0, 0, 0))

    # Flame plumage (top)
    flame_colors = [(255, 200, 0), (255, 150, 0), (255, 80, 0)]
    for i, color in enumerate(flame_colors):
        angle_off = 90 - i * 20
        fx = cx + 50 * math.cos(math.radians(angle_off))
        fy = cy - 40 - i * 15
        draw.polygon([(fx-15, fy), (fx+15, fy), (fx, fy-25)], fill=color)

    # Flame tail
    tail_pts = [(cx+40, cy+50), (cx+100, cy+30), (cx+120, cy+80)]
    draw.polygon(tail_pts, fill=(255, 100, 20))
    for j in range(3):
        tail_flame_pts = [(cx+60+j*20, cy+40+j*10), (cx+80+j*15, cy+50+j*5), (cx+70+j*20, cy+70+j*10)]
        draw.polygon(tail_flame_pts, fill=(255, 180, 0))

    save_icon(img, 'deco-pet-phoenix.png')

def create_deco_pet_snowman():
    """Mini snowman"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Three snowballs
    draw.ellipse([cx-50, cy-100, cx+50, cy-20], fill=(240, 240, 255), outline=(200, 200, 220), width=3*SCALE)
    draw.ellipse([cx-65, cy-20, cx+65, cy+70], fill=(240, 240, 255), outline=(200, 200, 220), width=3*SCALE)
    draw.ellipse([cx-50, cy+60, cx+50, cy+150], fill=(240, 240, 255), outline=(200, 200, 220), width=3*SCALE)

    # Coal eyes
    draw.circle((cx-15, cy-65), 8, fill=(30, 30, 30))
    draw.circle((cx+15, cy-65), 8, fill=(30, 30, 30))

    # Carrot nose
    draw.polygon([(cx-10, cy-40), (cx+20, cy-35), (cx-5, cy-30)], fill=(255, 140, 0))

    # Stick arms
    draw.line([(cx-65, cy), (cx-120, cy-30)], fill=(100, 70, 40), width=6*SCALE)
    draw.line([(cx+65, cy), (cx+120, cy-30)], fill=(100, 70, 40), width=6*SCALE)

    # Top hat
    hat_w = 50
    draw.rectangle([cx-hat_w, cy-120, cx+hat_w, cy-95], fill=(30, 30, 30), outline=(0, 0, 0), width=2*SCALE)
    draw.rectangle([cx-hat_w-15, cy-95, cx+hat_w+15, cy-85], fill=(30, 30, 30), outline=(0, 0, 0), width=2*SCALE)

    save_icon(img, 'deco-pet-snowman.png')

def create_deco_pet_fairy():
    """Tiny glowing fairy"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-100, cy-100, cx+100, cy+100], fill=(255, 200, 100, 100))
    glow = apply_blur(glow, 30)
    img = composite_layer(img, glow, 180)

    # Body (small ball)
    draw.ellipse([cx-20, cy-20, cx+20, cy+20], fill=(255, 200, 100), outline=(200, 150, 50), width=2*SCALE)

    # Wings (translucent butterfly)
    draw.ellipse([cx-50, cy-40, cx-10, cy+10], fill=(200, 220, 255, 200), outline=(100, 150, 200), width=2*SCALE)
    draw.ellipse([cx+10, cy-40, cx+50, cy+10], fill=(200, 220, 255, 200), outline=(100, 150, 200), width=2*SCALE)

    # Sparkle trail
    sparkle_pts = [(cx+30, cy+30), (cx+60, cy+60), (cx+80, cy+50)]
    for sx, sy in sparkle_pts:
        draw.polygon([
            (sx, sy-8),
            (sx+8, sy),
            (sx, sy+8),
            (sx-8, sy)
        ], fill=(255, 255, 200))

    save_icon(img, 'deco-pet-fairy.png')

def create_deco_pet_mini_croc():
    """Small green crocodile"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Body (elongated)
    draw.ellipse([cx-80, cy-30, cx+80, cy+60], fill=(80, 150, 80), outline=(50, 100, 50), width=3*SCALE)

    # Head
    draw.ellipse([cx-50, cy-70, cx+50, cy-10], fill=(80, 150, 80), outline=(50, 100, 50), width=3*SCALE)

    # Snout
    draw.ellipse([cx-30, cy-65, cx+50, cy-25], fill=(100, 170, 100))

    # Back spikes (dots)
    for i in range(7):
        spike_x = cx - 60 + i * 20
        draw.circle((spike_x, cy-45), 8, fill=(60, 120, 60))

    # Smile showing teeth
    draw.line([(cx-20, cy-35), (cx+40, cy-30)], fill=(50, 100, 50), width=4*SCALE)

    # Teeth
    for i in range(4):
        tx = cx - 10 + i * 15
        draw.polygon([(tx-5, cy-30), (tx+5, cy-30), (tx, cy-20)], fill=(250, 250, 250))

    # Eyes
    draw.circle((cx-20, cy-60), 12, fill=(0, 0, 0))
    draw.circle((cx+15, cy-60), 12, fill=(0, 0, 0))
    draw.circle((cx-15, cy-60), 5, fill=(100, 255, 100))
    draw.circle((cx+20, cy-60), 5, fill=(100, 255, 100))

    # Stubby legs
    for x_off in [-50, -20, 30, 60]:
        draw.ellipse([cx+x_off-15, cy+50, cx+x_off+15, cy+85], fill=(80, 150, 80))

    # Tail
    draw.line([(cx+70, cy+30), (cx+130, cy+20), (cx+150, cy-20), (cx+130, cy-60)], 
               fill=(80, 150, 80), width=20*SCALE)

    save_icon(img, 'deco-pet-mini-croc.png')

def create_deco_pet_owl():
    """Small brown owl"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 + 20

    # Body
    draw.ellipse([cx-50, cy-20, cx+50, cy+90], fill=(120, 80, 40), outline=(80, 50, 20), width=3*SCALE)

    # Head
    draw.ellipse([cx-60, cy-80, cx+60, cy], fill=(120, 80, 40), outline=(80, 50, 20), width=3*SCALE)

    # Big round yellow eyes
    draw.ellipse([cx-40, cy-60, cx-10, cy-30], fill=(255, 200, 0), outline=(180, 140, 0), width=3*SCALE)
    draw.ellipse([cx+10, cy-60, cx+40, cy-30], fill=(255, 200, 0), outline=(180, 140, 0), width=3*SCALE)

    # Pupils
    draw.circle((cx-25, cy-45), 12, fill=(0, 0, 0))
    draw.circle((cx+25, cy-45), 12, fill=(0, 0, 0))

    # Eyebrows (feather tufts)
    draw.polygon([(cx-45, cy-70), (cx-35, cy-80), (cx-30, cy-65)], fill=(100, 60, 20))
    draw.polygon([(cx+45, cy-70), (cx+35, cy-80), (cx+30, cy-65)], fill=(100, 60, 20))

    # Beak
    draw.polygon([(cx-10, cy-15), (cx+10, cy-15), (cx, cy+5)], fill=(200, 150, 0))

    # Folded wings
    draw.ellipse([cx-60, cy-20, cx-20, cy+60], fill=(100, 60, 20))
    draw.ellipse([cx+20, cy-20, cx+60, cy+60], fill=(100, 60, 20))

    # Feet/perch
    draw.line([(cx-20, cy+90), (cx-20, cy+120)], fill=(150, 120, 80), width=6*SCALE)
    draw.line([(cx+20, cy+90), (cx+20, cy+120)], fill=(150, 120, 80), width=6*SCALE)

    save_icon(img, 'deco-pet-owl.png')

def create_deco_pet_magic_orb():
    """Floating purple crystal orb"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2 - 30

    # Main orb (purple)
    draw.ellipse([cx-70, cy-70, cx+70, cy+70], fill=(100, 50, 150), outline=(150, 80, 200), width=5*SCALE)

    # Inner glow swirl
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-70, cy-70, cx+70, cy+70], fill=(150, 100, 200, 150))
    glow = apply_blur(glow, 25)
    img = composite_layer(img, glow, 200)

    # Inner spiral effect
    for i in range(20):
        angle = i * 18
        r = 40 - i
        x = cx + r * math.cos(math.radians(angle))
        y = cy + r * math.sin(math.radians(angle))
        draw.circle((x, y), 3, fill=(200, 150, 255))

    # Highlight shine
    draw.ellipse([cx-30, cy-40, cx+10, cy-10], fill=(200, 180, 255, 200))

    # Sparkles rotating around
    for i in range(8):
        angle = i * 45
        sx = cx + 100 * math.cos(math.radians(angle))
        sy = cy + 100 * math.sin(math.radians(angle))
        draw.polygon([
            (sx, sy-8),
            (sx+8, sy),
            (sx, sy+8),
            (sx-8, sy)
        ], fill=(200, 150, 255))

    save_icon(img, 'deco-pet-magic-orb.png')

print("\n=== PET ITEMS (27-38) ===")
create_deco_pet_mini_dragon()
create_deco_pet_kitty()
create_deco_pet_ghost()
create_deco_pet_robot()
create_deco_pet_star()
create_deco_pet_slime()
create_deco_pet_phoenix()
create_deco_pet_snowman()
create_deco_pet_fairy()
create_deco_pet_mini_croc()
create_deco_pet_owl()
create_deco_pet_magic_orb()


# ============================================================================
# EMOTE ITEMS (39-52) - Floating bubbles
# ============================================================================

def create_shop_music():
    """Musical notes with motion"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Motion lines
    for i in range(3):
        x_off = i * 30
        draw.line([(cx+60+x_off, cy-50-i*10), (cx+100+x_off, cy-40-i*10)], fill=(150, 100, 200), width=4*SCALE)

    # First note (♪)
    note1_x, note1_y = cx - 40, cy + 30
    # Note head
    draw.ellipse([note1_x-15, note1_y, note1_x+15, note1_y+30], fill=(100, 100, 200), outline=(50, 50, 150), width=2*SCALE)
    # Stem
    draw.line([(note1_x+15, note1_y), (note1_x+15, note1_y-80)], fill=(100, 100, 200), width=4*SCALE)
    # Flag
    draw.polygon([(note1_x+15, note1_y-80), (note1_x+40, note1_y-60), (note1_x+15, note1_y-60)], fill=(100, 100, 200))

    # Second note (♫)
    note2_x, note2_y = cx + 40, cy - 30
    draw.ellipse([note2_x-15, note2_y, note2_x+15, note2_y+30], fill=(100, 100, 200), outline=(50, 50, 150), width=2*SCALE)
    draw.line([(note2_x+15, note2_y), (note2_x+15, note2_y-80)], fill=(100, 100, 200), width=4*SCALE)
    draw.polygon([(note2_x+15, note2_y-80), (note2_x+40, note2_y-60), (note2_x+15, note2_y-60)], fill=(100, 100, 200))
    draw.polygon([(note2_x+15, note2_y-60), (note2_x+40, note2_y-40), (note2_x+15, note2_y-40)], fill=(100, 100, 200))

    # Third note
    note3_x, note3_y = cx - 20, cy - 80
    draw.ellipse([note3_x-15, note3_y, note3_x+15, note3_y+30], fill=(200, 100, 150), outline=(150, 50, 100), width=2*SCALE)
    draw.line([(note3_x+15, note3_y), (note3_x+15, note3_y-60)], fill=(200, 100, 150), width=4*SCALE)
    draw.polygon([(note3_x+15, note3_y-60), (note3_x+40, note3_y-40), (note3_x+15, note3_y-40)], fill=(200, 100, 150))

    save_icon(img, 'shop-music.png')

def create_shop_heart():
    """Floating hearts"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Large heart (center)
    hx, hy = cx, cy + 20
    draw.ellipse([hx-60, hy-70, hx-20, hy-10], fill=(255, 50, 100))
    draw.ellipse([hx+20, hy-70, hx+60, hy-10], fill=(255, 50, 100))
    draw.polygon([(hx-60, hy-10), (hx+60, hy-10), (hx, hy+80)], fill=(255, 50, 100))

    # Medium heart (upper right)
    hx2, hy2 = cx + 90, cy - 60
    draw.ellipse([hx2-40, hy2-50, hx2-10, hy2], fill=(255, 100, 150))
    draw.ellipse([hx2+10, hy2-50, hx2+40, hy2], fill=(255, 100, 150))
    draw.polygon([(hx2-40, hy2), (hx2+40, hy2), (hx2, hy2+60)], fill=(255, 100, 150))

    # Small heart (lower left)
    hx3, hy3 = cx - 80, cy + 70
    draw.ellipse([hx3-25, hy3-30, hx3+5, hy3], fill=(255, 150, 180))
    draw.ellipse([hx3+15, hy3-30, hx3+45, hy3], fill=(255, 150, 180))
    draw.polygon([(hx3-25, hy3), (hx3+45, hy3), (hx3+10, hy3+40)], fill=(255, 150, 180))

    # Tiny heart (upper left)
    hx4, hy4 = cx - 70, cy - 40
    draw.ellipse([hx4-15, hy4-20, hx4+5, hy4], fill=(255, 100, 150))
    draw.ellipse([hx4+15, hy4-20, hx4+35, hy4], fill=(255, 100, 150))
    draw.polygon([(hx4-15, hy4), (hx4+35, hy4), (hx4+10, hy4+25)], fill=(255, 100, 150))

    save_icon(img, 'shop-heart.png')

def create_bubble_base(icon_content_func):
    """Helper to create speech bubble with content"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # White bubble background
    bubble_x, bubble_y = cx, cy - 40
    bubble_w, bubble_h = 160, 140

    # Rounded rectangle (speech bubble)
    draw.rectangle([bubble_x - bubble_w//2, bubble_y - bubble_h//2,
                   bubble_x + bubble_w//2, bubble_y + bubble_h//2],
                  fill=(255, 255, 255), outline=(200, 200, 200), width=4*SCALE)

    # Round corners
    corner_r = 30
    for qx, qy in [(bubble_x - bubble_w//2 + corner_r, bubble_y - bubble_h//2 + corner_r),
                    (bubble_x + bubble_w//2 - corner_r, bubble_y - bubble_h//2 + corner_r),
                    (bubble_x - bubble_w//2 + corner_r, bubble_y + bubble_h//2 - corner_r),
                    (bubble_x + bubble_w//2 - corner_r, bubble_y + bubble_h//2 - corner_r)]:
        draw.ellipse([qx-corner_r, qy-corner_r, qx+corner_r, qy+corner_r],
                    fill=(255, 255, 255), outline=(200, 200, 200), width=4*SCALE)

    # Pointer tail (lower left)
    pointer_pts = [(bubble_x - bubble_w//2 + 20, bubble_y + bubble_h//2),
                  (bubble_x - bubble_w//2 - 40, bubble_y + bubble_h//2 + 60),
                  (bubble_x - bubble_w//2, bubble_y + bubble_h//2)]
    draw.polygon(pointer_pts, fill=(255, 255, 255), outline=(200, 200, 200))

    # Call content function to draw inside bubble
    icon_content_func(img, bubble_x, bubble_y)

    return img

def emote_victory(img, cx, cy):
    """V sign hand"""
    draw = ImageDraw.Draw(img, 'RGBA')
    # Hand position
    draw.ellipse([cx-30, cy-40, cx+30, cy], fill=(255, 200, 150), outline=(200, 150, 100), width=2*SCALE)
    # Two fingers (V)
    draw.line([(cx-15, cy), (cx-20, cy+60)], fill=(255, 200, 150), width=20*SCALE)
    draw.line([(cx+15, cy), (cx+20, cy+60)], fill=(255, 200, 150), width=20*SCALE)

def create_deco_emote_victory():
    img = create_bubble_base(emote_victory)
    save_icon(img, 'deco-emote-victory.png')

def emote_laugh(img, cx, cy):
    """Laughing face"""
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.ellipse([cx-50, cy-50, cx+50, cy+50], fill=(255, 200, 50), outline=(200, 150, 0), width=3*SCALE)
    # Closed happy eyes
    draw.arc([cx-35, cy-30, cx-15, cy-10], 0, 180, fill=(0, 0, 0), width=5*SCALE)
    draw.arc([cx+15, cy-30, cx+35, cy-10], 0, 180, fill=(0, 0, 0), width=5*SCALE)
    # Open mouth
    draw.arc([cx-30, cy, cx+30, cy+40], 0, 180, fill=(0, 0, 0), width=5*SCALE)
    # Tears of joy
    draw.ellipse([cx-30, cy+40, cx-20, cy+60], fill=(100, 200, 255))
    draw.ellipse([cx+20, cy+40, cx+30, cy+60], fill=(100, 200, 255))

def create_deco_emote_laugh():
    img = create_bubble_base(emote_laugh)
    save_icon(img, 'deco-emote-laugh.png')

def emote_angry(img, cx, cy):
    """Angry face"""
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.ellipse([cx-50, cy-50, cx+50, cy+50], fill=(255, 50, 50), outline=(200, 20, 20), width=3*SCALE)
    # Angry eyes
    draw.polygon([(cx-35, cy-25), (cx-15, cy-25), (cx-30, cy-10)], fill=(0, 0, 0))
    draw.polygon([(cx+35, cy-25), (cx+15, cy-25), (cx+30, cy-10)], fill=(0, 0, 0))
    # Furrowed brows
    draw.line([(cx-40, cy-35), (cx-20, cy-40)], fill=(0, 0, 0), width=4*SCALE)
    draw.line([(cx+40, cy-35), (cx+20, cy-40)], fill=(0, 0, 0), width=4*SCALE)
    # Angry mouth
    draw.arc([cx-30, cy, cx+30, cy+40], 180, 360, fill=(0, 0, 0), width=5*SCALE)
    # Popping vein
    draw.line([(cx, cy-60), (cx, cy-75)], fill=(200, 20, 20), width=6*SCALE)

def create_deco_emote_angry():
    img = create_bubble_base(emote_angry)
    save_icon(img, 'deco-emote-angry.png')

def emote_sad(img, cx, cy):
    """Sad face"""
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.ellipse([cx-50, cy-50, cx+50, cy+50], fill=(100, 150, 255), outline=(50, 100, 200), width=3*SCALE)
    # Sad eyes
    draw.ellipse([cx-35, cy-30, cx-15, cy-10], fill=(0, 0, 0))
    draw.ellipse([cx+15, cy-30, cx+35, cy-10], fill=(0, 0, 0))
    # Teardrop
    draw.ellipse([cx-28, cy+5, cx-15, cy+35], fill=(100, 150, 255), outline=(50, 100, 200), width=2*SCALE)
    # Sad mouth
    draw.arc([cx-30, cy-10, cx+30, cy+20], 180, 360, fill=(0, 0, 0), width=5*SCALE)

def create_deco_emote_sad():
    img = create_bubble_base(emote_sad)
    save_icon(img, 'deco-emote-sad.png')

def emote_heart_bubble(img, cx, cy):
    """Red heart"""
    draw = ImageDraw.Draw(img, 'RGBA')
    hx, hy = cx, cy
    draw.ellipse([hx-45, hy-55, hx-15, hy-10], fill=(255, 50, 100))
    draw.ellipse([hx+15, hy-55, hx+45, hy-10], fill=(255, 50, 100))
    draw.polygon([(hx-45, hy-10), (hx+45, hy-10), (hx, hy+60)], fill=(255, 50, 100))

def create_deco_emote_heart_bubble():
    img = create_bubble_base(emote_heart_bubble)
    save_icon(img, 'deco-emote-heart-bubble.png')

def emote_star_bubble(img, cx, cy):
    """Golden star"""
    draw = ImageDraw.Draw(img, 'RGBA')
    star_points = []
    for i in range(10):
        angle = i * math.pi / 5
        r = 50 if i % 2 == 0 else 25
        star_points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(star_points, fill=(255, 215, 0), outline=(200, 150, 0), width=2*SCALE)

def create_deco_emote_star_bubble():
    img = create_bubble_base(emote_star_bubble)
    save_icon(img, 'deco-emote-star-bubble.png')

def emote_fire_bubble(img, cx, cy):
    """Orange flame"""
    draw = ImageDraw.Draw(img, 'RGBA')
    # Main flame
    flame_pts = [
        (cx, cy+50),
        (cx-40, cy),
        (cx-30, cy-40),
        (cx, cy-60),
        (cx+30, cy-40),
        (cx+40, cy)
    ]
    draw.polygon(flame_pts, fill=(255, 100, 0), outline=(200, 60, 0), width=2*SCALE)
    # Inner yellow
    inner_pts = [
        (cx, cy+30),
        (cx-20, cy-5),
        (cx-10, cy-35),
        (cx, cy-50),
        (cx+10, cy-35),
        (cx+20, cy-5)
    ]
    draw.polygon(inner_pts, fill=(255, 180, 50))

def create_deco_emote_fire_bubble():
    img = create_bubble_base(emote_fire_bubble)
    save_icon(img, 'deco-emote-fire-bubble.png')

def emote_rainbow_bubble(img, cx, cy):
    """Rainbow gradient"""
    draw = ImageDraw.Draw(img, 'RGBA')
    colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
    for i, color in enumerate(colors):
        segment_w = 100 // 7
        draw.rectangle([cx - 50 + i*segment_w, cy-50, cx - 50 + (i+1)*segment_w, cy+50],
                      fill=color, outline=None)

def create_deco_emote_rainbow_bubble():
    img = create_bubble_base(emote_rainbow_bubble)
    save_icon(img, 'deco-emote-rainbow-bubble.png')

def emote_reading_bubble(img, cx, cy):
    """Open book"""
    draw = ImageDraw.Draw(img, 'RGBA')
    # Book cover
    draw.rectangle([cx-50, cy-40, cx+50, cy+40], fill=(180, 100, 50), outline=(120, 60, 30), width=3*SCALE)
    # Spine
    draw.line([(cx, cy-40), (cx, cy+40)], fill=(120, 60, 30), width=4*SCALE)
    # Pages
    draw.line([(cx-10, cy-35), (cx-10, cy+35)], fill=(240, 240, 220), width=2*SCALE)
    draw.line([(cx+10, cy-35), (cx+10, cy+35)], fill=(240, 240, 220), width=2*SCALE)
    # Text lines
    for y_off in [-25, -10, 5, 20]:
        draw.line([(cx-35, cy+y_off), (cx-15, cy+y_off)], fill=(100, 100, 100), width=2*SCALE)
        draw.line([(cx+15, cy+y_off), (cx+35, cy+y_off)], fill=(100, 100, 100), width=2*SCALE)

def create_deco_emote_reading_bubble():
    img = create_bubble_base(emote_reading_bubble)
    save_icon(img, 'deco-emote-reading-bubble.png')

def emote_idea_bulb(img, cx, cy):
    """Light bulb"""
    draw = ImageDraw.Draw(img, 'RGBA')
    # Bulb
    draw.ellipse([cx-40, cy-60, cx+40, cy+20], fill=(255, 255, 0), outline=(200, 180, 0), width=3*SCALE)
    # Rays
    for angle in range(0, 360, 45):
        rx = cx + 70 * math.cos(math.radians(angle))
        ry = cy + 70 * math.sin(math.radians(angle))
        draw.line([(cx + 45 * math.cos(math.radians(angle)), cy + 45 * math.sin(math.radians(angle))),
                  (rx, ry)], fill=(255, 255, 0), width=6*SCALE)
    # Base
    draw.rectangle([cx-25, cy+20, cx+25, cy+50], fill=(200, 100, 0), outline=(150, 70, 0), width=2*SCALE)
    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-40, cy-60, cx+40, cy+20], fill=(255, 255, 0, 150))
    glow = apply_blur(glow, 20)
    img = composite_layer(img, glow, 200)

def create_deco_emote_idea_bulb():
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2
    emote_idea_bulb(img, cx, cy)
    save_icon(img, 'deco-emote-idea-bulb.png')

def emote_music(img, cx, cy):
    """Musical notes"""
    draw = ImageDraw.Draw(img, 'RGBA')
    # Note 1
    note_x1 = cx - 30
    draw.ellipse([note_x1-12, cy, note_x1+12, cy+25], fill=(100, 100, 200))
    draw.line([(note_x1+12, cy), (note_x1+12, cy-60)], fill=(100, 100, 200), width=3*SCALE)
    draw.polygon([(note_x1+12, cy-60), (note_x1+35, cy-40), (note_x1+12, cy-40)], fill=(100, 100, 200))
    # Note 2
    note_x2 = cx + 30
    draw.ellipse([note_x2-12, cy-20, note_x2+12, cy+5], fill=(200, 100, 150))
    draw.line([(note_x2+12, cy-20), (note_x2+12, cy-80)], fill=(200, 100, 150), width=3*SCALE)
    draw.polygon([(note_x2+12, cy-80), (note_x2+35, cy-60), (note_x2+12, cy-60)], fill=(200, 100, 150))

def create_deco_emote_music():
    img = create_bubble_base(emote_music)
    save_icon(img, 'deco-emote-music.png')

def emote_crown(img, cx, cy):
    """Golden crown"""
    draw = ImageDraw.Draw(img, 'RGBA')
    # Base band
    draw.ellipse([cx-50, cy+10, cx+50, cy+40], fill=(218, 165, 32), outline=(139, 105, 20), width=2*SCALE)
    # Peaks
    for i, px_off in enumerate([-30, -10, 10, 30]):
        peak_x = cx + px_off
        draw.polygon([(peak_x-15, cy+10), (peak_x, cy-30), (peak_x+15, cy+10)], fill=(218, 165, 32))
        # Jewel
        jc = (255, 0, 0) if i % 2 == 0 else (0, 100, 200)
        draw.circle((peak_x, cy-15), 8, fill=jc)

def create_deco_emote_crown():
    img = create_bubble_base(emote_crown)
    save_icon(img, 'deco-emote-crown.png')

print("\n=== EMOTE ITEMS (39-52) ===")
create_shop_music()
create_shop_heart()
create_deco_emote_victory()
create_deco_emote_laugh()
create_deco_emote_angry()
create_deco_emote_sad()
create_deco_emote_heart_bubble()
create_deco_emote_star_bubble()
create_deco_emote_fire_bubble()
create_deco_emote_rainbow_bubble()
create_deco_emote_reading_bubble()
create_deco_emote_idea_bulb()
create_deco_emote_music()
create_deco_emote_crown()


# ============================================================================
# WEAPON ITEMS (53-64)
# ============================================================================

def create_deco_weapon_shiny_sword():
    """Silver sword with blue glow"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.polygon([(cx, cy-200), (cx-30, cy+100), (cx+30, cy+100)], fill=(0, 150, 255, 100))
    glow = apply_blur(glow, 20)
    img = composite_layer(img, glow, 180)

    # Blade (silver)
    draw.polygon([(cx, cy-200), (cx-25, cy+100), (cx+25, cy+100)], fill=(200, 200, 220), outline=(100, 100, 120), width=3*SCALE)
    
    # Blade highlight
    draw.polygon([(cx-5, cy-150), (cx-15, cy+50), (cx+5, cy+50)], fill=(240, 240, 255, 200))

    # Crossguard (golden)
    guard_w = 80
    draw.rectangle([cx-guard_w, cy+95, cx+guard_w, cy+130], fill=(218, 165, 32), outline=(139, 105, 20), width=3*SCALE)

    # Grip (leather)
    draw.rectangle([cx-15, cy+130, cx+15, cy+180], fill=(150, 100, 50), outline=(100, 70, 30), width=2*SCALE)

    # Grip wrapping
    for i in range(0, 50, 10):
        draw.line([(cx-15, cy+130+i), (cx+15, cy+130+i)], fill=(100, 70, 30), width=2*SCALE)

    # Pommel (golden)
    draw.ellipse([cx-20, cy+175, cx+20, cy+220], fill=(218, 165, 32), outline=(139, 105, 20), width=2*SCALE)

    save_icon(img, 'deco-weapon-shiny-sword.png')

def create_deco_weapon_magic_wand():
    """Dark wood wand with glowing star"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Wand shaft
    draw.rectangle([cx-8, cy-150, cx+8, cy+150], fill=(100, 60, 30), outline=(60, 35, 15), width=2*SCALE)

    # Wood grain
    for i in range(-140, 140, 20):
        draw.line([(cx-8, cy+i), (cx+8, cy+i)], fill=(80, 45, 20), width=1*SCALE)

    # Star tip (glowing)
    star_x, star_y = cx, cy - 160
    star_points = []
    for i in range(10):
        angle = i * math.pi / 5
        r = 35 if i % 2 == 0 else 18
        star_points.append((star_x + r * math.cos(angle), star_y + r * math.sin(angle)))
    draw.polygon(star_points, fill=(255, 200, 0), outline=(200, 150, 0), width=2*SCALE)

    # Glow around star
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.polygon(star_points, fill=(255, 200, 0, 150))
    glow = apply_blur(glow, 20)
    img = composite_layer(img, glow, 200)

    # Sparkle trail from tip
    for i in range(5):
        spark_y = star_y + 30 + i * 30
        draw.polygon([
            (star_x, spark_y-8),
            (star_x+8, spark_y),
            (star_x, spark_y+8),
            (star_x-8, spark_y)
        ], fill=(255, 255, 100))

    save_icon(img, 'deco-weapon-magic-wand.png')

def create_deco_weapon_gold_shield():
    """Round golden shield with emblem"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main shield (circular)
    draw.ellipse([cx-100, cy-120, cx+100, cy+120], fill=(218, 165, 32), outline=(139, 105, 20), width=6*SCALE)

    # Shield highlight
    draw.ellipse([cx-80, cy-100, cx-20, cy-40], fill=(255, 215, 100, 200))

    # Riveted edge
    for angle in range(0, 360, 30):
        rx = cx + 110 * math.cos(math.radians(angle))
        ry = cy + 110 * math.sin(math.radians(angle))
        draw.circle((rx, ry), 10, fill=(139, 105, 20), outline=(80, 60, 20), width=2*SCALE)

    # Lion emblem (shield center)
    # Lion head
    draw.ellipse([cx-50, cy-60, cx+50, cy+40], fill=(255, 180, 0), outline=(200, 120, 0), width=3*SCALE)
    # Mane
    for angle in range(0, 360, 30):
        mx = cx + 65 * math.cos(math.radians(angle))
        my = cy + 65 * math.sin(math.radians(angle))
        draw.polygon([(cx, cy), (mx-10, my-10), (mx+10, my+10)], fill=(255, 180, 0))
    # Eyes
    draw.circle((cx-20, cy-15), 8, fill=(0, 0, 0))
    draw.circle((cx+20, cy-15), 8, fill=(0, 0, 0))

    save_icon(img, 'deco-weapon-gold-shield.png')

def create_deco_weapon_energy_gun():
    """Sci-fi blaster"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main body
    draw.rectangle([cx-70, cy-20, cx+50, cy+40], fill=(80, 80, 100), outline=(40, 40, 60), width=3*SCALE)

    # Barrel (dark)
    draw.rectangle([cx+40, cy-15, cx+100, cy+35], fill=(60, 60, 80), outline=(30, 30, 50), width=2*SCALE)

    # Energy cell (glowing cyan)
    cell_x = cx - 30
    draw.ellipse([cell_x-25, cy-30, cell_x+25, cy+50], fill=(0, 200, 255), outline=(0, 150, 200), width=3*SCALE)
    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cell_x-25, cy-30, cell_x+25, cy+50], fill=(0, 200, 255, 150))
    glow = apply_blur(glow, 15)
    img = composite_layer(img, glow, 200)

    # Trigger
    draw.rectangle([cx-20, cy+30, cx-5, cy+60], fill=(100, 100, 120), outline=(50, 50, 70), width=2*SCALE)

    # Barrel glow
    barrel_glow = create_image()
    barrel_glow_draw = ImageDraw.Draw(barrel_glow, 'RGBA')
    barrel_glow_draw.rectangle([cx+40, cy-15, cx+100, cy+35], fill=(0, 150, 200, 100))
    barrel_glow = apply_blur(barrel_glow, 15)
    img = composite_layer(img, barrel_glow, 180)

    save_icon(img, 'deco-weapon-energy-gun.png')

def create_deco_weapon_ninja_star():
    """Silver 4-pointed shuriken"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # 4 blades
    for i in range(4):
        angle = i * 90
        # Blade points
        blade_pts = [
            (cx, cy),
            (cx + 80 * math.cos(math.radians(angle)), cy + 80 * math.sin(math.radians(angle))),
            (cx + 100 * math.cos(math.radians(angle+15)), cy + 100 * math.sin(math.radians(angle+15))),
            (cx + 100 * math.cos(math.radians(angle-15)), cy + 100 * math.sin(math.radians(angle-15)))
        ]
        draw.polygon(blade_pts, fill=(200, 200, 220), outline=(100, 100, 120), width=2*SCALE)
        # Highlight
        highlight_pts = [
            (cx + 30 * math.cos(math.radians(angle)), cy + 30 * math.sin(math.radians(angle))),
            (cx + 60 * math.cos(math.radians(angle)), cy + 60 * math.sin(math.radians(angle))),
            (cx + 70 * math.cos(math.radians(angle+10)), cy + 70 * math.sin(math.radians(angle+10))),
        ]
        draw.polygon(highlight_pts, fill=(240, 240, 255, 200))

    # Center circle
    draw.ellipse([cx-20, cy-20, cx+20, cy+20], fill=(200, 200, 220), outline=(100, 100, 120), width=3*SCALE)

    save_icon(img, 'deco-weapon-ninja-star.png')

def create_deco_weapon_pirate_sword():
    """Curved cutlass"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Curved blade
    blade_pts = []
    for i in range(20):
        angle = -20 + i * 2
        x_pos = cx - 200 + i * 20
        y_pos = cy + 80 * math.sin(math.radians(angle))
        blade_pts.append((x_pos, y_pos))
    draw.line(blade_pts, fill=(200, 200, 220), width=30*SCALE)
    
    # Blade highlight
    draw.line(blade_pts, fill=(240, 240, 255, 200), width=15*SCALE)

    # Ornate gold handle
    handle_x = cx + 80
    # Crossguard
    draw.rectangle([handle_x-50, cy-30, handle_x+50, cy+30], fill=(218, 165, 32), outline=(139, 105, 20), width=4*SCALE)
    # Grip
    draw.rectangle([handle_x-15, cy+20, handle_x+15, cy+120], fill=(150, 100, 50), outline=(100, 70, 30), width=2*SCALE)
    # Pommel
    draw.circle((handle_x, cy+130), 20, fill=(218, 165, 32))

    save_icon(img, 'deco-weapon-magic-book.png')

def create_deco_weapon_magic_book():
    """Thick glowing book"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Book cover (purple)
    book_w, book_h = 80, 120
    draw.rectangle([cx-book_w, cy-book_h, cx+book_w, cy+book_h], fill=(100, 50, 150), outline=(150, 80, 200), width=4*SCALE)

    # Spine
    draw.rectangle([cx-10, cy-book_h, cx+10, cy+book_h], fill=(80, 30, 130))

    # Mystical runes (glowing symbols)
    for i, (rx, ry) in enumerate([(-40, -60), (40, -60), (0, 0), (-30, 60), (30, 60)]):
        rune_x, rune_y = cx+rx, cy+ry
        draw.polygon([
            (rune_x, rune_y-12),
            (rune_x+12, rune_y),
            (rune_x, rune_y+12),
            (rune_x-12, rune_y)
        ], fill=(200, 150, 255), outline=(255, 200, 255), width=2*SCALE)

    # Glow effect
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.rectangle([cx-book_w, cy-book_h, cx+book_w, cy+book_h], fill=(150, 100, 200, 100))
    glow = apply_blur(glow, 25)
    img = composite_layer(img, glow, 180)

    # Floating sparkles
    for angle in range(0, 360, 60):
        sx = cx + 130 * math.cos(math.radians(angle))
        sy = cy + 130 * math.sin(math.radians(angle))
        draw.polygon([
            (sx, sy-10),
            (sx+10, sy),
            (sx, sy+10),
            (sx-10, sy)
        ], fill=(200, 150, 255))

    save_icon(img, 'deco-weapon-magic-book.png')

def create_deco_weapon_gold_key():
    """Ornate golden key"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Key shaft
    draw.rectangle([cx-80, cy-15, cx+80, cy+15], fill=(218, 165, 32), outline=(139, 105, 20), width=3*SCALE)

    # Key bow (circular handle)
    bow_x = cx - 90
    draw.ellipse([bow_x-40, cy-40, bow_x+40, cy+40], fill=(218, 165, 32), outline=(139, 105, 20), width=4*SCALE)

    # Teeth (key end)
    tooth_x = cx + 90
    draw.rectangle([tooth_x-20, cy-20, tooth_x+20, cy+20], fill=(218, 165, 32), outline=(139, 105, 20), width=2*SCALE)
    draw.rectangle([tooth_x-20, cy-35, tooth_x-5, cy-20], fill=(218, 165, 32))
    draw.rectangle([tooth_x+5, cy+20, tooth_x+20, cy+35], fill=(218, 165, 32))

    # Gem inlay on bow
    draw.ellipse([bow_x-20, cy-20, bow_x+20, cy+20], fill=(255, 0, 150), outline=(200, 0, 120), width=2*SCALE)
    draw.ellipse([bow_x-12, cy-12, bow_x+12, cy+12], fill=(255, 100, 200))

    # Highlight
    draw.polygon([(cx-60, cy-10), (cx+60, cy-10), (cx+70, cy+5)], fill=(255, 215, 100, 150))

    save_icon(img, 'deco-weapon-gold-key.png')

def create_deco_weapon_reading_staff():
    """Staff with glowing crystal book"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Staff shaft (wood)
    draw.rectangle([cx-10, cy-20, cx+10, cy+180], fill=(100, 60, 30), outline=(60, 35, 15), width=2*SCALE)

    # Wood grain
    for i in range(0, 200, 25):
        draw.line([(cx-10, cy+i), (cx+10, cy+i)], fill=(80, 45, 20), width=1*SCALE)

    # Crystal/book top (glowing)
    crystal_y = cy - 80
    draw.rectangle([cx-40, crystal_y-50, cx+40, crystal_y+30], fill=(100, 150, 200), outline=(50, 100, 200), width=3*SCALE)
    # Pages detail
    draw.line([(cx, crystal_y-50), (cx, crystal_y+30)], fill=(150, 200, 255), width=3*SCALE)
    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.rectangle([cx-40, crystal_y-50, cx+40, crystal_y+30], fill=(100, 150, 200, 150))
    glow = apply_blur(glow, 20)
    img = composite_layer(img, glow, 200)

    save_icon(img, 'deco-weapon-reading-staff.png')

def create_deco_weapon_knowledge_orb():
    """Floating blue energy sphere"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main orb
    draw.ellipse([cx-80, cy-80, cx+80, cy+80], fill=(80, 150, 200), outline=(40, 100, 200), width=5*SCALE)

    # Inner swirl pattern
    for i in range(20):
        angle = i * 18
        r = 50 - i
        x = cx + r * math.cos(math.radians(angle))
        y = cy + r * math.sin(math.radians(angle))
        draw.circle((x, y), 2, fill=(150, 200, 255))

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-80, cy-80, cx+80, cy+80], fill=(80, 150, 200, 150))
    glow = apply_blur(glow, 30)
    img = composite_layer(img, glow, 200)

    # Highlight
    draw.ellipse([cx-40, cy-60, cx+10, cy-20], fill=(200, 230, 255, 180))

    save_icon(img, 'deco-weapon-knowledge-orb.png')

def create_deco_weapon_quest_flag():
    """Red flag on golden pole"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Pole (golden)
    pole_x = cx - 50
    draw.rectangle([pole_x-8, cy-150, pole_x+8, cy+120], fill=(218, 165, 32), outline=(139, 105, 20), width=3*SCALE)

    # Flag (red triangular)
    flag_pts = [
        (pole_x+8, cy-120),
        (pole_x+120, cy-140),
        (pole_x+120, cy-80)
    ]
    draw.polygon(flag_pts, fill=(200, 20, 20), outline=(150, 10, 10), width=3*SCALE)

    # Flag stripes (wind effect)
    for i in range(4):
        stripe_x = pole_x + 20 + i * 25
        draw.line([(stripe_x, cy-130), (stripe_x, cy-90)], fill=(150, 10, 10), width=3*SCALE)

    # Wind lines
    for y_off in [-10, 0, 10]:
        draw.line([(pole_x+130, cy-120+y_off), (pole_x+160, cy-115+y_off)], fill=(200, 200, 200), width=3*SCALE)

    save_icon(img, 'deco-weapon-quest-flag.png')

def create_deco_weapon_trophy():
    """Golden trophy cup"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Cup bowl
    draw.ellipse([cx-70, cy-80, cx+70, cy+20], fill=(218, 165, 32), outline=(139, 105, 20), width=4*SCALE)

    # Cup handles
    draw.arc([cx-80, cy-60, cx-40, cy+20], 270, 90, fill=(218, 165, 32), width=12*SCALE)
    draw.arc([cx+40, cy-60, cx+80, cy+20], 90, 270, fill=(218, 165, 32), width=12*SCALE)

    # Base
    draw.rectangle([cx-80, cy+10, cx+80, cy+50], fill=(218, 165, 32), outline=(139, 105, 20), width=3*SCALE)
    draw.ellipse([cx-90, cy+45, cx+90, cy+65], fill=(218, 165, 32), outline=(139, 105, 20), width=3*SCALE)

    # Star emblem on cup
    star_x, star_y = cx, cy - 30
    star_pts = []
    for i in range(10):
        angle = i * math.pi / 5
        r = 25 if i % 2 == 0 else 12
        star_pts.append((star_x + r * math.cos(angle), star_y + r * math.sin(angle)))
    draw.polygon(star_pts, fill=(255, 200, 0), outline=(200, 150, 0), width=2*SCALE)

    # Shine
    draw.polygon([(cx-50, cy-60), (cx+30, cy-70), (cx+20, cy-20)], fill=(255, 215, 100, 200))

    save_icon(img, 'deco-weapon-trophy.png')

# ============================================================================
# WING ITEMS (65-76)
# ============================================================================

def create_deco_wing_angel():
    """Large white feathered wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left wing feathers
    for layer in range(4):
        start_angle = 90 + layer * 15
        for feather in range(8):
            angle = start_angle + feather * 20
            fx = cx - 200 - layer * 60 + 80 * math.cos(math.radians(angle))
            fy = cy + 100 * math.sin(math.radians(angle))
            feather_color = (250, 250, 255) if layer % 2 == 0 else (230, 230, 240)
            # Feather shape
            draw.ellipse([fx-15, fy-35, fx+15, fy+35], fill=feather_color, outline=(200, 200, 200), width=1*SCALE)

    # Right wing feathers
    for layer in range(4):
        start_angle = 90 - layer * 15
        for feather in range(8):
            angle = start_angle - feather * 20
            fx = cx + 200 + layer * 60 + 80 * math.cos(math.radians(angle))
            fy = cy + 100 * math.sin(math.radians(angle))
            feather_color = (250, 250, 255) if layer % 2 == 0 else (230, 230, 240)
            draw.ellipse([fx-15, fy-35, fx+15, fy+35], fill=feather_color, outline=(200, 200, 200), width=1*SCALE)

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-300, cy-100, cx+300, cy+300], fill=(250, 250, 255, 80))
    glow = apply_blur(glow, 40)
    img = composite_layer(img, glow, 150)

    save_icon(img, 'deco-wing-angel.png')

def create_deco_wing_devil():
    """Dark bat wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left wing membrane
    wing_pts_l = [
        (cx, cy),
        (cx-80, cy-150),
        (cx-200, cy-100),
        (cx-240, cy+50),
        (cx-180, cy+150),
        (cx-80, cy+100)
    ]
    draw.polygon(wing_pts_l, fill=(50, 20, 80), outline=(100, 40, 120), width=3*SCALE)

    # Left wing veins
    for i in range(3):
        vein_x = cx - 50 - i * 50
        draw.line([(cx, cy), (vein_x, cy-100+i*40)], fill=(100, 50, 120), width=2*SCALE)

    # Right wing membrane
    wing_pts_r = [
        (cx, cy),
        (cx+80, cy-150),
        (cx+200, cy-100),
        (cx+240, cy+50),
        (cx+180, cy+150),
        (cx+80, cy+100)
    ]
    draw.polygon(wing_pts_r, fill=(50, 20, 80), outline=(100, 40, 120), width=3*SCALE)

    # Right wing veins
    for i in range(3):
        vein_x = cx + 50 + i * 50
        draw.line([(cx, cy), (vein_x, cy-100+i*40)], fill=(100, 50, 120), width=2*SCALE)

    save_icon(img, 'deco-wing-devil.png')

def create_deco_wing_dragon():
    """Scaly dragon wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left wing
    wing_pts_l = [
        (cx, cy),
        (cx-100, cy-140),
        (cx-220, cy-80),
        (cx-240, cy+80),
        (cx-120, cy+160)
    ]
    draw.polygon(wing_pts_l, fill=(80, 150, 80), outline=(50, 100, 50), width=3*SCALE)

    # Scales (circles)
    for i in range(15):
        scale_angle = i * 12
        scale_r = 80 + i * 8
        sx = cx - 100 - scale_r * math.cos(math.radians(scale_angle))
        sy = cy + scale_r * math.sin(math.radians(scale_angle))
        draw.circle((sx, sy), 12, fill=(100, 170, 100), outline=(60, 120, 60), width=1*SCALE)

    # Right wing
    wing_pts_r = [
        (cx, cy),
        (cx+100, cy-140),
        (cx+220, cy-80),
        (cx+240, cy+80),
        (cx+120, cy+160)
    ]
    draw.polygon(wing_pts_r, fill=(80, 150, 80), outline=(50, 100, 50), width=3*SCALE)

    # Scales
    for i in range(15):
        scale_angle = i * 12
        scale_r = 80 + i * 8
        sx = cx + 100 + scale_r * math.cos(math.radians(scale_angle))
        sy = cy + scale_r * math.sin(math.radians(scale_angle))
        draw.circle((sx, sy), 12, fill=(100, 170, 100), outline=(60, 120, 60), width=1*SCALE)

    # Claw tips
    claw_tip_l = [(cx-240, cy+80), (cx-260, cy+100), (cx-250, cy+60)]
    draw.polygon(claw_tip_l, fill=(60, 120, 60))
    claw_tip_r = [(cx+240, cy+80), (cx+260, cy+100), (cx+250, cy+60)]
    draw.polygon(claw_tip_r, fill=(60, 120, 60))

    save_icon(img, 'deco-wing-dragon.png')

def create_deco_wing_butterfly():
    """Colorful butterfly wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left upper wing
    left_upper_pts = [
        (cx, cy),
        (cx-150, cy-150),
        (cx-180, cy-80),
        (cx-120, cy-20)
    ]
    draw.polygon(left_upper_pts, fill=(255, 140, 0), outline=(200, 100, 0), width=2*SCALE)
    # Pattern
    draw.ellipse([cx-150, cy-120, cx-130, cy-100], fill=(255, 200, 100), outline=None)

    # Left lower wing
    left_lower_pts = [
        (cx, cy),
        (cx-120, cy+20),
        (cx-150, cy+150),
        (cx-100, cy+120)
    ]
    draw.polygon(left_lower_pts, fill=(255, 100, 0), outline=(200, 60, 0), width=2*SCALE)

    # Right upper wing (blue)
    right_upper_pts = [
        (cx, cy),
        (cx+150, cy-150),
        (cx+180, cy-80),
        (cx+120, cy-20)
    ]
    draw.polygon(right_upper_pts, fill=(100, 150, 255), outline=(60, 100, 200), width=2*SCALE)
    draw.ellipse([cx+130, cy-120, cx+150, cy-100], fill=(150, 200, 255), outline=None)

    # Right lower wing
    right_lower_pts = [
        (cx, cy),
        (cx+120, cy+20),
        (cx+150, cy+150),
        (cx+100, cy+120)
    ]
    draw.polygon(right_lower_pts, fill=(100, 120, 255), outline=(60, 80, 200), width=2*SCALE)

    save_icon(img, 'deco-wing-butterfly.png')

def create_deco_wing_fire():
    """Flame wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left flame wing
    left_flame_pts = [
        (cx, cy),
        (cx-200, cy-100),
        (cx-180, cy+50),
        (cx-100, cy+80)
    ]
    draw.polygon(left_flame_pts, fill=(255, 100, 0), outline=(200, 60, 0), width=2*SCALE)
    # Inner yellow
    left_inner_pts = [
        (cx, cy),
        (cx-150, cy-50),
        (cx-120, cy+40),
        (cx-60, cy+60)
    ]
    draw.polygon(left_inner_pts, fill=(255, 180, 50))

    # Right flame wing
    right_flame_pts = [
        (cx, cy),
        (cx+200, cy-100),
        (cx+180, cy+50),
        (cx+100, cy+80)
    ]
    draw.polygon(right_flame_pts, fill=(255, 100, 0), outline=(200, 60, 0), width=2*SCALE)
    right_inner_pts = [
        (cx, cy),
        (cx+150, cy-50),
        (cx+120, cy+40),
        (cx+60, cy+60)
    ]
    draw.polygon(right_inner_pts, fill=(255, 180, 50))

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.polygon(left_flame_pts, fill=(255, 100, 0, 100))
    glow_draw.polygon(right_flame_pts, fill=(255, 100, 0, 100))
    glow = apply_blur(glow, 30)
    img = composite_layer(img, glow, 180)

    save_icon(img, 'deco-wing-fire.png')

def create_deco_wing_ice():
    """Crystal ice wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left ice wing (angular crystalline)
    left_pts = [
        (cx, cy),
        (cx-100, cy-180),
        (cx-180, cy-100),
        (cx-200, cy+80),
        (cx-100, cy+100)
    ]
    draw.polygon(left_pts, fill=(150, 200, 255), outline=(100, 150, 200), width=3*SCALE)

    # Crystal facets
    draw.line([(cx-100, cy-180), (cx-180, cy-100)], fill=(200, 230, 255), width=3*SCALE)
    draw.line([(cx-180, cy-100), (cx-200, cy+80)], fill=(200, 230, 255), width=3*SCALE)

    # Right ice wing
    right_pts = [
        (cx, cy),
        (cx+100, cy-180),
        (cx+180, cy-100),
        (cx+200, cy+80),
        (cx+100, cy+100)
    ]
    draw.polygon(right_pts, fill=(150, 200, 255), outline=(100, 150, 200), width=3*SCALE)

    draw.line([(cx+100, cy-180), (cx+180, cy-100)], fill=(200, 230, 255), width=3*SCALE)
    draw.line([(cx+180, cy-100), (cx+200, cy+80)], fill=(200, 230, 255), width=3*SCALE)

    save_icon(img, 'deco-wing-ice.png')

def create_deco_wing_mech():
    """Mechanical metallic wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left wing panels
    left_main = [
        (cx, cy),
        (cx-140, cy-120),
        (cx-200, cy-60),
        (cx-180, cy+100),
        (cx-80, cy+120)
    ]
    draw.polygon(left_main, fill=(180, 180, 180), outline=(100, 100, 100), width=3*SCALE)

    # Panel divisions
    draw.line([(cx-100, cy-60), (cx-160, cy+40)], fill=(120, 120, 120), width=3*SCALE)
    draw.line([(cx-140, cy-120), (cx-180, cy+100)], fill=(120, 120, 120), width=3*SCALE)

    # Rivets
    for i in range(5):
        riv_x = cx - 100 - i * 20
        riv_y = cy - 40 + i * 30
        draw.circle((riv_x, riv_y), 5, fill=(100, 100, 100))

    # Right wing panels
    right_main = [
        (cx, cy),
        (cx+140, cy-120),
        (cx+200, cy-60),
        (cx+180, cy+100),
        (cx+80, cy+120)
    ]
    draw.polygon(right_main, fill=(180, 180, 180), outline=(100, 100, 100), width=3*SCALE)

    draw.line([(cx+100, cy-60), (cx+160, cy+40)], fill=(120, 120, 120), width=3*SCALE)
    draw.line([(cx+140, cy-120), (cx+180, cy+100)], fill=(120, 120, 120), width=3*SCALE)

    for i in range(5):
        riv_x = cx + 100 + i * 20
        riv_y = cy - 40 + i * 30
        draw.circle((riv_x, riv_y), 5, fill=(100, 100, 100))

    save_icon(img, 'deco-wing-mech.png')

def create_deco_wing_rainbow():
    """Rainbow gradient wings"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Left wing with gradient colors
    colors_l = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0)]
    for i, color in enumerate(colors_l):
        angle_off = 45 + i * 12
        wing_pts = [
            (cx, cy),
            (cx - 100 * math.cos(math.radians(angle_off)), cy - 150 * math.sin(math.radians(angle_off))),
            (cx - 180 * math.cos(math.radians(angle_off)), cy - 80 * math.sin(math.radians(angle_off))),
            (cx - 80 * math.cos(math.radians(angle_off+20)), cy - 120 * math.sin(math.radians(angle_off+20)))
        ]
        draw.polygon(wing_pts, fill=color)

    # Right wing
    colors_r = [(0, 0, 255), (75, 0, 130), (148, 0, 211), (255, 0, 0)]
    for i, color in enumerate(colors_r):
        angle_off = 135 + i * 12
        wing_pts = [
            (cx, cy),
            (cx + 100 * math.cos(math.radians(angle_off)), cy - 150 * math.sin(math.radians(angle_off))),
            (cx + 180 * math.cos(math.radians(angle_off)), cy - 80 * math.sin(math.radians(angle_off))),
            (cx + 80 * math.cos(math.radians(angle_off-20)), cy - 120 * math.sin(math.radians(angle_off-20)))
        ]
        draw.polygon(wing_pts, fill=color)

    save_icon(img, 'deco-wing-rainbow.png')

def create_deco_wing_cape_red():
    """Flowing red cape"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Cape shape (flowing downward)
    cape_pts = [
        (cx-100, cy-150),
        (cx+100, cy-150),
        (cx+140, cy+150),
        (cx, cy+180),
        (cx-140, cy+150)
    ]
    draw.polygon(cape_pts, fill=(200, 20, 20), outline=(150, 10, 10), width=4*SCALE)

    # Cape folds
    for i in range(3):
        fold_x = cx - 80 + i * 80
        draw.line([(fold_x, cy-150), (fold_x + 20, cy+180)], fill=(150, 10, 10), width=6*SCALE)

    # Highlight stripe
    draw.polygon([(cx-80, cy-150), (cx-60, cy-150), (cx+20, cy+180), (cx-20, cy+180)], fill=(255, 100, 100, 150))

    save_icon(img, 'deco-wing-cape-red.png')

def create_deco_wing_cape_purple():
    """Purple cape with stars"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Cape
    cape_pts = [
        (cx-100, cy-150),
        (cx+100, cy-150),
        (cx+140, cy+150),
        (cx, cy+180),
        (cx-140, cy+150)
    ]
    draw.polygon(cape_pts, fill=(100, 50, 150), outline=(70, 30, 120), width=4*SCALE)

    # Folds
    for i in range(3):
        fold_x = cx - 80 + i * 80
        draw.line([(fold_x, cy-150), (fold_x + 20, cy+180)], fill=(70, 30, 120), width=6*SCALE)

    # Star patterns
    for star_y in [cy-100, cy, cy+100]:
        for star_x in [cx-60, cx, cx+60]:
            star_pts = []
            for i in range(10):
                angle = i * math.pi / 5
                r = 12 if i % 2 == 0 else 6
                star_pts.append((star_x + r * math.cos(angle), star_y + r * math.sin(angle)))
            draw.polygon(star_pts, fill=(255, 215, 0))

    save_icon(img, 'deco-wing-cape-purple.png')

def create_deco_wing_jetpack():
    """Mechanical jetpack with flame"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main body
    draw.rectangle([cx-50, cy-80, cx+50, cy+80], fill=(150, 150, 150), outline=(80, 80, 80), width=3*SCALE)

    # Left thruster
    thruster_l_x = cx - 50
    draw.rectangle([thruster_l_x-40, cy-40, thruster_l_x-10, cy+40], fill=(100, 100, 100), outline=(50, 50, 50), width=2*SCALE)

    # Right thruster
    thruster_r_x = cx + 50
    draw.rectangle([thruster_r_x+10, cy-40, thruster_r_x+40, cy+40], fill=(100, 100, 100), outline=(50, 50, 50), width=2*SCALE)

    # Blue flame exhaust (left)
    flame_l = [
        (thruster_l_x-25, cy+40),
        (thruster_l_x-50, cy+140),
        (thruster_l_x, cy+160)
    ]
    draw.polygon(flame_l, fill=(0, 150, 255))
    draw.polygon([(thruster_l_x-25, cy+50), (thruster_l_x-30, cy+120), (thruster_l_x+5, cy+140)], fill=(100, 200, 255))

    # Blue flame exhaust (right)
    flame_r = [
        (thruster_r_x+25, cy+40),
        (thruster_r_x+50, cy+140),
        (thruster_r_x, cy+160)
    ]
    draw.polygon(flame_r, fill=(0, 150, 255))
    draw.polygon([(thruster_r_x+25, cy+50), (thruster_r_x+30, cy+120), (thruster_r_x-5, cy+140)], fill=(100, 200, 255))

    save_icon(img, 'deco-wing-jetpack.png')

def create_deco_wing_magic_bag():
    """Magical satchel with runes"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Bag body (brown leather)
    draw.rectangle([cx-70, cy-100, cx+70, cy+100], fill=(150, 100, 50), outline=(100, 70, 30), width=4*SCALE)

    # Flap
    draw.polygon([(cx-70, cy-100), (cx+70, cy-100), (cx+50, cy-150), (cx-50, cy-150)], fill=(130, 80, 40))

    # Buckle straps
    draw.rectangle([cx-60, cy-80, cx+60, cy-50], fill=(120, 70, 30), outline=(80, 50, 20), width=2*SCALE)
    draw.rectangle([cx-50, cy+50, cx+50, cy+80], fill=(120, 70, 30), outline=(80, 50, 20), width=2*SCALE)

    # Glowing runes (mystical symbols)
    for rune_y in [cy-40, cy+20]:
        for rune_x in [cx-40, cx, cx+40]:
            draw.polygon([
                (rune_x, rune_y-10),
                (rune_x+10, rune_y),
                (rune_x, rune_y+10),
                (rune_x-10, rune_y)
            ], fill=(200, 150, 255), outline=(255, 200, 255), width=2*SCALE)

    # Glow
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.rectangle([cx-70, cy-100, cx+70, cy+100], fill=(200, 150, 255, 80))
    glow = apply_blur(glow, 20)
    img = composite_layer(img, glow, 150)

    save_icon(img, 'deco-wing-magic-bag.png')

print("\n=== WEAPON ITEMS (53-64) ===")
create_deco_weapon_shiny_sword()
create_deco_weapon_magic_wand()
create_deco_weapon_gold_shield()
create_deco_weapon_energy_gun()
create_deco_weapon_ninja_star()
create_deco_weapon_pirate_sword()
create_deco_weapon_magic_book()
create_deco_weapon_gold_key()
create_deco_weapon_reading_staff()
create_deco_weapon_knowledge_orb()
create_deco_weapon_quest_flag()
create_deco_weapon_trophy()

print("\n=== WING ITEMS (65-76) ===")
create_deco_wing_angel()
create_deco_wing_devil()
create_deco_wing_dragon()
create_deco_wing_butterfly()
create_deco_wing_fire()
create_deco_wing_ice()
create_deco_wing_mech()
create_deco_wing_rainbow()
create_deco_wing_cape_red()
create_deco_wing_cape_purple()
create_deco_wing_jetpack()
create_deco_wing_magic_bag()


# ============================================================================
# FRAME ITEMS (77-89)
# ============================================================================

def create_shop_star_frame():
    """Gold ring with stars"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Outer ring
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(218, 165, 32), width=40*SCALE)

    # Inner ring (transparent cutout)
    draw.ellipse([cx-100, cy-100, cx+100, cy+100], fill=(0, 0, 0, 0))

    # Stars around ring
    for i in range(12):
        angle = i * 30
        star_x = cx + 140 * math.cos(math.radians(angle))
        star_y = cy + 140 * math.sin(math.radians(angle))
        star_pts = []
        for j in range(10):
            star_angle = j * math.pi / 5
            r = 15 if j % 2 == 0 else 8
            star_pts.append((star_x + r * math.cos(star_angle), star_y + r * math.sin(star_angle)))
        draw.polygon(star_pts, fill=(255, 215, 0), outline=(200, 150, 0), width=1*SCALE)

    save_icon(img, 'shop-star-frame.png')

def create_deco_frame_gold_crown():
    """Ornate golden circular frame"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main ring
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(218, 165, 32), width=45*SCALE)
    draw.ellipse([cx-170, cy-170, cx+170, cy+170], fill=None, outline=(255, 215, 100), width=15*SCALE)

    # Inner circle (transparent)
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    # Filigree details (small circles)
    for i in range(16):
        angle = i * 22.5
        detail_x = cx + 150 * math.cos(math.radians(angle))
        detail_y = cy + 150 * math.sin(math.radians(angle))
        draw.circle((detail_x, detail_y), 12, fill=(218, 165, 32))

    save_icon(img, 'deco-frame-gold-crown.png')

def create_deco_frame_diamond():
    """Gem-studded frame"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Main ring (white/silver)
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(220, 220, 240), width=45*SCALE)

    # Inner transparent circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    # Gems around
    for i in range(12):
        angle = i * 30
        gem_x = cx + 155 * math.cos(math.radians(angle))
        gem_y = cy + 155 * math.sin(math.radians(angle))
        # Main gem
        draw.ellipse([gem_x-18, gem_y-18, gem_x+18, gem_y+18], fill=(255, 100, 200), outline=(200, 50, 150), width=2*SCALE)
        # Highlight
        draw.ellipse([gem_x-10, gem_y-10, gem_x, gem_y], fill=(255, 200, 255))

    save_icon(img, 'deco-frame-diamond.png')

def create_deco_frame_fire():
    """Flame ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Flame shapes around circle
    for i in range(12):
        angle = i * 30
        flame_base_x = cx + 140 * math.cos(math.radians(angle))
        flame_base_y = cy + 140 * math.sin(math.radians(angle))
        flame_angle = angle + 90
        flame_tip_x = flame_base_x + 60 * math.cos(math.radians(flame_angle))
        flame_tip_y = flame_base_y + 60 * math.sin(math.radians(flame_angle))
        
        flame_pts = [
            (flame_base_x, flame_base_y),
            (flame_base_x - 20 * math.sin(math.radians(angle)), flame_base_y + 20 * math.cos(math.radians(angle))),
            (flame_tip_x, flame_tip_y),
            (flame_base_x + 20 * math.sin(math.radians(angle)), flame_base_y - 20 * math.cos(math.radians(angle)))
        ]
        draw.polygon(flame_pts, fill=(255, 100, 0))

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-fire.png')

def create_deco_frame_ice():
    """Icy crystal ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Crystal formations around ring
    for i in range(8):
        angle = i * 45
        crystal_x = cx + 150 * math.cos(math.radians(angle))
        crystal_y = cy + 150 * math.sin(math.radians(angle))
        
        crystal_pts = [
            (crystal_x, crystal_y),
            (crystal_x - 30 * math.cos(math.radians(angle)), crystal_y - 30 * math.sin(math.radians(angle))),
            (crystal_x - 40 * math.cos(math.radians(angle-45)), crystal_y - 40 * math.sin(math.radians(angle-45))),
            (crystal_x - 30 * math.cos(math.radians(angle+45)), crystal_y - 30 * math.sin(math.radians(angle+45)))
        ]
        draw.polygon(crystal_pts, fill=(150, 200, 255), outline=(100, 150, 200), width=2*SCALE)

    # Ring base
    draw.ellipse([cx-160, cy-160, cx+160, cy+160], fill=None, outline=(100, 150, 200), width=30*SCALE)

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-ice.png')

def create_deco_frame_rainbow():
    """Rainbow gradient ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Rainbow ring segments
    colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
    
    for i, color in enumerate(colors):
        angle_start = i * 51.4
        angle_end = (i + 1) * 51.4
        
        # Outer arc
        for angle in range(int(angle_start), int(angle_end)):
            rad = math.radians(angle)
            x_outer = cx + 190 * math.cos(rad)
            y_outer = cy + 190 * math.sin(rad)
            x_inner = cx + 150 * math.cos(rad)
            y_inner = cy + 150 * math.sin(rad)
            draw.line([(x_outer, y_outer), (x_inner, y_inner)], fill=color, width=2*SCALE)

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-rainbow.png')

def create_deco_frame_starlight():
    """Twinkling star ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Soft glow ring
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(200, 180, 255, 150), width=35*SCALE)

    # Stars scattered
    for i in range(24):
        angle = i * 15
        star_x = cx + 150 * math.cos(math.radians(angle))
        star_y = cy + 150 * math.sin(math.radians(angle))
        star_pts = []
        for j in range(10):
            star_angle = j * math.pi / 5
            r = 10 if j % 2 == 0 else 5
            star_pts.append((star_x + r * math.cos(star_angle), star_y + r * math.sin(star_angle)))
        draw.polygon(star_pts, fill=(255, 255, 200))

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-starlight.png')

def create_deco_frame_dragon():
    """Dragon scale ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Scales around ring
    for i in range(16):
        angle = i * 22.5
        scale_x = cx + 150 * math.cos(math.radians(angle))
        scale_y = cy + 150 * math.sin(math.radians(angle))
        draw.circle((scale_x, scale_y), 15, fill=(80, 150, 80), outline=(50, 100, 50), width=2*SCALE)

    # Ring base
    draw.ellipse([cx-170, cy-170, cx+170, cy+170], fill=None, outline=(50, 100, 50), width=30*SCALE)

    # Red gem accents
    for i in [0, 4, 8, 12]:
        angle = i * 22.5
        gem_x = cx + 150 * math.cos(math.radians(angle))
        gem_y = cy + 150 * math.sin(math.radians(angle))
        draw.circle((gem_x, gem_y), 20, fill=(200, 20, 20), outline=(150, 10, 10), width=2*SCALE)

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-dragon.png')

def create_deco_frame_skull():
    """Skull-decorated ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Dark ring
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(100, 50, 50), width=45*SCALE)

    # Skulls at 4 compass points
    skull_positions = [(cx, cy-160), (cx+160, cy), (cx, cy+160), (cx-160, cy)]
    
    for skull_x, skull_y in skull_positions:
        # Main skull
        draw.ellipse([skull_x-20, skull_y-25, skull_x+20, skull_y+15], fill=(200, 200, 200))
        # Eyes
        draw.circle((skull_x-10, skull_y-10), 5, fill=(0, 0, 0))
        draw.circle((skull_x+10, skull_y-10), 5, fill=(0, 0, 0))
        # Nose
        draw.polygon([(skull_x-3, skull_y), (skull_x+3, skull_y), (skull_x, skull_y+5)], fill=(0, 0, 0))

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-skull.png')

def create_deco_frame_flower():
    """Flower wreath ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Flowers around ring
    for i in range(12):
        angle = i * 30
        flower_x = cx + 150 * math.cos(math.radians(angle))
        flower_y = cy + 150 * math.sin(math.radians(angle))
        
        # Petals
        petal_colors = [(255, 180, 200), (255, 200, 150), (255, 255, 150), (200, 255, 150)]
        for j, color in enumerate(petal_colors):
            petal_angle = j * 90
            petal_x = flower_x + 20 * math.cos(math.radians(petal_angle))
            petal_y = flower_y + 20 * math.sin(math.radians(petal_angle))
            draw.ellipse([petal_x-12, petal_y-12, petal_x+12, petal_y+12], fill=color)
        
        # Center
        draw.circle((flower_x, flower_y), 8, fill=(255, 200, 0))

    # Green leaves
    for i in range(24):
        if i % 2 == 1:
            angle = i * 15
            leaf_x = cx + 120 * math.cos(math.radians(angle))
            leaf_y = cy + 120 * math.sin(math.radians(angle))
            draw.ellipse([leaf_x-8, leaf_y-12, leaf_x+8, leaf_y+12], fill=(100, 180, 100))

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-flower.png')

def create_deco_frame_lightning():
    """Electric lightning ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Lightning bolts around ring
    for i in range(8):
        angle = i * 45
        bolt_x = cx + 150 * math.cos(math.radians(angle))
        bolt_y = cy + 150 * math.sin(math.radians(angle))
        
        bolt_angle = angle + 90
        bolt_pts = [
            (bolt_x, bolt_y),
            (bolt_x + 25 * math.cos(math.radians(bolt_angle)), bolt_y + 25 * math.sin(math.radians(bolt_angle))),
            (bolt_x - 10 * math.sin(math.radians(bolt_angle)), bolt_y + 10 * math.cos(math.radians(bolt_angle))),
            (bolt_x + 50 * math.cos(math.radians(bolt_angle)), bolt_y + 50 * math.sin(math.radians(bolt_angle)))
        ]
        draw.polygon(bolt_pts, fill=(255, 255, 0), outline=(200, 200, 0), width=2*SCALE)

    # Ring base
    draw.ellipse([cx-170, cy-170, cx+170, cy+170], fill=None, outline=(255, 255, 0), width=30*SCALE)

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-lightning.png')

def create_deco_frame_neon():
    """Neon glow ring"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Glow effect
    glow = create_image()
    glow_draw = ImageDraw.Draw(glow, 'RGBA')
    glow_draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=(255, 50, 200, 100))
    glow = apply_blur(glow, 30)
    img = composite_layer(img, glow, 200)

    # Outer neon (hot pink)
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(255, 50, 200), width=30*SCALE)

    # Inner neon (cyan)
    draw.ellipse([cx-140, cy-140, cx+140, cy+140], fill=None, outline=(0, 255, 255), width=20*SCALE)

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-neon.png')

def create_deco_frame_space():
    """Space ring with stars"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Ring base (dark blue/purple)
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], fill=None, outline=(50, 100, 200), width=45*SCALE)

    # Tiny stars scattered
    for i in range(30):
        angle = (i * 12) + (i % 3) * 20
        star_x = cx + (120 + (i % 3) * 30) * math.cos(math.radians(angle))
        star_y = cy + (120 + (i % 3) * 30) * math.sin(math.radians(angle))
        draw.circle((star_x, star_y), 2 + (i % 3), fill=(255, 255, 200))

    # Planet dots
    for i in [0, 6, 12, 18]:
        angle = i * 20
        planet_x = cx + 160 * math.cos(math.radians(angle))
        planet_y = cy + 160 * math.sin(math.radians(angle))
        draw.circle((planet_x, planet_y), 12, fill=(100, 150, 255), outline=(50, 100, 200), width=2*SCALE)

    # Inner circle
    draw.ellipse([cx-95, cy-95, cx+95, cy+95], fill=(0, 0, 0, 0))

    save_icon(img, 'deco-frame-space.png')

# ============================================================================
# AURA ITEMS (90-104)
# ============================================================================

def create_shop_fire_aura():
    """Orange/red fire aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Gradient from center
    for i in range(10):
        radius = 500 - i * 40
        opacity = int(150 * (1 - i / 10))
        color = (255 - i*15, 100 + i*10, 0, opacity)
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=color)

    # Flame wisps
    for j in range(8):
        angle = j * 45
        for i in range(5):
            x = cx + (i+1) * 80 * math.cos(math.radians(angle))
            y = cy + (i+1) * 80 * math.sin(math.radians(angle))
            draw.ellipse([x-20-i*3, y-20-i*3, x+20+i*3, y+20+i*3], 
                        fill=(255 - i*30, 100 + i*20, 0, 80 - i*10))

    save_icon(img, 'shop-fire-aura.png')

def create_shop_rainbow():
    """Rainbow aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Conic rainbow gradient
    colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

    for angle in range(360):
        color_idx = (angle // 51) % 7
        color = colors[color_idx]
        rad = math.radians(angle)
        for r in range(100, 500, 20):
            x = cx + r * math.cos(rad)
            y = cy + r * math.sin(rad)
            draw.circle((x, y), 20, fill=(*color, 100 - r//20 * 15))

    save_icon(img, 'shop-rainbow.png')

def create_shop_lightning():
    """Yellow electric aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Bright yellow center glow
    for i in range(8):
        radius = 400 - i * 40
        opacity = int(180 * (1 - i / 8))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], 
                    fill=(255, 255, 0, opacity))

    # Lightning rays
    for angle in range(0, 360, 45):
        pts = [(cx, cy)]
        for j in range(8):
            offset_angle = angle + (j % 2) * 15 - 7.5
            rad = math.radians(offset_angle)
            x = cx + (j+1) * 60 * math.cos(rad)
            y = cy + (j+1) * 60 * math.sin(rad)
            pts.append((x, y))
        draw.line(pts, fill=(255, 255, 0), width=8*SCALE)

    save_icon(img, 'shop-lightning.png')

def create_deco_aura_fire():
    """Intense red fire aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Intense gradient
    for i in range(12):
        radius = 500 - i * 30
        opacity = int(200 * (1 - i / 12))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(255 - i*10, 50 + i*5, 0, opacity))

    # More visible flame shapes
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        for i in range(3):
            fx = cx + (i+1) * 120 * math.cos(rad)
            fy = cy + (i+1) * 120 * math.sin(rad)
            draw.polygon([
                (fx, fy),
                (fx-30, fy-40),
                (fx-60, fy-30),
                (fx-40, fy)
            ], fill=(255-i*40, 100, 0, 120-i*30))

    save_icon(img, 'deco-aura-fire.png')

def create_deco_aura_ice():
    """Cool blue ice aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Blue gradient
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(160 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(100 + i*10, 150 + i*5, 255, opacity))

    # Ice particles
    for i in range(40):
        angle = (i * 9) % 360
        distance = 150 + (i % 5) * 60
        px = cx + distance * math.cos(math.radians(angle))
        py = cy + distance * math.sin(math.radians(angle))
        size = 2 + (i % 3)
        draw.circle((px, py), size, fill=(200, 230, 255, 150 - i*2))

    save_icon(img, 'deco-aura-ice.png')

def create_deco_aura_electric():
    """Bright yellow electric aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Intense yellow gradient
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(180 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(255, 255 - i*20, 0, opacity))

    # Lightning bolts
    for angle in range(0, 360, 60):
        bolt_pts = [(cx, cy)]
        for j in range(6):
            jitter = 20 * math.sin(j)
            next_angle = angle + jitter
            rad = math.radians(next_angle)
            x = cx + (j+1) * 75 * math.cos(rad)
            y = cy + (j+1) * 75 * math.sin(rad)
            bolt_pts.append((x, y))
        draw.line(bolt_pts, fill=(255, 255, 100), width=6*SCALE)

    save_icon(img, 'deco-aura-electric.png')

def create_deco_aura_poison():
    """Purple/green toxic mist"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Swirling gradient
    for i in range(12):
        radius = 480 - i * 30
        opacity = int(140 * (1 - i / 12))
        # Alternate purple and green
        if i % 2 == 0:
            color = (150 - i*5, 100 + i*5, 150 - i*10, opacity)
        else:
            color = (100 + i*5, 150 - i*10, 100 + i*5, opacity)
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=color)

    # Swirl effect
    for i in range(20):
        angle = i * 18 + i * 2
        distance = 150 + (i % 4) * 60
        px = cx + distance * math.cos(math.radians(angle))
        py = cy + distance * math.sin(math.radians(angle))
        draw.circle((px, py), 10 + (i % 3)*5, fill=(150, 150, 100, 100 - i*3))

    save_icon(img, 'deco-aura-poison.png')

def create_deco_aura_light():
    """Bright golden holy light"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Bright gradient
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(200 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(255, 240 - i*10, 150, opacity))

    # Rays
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        ray_pts = [
            (cx + 200 * math.cos(rad), cy + 200 * math.sin(rad)),
            (cx + 350 * math.cos(rad), cy + 350 * math.sin(rad))
        ]
        draw.line(ray_pts, fill=(255, 255, 100), width=10*SCALE)

    save_icon(img, 'deco-aura-light.png')

def create_deco_aura_dark():
    """Deep purple/black dark aura"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Dark gradient (inverted from edges)
    for i in range(12):
        radius = 480 - i * 30
        opacity = int(120 * i / 12)
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(50 - i*2, 30 - i, 80 - i*3, opacity))

    # Shadow wisps
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        for i in range(4):
            sx = cx + (i+1) * 80 * math.cos(rad)
            sy = cy + (i+1) * 80 * math.sin(rad)
            draw.ellipse([sx-30, sy-30, sx+30, sy+30],
                        fill=(40, 20, 60, 80 - i*15))

    save_icon(img, 'deco-aura-dark.png')

def create_deco_aura_rainbow():
    """Rainbow radial gradient"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

    for i in range(10):
        radius = 450 - i * 35
        color_idx = (i * 2) % 7
        color = colors[color_idx]
        opacity = int(180 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(*color, opacity))

    # Sparkles
    for i in range(20):
        angle = i * 18
        distance = 200 + (i % 3) * 80
        px = cx + distance * math.cos(math.radians(angle))
        py = cy + distance * math.sin(math.radians(angle))
        draw.polygon([
            (px, py-8),
            (px+8, py),
            (px, py+8),
            (px-8, py)
        ], fill=(255, 255, 200, 150))

    save_icon(img, 'deco-aura-rainbow.png')

def create_deco_aura_star():
    """Golden star-burst"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Golden gradient
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(200 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(255, 215 - i*10, 0, opacity))

    # Radiating star points
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        star_pts = []
        for j in range(6):
            r = 150 + j * 60
            star_pts.append((cx + r * math.cos(rad), cy + r * math.sin(rad)))
        draw.line(star_pts, fill=(255, 255, 0), width=8*SCALE)

    save_icon(img, 'deco-aura-star.png')

def create_deco_aura_heart_bg():
    """Pink heart glow with mini hearts"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Pink gradient
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(180 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(255, 150 - i*10, 200 - i*5, opacity))

    # Floating mini hearts
    for i in range(12):
        angle = i * 30
        distance = 180 + (i % 3) * 80
        hx = cx + distance * math.cos(math.radians(angle))
        hy = cy + distance * math.sin(math.radians(angle))
        
        # Tiny heart
        h_size = 15
        draw.ellipse([hx-h_size//2, hy-h_size//2-10, hx-h_size//4, hy-h_size//2], fill=(255, 100, 150))
        draw.ellipse([hx+h_size//4, hy-h_size//2-10, hx+h_size//2, hy-h_size//2], fill=(255, 100, 150))
        draw.polygon([(hx-h_size//2, hy-h_size//2), (hx+h_size//2, hy-h_size//2), (hx, hy+h_size//3)],
                    fill=(255, 100, 150))

    save_icon(img, 'deco-aura-heart-bg.png')

def create_deco_aura_explosion():
    """Orange/yellow explosion burst"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Explosion rings
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(180 * (1 - i / 10))
        color = (255 - i*15, 150 - i*10, 0, opacity)
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=color)

    # Explosion spikes
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        spike_pts = [
            (cx + 150 * math.cos(rad), cy + 150 * math.sin(rad)),
            (cx + 320 * math.cos(rad), cy + 320 * math.sin(rad))
        ]
        draw.line(spike_pts, fill=(255, 150, 0), width=8*SCALE)

    save_icon(img, 'deco-aura-explosion.png')

def create_deco_aura_galaxy():
    """Deep purple spiral galaxy"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Dark purple gradient
    for i in range(12):
        radius = 480 - i * 30
        opacity = int(150 * (1 - i / 12))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(80 + i*3, 50 + i*2, 150 + i*3, opacity))

    # Spiral pattern
    for i in range(60):
        angle = i * 6 + i * 0.5
        distance = 100 + i * 4
        px = cx + distance * math.cos(math.radians(angle))
        py = cy + distance * math.sin(math.radians(angle))
        size = 2 + (i % 4)
        draw.circle((px, py), size, fill=(200, 180, 255, 150 - i*2))

    save_icon(img, 'deco-aura-galaxy.png')

def create_deco_aura_cherry_blossom():
    """Pink cherry blossom petals"""
    img = create_image()
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = RENDER_SIZE // 2, RENDER_SIZE // 2

    # Soft pink gradient
    for i in range(10):
        radius = 450 - i * 35
        opacity = int(160 * (1 - i / 10))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    fill=(255, 180 - i*10, 200 - i*5, opacity))

    # Scattered petals
    for i in range(30):
        angle = (i * 12) % 360
        distance = 150 + (i % 5) * 60
        px = cx + distance * math.cos(math.radians(angle))
        py = cy + distance * math.sin(math.radians(angle))
        
        # Petal (circle)
        draw.circle((px, py), 12 + (i % 3)*3, fill=(255, 150, 200, 150 - i*2))

    save_icon(img, 'deco-aura-cherry-blossom.png')

print("\n=== FRAME ITEMS (77-89) ===")
create_shop_star_frame()
create_deco_frame_gold_crown()
create_deco_frame_diamond()
create_deco_frame_fire()
create_deco_frame_ice()
create_deco_frame_rainbow()
create_deco_frame_starlight()
create_deco_frame_dragon()
create_deco_frame_skull()
create_deco_frame_flower()
create_deco_frame_lightning()
create_deco_frame_neon()
create_deco_frame_space()

print("\n=== AURA ITEMS (90-104) ===")
create_shop_fire_aura()
create_shop_rainbow()
create_shop_lightning()
create_deco_aura_fire()
create_deco_aura_ice()
create_deco_aura_electric()
create_deco_aura_poison()
create_deco_aura_light()
create_deco_aura_dark()
create_deco_aura_rainbow()
create_deco_aura_star()
create_deco_aura_heart_bg()
create_deco_aura_explosion()
create_deco_aura_galaxy()
create_deco_aura_cherry_blossom()

print("\n" + "="*60)
print("ICON GENERATION COMPLETE!")
print("="*60)
print(f"Output directory: {OUTPUT_DIR}")

# Count generated files
import os
file_count = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
print(f"Total PNG files generated: {file_count}")

