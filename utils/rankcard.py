"""Generación de la tarjeta de rango con Pillow (requiere Pillow >= 10.1)."""
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 934, 282
FONT_PATH = Path("assets/fonts/font.ttf")  # opcional: pon aquí tu fuente


def _font(size):
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    for name in ("DejaVuSans-Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def _fmt(n):
    return f"{n / 1000:.1f}K" if n >= 1000 else str(n)


def _gradient(size, c1, c2):
    top = Image.new("RGB", size, c2)
    base = Image.new("RGB", size, c1)
    mask = Image.linear_gradient("L").resize(size)
    return Image.composite(top, base, mask)


# ---------- guardado de imágenes subidas por mods ----------
def save_background(data: bytes, dest: Path):
    img = Image.open(BytesIO(data)).convert("RGB")
    img = ImageOps.fit(img, (W, H), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "PNG")


def save_icon(data: bytes, dest: Path):
    img = Image.open(BytesIO(data)).convert("RGBA")
    img = ImageOps.contain(img, (128, 128), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "PNG")


# ---------- tarjeta ----------
def render_card(*, avatar_bytes, bg_path, name, level, xp, needed, rank,
                medal_paths=(), accent=0x5865F2) -> BytesIO:
    if bg_path and Path(bg_path).exists():
        bg = ImageOps.fit(Image.open(bg_path).convert("RGB"), (W, H), Image.LANCZOS)
    else:
        bg = _gradient((W, H), (38, 40, 58), (16, 16, 24))

    card = bg.convert("RGBA")
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle(
        (20, 20, W - 20, H - 20), radius=28, fill=(0, 0, 0, 150)
    )
    card = Image.alpha_composite(card, panel)
    d = ImageDraw.Draw(card)

    color = ((accent >> 16) & 255, (accent >> 8) & 255, accent & 255)

    # avatar circular con aro
    d.ellipse((44, 50, 226, 232), fill=color)
    av = Image.open(BytesIO(avatar_bytes)).convert("RGBA").resize((170, 170), Image.LANCZOS)
    mask = Image.new("L", (170, 170), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 169, 169), fill=255)
    card.paste(av, (50, 56), mask)

    # nombre (recortado si es muy largo)
    f_name = _font(42)
    max_w = W - 50 - 260
    while d.textlength(name, font=f_name) > max_w and len(name) > 1:
        name = name[:-2] + "…"
    d.text((260, 46), name, font=f_name, fill=(255, 255, 255))

    # nivel / rank
    d.text((260, 100), f"NIVEL {level}   •   RANK #{rank}", font=_font(28), fill=color)

    # texto de xp
    d.text((W - 50, 140), f"{_fmt(xp)} / {_fmt(needed)} XP",
           font=_font(24), fill=(210, 210, 215), anchor="ra")

    # barra de progreso
    x0, y0, x1, y1 = 260, 176, W - 50, 204
    track = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(track).rounded_rectangle((x0, y0, x1, y1), radius=14, fill=(255, 255, 255, 45))
    card = Image.alpha_composite(card, track)
    d = ImageDraw.Draw(card)
    ratio = max(0.0, min(1.0, xp / needed if needed else 0))
    if ratio > 0:
        fill_x = max(x0 + 28, x0 + int((x1 - x0) * ratio))
        d.rounded_rectangle((x0, y0, fill_x, y1), radius=14, fill=color)

    # medallas (hasta 6 iconos)
    x = 260
    for p in list(medal_paths)[:6]:
        try:
            icon = Image.open(p).convert("RGBA")
            icon = ImageOps.contain(icon, (38, 38), Image.LANCZOS)
            card.paste(icon, (x, 216), icon)
            x += 46
        except Exception:
            continue

    out = BytesIO()
    card.convert("RGB").save(out, "PNG")
    out.seek(0)
    return out
