#!/usr/bin/env python3
"""Deteta sinais de escrita de IA em texto português de Portugal.

Só lê e reporta. Nunca escreve, nunca substitui: transformações cegas sobre texto
português partem acentos e cedilhas (regra do CLAUDE.md).

Uso:
    python3 deteta.py ficheiro.html
    python3 deteta.py pasta/ --ext md,html
    python3 deteta.py ficheiro.md --so pontuacao,estrutura
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXTENSOES = {".md", ".html", ".htm", ".txt", ".mdx"}

# (categoria, etiqueta, regex[, "cs" para distinguir maiúsculas])
PADROES: list[tuple] = [
    # ---------- pontuação e formatação ----------
    ("pontuacao", "travessão (em dash)", r"—"),
    ("pontuacao", "meia-risca (en dash)", r"–"),
    ("pontuacao", "aspas curvas", r"[“”‘’]"),
    ("pontuacao", "hífen duplo usado como travessão", r"\s--\s"),
    ("pontuacao", "emoji", r"[\U0001F300-\U0001FAFF✅❌❤⭐⚡✨]"),
    ("formatacao", "bullet com cabeçalho a negrito", r"^\s*[-*]\s*\*\*[^*\n]{2,40}\*\*\s*:|^\s*[-*]\s*\*\*[^*\n]{2,40}:\*\*"),
    ("formatacao", "título em Title Case", r"^#{1,6} .*\b(O|A|Os|As|Um|Uma|Teu|Tua|Teus|Tuas|Meu|Minha|Que|De|Do|Da|Dos|Das|No|Na|Nos|Nas|Para|Com|Sem|Em|E|Ou|Se|Ao|Aos|À|Às|Pelo|Pela)\b.*\b(O|A|Os|As|Um|Uma|Teu|Tua|Teus|Tuas|Meu|Minha|Que|De|Do|Da|Dos|Das|No|Na|Nos|Nas|Para|Com|Sem|Em|E|Ou|Se|Ao|Aos|À|Às|Pelo|Pela)\b", "cs"),

    # ---------- vocabulário inflacionado ----------
    ("vocabulario", "adjetivo de importância", r"\b(crucial|crucia(is)?|pivotal|vital|imprescindível|inquestionável)\b"),
    ("vocabulario", "adjetivo de brochura", r"\b(robust[oa]s?|poderos[oa]s?|inovador(a|es|as)?|revolucionári[oa]s?|transformador(a|es|as)?|disruptiv[oa]s?|vibrante|dinâmic[oa]s?|cativante|envolvente|impactante)\b"),
    ("vocabulario", "verbo de consultora", r"\b(alavanca|alavancar|potenciar|impulsionar|desbloquear|maximizar|catalisar|revolucionar)\w*\b"),
    ("vocabulario", "substantivo abstrato de IA", r"\b(panorama|paisagem|ecossistema|tapeçaria|espinha dorsal|jornada do cliente)\b"),
    ("vocabulario", "anúncio em vez de facto", r"\b(mergulha(r|mos)?|aprofunda(r|mos)?|explora(r|mos)? em detalhe|vamos desvendar)\b"),
    ("vocabulario", "moldura temporal vazia", r"\b(em constante evolução|nos dias de hoje|no mundo atual|na era digital|cada vez mais competitiv[oa])\b"),
    ("vocabulario", "elogio de si própria", r"\b(um testemunho d[eo]|um marco|no cerne d[eo]|desempenha um papel)\b"),

    # ---------- muletas ----------
    ("muleta", "frase-muleta", r"\b(é importante (notar|salientar|referir|realçar|destacar)|vale a pena (notar|destacar|referir)|convém (notar|referir))\b"),
    ("muleta", "fecho de redação", r"\b(em suma|em conclusão|em jeito de conclusão|por fim mas não menos importante|resumindo,)\b"),
    ("muleta", "advérbio colado", r"\bde forma (eficaz|eficiente|estratégica|consistente|simples e rápida|automática)\b"),
    ("muleta", "hipérbole de facilidade", r"\b(sem esforço|num piscar de olhos|num ápice|de forma totalmente automática)\b"),

    # ---------- estrutura ----------
    ("estrutura", "gerúndio de remate", r",\s*(garantindo|assegurando|permitindo|proporcionando|oferecendo|contribuindo|refletindo|destacando|sublinhando|evidenciando|criando|gerando|aumentando|melhorando|reforçando|impulsionando|potenciando)\b"),
    ("estrutura", "paralelismo negativo", r"\bnão (é|são|se trata|basta|chega)\b[^.!?\n]{0,80},\s*(é|são|trata-se)\b"),
    ("estrutura", "paralelismo negativo (não só)", r"\bnão (só|apenas)\b[^.!?\n]{0,80}\b(mas também|mas sim)\b"),
    ("estrutura", "paralelismo negativo (mais do que)", r"\bmais do que\b[^.!?\n]{0,60},\s*(é|são)\b"),
    ("estrutura", "negação em cauda", r"[,.]\s*(sem (adivinhar|esforço|fricção|ruído|rodeios|desculpas|surpresas)|zero (fricção|ruído|desculpas))\b"),
    ("estrutura", "abertura de intimidade falsa", r"\b(a verdade é que|a realidade é (esta|que)|sejamos (honestos|claros)|vamos ser honestos|vou ser direto|aqui está o que|vamos por partes|imagina isto|e se te dissesse)\b"),
    ("estrutura", "conclusão animadora", r"\b(o futuro (é|parece) (promissor|risonho|brilhante)|a escolha é tua|agora é contigo|o próximo passo é teu|resta(-te)? apenas)\b"),
    ("estrutura", "aforismo de formulário", r"\b(é a (moeda|linguagem|arquitetura|espinha) d[eoa])\b"),

    # ---------- português do Brasil ----------
    ("ptbr", "tratamento por você", r"\bvocês?\b"),
    ("ptbr", "léxico PT-BR", r"\b(tela|celular|usuári[oa]s?|gerenciamento|planejamento|equipes?|acessar|arquivos? (digital|do sistema))\b"),
    ("ptbr", "gerúndio contínuo", r"\b(est(ou|á|ão|amos|ava|avam))\s+\w{3,}ndo\b"),
]

CATEGORIAS = ["pontuacao", "formatacao", "vocabulario", "muleta", "estrutura", "ptbr"]

RE_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
RE_TAG = re.compile(r"<[^>]{1,400}>", re.S)


def limpa_html(texto: str) -> str:
    """Apaga script/style e tags, preservando o número de linhas."""
    def branco(m: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    texto = RE_SCRIPT.sub(branco, texto)
    return RE_TAG.sub(branco, texto)


MARCADOR_IGNORAR = "humanizer-pt: ignorar"


def linhas_de_codigo(linhas: list[str]) -> set[int]:
    """Números de linha dentro de blocos ``` (o código não é prosa)."""
    dentro = False
    marcadas: set[int] = set()
    for n, linha in enumerate(linhas, 1):
        if linha.lstrip().startswith("```"):
            dentro = not dentro
            marcadas.add(n)
            continue
        if dentro:
            marcadas.add(n)
    return marcadas


