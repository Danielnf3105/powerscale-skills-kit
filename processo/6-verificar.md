# Fase 6: verificar

**Objetivo:** provar que está bom, com uma imagem que a pessoa vê.

**Pré-condição:** fase 5 feita.

## Passos

1. Corre a verificação completa:

   ```
   <python> ferramentas/verificar.py --nivel completo
   ```

   `0` é PRONTO. `2` são avisos que não travam o trabalho (o mais comum é faltar
   o Pillow). `1` é para resolver antes de avançar: cada linha traz o que fazer.

2. A verificação gera uma imagem de prova. **Abre-a e olha para ela.** Confirma
   três coisas com os teus próprios olhos:
   - os acentos estão inteiros (ação, coração, ó, ã, ç)
   - a cor é a da marca da pessoa, não a do kit
   - o nome do negócio está lá

   Se os acentos vierem partidos, é encoding, e está em `problemas.md`.

3. **Mostra-lhe a imagem.** É a primeira coisa que se vê a funcionar, e é o que
   lhe prova que isto não é uma pasta de ficheiros: é uma máquina que produz.

4. Marca a fase e pede o reinício. **É aqui, e só aqui:**

   ```
   <python> ferramentas/estado.py --marcar verificar=feita
   <python> ferramentas/estado.py --definir reinicio_pedido=true
   ```

   Diz-lhe, exatamente: "fecha esta janela do terminal e abre outra na mesma
   pasta. As skills só são lidas quando o programa arranca. Quando voltares, é
   só dizeres olá: eu sei onde ficámos."

**Está feita quando:** a verificação passa e a pessoa viu a imagem.

Na sessão seguinte, começas por ler o estado, vês as fases 0 a 6 feitas, e vais
direto à 7. Ela não tem de se lembrar de nada.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
