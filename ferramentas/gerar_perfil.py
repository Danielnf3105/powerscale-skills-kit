#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: escreve o ~/.claude/CLAUDE.md a partir do perfil.

  python3 gerar_perfil.py                       usa ~/.claude/kit/perfil.json
  python3 gerar_perfil.py --perfil X.json       usa outro perfil (testes)
  python3 gerar_perfil.py --saida Y.md          escreve noutro sitio (testes)
  python3 gerar_perfil.py --ver                 mostra o resultado, nao grava

O que sai fica entre <!-- kit:inicio --> e <!-- kit:fim -->. Tudo o que a pessoa
escrever FORA desses marcadores sobrevive a uma nova geracao, byte a byte. Sem
isto, a primeira vez que ela editasse o ficheiro a mao perdia tudo, e passava a
haver medo de voltar a correr.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estado as E  # noqa: E402

INICIO = "<!-- kit:inicio -->"
FIM = "<!-- kit:fim -->"
REPO = "github.com/Danielnf3105/powerscale-skills-kit"
SITE = "powerscale.pro"

# ------------------------------------------------------------------ template

FICHA = re.compile(r"{{\s*(#se|#cada|/se|/cada)?\s*([a-zA-Z0-9_.]*)\s*}}")


SOZINHA = re.compile(
    r"^[ \t]*({{\s*(?:#se|#cada|/se|/cada)\s*[a-zA-Z0-9_.]*\s*}})[ \t]*\r?\n",
    re.MULTILINE,
)


def _limpar_linhas_de_bloco(txt):
    """Uma tag de bloco sozinha na linha leva a linha inteira com ela.

    E o que o Mustache faz. Sem isto, um {{#cada}} de bullets deixa uma linha
    em branco entre cada item, e o markdown passa a lista solta.
    """
    return SOZINHA.sub(r"\1", txt)


def _tokenizar(txt):
    txt = _limpar_linhas_de_bloco(txt)
    pos, saida = 0, []
    for m in FICHA.finditer(txt):
        if m.start() > pos:
            saida.append(("texto", txt[pos:m.start()]))
        tipo, nome = m.group(1), m.group(2)
        if tipo == "#se":
            saida.append(("se", nome))
        elif tipo == "#cada":
            saida.append(("cada", nome))
        elif tipo == "/se":
            saida.append(("fim_se", nome))
        elif tipo == "/cada":
            saida.append(("fim_cada", nome))
        else:
            saida.append(("var", nome))
        pos = m.end()
    saida.append(("texto", txt[pos:]))
    return saida


def _arvore(tokens, i=0, ate=None):
    nos = []
    while i < len(tokens):
        tipo, valor = tokens[i]
        if tipo in ("fim_se", "fim_cada"):
            if ate is None:
                raise ValueError("bloco fechado sem abrir: %s" % valor)
            return nos, i + 1
        if tipo in ("se", "cada"):
            filhos, i = _arvore(tokens, i + 1, ate=tipo)
            nos.append((tipo, valor, filhos))
            continue
        nos.append((tipo, valor, None))
        i += 1
    if ate is not None:
        raise ValueError("bloco aberto e nunca fechado")
    return nos, i


def _valor(chave, ctx, item):
    if chave == "" or chave == ".":
        return item
    if chave.startswith("."):
        if isinstance(item, dict):
            return item.get(chave[1:], "")
        return ""
    v = E.caminho(chave, ctx)
    return "" if v is None else v


