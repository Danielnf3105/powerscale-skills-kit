# Blueprint da página de oferta de parceiro

Estrutura, sistema de design e padrões de copy provados numa página real de
oferta de parceiro. Copiar o esqueleto da melhor página de oferta que já
construíste e adaptar.

## Sistema de design (single-file)

- **Single-file HTML**, autossuficiente. Google Fonts via `<link>` (Inter +
  Instrument Serif itálico), ou as fontes do parceiro.
- **CSS variables** para cor. Se a marca é P&B: fundo `#09090A`, texto `#F6F6F7`,
  cinza `#9A9DA3`, cartões `#141518`, bordas `rgba(255,255,255,.10)`, accent =
  branco. Se a marca tem cor: accent = cor primária do parceiro (gerar variante
  por troca de strings, como `make-orange-variants.py` na landing-b2b).
- **Tipografia**: sans (Inter) no corpo; **serif itálico (Instrument Serif)**
  nas palavras-accent dos títulos (`<span class="it">`).
- **Motion premium** (`motion-framer`, vanilla): fundo animado coerente com a
  marca (ondas se o método usa a metáfora do mar, aurora para outras), reveals por IntersectionObserver,
  count-up, draw-on-scroll dos diagramas SVG, botões magnéticos, hover-lift,
  barra de progresso de scroll. Tudo com `try/catch` por módulo e
  `prefers-reduced-motion` a desligar o decorativo.
- **Grafismos para explicar conceitos** (quase sempre valem a pena): SVG
  à medida + mock-ups tipo screenshot em HTML/CSS. Não usar imagens AI genéricas.

## Secções (ordem provada)

1. **Nav**, logo do parceiro (glifo + nome). Minimal; opcionalmente CTA "Marcar reunião".
2. **Hero**, eyebrow (= método), `<h1>` grande com palavra-accent em serif itálico,
   subheadline, 2 CTAs (primário + "Ver o método"), linha de meta (3 provas rápidas).
   Fundo animado da marca.
3. **Problema**, 3 a 5 "dores" do ICP em cartões numerados.
4. **Viragem / shift**, uma frase que introduz a metáfora do método ("Não precisas de X. Precisas de Y.").
5. **Método (acrónimo)**, as letras em serif, cada uma com um mini-grafismo SVG +
   uma frase. Se o nome tiver metáfora (onda), incluir um **diagrama-mestre** SVG
   animado (ex.: swell-to-break). Mapear cada letra a uma fase real.
6. **Processo (passo-a-passo)**, 5 passos, cada um com um **mock-up tipo screenshot
   P&B** (ficha de dados estilo Apollo → email → conversa LinkedIn → pipeline CRM →
   reunião/calendário). Dados inventados, sem clientes reais. Responde a "mostra os passos que vão ser executados".
7. **Mecanismo único**, o que os diferencia + **"porque é que não fazes isto sozinho?"**
   (4 cartões). Se houver automação/IA, um **terminal animado** a mostrá-la (ex.:
   `claude scrape ... → N empresas em 4 min vs 3 dias`). ⚠️ reconciliar com as ferramentas reais.
8. **Entrega (done-for-you)**, lista de entregáveis (~10) + aside "tu não tocas em nada".
9. **CRM**, grafismo (canais → CRM/pipeline → reunião) + capacidades (6) + **"o que vês em
   cada lead"** (campos + score de qualificação por IA) + contraste **Sem CRM vs Com o teu CRM**.
10. **Ferramentas (O stack)**, grelha de cartões com o stack real + nota **"todos os custos incluídos"**.
11. **Prova real**, stats agregados com count-up + parede de logos + **galeria de prints
    com lightbox** (ver `proof-assets-deploy.md`). Disclaimer honesto.
12. **Plano**, 5 fases (Setup → Arranque → Otimização → Velocidade de cruzeiro → Consolidação).
13. **Fit**, "é para ti se" vs "não é para ti se".
14. **Valor (calculadora ao vivo)**, sliders da economia do cliente → **vale cada reunião**
    + pipeline. Na versão **com preço**, +2 outputs: **A tua fee (X%)** e **Ficas com (resto)**.
15. **Investimento**, **só na versão com preço**: o modelo de preço (cartões + exemplo).
16. **CTA band**, reformulado para o contexto (proposta pós-discovery: "A pergunta não é se vale a pena, é quando começamos" → "Quero avançar").
17. **FAQ**, 5 objeções.
18. **Footer**, marca de quem vende + ano.

## Calculadora de valor / fee (mecânica)

Padrão Hormozi: construir valor até "se fosse grátis avançava 100%", só depois o preço.

- **Inputs (sliders)**: valor médio de um cliente (ou unidades × preço), **taxa de
  fecho** (benchmark conservador, ex. 10%), reuniões/mês.
- **Output de valor** (nas duas versões): `vale cada reunião = ticket × taxa de fecho`;
  pipeline/mês; pipeline/ano. Formatar com `toLocaleString('pt-PT')` + `€`.
- **Output de fee (só versão com preço)**: `fee = vale_reunião × %fee` (ex. 30%);
  `ficas com = vale_reunião × (1 − %fee)`. Mostrar lado a lado ("A tua fee (30%)" / "Ficas com (70%)").
- **Exemplo de cálculo a confirmar** (caso real <cliente> / <Cliente do parceiro>): frota 100
  carros × 30€ = 3.000€/cliente; 10% fecho → reunião vale 300€; fee 30% = 90€; cliente fica 210€.
- O IntersectionObserver pode não disparar no preview (viewport instável); a lógica
  é boa, testar a matemática disparando `input` nos sliders por DOM.

## Padrões de copy (resposta direta, pt-PT)

- Headline = promessa concreta com número quando possível; palavra-accent em serif itálico.
- Problema = dores específicas e reconhecíveis do ICP, não genéricas.
- "Porque não sozinho" = expertise + infraestrutura técnica + sistema (não tarefas soltas) + mecanismo que não se copia.
- CTA pós-discovery = avançar/arranque, não "marcar diagnóstico" (esse já aconteceu).
- Generalizar a copy para o ICP do parceiro (tirar exemplos demasiado específicos de um único cliente).
- Marcar tudo como rascunho até validação.
