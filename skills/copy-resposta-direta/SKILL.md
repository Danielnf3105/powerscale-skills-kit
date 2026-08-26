---
name: copy-resposta-direta
description: >
  Escreve copy de resposta direta para funis de webinar, páginas de registo,
  sequências de email, anúncios e criativos, guiões de webinar, páginas de venda
  e mensagens de SMS/WhatsApp, aplicando SEMPRE em conjunto duas exigências:
  os frameworks clássicos de direct response E a voz de marca do cliente. Usar
  sempre que o utilizador pede para "escrever copy", "escrever uma headline",
  "criar uma landing/página de registo", "escrever os emails do funil", "copy
  do webinar", "guião do webinar", "página de vendas", "anúncio para o Meta",
  "criativo", "mensagem de WhatsApp para o grupo", "SMS do funil", ou para
  rever, melhorar ou reescrever copy existente. Também despoleta com "isto não
  converte", "torna isto mais persuasivo", "isto não soa ao cliente", "copy
  para o cliente X". Não usar para gerar guidelines de marca de raiz (usar
  brand-voice:generate-guidelines) nem para descobrir materiais de marca (usar
  brand-voice:discover-brand), esta skill consome essas guidelines, não as cria.
---

# Copy de Resposta Direta (com a voz do cliente)

Esta skill escreve copy que converte: páginas, emails, anúncios, guiões,
mensagens de DM e WhatsApp. Une duas coisas que na maioria das skills andam
separadas: os frameworks clássicos de resposta direta e a voz de marca de quem
assina a peça.

Quando escreves para um cliente, quem fala é o cliente, não tu. Por isso esta
skill tem uma regra inegociável.

## A regra de ouro: duas exigências, nunca uma só

Cada peça de copy tem de cumprir **as duas** exigências ao mesmo tempo:

1. **Converte**, usa estrutura e psicologia de resposta direta. Headline que
   pára o scroll, dor quantificada, transformação clara, provas específicas,
   loops de curiosidade, CTA orientado ao benefício.
2. **Soa ao cliente**, respeita a voz de marca dele. Vocabulário, tom, registo,
   personalidade, o que o cliente diria e o que nunca diria.

Uma peça que converte mas não soa ao cliente **falha**, quebra a confiança de
quem te contratou. Uma peça perfeitamente on-brand mas que não
converte **falha** na mesma, não cumpre o trabalho. Nunca entregar copy que
só cumpra uma das duas.

### Como é que as duas encaixam

Não são rivais. Têm papéis diferentes:

- **Resposta direta = o esqueleto.** Decide *o que* vai em cada sítio, por que
  ordem, que gatilhos psicológicos, a sequência de consciência do leitor.
- **Voz de marca = a pele.** Decide *como* soa, vocabulário, tom, registo,
  personalidade, o que o cliente diria.

Na prática raramente colidem. Quando colidem mesmo, a voz de marca ganha na
*expressão* e a tua tarefa é encontrar uma forma on-brand de atingir o mesmo
objetivo persuasivo. Ver "Quando há conflito" mais abaixo.

## Passo 1: Carregar a voz do cliente (obrigatório, antes de escrever)

Não escrevas uma linha de copy sem teres a voz do cliente. Procura por esta
ordem e pára assim que encontrares:

1. **Contexto da sessão**, se a voz já foi trabalhada nesta conversa, usa-a
   diretamente. É a mais fresca.
2. **Voice Bible do cliente**, procura `clientes/<cliente>/voz.md` (o ficheiro
   que a skill `voz-de-marca` produz). É a fonte oficial.
3. **Material em bruto do cliente**, posts, emails antigos, transcrições de
   calls, DMs dele. Serve para escrever, mas assinala que a voz ainda não está
   codificada e propõe correr `/voz-de-marca` para a fixar.
4. **Perguntar**, se não encontraste nada, **não inventes uma voz**. Diz:
   "Não tenho a voz deste cliente. Posso correr `/voz-de-marca` para a extrair
   de material que me deres (posts, calls, emails), ou escrever a partir de 3
   exemplos que me coles aqui."

   Espera pela resposta antes de continuar. Copy sem voz definida é copy
   genérico, e copy genérico não se distingue do da concorrência.

**Língua de saída.** Deteta a língua a partir dos materiais do cliente (pt-PT,
pt-BR, inglês, espanhol...). Escreve o copy na língua do cliente, não na língua
do pedido. Se for ambíguo, pergunta.

