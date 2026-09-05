# Mecânica do MCP meta-ads: parâmetros, formatos, erros e correções

Tudo aqui foi descoberto à força em produção (<cliente>/<cliente>, jul 2026). Consultar ANTES de cada create/update.

## Nomes e formatos de parâmetros (a causa nº 1 de erros de validação)

| Tool | O que exige |
|---|---|
| `ads_create_campaign` | **`campaign_name`** (não `name`) + **`buying_type: "AUCTION"`**, `objective`, `special_ad_categories: []`. ABO = NÃO passar `campaign_daily_budget` |
| `ads_create_ad_set` | `ad_set_name`, `daily_budget` em cêntimos, `optimization_goal`, `billing_event`, `destination_type`, `promoted_object` e `targeting` como strings JSON |
| `ads_update_entity` | exige **`ad_account_id`** e entity_type **`ad_set`** com underscore (não `adset`) |
| `ads_create_ad` | parâmetro **`creative`**, string JSON: `{"creative_id": "123"}`. ID solto dá "creative must be a valid JSON object string" |
| `ads_get_errors` | **`entity_ids` é array obrigatório**; sem ele rejeita |

## Targeting

- **Confirmado em produção: campanha montada com esta receita publicou pela interface sem um único erro.** É o molde a seguir.
- **#1870194 / `location_types`: A CURA (provada em produção). Enviar SEMPRE `location_types: ["home","recent"]` explicitamente em `geo_locations` (e em `excluded_geo_locations`, se existir), em TODOS os creates e updates de ad set. Sem exceção.**
  1. **A causa:** a Meta removeu o menu "moram / estiveram recentemente / de visita" da interface e ficou só o comportamento único "vive ou esteve recentemente", que na API é exatamente `["home","recent"]`. O campo continua obrigatório no backend: se não o enviarmos, o servidor grava o default histórico **`["home"]`**, que corresponde à opção **removida**. A UI de publicação vê `["home"]`, reconhece a opção morta e recusa o "Publicar" com #1870194.
  2. **A versão anterior desta nota estava ERRADA** e dizia "nunca enviar `location_types`". Era essa instrução que produzia o erro: omitir o campo é que o deixa em `["home"]`. Enviar `[]` de facto não limpa (regrava `["home"]`), mas **enviar `["home","recent"]` grava e fica** (verificado por update + releitura em 12 conjuntos da o kit e 16 da <cliente>).
  3. **Diagnóstico em 1 comando:** `ads_get_ad_entities` level=adset fields `["id","name","status","targeting"]` e agrupar por `targeting.geo_locations.location_types`. Os que dizem só `home` são os que vão trancar; os que dizem `home+recent` publicam sem aviso. Foi assim que se separou o trigo do joio nas 6 contas.
  4. `ads_get_errors` devolve `{}` mesmo nos conjuntos partidos: é validação de publicação, não erro de entidade. **Nunca usar `ads_get_errors` para dar isto por resolvido**; a prova é a releitura do `location_types`.
  5. A entrega em si não é bloqueada pelo valor (há conjuntos com `["home"]` a entregar em learning phase). O que fica bloqueado é o cliente publicar ou editar pela UI.
  6. **Ao corrigir um ad set existente, o update de targeting SUBSTITUI o objeto todo:** ler o targeting atual, remover os campos derivados (`page_types`, `dt_consolidation_state`, `age_range` e todos os `effective_*`, que a API devolve mas não aceita), reduzir `custom_audiences`/`excluded_custom_audiences` a `[{"id": "..."}]`, forçar o `location_types` e reenviar TUDO o resto (interesses, exclusões, posicionamentos, género, idades). Guardar backup do targeting original antes de escrever.
  7. **O update força o ad set a PAUSED** (`status_forced_to_paused: true` na resposta). Reativar a seguir com `ads_activate_entity`, senão o conjunto não arranca quando a campanha for ligada.
  8. **Operações ao NÍVEL DA CAMPANHA na UI (ex.: converter CBO↔ABO) republicam a campanha inteira e a validação varre TODOS os conjuntos, incluindo os pausados antigos** (<cliente> 30.07: a conversão da [USA] para ABO chumbou por conjuntos com `["home"]`). Antes de o cliente fazer qualquer operação de campanha na UI, garantir que TODOS os ad sets dessa campanha têm `["home","recent"]`, pausados incluídos. Nota: CBO→ABO não é convertível por API (não se consegue tirar o budget da campanha); essa operação é mesmo da UI, a nossa parte é limpar o caminho.
  9. **⚠️ NUNCA construir a lista de "quais reativar" a partir de uma leitura antiga.** O update força PAUSED, por isso a decisão de reativar tem de vir do estado LIDO NO MOMENTO, ad set a ad set: ler `status` imediatamente antes do update e reativar se era ACTIVE. Incidente <cliente> 30.07: o plano foi montado com um retrato de há horas (correu 3h30), o cliente entretanto ativou conjuntos pela UI, e a correção desligou 2 conjuntos que estavam a ENTREGAR (48 EUR e 6 EUR gastos) e não os repôs. Regra prática: numa correção em massa, ou se lê o estado dentro do mesmo passo do update, ou se reativa TUDO o que tinha gasto recente. E no fim, varrer sempre à procura de `status: PAUSED` com `amount_spent > 0` nos últimos dias: é a assinatura de ter desligado algo vivo.
  10. **Antes de aplicar a cura de um erro conhecido, RELER esta referência** (<cliente> 30.07: uma sessão aplicou a doutrina antiga "omitir o campo" DEPOIS de outra sessão já ter provado o contrário, e piorou 13 conjuntos que estavam bons; a skill é partilhada entre sessões e pode ter sido corrigida entretanto).
