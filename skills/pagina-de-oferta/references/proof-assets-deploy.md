# Prova, assets, verificação e deploy

Lições operacionais do build da <cliente>. Seguir à risca evita repetir erros.

## ⚠️ Rede do Bash está em SANDBOX

- Downloads e deploy (curl, vercel) **falham em silêncio** no Bash normal (DNS não resolve).
- Usar `dangerouslyDisableSandbox: true` nessas chamadas.
- Com o sandbox desligado o **PATH fica mínimo** (sem `mkdir`/`awk`/`cut`/`file`): nessas
  chamadas usa **só `curl`/`vercel`** e **caminhos absolutos**. Cria pastas e inspeciona
  ficheiros numa chamada Bash NORMAL (sandboxed) à parte.
- Binários: node em `/usr/local/bin/node`, vercel em `~/.npm-global/bin/vercel`. Exportar
  `PATH="/usr/local/bin:$HOME/.npm-global/bin:$PATH"` antes do `vercel`.

## Extrair prova de um deck/PDF

- **Usar as SLIDES renderizadas, não os prints crus.** As tarjas pretas de censura
  estão nas slides (formas por cima), não nas imagens embebidas. Extrair a imagem crua
  expõe nomes/emails que o deck escondeu.
- Render: `pdftoppm -png -f P -l P -scale-to 1300 "ficheiro.pdf" out` → `out-PP.png` por
  página. Converter para JPEG com `sips -s format jpeg -s formatOptions 80 in.png --out out.jpg`
  (~100KB cada).
- **Ler as páginas do PDF** (Read com `pages`) para mapear página → empresa (caption correta) e **procurar fugas** (ver checklist de honestidade no SKILL.md).
- Galeria em grelha + **lightbox** (clique/setas/Esc) referenciando `assets/prints/<empresa>.jpg`.
- Stats agregados (count-up): só números honestos do deck (reuniões geradas, taxa de
  abertura, emails, países). Script de count-up próprio com `toLocaleString('pt-PT')`.

## Logos das marcas

- **Clearbit (`logo.clearbit.com`) foi descontinuado** (não resolve). Alternativas:
  - Google: `https://www.google.com/s2/favicons?domain=DOMINIO&sz=256`
  - DuckDuckGo: `https://icons.duckduckgo.com/ip3/DOMINIO.ico`
  - apple-touch-icon: `https://DOMINIO/apple-touch-icon.png` (~180px, melhor qualidade)
- **Verificar SEMPRE os logos** antes de usar (folha de teste curta + screenshot, página
  curta evita o bug do screenshot). Armadilhas reais: **sites em WordPress devolvem o
  logo do WordPress**; domínios desconhecidos devolvem **globo genérico**; favicons de 16-32px ficam tremidos.
- Usar como imagem **só os confirmados**; os restantes ficam **texto** (cartão com o nome).
  Em P&B: cartões brancos + `filter:grayscale(1)`.

## Deploy (Vercel)

- Pasta de raiz **sem espaços** `<parceiro>-online/` com `index.html` (= cópia do canónico
  sem-preço) + `assets/` + (opcional) `vercel.json`.
- `cd "<parceiro>-online" && export PATH="/usr/local/bin:$HOME/.npm-global/bin:$PATH" && vercel --prod --scope <o-teu-scope-vercel> --yes` (com `dangerouslyDisableSandbox:true`).
- Confirmar live: `curl -s -o /dev/null -w "%{http_code}" URL/` = 200 e um asset = 200 (também sandbox off).
- Sincronizar: a pasta de deploy e o ficheiro de trabalho devem ficar iguais (cópia + `assets/`).
- ⚠️ Estratégia: a versão **online é a sem preço**; a com preço fica para as reuniões de fecho (ou deploy à parte).

## Verificação no preview

- Servidor: `.claude/launch.json` com `npx serve -l PORTA "pasta"` + `preview_start`.
- **O servidor de preview morre com frequência** entre navegações; se vier `body` quase
  vazio ou "Server not found", **reiniciar** (`preview_start`) e repetir.
- O **viewport do preview é instável** (altura 0 por vezes) → IntersectionObserver pode não
  disparar (count-up/reveals). A lógica está bem; verificar por DOM, não só por ecrã.
- **Bug do screenshot em páginas longas**: pinta preto abaixo da 1.ª dobra. Confirmar as
  secções de baixo por **inspeção do DOM** (contar elementos, ler textContent, getBBox dos
  SVG, disparar `input` nas calculadoras e ler os outputs). Para mostrar uma secção de
  baixo num screenshot, fazer uma folha curta isolada.
- Checklist final por ficheiro: `grep -c $', '` = 0; sem IDs duplicados; matemática das
  calculadoras certa; consola sem erros; ordem das secções correta.

## Documentação (sempre)

- a página de referência que já construíste: oferta, método, decisões tomadas, **pendentes**, avisos de honestidade/RGPD.
- Atualizar `CLAUDE.md` (entrada datada em "Estado / decisões importantes") + ficheiro de memória `project_<parceiro>.md` + ponteiro em `MEMORY.md`.
