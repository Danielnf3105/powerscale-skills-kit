---
name: criativos-anuncios
description: Gera lotes de anúncios tipográficos 9:16 (story e reel), fundo branco, texto bold all-caps em Big Shoulders Black com ligeira inclinação itálica, palavras-chave destacadas na cor de acento da marca, e o logótipo em baixo à direita. É o estilo "estou à procura de X" da resposta direta, sem imagem nenhuma, o mais barato de produzir e dos que mais parem o scroll. Usar quando pedes "anúncios tipográficos", "ads só de texto", "preciso de variações para [novo nicho]", "criativos rápidos para testar um ângulo".
---

# Criativos tipográficos 9:16 (estilo "7 [NICHO]")

## O que esta skill faz

Produz lotes de anúncios verticais (9:16, 1080×1920) puramente tipográficos:
- Fundo branco (ou o inverso: fundo escuro e texto branco, se for a marca)
- Texto bold all-caps **Big Shoulders 60pt Black** com shear sintético ~5.7° (italic ligeiro)
- Hierarquia de cor: preto para texto neutro, **a cor de acento da marca** para os destaques (nicho, número, qualificador, mecanismo, reversão de risco). A cor vem sozinha da tua marca (`marca.cor_acento` do teu perfil). Enquanto nao a definires, sai o laranja do kit.
- "QUALQUER RISCO" sempre sublinhado a laranja
- Logótipo de quem assina, em baixo à direita, tirado de `assets/logos/`
- Alinhamento centrado horizontal + vertical

Output: PNGs na pasta `out/` (ou onde apontares com a variável `PS_OUT`).

## Quando usar

- "Preciso de ads tipográficos" / "ads só de texto"
- "Variar o ad 7 [nicho] para [novo segmento]" (ex: dentistas, advogados, donos de e-commerce)
- "Criar variante com nova promessa central" (ex: trocar "INSTALAR" por "DOBRAR FATURAÇÃO")
- "Adaptar para outra língua" (manter estrutura, traduzir lines)

Não usar para:
- Ads com imagem ou fotografia de fundo (esses são outro lote)
- Copy longa narrativa (são lotes separados)
- Geração de guidelines de marca

## Antes de correr o script (obrigatorio)

O lote que vem de fabrica no `build_typography_ads.py` e **um exemplo**, com a
copy de outra pessoa ("7 [NICHO] COACHES"). Nunca se entrega esse lote a um
cliente: escreve-se a copy dele na lista `ADS` antes de gerar.

A ordem certa:

1. Voice Bible de quem assina o anuncio (skill `voz-de-marca`). A copy sai de la.
2. Trocar as linhas em `ADS` pela copy dele, mantendo a estrutura de hierarquia
   (neutro em preto, destaque na cor de acento).
3. Correr o script e **olhar para uma imagem** antes de mostrar seja o que for.

O logotipo e opcional: sem ficheiro em `assets/logos/`, o anuncio sai na mesma,
so sem assinatura visual.

## Fonte (obrigatório)

**Big Shoulders 60pt Black**, Google Fonts, licença OFL.

Está no kit: `assets/fontes/BigShoulders_60pt-Black.ttf`. Licença OFL, uso comercial livre.

Características que fazem este match (vs Lato, DejaVu, Liberation):
- "A" topo plano (não pontiagudo), geométrica vs humanista
- "R" perna direita reta, não curva
- Peso Black + proporções condensed (altura > largura)
- Família otimizada por tamanho ótico, usar `60pt` para display headlines (1080×1920)

**Italic:** Big Shoulders não tem italic oficial. Aplicar shear sintético `0.10` (~5.7°) via `Image.AFFINE`. O ad de referência tem inclinação similar.

Variantes alternativas (também no kit):
- `BigShoulders_36pt-Black.ttf`: letras ligeiramente menos extreme display, melhor para subheadlines
- `BigShoulders_18pt-Black.ttf`: proporções "text" (legível em corpo pequeno)

## Estrutura do copy

Esqueleto de resposta direta (modelo do ad de referência):

