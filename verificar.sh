#!/usr/bin/env bash
# PowerScale Skills Kit: esta bem instalado?
#   ./verificar.sh              verificacao completa
#   ./verificar.sh instalacao   so a parte tecnica, sem exigir perfil
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NIVEL="${1:-completo}"
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys;sys.exit(0 if sys.version_info[0]==3 else 1)' 2>/dev/null; then
    exec "$c" "$KIT/ferramentas/verificar.py" --nivel "$NIVEL"
  fi
done
echo "Sem Python 3 nesta maquina. Instala com: brew install python"
exit 1
