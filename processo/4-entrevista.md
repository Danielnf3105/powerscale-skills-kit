# Fase 4: a entrevista

**Objetivo:** saber quem a pessoa é, onde publica, como escreve, e ter na mão
o material com que se vai trabalhar.

**Pré-condição:** fase 3 feita ou saltada.

Esta é a fase que decide se o kit vale alguma coisa. Uma instalação sem esta
fase deixa a pessoa com um assistente genérico que escreve como uma IA. Com
ela, fica
com um que escreve como ele.

## Como se conduz

- **Uma pergunta por mensagem.** Nunca um questionário de vinte linhas.
- **Grava a seguir a cada resposta**, sempre:

  ```
  <python> ferramentas/estado.py --responder pessoa.nome="Samuel Lowe"
  <python> ferramentas/estado.py --responder 'trabalho.tipos=["copy","anúncios"]'
  ```

  É isto que faz a entrevista sobreviver a uma conversa interrompida.

- **Nunca repitas uma pergunta já respondida.** Corre `estado.py --falta` e
  pergunta só o que aparecer.
- Se retomas a meio, abre com uma linha: "já me disseste os canais e o que
  vendes; faltam-me três coisas".

---

## 1. Os canais (é a primeira, e é uma tabela)

Perguntado à solta, ele responde "Instagram e TikTok" e ficas sem os handles.
Por isso pede-se **em tabela, com o link completo de cada um**.

> **Onde vives online? Deixa o link completo, não só o nome do canal.**
>
> | Canal | Link ou @ | Quem publica | Ativo? |
> |---|---|---|---|
> | Site | | | |
> | Instagram | | | |
> | TikTok | | | |
> | YouTube | | | |
> | Facebook (página) | | | |
> | LinkedIn | | | |
> | Comunidade (Discord, Whop, grupo de WhatsApp, Telegram) | | | |
> | Podcast | | | |
> | Newsletter ou lista de email | | | |
> | Outro | | | |
>
> Se um canal existe mas está parado, escreve na mesma e marca como parado. Se
> houver mais do que um perfil no mesmo canal (o pessoal e o da marca), põe os
> dois e diz qual é o principal.

Isto não é burocracia. Os canais entram em quase tudo o que se constrói a
seguir: CTA de emails e páginas, lives, retargeting, instalação do pixel,
publicações, prova social, criativos que reaproveitam o orgânico. **E são a
matéria-prima da voz dele**, que é o passo seguinte.

Um caso real: uma live estava marcada no Instagram e o perfil não estava
registado em lado nenhum. O convite para 2.026 pessoas ficou parado à espera de
um dado que devia ter sido recolhido no primeiro dia.

```
<python> ferramentas/estado.py --responder 'canais=[{"canal":"Instagram","link":"https://instagram.com/x","quem":"ele","ativo":true}]'
```

---

## 2. A voz dele (a parte que o resto do kit precisa)

**Esta é a razão pela qual a fase existe.** Tudo o que ele escrever a partir de
agora sai assinado por ele. Se soar a IA, não presta, e ele reescreve tudo à
mão, que é o mesmo que não ter kit nenhum.

Uma voz não se inventa nem se descreve com adjetivos. **Extrai-se de material
real e prova-se com citações.** "Tom profissional mas próximo" cabe em qualquer
marca do mundo, logo não descreve nenhuma.

Vai buscar tu, aos canais que ele acabou de dar, e só depois pede o que faltar:

> Vou escrever em teu nome, por isso preciso de te ouvir primeiro. Manda-me
> três ou quatro coisas que sejam **mesmo** a tua voz:
>
> - dois ou três posts ou legendas que tenhas escrito
> - um email ou uma mensagem que tenhas mandado a um cliente
> - se tiveres, um áudio ou um vídeo teu a falar sem guião
>
> Não escolhas os mais bonitos. Escolhe os que soam mais a ti.

As fontes, por ordem de valor: **ele a falar sem guião** (áudios, lives,
podcasts, calls) vale mais do que o que ele escreveu com cuidado; o que ele
escreveu vale mais do que o que outra pessoa escreveu por ele; e o que ele
*diz* que a voz dele é vale pouco sozinho, serve para confirmar.

Com o material na mão, corre a skill **`voz-de-marca`** e escreve o Voice Bible
dele em `<pasta de trabalho>/meu/voz.md`: regra de ouro, leis com **citações à
letra**, léxico do que ele usa e do que nunca diz. Uma secção sem citação real
fica marcada como rascunho.

```
<python> ferramentas/estado.py --responder voz.ficheiro="meu/voz.md"
<python> ferramentas/estado.py --responder voz.regra_de_ouro="Frases curtas. Diz o número antes do argumento."
<python> ferramentas/estado.py --responder 'voz.fontes=["8 posts LinkedIn","2 emails","1 áudio de 4 min"]'
```

**Não avances sem isto.** Se ele não tiver material nenhum (canal novo, ainda
não publicou), escreve o que der com o que houver, marca `voz.regra_de_ouro`
como rascunho e diz-lhe que a voz se afina na primeira peça que ele corrigir.

---

## 3. Os ficheiros (obrigatório, e é onde quase toda a gente encolhe)

O kit trabalha com o que lhe derem. Uma pessoa que entrega três ficheiros fica
com um assistente que adivinha; uma que entrega trinta fica com um que sabe.

**Pede tudo, de uma vez, e pede em excesso.** É mais barato receber material a
mais do que descobrir a meio de uma peça que falta o essencial.

