# Quando alguma coisa corre mal

Procura aqui **antes** de lhe perguntares seja o que for. Quase tudo o que
falha nesta instalação já falhou antes.

## Windows

| Sintoma | Causa | O que fazer |
|---|---|---|
| `não é possível carregar o ficheiro .ps1` | política de execução | já corres com `-ExecutionPolicy Bypass`; se a política for da empresa, `Set-ExecutionPolicy -Scope Process Bypass` e repete |
| o `.ps1` não corre e veio de um ZIP | marca de ficheiro descarregado | `Get-ChildItem -Recurse -File \| Unblock-File` (o instalador já faz) |
| `python` abre a Microsoft Store | é o atalho da Store, não é Python | instala a sério com `winget install Python.Python.3.12` e usa `py -3` |
| acentos com lixo num ficheiro | o PowerShell grava UTF-8 com BOM | esse ficheiro tem de ser escrito por Python, não por PowerShell |
| `settings.json` deixou de funcionar | BOM no início | reescreve sem BOM; o verificador deteta |
| caminhos partem a meio | nome de utilizador com espaços ou acentos | aspas em tudo; se persistir, trabalha a partir do Python |
| a pasta Documentos não é a que se vê | OneDrive redireciona | usa `[Environment]::GetFolderPath("MyDocuments")` |

## Instalação

| Sintoma | Causa | O que fazer |
|---|---|---|
| `permission denied: ./instalar.sh` | falta o bit de execução | `chmod +x instalar.sh` |
| "instalei N skills mas o kit tem M" | cópia incompleta | corre outra vez; se repetir, o descarregamento veio truncado |
| as skills não aparecem no Claude | a sessão não reiniciou | fechar e abrir o terminal. Só são lidas no arranque |
| `No module named 'PIL'` | falta o Pillow | `<python> -m pip install --user Pillow` |
| "Nao encontro as fontes" | o instalador não correu, ou correu antes desta versão | repete a fase 2 |
| o gerador de anúncios queixa-se do logótipo | não há logótipo | é opcional, o anúncio sai na mesma; põe o ficheiro em `assets/logos/` quando o tiveres |

## Descarregar o kit

| Sintoma | Causa | O que fazer |
|---|---|---|
| `command not found: git` | não há git | o kit é público: descarrega o ZIP do GitHub, não precisa de git nenhum |
| o clone pede utilizador e password | o GitHub já não aceita passwords | com o repo público não devia acontecer; confirma o endereço |
| `repository not found` | endereço errado | confirma o URL com quem te deu o kit |

## Perfil e CLAUDE.md

| Sintoma | Causa | O que fazer |
|---|---|---|
| "Nao dá para escrever o CLAUDE.md ainda" | faltam respostas | o comando diz quais; volta à fase 4 só para essas |
| ficaram `{{` ou `<NOME>` no ficheiro | gerado a partir de um perfil incompleto | acaba a entrevista e gera outra vez |
| editou o ficheiro e quer regerar | é seguro | o que estiver fora dos marcadores `kit:inicio`/`kit:fim` sobrevive |
| o `CLAUDE.md` está velho | o perfil mudou depois | `gerar_perfil.py` outra vez; o verificador avisa disto |

## Regras que valem sempre

- **Nunca lhe digas "não consigo" sem lhe dares o passo seguinte.**
- Se o problema é mesmo de outra pessoa (um acesso, uma chave), escreve-lhe a
  mensagem pronta a enviar, em vez de a mandar pedir.
- Se colarem uma chave no chat, avisa na hora que essa chave passou a estar
  exposta e tem de ser trocada no serviço. Guarda a nova no cofre e nunca a
  repitas no chat.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