## Passo 2: Enquadrar o pedido

Antes de escrever, identifica:

- **Formato**, página de registo, sequência de email, anúncio, guião do
  webinar, página de vendas, mensagem de WhatsApp/SMS. Cada formato tem uma
  estrutura própria em `references/formatos-de-funil.md`.
- **Nível de consciência do leitor**, Os 5 níveis de Schwartz (Inconsciente →
  Mais Consciente). Determinam o ângulo e o comprimento. Ver
  `references/frameworks-classicos.md`. Quanto menos consciente, mais longo e
  mais educativo o copy.
- **Público-alvo**, cargo, setor, momento do funil em que está.
- **A oferta**, o que se está a vender e qual é a transformação.
- **A única ação desejada**, cada peça pede *uma* coisa.

Se faltar informação crítica (a oferta, o público, a fase do funil), pergunta
em vez de assumir.

## Passo 3: Construir o esqueleto de resposta direta

Vai a `references/formatos-de-funil.md` buscar a estrutura do formato pedido.
Aplica os princípios centrais, estão destilados aqui para usares sem teres
sempre de abrir as referências:

- **Escreve como quem explica a um amigo inteligente, cético mas curioso.** Nem
  equipa de marketing, nem guru, nem robô. Uma pessoa que percebeu algo e quer
  partilhar.
- **Cada afirmação ancorada num específico.** Um número, uma prova, um detalhe.
  "Reduz 99,6% das bactérias" ganha a "reduz quase todas as bactérias".
- **Torna a transformação visceral.** Para cada característica, pergunta "e
  então?" até chegares ao fundo emocional ou financeiro. Não "poupa 4 horas" mas
  "fecha o portátil às 17h em vez das 21h". (A cadeia "E então?" está em
  `references/frameworks-classicos.md`.)
- **A headline faz 80% do trabalho.** Escreve sempre várias (5+). Onde a
  headline é central, página de registo, anúncio, subject lines, não entregues
  só a escolhida: apresenta a tua recomendação **e mais 2-3 alternativas
  fortes**, marcando a recomendada. Quem aprova a peça decide melhor
  com opções à frente. As fórmulas estão em `references/headlines-e-hooks.md`.
- **A primeira frase só tem um trabalho:** levar à segunda. Curta, sem atrito.
- **Quantifica a dor.** Problemas vagos parecem esmagadores; problemas com
  número parecem resolúveis. Faz as contas da dor.
- **Abre loops de curiosidade** para puxar o leitor para a frente, e **fecha
  todos os loops que abres**. Loop aberto e não fechado destrói confiança.
- **Slippery slide:** cada elemento existe para fazer ler o seguinte.
- **Ritmo:** alterna frases curtas de impacto com frases mais longas que
  respiram. Copy só de fragmentos curtos cansa; copy só de parágrafos longos
  afoga.
- **CTA descreve o benefício, não o comando.** "Garantir o meu lugar" ganha a
  "Submeter". Por baixo, redutores de atrito (prova social, rapidez, risco zero).

## Passo 4: Escrever através do filtro da voz

Agora escreve a peça, mas cada linha passa pelo filtro da voz de marca:

- Aplica os atributos "Somos / Não somos" das guidelines.
- Usa a terminologia aprovada; rejeita a terminologia proibida.
- Ajusta o tom ao contexto pela matriz tom-por-contexto das guidelines
  (formalidade, energia, profundidade técnica).
- Espelha a qualidade e o estilo dos exemplos das guidelines.

**Atenção ao registo "internet-native".** O material fonte de resposta direta
empurra muito para marcadores de criador online: transparência de receita
("$45k/mês"), emojis, gíria de nicho, confissões casuais de fundador. **Isto não
é universal**, é o registo certo para *alguns* clientes (infoprodutores,
agências jovens) e o registo errado para outros (seguradoras, credit companies,
marcas premium ou institucionais). Mantém sempre o motor de persuasão; troca o
"disfarce" pelo registo do cliente. Quando a voz do cliente é reservada ou
institucional, ganha-se credibilidade com casos de estudo, dados de terceiros e
certificações, não com fundadores a exibir receitas. Detalhe em
`references/anti-ia-e-voz.md`.

## Passo 5: Validar contra as duas exigências

Antes de entregar, corre as duas listas. Se alguma resposta for "não", reescreve
essa parte.