def analisa(caminho: Path, categorias: set[str]) -> list[tuple[str, str, int, str]]:
    bruto = caminho.read_text(encoding="utf-8", errors="replace")
    if MARCADOR_IGNORAR in bruto[:2000]:
        return []
    texto = limpa_html(bruto) if caminho.suffix.lower() in {".html", ".htm"} else bruto
    linhas = texto.splitlines()
    saltar = linhas_de_codigo(linhas)

    achados: list[tuple[str, str, int, str]] = []
    for padrao_def in PADROES:
        categoria, etiqueta, padrao = padrao_def[0], padrao_def[1], padrao_def[2]
        maiusculas_contam = len(padrao_def) > 3 and padrao_def[3] == "cs"
        if categoria not in categorias:
            continue
        rx = re.compile(padrao, re.M if maiusculas_contam else re.I | re.M)
        for n, linha in enumerate(linhas, 1):
            if n in saltar:
                continue
            for m in rx.finditer(linha):
                inicio = max(0, m.start() - 40)
                trecho = linha[inicio:m.end() + 40].strip()
                achados.append((categoria, etiqueta, n, trecho))
    achados.sort(key=lambda a: (a[2], a[0]))
    return achados


def main() -> int:
    ap = argparse.ArgumentParser(description="Deteta sinais de escrita de IA em PT-PT.")
    ap.add_argument("alvo", help="ficheiro ou pasta")
    ap.add_argument("--ext", default="", help="extensões a incluir numa pasta, ex: md,html")
    ap.add_argument("--so", default="", help=f"categorias: {','.join(CATEGORIAS)}")
    args = ap.parse_args()

    categorias = set(c.strip() for c in args.so.split(",") if c.strip()) or set(CATEGORIAS)
    desconhecidas = categorias - set(CATEGORIAS)
    if desconhecidas:
        print(f"categoria desconhecida: {', '.join(sorted(desconhecidas))}", file=sys.stderr)
        return 2

    alvo = Path(args.alvo).expanduser()
    if not alvo.exists():
        print(f"não existe: {alvo}", file=sys.stderr)
        return 2

    extensoes = {f".{e.strip().lstrip('.')}" for e in args.ext.split(",") if e.strip()} or EXTENSOES
    ficheiros = [alvo] if alvo.is_file() else sorted(
        p for p in alvo.rglob("*") if p.is_file() and p.suffix.lower() in extensoes
    )

    total = 0
    for ficheiro in ficheiros:
        achados = analisa(ficheiro, categorias)
        if not achados:
            continue
        total += len(achados)
        print(f"\n{ficheiro}")
        for categoria, etiqueta, n, trecho in achados:
            print(f"  {categoria:11} L{n:<5} {etiqueta:32} {trecho[:110]}")

    print(f"\n{total} sinais em {len(ficheiros)} ficheiro(s).")
    if total:
        print("Um sinal isolado costuma ser prosa legítima. Cluster de sinais é confissão.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
