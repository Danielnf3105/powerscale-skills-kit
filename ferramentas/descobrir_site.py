#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: le o site dela para nao lhe perguntar o que ja la esta.

  python3 descobrir_site.py https://osite.pt
  python3 descobrir_site.py https://osite.pt --gravar   grava em perfil.descoberta

Vem de la: o que vende e a quem, as cores com o numero de vezes que aparecem, a
tipografia, e se trata por tu ou por voce.

Nunca bloqueia. Se o site nao responder, ou nao trouxer estilo nenhum (acontece
em Wix, Squarespace e React), sai com fonte "nenhuma" e a entrevista pergunta.
O plano B e uma captura de ecra e o cores.py.

O Instagram nao entra aqui: exige sessao iniciada e nao se le por programa. Pede
antes tres publicacoes que sejam mesmo a voz dela.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estado as E  # noqa: E402

AGENTE = "Mozilla/5.0 (compatible; PowerScaleSkillsKit/2.0; +https://powerscale.pro)"
TEMPO = 12

CINZA = re.compile(r"^#?(?:([0-9a-f])\1\1|([0-9a-f]{2})\2\2)$", re.I)
HEX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
RGB = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")
FAMILIA = re.compile(r"font-family\s*:\s*([^;}\"']+)", re.I)


class Texto(HTMLParser):
    """So o que interessa: titulos, descricao, e o texto visivel."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titulo = ""
        self.descricao = ""
        self.h = []
        self.texto = []
        self.css = []
        self.logo = ""
        self._onde = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._onde = tag
        if tag == "meta":
            nome = (a.get("name") or a.get("property") or "").lower()
            if nome in ("description", "og:description") and not self.descricao:
                self.descricao = (a.get("content") or "").strip()
        elif tag == "link" and "stylesheet" in (a.get("rel") or ""):
            if a.get("href"):
                self.css.append(a["href"])
        elif tag == "img" and not self.logo:
            if "logo" in ((a.get("src") or "") + (a.get("alt") or "")).lower():
                self.logo = a.get("src") or ""

    def handle_endtag(self, tag):
        self._onde = ""

    def handle_data(self, d):
        d = d.strip()
        if not d:
            return
        if self._onde == "title" and not self.titulo:
            self.titulo = d
        elif self._onde in ("h1", "h2", "h3"):
            self.h.append(d)
        elif self._onde in ("p", "li", "span", "a", "div", "strong", "em"):
            self.texto.append(d)


def buscar(url, limite=400_000):
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=TEMPO) as r:
        bruto = r.read(limite)
    for cod in ("utf-8", "latin-1"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", "replace")


def normalizar(v):
    v = v.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return "#" + v.upper() if len(v) == 6 else None


def cores_de(css):
    c = Counter()
    for m in HEX.finditer(css):
        v = normalizar(m.group(1))
        if v:
            c[v] += 1
    for m in RGB.finditer(css):
        try:
            v = "#%02X%02X%02X" % tuple(int(x) for x in m.groups())
            c[v] += 1
        except ValueError:
            pass
    interessantes = []
    for v, n in c.most_common(40):
        r, g, b = (int(v[i:i + 2], 16) for i in (1, 3, 5))
        if max(r, g, b) - min(r, g, b) <= 16:
            continue  # preto, branco e cinzentos nao dizem qual e a marca
        interessantes.append((v, n))
    return interessantes[:6], [v for v, _ in c.most_common(6)]


def tratamento(texto):
    tu = len(re.findall(r"\b(o teu|a tua|os teus|as tuas|tens|queres|podes|vais)\b", texto, re.I))
    voce = len(re.findall(r"\b(o seu|a sua|os seus|as suas|tem de|deseja|pode contar|irá)\b", texto, re.I))
    if tu > voce * 1.4 and tu >= 3:
        return "tu", tu, voce
    if voce > tu * 1.4 and voce >= 3:
        return "voce", tu, voce
    return "", tu, voce


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--gravar", action="store_true")
    a = ap.parse_args()

    url = a.url if a.url.startswith("http") else "https://" + a.url
    resultado = {"site": url, "fonte": "nenhuma", "notas": []}

    try:
        html = buscar(url)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
        print("Nao consegui ler o site (%s)." % e)
        print("Nao faz mal: pede-lhe uma captura de ecra da pagina inicial e mede")
        print("com  python3 cores.py <imagem>. Se nem isso, pergunta na entrevista.")
        if a.gravar:
            p = E.ler_perfil()
            p["descoberta"].update(resultado)
            E.gravar_perfil(p)
        return 0  # nunca bloqueia

    parser = Texto()
    parser.feed(html)

    css = html
    for href in parser.css[:5]:
        try:
            css += buscar(urljoin(url, href), 250_000)
        except Exception:
            continue

    marca, todas = cores_de(css)
    familias = []
    for m in FAMILIA.finditer(css):
        f = m.group(1).split(",")[0].strip(" \"'")
        if f and f.lower() not in ("inherit", "initial", "unset") and f not in familias:
            familias.append(f)

    corpo = " ".join(parser.h + parser.texto)[:20000]
    trato, n_tu, n_voce = tratamento(corpo)

    resultado.update({
        "fonte": "site" if (marca or familias) else "site-sem-estilo",
        "titulo": parser.titulo,
        "descricao": parser.descricao,
        "titulos": parser.h[:8],
        "cores_marca": [v for v, _ in marca],
        "cores_todas": todas,
        "tipografia": familias[:3],
        "tratamento": trato,
        "logo": urljoin(url, parser.logo) if parser.logo else "",
        "recolhido_em": E.agora(),
    })

    print("Site: %s" % url)
    print("Titulo: %s" % (parser.titulo or "(sem titulo)"))
    if parser.descricao:
        print("Descricao: %s" % parser.descricao[:160])
    if parser.h:
        print("Diz na pagina: %s" % " / ".join(parser.h[:4]))
    print("")
    print("Cores da marca: %s" % (", ".join(v for v, _ in marca) or "nenhuma encontrada no CSS"))
    print("Tipografia: %s" % (", ".join(familias[:3]) or "nao declarada"))
    print("Tratamento: %s (tu:%d, voce:%d)" % (trato or "indeterminado", n_tu, n_voce))
    print("")

    if not marca:
        print("Sem cores no CSS. E normal em Wix, Squarespace e sites em React:")
        print("o estilo nao vem no HTML. Pede-lhe uma captura da pagina inicial e")
        print("corre  python3 cores.py <imagem>.")
    else:
        print("Leva isto ao cartao de confirmacao da entrevista (pergunta 2).")
        print("Mostras o retrato, ela corrige. Nao lhe perguntes o que ja mediste.")

    if a.gravar:
        p = E.ler_perfil()
        p["descoberta"].update(resultado)
        E.gravar_perfil(p)
        print("")
        print("Gravado em perfil.descoberta. As cores so entram em marca.* depois")
        print("de ela confirmar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
