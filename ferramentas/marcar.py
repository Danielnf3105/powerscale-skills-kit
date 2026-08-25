#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: poe (e mantem) a assinatura da marca nos ficheiros do kit.

  python3 marcar.py            aplica ou atualiza a assinatura
  python3 marcar.py --ver      so diz o que falta, nao escreve

E idempotente: correr outra vez nao acumula assinaturas. Quando se acrescenta
uma skill nova, corre-se isto e ela fica marcada como as outras.

A assinatura diz onde a skill foi DISTRIBUIDA, nao quem a escreveu: parte destas
skills vem de terceiros com licenca propria, e reclamar autoria seria falso.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MARCA = "<!-- powerscale-skills-kit -->"
ASSINATURA = (
    MARCA
    + "\n\n---\n\nDistribuído no **PowerScale Skills Kit** · powerscale.pro\n"
)

# O modelo do CLAUDE.md dela ja tem a seccao "De onde vem este kit", nao leva
# assinatura por cima. Os ficheiros de licenca de terceiros ficam intactos.
FORA = {"LICENSE", "LICENSE.txt", "LICENCE", "NOTICE"}


def alvos():
    for f in sorted(RAIZ.glob("skills/*/SKILL.md")):
        yield f
    for nome in ("LEIA-ME.md", "ENTREGAR.md", "PROCESSO.md"):
        f = RAIZ / nome
        if f.exists():
            yield f
    for f in sorted(RAIZ.glob("processo/*.md")):
        yield f


def marcar(f: Path, escrever=True):
    txt = f.read_text(encoding="utf-8-sig")
    if MARCA in txt:
        corpo = txt.split(MARCA)[0].rstrip()
        novo = corpo + "\n\n" + ASSINATURA
        estado = "igual" if novo == txt else "atualizada"
    else:
        novo = txt.rstrip() + "\n\n" + ASSINATURA
        estado = "posta"
    if escrever and novo != txt:
        with open(f, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(novo)
    return estado


def main():
    ver = "--ver" in sys.argv
    contas = {"posta": 0, "atualizada": 0, "igual": 0}
    faltam = []
    for f in alvos():
        if f.name in FORA:
            continue
        e = marcar(f, escrever=not ver)
        contas[e] += 1
        if ver and e != "igual":
            faltam.append(str(f.relative_to(RAIZ)))
    if ver:
        if faltam:
            print("Sem assinatura da marca (%d):" % len(faltam))
            for x in faltam:
                print("  " + x)
            return 1
        print("Todos os ficheiros do kit estao assinados.")
        return 0
    print("Assinatura: %d postas, %d atualizadas, %d ja estavam bem."
          % (contas["posta"], contas["atualizada"], contas["igual"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