- **Rascunhos do Ads Manager guardam a fotografia ANTIGA do targeting.** Depois de corrigir por API, o painel "Conferir itens de rascunho" pode continuar a acusar o erro: o rascunho valida o snapshot dele, não o servidor. Correção: fazer as alterações de status por API (a autonomia cobre conjuntos e anúncios) e o cliente clica **"Descartar rascunhos"** + refresh. Nunca perseguir um erro de rascunho no lado do servidor sem primeiro perguntar se há rascunhos abertos.
- **⚠️ ENTIDADES COM #1870194 FICAM COM AS PUBLICAÇÕES CONGELADAS (incidente <cliente> 23.07, o mais grave até hoje):** a API aceita e GRAVA alterações de budget/targeting (o Ads Manager até as mostra), mas a Meta **continua a ENTREGAR com a última configuração publicada com sucesso**. Resultado real: budgets gravados de 95€/dia, entrega a ~200€/dia (cada conjunto a ~2x). **Alterações de ESTADO (pausar/ativar) continuam a propagar; usar isso como travão de emergência.** Deteção: comparar `amount_spent` de hoje com `daily_budget` gravado, conjunto a conjunto; >135% do budget = entrega dessincronizada. Enviar `"location_types": []` não limpa (o servidor normaliza para `['home']`). **A única cura é a migração de público na UI pelo cliente** (Editar → Público → Localização → re-selecionar países → Publicar, conjunto a conjunto), ou recriar os conjuntos de raiz (a 1.ª publicação de um conjunto novo entrega com os budgets de criação). Nunca confiar que um update de budget teve efeito numa entidade marcada com #1870194.
- **Erro 1487056 "Os conjuntos de anúncios eliminados não podem ser editados"**: a entidade foi apagada e substituída (duplicação na UI ou recriação). Encontrar a versão viva pelo NOME na listagem completa, ou pelos criativos com `ads_get_creative_ads` (creative_id → ad ids), que também resolve quando a listagem geral corta no limite.
- **O update de targeting SUBSTITUI, não faz merge**: reenviar SEMPRE completo (geo + genders + age + flexible_spec + custom_audiences + excluded + targeting_automation), senão perde-se o que não for reenviado.
- **`marketing_goal: "NONE"` sempre** após criar o ad set: o default "Acquire new customers" exige Custom Audience de clientes → **#1870251**, fatal em contas sem ToS de audiences.
- Interesses: `flexible_spec: [{"interests": [{"id": "..."}], "income": [...]}]`. Advantage+ audience: `targeting_automation: {"advantage_audience": 1}` (0 quando há interesses manuais).
- **⚠️ O MCP cria TODOS os ad sets com `targeting_as_signal: 3`** (audiências e interesses tratados como SINAL, não como limite: a Meta expande para fora deles). Num conjunto de prospecting é aceitável; **num conjunto de REMARKETING é um bug de entrega**, o dinheiro vaza para "Novo público" (na <cliente>: 35% do gasto do DPA foi para gente nova). Correção validada: `ads_update_entity` com fields `{"targeting_as_signal": 0}` (aceite como campo direto). Verificar a entrega real no Ads Manager pelo breakdown de segmentos Advantage+ (Novo público / Engajado / Clientes existentes): é o teste de que o desenho está mesmo a acontecer. Regra: em ad sets de remarketing, pôr `targeting_as_signal: 0` LOGO na criação.

