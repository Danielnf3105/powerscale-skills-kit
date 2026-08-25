# Fase 7: o primeiro trabalho

**Objetivo:** entregar-lhe uma coisa que a pessoa usa hoje.

**Pré-condição:** fase 6 feita e a sessão reiniciada.

Um arranque que acaba em "está tudo instalado" não entregou nada. Acaba-se a
**fazer** a coisa que a pessoa disse na entrevista.

## Passos

1. Lê o que a pessoa disse:

   ```
   <python> ~/.claude/kit/ferramentas/estado.py --mostrar
   ```

   O campo é `trabalho.urgente`.

2. Confirma numa linha e começa: "disseste que tinhas de [X]. Vamos a isso."

3. Escolhe a skill certa e usa-a a sério, não em demonstração:

   | O que a pessoa disse | Por onde começas |
   |---|---|
   | falar com leads, follow-up | `setting-e-follow-up` |
   | copy, página, anúncios para um cliente | `voz-de-marca` **primeiro**, depois `copy-resposta-direta` |
   | uma página | `pagina-de-oferta` |
   | criativos | `criativos-anuncios` (a copy é da pessoa, a de fábrica é exemplo) |
   | perceber porque não fecha | `calls-de-venda` |
   | saber que anúncio traz os melhores clientes | `ghl-meta` |
   | ligar uma ferramenta | `ferramentas-e-acessos` |

4. **Toda a copy passa pelo Voice Bible.** O da própria pessoa está em
   `meu/voz.md` desde a fase 4. Se o trabalho é para um cliente dela, o primeiro
   passo é a voz **desse cliente**, que é outra pessoa: skill `voz-de-marca`.
   Copy escrita antes do Voice Bible é copy para deitar fora.

   Antes de entregar seja o que for escrito, corre o filtro anti-IA
   (`humanizer-pt`). Se se perceber que foi uma máquina a escrever, o trabalho
   não está feito.

5. Entrega a sério: o ficheiro, o texto, a imagem. Nada de "aqui está um exemplo
   do que eu poderia fazer".

6. Fecha:

   ```
   <python> ~/.claude/kit/ferramentas/estado.py --marcar primeiro-trabalho=feita
   <python> ~/.claude/kit/ferramentas/estado.py --definir reinicio_pedido=false
   ```

7. Diz-lhe, em cinco linhas:
   - o que ficou instalado e onde
   - o que pode pedir a partir de agora, com dois ou três exemplos nas
     palavras da própria pessoa
   - o que ficou por decidir ou à espera de alguém
   - que para atualizar o kit basta dizer "atualiza o kit"
   - que se melhorar uma skill, deve dizer, para voltar ao kit

**Está feita quando:** existe um entregável real que a pessoa pode usar hoje, e
consegue dizer por palavras dela o que é que isto faz.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
