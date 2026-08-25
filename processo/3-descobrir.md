# Fase 3: descobrir

**Objetivo:** chegar à entrevista já a saber metade das respostas.

**Pré-condição:** fase 2 feita.

O princípio da casa: os inputs que separam um trabalho premium de um genérico
vais buscá-los tu, não os pedes. Perguntar a cor da marca a quem tem um site é
fazê-la trabalhar por ti.

## Passos

1. Pergunta-lhe **só isto**: "Qual é o teu site? E o Instagram, se tiveres."
   Aceita "não tenho" sem insistir.

2. Se deu um site, mede-o:

   ```
   <python> ferramentas/descobrir_site.py https://osite.pt
   ```

   Vem de lá: o que vende e a quem, as cores dominantes com o número de vezes
   que aparecem, a tipografia, o tratamento (tu ou você), e o logótipo se for
   apanhável.

3. **Se o site não deu cores** (acontece em Wix, Squarespace e sites feitos em
   React, onde o estilo não vem no HTML), pede-lhe uma captura de ecrã da
   página inicial e mede a partir daí:

   ```
   <python> ferramentas/cores.py ~/Desktop/captura.png
   ```

   Isto continua a ser medir. O que não se faz é adivinhar uma cor.

4. **O Instagram não se lê por programa** (exige sessão iniciada). Se ela deu o
   Instagram, usa-o de outra maneira: "manda-me três publicações que sejam mesmo
   a tua voz". Isso vale mais para a voz do que qualquer raspagem.

5. Grava o que apanhaste em `perfil.descoberta` e nas propostas de marca. O
   `descobrir_site.py` já escreve o que encontrou.

6. Marca a fase. **Sem internet ou sem site, marca `saltada` e segue**: a
   descoberta acelera a entrevista, não é condição para ela.

   ```
   <python> ferramentas/estado.py --marcar descobrir=feita
   ```

**Está feita quando:** ou tens um retrato do negócio dela para confirmar na fase
seguinte, ou sabes que não há e vais perguntar tudo.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
