#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: impressao digital das skills.

  python3 manifesto.py --gerar    reescreve o manifesto.json (fazer antes de publicar)
  python3 manifesto.py            compara o kit com o manifesto e diz o que mudou

Serve duas coisas:
  1. o instalador saber quantas skills TEM de instalar (contar o destino mente,
     porque a pessoa pode ter skills dela la dentro);
  2. detetar skills que ELA alterou, para as guardar antes de escrever por cima.
     Sem isto, atualizar o kit apaga-lhe trabalho e ela nunca mais atualiza.
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANIFESTO = RAIZ / "manifesto.json"


def impressao(pasta: Path) -> str:
    """Hash de uma skill inteira: caminhos e conteudos, por ordem estavel."""
    h = hashlib.sha256()
    for f in sorted(p for p in pasta.rglob("*") if p.is_file()):
        if f.name in (".DS_Store",) or "__pycache__" in f.parts:
            continue
        h.update(str(f.relative_to(pasta)).replace("\\", "/").encode("utf-8"))
        h.update(f.read_bytes())
    return h.hexdigest()


def actual(base: Path = None) -> dict:
    base = base or (RAIZ / "skills")
    return {
        d.name: impressao(d)
        for d in sorted(base.iterdir())
        if d.is_dir() and (d / "SKILL.md").exists()
    }


def ler() -> dict:
    if not MANIFESTO.exists():
        return {}
    return json.loads(MANIFESTO.read_text(encoding="utf-8-sig"))


def gerar():
    skills = actual()
    versao = (RAIZ / "VERSAO").read_text(encoding="utf-8").strip()
    dados = {
        "kit": "powerscale-skills-kit",
        "versao": versao,
        "gerado": date.today().isoformat(),
        "total": len(skills),
        "skills": skills,
    }
    with open(MANIFESTO, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("manifesto.json: %d skills, versao %s" % (len(skills), versao))
    return 0


def comparar():
    m = ler()
    if not m:
        print("Nao ha manifesto.json. Corre: python3 manifesto.py --gerar")
        return 1
    agora, antes = actual(), m.get("skills", {})
    novas = sorted(set(agora) - set(antes))
    idas = sorted(set(antes) - set(agora))
    mudadas = sorted(k for k in set(agora) & set(antes) if agora[k] != antes[k])
    for etiqueta, lista in (("novas", novas), ("desaparecidas", idas), ("alteradas", mudadas)):
        if lista:
            print("%s (%d): %s" % (etiqueta, len(lista), ", ".join(lista)))
    if not (novas or idas or mudadas):
        print("O kit bate certo com o manifesto (%d skills)." % len(agora))
        return 0
    print("\nSe as mudancas sao de proposito: python3 manifesto.py --gerar")
    return 1


if __name__ == "__main__":
    sys.exit(gerar() if "--gerar" in sys.argv else comparar())