## Criativos

- **Vídeo exige thumbnail sempre**: `ads_get_ad_videos` com `video_ids` + `fields:["picture"]` (1 chamada cobre o lote) → passar em `image_url`. Sem isso: "At least one of image_hash or image_url must be provided".
- **Imagem da biblioteca**: `image_hash` direto no `ads_create_creative`, sem alojar nada.
- **Stories sem texto**: omitir `message`/`headline`/`description`; a API aceita media + link + CTA.
- **Criativos são IMUTÁVEIS**: não há edição de copy/link/media num anúncio existente. Correção = criativo novo + anúncio novo + renomear o antigo `[APAGAR]` (o MCP não apaga anúncios). Logo: confirmar copy e URLs ANTES do lote.
- **`asset_feed_spec` FUNCIONA pelo MCP** (corrigido 2026-07-27; a versão antiga desta nota estava errada e levou a 2 anúncios feed/stories separados). Passa-se um `asset_feed_spec` completo DENTRO do JSON do argumento `creative` do `ads_create_ad` (ao lado de um `object_story_spec` mínimo só com `page_id`), e o MCP entrega-o à Graph API tal e qual. Assim faz-se **1 anúncio com o vídeo certo em cada posicionamento** (feed 4:5 + stories/reels 9:16). Ver a secção "Personalização por posicionamento" abaixo.
- VISIT_WEBSITE não existe para image ads → SHOP_NOW / LEARN_MORE.
- Carrossel de catálogo: `product_set_id` no creative, sem image/video. Se "conta do Instagram em falta" e `ads_get_ig_accounts` vier vazio: reutilizar um creative de catálogo existente que funcione.

## Estados e ativação

- **`status: "ACTIVE"` na criação é IGNORADO**: `ads_create_ad` força PAUSED sempre. Ativar é chamada separada (`ads_activate_entity`).
- **`ads_update_entity` pode devolver `status_forced_to_paused: true`**: se a entidade estava ativa, `ads_activate_entity` logo a seguir.
- **CBO → ABO não é convertível** (rejeita `daily_budget: 0` como "orçamento demasiado baixo"): recriar a campanha sem `campaign_daily_budget`.
- Sob CBO todos os conjuntos ficam presos à mesma optimization goal; ABO liberta.
- OUTCOME_ENGAGEMENT + THRUPLAY: se "É necessário um conjunto de anúncios com um objeto promovido", usar `destination_type: "ON_VIDEO"`; o promoted_object não se adiciona depois, recria-se o conjunto.

## Listagem e verificação

- **`filter_key`/`filter_value` em `ads_get_ad_entities` são IGNORADOS**: devolve a conta inteira cortada no `limit`. Não serve para verificar um lote novo; confiar nos `ad_id` + status devolvidos por cada create, e validar com `ads_get_errors`.
- Outputs grandes (targeting de 60+ ad sets = 150k+ chars) vão para ficheiro: processar com python/jq, nunca tentar ler em contexto.
- `targeting` É legível em fields de adset (ao contrário do que a versão antiga desta skill dizia): é a fonte para recuperar interesses e posicionamentos históricos.
- `ads_get_creatives` sem IDs faz timeout: pedir por `creative_ids` específicos.
- Preview é desnecessário: validar com effective_status + `ads_get_errors`.

## Flakiness (repetir a MESMA chamada 1x resolve)

- `ads_create_ad`: erro "permission" 1815694 transiente.
- `ads_activate_entity`: `INTERNAL: An internal error occurred` sem código.
- Se persistir à segunda, aí sim é problema real.

## Pôr criativos em produção: IMAGEM vs VÍDEO (não confundir)

### IMAGEM: autonomia total, a biblioteca é dispensável
`ads_create_creative` aceita **`image_url`** e a Meta copia o ficheiro na criação. **Nunca pedir upload ao cliente para imagens.** Procedimento validado em produção num e-commerce real, sem intervenção do cliente:

```bash
DEST=~/Documents/Claude/Deploys/<cliente>-ads-assets
mkdir -p "$DEST" && cp <ficheiros renomeados> "$DEST/"
cd "$DEST" && vercel deploy --prod --yes --name <cliente>-ads-assets --scope <o-teu-scope-vercel>
```
- Precisa de `dangerouslyDisableSandbox: true` (rede) e do caminho absoluto do vercel (`~/.npm-global/bin/vercel`).
- Um `index.html` mínimo evita listagem vazia; `vercel.json` com Cache-Control é opcional.
- **Verificar cada URL a 200 ANTES de criar criativos**, com o nome **URL-encoded** (`urllib.parse.quote`): nomes com espaços, parênteses ou `&` partem o pedido da Meta silenciosamente.
- URL final: `https://<cliente>-ads-assets.vercel.app/<ficheiro>`. Projeto por cliente, NUNCA no site de outro cliente ou da tua marca.
- Alternativa se já estiver na biblioteca: `image_hash` direto (não precisa de alojamento).

### VÍDEO: precisa mesmo de estar na biblioteca (`video_id`)
O MCP não faz upload de vídeo e `ads_create_creative` não aceita URL de vídeo. Opções, por ordem:
1. **Verificar primeiro se já lá está** (`ads_get_ad_videos` com filtro `title`): pode ter sido subido num lote anterior. Já aconteceu um vídeo estar subido de um lote anterior, o que poupou uma ida ao cliente.
2. `meta_upload.py upload` via Graph API `file_url` (exige token System User em `~/.config/a-casa/meta-ads.env`; suporta `META_TOKEN_<account_id>` por BM ou `META_ACCESS_TOKEN` de BM guarda-chuva). **Ainda por criar: é o único bloqueio real que resta.**
3. Último recurso: o cliente carrega a pasta renomeada no Ads Manager (validado: 84 ficheiros em ~5 min).

Vídeos >100 MB excedem o limite estático do Vercel para a via 2: alojar na VPS (`vps.a-casa.pro`) e passar esse URL ao `upload`.

**Thumbnail do criativo de vídeo**: sai do próprio vídeo da biblioteca (`ads_get_ad_videos` + `fields:["picture"]`), não precisa de alojamento.

## Renomeação de criativos (`rename_criativos.py`)

- Produto vem da PASTA (folder-first), não do nome do ficheiro; aliases para pastas com nome errado; typos corrigidos.
- Rácio vem das DIMENSÕES REAIS (ffprobe/PIL): AR<0,65 = 9x16, <0,95 = 4x5, <1,15 = 1x1, resto 16x9 (não usar). Ficheiros chamados "16x9" podem ser 1080x1920 verticais verdadeiros; nunca confiar no nome.
- Tags de coleção `--tag BS`/`NI` → `BS_PRODUTO_4x5.mp4`. Dedupe md5, filtro de lixo (screenshots, "untitled"). ⚠️ O filtro de lixo NÃO pode descartar às cegas ficheiros "ChatGPT Image...": a <cliente> usa imagens AI como criativos de produto reais (23.07). Renomear pelo nome da PASTA e marcar como AI → os ads destes criativos levam `self_ai_disclosure: "OPT_IN"`.
- **Sincronização com o Drive**: antes de assumir que "está tudo subido", re-descarregar a pasta do Drive (`drive-grab <folder_id>`) e comparar por **md5** com a cópia local; o cliente adiciona produtos novos sem avisar (23.07: 3 produtos novos apareceram no Drive no próprio dia).
- ⚠️ Nomes de pasta com ESPAÇO NO FIM (`"<cliente> CORE & NEW IN "`): usar o caminho exato do `ls`, senão tudo falha em silêncio.

## Personalização por posicionamento (asset customization): 1 anúncio feed+stories

Validado em produção com um anúncio de teste real. Cria UM anúncio que serve o vídeo 4:5 no feed e o 9:16 nos stories/reels. Mecânica (confirmada com a doc da Marketing API):

- **Não existe `optimization_type: "PLACEMENT"`** (dá erro). A customização por posicionamento é ativada só pela presença de `asset_customization_rules`.
- **Mínimo 2 regras.** O mapeamento vídeo→posicionamento é por `adlabels` (nome do label), nunca por índice. Cada regra referencia um label para CADA asset que uses (video, body, title, link).
- **Cobertura de posicionamentos:** as regras só precisam de cobrir os grupos que interessam (feed + stories/reels); a Meta aceitou o ad com os posicionamentos exóticos (instream 16:9, messenger, threads, notification) de fora. Feed do Instagram = `stream` (não `feed`).
- Passa-se via `ads_create_ad`, argumento `creative` (JSON string). `object_story_spec` leva só `page_id` (se a página do cliente já tiver o IG ligado não é preciso `instagram_user_id`; se as regras de IG falharem, adicionar `instagram_user_id`).
- Vídeos: obter o `video_id` de cada creative FEED e STORIES existente (`ads_get_creatives` fields `["video_id","body"]`); o body do creative de feed é a copy do produto.
- O ad nasce `PENDING_REVIEW` PAUSED (normal). Confirmar com `ads_get_ad_preview` em `MOBILE_FEED_STANDARD` (sai 4:5) e `INSTAGRAM_STORY` (sai 9:16).

