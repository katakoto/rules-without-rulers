"""
Spinning record + moving tonearm MP4 generator

- Record: 1 revolution / 1.5s (matches CSS `spin 1.5s`)
- Tonearm: swings from outer groove (-2 deg CSS) to inner groove (+20 deg CSS)
           linearly over the full track duration (3:42)
- Duration: 222 seconds, 30 fps
- Output: output.mp4 with audio merged
"""
import math
import subprocess
import os

import cairo
import numpy as np
import imageio_ffmpeg
from PIL import Image

# ── Config ────────────────────────────────────────────────────────────
FPS            = 30
DURATION       = 222          # 3:42 in seconds
CANVAS         = 900          # square canvas pixels
RECORD_FRAC    = 0.82         # record is 82% of canvas
REV_SPEED      = 1.5          # seconds per revolution (CSS: spin 1.5s)
DEG_PER_FRAME  = 360 / REV_SPEED / FPS   # 8 deg/frame

# Tonearm angles in PIL convention (CCW positive)
# CSS rotate(+20deg) = outer groove start → PIL -20
# CSS rotate(-2deg)  = inner groove end  → PIL +2
TONEARM_START  = -20.0  # PIL degrees at frame 0   (= CSS +20deg, outer groove)
TONEARM_END    =   2.0  # PIL degrees at last frame (= CSS  -2deg, inner groove)

RECORD_PATH    = "src/assets/record_circle.webp"
AUDIO_PATH     = "public/audio/rules-without-rulers.mp3"
SILENT_OUT     = "output_silent.mp4"
FINAL_OUT      = "output.mp4"

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()


