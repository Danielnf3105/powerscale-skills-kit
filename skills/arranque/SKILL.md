---
name: arranque
description: >
  Personaliza este kit para quem o instalou, ou volta a personalizá-lo quando
  algo muda: entrevista curta, escreve o CLAUDE.md global dela, cria as pastas
  de trabalho e verifica a máquina. Correr no primeiro dia, e outra vez sempre
  que mude a marca, entre um cliente novo, ou apareça uma ferramenta nova.
  Usar quando ela diz "vamos configurar", "primeiro dia", "personaliza o kit",
  "atualiza o meu CLAUDE.md", "entrou um cliente novo", "mudámos as cores".
version: 2.0.0
author: PowerScale Skills Kit
---

# Arranque: tornar o kit dela

O processo completo vive em `~/.claude/kit/processo/`, que o instalador deixou
lá de propósito: assim continua a funcionar mesmo que a pasta de onde o kit foi
instalado seja movida ou apagada. **Lê de lá, não repitas aqui o que lá está.**

## Primeiro, vê onde estás

```
python3 ~/.claude/kit/ferramentas/estado.py --mostrar
```

(No Windows, `py -3`. O comando certo está em `estado.json`, campo `python_cmd`.)

## Depois, uma de três

**O perfil está incompleto** (aparecem campos em `--falta`): retoma na primeira
fase por concluir. As fases estão em `~/.claude/kit/processo/`, uma de cada vez.
Não repitas perguntas já respondidas: diz numa linha o que já sabes e pergunta
só o resto.

**O perfil está completo e ela quer mudar alguma coisa:** pergunta o que mudou e
corre **só** o que interessa. Nada de repetir a entrevista toda.

| Mudou | O que fazer |
|---|---|
| a marca (cores, tipografia, tratamento) | fase 3 para medir outra vez, gravar em `marca.*`, gerar |
| entrou ou saiu um cliente | `trabalho.clientes`, criar a pasta dele, gerar |
| ferramentas novas | `ferramentas.*`, gerar |
| ela quer outro tom nas respostas | `pessoa.estilo_resposta`, gerar |

Gravar cada resposta na hora:

```
python3 ~/.claude/kit/ferramentas/estado.py --responder marca.cor_acento="#C9A227"
python3 ~/.claude/kit/ferramentas/gerar_perfil.py
```

O que ela tiver escrito no `CLAUDE.md` fora dos marcadores `kit:inicio` e
`kit:fim` sobrevive. Por isso é seguro voltar a gerar.

**Está tudo feito e ela só quer confirmar:**

```
python3 ~/.claude/kit/ferramentas/verificar.py --nivel completo
```

## Regra final

Nunca acabes num "está tudo pronto". Acaba a **fazer** a coisa que ela tem para
despachar, e diz o que ficou à espera de alguém.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
