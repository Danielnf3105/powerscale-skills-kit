---
name: thank-you-page
description: >
  Constrói ou melhora páginas de "obrigado"/confirmação que aparecem
  imediatamente a seguir a um COMPROMISSO do lead: registo em webinar,
  marcação de call/auditoria, pedido de diagnóstico, quiz que termina em
  agendamento. Aplica o princípio de que a primeira coisa que a pessoa vê
  a seguir a comprometer-se decide metade do show rate, e nunca deve ser
  um genérico "não te esqueças de aparecer". Usar quando pedes
  "faz a thank you page", "página de obrigado", "página de confirmação",
  "melhora o show rate desta página de obrigado", "página depois de
  marcarem a call", "o que ponho na página depois do registo do webinar".
  Não usar para o follow-up humano pós-página (isso é `setting-e-follow-up`),
  nem para a página de OFERTA/registo em si, antes do compromisso (isso é
  `pagina-de-oferta`), nem para copy solta sem
  ser este momento específico (`copy-resposta-direta`).
version: 1.0.0
author: kit
---

# Página de Obrigado / Confirmação (o momento pós-compromisso)

## Para que serve

Todas as páginas de "obrigado" que valem alguma coisa têm o mesmo momento em
comum: a pessoa **acabou de se comprometer** (registou-se no webinar,
marcou a call, pediu o diagnóstico) e está a ver, pela primeira vez, o
que vem a seguir. Esse ecrã decide grande parte de quantas destas pessoas
aparecem de facto.

O erro mais comum (e o que esta skill existe para evitar) é tratar essa
página como um recibo: "obrigado, já está, aparece na hora marcada". Isso
não reduz no-shows, é um placeholder. A página tem de FAZER trabalho.

## Quando invocar

- "faz a thank you page do [funil]"
- "página de obrigado depois de marcarem a call/auditoria"
- "o que ponho na página de confirmação do webinar"
- "esta página de obrigado está fraca, o show rate está mau"
- "página depois do quiz, quando marcam a reunião"

---

## O diagnóstico: qual é o problema real do show rate?

Antes de escrever nada, identificar qual dos dois problemas está a fazer
as pessoas faltarem (são causas diferentes, pedem conteúdo diferente na
página; nunca tentar resolver os dois ao mesmo tempo na mesma peça
principal):

**A. Falta de urgência/intenção real**, a pessoa registou-se por
curiosidade, sem uma razão concreta para aparecer NAQUELE dia/hora. Sintoma:
regista-se muita gente, mas o show rate é baixo mesmo sem sinais de
desconfiança.
→ **Conteúdo de urgência**: dar-lhe, já nesta página, razões reais e
específicas para aparecer agora (não genéricas tipo "vais aprender muito"),
ligadas à dor/consequência concreta de não ir. Nunca inventar escassez falsa.

**B. Risco de confiança/reputação**, existe algo pesquisável sobre a
pessoa/marca que, se o lead for procurar sozinho antes da call, pode
travá-lo (uma review negativa, um tópico de fórum, o que uma IA de busca
diz sobre o nome). Sintoma: leads qualificados que desaparecem entre o
registo e a call sem razão aparente.
→ **Conteúdo de "due diligence antecipada"**: tu próprio adiantas, nesta
página, o que a pessoa poderia encontrar e como interpretá-lo, ANTES de
ela ir à procura sozinha e tirar as suas próprias conclusões. Só faz
sentido se o problema for real; nunca inventar uma ameaça à reputação
que não existe só para ter conteúdo.

Escolher UM como peça principal (vídeo, ou se não houver vídeo, o bloco
de texto imediatamente a seguir à confirmação). Não empilhar os dois; se
os dois problemas forem reais, o principal é o que mais pesa no show
rate atual.

---

## O que construir (estrutura, do topo para baixo)

1. **Confirmação**, reforça que o compromisso foi registado (nome, se
   disponível). Título curto, sem enrolar.
2. **A peça de urgência OU de due diligence** (ver diagnóstico acima) -
   imediatamente a seguir à confirmação, antes de qualquer outra coisa.
   Se não houver vídeo disponível, um bloco de texto com o mesmo trabalho
   (as razões reais, ou a antecipação da due diligence) substitui-o.
3. **Passos de ação imediata**, o padrão já provado nas nossas páginas
   (ex.: <Cliente>): 3 passos concretos e pequenos (confirmar no
   calendário, verificar o email, avisar um humano por WhatsApp se
   houver). Cada passo com um botão que já leva à app certa. Reduz
   fricção e usa reciprocidade (quem dá um passo pequeno tende a dar o
   seguinte).
4. **Reforço do compromisso**, em calls 1:1 (não em webinars de massa):
   dizer explicitamente que é uma reunião COM compromisso, que o horário
   foi reservado só para a pessoa, e que faltar sem motivo justificável
   normalmente significa não haver remarcação. Isto sobe o show rate mais
   do que parece: transforma uma marcação leve numa promessa.
5. **Tracking**, Pixel do evento (Lead/Schedule conforme o funil) +
   evento custom de compromisso + Clarity (ver `references/boilerplate-tecnico.md`).

## Diferenciação por tipo de funil

| Tipo | Peça principal | Passo 3 (WhatsApp) | Reforço de compromisso |
|---|---|---|---|
| Webinar (massa, sem call 1:1) | Urgência (porque aparecer ao vivo importa) | Normalmente não há humano 1:1 | Mais suave ("guarda o lugar") |
| Call/auditoria 1:1 | Due diligence se houver risco de confiança; senão urgência | Sim, se houver SDR/closer disponível | Forte ("com compromisso", sem remarcação) |
| Lead assíncrono (sem call marcada ainda) | Due diligence ou prova social, para gerir a espera | Não aplicável | Não aplicável (ainda não há hora marcada) |

---

## Regras invioláveis

- **pt-PT (AO90). ZERO em-dash.**
- **Nunca inventar** um problema de confiança que não existe, nem uma
  escassez/urgência falsa. Se não houver um motivo real para nenhum dos
  dois, o conteúdo principal é honesto e específico à dor do lead, não
  um substituto fabricado.
- **Nunca prometer cura/resultado garantido** (nichos de saúde: política
  da Meta, ver `copy-resposta-direta`).
- Marca do **cliente** quando é página de cliente; a tua marca quando és tu
  a assinar. Nunca as duas ao mesmo tempo.
- Tudo o que envolve números/prova é **rascunho até o cliente validar**.

## Quando NÃO usar

- Follow-up humano depois da página (mensagens, DMs, reanimar ghosts) → `setting-e-follow-up`.
- A página de registo/oferta em si, ANTES do compromisso → `pagina-de-oferta`.
- Copy solta sem ser este momento específico → `copy-resposta-direta`.

---

*Ver `references/boilerplate-tecnico.md` para o código reutilizável (Pixel, Clarity, botão de WhatsApp, contador).*

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
