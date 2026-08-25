---
name: calls-de-venda
description: >
  Analisa calls de venda (diagnóstico, discovery, fecho) contra o playbook de
  quem vende, e devolve correção concreta: onde se perdeu o frame, que objeções
  ficaram por bater, a frase certa à letra para a próxima vez, e um score
  comparável entre calls. Também prepara a call antes de ela acontecer. Usar
  quando pedes "analisa esta call", "porque é que esta reunião não fechou",
  "onde é que perdi esta venda", "prepara-me para a call com o X", "faz o
  relatório das calls desta semana". Não é um resumo de reunião.
version: 1.0.0
author: kit
---

# Calls de venda: preparar e analisar

Transforma uma gravação numa correção concreta. O objetivo não é descrever a
call, é dar à pessoa a frase que devia ter dito, ao minuto em que devia ter
sido dita.

## Antes da call: preparação

Quando pedes "prepara-me para a call com o X", entrego uma página só:

1. **Quem é**, o que se sabe: negócio, faturação, o que já tentou, de onde veio
   (que anúncio, que DM, que formulário). Tirado do CRM, do histórico de
   mensagens e do que a pessoa escreveu no formulário, à letra.
2. **A hipótese**, qual é provavelmente o problema real, e a pergunta que o
   confirma ou desmente nos primeiros 5 minutos.
3. **As 3 objeções mais prováveis** para este perfil, com a resposta escrita.
4. **A ordem da oferta**, o que se propõe primeiro e o que nunca se propõe nesta
   call.
5. **O próximo passo a fechar**, com dia e hora, antes de desligar.

## Depois da call: análise

### Passo 1, arranjar a transcrição

Por ordem de preferência:

1. **Fathom, Fireflies, Otter ou equivalente**, já trazem oradores separados e
   timestamps. É a melhor fonte.
2. **Notas do Gemini / transcrição do Meet ou do Teams**, também trazem
   oradores. Melhor do que transcrever à mão o áudio.
3. **Ficheiro de áudio**, transcrever localmente. Ver
   `references/transcrever.md` (whisper, comandos e as armadilhas do português).

Guardar em `clientes/<cliente>/calls/transcricoes/<data>-<nome>.txt`.

### Passo 2, pontuar contra o playbook

**Pontua-se contra o playbook de quem vende, nunca contra uma ideia genérica de
vendas.** O playbook vive em `clientes/<cliente>/calls/playbook.md` e diz: as
fases da call por ordem, as objeções esperadas, as regras da marca (tratamento,
o que nunca se promete) e a escada de produtos (o que se propõe primeiro).

Se não existir playbook, faz-se um antes de analisar seja o que for. Modelo em
`references/playbook-modelo.md`. Sem playbook, a análise é opinião.

### Regras da análise

- **Cada afirmação com prova**: timestamp e citação da transcrição. Sem citação,
  não entra no relatório.
- **A alternativa escreve-se à letra**, na voz de quem vende. Uma frase que a
  pessoa consiga dizer na call seguinte, não um conselho abstrato. "Devias ter
  criado mais urgência" não serve. "E o que é que acontece se daqui a três
  meses estiveres exatamente na mesma?" serve.
- **Separar o que correu bem.** Uma análise só com erros não muda comportamento
  nenhum, só põe a pessoa na defensiva.
- **Nunca inventar resultados.** Não se escreve "esta call teria fechado". Diz-se
  o que ficou por fazer.
- **O score não se escreve a olho**, calcula-se com a fórmula fixa abaixo, senão
  não se comparam duas calls.

### A fórmula do score (0 a 100)

```
fases      55%   fases cumpridas a dividir pelas aplicáveis (parcial vale metade)
objeções   25%   objeções batidas a dividir pelas levantadas (parcial vale metade)
fecho      20%   pediu o fecho (10) + próximo passo agendado com dia e hora (10)
menos           5 pontos por cada regra da marca quebrada, até um máximo de 20
```

Sem objeções levantadas, os 25% distribuem-se pelas fases. O número interessa
pouco isolado, interessa a série: 10 calls seguidas dizem onde está o buraco.

### Passo 3, o relatório

Formato completo em `references/formato-analise.md`. O essencial:

- **Resumo**, 2 a 4 frases: onde a call se ganhou e onde se perdeu.
- **Resultado**: fechou, follow-up, não fechou, não qualificado.
- **Fases**, uma linha por fase com estado, minuto e citação.
- **Objeções**, com a citação da lead, a resposta dada, porque falhou e a
  resposta recomendada à letra.
- **Momentos que decidiram a call**, os 3 a 5 que interessam.
- **Tempo de fala** (quem falou mais) e número de perguntas feitas.
- **Regras da marca quebradas**, com citação.
- **Lições**, no máximo 3, acionáveis.

### Passo 4, o agregado

Uma call diz pouco. A partir de 5, o relatório do lote responde a três
perguntas: que fase falha mais vezes, que objeção fica mais vezes por bater, e
se o problema é da pessoa ou do processo. Se a mesma fase falha em 9 de 10
calls, o problema é o guião, não quem vende.

## Armadilhas conhecidas

- Modelos de transcrição pequenos confundem termos técnicos e nomes de marca em
  português. Usar modelo médio, forçar a língua e dar uma lista de termos do
  nicho, senão inventam palavras que nunca foram ditas.
- Gravações de Meet e Zoom vêm em mono com os dois oradores misturados: não há
  separação automática, os oradores atribuem-se pelo conteúdo. Uma transcrição
  que já traga oradores vale mais do que uma transcrição melhor sem eles.
- Uma call de 50 minutos demora perto de 30 minutos a transcrever num portátil
  normal. Uma de cada vez.
- **Gravar uma call sem avisar é ilegal na maioria dos países da UE.** Pedir
  autorização no início, e ficar com o "sim" gravado.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
