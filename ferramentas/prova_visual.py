#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: a prova de que a instalacao ficou boa, em imagem.

  python3 prova_visual.py                 usa o perfil e grava no Desktop
  python3 prova_visual.py --saida X.png

Gera UM ficheiro 1080x1920 nas cores dela, com o nome do negocio dela e uma
frase cheia de acentos. Num so ficheiro testa: as fontes chegaram, o Pillow
funciona, os caminhos resolvem, a cor do perfil e lida, e o texto portugues sai
inteiro. E a primeira coisa que ela ve a funcionar.

Nao se usa o gerador de anuncios para isto: ele depende de um logotipo que pode
nao existir e a copy dele nao e dela.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estado as E  # noqa: E402

FRASE = "Instalação concluída. Acentuação: ação, coração, ó, ã, ç."
LARGURA, ALTURA = 1080, 1920


def pasta_fontes() -> Path:
    for c in (
        Path(os.environ["KIT_ASSETS"]) / "fontes" if os.environ.get("KIT_ASSETS") else None,
        E.ASSETS / "fontes",
        Path(__file__).resolve().parent.parent / "assets" / "fontes",
    ):
        if c and c.is_dir():
            return c
    raise SystemExit("Nao encontro as fontes. O instalador correu? (esperado em %s)" % (E.ASSETS / "fontes"))


def hex_para_rgb(v, defeito=(13, 13, 13)):
    v = (v or "").strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        return defeito
    try:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return defeito


def luminancia(rgb):
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255


def quebrar(desenho, texto, fonte, largura):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if desenho.textlength(teste, font=fonte) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida")
    ap.add_argument("--perfil")
    a = ap.parse_args()

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Falta o Pillow. Instala com:  %s -m pip install --user Pillow"
              % (E.ler_estado().get("python_cmd") or "python3"))
        return 2  # aviso, nao falha dura: o kit funciona a mesma sem isto

    perfil = json.loads(Path(a.perfil).read_text(encoding="utf-8-sig")) if a.perfil else E.ler_perfil()
    marca = perfil.get("marca") or {}
    negocio = (perfil.get("pessoa") or {}).get("negocio") or (perfil.get("pessoa") or {}).get("nome") or "O teu negócio"

    fundo = hex_para_rgb(marca.get("cor_fundo"), (255, 255, 255))
    acento = hex_para_rgb(marca.get("cor_acento"), (232, 74, 28))
    texto_cor = hex_para_rgb(marca.get("cor_texto"), (13, 13, 13))
    # Se o texto nao se ler sobre o fundo, ganha o contraste e nao a preferencia.
    if abs(luminancia(fundo) - luminancia(texto_cor)) < 0.35:
        texto_cor = (13, 13, 13) if luminancia(fundo) > 0.5 else (255, 255, 255)

    fontes = pasta_fontes()
    f_titulo = ImageFont.truetype(str(fontes / "BigShoulders_60pt-Black.ttf"), 132)
    f_corpo = ImageFont.truetype(str(fontes / "Inter-Medium.ttf"), 46)
    f_rodape = ImageFont.truetype(str(fontes / "Inter-Regular.ttf"), 32)

    img = Image.new("RGB", (LARGURA, ALTURA), fundo)
    d = ImageDraw.Draw(img)
    margem, y = 96, 520

    d.rectangle([margem, y, margem + 180, y + 14], fill=acento)
    y += 90

    for linha in quebrar(d, negocio.upper(), f_titulo, LARGURA - margem * 2):
        d.text((margem, y), linha, font=f_titulo, fill=texto_cor)
        y += 140
    y += 40

    for linha in quebrar(d, FRASE, f_corpo, LARGURA - margem * 2):
        d.text((margem, y), linha, font=f_corpo, fill=texto_cor)
        y += 68

    y += 40
    for linha in quebrar(d, "As cores acima são as tuas. Se não são, diz-me.",
                         f_corpo, LARGURA - margem * 2):
        d.text((margem, y), linha, font=f_corpo, fill=acento)
        y += 68

    logo = None
    for cand in (marca.get("logo_icone"), marca.get("logo_completo")):
        if cand and Path(cand).exists():
            logo = Path(cand)
            break
    if logo:
        try:
            marca_img = Image.open(logo).convert("RGBA")
            marca_img.thumbnail((200, 200))
            img.paste(marca_img, (LARGURA - marca_img.width - margem,
                                  ALTURA - marca_img.height - 150), marca_img)
        except Exception:
            pass  # um logotipo estragado nunca trava a prova

    d.text((margem, ALTURA - 130), "PowerScale Skills Kit", font=f_rodape, fill=acento)

    destino = Path(a.saida) if a.saida else (Path.home() / "Desktop" / "kit-instalado.png")
    if not destino.parent.exists():
        destino = Path.home() / "kit-instalado.png"
    img.save(destino)
    print("Prova visual: %s (%d bytes)" % (destino, destino.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
