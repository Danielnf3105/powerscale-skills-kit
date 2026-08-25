---
name: pagina-de-oferta
description: >
  Produz a página de venda de uma oferta (a tua ou a de um cliente teu):
  single-file HTML premium na marca de quem vende, com as secções provadas
  (hero, problema, método com acrónimo, processo passo a passo, mecanismo
  único, ferramentas, prova real, plano, fit, calculadora de valor,
  investimento, CTA, FAQ), versão sem preço (proposta) e versão com preço.
  Usar quando pedes "monta a página da oferta do cliente X", "cria a página
  de proposta", "uma página para eu mostrar na call", "página de vendas do
  serviço Y". REGRA: só construir depois de ter a informação toda do gate de
  intake (ver abaixo); se faltar, perguntar primeiro. Não usar para copy
  solta (`copy-resposta-direta`) nem para a página que aparece depois do
  compromisso (`thank-you-page`).
version: 1.0.0
author: kit
---

# Página de Oferta (proposta ou página de venda)

## Para que serve

Uma página única que explica uma oferta melhor do que qualquer PDF: o que é,
para quem, como funciona, quanto vale e o que acontece a seguir. Serve para
dois momentos:

- **Proposta pós-reunião**, mostrada no ecrã ou enviada a seguir ao discovery.
  É o caso mais frequente e o que converte melhor. CTA = avançar.
- **Página de venda fria**, para quem chega sem falar com ninguém. Precisa de
  mais prova, mais objeções respondidas e um CTA de marcação.

A página vai sempre na **marca de quem vende**. Se estás a vender a oferta de
um cliente, a página é dele: cores dele, voz dele, logo dele. Tu ficas atrás.

Skills irmãs: a copy sai da `copy-resposta-direta`, o movimento da
`motion-framer`, o acabamento visual da `craft` e da
`web-interface-guidelines`, a voz da `voz-de-marca`.

---

## REGRA DE OURO: o gate de intake (não avançar sem isto)

> NÃO comeces a construir enquanto não tiveres o **essencial** abaixo.
> Para cada item em falta, **pergunta primeiro**. Nos itens marcados
> *(posso propor)*, propõe tu e espera que validem. Confirma o gate,
> depois constrói.

**A. Marca**
- [ ] Nome de quem vende (tu ou o cliente).
- [ ] Cores (HEX), ou **preto e branco**, ou *(posso propor)* uma identidade.
- [ ] Logo (ficheiro), ou autorização para desenhar um wordmark.
- [ ] Tipografia (ou uso o par padrão: Inter + Instrument Serif itálico).
- [ ] Material de voz e prova: site, Instagram, Drive, deck, PDF.

**B. A oferta**
- [ ] O que se vende, em concreto.
- [ ] ICP: a quem vende e a **economia dele** (ticket médio, ou como se calcula:
      nº de unidades × preço, valor de um cliente, margem por venda).
- [ ] Entregáveis: o que está incluído, o que não está.
- [ ] O **mecanismo único**: porque é que isto funciona e a alternativa não.

**C. O método**
- [ ] Já existe método com nome? Se não, dá-me os **passos de como funciona**
      e *(posso propor)* um acrónimo.

**D. Contexto**
- [ ] Landing fria ou proposta pós-reunião? Muda o CTA e metade da copy.

**E. Preço**
- [ ] Modelo (avença, fee de arranque, % por venda, pacote), *(posso propor)*.
- [ ] Mostra preço? Padrão: **versão principal sem preço** + **versão com preço**
      à parte, para mostrares só quando quiseres.
- [ ] Para a calculadora: a economia do cliente + a taxa de conversão de
      referência + a percentagem que fica para ti.

**F. Prova**
- [ ] Casos, prints, números, logos.
- [ ] **Autorização** para usar nomes e marcas publicamente (ver honestidade).

**G. Ferramentas**
- [ ] Que ferramentas entram na entrega (para a secção do stack).

Com A (nome e marca), B (oferta e ICP), C (método), D (contexto) e E (preço),
avança. F e G enriquecem mas não bloqueiam um primeiro rascunho.

---

## O que construir

1. **Pasta do trabalho** em `clientes/<cliente>/pagina/`, com `index.html` e
   `assets/`. Sem espaços no nome da pasta se houver deploy.
2. **Página em single-file HTML**, na marca de quem vende, seguindo o blueprint
   de secções e o sistema de design em `references/page-blueprint.md`.
3. **Duas versões**: `oferta.html` (principal, sem preço) e
   `oferta-com-preco.html` (mais a secção de investimento e a calculadora).
4. **Prova**, se houver deck ou PDF: extrair, tratar privacidade, parede de
   logos e galeria com lightbox. Ver `references/proof-assets-deploy.md`.
5. **Verificar** no browser: consola limpa, IDs únicos, a matemática das
   calculadoras certa, **0 em-dash**, e ler a página inteira no telemóvel.
6. **Publicar**, se for pedido (Vercel, Netlify ou o alojamento do cliente).
7. **Documentar**: um README ao lado com as decisões, os rascunhos por validar
   e os pendentes de quem tem de aprovar.

---

## Regras invioláveis

- **pt-PT (AO90). ZERO em-dash.** O travessão U+2014 nunca aparece em ficheiro
  nenhum. Confirmar com uma procura pelo caractere antes de entregar.
- **Marca de quem vende.** Se a página é do cliente, o teu nome não aparece.
- **Tudo é rascunho** até quem vende validar: copy, método, preço, prova.
- **prefers-reduced-motion** sempre respeitado.
- Nada de preço inventado a fingir que é real. Preço por confirmar diz-se.

---

## Checklist de honestidade e privacidade (sinalizar sempre)

A prova é a zona de maior risco de uma página destas. Antes de publicar:

1. **Reunião marcada não é venda fechada.** Não deixar a página implicar
   resultados que não aconteceram.
2. **Faturação grande de um cliente é a dimensão dele, não a tua receita.**
   Dizê-lo à letra na página.
3. **Autorização para nomear marcas.** Mostrar numa reunião não é publicar.
4. **RGPD**: nada de nomes, emails ou telefones de pessoas reais nos prints.
   Censurar, e oferecer recortar.
5. **Fugas entre contas**: procurar nos prints emails ou domínios de outro
   cliente teu. Excluir e avisar.
6. **A stack tem de ser a real.** Não inventar ferramentas para soar melhor.

---

## Quando NÃO usar

- Escrever só a copy de uma página → `copy-resposta-direta`.
- A página que aparece depois de a pessoa se comprometer → `thank-you-page`.
- Recolher a oferta de um parceiro antes de haver página → faz primeiro o
  documento de intake (o gate acima serve de guião de perguntas).
- Um deck em PowerPoint em vez de página → skill `pptx`.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
