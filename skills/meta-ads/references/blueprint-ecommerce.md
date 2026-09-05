# Blueprint de conta E-COMMERCE (validado na <cliente>, 2026-07-22)

Arquitetura completa que sobreviveu a uma ronda inteira de correções do cliente ao vivo. Replicar para qualquer cliente e-commerce, adaptando geo, coleções e interesses ao histórico da conta dele.

## Arquitetura: 4 campanhas

| Campanha | Objetivo | Budget | Papel |
|---|---|---|---|
| `[<TAG>] BEST-SELLERS \| PROSPECTING` | OUTCOME_SALES, ABO | ~30€/dia | motor principal, coleção core |
| `[<TAG>] NEW-IN \| PROSPECTING` | OUTCOME_SALES, ABO | ~20€/dia | coleção nova do ciclo |
| `[<TAG>] CATÁLOGOS` | OUTCOME_SALES, ABO | ~40€/dia | 2 conjuntos: ABERTO (ADV+ audience + product set dos best sellers em stock) e REMARKETING (DPA: site 180d + ATC + IC, exclui compradores 180d) |
| `[<TAG>] BRANDING` | OUTCOME_ENGAGEMENT, ABO | ~5€/dia | vídeos de marca, THRUPLAY + ON_VIDEO |

`<TAG>` = nomenclatura do ciclo (na <cliente>: `DDUA26`, herdada das campanhas históricas que funcionaram). Uma campanha por coleção-âncora; a coleção roda ao longo do ano (resort → best-sellers → pre-fall...).

## Conjuntos de cada campanha de prospecting: 3 públicos, MESMO pool de criativos

| Conjunto | Público | Peso do budget |
|---|---|---|
| `[XX] AMPLO \| Advantage+` | `targeting_automation.advantage_audience: 1`, sem interesses | ~40% |
| `[XX] MODA \| <interesses>` | flexible_spec com o cluster de interesses do nicho | ~40% |
| `[XX] LUXO \| <interesses+rendimento>` | cluster de luxo + income top ZIP US | ~20% |

- Género/idade conforme a marca (<cliente>: mulheres 18-65).
- Geo: só os países que vendem (cruzar Meta × loja; cortar a cauda worldwide). <cliente>: Europa SEM Portugal (31 países) + US + AU + HK + AE. **`geo_locations:{countries:[...], location_types:["home","recent"]}`: o `location_types` vai SEMPRE com este valor, senão a UI recusa publicar (#1870194).**
- `marketing_goal: "NONE"` em todos, logo após criar.
- Posicionamentos automáticos (não enviar campos de posicionamento).

### Interesses (IDs globais da Meta, extraídos do histórico da <cliente>; servem para qualquer conta de moda)

Cluster MODA (aparecia em 13-20 conjuntos históricos):
`6003188355978` Vestidos · `6004474265429` Vestido de festa · `6003552041427` Vogue · `6002978731374` Cosmopolitan · `6003266266843` Design de moda · `6003299793901` Elle · `6003456388203` Vestuário · `6011366104268` Roupas femininas · `6003354726060` Arte do Japão

Cluster LUXO:
`6003383552337` Resorts de luxo · `6003552041427` Vogue · `6004112805589` moda (revista) + income `6107813079183` (top 5% ZIP US) / `6107813551783` (top 10%) / `6107813553183` (top 10-25%)

Para outro nicho: repetir o processo (ler o targeting histórico da conta do cliente e extrair os IDs que ele já usou). Nunca inventar IDs.

## Anúncios: 1 por produto por conjunto (personalização por posicionamento)

Um único anúncio por produto, com o formato certo em cada posicionamento (feature "Opções de exibição de formato"). Dentro do mesmo anúncio:
- **Feed** → ficheiro 4:5 (ou 1:1) + message + headline + description da copy do produto, link, SHOP_NOW.
- **Stories/Reels** → ficheiro 9:16 verdadeiro, SÓ media (sem texto).
- Implementação: `asset_feed_spec` no `creative` do `ads_create_ad`, com os 2 vídeos rotulados (`adlabels`) e 2 `asset_customization_rules` (grupo feed / grupo stories-reels). Payload literal em `erros-api.md`.
- NUNCA dois anúncios FEED/STORIES separados (erro apanhado pelo cliente 2026-07-27; divide aprendizado e prova social).
- Destinos: produto próprio quando existe página; kimonos/categoria genérica → página da categoria; resto → coleção core best sellers. Tudo verificado com curl 200 antes.
- Contas de referência do cliente: pixel `<pixel-id>`, página `<page-id>`, conta `<account-id>` (tira-os do Business Manager dele antes de começar).
- Produto só com um formato: um anúncio simples com esse único vídeo/imagem.

## Números da <cliente> como referência de escala

~45 anúncios na BEST-SELLERS (3 conjuntos × 15 produtos), ~39 na NEW-IN (3 × 13), 1 anúncio por produto por conjunto. 50€/dia nas duas + 40€ catálogos + 5€ branding = 95€/dia num teto de 200€.

⚠️ Trade-off conhecido: pool grande + budget pequeno por conjunto (ex.: 26 anúncios a 4€/dia) faz a Meta concentrar em 2-3 anúncios. A resposta certa é gerir por BUDGET (arrancar só com AMPLO, ou subir o budget dos conjuntos de interesses), NUNCA encolher o pool, que tem de ser igual nos 3 conjuntos.

## Distribuição de budget (método validado 2026-07-22, teto 150€/dia na <cliente>)

Distribuir por **ROAS histórico por TIPO de campanha** (ler da API com time_range da era boa), não por intuição. Na <cliente>: catálogo ADV+ ~5,9 · prospecting multi-geo ~2,6 · mono-país 0,5-1,6 (nunca repetir) · retargeting sub-investido · branding sem retorno direto. Alocação resultante: **~40% catálogos** (desvio deliberado face aos ~25% históricos, porque renderam ~2x), **~57% prospecting** (mantém a maioria: alimenta o catálogo e o remarketing de sinal), **~3% branding**. Dentro do prospecting: coleção core > coleção nova; AMPLO = MODA; LUXO a metade. Remarketing com teto baixo (audiência 180d satura por frequência). Regras de aplicação: conjuntos AO VIVO sobem por degraus de +20% cada 3-4 dias; conjuntos recém-criados podem ir direto ao alvo; deixar folga sob o teto porque o ABO sobre-entrega até +25% num dia (compensa na semana).

## Métricas de gestão

- **ROAS blended** = receita total da loja ÷ gasto Meta (meta <cliente>: 10).
- **CAC blended**: Compras ≈ `omni_initiated_checkout` × 0,68; CAC = gasto ÷ compras. Julgar campanhas/conjuntos/países por isto, não pelo Purchase do pixel.
- Escala: +20% de budget cada 3-4 dias no que funciona; matar cauda de países sem vendas com breakdown por país a 7 dias.

## Checklist de ativação (autonomia)

1. Ativar os conjuntos, depois os anúncios (a criação força PAUSED mesmo pedindo ACTIVE).
2. `ads_get_errors` (entity_ids em array) nos conjuntos + amostra de anúncios por tipo.
3. Erros INTERNAL sem código: repetir 1x.
4. Campanha fica PAUSED para o cliente ligar. Ao ativar, ele pausa as campanhas antigas que estejam a gastar em sobreposição.
