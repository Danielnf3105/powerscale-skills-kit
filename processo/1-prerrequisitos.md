# Fase 1: pré-requisitos

**Objetivo:** a máquina ter o que o kit precisa.

**Pré-condição:** fase 0 feita.

## Passos

1. Corre a verificação, que não instala nada:

   ```
   Windows:  powershell -ExecutionPolicy Bypass -File .\instalar.ps1 -Verificar
   Mac:      ./instalar.sh --verificar
   ```

2. Explica-lhe, em português, o que falta e para que serve. Não leias a lista
   toda: diz só o que falta.

   | Ferramenta | Precisa? | Para quê |
   |---|---|---|
   | Claude Code | obrigatório | é o programa que estás a correr |
   | Python 3 | obrigatório | escreve o teu ficheiro de instruções e gera as imagens |
   | Node.js | quase sempre | várias ferramentas de linha de comandos |
   | Git | ajuda | receber atualizações do kit |
   | ffmpeg | só se analisares calls | extrair o áudio das gravações |

3. **Pergunta antes de instalar**, e depois instala tu:

   ```
   Windows:  winget install Python.Python.3.12
   Mac:      brew install python
   ```

4. **Cuidado com o Python no Windows.** O `python.exe` que aparece por defeito
   pode ser o atalho da Microsoft Store: existe, responde, abre a loja e não é
   um interpretador. O instalador já testa a sério (corre e lê a versão), por
   isso confia no que ele diz, não no que o PATH sugere.

5. Marca a fase:

   ```
   <python> ferramentas/estado.py --marcar prerrequisitos=feita --nota "faltava o ffmpeg, ficou de fora"
   ```

**Está feita quando:** o Python 3 responde com a versão, e o que faltava ou foi
instalado ou ficou registado como dispensável para o trabalho dela.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