def _verdade(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    if isinstance(v, (list, dict, str)):
        return len(v) > 0
    return bool(v)


def _render(nos, ctx, item=None):
    out = []
    for tipo, valor, filhos in nos:
        if tipo == "texto":
            out.append(valor)
        elif tipo == "var":
            v = _valor(valor, ctx, item)
            if isinstance(v, bool):
                out.append("sim" if v else "não")
            elif isinstance(v, list):
                out.append(", ".join(str(x) for x in v))
            else:
                out.append("" if v is None else str(v))
        elif tipo == "se":
            if _verdade(_valor(valor, ctx, item)):
                out.append(_render(filhos, ctx, item))
        elif tipo == "cada":
            lista = _valor(valor, ctx, item)
            if isinstance(lista, list):
                for sub in lista:
                    out.append(_render(filhos, ctx, sub))
    return "".join(out)


def render(tpl, ctx):
    nos, _ = _arvore(_tokenizar(tpl))
    return _render(nos, ctx)


# ------------------------------------------------------------------ contexto

PERSONALIDADE = {
    "direta": "direta. Sem enfeites, vou ao assunto.",
    "com_contexto": "direta, mas dou o contexto e o porque antes da conclusao.",
}

LINGUAS = {
    "pt-PT": "português de Portugal",
    "pt-BR": "português do Brasil",
    "en": "inglês",
    "es": "espanhol",
    "fr": "francês",
}


def contexto(perfil, versao):
    c = json.loads(json.dumps(perfil))
    p = c.setdefault("pessoa", {})
    estilo = (p.get("estilo_resposta") or "direta").strip()
    p["personalidade"] = PERSONALIDADE.get(estilo, PERSONALIDADE["direta"])
    lingua = (p.get("lingua") or "pt-PT").strip()
    p["lingua_nome"] = LINGUAS.get(lingua, lingua)
    p["e_pt_pt"] = lingua == "pt-PT"

    m = c.setdefault("maquina", {})
    if (m.get("so") or "").lower().startswith("win"):
        m["cofre"] = r"%USERPROFILE%\.config\chaves\secrets.env"
    else:
        m["cofre"] = "~/.config/chaves/secrets.env"
    m.setdefault("python_cmd", "python3")

    # Defeitos visiveis, para nunca sair uma tabela de marca vazia.
    marca = c.setdefault("marca", {})
    for k, d in (("cor_principal", "#0D0D0D"), ("cor_acento", "#E84A1C"),
                 ("cor_fundo", "#FFFFFF"), ("cor_texto", "#0D0D0D")):
        if not marca.get(k):
            marca[k] = d
    if not marca.get("tipografia"):
        marca["tipografia"] = "Inter (a do kit)"
    if not marca.get("fonte_cores"):
        marca["fonte_cores"] = "por definir, a confirmar com ela"

    c["kit"] = {
        "repo": REPO,
        "site": SITE,
        "versao": versao,
        "data": date.today().isoformat(),
    }
    return c


def versao_do_kit():
    f = Path(__file__).resolve().parent.parent / "VERSAO"
    if f.exists():
        return f.read_text(encoding="utf-8").strip()
    e = E.ler_estado()
    return e.get("kit_versao") or "?"


# ------------------------------------------------------------------ escrita

def juntar(bloco, existente):
    """Poe o bloco gerado no ficheiro, sem destruir o que ja la estava."""
    marcado = INICIO + "\n" + bloco.rstrip() + "\n" + FIM + "\n"
    if existente is None:
        return marcado, "novo"
    if INICIO in existente and FIM in existente:
        i = existente.index(INICIO)
        j = existente.index(FIM) + len(FIM) + 1
        return existente[:i] + marcado + existente[j:], "bloco substituido"
    return (marcado + "\n## O que já cá estava\n\n" + existente.strip() + "\n"), "juntado ao que existia"


def arrumar(txt):
    """Tirar blocos deixa linhas coladas. Repor o ar que o markdown precisa."""
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    # separador ou titulo colado a linha de cima passa a ter linha em branco
    txt = re.sub(r"(?<=\S)\n(---\n)", r"\n\n\1", txt)
    txt = re.sub(r"(?<=\S)\n(#{2,3} )", r"\n\n\1", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip() + "\n"


PROIBIDOS = ("{{", "<NOME", "<#HEX", "<cliente", "<Negócio", "<o que faz")


def validar(texto):
    erros = []
    for p in PROIBIDOS:
        if p in texto:
            erros.append("sobrou um marcador por preencher: %s" % p)
    if "—" in texto:
        erros.append("tem travessão (em-dash), que é proibido em tudo o que sai daqui")
    return erros


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--perfil")
    ap.add_argument("--saida")
    ap.add_argument("--ver", action="store_true")
    a = ap.parse_args()

    if a.perfil:
        perfil = json.loads(Path(a.perfil).read_text(encoding="utf-8-sig"))
    else:
        perfil = E.ler_perfil()

    falta = E.em_falta(perfil)
    if falta:
        print("Nao dá para escrever o CLAUDE.md ainda. Falta responder a:")
        for f in falta:
            print("  - %s" % f)
        print("\nVolta à fase da entrevista (processo/4-entrevista.md).")
        return 1

    tpl_f = Path(__file__).resolve().parent.parent / "modelo" / "CLAUDE.md.tpl"
    if not tpl_f.exists():
        tpl_f = E.KIT_DIR / "modelo" / "CLAUDE.md.tpl"
    if not tpl_f.exists():
        print("Nao encontro o modelo CLAUDE.md.tpl (nem no kit nem em ~/.claude/kit/modelo/).")
        return 1

    versao = versao_do_kit()
    bloco = render(tpl_f.read_text(encoding="utf-8"), contexto(perfil, versao))
    bloco = arrumar(bloco)

    erros = validar(bloco)
    if erros:
        print("O ficheiro gerado nao passa na verificacao:")
        for e in erros:
            print("  - %s" % e)
        return 1

    if a.ver:
        print(bloco)
        return 0

    destino = Path(a.saida) if a.saida else E.CLAUDE_MD
    existente = destino.read_text(encoding="utf-8-sig") if destino.exists() else None

    if existente is not None and INICIO not in existente:
        copia = destino.with_name(destino.name + ".backup-" + E.agora().replace(" ", "-").replace(":", ""))
        with open(copia, "w", encoding="utf-8", newline="\n") as f:
            f.write(existente)
        print("Ja existia um %s. Guardei uma cópia em %s" % (destino.name, copia.name))

    final, como = juntar(bloco, existente)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(final)

    if not a.saida:
        import hashlib
        perfil["completo"] = True
        E.gravar_perfil(perfil)
        # O hash tem de ser do perfil TAL COMO fica gravado e TAL COMO o
        # verificador o vai ler, senao o aviso de "o perfil mudou" dispara
        # sempre, e um aviso que grita todos os dias deixa de se ler.
        h = hashlib.sha256(
            json.dumps(E.ler_perfil(), sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        est = E.ler_estado()
        est["perfil_hash"] = h
        est["kit_versao"] = versao
        E.gravar_estado(est)

    print("Escrito: %s (%s, %d linhas)" % (destino, como, final.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