**Teste de resposta direta:**
1. Soa a alguém a falar, ou a alguém "a fazer copy"?
2. Cada afirmação está apoiada num número ou prova específica?
3. O ritmo alterna (momentos de soco, momentos de respiração)?
4. É sobre o LEITOR (a transformação dele) ou sobre o produto?
5. Há loops abertos a puxar para a frente, e todos fecham?
6. A headline pára o scroll? Escolheste-a entre várias?
7. Termina com momento (CTA claro orientado ao benefício)?

**Teste de voz de marca:**
1. Os atributos "Somos / Não somos" estão respeitados ao longo de toda a peça?
2. Não há terminologia proibida? Usaste a terminologia aprovada?
3. O tom está calibrado para este formato e este público?
4. Um leitor que conheça o cliente reconhecê-lo-ia nesta peça?
5. O registo internet-native foi importado só se for mesmo o registo do cliente?

Por fim, relê a peça à procura de gralhas, com atenção especial a saudações,
assinaturas e nomes próprios, onde os erros passam despercebidos (uma despedida
mal escrita numa marca sóbria custa mais credibilidade do que parece).

Depois explica em poucas linhas as decisões-chave: que framework estruturou a
peça, que escolhas de voz fizeste, e onde (se houver) adaptaste alguma coisa.

## Quando há conflito entre converter e a voz

Acontece. Exemplo típico: a resposta direta sugere headline com número de
receita chocante, mas a voz do cliente é sóbria e nunca divulga números
internos. Ou a resposta direta quer emojis e a marca é formal.

Quando o pedido ou a técnica colide com a voz de marca:

1. **Explica o conflito** com clareza, o que a técnica quer, o que a voz não
   permite.
2. **Dá uma recomendação.** Por defeito: a voz de marca ganha na expressão; o
   objetivo persuasivo mantém-se, muda a forma de o atingir. Em vez do número de
   receita, usa um caso de estudo concreto do cliente. Em vez do emoji, usa uma
   frase curta de impacto.
3. **Oferece opções:** cumprir a voz à risca, adaptar com explicação, ou (se o
   utilizador insistir) sobrepor-se à voz assumindo o risco.

Nunca sacrifiques o cliente soar a ele próprio por causa de uma linha
inteligente. Uma headline brilhante na voz errada é uma headline má.

## Consciência de questões em aberto

Se as guidelines de marca tiverem uma secção "Questões em Aberto" (decisões de
posicionamento ainda por resolver), verifica se o copy toca alguma. Se tocar,
aplica a recomendação registada e assinala-o ao utilizador.

## Ficheiros de referência

Lê o ficheiro relevante quando precisares, não precisas de ter tudo em contexto
ao mesmo tempo.

- **`references/frameworks-classicos.md`**, Os 5 níveis de consciência de
  Schwartz, e os princípios de Hopkins, Ogilvy, Halbert, Caples, Sugarman e
  Collier. A cadeia "E então?", a quantificação da dor e o slippery slide. Lê
  para escolher o ângulo e estruturar a persuasão.
- **`references/headlines-e-hooks.md`**, Fórmulas de headline, linhas de
  abertura e técnicas de loop de curiosidade, com exemplos. Lê sempre que
  escreveres headlines, subject lines ou aberturas.
- **`references/formatos-de-funil.md`**, A estrutura, secção a secção, de cada
  formato do funil: página de registo, sequência de email, anúncios, guião do
  webinar, página de vendas e mensagens de WhatsApp/SMS. Lê para saber o que vai
  em cada peça.
- **`references/anti-ia-e-voz.md`**, Os "AI tells" a evitar (palavras, frases e
  estruturas que denunciam texto gerado) e como a voz de marca decide quando
  importar, ou não, os marcadores internet-native. Lê antes de validar.

---

## Copy de anúncios: lê a estratégia primeiro

Antes de escrever a primeira linha de um anúncio, **`estrategia-criativos`**.
Lá está o que decide se a copy tem hipótese: o conceito (persona, ângulo,
oferta), os ingredientes de um ângulo que dura, as três camadas do hook
(visual, áudio, copy), e a transição do hook para o corpo sem degrau.

Duas coisas de lá que mudam a forma de escrever:

- **O hook vale 80% do criativo.** Quinze hooks e dois corpos ganham a dois
  hooks e cinco corpos. Escreve os hooks em série, não um de cada vez.
- **Agitar a dor dura mais do que chamar a persona.** "Tens dor nas costas e
  passas o dia sentado" aguenta meses; "És empresário e passas o dia sentado"
  queima em semanas.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
