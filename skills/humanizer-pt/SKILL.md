---
name: humanizer-pt
description: |
  Camada PT-PT do humanizer. Apanha os sinais de escrita de IA em português de Portugal
  (vocabulário inflacionado, gerúndio de remate, paralelismos negativos, regra de três,
  aforismos, conclusões animadoras, aspas curvas, contaminação PT-BR) e diz o que escrever
  em vez disso. Usar SEMPRE que se escreve ou revê texto em português: respostas de chat,
  copy de páginas e anúncios, emails, propostas, contratos, decks, notas internas e
  mensagens para clientes. Correr em conjunto com a skill humanizer (inglês) quando o
  texto for em inglês. Não usar para inventar copy de raiz (isso é a direct-response-copy);
  esta skill entra no fim, em cima da copy já escrita.
license: MIT
metadata:
  version: "1.0"
---

<!-- humanizer-pt: ignorar (este ficheiro é o catálogo dos padrões, cita-os de propósito) -->

# Humanizer PT-PT

A skill `humanizer` (blader/humanizer, instalada ao lado desta) lista 33 padrões de escrita
de IA. Vale toda, mas o vocabulário e os exemplos são ingleses. Este ficheiro é a parte que
falta: os mesmos padrões como aparecem em português de Portugal, mais a regra de quando
parar de cortar para não estragar copy de resposta direta.

Ordem de trabalho: escrever com a skill de copy → passar este filtro → só depois entregar.

## A regra de ouro

O leitor não deteta IA pelas palavras. Deteta pela **simetria**. Frases do mesmo comprimento,
listas sempre de três, cada parágrafo com a mesma forma, cada secção a fechar com uma
sentença bonita. Um humano é irregular: escreve uma frase de 4 palavras seguida de uma de 30,
dá um exemplo esquisito, corta a meio, repete a mesma palavra porque é a palavra certa.

Se a alternativa for entre soar polido e soar a pessoa, escolhe a pessoa.

## 1. Vocabulário que denuncia

Coluna da esquerda: fora. Coluna da direita: o que um português escreve.

| Sinal de IA | Escreve antes |
|---|---|
| crucial, fundamental, essencial, vital, pivotal | (corta o adjetivo, ou diz porquê: "sem isto não há reuniões") |
| robusto, poderoso, sólido, completo, abrangente | o que faz, em concreto |
| inovador, revolucionário, transformador, disruptivo | (corta) |
| vibrante, dinâmico, cativante, envolvente | (corta) |
| alavancar, potenciar, impulsionar, elevar, desbloquear, maximizar | usar, aumentar, abrir, subir |
| otimizar, escalar (quando não há número) | o número que muda |
| panorama, paisagem, cenário, ecossistema, universo | o mercado, o negócio, o funil |
| jornada (do cliente) | o caminho, o percurso, os passos |
| mergulhar, aprofundar, explorar (como anúncio) | (faz, não anuncies) |
| um testemunho de, um marco, no cerne de, a espinha dorsal | (corta) |
| em constante evolução, cada vez mais, nos dias de hoje, no mundo atual | (corta a moldura, começa na frase a seguir) |
| soluções, estratégias, ferramentas (genérico, plural vago) | a coisa concreta: a landing, a sequência, os 4 anúncios |
| resultados (sem número) | o número |

Frases-muleta a cortar inteiras: "é importante notar que", "vale a pena destacar", "em suma",
"em conclusão", "por fim mas não menos importante", "ao longo dos anos", "sem esforço",
"num piscar de olhos", "de forma eficaz", "de forma consistente", "de forma estratégica".

## 2. Estruturas que denunciam

**Gerúndio de remate.** O equivalente português do "-ing" do §3 da humanizer. Cola-se no fim
da frase para fingir profundidade.

> Montamos a sequência de emails, garantindo que nenhuma lead fica sem resposta e
> aumentando a taxa de conversão.

> Montamos a sequência de emails. Nenhuma lead fica sem resposta.

Suspeitos: garantindo, permitindo, proporcionando, oferecendo, contribuindo, refletindo,
destacando, sublinhando, evidenciando, criando, gerando, aumentando, melhorando.

**Paralelismo negativo.** "Não é X, é Y." É a construção mais viciante dos modelos e a mais
gasta na copy portuguesa.

> Não é só um funil, é uma máquina de vendas.

> O funil trata do que tu não consegues tratar: responder às 200 leads que entraram ontem.

Variantes da mesma família: "mais do que X, é Y", "não se trata de X, trata-se de Y",
"não precisas de X. Precisas de Y."

**Negação em cauda.** Fragmento colado no fim, sem verbo. "Sem adivinhar." "Sem perder tempo."
"Zero fricção." Escreve a frase inteira ou corta.

**Regra de três.** Três adjetivos, três bullets, três benefícios. Uma vez é ritmo, três vezes
na mesma página é máquina. Quando tiveres três, pergunta se dois chegam ou se o terceiro é o
único verdadeiro.

**Aforismo.** "X é a moeda de Y", "X é a linguagem de Y", "o problema não é o tráfego, é a
estrutura" dito como sentença universal. Se a frase serve para qualquer negócio, não diz nada
sobre este.

**Staccato dramático.** Fila de frases de três palavras a construir tensão. Uma frase curta
para bater é boa. Quatro seguidas é um trailer.

> Depois veio o lançamento. Sem estrutura. Sem follow-up. Sem plano.

