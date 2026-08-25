---
name: ferramentas-e-acessos
description: >
  Como dar autonomia real ao Claude nesta máquina: a ordem obrigatória para
  operar qualquer sistema externo (MCP, depois CLI, depois API, e só no fim o
  browser), como ligar cada ferramenta, onde guardar chaves em segurança, e o
  que a plataforma NÃO deixa fazer por API (para não se perder um dia a tentar).
  Usar quando pedes "liga o X", "consegues aceder ao meu Y", "automatiza isto",
  "porque é que não consegues fazer Z sozinho", "onde ponho esta chave", ou
  sempre que uma tarefa exige tocar num sistema de fora.
version: 1.0.0
author: kit
---

# Ferramentas e acessos

O princípio que manda em tudo o resto:

> **Não existe "não dá". Existe "ainda não tenho acesso".**
> A pergunta certa nunca é "consegues?", é "por que via?".

Quando uma tarefa parece impossível, quase sempre é uma destas três:
falta uma chave, falta a ferramenta instalada, ou está a tentar-se pela via
errada. As três resolvem-se.

---

## A ordem obrigatória (não se salta)

1. **MCP dedicado**, se existir para essa aplicação. É a via mais rápida e a
   que menos parte.
2. **CLI oficial** (`gh`, `vercel`, `aws`, `stripe`, `rclone`, `az`).
3. **API HTTP direta**, com a chave guardada no cofre (ver abaixo).
4. **Ponte de terceiros paga**, quando compensa: um serviço que expõe por REST
   uma plataforma fechada. Vale a pena pagar 40 euros por mês para não depender
   de um browser aberto.
5. **Só no fim, automação de browser.**

**Porque é que o browser é o último recurso:** uma rotina que precisa de uma
janela aberta e de uma sessão iniciada é uma rotina que não corre. Basta a
sessão expirar, o computador estar desligado ou aparecer um pedido de
verificação, e a automação morre em silêncio. Serve para o que não tem API
nenhuma (portais fechados, verificação visual pontual), nunca para o que corre
todos os dias.

**Mas quando o browser é a única via, usa-se, e sem pedir autorização para cada
clique.** O que não se faz nunca é empurrar a tarefa de volta para a pessoa com
um "isto é contigo, são 10 minutos". Percorre-se o fluxo, deixa-se o formulário
preenchido até ao último campo possível, e diz-se exatamente o que falta. Só
param mesmo três coisas: escrever passwords, pagar, e enviar ficheiros do disco
em janelas de sistema.

---

## O cofre de chaves

**Uma pasta, um ficheiro, permissões fechadas. Nunca no chat, nunca no código,
nunca num ficheiro que vá para o Git.**

**Windows:**

```powershell
# uma vez
New-Item -ItemType Directory -Force "$HOME\.config\chaves"
notepad "$HOME\.config\chaves\secrets.env"
```

Formato do ficheiro, uma linha por chave:

```
META_ADS_TOKEN=...
OPENAI_API_KEY=...
CAL_API_KEY=...
```

**Ler dentro de um script (PowerShell):**

```powershell
Get-Content "$HOME\.config\chaves\secrets.env" | ForEach-Object {
  if ($_ -match '^\s*([A-Z0-9_]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) }
}
```

**Regras que não se negoceiam:**

- **Uma chave nunca se cola no chat.** Se acontecer, essa chave está queimada:
  rodá-la no serviço e substituir no ficheiro.
- Antes de pedir uma chave, avisa-se o que ela dá acesso a e o que vai ser feito
  com ela.
- Chave de leitura sempre que chegue. Só se pede escrita quando se vai escrever.
- Nada de chaves em capturas de ecrã, prints ou documentos partilhados.
- Se um serviço permitir chave por projeto ou por cliente, uma por cliente.
  Assim revoga-se uma sem partir as outras.

---

## O que ligar, e para quê

| Preciso de... | Via |
|---|---|
| Anúncios Meta (criar, ler, pausar) | MCP oficial da Meta, ou token de utilizador de sistema do Business Manager |
| Google Ads | API oficial, com token de programador e conta MCC |
| Email, calendário, Drive | conectores do Google (MCP) |
| Enviar email em nome de um domínio | serviço de envio (SES, Brevo, Postmark) com o domínio autenticado |
| Publicar ou agendar em redes sociais | serviço de publicação com OAuth oficial (não vale a pena montar isto de raiz) |
| WhatsApp | API oficial (Cloud API) para negócio, ou ponte não oficial num número dedicado, nunca no principal |
| Loja online | API da plataforma (Shopify, WooCommerce) com token de app privada |
| Publicar páginas | CLI da Vercel ou da Netlify |
| Domínios e DNS | API do registador |
| Transcrições de reuniões | MCP ou exportação da ferramenta de reunião |

---

## Limites reais das plataformas (não gastar o dia a tentar)

A plataforma está mesmo a dizer que não. Confirmado na prática:

- **Instagram e Messenger: não se inicia uma conversa por API.** Só se responde
  a quem escreveu primeiro, e dentro de uma janela de tempo. Prospeção por DM
  automatizada não tem via oficial, e as não oficiais custam a conta.
- **Instagram: não se agendam publicações por API** a partir de uma conta que
  não seja gerida por uma app aprovada. Usa-se um serviço de publicação.
- **Meta: muitas capacidades exigem uma app revista** no portal de programadores.
  Quando o portal está bloqueado, a saída é sondar por API em vez de esperar por
  webhooks.
- **Tokens de OAuth de um MCP não servem para a API HTTP** do mesmo serviço.
  São mundos separados, não há atalho por `curl`.
- **Tokens de utilizador de sistema só veem o Business Manager onde nasceram.**
  Um cliente novo é um token novo.
- **Captchas não se resolvem.** Se aparece um, a tarefa é da pessoa.
- **Contas com faturação por regularizar deixam de responder à API**, sem erro
  claro. Vale a pena verificar isso antes de investigar durante uma hora.

---

## Instalar o que falta (Windows)

O gestor de pacotes é o `winget`. As instalações mais úteis:

```powershell
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install GitHub.cli
winget install Gyan.FFmpeg
npm install -g vercel
```

Depois de instalar, **fechar e abrir o terminal** para o PATH atualizar. Uma
ferramenta que "não existe" logo a seguir a ser instalada quase sempre é isto.

---

## Antes de dizer que não dá

Percorre esta lista, por esta ordem:

1. Existe MCP para isto? (procurar no registo de conectores)
2. Existe CLI oficial?
3. A API pública faz isto? Ler a documentação, não a memória.
4. Existe uma ponte paga que resolva por 20 ou 40 euros por mês?
5. Dá para fazer pelo browser uma vez e automatizar o resto?
6. Só se as cinco falharem é que se diz que não dá, **e diz-se porquê**, com o
   erro exato ou a linha da documentação que o proíbe.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
