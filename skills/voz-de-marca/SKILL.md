---
name: voz-de-marca
description: >
  Extrai, codifica e aplica a voz de uma marca ou pessoa, para que tudo o que
  se escreve em nome dela soe a ela e não a uma IA. Produz um Voice Bible
  (regra de ouro, leis, registos, léxico do que se usa e do que nunca se diz,
  prova) e verifica copy contra ele. Usar quando pedes "extrai a voz do cliente
  X", "isto não soa ao cliente", "cria o guia de voz", "escreve como ele
  escreve", "vou começar a escrever para o cliente Y", ou sempre que uma peça
  vai sair assinada por outra pessoa. Correr ANTES de qualquer copy nova para
  um cliente novo.
version: 1.0.0
author: kit
---

# Voz de marca

A diferença entre copy que o cliente aprova ao primeiro e copy que volta com
"não é bem assim que eu falo" é esta skill. Não é decoração: quando escreves
em nome de alguém, quem fala é essa pessoa.

Uma voz não se inventa nem se descreve com adjetivos. **Extrai-se de material
real e prova-se com citações.** Um guia de voz que diga "tom profissional mas
acessível, próximo e confiante" não serve para nada: cabe em qualquer marca do
mundo, logo não descreve nenhuma.

---

## Parte 1: extrair

### As fontes, por ordem de valor

1. **A pessoa a falar sem guião.** Áudios de WhatsApp, gravações de calls,
   stories, lives, podcasts. É aqui que está a voz verdadeira, porque ninguém
   se autocorrige a falar. Transcreve (ver skill `calls-de-venda`) e lê.
2. **O que ela já escreveu e publicou.** Posts, legendas, emails à lista,
   páginas de venda, respostas a comentários. Já passou pelo filtro dela.
3. **Mensagens diretas dela a clientes.** O registo mais honesto que existe em
   texto.
4. **Material escrito por terceiros e aprovado por ela.** Vale menos: já tem a
   voz de outra pessoa lá dentro.
5. **O que ela diz que a voz dela é.** Vale pouco sozinho. Quase toda a gente
   se descreve como "próximo e profissional". Serve para confirmar, não para
   definir.

**Mínimo aceitável:** 5 peças escritas e 10 minutos de fala. Abaixo disto, o
Voice Bible sai como rascunho e diz-se que é rascunho.

### O que procurar (é aqui que está o trabalho)

Lê o material com uma lista aberta e apanha:

- **Construções que se repetem.** Como abre uma frase, como remata, que
  conector usa três vezes por parágrafo. Uma marca reconhece-se pela sintaxe,
  não pelo vocabulário.
- **Palavras dela.** As que usa muito e que outra pessoa não usaria assim.
- **Palavras que nunca aparecem.** Tão importante como as anteriores. Se em 40
  peças nunca escreveu "solução", tu também não escreves.
- **Como trata a pessoa.** Tu ou você. Nunca os dois. Verifica se muda por
  canal.
- **Como diz que não.** A forma como exclui gente ("isto não é para quem...")
  é a assinatura mais difícil de imitar e a mais reconhecível.
- **O que promete e o que se recusa a prometer.** Em saúde, dinheiro e emprego
  isto passa de estilo a risco legal.
- **Como usa a prova.** Números? Casos com nome? Prints? Ou nunca?
- **Ritmo.** Frases curtas a bater, ou parágrafos longos que respiram.
- **Humor, ironia, palavrões.** Existe ou não existe. Se existe, em que dose.

### Registos

Quase toda a gente tem dois ou três registos e não os mistura: o de vender não
é o de ensinar, o do email não é o do story. Nomeia-os e diz onde cada um vive.
Misturar registos é o erro que mais denuncia copy escrita por fora.

---

## Parte 2: codificar (o Voice Bible)

Guardar em `clientes/<cliente>/voz.md`. Estrutura fixa, ver o modelo completo
em `references/modelo-voice-bible.md`:

1. **A regra de ouro.** Uma frase. Se a pessoa que escreve só ler uma linha, é
   esta.
2. **As leis** (4 a 8). Cada lei é um padrão concreto, com um exemplo real dela
   ao lado e o contra-exemplo do que se costuma escrever em vez disso. Uma lei sem citação é palpite.
3. **Os registos** e onde cada um se usa.
4. **Léxico:** a coluna do que ela diz à letra, e a coluna do que nunca se
   escreve. A segunda coluna é a que mais trabalho poupa.
5. **Limites:** o que nunca se promete, e porquê.
6. **A prova:** pega numa peça que já esteja escrita (tua ou da equipa) e
   reescreve-a na voz dela, lado a lado. É o teste que mostra que o guia
   funciona, e é a parte que o cliente lê primeiro.
7. **O que falta para a v2.** Nenhum Voice Bible nasce completo. Diz-se o que
   ainda não se sabe.

**Marcar a versão e a data.** Uma voz muda quando o negócio muda.

---

## Parte 3: aplicar e verificar

Antes de entregar qualquer peça escrita em nome de alguém:

1. **Passa o léxico.** Procura no texto cada palavra da coluna "nunca". Zero
   ocorrências.
2. **Passa as leis.** Uma a uma, com o texto à frente.
3. **Corre o filtro anti-IA.** Skill `humanizer-pt` (e `humanizer` se for em
   inglês). A voz mais bem extraída do mundo não sobrevive a um texto cheio de
   "não é X, é Y" e gerúndios de remate.
4. **O teste do reconhecimento.** Se apagares o logótipo e mostrares o texto a
   quem conhece a marca, ela reconhece? Se não, ainda não está.
5. **O teste do inverso.** Se o texto servisse igualmente bem para o concorrente
   dela, o texto não diz nada. Reescreve.

Quando a técnica de copy e a voz colidem (a resposta direta quer um número
chocante, a marca nunca fala de dinheiro), **a voz ganha na expressão e o
objetivo mantém-se**: encontra-se outra forma de o atingir. Explica-se a
troca a quem aprova, não se decide sozinho e em silêncio.

---

## Erros que custam clientes

- **Inventar a voz** porque o material era pouco. Diz-se que é rascunho e
  pede-se mais material. Um Voice Bible errado espalha o erro por 40 peças.
- **Descrever em vez de citar.** "Tom caloroso" não é acionável. "Abre sempre
  a tratar a pessoa pelo primeiro nome e a referir o que ela disse na última
  mensagem" é.
- **Copiar a voz de um cliente para outro** porque estão no mesmo nicho. São
  pessoas diferentes.
- **Deixar a tua própria voz entrar.** Se escreves para cinco clientes e os
  cinco começam a soar iguais, o que estás a espalhar é a tua voz, não a deles.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
