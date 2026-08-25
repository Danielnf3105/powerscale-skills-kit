# Formato da análise de uma call

Guardar em `clientes/<cliente>/calls/analises/<data>-<nome>.md`. Se preferires
dados estruturados para agregar depois, guarda também um `.json` com as mesmas
chaves.

```markdown
# <Cliente> · call com <Lead> · <data>

**Score:** 62/100 · **Resultado:** follow-up · **Duração:** 47 min ·
**Tempo de fala:** 68% quem vende / 32% lead · **Perguntas feitas:** 21

## Resumo
Duas a quatro frases. Onde a call se ganhou e onde se perdeu.

## Fases
| Fase | Estado | Min | Prova |
|---|---|---|---|
| Abertura e frame | ok | 00:40 | "vamos estar 40 minutos, e no fim digo-te se faz sentido" |
| Ponto B | falhou | - | nunca perguntou o objetivo dela |

Estados: ok, parcial, falhou, não aplicável.

## Objeções
### 32:11 · Preço
- **Ela disse:** "isso é muito acima do que eu estava a pensar"
- **Resposta dada:** "eu percebo, mas o valor compensa"
- **Resultado:** não batida
- **Porque falhou:** respondeu com afirmação, não com pergunta. Não descobriu
  com o que ela estava a comparar.
- **A dizer da próxima, à letra:** "Muito acima do quê? Do que estavas à espera,
  ou do que tens disponível este mês?"

## Momentos que decidiram a call
- **21:04 · perda de frame.** Ela perguntou o preço e ele deu-o antes de haver
  valor construído. Citação: "..." Alternativa: "Já lá vamos, e prometo que não
  saímos daqui sem esse número. Antes disso preciso de perceber uma coisa: ..."

## Regras da marca quebradas
- 38:20, tratou por você depois de ter começado por tu. Citação: "..."

## O que correu bem
- 12:30, a pergunta sobre o último lançamento abriu a conversa toda.

## Lições (máximo 3)
1. ...
```

## Campos para o agregado

Se guardares JSON, usa estas chaves, que são as que o relatório do lote soma:

`score`, `outcome`, `stages[].status`, `objections[].resultado`,
`regras_violadas[]`, `pediu_fecho`, `proximo_passo_agendado`, `talk_ratio`.
