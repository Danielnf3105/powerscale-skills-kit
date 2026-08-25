# PowerScale Skills Kit

Skills, método e travões para o Claude trabalhar contigo como trabalha numa
equipa a sério: escrever na tua voz e na dos teus clientes, tratar de leads e
follow-up, montar páginas e criativos, operar as ferramentas por API.

Instala-se uma vez. A partir daí o Claude desta máquina sabe quem és, como se
escreve cá em casa, e o que nunca pode fazer sem te perguntar.

---

## Como se instala

**Uma coisa só:** abre o Claude dentro desta pasta e diz olá.

Ele lê as instruções que estão aqui, verifica a tua máquina, instala o que
falta, faz-te umas perguntas sobre o teu negócio e acaba a fazer contigo um
trabalho a sério. Uns 20 minutos, e não escreves um único comando.

Se te apetecer dar-lhe um empurrão, cola o texto do `PROMPT.txt`. Dá no mesmo.

**A meio interrompeu?** Fecha e volta a abrir na mesma pasta. Ele sabe onde
ficaram e continua daí. Não repete nada.

---

## O que fica instalado

**As skills**, em `~/.claude/skills/`. Aparecem sozinhas quando o pedido bate
certo, ou chamas por elas com `/nome`.

| Área | Skills |
|---|---|
| Arranque | `arranque`, `ferramentas-e-acessos` |
| Voz e escrita | `voz-de-marca`, `humanizer-pt`, `humanizer`, `copy-resposta-direta`, `copywriting` |
| Comercial | `setting-e-follow-up`, `calls-de-venda` |
| Páginas | `pagina-de-oferta`, `thank-you-page`, `craft`, `web-interface-guidelines`, `ux-heuristics-review`, `cognitive-load-conversion`, `accessibility`, `general-design-review`, `frontend-design`, `motion-framer`, `webapp-testing` |
| Anúncios | `meta-ads`, `criativos-anuncios`, `ghl-meta` (que anúncio traz os melhores clientes) |
| Documentos | `doc-coauthoring` |
| Fazer skills novas | `skill-creator` |

**O teu ficheiro de instruções**, em `~/.claude/CLAUDE.md`, escrito a partir das
tuas respostas. É teu: edita-o à vontade. Se pedires para o regerar, o que tu lá
escreveste não se perde.

**Fontes e logótipos** em `~/.claude/kit-assets/`. As fontes são livres para uso
comercial. O teu logótipo pões tu.

**Permissões** em `~/.claude/settings.json`: liberdade para ler, escrever,
correr comandos e procurar na web; travões no que apaga, publica ou gasta
dinheiro.

**Cofre de chaves** em `~/.config/chaves/secrets.env`. As chaves vivem lá
dentro, nunca no chat.

---

## As três regras da casa

1. **Não existe "não dá".** Existe "ainda não tenho acesso" ou "ainda não
   descobri por onde". Se ele disser que não dá, tem de dizer porquê, com o erro
   exato.
2. **Nada sai para uma pessoa real sem tu leres primeiro.** Mensagens,
   publicações, campanhas.
3. **Se se percebe que foi escrito por uma IA, o trabalho não está feito.**

---

## Depois

- **Atualizar:** diz "atualiza o kit". Ele vai buscar a versão nova e reinstala.
  As skills que tiveres alterado ficam guardadas antes, não se perde nada.
- **Mudou a marca, entrou um cliente novo?** Diz `/arranque`. Ele volta a
  perguntar só o que mudou.
- **Trabalho novo que se repete?** Pede uma skill: `/skill-creator`.
- **Está tudo bem instalado?** Pergunta-lhe. Ele corre a verificação e mostra-te
  a lista.

Isto é teu. As skills são ficheiros de texto em `~/.claude/skills/`, e podes
mexer em todas.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
