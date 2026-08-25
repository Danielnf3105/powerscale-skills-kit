# Passar o kit a alguém

Um comando teu, uma mensagem enviada, e o resto acontece do lado de lá.

## Publicar

```bash
cd ~/Documents/Claude/powerscale-skills-kit
./ferramentas/entregar.sh "Carolina"
```

O que isto faz: verifica que o kit está inteiro (manifesto certo, tudo
assinado, nada por commitar), cria ou atualiza o repositório **público**, marca a
versão, e deixa no teu Desktop a mensagem pronta a enviar.

Recusa publicar se houver trabalho por commitar. É de propósito: o que ficasse
de fora nunca chegava a quem instala, e a falha só aparecia do lado dela.

## Enviar

Manda-lhe o texto que ficou em `~/Desktop/MENSAGEM-PARA-<Nome>.txt`. São três
passos: descarregar, abrir o Claude na pasta, dizer olá.

**Não lhe mandes fazer mais nada.** Nem aceitar convites, nem instalar Python,
nem criar contas. O Claude dela trata disso e pede-lhe autorização quando
precisar.

## Porque é que o repositório é público

O kit não tem chaves nem dados de clientes: são skills, método e fontes livres.
Público significa que ela descarrega sem conta, sem convite e sem autenticação,
que é exatamente onde uma pessoa não técnica em Windows trava. E significa que
recebe atualizações com um `git pull`, ou com um ZIP novo.

O que é proprietário (clientes, contratos, o House, as contas de anúncios) nunca
entrou aqui e não entra.

## Como saber que correu bem

Pergunta-lhe se o Claude lhe mostrou uma imagem com o nome do negócio dela. É o
sinal de que está tudo no sítio: Python, fontes, skills, caminhos e acentos.

Se quiseres confirmar tu, pede-lhe para dizer ao Claude dela "verifica se o kit
está bem instalado". Ele corre a verificação e devolve PRONTO ou a lista do que
falta.

## Quando melhorares o kit

```bash
git add -A && git commit -m "o que mudou" && ./ferramentas/entregar.sh
```

Do lado dela é só dizer "atualiza o kit". As skills que ela tiver alterado ficam
guardadas em `~/.claude/kit/skills-alteradas/` antes de serem substituídas: não
se perde trabalho dela, e por isso ela não ganha medo de atualizar.

Sobe a `VERSAO` quando a mudança for grande. É o que aparece no ficheiro de
instruções dela e nas etiquetas do repositório.

## O que este kit NÃO leva

Nada de PowerScale House, GoHighLevel, contratos, clientes, contas de anúncios,
nem a paleta da nossa marca aplicada ao trabalho dela. A marca aparece como
origem (nos ficheiros do kit e no ficheiro de instruções dela), e nunca no que
ela produz para os clientes dela.

Se um dia quiseres dar a alguém acesso ao que é nosso a sério, isso é o kit
interno, e esse é privado por bons motivos.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