> O lançamento correu bem e depois ninguém respondeu às leads durante duas semanas.

**Perguntas retóricas em cadeia.** "E se te dissesse que...?", "Já pensaste no que acontece
quando...?" Uma pergunta a abrir é copy. Três é um chatbot a aquecer.

**Aberturas de intimidade falsa.** "A verdade é que", "Sejamos honestos", "Olha", "Vou ser
direto contigo", "Aqui está o que precisas de saber", "Vamos por partes", "Imagina isto".
Quem é direto diz a coisa.

**Conclusão animadora.** "O futuro é promissor." "A escolha é tua." "Agora é contigo."
Acaba no último facto concreto. Numa página, o último elemento é o botão, não uma frase de
despedida.

**Cabeçalho seguido de eco.** Título "Estrutura" e a seguir a linha "A estrutura é o que
falta." Corta a linha, entra no conteúdo.

## 3. Pontuação e formatação

- Travessão (—) e meia-risca (–): zero. É o tell número um e é regra da casa.
- Aspas curvas (" " ' '): trocar por aspas direitas ("). Aparecem sozinhas quando o texto passa
  por Word, Docs ou macOS, por isso não são prova por si só, mas num HTML escrito por mim são.
- Emojis a decorar títulos e bullets: fora (exceto onde a marca já os usa, ex. os prefixos de
  emoji das pastas do ClickUp).
- Negrito mecânico a cada duas linhas: fora. Negrito é para o que a pessoa lê se só ler uma
  coisa.
- Listas com cabeçalho a negrito e dois pontos ("**Rapidez:** o sistema é rápido") : ou vira
  frase, ou o cabeçalho ganha conteúdo próprio.
- Títulos em Title Case ("Como Montamos O Teu Funil"): em português só a primeira palavra e os
  nomes próprios levam maiúscula.

## 4. PT-PT, não PT-BR

A contaminação brasileira lê-se como tradução automática, logo lê-se como IA. A tabela do
CLAUDE.md global manda (ecrã, ficheiro, telemóvel, utilizador, equipa, aceder, gestão).
Mais dois que passam despercebidos:

- Tratamento: "tu"/"a tua equipa", nunca "você" (a não ser que a marca do cliente use "você",
  como material antigo já corrigido de propósito).
- Gerúndio contínuo: "está a montar", nunca "está montando".

## 5. O que NÃO se corta

Esta skill é um filtro, não um esterilizador. Copy de resposta direta usa de propósito coisas
que a lista acima proíbe. Fica tudo isto:

- **Repetição da palavra âncora.** Se a página é sobre estrutura, "estrutura" repete-se. A
  variação elegante de sinónimos é que é sinal de IA (§11 da humanizer), não a repetição.
- **Segunda pessoa e imperativo.** "Marca a auditoria." É copy, não é robô.
- **Números específicos e feios.** 12.500€ com 2.000€ de ads. 6,2x. 47 leads. Quanto mais
  específico, mais humano. Nunca arredondar para parecer limpo.
- **A voz do cliente à letra.** Se a lead escreveu "não existe uma timeline", isso entra tal
  e qual, mesmo que soe estranho. Frase de call gravada vale mais que qualquer reescrita.
- **Objeções ditas pelo nome.** "Vais achar que é caro."
- **Frases curtas.** Curto é bom e é teu. O que se corta é a fila de
  fragmentos sem sujeito a fingir suspense.
- **Uma pergunta de abertura**, um aforismo por página se for mesmo bom, um trio quando o
  trio é real.

E a regra que não se dobra: **nunca inventar factos para soar mais humano.** Um caso, um
número ou um nome que não venha do cliente não entra. Se a frase precisa de um detalhe real
para funcionar, pede o detalhe ou escreve a versão sem ele.

## 6. Como aplicar, por tipo de peça

**Chat contigo.** Sem invocar nada, sem draft e sem auditoria. Escrever direto e
verificar mentalmente as três armadilhas mais frequentes: paralelismo negativo, gerúndio de
remate, conclusão animadora. Resposta a uma pergunta simples é uma frase.

**Copy de cliente (página, anúncio, email, deck, proposta).** Escrever, passar o filtro,
correr o detetor da secção 7 e só depois entregar. Se a peça for longa (página inteira,
sequência completa), invocar a skill `humanizer` em modo embedded sobre o texto final.

**Documentos oficiais (contratos, briefings, planos de negócio).** Aqui o registo neutro e
seco é o registo humano correto. Não injetar voz nem opinião. O que se caça é só o
vocabulário inflacionado e as frases-muleta.

**Notas internas.** Mesmo filtro do chat. Vale mais uma nota irregular e específica do que
uma nota bem arrumada e vazia.

## 7. Detetor

`deteta.py` sinaliza ocorrências num ficheiro ou pasta. Só lê e reporta, nunca substitui
(transformação cega sobre texto português parte acentos, é regra do CLAUDE.md).

```bash
python3 ~/.claude/skills/humanizer-pt/deteta.py caminho/para/pagina.html
```

Saída: categoria, linha, trecho. Um resultado não é um erro, é um sítio para olhar. O que
manda é o julgamento: cluster de sinais é confissão, sinal isolado costuma ser prosa
legítima.

Antes de dar uma peça por terminada: 0 travessões, 0 aspas curvas, 0 "você" (salvo marca do
cliente), e a lista de vocabulário revista uma a uma.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
