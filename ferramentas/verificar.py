#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: diz se isto ficou bem instalado, e o que falta.

  python3 verificar.py --nivel instalacao   logo a seguir a instalar
  python3 verificar.py --nivel completo     no fim do arranque (o que conta)
  python3 verificar.py --json               para outro programa ler

Saida: 0 pronto, 1 ha falhas, 2 so avisos.

Dois niveis de proposito: o nivel "instalacao" tem de poder passar ANTES de
haver perfil nenhum, senao nao serve para diagnosticar nada a meio.
"""
import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estado as E  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
OK, FALHA, AVISO = "ok", "falha", "aviso"
PROIBIDOS = ("{{", "<NOME", "<#HEX", "<cliente", "<Negócio")


class Relatorio:
    def __init__(self):
        self.linhas = []

    def add(self, id, estado, msg, resolver=""):
        self.linhas.append({"id": id, "estado": estado, "mensagem": msg, "resolver": resolver})

    def ok(self, id, msg):
        self.add(id, OK, msg)

    def falha(self, id, msg, resolver=""):
        self.add(id, FALHA, msg, resolver)

    def aviso(self, id, msg, resolver=""):
        self.add(id, AVISO, msg, resolver)

    def codigo(self):
        if any(l["estado"] == FALHA for l in self.linhas):
            return 1
        if any(l["estado"] == AVISO for l in self.linhas):
            return 2
        return 0


def manifesto():
    f = RAIZ / "manifesto.json"
    if not f.exists():
        f = E.KIT_DIR / "manifesto.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def tem_bom(f: Path) -> bool:
    with open(f, "rb") as fh:
        return fh.read(3) == b"\xef\xbb\xbf"


# ------------------------------------------------------------ instalacao

def ver_skills(r):
    m = manifesto()
    esperado = m.get("total")
    if not E.SKILLS.is_dir():
        r.falha("skills", "Nao ha pasta de skills em %s" % E.SKILLS,
                "correr o instalador do kit")
        return
    instaladas = {d.name for d in E.SKILLS.iterdir()
                  if d.is_dir() and (d / "SKILL.md").exists()}
    if not esperado:
        r.aviso("skills", "%d skills instaladas, mas nao ha manifesto para comparar"
                % len(instaladas), "python3 ferramentas/manifesto.py --gerar")
        return
    faltam = sorted(set(m.get("skills", {})) - instaladas)
    if faltam:
        r.falha("skills", "Faltam %d skills: %s" % (len(faltam), ", ".join(faltam[:6])),
                "correr o instalador outra vez")
    else:
        r.ok("skills", "%d skills do kit instaladas (a pessoa tem %d ao todo)"
             % (len(m.get("skills", {})), len(instaladas)))
    sem_nome = [d.name for d in E.SKILLS.iterdir()
                if d.is_dir() and (d / "SKILL.md").exists()
                and "name:" not in (d / "SKILL.md").read_text(encoding="utf-8-sig", errors="replace")[:600]]
    if sem_nome:
        r.aviso("skills-frontmatter", "Sem 'name:' no cabecalho: %s" % ", ".join(sem_nome),
                "sem isso a skill nao e invocavel por /nome")


def ver_settings(r):
    f = E.CASA / ".claude" / "settings.json"
    if not f.exists():
        r.falha("settings", "Nao ha %s" % f, "correr o instalador")
        return
    if tem_bom(f):
        r.falha("settings", "O settings.json tem BOM e nao vai parsear",
                "reescrever o ficheiro em UTF-8 sem BOM (o PowerShell poe BOM)")
        return
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        r.falha("settings", "settings.json invalido: %s" % e, "corrigir o JSON a mao")
        return
    if not (d.get("permissions", {}).get("allow")):
        r.aviso("settings", "settings.json sem permissoes de allow",
                "o Claude vai pedir autorizacao a toda a hora")
    else:
        r.ok("settings", "permissoes instaladas e validas")


def ver_assets(r):
    fontes = E.ASSETS / "fontes"
    if not fontes.is_dir():
        r.falha("assets", "Nao ha fontes em %s" % fontes, "correr o instalador")
        return
    ttf = [f for f in fontes.glob("*.ttf") if f.stat().st_size > 10_000]
    if len(ttf) < 9:
        r.falha("assets", "So %d fontes utilizaveis (esperadas 9)" % len(ttf),
                "correr o instalador outra vez")
        return
    try:
        from PIL import ImageFont
        ImageFont.truetype(str(fontes / "BigShoulders_60pt-Black.ttf"), 40)
        r.ok("assets", "%d fontes, e o Pillow abre-as" % len(ttf))
    except ImportError:
        r.aviso("assets", "%d fontes, mas falta o Pillow para as usar" % len(ttf),
                "%s -m pip install --user Pillow" % (E.ler_estado().get("python_cmd") or "python3"))
    except Exception as e:
        r.falha("assets", "As fontes nao abrem: %s" % e, "reinstalar os assets")


def ver_cofre(r):
    if not E.COFRE.exists():
        r.falha("cofre", "Nao ha cofre de chaves em %s" % E.COFRE, "correr o instalador")
        return
    if platform.system() != "Windows":
        modo = oct(E.COFRE.stat().st_mode)[-3:]
        if modo != "600":
            r.aviso("cofre", "O cofre esta em modo %s, devia ser 600" % modo,
                    "chmod 600 %s" % E.COFRE)
            return
    r.ok("cofre", "cofre de chaves no sitio, so para ela")


def ver_processo(r):
    if not (E.PROCESSO / "4-entrevista.md").exists():
        r.falha("processo", "O processo nao foi copiado para %s" % E.PROCESSO,
                "correr o instalador (a skill arranque le daqui, nao do repo)")
    else:
        n = len(list(E.PROCESSO.glob("*.md")))
        r.ok("processo", "processo copiado (%d ficheiros), o arranque sobrevive a mudar o kit de pasta" % n)


def ver_assinatura(r):
    if not RAIZ.joinpath("skills").is_dir():
        return
    sem = [d.name for d in sorted((RAIZ / "skills").iterdir())
           if d.is_dir() and (d / "SKILL.md").exists()
           and "<!-- powerscale-skills-kit -->" not in (d / "SKILL.md").read_text(encoding="utf-8-sig", errors="replace")]
    if sem:
        r.aviso("assinatura", "Skills sem assinatura do kit: %s" % ", ".join(sem),
                "python3 ferramentas/marcar.py")
    else:
        r.ok("assinatura", "todas as skills do kit assinadas")


# ------------------------------------------------------------ completo

def ver_perfil(r):
    if not E.PERFIL.exists():
        r.falha("perfil", "Nao ha perfil. O kit esta instalado mas nao e de ninguem.",
                "correr a entrevista: /arranque")
        return None
    p = E.ler_perfil()
    falta = E.em_falta(p)
    if falta:
        r.falha("perfil", "Perfil por acabar, falta: %s" % ", ".join(falta),
                "retomar a entrevista: /arranque")
    elif not p.get("completo"):
        r.aviso("perfil", "Perfil preenchido mas nao marcado como completo",
                "python3 ferramentas/gerar_perfil.py")
    else:
        r.ok("perfil", "perfil de %s, completo" % (p.get("pessoa", {}).get("nome") or "?"))
    return p


def ver_claude_md(r, p):
    f = E.CLAUDE_MD
    if not f.exists():
        r.falha("claude-md", "Nao ha %s" % f, "python3 ferramentas/gerar_perfil.py")
        return
    t = f.read_text(encoding="utf-8-sig")
    if tem_bom(f):
        r.aviso("claude-md", "O CLAUDE.md tem BOM", "reescrever em UTF-8 sem BOM")
    if "<!-- kit:inicio -->" not in t:
        r.aviso("claude-md", "Sem marcadores do kit: uma nova geracao vai escrever por baixo",
                "python3 ferramentas/gerar_perfil.py")
    achados = [x for x in PROIBIDOS if x in t]
    if achados:
        r.falha("claude-md", "Ficaram marcadores por preencher: %s" % ", ".join(achados),
                "voltar a gerar o ficheiro depois de acabar a entrevista")
    if "—" in t:
        r.falha("claude-md", "O CLAUDE.md tem travessao, que e proibido",
                "tirar o travessao do modelo ou das respostas")
    if p:
        nome = (p.get("pessoa") or {}).get("nome") or ""
        oferta = (p.get("negocio") or {}).get("oferta") or ""
        if nome and nome not in t:
            r.falha("claude-md", "O ficheiro nao fala da pessoa (%s nao aparece)" % nome,
                    "python3 ferramentas/gerar_perfil.py")
        elif oferta and oferta[:25] not in t:
            r.aviso("claude-md", "O ficheiro nao menciona a oferta dela",
                    "python3 ferramentas/gerar_perfil.py")
    if not achados and "<!-- kit:inicio -->" in t:
        r.ok("claude-md", "CLAUDE.md personalizado, %d linhas, sem marcadores por preencher"
             % t.count("\n"))


def ver_frescura(r, p):
    if not p:
        return
    import hashlib
    h = hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    guardado = E.ler_estado().get("perfil_hash")
    if guardado and guardado != h:
        r.aviso("frescura", "O perfil mudou depois de o CLAUDE.md ter sido escrito",
                "python3 ferramentas/gerar_perfil.py")
    elif guardado:
        r.ok("frescura", "o CLAUDE.md corresponde ao perfil de agora")


def ver_pastas(r, p):
    if not p:
        return
    raiz = (p.get("maquina") or {}).get("pasta_trabalho") or ""
    if not raiz:
        r.aviso("pastas", "Sem pasta de trabalho definida no perfil",
                "criar a pasta do negocio dela e gravar em maquina.pasta_trabalho")
        return
    base = Path(os.path.expandvars(raiz)).expanduser()
    if not base.is_dir():
        r.falha("pastas", "A pasta de trabalho nao existe: %s" % base, "criar a pasta")
        return
    em_falta = [c.get("pasta") for c in (p.get("trabalho") or {}).get("clientes", [])
                if c.get("pasta") and not (base / c["pasta"]).is_dir()]
    if em_falta:
        r.aviso("pastas", "Clientes sem pasta: %s" % ", ".join(em_falta), "criar as pastas em falta")
    else:
        r.ok("pastas", "pasta de trabalho e pastas de clientes no sitio")


def ver_prova(r, p):
    script = RAIZ / "ferramentas" / "prova_visual.py"
    if not script.exists():
        script = E.KIT_DIR / "ferramentas" / "prova_visual.py"
    if not script.exists():
        r.aviso("prova", "Nao encontro o prova_visual.py", "reinstalar o kit")
        return
    destino = Path(os.environ.get("TMPDIR", "/tmp")) / "kit-prova-visual.png"
    try:
        res = subprocess.run([sys.executable, str(script), "--saida", str(destino)],
                             capture_output=True, text=True, timeout=120)
    except Exception as e:
        r.aviso("prova", "Nao consegui correr a prova visual: %s" % e)
        return
    if res.returncode == 2:
        r.aviso("prova", "Sem prova visual: falta o Pillow",
                "%s -m pip install --user Pillow" % (E.ler_estado().get("python_cmd") or "python3"))
        return
    if res.returncode != 0 or not destino.exists():
        r.falha("prova", "A prova visual falhou: %s" % (res.stderr.strip().splitlines()[-1:] or "?"),
                "ver o erro acima; costuma ser fontes em falta")
        return
    tamanho = destino.stat().st_size
    if tamanho < 20_000:
        r.falha("prova", "A imagem saiu vazia (%d bytes)" % tamanho, "verificar as fontes")
        return
    detalhe = ""
    if p:
        try:
            from PIL import Image
            img = Image.open(destino).convert("RGB")
            alvo = (p.get("marca") or {}).get("cor_acento", "").strip().lstrip("#")
            if len(alvo) == 6:
                rgb = tuple(int(alvo[i:i + 2], 16) for i in (0, 2, 4))
                total = img.width * img.height
                conta = sum(n for n, c in img.getcolors(500_000) or []
                            if sum(abs(a - b) for a, b in zip(c, rgb)) < 30)
                if conta / total < 0.002:
                    r.aviso("prova", "A cor de acento dela quase nao aparece na imagem",
                            "confirmar marca.cor_acento no perfil")
                    return
                detalhe = ", com a cor da marca dela"
        except Exception:
            pass
    r.ok("prova", "prova visual gerada (%d KB%s): %s" % (tamanho // 1024, detalhe, destino))
    print("   >>> ABRE ESTA IMAGEM E OLHA PARA ELA antes de dizer que esta feito: %s" % destino)


# ------------------------------------------------------------ saida

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nivel", choices=("instalacao", "completo"), default="completo")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = Relatorio()
    ver_skills(r)
    ver_settings(r)
    ver_assets(r)
    ver_cofre(r)
    ver_processo(r)
    ver_assinatura(r)

    if a.nivel == "completo":
        p = ver_perfil(r)
        ver_claude_md(r, p)
        ver_frescura(r, p)
        ver_pastas(r, p)
        ver_prova(r, p)

    codigo = r.codigo()

    if a.json:
        print(json.dumps({"codigo": codigo, "nivel": a.nivel, "linhas": r.linhas},
                         ensure_ascii=False, indent=2))
        return codigo

    simbolo = {OK: "[ok]   ", FALHA: "[FALHA]", AVISO: "[aviso]"}
    print("PowerScale Skills Kit, verificacao (%s)" % a.nivel)
    print("=" * 52)
    for l in r.linhas:
        print("%s %s" % (simbolo[l["estado"]], l["mensagem"]))
        if l["estado"] != OK and l["resolver"]:
            print("         -> %s" % l["resolver"])
    print("=" * 52)
    if codigo == 0:
        print("PRONTO." if a.nivel == "completo" else "Instalacao boa. Falta personalizar.")
    elif codigo == 2:
        print("Funciona, mas ha avisos acima. Nenhum trava o trabalho.")
    else:
        n = sum(1 for l in r.linhas if l["estado"] == FALHA)
        print("%d coisa(s) por resolver. Ver as linhas [FALHA]." % n)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
