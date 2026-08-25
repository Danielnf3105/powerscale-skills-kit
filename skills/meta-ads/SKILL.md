---
name: meta-ads
description: >
  Processo para montar, subir, ativar e validar campanhas Meta Ads por API
  (MCP oficial da Meta ou Graph API), com o blueprint de conta e-commerce e
  os erros conhecidos da API. Usar sempre que pedes "sobe anúncios para X",
  "monta a campanha do cliente Y", "cria ads", "reestrutura a conta Meta",
  "resolve este erro do Ads Manager", ou quando entra um cliente novo com
  conta de anúncios para operar. Cobre estrutura de campanhas, criativos,
  copy, catálogos, interesses, orçamentos e ativação.
---

# Subir anúncios Meta por API

Duas referências obrigatórias nesta pasta:

- `references/blueprint-ecommerce.md`: a arquitetura de conta de e-commerce
  completa (campanhas, conjuntos, públicos, orçamentos, métricas). Para contas
  de e-commerce, começar por aí.
- `references/erros-api.md`: a mecânica da API (nomes de parâmetros, formatos,
  erros e correções). Consultar antes de cada create ou update, poupa rondas
  inteiras de tentativa e erro.

**Antes da primeira campanha:** o acesso faz-se por MCP da Meta ou por token de
utilizador de sistema do Business Manager do cliente. Ver a skill
`ferramentas-e-acessos` para ligar e para guardar a chave. Sem acesso próprio à
conta do cliente, não se monta nada por API.

## As 10 regras de ouro

0. **`location_types: ["home","recent"]` em TODO o `geo_locations`, sempre, na
   criação e na edição.** É a regra zero. Sem ela o servidor grava `["home"]`,
   uma opção que a Meta removeu, e o Ads Manager recusa o "Publicar" com o erro
   **#1870194**. Vale também para `excluded_geo_locations`. A prova não é o
   `success` da criação nem o `get_errors` (devolve `{}` na mesma): é reler o
   `targeting` do conjunto no servidor e ver lá o valor.
1. **Posicionamentos automáticos SEMPRE. Nunca separar feed de stories em
   conjuntos diferentes.** Não passar `publisher_platforms`,
   `facebook_positions` nem `instagram_positions`. Separar tira liquidez ao
   leilão e fragmenta a aprendizagem. Antes de assumir, lê o `targeting` dos
   conjuntos históricos da conta e conta quantos são automáticos.
2. **Um só anúncio por produto, com o ficheiro certo em cada posicionamento.**
   O MESMO anúncio leva o 4:5 no feed (com texto) e o 9:16 verdadeiro nos
   stories e reels (só media). Nunca dois anúncios feed/stories separados: dois
   anúncios do mesmo produto partem a aprendizagem e a prova social por dois
   posts. Faz-se com um `asset_feed_spec` dentro do argumento `creative`, com os
   ficheiros rotulados por `adlabels` e pelo menos duas
   `asset_customization_rules`. Payload literal em `references/erros-api.md`.
3. **O mesmo pool de criativos em todos os conjuntos da mesma campanha.** O
   público é a variável, o criativo é a constante. Sinal de alarme: dois
   conjuntos com o mesmo orçamento e número de anúncios diferente. Os
   `creative_id` são partilháveis, por isso equalizar custa zero produção.
4. **ABO com orçamentos fragmentados e baixos** (conjuntos de 4 a 30 euros).
   CBO esfomeia conjuntos pequenos e remarketing. Escalar é +20% de 3 em 3 ou 4
   em 4 dias, ou acrescentar conjuntos. Nunca engordar um de repente. Se o
   orçamento total for curto, arranca só com o conjunto amplo; nunca cortes no
   pool de criativos.
5. **Nunca OUTCOME_AWARENESS para vídeo.** Branding e vídeo é
   OUTCOME_ENGAGEMENT + `optimization_goal: THRUPLAY` + `destination_type:
   ON_VIDEO`, em ABO.
