#!/usr/bin/env bash
# PowerScale Skills Kit: publicar o kit e preparar a entrega. Lado do Daniel.
#
#   ./ferramentas/entregar.sh "Maria"
#
# Publica (ou atualiza) o repositorio publico, marca a versao, e deixa no
# Desktop a mensagem pronta a enviar.
set -euo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NOME="${1:-}"
REPO="powerscale-skills-kit"
cd "$KIT"

echo
echo "PowerScale Skills Kit, entrega"
echo "=============================="
echo

command -v gh >/dev/null 2>&1 || { echo "Falta o gh. brew install gh && gh auth login"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "O gh nao esta autenticado. Corre: gh auth login"; exit 1; }
DONO="$(gh api user --jq .login)"
echo "Conta GitHub: $DONO"

[ -d .git ] || { echo "Isto nao e um repositorio git. Corre: git init"; exit 1; }

# Nada se publica com trabalho por commitar: o que ficasse de fora nunca chegava
# a quem instala, e a falha so aparecia do lado dela.
if [ -n "$(git status --porcelain)" ]; then
  echo
  echo "Ha coisas por commitar. Resolve isso primeiro:"
  git status --short
  exit 1
fi

echo "A verificar o kit antes de publicar..."
python3 ferramentas/manifesto.py     || { echo "O manifesto nao bate certo com as skills."; exit 1; }
python3 ferramentas/marcar.py --ver  || { echo "Ha ficheiros sem a assinatura da marca."; exit 1; }

VERSAO="$(cat VERSAO)"
echo "Versao: $VERSAO"
echo

if gh repo view "$DONO/$REPO" >/dev/null 2>&1; then
  echo "O repositorio ja existe. A enviar o que mudou..."
  git push origin HEAD 2>/dev/null || git push -u origin "$(git branch --show-current)"
else
  echo "A criar o repositorio publico..."
  gh repo create "$REPO" --public --source=. --remote=origin --push \
    --description "Skills, metodo e travoes para o Claude trabalhar como uma equipa a serio. Feito pela PowerScale."
fi

git tag -f "v$VERSAO" >/dev/null 2>&1 || true
git push -f origin "v$VERSAO" >/dev/null 2>&1 || true

URL="https://github.com/$DONO/$REPO"
ZIP="$URL/archive/refs/heads/main.zip"

DESTINO="$HOME/Desktop/MENSAGEM-PARA-${NOME:-PARCEIRO}.txt"
cat > "$DESTINO" <<MSG
Preparei-te o kit do Claude que uso cá. Instala-se sozinho e não precisas de
perceber nada de terminal.

1. Descarrega e descompacta:
   $ZIP

2. Abre o Claude Code dentro da pasta que saiu de lá.

3. Diz-lhe olá.

Ele trata do resto: verifica a tua máquina, instala o que falta, faz-te umas
perguntas sobre o teu negócio e no fim já fazem uma coisa a sério juntos. Uns 20
minutos.

Se ficares a meio, fecha e volta a abrir na mesma pasta: ele sabe onde ficaram.

(Se usares git, dá também: git clone $URL)
MSG

echo
echo "Publicado: $URL"
echo "Mensagem pronta: $DESTINO"
echo
echo "Falta-te so enviar-lha."