# ── Tonearm renderer (pycairo) ────────────────────────────────────────
def render_tonearm(px_size: int) -> Image.Image:
    """Render the tonearm SVG (viewBox 0 0 200 200) at px_size x px_size."""
    s = px_size / 200.0   # SVG → pixel scale factor

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, px_size, px_size)
    ctx = cairo.Context(surface)
    ctx.scale(s, s)

    # transparent background
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)

    # armGrad: #d8d2c0 → #9a9080 → #5a5448  (along arm direction)
    arm_grad = cairo.LinearGradient(180, 24, 58, 118)
    arm_grad.add_color_stop_rgb(0.0, 0xd8/255, 0xd2/255, 0xc0/255)
    arm_grad.add_color_stop_rgb(0.5, 0x9a/255, 0x90/255, 0x80/255)
    arm_grad.add_color_stop_rgb(1.0, 0x5a/255, 0x54/255, 0x48/255)

    # main arm line  (180,24) → (58,118)
    ctx.set_source(arm_grad)
    ctx.set_line_width(3.5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(180, 24); ctx.line_to(58, 118)
    ctx.stroke()

    # counter-balance arm  (180,24) → (194,14)
    cb_grad = cairo.LinearGradient(180, 24, 194, 14)
    cb_grad.add_color_stop_rgb(0.0, 0xd8/255, 0xd2/255, 0xc0/255)
    cb_grad.add_color_stop_rgb(1.0, 0x5a/255, 0x54/255, 0x48/255)
    ctx.set_source(cb_grad)
    ctx.set_line_width(3.0)
    ctx.move_to(180, 24); ctx.line_to(194, 14)
    ctx.stroke()

    # counter-balance tip circle  cx=195 cy=13 r=6
    ctx.set_source_rgb(0x2a/255, 0x25/255, 0x20/255)
    ctx.arc(195, 13, 6, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(0x0a/255, 0x0a/255, 0x08/255)
    ctx.set_line_width(0.5)
    ctx.arc(195, 13, 6, 0, 2*math.pi); ctx.stroke()

    # pivot circle  cx=180 cy=24 r=9  (radial gradient)
    pivot_rg = cairo.RadialGradient(176, 20, 0, 180, 24, 9)
    pivot_rg.add_color_stop_rgb(0.0, 0x3a/255, 0x35/255, 0x30/255)
    pivot_rg.add_color_stop_rgb(0.6, 0x1a/255, 0x18/255, 0x15/255)
    pivot_rg.add_color_stop_rgb(1.0, 0x0a/255, 0x0a/255, 0x08/255)
    ctx.set_source(pivot_rg)
    ctx.arc(180, 24, 9, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(0x0a/255, 0x0a/255, 0x08/255)
    ctx.set_line_width(0.6)
    ctx.arc(180, 24, 9, 0, 2*math.pi); ctx.stroke()

    # pivot center dot  r=3
    ctx.set_source_rgb(0x0a/255, 0x0a/255, 0x08/255)
    ctx.arc(180, 24, 3, 0, 2*math.pi); ctx.fill()

    # cartridge group at (58, 118) rotated 38 deg
    ctx.save()
    ctx.translate(58, 118)
    ctx.rotate(38 * math.pi / 180)

    # cartridge body  x=-12 y=-2 w=22 h=9 rx=1
    cart_grad = cairo.LinearGradient(0, -2, 0, 7)
    cart_grad.add_color_stop_rgb(0, 0x1a/255, 0x18/255, 0x15/255)
    cart_grad.add_color_stop_rgb(1, 0x08/255, 0x08/255, 0x0a/255)
    ctx.set_source(cart_grad)
    rx = 1.0
    x, y, w, h = -12, -2, 22, 9
    ctx.new_path()
    ctx.move_to(x+rx, y)
    ctx.line_to(x+w-rx, y);  ctx.arc(x+w-rx, y+rx, rx, -math.pi/2, 0)
    ctx.line_to(x+w, y+h-rx); ctx.arc(x+w-rx, y+h-rx, rx, 0, math.pi/2)
    ctx.line_to(x+rx, y+h);  ctx.arc(x+rx, y+h-rx, rx, math.pi/2, math.pi)
    ctx.line_to(x, y+rx);    ctx.arc(x+rx, y+rx, rx, math.pi, 3*math.pi/2)
    ctx.close_path(); ctx.fill()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.4)
    ctx.new_path()
    ctx.move_to(x+rx, y)
    ctx.line_to(x+w-rx, y);  ctx.arc(x+w-rx, y+rx, rx, -math.pi/2, 0)
    ctx.line_to(x+w, y+h-rx); ctx.arc(x+w-rx, y+h-rx, rx, 0, math.pi/2)
    ctx.line_to(x+rx, y+h);  ctx.arc(x+rx, y+h-rx, rx, math.pi/2, math.pi)
    ctx.line_to(x, y+rx);    ctx.arc(x+rx, y+rx, rx, math.pi, 3*math.pi/2)
    ctx.close_path(); ctx.stroke()

    # cartridge stripe
    ctx.set_source_rgba(0x3a/255, 0x35/255, 0x30/255, 0.6)
    ctx.rectangle(-10, 0, 18, 2); ctx.fill()

    # stylus cantilever  (-9,7) → (-11,11)
    ctx.set_source_rgb(0xaa/255, 0x8a/255, 0x55/255)
    ctx.set_line_width(0.8)
    ctx.move_to(-9, 7); ctx.line_to(-11, 11); ctx.stroke()

    # stylus tip  r=0.8
    ctx.set_source_rgb(0xf4/255, 0xf1/255, 0xea/255)
    ctx.arc(-11, 11, 0.8, 0, 2*math.pi); ctx.fill()

    ctx.restore()

    # Cairo BGRA → PIL RGBA
    buf = bytes(surface.get_data())
    arr = np.frombuffer(buf, dtype=np.uint8).reshape((px_size, px_size, 4))
    rgba = arr[:, :, [2, 1, 0, 3]]   # swap B↔R
    return Image.fromarray(rgba, 'RGBA')


# ── Pre-compute assets ────────────────────────────────────────────────
print("Loading record image...")
rec_size = int(CANVAS * RECORD_FRAC)
rec_img = Image.open(RECORD_PATH).convert("RGBA")
rec_img = rec_img.resize((rec_size, rec_size), Image.LANCZOS)
rec_offset = ((CANVAS - rec_size) // 2, (CANVAS - rec_size) // 2)

print("Rendering tonearm...")
ta_size  = int(CANVAS * 0.56)     # 56% of stage
ta_img   = render_tonearm(ta_size)

# Tonearm pivot point within the tonearm image (matches CSS transform-origin: 90% 12%)
pivot_x  = ta_size * 0.90
pivot_y  = ta_size * 0.12

# Tonearm top-left in canvas (CSS: right:2%, top:-4%)
ta_left  = int(CANVAS * (0.98 - 0.56))   # = CANVAS*0.42
ta_top   = int(-CANVAS * 0.04)            # = -36  (overhangs top)

black_bg = Image.new("RGB", (CANVAS, CANVAS), (0, 0, 0))
total_frames = int(DURATION * FPS)

print(f"Generating {total_frames} frames ({FPS} fps, {DURATION}s)...")

# ── Stream raw RGB frames into ffmpeg ─────────────────────────────────
proc = subprocess.Popen(
    [
        ffmpeg_exe, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{CANVAS}x{CANVAS}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "pipe:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "18",
        SILENT_OUT,
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

for i in range(total_frames):
    progress = i / max(total_frames - 1, 1)

    # Spinning record
    rec_angle  = -(i * DEG_PER_FRAME) % 360   # PIL CCW → negate for CW spin
    rec_rot    = rec_img.rotate(rec_angle, resample=Image.BICUBIC, expand=False)

    # Moving tonearm
    ta_angle   = TONEARM_START + (TONEARM_END - TONEARM_START) * progress
    ta_rot     = ta_img.rotate(ta_angle, resample=Image.BICUBIC,
                               center=(pivot_x, pivot_y), expand=False)

    canvas = black_bg.copy()
    canvas.paste(rec_rot, rec_offset, rec_rot)
    canvas.paste(ta_rot,  (ta_left, ta_top), ta_rot)

    proc.stdin.write(np.array(canvas, dtype=np.uint8).tobytes())

    if i % 300 == 0:
        print(f"  {i/total_frames*100:.0f}%  ({i}/{total_frames})", end="\r", flush=True)

proc.stdin.close()
proc.wait()
print("\nVideo encoded. Merging audio...")

subprocess.run(
    [
        ffmpeg_exe, "-y",
        "-i", SILENT_OUT,
        "-i", AUDIO_PATH,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        FINAL_OUT,
    ],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

os.remove(SILENT_OUT)
size_mb = os.path.getsize(FINAL_OUT) / 1024 / 1024
print(f"Done! {FINAL_OUT}  ({size_mb:.0f} MB)")