6. **Todos os produtos da pasta entram em teste.** Contar os produtos antes de
   montar e mapear cada um a um anúncio. Varrer imagens E vídeos: um produto
   pode existir só num formato.
7. **Uma copy por produto, à letra.** O texto do cliente fica intocado,
   incluindo a pontuação. Rascunhos teus marcam-se para validação e levam zero
   em-dash.
8. **Nada fora de época e nada de auto-crops.** Um criativo que diga "Spring"
   não corre no verão. Os cortes automáticos que a Meta gera dos 1x1 aparecem
   com cabeças cortadas: usar só 9:16 originais e classificar sempre pelas
   dimensões reais do ficheiro (ffprobe ou PIL), nunca pelo nome.
9. **Interesses vêm do histórico da conta, nunca inventados.** A fonte certa
   são os conjuntos antigos do cliente: ler `targeting` ao nível do conjunto e
   extrair os `flexible_spec.interests[].id`. A estrutura padrão é AMPLO mais um
   ou dois conjuntos de interesses.
10. **Confirmar destino e copy ANTES de criar o lote.** Criativos são
    imutáveis: corrigir depois obriga a criar tudo de novo e a renomear os
    errados. Verificar cada URL com um pedido HTTP a 200.

## Ativação: o que se pode ligar sozinho

**Regra do kit: conjuntos e anúncios podem ser ativados sozinhos; a campanha
fica sempre para quem paga a conta.** Com a campanha em PAUSED nada entrega nem
gasta, mas a Meta corre a validação toda. É passo obrigatório, não opcional.

Se a campanha destino já estiver ATIVA, ativar os anúncios põe-nos a gastar de
imediato. Dizer isso à letra no relatório final.

Fluxo no fim de cada montagem:

1. Ativar os conjuntos.
2. Ativar os anúncios um a um (muitas APIs ignoram o `status: ACTIVE` na criação
   e forçam PAUSED).
3. Correr o `get_errors` nos conjuntos e numa amostra de anúncios de cada tipo
   (vídeo feed, vídeo stories, imagem feed, imagem stories).
4. Resolver qualquer erro na hora. Erros `INTERNAL` sem código são falhas
   passageiras: repetir a mesma chamada uma vez.
5. Só a campanha fica por ligar.

**Quem paga tem de conseguir publicar e editar pela interface.** Um conjunto que
só se consegue ligar por API está partido, não resolvido.

## O fluxo em 6 fases

### Fase 0: Levantamento (nunca saltar)
1. Confirmar a conta certa (um cliente pode ter várias, e gastar em duas).
2. Histórico da conta: campanhas e conjuntos com métricas, e o `targeting` dos
   conjuntos antigos (posicionamentos, interesses, geografia que vendeu). A
   conta do cliente é a melhor fonte de verdade sobre o que funciona nela.
3. Pixel (o evento de compra dispara? web ou CAPI?), página de Facebook,
   públicos (sem termos aceites não há remarketing), catálogo e conjuntos de
   produtos.
4. Dados do negócio: emparelhar com a fonte de verdade (a loja, o backoffice).
   Best sellers dos últimos 30 dias e stock antes de escolher produtos.
5. Biblioteca de criativos: listar vídeos e imagens já lá dentro.

### Fase 1: Criativos

**Sincronizar primeiro.** Nunca assumir que a pasta local está atualizada. O
cliente acrescenta produtos sem avisar. Renomear com o produto vindo da pasta e
o rácio das dimensões reais.

**Imagem e vídeo não seguem o mesmo caminho:**

| Tipo | Precisa da biblioteca? | Caminho |
|---|---|---|
| Imagem (png, jpg, gif) | Não | alojar num URL público e passar `image_url` na criação do criativo; a Meta copia sozinha |
| Vídeo (mp4, mov) | Sim (precisa de `video_id`) | upload por API com token de utilizador de sistema, ou o cliente carrega no Ads Manager |

- Um produto = idealmente 3 rácios: 4:5 e 1x1 para feed, 9:16 para stories. O
  16:9 não se usa.
