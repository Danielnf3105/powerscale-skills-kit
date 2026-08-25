# Fase 7: o primeiro trabalho

**Objetivo:** entregar-lhe uma coisa que ela usa hoje.

**Pré-condição:** fase 6 feita e a sessão reiniciada.

Um arranque que acaba em "está tudo instalado" não entregou nada. Acaba-se a
**fazer** a coisa que ela disse na pergunta 6 da entrevista.

## Passos

1. Lê o que ela disse:

   ```
   <python> ~/.claude/kit/ferramentas/estado.py --mostrar
   ```

   O campo é `trabalho.urgente`.

2. Confirma numa linha e começa: "disseste que tinhas de [X]. Vamos a isso."

3. Escolhe a skill certa e usa-a a sério, não em demonstração:

   | O que ela disse | Por onde começas |
   |---|---|
   | falar com leads, follow-up | `setting-e-follow-up` |
   | copy, página, anúncios para um cliente | `voz-de-marca` **primeiro**, depois `copy-resposta-direta` |
   | uma página | `pagina-de-oferta` |
   | criativos | `criativos-anuncios` (a copy é dela, a de fábrica é exemplo) |
   | perceber porque não fecha | `calls-de-venda` |
   | ligar uma ferramenta | `ferramentas-e-acessos` |

4. **Se o trabalho é para um cliente dela, o primeiro passo é sempre a voz desse
   cliente.** Copy escrita antes do Voice Bible é copy para deitar fora.

5. Entrega a sério: o ficheiro, o texto, a imagem. Nada de "aqui está um exemplo
   do que eu poderia fazer".

6. Fecha:

   ```
   <python> ~/.claude/kit/ferramentas/estado.py --marcar primeiro-trabalho=feita
   <python> ~/.claude/kit/ferramentas/estado.py --definir reinicio_pedido=false
   ```

7. Diz-lhe, em cinco linhas:
   - o que ficou instalado e onde
   - o que ela pode pedir a partir de agora, com dois ou três exemplos das
     palavras dela
   - o que ficou por decidir ou à espera de alguém
   - que para atualizar o kit basta dizer "atualiza o kit"
   - que se melhorar uma skill, deve dizer, para voltar ao kit

**Está feita quando:** existe um entregável real que ela pode usar hoje, e ela
consegue dizer por palavras dela o que é que isto faz.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
