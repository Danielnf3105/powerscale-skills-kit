# Fase 4: a entrevista

**Objetivo:** saber quem ele é, onde publica, e **como é que ele escreve**.

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

## 3. As perguntas

3. **Cartão de confirmação.** Mostra-lhe o retrato que mediste na fase 3 e pede
   correção, em vez de o fazer responder do zero:

   > Fui ver o teu site. Encontrei isto: vendes [X] a [Y], as cores são [#A] e
   > [#B], tratas as pessoas por [tu], a tipografia é [F]. O que está errado?

   Uma resposta corrige oito campos. Se a descoberta falhou, desdobra em três
   diretas: o que vendes, a quem, e que cores usa a tua marca.
   → `negocio.oferta`, `negocio.quem_compra`, `marca.*`

4. **"Como é que me chamo? E preferes respostas secas e diretas, ou com mais
   contexto à volta?"**
   → `pessoa.assistente`, `pessoa.estilo_resposta`

5. **"Que trabalho vai passar por aqui?"** Opções: mensagens a leads, copy,
   páginas, anúncios, propostas, análise de calls, outra coisa.
   → `trabalho.tipos`

6. **"Isto é só para o teu negócio, ou também trabalhas para clientes? Se sim,
   quais estão ativos hoje?"**
   → `trabalho.para_clientes`, `trabalho.clientes`

7. **"O que é que tens de despachar esta semana?"**
   A mais valiosa: é o trabalho da fase 7 e o único teste real ao kit. Insiste
   até vir uma coisa concreta, não "organizar-me melhor".
   → `trabalho.urgente`

8. **"Que ferramentas usas todos os dias? E alguma em que eu não deva mexer?"**
   Se disser um CRM (GoHighLevel, HubSpot, Close) **e** correr anúncios, diz-lhe
   já que dá para saber que anúncio traz os melhores clientes, e aponta a skill
   `ghl-meta`. Não a corras agora: fica para a fase 7 se for o trabalho dele.
   → `ferramentas.usa`, `ferramentas.operar_sozinho`, `ferramentas.fora`

9. **"Por defeito peço confirmação antes de enviar mensagens a pessoas reais,
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
