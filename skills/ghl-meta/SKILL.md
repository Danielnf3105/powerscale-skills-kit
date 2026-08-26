---
name: ghl-meta
description: >
  Junta o CRM (GoHighLevel) com o Facebook Ads e mostra, por anúncio, quantas
  leads trouxe, em que etapa do funil cada uma está agora, e quanto dinheiro
  fechou. Sai em quadro no terminal e em relatório visual que abre no browser.
  Diz também o que corrigir quando os dados não emparelham. Usar quando ele diz
  "que anúncio está a trazer os melhores clientes", "onde é que as leads deste
  anúncio ficaram presas", "não consigo cruzar o CRM com o Facebook", "o
  Facebook diz X leads e no CRM tenho Y", "que criativo devo cortar", "qual é o
  custo por cliente e não por lead", ou quando entra uma conta nova que corre
  anúncios e tem CRM.
version: 1.1.0
author: PowerScale Skills Kit
---

# Que anúncio trouxe os melhores clientes

O Facebook conta leads. O CRM conta dinheiro. Enquanto os dois não falarem, a
decisão de cortar ou escalar um criativo é um palpite, e corta-se quase sempre
o anúncio errado: **o que traz mais leads raramente é o que traz mais receita.**

Esta skill fecha essa distância.

## O que precisas antes de começar

Quatro chaves, no cofre (`~/.config/chaves/secrets.env`). **Nunca coladas no
chat:** uma chave que passa por ali fica queimada e tem de ser trocada.

| Chave | Onde se vai buscar |
|---|---|
| `GHL_TOKEN` | GoHighLevel, na subconta: Settings → Private Integrations → criar uma, com leitura de *contacts* e *opportunities*. É um token de subconta, não da agência. |
| `GHL_LOCATION_ID` | Settings → Business Profile, o id da subconta |
| `META_TOKEN` | business.facebook.com → Definições da empresa → Utilizadores de sistema → gerar token com `ads_read`, expiração Nunca |
| `META_AD_ACCOUNT` | o id da conta de anúncios, no formato `act_1234567890` |

Pede-as uma de cada vez e explica para que serve cada uma. Se ele não souber
onde ir, guia-o clique a clique: são dois menus em cada plataforma.

## Passo 1: o diagnóstico, e corre-se sempre primeiro

```
python3 ~/.claude/kit/ferramentas/ghl_meta.py --diagnostico
```

Diz quantos contactos têm atribuição, quantos trazem o **ID** do anúncio
(junção exata), quantos trazem só texto (junção por nome, aproximada), e quantos
anúncios não levam UTM nenhum no link.

Não saltes isto para ir direto ao relatório. Se os links não carregarem a
origem, o relatório sai vazio e ninguém percebe porquê: parece um problema do
CRM, e é do link do anúncio.

## Passo 2: o que quase sempre falta

Os anúncios não passam a origem. Resolve-se uma vez e vale para sempre: no
destino de cada anúncio, no fim do URL,

```
?utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.id}}&utm_term={{adset.name}}
```

A Meta substitui as chavetas no momento do clique.

**O `utm_content` leva o ID e não o nome, de propósito.** Renomear um anúncio é
uma coisa que se faz todas as semanas, e no dia em que se renomeia, um histórico
guardado por nome parte-se ao meio: metade dos dados fica num nome que já não
existe. O ID nunca muda. O nome bonito vem do Facebook na hora do relatório.

Duas notas que poupam uma tarde:

- **Isto vale para anúncios novos.** Editar o link de um anúncio a correr
  reinicia a aprendizagem dele. Em campanhas que estão a andar bem, aplica-se ao
  próximo lote, não de repente a todos.
- **Formulários instantâneos não têm link**, logo não têm UTM. Nesses, a origem
  entra pelo `ad_id` que a Meta manda com a lead, e o emparelhamento faz-se do
  lado de quem recebe o formulário.

## Passo 3: o relatório

```
python3 ~/.claude/kit/ferramentas/ghl_meta.py --relatorio --dias 30
python3 ~/.claude/kit/ferramentas/ghl_meta.py --relatorio --dias 30 --html relatorio.html
python3 ~/.claude/kit/ferramentas/ghl_meta.py --relatorio --dias 90 --csv dados.csv
```

Saem duas coisas.

**Onde estão as leads de cada anúncio, agora.** Cada linha é um anúncio, cada
coluna é uma etapa do funil dele no GHL, e o número é quantas leads desse
anúncio estão paradas ali:

```
ANUNCIO                      Lead nova Contactad Reuniao m Proposta   Ganhas Perdidas
VSL | Caso Joana | 4x5               0         3         4        3        2        0
VSL | Hook agressivo | 9x16         26         0         0        0        0        3
Carrossel | 5 erros | 1x1            0         0         0        0        0        0
```

Aquela coluna com 26 é o diagnóstico inteiro: esse anúncio traz muita gente que
entra no CRM e **nunca anda**. Isso não se resolve trocando o criativo, resolve-se
na qualificação ou no que a página promete. E o primeiro anúncio, com menos de
metade das leads, é o único que produz reuniões e vendas.

**E o quadro por resultado**, ordenado por valor ganho:

```
ANUNCIO                             LEADS  OPORT  GANHAS      VALOR     GASTO CUSTO/LEAD
VSL | Prova social | 4x5                3      2       1    4500.00    310.40    103.47
VSL | Hook agressivo | 9x16             5      2       0       0.00    640.00    128.00
```

É este o quadro que muda decisões. O segundo anúncio traz **mais leads e custa
mais do dobro em gasto**, e não fechou um único cliente. Num painel de Facebook
ele parece o melhor dos dois.

Linhas marcadas com `~` foram juntas por nome e são aproximadas: dois anúncios
com o mesmo nome ficam somados.

## Passo 4: a versão que se vê

```
python3 ~/.claude/kit/ferramentas/ghl_meta.py --relatorio --dias 30 --html ~/Desktop/anuncios.html
```

Escreve **um ficheiro só**, nas cores da marca dele (lidas do perfil), que abre
no browser com dois cliques e se manda por email a quem for preciso. Traz os
números do topo (leads, clientes fechados, valor, gasto, custo por cliente), a
matriz anúncio × etapa com as células pintadas por intensidade, e o quadro por
resultado. Quanto mais escura a célula, mais leads paradas ali: vê-se o
problema antes de se ler o número.

Sem ligações para fora e sem bibliotecas: abre sempre, mesmo sem internet.

## Passo 5: correr sozinho, uma vez por semana

Um relatório que só existe quando alguém se lembra de o pedir não se lê.
Agenda-o e ele passa a estar lá.

**Windows**, todas as segundas às 9h:

```
schtasks /create /tn "Relatorio de anuncios" /sc weekly /d MON /st 09:00 ^
  /tr "py -3 %USERPROFILE%\.claude\kit\ferramentas\ghl_meta.py --relatorio --dias 30 --html %USERPROFILE%\Desktop\anuncios.html"
```

**Mac**, o mesmo com `crontab -e`:

```
0 9 * * 1 /usr/bin/python3 ~/.claude/kit/ferramentas/ghl_meta.py --relatorio --dias 30 --html ~/Desktop/anuncios.html
```

Depois de agendar, **corre a tarefa uma vez à mão e confirma que o ficheiro
aparece**. Um agendamento que nunca se viu correr não está feito: é só uma
linha numa lista.

A janela de 30 dias é o mínimo razoável. Se o ciclo de venda dele for mais
longo do que isso, sobe para 60 ou 90, senão o relatório mostra gasto sem
receita e faz cortar o que estava a resultar.

## Como se lê

- **A matriz das etapas responde a uma pergunta diferente da tabela.** A tabela
  diz o que já deu dinheiro; a matriz diz o que está a caminho e onde está
  encravado. Um anúncio com poucas vendas mas com gente na etapa de proposta
  não é um anúncio mau, é um anúncio recente.
- **Ordena por valor ganho, nunca por leads.** Leads baratas de gente que nunca
  compra são o caminho mais rápido para escalar um prejuízo.
- **Custo por cliente, não custo por lead.** Gasto a dividir pelas ganhas.
- **Poucas ganhas não decidem nada.** Com uma ou duas vendas por anúncio, o que
  estás a ver é ruído. Junta semanas ou olha ao nível do conjunto.
- **Uma lead demora a fechar.** Se o ciclo de venda dele é de três semanas, um
  relatório a 7 dias mostra gasto sem receita e faz cortar o que estava a
  resultar. A janela tem de ser maior do que o ciclo de venda.
- **Contactos sem origem** aparecem no fim. Muitos significa fuga na medição,
  não vendas orgânicas.

## O que isto não faz

Não decide por ele e não mexe em campanha nenhuma: **só lê**. Ativar, pausar ou
mudar orçamentos é decisão dele, e faz-se com a skill `meta-ads`.

Também não corrige atribuição em falta para trás. O que não foi medido no
momento do clique não se recupera depois.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