```
ESTOU À              <- 1: setup
PROCURA DE           <- 2: setup
7 [NICHO]            <- 3: número + nicho (RED)
[COMPLEMENTO]        <- 4: continuação nicho (RED)
A FATURAR            <- 5: qualifier (BLACK)
ENTRE [VALOR]        <- 6: range (parte RED)
QUE QUEREM           <- 7: action (BLACK)
INSTALAR             <- 8: verb
A NOSSA              <- 9
"MÁQUINA DE          <- 10: mechanism (RED)
AQUISIÇÃO"           <- 11: mechanism (RED)
SEM QUALQUER         <- 12: SEM black + QUALQUER red+underlined
RISCO                <- 13: red+underlined
```

13 linhas é o sweet spot, fonte fica ~115px e ad sai limpo. 14+ linhas força fonte para baixo (~100px ainda OK).

**Variante "DOBRAR" (v2):** substituir linhas 7-8 por:
```
QUE QUEREM DOBRAR    <- 7: "QUEREM" black + "DOBRAR" red
A SUA FATURAÇÃO      <- 8: RED, promessa central
INSTALANDO           <- 9: muda verb (não "INSTALAR")
A NOSSA              <- 10
```

Total: 14 linhas. Fonte cai para ~107px. Promessa concreta atrai mais cliques mas atrai leads menos qualificados, usar como B-test contra v1.

## Voz e copy

Ler sempre a voz de quem assina (`voz-de-marca` → `clientes/<cliente>/voz.md`)
antes de escrever uma linha. Regras que valem quase sempre:
- pt-PT, tratamento de acordo com a marca (tu ou você, nunca os dois)
- Inglês permitido em terms já consagrados na indústria do cliente: `MRR`, `Skool owners`, `DM`, `closer`, `funnel`
- Mecanismo sempre entre aspas: `"MÁQUINA DE AQUISIÇÃO"`
- Range de faturação deve auto-qualificar o lead (não pôr ranges abaixo do ICP real)
- "SEM QUALQUER RISCO" obriga performance-based / refund / trial real, confirmar antes

## Workflow

### 1. Clarificar
Antes de gerar, perguntar com `AskUserQuestion`:
- Nicho(s) alvo (ex: Business coaches, Health coaches, Dentistas, etc)
- Faixa de faturação (5-15K? 10-30K? MRR vs /mês?)
- Variante: v1 (INSTALAR) só, ou também v2 (DOBRAR)?

### 2. Editar `build_typography_ads.py`
Acrescentar entradas em `ADS = [...]` com a função `lines_coach_v1()` ou `lines_skool_v1()` (ou v2). Exemplo:

```python
(lines_coach_v1("DENTISTAS"), "ad-dentistas-01-v1.png"),
(lines_coach_v2("DENTISTAS"), "ad-dentistas-01-v2-dobrar.png"),
```

### 3. Render
```bash
python3 build_typography_ads.py
```
Outputs na pasta `out/`.

### 4. Entregar
Abrir uma amostra e olhar mesmo para ela antes de entregar. Depois mostrar o lote todo (folha de contacto ou envio dos ficheiros).

## Especificações técnicas

| Elemento | Spec |
|---|---|
| Canvas | 1080×1920 (9:16) |
| Padding lateral | 70px |
| Padding topo | 110px |
| Logo bottom-right | 150×150 max, padding 60px direito + 60px baixo |
| Fonte | `BigShoulders_60pt-Black.ttf`, auto-size para caber largura |
| Shear italic | `0.10` (matriz AFFINE) |
| Line height | `(asc + desc) * 0.95` (tight) |
| Cor preto | `#000000` |
| Cor accent | constante `ACCENT` no script, a cor da marca |
| Fundo | `#FFFFFF` |
| Underline | thickness = `font_size // 14`, distância = `asc + 6px` |

## Notas de quem já bateu nisto

- A fonte foi a decisão que demorou mais. Liberation Sans Narrow Bold com
  contorno sai agressiva demais, DejaVu Condensed BoldOblique tem itálico a
  mais, Lato Black Italic é humanista demais. **Big Shoulders 60pt Black com
  shear 0.10** é o que bate certo com o estilo de referência: letras
  geométricas, "A" de topo plano, "R" de perna reta.
- A promessa concreta ("dobrar a faturação") atrai mais cliques e leads menos
  qualificados. Usa-a como teste B contra a versão mais seca, não como padrão.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