Payload do `creative` (substituir os `<...>`):

```json
{
  "object_story_spec": { "page_id": "<PAGE_ID>" },
  "asset_feed_spec": {
    "ad_formats": ["SINGLE_VIDEO"],
    "videos": [
      { "video_id": "<VID_FEED_4x5>",  "adlabels": [{ "name": "v_feed" }] },
      { "video_id": "<VID_STORY_9x16>", "adlabels": [{ "name": "v_story" }] }
    ],
    "bodies":  [{ "text": "<copy do produto>", "adlabels": [{ "name": "b1" }] }],
    "titles":  [{ "text": "<headline>",        "adlabels": [{ "name": "t1" }] }],
    "link_urls": [{ "website_url": "<link>",   "adlabels": [{ "name": "l1" }] }],
    "call_to_action_types": ["SHOP_NOW"],
    "asset_customization_rules": [
      { "priority": 1,
        "customization_spec": { "publisher_platforms": ["facebook","instagram"],
          "facebook_positions": ["feed","profile_feed","marketplace","video_feeds","search","biz_disco_feed"],
          "instagram_positions": ["stream","explore","explore_home","profile_feed","ig_search"] },
        "video_label": { "name": "v_feed" }, "body_label": { "name": "b1" }, "title_label": { "name": "t1" }, "link_url_label": { "name": "l1" } },
      { "priority": 2,
        "customization_spec": { "publisher_platforms": ["facebook","instagram"],
          "facebook_positions": ["story","facebook_reels"], "instagram_positions": ["story","reels"] },
        "video_label": { "name": "v_story" }, "body_label": { "name": "b1" }, "title_label": { "name": "t1" }, "link_url_label": { "name": "l1" } }
    ]
  }
}
```

Para produto só com um formato: anúncio simples (um `video_id`/`image_hash`), sem `asset_feed_spec`. Token: user token com `ads_management` chega (o do MCP serve); system user só se for para automação sem expirar.

**Variante IMAGEM: confirmada em produção (<cliente>, 07-10.08.2026, 24+24 anúncios "LNW"/"JL", zero erros, previews verificadas).** Mesma mecânica, com 3 trocas: `ad_formats: ["SINGLE_IMAGE"]`, bloco `images` com `hash` (o image_hash da biblioteca) em vez de `videos`/`video_id`, e `image_label` em vez de `video_label` nas 2 regras. O upload da imagem (`ads_creative_upload_image` por `image_url`) devolve o hash na hora, síncrono; o `title_label` pode ficar de fora se o cliente não deu headline (validado: anúncio só com body).


## Lições de 11-12.08.2026 (lote JL/teasers <cliente>)

- **Anúncio de produto novo linka ao PRÓPRIO produto, nunca à shop-all.** Regra da cliente <cliente>,
  por escrito ("Se estamos a anunciar produtos novos tens que linkar ao próprio produto"), depois
  de 24 anúncios JUST LANDED irem para o ar com shop-all. Teasers de produto que ainda não existe
  são a exceção (aí a shop-all é dela). Perguntar o destino POR PRODUTO antes de subir um lote de
  lançamento; se a página ainda não existir na loja, é sinal de teaser.
- **Copy só no feed (stories limpas): 2 `bodies` no asset_feed_spec**, um com a copy (label do
  feed) e um **vazio `""`** (label das stories). A API aceita o body vazio sem fallback nenhum
  (validado em produção). Confirmar com os 2 previews.
- **`ads_activate_entity` pode estar sob regra "ask" nas settings**, e o ask ganha ao
  allow do projeto mesmo em sessões headless. Não contornes a regra: ela existe para nenhuma
  campanha ser ativada sem um humano confirmar. Se uma sessão automática precisa de ativar
  entidades, deixa-as criadas em pausa e ativa tu pela sessão interativa.
