"""
Builder dos ads tipograficos "7 [NICHO]" + variantes ("DOBRAR").

ATENCAO: a lista ADS aqui em baixo e um EXEMPLO, com a copy de outra
pessoa. Antes de gerar para um cliente, troca as linhas pela copy dele
(ver a skill criativos-anuncios). A cor de acento ja vem do perfil.
Fonte: Big Shoulders 60pt Black + shear sintético (~5.7°) para italic ligeiro.
Output: OUT_DIR (ver constantes no topo)
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# --- Assets do kit (resolvidos em runtime, funcionam em qualquer maquina) ---
# Ordem: variavel de ambiente PS_ASSETS > pasta assets/ do kit > cwd
import os as _os
from pathlib import Path as _P
def _assets_dir():
    env = _os.environ.get("KIT_ASSETS") or _os.environ.get("PS_ASSETS")
    if env and _P(env).is_dir():
        return _P(env)
    aqui = _P(__file__).resolve()
    for base in list(aqui.parents)[:6]:
        cand = base / "assets"
        if (cand / "fontes").is_dir():
            return cand
    # instalado em ~/.claude/skills/: o instalador deixa uma copia aqui
    cand = _P.home() / ".claude/kit-assets"
    if (cand / "fontes").is_dir():
        return cand
    raise SystemExit(
        "Assets nao encontrados. Corre a partir da pasta do kit "
        "ou define KIT_ASSETS=/caminho/para/assets"
    )
ASSETS = _assets_dir()
FONTES = ASSETS / "fontes"
LOGOS  = ASSETS / "logos"
# Output: por defeito ./out ao lado de onde corres; muda com PS_OUT
OUT_BASE = _P(_os.environ.get("KIT_OUT") or _os.environ.get("PS_OUT") or (_P.cwd() / "out"))

W, H = 1080, 1920
PAD_X = 70
PAD_TOP = 110
BLACK = (0, 0, 0)


def _cor_de_acento():
    """A cor vem da marca de quem instalou, nao de quem escreveu o script.

    Le ~/.claude/kit/perfil.json (marca.cor_acento). Sem perfil, fica o laranja
    do PowerScale Skills Kit, que e o defeito ate ela definir o dela.
    """
    import json as _json
    try:
        _p = _P.home() / ".claude" / "kit" / "perfil.json"
        _hex = (_json.loads(_p.read_text(encoding="utf-8-sig"))
                .get("marca", {}).get("cor_acento", "") or "").strip().lstrip("#")
        if len(_hex) == 3:
            _hex = "".join(c * 2 for c in _hex)
        if len(_hex) == 6:
            return tuple(int(_hex[i:i + 2], 16) for i in (0, 2, 4))
    except Exception:
        pass
    return (232, 74, 28)


# Cor de acento da marca. Vem do perfil; muda la e muda em todos os ads do lote.
ACCENT = _cor_de_acento()
RED = ACCENT  # nome antigo, mantido para nao partir as funcoes abaixo
WHITE = (255, 255, 255)

FONT_PATH = str(FONTES / "BigShoulders_60pt-Black.ttf")
SHEAR = 0.10  # ~5.7° italic sintético
LOGO_PATH = str(LOGOS / "logo-icone.png")
OUT_DIR = OUT_BASE / "typography"

# ----------------------------- LINHAS ------------------------------------
def lines_coach_v1(nicho):
    return [
        [("ESTOU À", "k", False)],
        [("PROCURA DE", "k", False)],
        [(f"7 {nicho}", "r", False)],
        [("COACHES", "r", False)],
        [("A FATURAR", "k", False)],
        [("ENTRE ", "k", False), ("5 A 15K", "r", False)],
        [("QUE QUEREM", "k", False)],
        [("INSTALAR", "k", False)],
        [("A NOSSA", "k", False)],
        [('"MÁQUINA DE', "r", False)],
        [('AQUISIÇÃO"', "r", False)],
        [("SEM ", "k", False), ("QUALQUER", "r", True)],
        [("RISCO", "r", True)],
    ]

def lines_skool_v1(nicho_l1, nicho_l2, valor):
    return [
        [("ESTOU À", "k", False)],
        [("PROCURA DE", "k", False)],
        [(nicho_l1, "r", False)],
        [(nicho_l2, "r", False)],
        [("A FATURAR", "k", False)],
        [("ENTRE ", "k", False), (valor, "r", False)],
        [("QUE QUEREM", "k", False)],
        [("INSTALAR", "k", False)],
        [("A NOSSA", "k", False)],
        [('"MÁQUINA DE', "r", False)],
        [('AQUISIÇÃO"', "r", False)],
        [("SEM ", "k", False), ("QUALQUER", "r", True)],
        [("RISCO", "r", True)],
    ]

def lines_coach_v2(nicho):
    return [
        [("ESTOU À", "k", False)],
        [("PROCURA DE", "k", False)],
        [(f"7 {nicho}", "r", False)],
        [("COACHES", "r", False)],
        [("A FATURAR", "k", False)],
        [("ENTRE ", "k", False), ("5 A 15K", "r", False)],
        [("QUE QUEREM ", "k", False), ("DOBRAR", "r", False)],
        [("A SUA FATURAÇÃO", "r", False)],
        [("INSTALANDO", "k", False)],
        [("A NOSSA", "k", False)],
        [('"MÁQUINA DE', "r", False)],
        [('AQUISIÇÃO"', "r", False)],
        [("SEM ", "k", False), ("QUALQUER", "r", True)],
        [("RISCO", "r", True)],
    ]

def lines_skool_v2(nicho_l1, nicho_l2, valor):
    return [
        [("ESTOU À", "k", False)],
        [("PROCURA DE", "k", False)],
        [(nicho_l1, "r", False)],
        [(nicho_l2, "r", False)],
        [("A FATURAR", "k", False)],
        [("ENTRE ", "k", False), (valor, "r", False)],
        [("QUE QUEREM ", "k", False), ("DOBRAR", "r", False)],
        [("A SUA FATURAÇÃO", "r", False)],
        [("INSTALANDO", "k", False)],
        [("A NOSSA", "k", False)],
        [('"MÁQUINA DE', "r", False)],
        [('AQUISIÇÃO"', "r", False)],
        [("SEM ", "k", False), ("QUALQUER", "r", True)],
        [("RISCO", "r", True)],
    ]

ADS = [
    # ---- v1 coaches ----
    (lines_coach_v1("BUSINESS"), "ad-7coaches-01-business.png"),
    (lines_coach_v1("HEALTH"),   "ad-7coaches-02-health.png"),
    (lines_coach_v1("DATING"),   "ad-7coaches-03-dating.png"),
    (lines_coach_v1("MONEY"),    "ad-7coaches-04-money.png"),
    # ---- v1 skool ----
    (lines_skool_v1("7 COMUNIDADES", "SKOOL", "5 A 15K MRR"),  "ad-skool-01-mrr-pt.png"),
    (lines_skool_v1("7 SKOOL", "OWNERS", "5 A 15K MRR"),       "ad-skool-02-mrr-en.png"),
    (lines_skool_v1("7 COMUNIDADES", "SKOOL", "5 A 15K/MÊS"),  "ad-skool-03-mes-pt.png"),
    # ---- v2 coaches (DOBRAR) ----
    (lines_coach_v2("BUSINESS"), "ad-7coaches-01-business-v2-dobrar.png"),
    (lines_coach_v2("HEALTH"),   "ad-7coaches-02-health-v2-dobrar.png"),
    (lines_coach_v2("DATING"),   "ad-7coaches-03-dating-v2-dobrar.png"),
    (lines_coach_v2("MONEY"),    "ad-7coaches-04-money-v2-dobrar.png"),
    # ---- v2 skool (DOBRAR) ----
    (lines_skool_v2("7 COMUNIDADES", "SKOOL", "5 A 15K MRR"),  "ad-skool-01-mrr-pt-v2-dobrar.png"),
    (lines_skool_v2("7 SKOOL", "OWNERS", "5 A 15K MRR"),       "ad-skool-02-mrr-en-v2-dobrar.png"),
    (lines_skool_v2("7 COMUNIDADES", "SKOOL", "5 A 15K/MÊS"),  "ad-skool-03-mes-pt-v2-dobrar.png"),
]

# ----------------------------- RENDER ------------------------------------
def line_text(line):
    return "".join(seg[0] for seg in line)

def fit_size_for_text(text, max_w, lo=40, hi=260):
    """Largest font size where text width <= max_w (accounting for shear)."""
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(FONT_PATH, mid)
        bbox = f.getbbox(text)
        # shear adds horizontal width: extra = shear * font_height
        extra = int(SHEAR * mid * 1.1)
        w = bbox[2] - bbox[0] + extra
        if w <= max_w:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best

def render_line_to_layer(line, font, asc, desc):
    """
    Render a line (with mixed-color segments + optional underline) to a
    transparent RGBA layer, then shear it for italic. Returns (image, baseline_y_in_image).
    """
    # First, compute total width (no shear)
    tmp_w = 0
    seg_widths = []
    measurer = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    for (text, _, _) in line:
        sw = int(measurer.textlength(text, font=font))
        seg_widths.append(sw)
        tmp_w += sw

    # Layer height: needs room for ascender + descender + small padding
    pad = max(8, font.size // 12)
    layer_h = asc + desc + 2 * pad
    layer_w = tmp_w + 2 * pad

    layer = Image.new("RGBA", (layer_w, layer_h), (255, 255, 255, 0))
    d = ImageDraw.Draw(layer)

    # Baseline-aligned: y for draw.text is top of glyph, so use pad as top.
    y_top = pad
    x = pad
    for (text, color_code, underline), sw in zip(line, seg_widths):
        color = RED if color_code == "r" else BLACK
        d.text((x, y_top), text, font=font, fill=color)
        if underline:
            uy = y_top + asc + 4
            thickness = max(5, font.size // 14)
            d.line([(x, uy), (x + sw, uy)], fill=RED, width=thickness)
        x += sw

    # Apply shear: x' = x - shear*(y - baseline). We use negative coefficient
    # to lean to the right (top moves right relative to bottom).
    # We expand width to avoid clipping.
    extra_w = int(SHEAR * layer_h) + 4
    new_w = layer_w + extra_w
    # Affine: (a, b, c, d, e, f) gives x_src = a*x + b*y + c
    # We want a forward shear where top of glyphs moves right. In PIL.transform,
    # the matrix maps output->input. So if we want output to be a sheared
    # version (top shifted right), input x at output (x', y') is x' + shear*(layer_h - y')
    sheared = layer.transform(
        (new_w, layer_h),
        Image.AFFINE,
        (1, SHEAR, -SHEAR * (layer_h - 1), 0, 1, 0),
        Image.BICUBIC
    )
    return sheared, pad  # pad = top inset; baseline = pad + asc

def render_ad(lines, out_path):
    max_line_w = W - 2 * PAD_X

    # Per-line max font size, take min
    per_line_max = [fit_size_for_text(line_text(l), max_line_w) for l in lines]
    h_max = min(per_line_max)

    logo_area = 230
    avail_h = H - PAD_TOP - logo_area
    # line_h ratio for Big Shoulders Black: tighter because letters are narrow/tall
    LH_RATIO = 1.05
    v_max = int(avail_h / (len(lines) * LH_RATIO))
    font_size = min(h_max, v_max, 200)

    font = ImageFont.truetype(FONT_PATH, font_size)
    asc, desc = font.getmetrics()
    line_h = int((asc + desc) * 0.95)  # tight

    img = Image.new("RGB", (W, H), WHITE)

    total_h = line_h * len(lines)
    y = PAD_TOP + max(0, (avail_h - total_h) // 2)

    for line in lines:
        sheared, top_pad = render_line_to_layer(line, font, asc, desc)
        # Center horizontally
        lw, lh = sheared.size
        x = (W - lw) // 2
        # Vertically: y is target top of glyph. Layer has 'top_pad' at top, so
        # to align glyph top with y, paste at y - top_pad.
        img.paste(sheared, (x, y - top_pad), sheared)
        y += line_h

    # Logo, se existir. Sem logotipo o anuncio sai na mesma: um ficheiro em
    # falta nunca pode travar o lote inteiro.
    if _P(LOGO_PATH).exists():
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo.thumbnail((150, 150))
            lx = W - logo.width - PAD_X
            ly = H - logo.height - 60
            img.paste(logo, (lx, ly), logo)
        except Exception as e:
            print(f"aviso: logotipo ignorado ({e})")

    img.save(out_path, "PNG", optimize=True)
    print(f"OK  {out_path.name}  size={font_size}px")

if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lines, fname in ADS:
        render_ad(lines, OUT_DIR / fname)
    print(f"Done. {len(ADS)} ads in {OUT_DIR}")
