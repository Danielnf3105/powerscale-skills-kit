#!/usr/bin/env bash
# PowerScale Skills Kit, instalador (Mac e Linux).
#   ./instalar.sh              instala
#   ./instalar.sh --verificar  so diz o que falta na maquina
#
# Este script e de proposito burro: verifica binarios, copia ficheiros e chama
# o Python. Tudo o que envolve acentos, JSON ou templates vive em Python, para
# nao haver duas implementacoes a divergir entre o Mac e o Windows.
set -euo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE="$HOME/.claude"
SKILLS="$CLAUDE/skills"
ASSETS="$CLAUDE/kit-assets"
KITDIR="$CLAUDE/kit"
COFRE="$HOME/.config/chaves"
STAMP="$(date +%Y-%m-%d-%H%M)"

ok()    { printf '  ok     %s\n' "$1"; }
falta() { printf '  falta  %s\n' "$1"; }
erro()  { printf '  ERRO   %s\n' "$1"; }

echo
echo "PowerScale Skills Kit"
echo "====================="
echo

# ------------------------------------------------------------ 1. a maquina
EM_FALTA=()
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info[0]==3 else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done

echo "A maquina:"
[ -n "$PY" ] && ok "Python 3 ($PY, $($PY -V 2>&1))" || { falta "Python 3  ->  brew install python"; EM_FALTA+=(python); }
for f in claude node git ffmpeg; do
  if command -v "$f" >/dev/null 2>&1; then ok "$f"; else falta "$f"; EM_FALTA+=("$f"); fi
done
echo

if [ "${1:-}" = "--verificar" ]; then
  echo "Modo verificacao. Nada foi instalado."
  [ ${#EM_FALTA[@]} -gt 0 ] && echo "Em falta: ${EM_FALTA[*]}"
  exit 0
fi

if [ -z "$PY" ]; then
  erro "Sem Python 3 nao da para continuar: e ele que escreve o teu CLAUDE.md."
  echo "         Instala com: brew install python"
  exit 1
fi
if ! command -v claude >/dev/null 2>&1 && [ ! -d "$CLAUDE" ]; then
  erro "Nao encontro o Claude Code nesta maquina."
  exit 1
fi

# ------------------------------------------------------------ 2. pastas
mkdir -p "$SKILLS" "$ASSETS" "$KITDIR" "$COFRE"
chmod 700 "$COFRE"

# ------------------------------------------------------------ 3. skills
# Skills que ELA alterou sao guardadas antes de escrever por cima. Sem isto,
# atualizar o kit apaga-lhe trabalho, e ela nunca mais atualiza.
GUARDADAS="$KITDIR/skills-alteradas"
alteradas=0
for d in "$KIT"/skills/*/; do
  nome="$(basename "$d")"
  destino="$SKILLS/$nome"
  if [ -d "$destino" ]; then
    if ! diff -rq "$d" "$destino" >/dev/null 2>&1; then
      mkdir -p "$GUARDADAS/$STAMP"
      cp -R "$destino" "$GUARDADAS/$STAMP/$nome" 2>/dev/null || true
      alteradas=$((alteradas+1))
    fi
    rm -rf "$destino"
  fi
  cp -R "${d%/}" "$SKILLS/"
done
[ "$alteradas" -gt 0 ] && ok "$alteradas skill(s) que tinhas mexido: copia em $GUARDADAS/$STAMP"

esperado=$(find "$KIT/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')
instaladas=0
for d in "$KIT"/skills/*/; do
  [ -f "$SKILLS/$(basename "$d")/SKILL.md" ] && instaladas=$((instaladas+1))
done
if [ "$instaladas" != "$esperado" ]; then
  erro "instalei $instaladas skills mas o kit tem $esperado. Nao continues sem perceber porque."
  exit 1
fi
ok "$instaladas skills em $SKILLS"

# ------------------------------------------------------------ 4. assets
cp -R "$KIT"/assets/* "$ASSETS"/ && ok "fontes e logotipos em $ASSETS"

# ------------------------------------------------------------ 5. o processo
# Vai para ~/.claude/kit para o arranque sobreviver a mudares esta pasta de
# sitio, ou a apaga-la depois de instalar.
for p in processo modelo ferramentas; do
  rm -rf "${KITDIR:?}/$p"
  cp -R "$KIT/$p" "$KITDIR/$p"
done
cp "$KIT/PROCESSO.md" "$KITDIR/" 2>/dev/null || true
cp "$KIT/manifesto.json" "$KITDIR/" 2>/dev/null || true
cp "$KIT/VERSAO" "$KITDIR/" 2>/dev/null || true
ok "processo e ferramentas em $KITDIR"

# ------------------------------------------------------------ 6. permissoes
if [ -f "$CLAUDE/settings.json" ]; then
  if ! diff -q "$KIT/settings.json" "$CLAUDE/settings.json" >/dev/null 2>&1; then
    cp "$CLAUDE/settings.json" "$CLAUDE/settings.json.backup-$STAMP"
    falta "ja tinhas um settings.json (copia em settings.json.backup-$STAMP)"
    echo "         O Claude junta os dois na fase de instalacao. Nao fica nada por fundir."
  else
    ok "permissoes ja estavam certas"
  fi
else
  cp "$KIT/settings.json" "$CLAUDE/settings.json"
  ok "permissoes instaladas"
fi

# ------------------------------------------------------------ 7. cofre
if [ ! -f "$COFRE/secrets.env" ]; then
  echo "# Uma chave por linha, NOME=valor. Nunca colar chaves no chat." > "$COFRE/secrets.env"
  chmod 600 "$COFRE/secrets.env"
  ok "cofre de chaves criado em $COFRE/secrets.env"
else
  chmod 600 "$COFRE/secrets.env" 2>/dev/null || true
  ok "cofre de chaves ja existia"
fi

# ------------------------------------------------------------ 8. estado
"$PY" "$KIT/ferramentas/estado.py" --definir python_cmd="$PY"      >/dev/null
"$PY" "$KIT/ferramentas/estado.py" --definir kit_caminho="$KIT"    >/dev/null
"$PY" "$KIT/ferramentas/estado.py" --definir kit_versao="$(cat "$KIT/VERSAO" 2>/dev/null || echo '?')" >/dev/null
if [ -d "$KIT/.git" ]; then ORIGEM=git; else ORIGEM=zip; fi
"$PY" "$KIT/ferramentas/estado.py" --definir origem="$ORIGEM"      >/dev/null
"$PY" "$KIT/ferramentas/estado.py" --marcar instalar=feita         >/dev/null
ok "estado da instalacao gravado"

echo
echo "Instalado. O Claude continua daqui: fase seguinte em PROCESSO.md."
echo "PowerScale Skills Kit  ·  powerscale.pro"
echo