- **Sessões headless (`claude -p` + runbook fechado) funcionam para operar a Meta** quando o MCP
  está em baixo na sessão principal: runbook com payloads literais + ficheiro de RESULTADOS
  escrito à medida + regra "se falhar fora do previsto, PÁRA". Duas execuções limpas (teasers LA
  e fix dos links). O agente parou sozinho no gate de permissões duas vezes SEM pausar nada, que
  era o comportamento certo (activate-first).
- **Token invalidado (subcódigo 460 = password mudada ou sessão terminada).** Enquanto não
  houver token de utilizador de sistema no Business Manager do cliente, contar com o ritual de
  reautorização a cada falha.
- **Os campos de Advantage+ creative enhancements são ILEGÍVEIS pelo MCP** (12.08.2026):
  `ads_get_creatives` rejeita `degrees_of_freedom_spec`, `asset_feed_spec` e `object_story_spec`
  como "Unsupported field(s)" e o catálogo do MCP não os tem a nível nenhum. Consequência: não dá
  para AUDITAR se um anúncio existente tem os automatismos ligados; a confirmação é só na UI ou
  pela Graph API direta. O que o MCP DEIXA fazer é escrevê-los na criação: o
  `degrees_of_freedom_spec.creative_features_spec.standard_enhancements.enroll_status = OPT_OUT`
  dentro do `creative` do `ads_create_ad` é ACEITE e ecoado no spec (validado em 6 anúncios).
  Regra prática: anúncios novos nascem sempre com o OPT_OUT; para os antigos presume-se ligado
  (é o default da Meta). O sintoma clássico de enhancements ligados numa imagem sem 9:16 dedicado
  é a imagem esticada/duplicada nas Stories, que foi o que a cliente <cliente> apanhou.
- **`ads_get_ad_entities` sem filtro pode vir truncado** mesmo com limit alto: a leitura
  autoritativa de ativos é com filtro `effective_status IN [ACTIVE]` (12.08: a leitura sem filtro
  omitiu 2 anúncios de uma campanha).- **Print de cliente "a ver um anúncio antigo" pode ser a vista de GUARDADOS/histórico do
  Instagram, não o feed** (13.08.2026, <cliente>): ecrã com título "Ad" + seta de voltar + ícone de
  recarregar + bookmark preenchido = anúncio guardado/atividade de anúncios. Um anúncio PAUSED
  renderiza aí para sempre com o criativo antigo, logo não prova entrega ao vivo. Diagnóstico
  correto: listar ativos com `creative_id` → mapear thumbnail/hash ao ficheiro CDN
  (`ads_get_ad_images` com os hashes dá o URL CDN por hash; comparar com o do thumbnail do
  criativo) → cruzar com insights do período. Só depois decidir se há algo a pausar.
- **A identidade que aparece nos registos de atividade das ações por MCP pode não ser a tua**,
  é a da conta que autorizou a aplicação: não confundir com alguém da equipa do cliente a mexer
  na conta.
- **Bid cap em campanha CBO (13.08.2026, lote BID CAP da <cliente>):** (1) `ads_create_campaign`
  IGNORA `daily_budget` e `bid_strategy` (o echo do spec não os traz): aplicar logo a seguir com
  `ads_update_entity` da campanha. (2) Ovo-e-galinha: o pré-check do MCP recusa `bid_amount` no
  conjunto sob CBO ("remove these fields") e a Graph recusa `LOWEST_COST_WITH_BID_CAP` sem bids
  nos conjuntos (subcódigo 1885924) e recusa `bid_amount` avulso sob lowest cost (1885742). A
  saída é UMA chamada à campanha: `ads_update_entity` fields
  `{"bid_strategy":"LOWEST_COST_WITH_BID_CAP","adset_bid_amounts":{"<adset_id>":500,...}}`.
  Serve também para subir o teto depois (a rotina diária usa isto). (3) `entity_type` de conjuntos
  no update é `ad_set`; `adset` é recusado. (4) `bid_amount` NÃO é legível em
  `ads_get_ad_entities` (campo não suportado): o valor corrente do teto tem de viver fora da Meta
  (no House, `agents.state`). (5) `ads_create_ad` aceita `creative` = `{"creative_id":"..."}`
  para REUTILIZAR um criativo existente (o anúncio novo partilha o post e a prova social);
  validado em 51 anúncios. (6) O parâmetro do conjunto na criação é `ad_set_id`/`ad_name`
  (não adset_id/name), e `entity_ids` em `ads_get_ad_entities` é IGNORADO (vem tudo): filtrar
  localmente. (7) `filtering` value tem de ser array (["x"]), mesmo com um só valor.