> Vou pedir-te para descarregares umas coisas. Parece muito, mas é uma vez só, e
> é o que faz a diferença entre eu adivinhar e eu saber. Manda tudo em bruto,
> não filtres nem organizes: eu trato disso.

| O quê | Onde se descarrega | Para que serve |
|---|---|---|
| **Anúncios que já correram** | Gestor de Anúncios → Anúncios → Exportar (CSV com nome, gasto, resultados) | saber o que já funcionou e o que não, antes de propor seja o que for |
| **Os criativos em si** | as imagens e os vídeos dos anúncios, mesmo os antigos | ver os ângulos já testados e não repetir os que morreram |
| **A copy dos anúncios** | a coluna de texto principal do export, ou os prints | é voz dele já validada pelo mercado |
| **Contactos e funil** | CRM → Contactos → Exportar; e um print do funil com as etapas | perceber onde as leads encravam |
| **Páginas que já tem** | o URL basta, eu vou lá | estrutura, oferta, prova, tratamento |
| **Emails e sequências** | export da ferramenta de email, ou copiar e colar | a voz escrita dele em formato longo |
| **A oferta** | proposta, tabela de preços, deck de venda | sem isto a copy é genérica por obrigação |
| **Gravações de calls** | Zoom, Meet, Fathom, ou o telemóvel | a voz dele a falar, que vale mais do que tudo o resto |
| **Logótipo e tipografia** | os ficheiros originais, não prints | o logótipo nunca se desenha à mão |
| **Testemunhos e prova** | prints, capturas, resultados com números | a prova não se inventa, e sem ela a copy fica oca |

Regras ao receber:

- **Uma pasta só**, dentro da pasta de trabalho dele: `meu/material/`. Nada de
  ficheiros espalhados pelos Downloads.
- **Confirma o que chegou e diz o que falta**, pelo nome. "Recebi os anúncios e
  a proposta, falta-me o export dos contactos."
- **Não faças esperar por tudo.** Com metade já se começa; o resto entra depois.
  O que não se pode é começar sem nada e fingir que dá.
- Se ele disser que não tem alguma coisa, escreve isso no perfil. Um buraco
  conhecido é um buraco; um buraco esquecido é um erro à espera de acontecer.

---

## 4. As chaves

Se o trabalho dele envolver anúncios e CRM, as chaves tratam-se agora, não
quando forem precisas. **Segue `processo/chaves-e-acessos.md`**, que tem o
caminho clique a clique para o GoHighLevel e para a Meta.

Duas coisas a dizer-lhe antes de começar:

- As chaves vão para o cofre, nunca para o chat. Uma chave que passa pelo chat
  fica queimada e tem de ser trocada no serviço.
- **Se estiverem a gravar o ecrã, isto faz-se antes ou fora da gravação.**

No fim, prova que ficaram boas:

```
<python> ~/.claude/kit/ferramentas/ghl_meta.py --diagnostico
```

---

## 5. As perguntas

1. **Cartão de confirmação.** Mostra-lhe o retrato que mediste na fase 3 e pede
   correção, em vez de o fazer responder do zero:

   > Fui ver o teu site. Encontrei isto: vendes [X] a [Y], as cores são [#A] e
   > [#B], tratas as pessoas por [tu], a tipografia é [F]. O que está errado?

   Uma resposta corrige oito campos. Se a descoberta falhou, desdobra em três
   diretas: o que vendes, a quem, e que cores usa a tua marca.
   → `negocio.oferta`, `negocio.quem_compra`, `marca.*`

2. **"Como é que me chamo? E preferes respostas secas e diretas, ou com mais
   contexto à volta?"**
   → `pessoa.assistente`, `pessoa.estilo_resposta`

3. **"Que trabalho vai passar por aqui?"** Opções: mensagens a leads, copy,
   páginas, anúncios, propostas, análise de calls, outra coisa.
   → `trabalho.tipos`

4. **"Isto é só para o teu negócio, ou também trabalhas para clientes? Se sim,
   quais estão ativos hoje?"**
   → `trabalho.para_clientes`, `trabalho.clientes`

5. **"O que é que tens de despachar esta semana?"**
   A mais valiosa: é o trabalho da fase 7 e o único teste real ao kit. Insiste
   até vir uma coisa concreta, não "organizar-me melhor".
   → `trabalho.urgente`

6. **"Que ferramentas usas todos os dias? E alguma em que eu não deva mexer?"**
   Se disser um CRM (GoHighLevel, HubSpot, Close) **e** correr anúncios, diz-lhe
   já que dá para saber que anúncio traz os melhores clientes, e aponta a skill
   `ghl-meta`. Não a corras agora: fica para a fase 7 se for o trabalho dele.
   → `ferramentas.usa`, `ferramentas.operar_sozinho`, `ferramentas.fora`

7. **"Por defeito peço confirmação antes de enviar mensagens a pessoas reais,
   publicar, apagar e gastar dinheiro. Queres acrescentar mais alguma coisa?"**
   → `travoes.extra`

`pessoa.papel` e `maquina.pasta_trabalho` saem do que ele já disse: escreve-os
tu e confirma numa frase.

## O que não se pergunta

- **A língua.** Fica pt-PT e confirma-se no cartão.
- **O nível de autonomia.** Não é escolha dele, é o que o kit é.
- **"Descreve a tua voz."** Não produz nada. A voz sai do material do ponto 2.

## Fim

```
<python> ferramentas/estado.py --falta      # tem de vir vazio
<python> ferramentas/estado.py --marcar entrevista=feita
```

**Está feita quando:** `--falta` não devolve nada, e existe um `voz.md` com
citações reais dele lá dentro.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
