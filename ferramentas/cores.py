#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: tira as cores dominantes de uma imagem.

  python3 cores.py ~/Desktop/captura.png

Plano B da descoberta, para quando o site nao entrega o estilo no HTML (Wix,
Squarespace, sites feitos em React). Uma captura de ecra da pagina inicial e o
suficiente. Isto continua a ser medir. O que nao se faz e adivinhar uma cor.
"""
import sys
from collections import Counter
from pathlib import Path


def cinzento(rgb, tolerancia=18):
    return max(rgb) - min(rgb) <= tolerancia


def dominantes(caminho: Path, quantas=6):
    """Duas passagens: agrupar para contar, e depois devolver a cor EXATA.

    Agrupar e preciso, senao o anti-aliasing de um titulo devolve duzentos
    tons do mesmo laranja. Mas o que sai tem de ser o hex que esta mesmo na
    imagem, nao o centro do grupo: quem vai gravar isto no perfil precisa da
    cor da marca, nao de uma aproximacao.
    """
    from PIL import Image
    img = Image.open(caminho).convert("RGB")
    img.thumbnail((400, 400))  # chega e sobra, e e rapido

    pixeis = list(img.getdata())
    total = len(pixeis)
    grupos = Counter(tuple(v // 16 * 16 for v in p) for p in pixeis)
    exatas = Counter(pixeis)

    def exata_do_grupo(g):
        candidatas = [(n, c) for c, n in exatas.items()
                      if all(c[i] // 16 * 16 == g[i] for i in range(3))]
        return max(candidatas)[1] if candidatas else g

    neutras, candidatas = [], []
    for grupo, n in grupos.most_common(150):
        exata = exata_do_grupo(grupo)
        if cinzento(grupo):
            if len(neutras) < 3:
                neutras.append((exata, n / total))
        else:
            candidatas.append((exata, n / total))

    # A cor da marca aparece quase sempre em texto fino e em detalhes, por isso
    # perde em area para os tons esbatidos do anti-aliasing, que sao a mesma cor
    # lavada pelo fundo. Ordenar so por area devolve a lavagem, nao a marca.
    # Pesar pela saturacao poe a cor a serio a frente.
    def peso(par):
        (r, g, b), area = par
        sat = (max(r, g, b) - min(r, g, b)) / max(max(r, g, b), 1)
        return area * (sat ** 2)

    candidatas.sort(key=peso, reverse=True)
    return neutras[:3], candidatas[:quantas]


def hexa(rgb):
    return "#%02X%02X%02X" % rgb


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    f = Path(sys.argv[1]).expanduser()
    if not f.exists():
        print("Nao encontro a imagem: %s" % f)
        return 1
    try:
        neutras, cores = dominantes(f)
    except ImportError:
        print("Falta o Pillow. Instala com: python3 -m pip install --user Pillow")
        return 2

    print("Medido em: %s" % f.name)
    print("")
    print("Fundo e texto (os neutros, por ordem de area):")
    for rgb, p in neutras:
        print("  %s  %5.1f%%" % (hexa(rgb), p * 100))
    print("")
    print("Cores da marca (candidatas a principal e acento):")
    if not cores:
        print("  nenhuma. A pagina e toda a preto e branco, e isso tambem e uma decisao.")
    for rgb, p in cores:
        print("  %s  %5.1f%%" % (hexa(rgb), p * 100))
    print("")
    print("A mais usada das cores costuma ser a principal, e a que aparece em")
    print("botoes e detalhes e o acento. Confirma com ela antes de gravar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
