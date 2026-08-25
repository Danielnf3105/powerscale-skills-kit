#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: estado da instalacao e perfil de quem instala.

Dois ficheiros, dois trabalhos:
  ~/.claude/kit/estado.json   que fases estao feitas (marca o progresso)
  ~/.claude/kit/perfil.json   as respostas da entrevista (grava-se a CADA resposta)

Sem o segundo, uma entrevista interrompida perde-se toda, que era o defeito do
kit anterior. Toda a escrita e atomica: um Ctrl+C nunca deixa JSON truncado.

Uso como CLI:
  python3 estado.py --mostrar
  python3 estado.py --marcar instalar=feita
  python3 estado.py --marcar entrevista=em_curso --nota "parou na pergunta 4"
  python3 estado.py --proxima
  python3 estado.py --definir python_cmd="py -3"
  python3 estado.py --responder pessoa.nome="Carolina Dinis"
  python3 estado.py --responder trabalho.tipos='["copy","anuncios"]'
"""
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

CASA = Path.home()
KIT_DIR = CASA / ".claude" / "kit"
ESTADO = KIT_DIR / "estado.json"
PERFIL = KIT_DIR / "perfil.json"
CLAUDE_MD = CASA / ".claude" / "CLAUDE.md"
SKILLS = CASA / ".claude" / "skills"
ASSETS = CASA / ".claude" / "kit-assets"
COFRE = CASA / ".config" / "chaves" / "secrets.env"
PROCESSO = KIT_DIR / "processo"

FASES = [
    "preparar",
    "prerrequisitos",
    "instalar",
    "descobrir",
    "entrevista",
    "perfil",
    "verificar",
    "primeiro-trabalho",
]

ESTADOS = ("por_fazer", "em_curso", "feita", "falhou", "saltada")


def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _gravar(caminho: Path, dados: dict):
    """Escrita atomica: escreve num temporario ao lado e troca de nome."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(caminho.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, caminho)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _ler(caminho: Path, defeito: dict) -> dict:
    if not caminho.exists():
        return json.loads(json.dumps(defeito))
    try:
        with open(caminho, encoding="utf-8-sig") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Ficheiro corrompido nao pode travar a instalacao: guarda e recomeca.
        estragado = caminho.with_suffix(".estragado-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
        try:
            caminho.rename(estragado)
        except OSError:
            pass
        return json.loads(json.dumps(defeito))


def estado_vazio() -> dict:
    return {
        "kit": "powerscale-skills-kit",
        "kit_versao": "",
        "kit_caminho": "",
        "origem": "",
        "python_cmd": "",
        "perfil_hash": "",
        "reinicio_pedido": False,
        "criado": agora(),
        "atualizado": agora(),
        "fases": {f: {"estado": "por_fazer", "em": "", "nota": ""} for f in FASES},
    }


def perfil_vazio() -> dict:
    return {
        "versao_esquema": 1,
        "completo": False,
        "atualizado": agora(),
        "pessoa": {
            "nome": "", "assistente": "", "negocio": "", "papel": "",
            "estilo_resposta": "", "lingua": "pt-PT", "outras_linguas": [],
        },
        "negocio": {"oferta": "", "quem_compra": "", "prova": [], "modelo": ""},
        "marca": {
            "cor_principal": "", "cor_acento": "", "cor_fundo": "", "cor_texto": "",
            "tipografia": "", "logo_completo": None, "logo_icone": None,
            "tratamento_publico": "", "nunca_dizer": [], "fonte_cores": "",
        },
        "trabalho": {"tipos": [], "para_clientes": False, "clientes": [], "urgente": ""},
        "ferramentas": {"usa": [], "operar_sozinho": [], "fora": []},
        "travoes": {
            "confirmar_antes": ["enviar", "publicar", "apagar", "gastar"],
            "extra": [],
        },
        "maquina": {
            "so": "", "terminal": "", "gestor_pacotes": "", "python_cmd": "",
            "pasta_trabalho": "", "constrangimentos": "",
        },
        "canais": [],
        "voz": {
            "ficheiro": "", "fontes": [], "regra_de_ouro": "",
            "recolhido_em": "", "amostras": 0,
        },
        "descoberta": {"site": "", "instagram": "", "fonte": "", "recolhido_em": "", "notas": []},
    }


# Campos sem os quais o CLAUDE.md sairia oco. Verificados pelo gerador.
OBRIGATORIOS = [
    "pessoa.nome",
    "pessoa.assistente",
    "pessoa.papel",
    "pessoa.estilo_resposta",
    "negocio.oferta",
    "negocio.quem_compra",
    "marca.tratamento_publico",
    "maquina.so",
    "trabalho.urgente",
    "canais",
    "voz.regra_de_ouro",
]


def ler_estado() -> dict:
    e = _ler(ESTADO, estado_vazio())
    base = estado_vazio()
    for k, v in base.items():
        e.setdefault(k, v)
    for f in FASES:
        e["fases"].setdefault(f, {"estado": "por_fazer", "em": "", "nota": ""})
    return e


def gravar_estado(e: dict):
    e["atualizado"] = agora()
    _gravar(ESTADO, e)


def ler_perfil() -> dict:
    p = _ler(PERFIL, perfil_vazio())
    base = perfil_vazio()
    for k, v in base.items():
        if k not in p:
            p[k] = v
        elif isinstance(v, dict) and isinstance(p[k], dict):
            for k2, v2 in v.items():
                p[k].setdefault(k2, v2)
    return p


def gravar_perfil(p: dict):
    p["atualizado"] = agora()
    _gravar(PERFIL, p)


def marcar_fase(fase: str, estado: str = "feita", nota: str = ""):
    if fase not in FASES:
        raise SystemExit("Fase desconhecida: %s. Conhecidas: %s" % (fase, ", ".join(FASES)))
    if estado not in ESTADOS:
        raise SystemExit("Estado desconhecido: %s. Conhecidos: %s" % (estado, ", ".join(ESTADOS)))
    e = ler_estado()
    e["fases"][fase] = {"estado": estado, "em": agora(), "nota": nota}
    gravar_estado(e)
    return e


def proxima_fase(e: dict = None) -> str:
    e = e or ler_estado()
    for f in FASES:
        if e["fases"][f]["estado"] not in ("feita", "saltada"):
            return f
    return ""


def caminho(chave: str, dados: dict):
    alvo = dados
    for parte in chave.split("."):
        if not isinstance(alvo, dict) or parte not in alvo:
            return None
        alvo = alvo[parte]
    return alvo


def definir_caminho(chave: str, valor, dados: dict):
    partes = chave.split(".")
    alvo = dados
    for parte in partes[:-1]:
        alvo = alvo.setdefault(parte, {})
    alvo[partes[-1]] = valor


def responder(chave: str, valor):
    """Grava UMA resposta da entrevista. Chamar depois de cada resposta."""
    p = ler_perfil()
    definir_caminho(chave, valor, p)
    gravar_perfil(p)
    return p


def em_falta(p: dict = None):
    p = p or ler_perfil()
    falta = []
    for c in OBRIGATORIOS:
        v = caminho(c, p)
        if v is None or v == "" or v == []:
            falta.append(c)
    return falta


def _valor_de(txt: str):
    txt = txt.strip()
    if txt[:1] in "[{" or txt in ("true", "false", "null"):
        try:
            return json.loads(txt)
        except json.JSONDecodeError:
            pass
    return txt


def main(argv):
    args = list(argv)
    nota = ""
    if "--nota" in args:
        i = args.index("--nota")
        nota = args[i + 1]
        del args[i:i + 2]

    if not args or "--mostrar" in args:
        e = ler_estado()
        p = ler_perfil()
        print("PowerScale Skills Kit %s" % (e.get("kit_versao") or "?"))
        print("Kit em: %s (origem: %s)" % (e.get("kit_caminho") or "?", e.get("origem") or "?"))
        print("Python: %s" % (e.get("python_cmd") or "?"))
        print("")
        for f in FASES:
            d = e["fases"][f]
            marca = {"feita": "[x]", "em_curso": "[~]", "falhou": "[!]", "saltada": "[-]"}.get(d["estado"], "[ ]")
            print("%s %-18s %-10s %s" % (marca, f, d["estado"], d.get("nota", "")))
        prox = proxima_fase(e)
        print("")
        print("Proxima fase: %s" % (prox or "nenhuma, o arranque esta completo"))
        falta = em_falta(p)
        if falta:
            print("Perfil por preencher: %s" % ", ".join(falta))
        else:
            print("Perfil: completo" if p.get("completo") else "Perfil: campos todos preenchidos, falta marcar completo")
        return 0

    if "--proxima" in args:
        print(proxima_fase() or "")
        return 0

    if "--marcar" in args:
        par = args[args.index("--marcar") + 1]
        fase, _, est = par.partition("=")
        marcar_fase(fase, est or "feita", nota)
        print("%s = %s" % (fase, est or "feita"))
        return 0

    if "--definir" in args:
        par = args[args.index("--definir") + 1]
        chave, _, val = par.partition("=")
        e = ler_estado()
        definir_caminho(chave, _valor_de(val), e)
        gravar_estado(e)
        print("estado.%s = %s" % (chave, val))
        return 0

    if "--responder" in args:
        par = args[args.index("--responder") + 1]
        chave, _, val = par.partition("=")
        responder(chave, _valor_de(val))
        print("perfil.%s gravado" % chave)
        falta = em_falta()
        print("Falta: %s" % (", ".join(falta) if falta else "nada"))
        return 0

    if "--falta" in args:
        falta = em_falta()
        print("\n".join(falta))
        return 1 if falta else 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
