# Boilerplate técnico das páginas de obrigado

Código reutilizável já provado nas páginas existentes. Copiar e adaptar
os IDs/tokens ao cliente/funil em causa (nunca reutilizar o Pixel ID ou
o Clarity ID de outro cliente).

## Os três tipos, e o que muda em cada um

- **Call 1:1 marcada**: revela o diagnóstico ou o motivo pelo qual a call vai
  valer a pena, 3 passos concretos, botão de WhatsApp pré-preenchido, e a nota
  de "reservado só para ti, sem remarcação".
- **Lead assíncrono** (ainda sem hora marcada): confirmação + expectativa
  concreta ("respondo em 24 a 48 horas") + uma peça que mate a dúvida que ia
  travar a decisão. Sem contador, que não há hora.
- **Webinar ou evento**: urgência de aparecer ao vivo, data e hora com fuso,
  botão de calendário, e o link do grupo se existir.

## Meta Pixel (PageView + evento de conversão)

```html
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '<PIXEL_ID_DO_CLIENTE>');
fbq('track', 'PageView');
fbq('track', 'Lead'); <!-- ou 'Schedule' se for marcação de call -->
fbq('trackCustom', 'Compromisso'); <!-- opcional: só em páginas com reforço de compromisso -->
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=<PIXEL_ID_DO_CLIENTE>&ev=Lead&noscript=1"/></noscript>
```

## Microsoft Clarity

```html
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "<CLARITY_ID>");
</script>
```

## Botão de WhatsApp pré-preenchido (passo 3 do compromisso)

```html
<script>
(function(){
  var WA_NUMERO = "<numero-com-indicativo-sem-mais>"; // ex: 351917992016
  var nome = "<nome-da-lead-se-disponivel>";
  var txt = nome
    ? "Olá, já marquei a minha sessão. Sou o/a " + nome + "."
    : "Olá, já marquei a minha sessão.";
  document.getElementById("wa").href = "https://wa.me/" + WA_NUMERO + "?text=" + encodeURIComponent(txt);
})();
</script>
```

## Nota de compromisso (copy-base, adaptar à voz do cliente)

> "É uma reunião com compromisso. Reservamos este horário e este tempo
> só para ti. Por isso, esta reunião não se repete: se faltares sem um
> motivo justificável, não voltamos a remarcar."

Adaptar o tom à marca (mais suave para clientes com voz "amiga
especialista", mais direto para marcas mais assertivas), mas manter a
lógica: horário reservado + consequência clara de faltar.
