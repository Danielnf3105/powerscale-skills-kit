# Fase 4: entrevista

**Objetivo:** o perfil dela preenchido, em oito perguntas.

**Pré-condição:** fase 3 feita ou saltada.

## Como se conduz

- **Uma pergunta por mensagem.** Nunca um questionário de vinte linhas.
- **Grava a seguir a cada resposta**, sempre:

  ```
  <python> ferramentas/estado.py --responder pessoa.nome="Carolina Dinis"
  <python> ferramentas/estado.py --responder 'trabalho.tipos=["copy","anúncios"]'
  ```

  É isto que faz a entrevista sobreviver a uma conversa interrompida. O kit
  antigo perdia tudo por não o fazer.

- **Nunca repitas uma pergunta já respondida.** Corre `estado.py --falta` e
  pergunta só o que aparecer. Se ela já disse alguma coisa noutra conversa, essa
  também não se repete.
- Se retomas a meio, abre com uma linha do género: "já me disseste o site, o
  nome e o que vendes; faltam-me três coisas".

## As perguntas

1. **"Qual é o teu site? E o Instagram, se tiveres."**
   (feita na fase 3; se saltaste a descoberta, é aqui)
   → `descoberta.site`, `descoberta.instagram`

2. **O cartão de confirmação.** Mostra-lhe o retrato que mediste e pede correção,
   em vez de a fazer responder do zero:

   > Fui ver o teu site. Encontrei isto: vendes [X] a [Y], as cores são [#A] e
   > [#B], tratas as pessoas por [tu], a tipografia é [F]. O que é que está
   > errado?

   → `negocio.oferta`, `negocio.quem_compra`, `marca.*`, `pessoa.negocio`
   Se a descoberta falhou, desdobra em três perguntas diretas: o que vendes, a
   quem, e que cores usa a tua marca.

3. **"Como é que me chamo? E preferes respostas secas e diretas, ou com mais
   contexto à volta?"**
   → `pessoa.assistente`, `pessoa.estilo_resposta` ("direta" ou "com_contexto")

4. **"Que trabalho vai passar por aqui?"** Dá-lhe as opções: mensagens a leads,
   copy, páginas, anúncios, propostas, análise de calls, outra coisa.
   → `trabalho.tipos`

5. **"Isto é só para o teu negócio, ou também trabalhas para clientes? Se sim,
   quais estão ativos hoje?"**
   → `trabalho.para_clientes`, `trabalho.clientes` (nome, serviço, pasta)

6. **"O que é que tens de despachar esta semana?"**
   A pergunta mais valiosa das oito: é o trabalho da fase 7 e o único teste real
   ao kit. Insiste até vir uma coisa concreta, não "organizar-me melhor".
   → `trabalho.urgente`

7. **"Que ferramentas usas todos os dias? E alguma em que eu não deva mexer?"**
   → `ferramentas.usa`, `ferramentas.operar_sozinho`, `ferramentas.fora`

8. **"Por defeito, peço-te confirmação antes de enviar mensagens a pessoas
   reais, publicar, apagar e gastar dinheiro. Queres acrescentar mais alguma
   coisa a essa lista?"**
   → `travoes.extra`

Falta preencher `pessoa.papel` (o que ela faz, uma linha) e
`maquina.pasta_trabalho`: os dois saem do que ela já disse, escreve-os tu e
confirma numa frase, não faças disso perguntas.

## O que não se pergunta

- **A língua.** Fica pt-PT e confirma-se no cartão da pergunta 2.
- **O nível de autonomia.** Não é escolha dela, é o que o kit é.
- **"O que nunca se diz em nome da tua marca."** A frio não produz nada. Anota
  quando aparecer numa correção real e acrescenta ao perfil nesse dia.

## Fim

```
<python> ferramentas/estado.py --falta      # tem de vir vazio
<python> ferramentas/estado.py --marcar entrevista=feita
```

**Está feita quando:** `--falta` não devolve nada.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