- Imagens geradas por IA levam `self_ai_disclosure: "OPT_IN"`. Fotografia real,
  OPT_OUT.

### Fase 2: Copy
Uma copy por produto (regra 7). Adaptar apenas menções de estação fora de época,
e assinalar a alteração. O resto fica intocado.

### Fase 3: Estrutura

Seguir o `references/blueprint-ecommerce.md`. Receita de criação validada:

```
1. create_campaign   nome + objetivo (ODAX) + buying_type:"AUCTION" + special_ad_categories:"[]"
                     ABO = não passar orçamento de campanha
2. create_ad_set     optimization_goal:"OFFSITE_CONVERSIONS", billing_event:"IMPRESSIONS",
                     destination_type:"WEBSITE", daily_budget (em cêntimos),
                     promoted_object: {"pixel_id":"...","custom_event_type":"LEAD"|"PURCHASE"},
                     targeting: {"age_min":18,"age_max":65,
                                 "geo_locations":{"countries":["PT"],
                                                  "location_types":["home","recent"]},
                                 "targeting_automation":{"advantage_audience":1}}
                     dsa_beneficiary + dsa_payor (obrigatórios na UE)
                     NADA de publisher_platforms nem positions (regra 1)
3. update_entity     {"marketing_goal":"NONE"} no conjunto, logo a seguir
4. create_creative   page_id + image_hash (ou image_url) + link_url + texto + CTA
5. create_ad         creative: {"creative_id":"..."} + conversion_domain
```

**Macros de atribuição no `link_url` (obrigatório).** Os UTMs vão dentro do
próprio URL, porque o campo `url_tags` não existe nesta API:

`?utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.id}}&utm_term={{adset.id}}&utm_content={{ad.id}}`

O `utm_content={{ad.id}}` é a chave da atribuição: é o que liga cada lead ao
anúncio que a trouxe. Sem ele, a lead entra como "direto" e ninguém sabe que
criativo pagou a venda.

**Verificação obrigatória antes de reportar** (é o que transforma "criei" em
"está bom"):

1. Reler o conjunto no servidor e confirmar com os olhos: `location_types` =
   `["home","recent"]` e os posicionamentos efetivos com facebook, instagram,
   messenger e threads.
2. Correr o `get_errors` nos três níveis.
3. Pedir a pré-visualização do anúncio e olhar mesmo para a imagem devolvida.

### Fase 4: Anúncios
Um anúncio por produto por conjunto (regra 2), com personalização por
posicionamento. Vídeo exige thumbnail. Imagem usa `image_hash` direto.

### Fase 5: Ativação e validação
O fluxo de ativação acima, depois de passar a verificação da fase 3. A ativação
por API não substitui a verificação: a API liga conjuntos que a interface
recusa publicar, e o defeito fica escondido até alguém mexer.

### Fase 6: Fecho (obrigatório)
1. Documentar todos os IDs num ficheiro por lote:
   `clientes/<cliente>/ads/estrutura-<AAAA-MM>.md`.
2. Reportar: o que está ativo, o que está pausado, orçamento diário total,
   decisões tomadas sozinho (com justificação) e a lista curta do que só o
   cliente desbloqueia.

## Medição

- **ROAS blended** = receita total da loja a dividir pelo gasto Meta. O ROAS por
  campanha é diagnóstico, não é verdade.
- **CAC blended**, quando o pixel de compra é pouco fiável: compras estimadas ≈
  finalizações de compra iniciadas × 0,68; CAC ≈ gasto a dividir por compras.

## CTAs e compliance

- SHOP_NOW para e-commerce genérico, BUY_NOW para compra imediata, GET_QUOTE
  para B2B. VISIT_WEBSITE não existe para anúncios de imagem.
- Nichos de saúde, dinheiro e emprego têm regras próprias. Nada de promessa de
  cura, de rendimento garantido, nem de linguagem que identifique a pessoa
  ("estás acima do peso?").

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
