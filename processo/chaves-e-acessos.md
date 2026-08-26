# Onde se vão buscar as chaves, clique a clique

Quem lê isto é o Claude. **Não mandes a pessoa "ir às definições".** Diz o menu,
o submenu e o botão, um passo de cada vez, e espera que ela confirme antes de
dares o seguinte.

## Regra que vale para todas

Uma chave **nunca é colada no chat**. Vai direta para o cofre:

```
~/.config/chaves/secrets.env          (Windows: %USERPROFILE%\.config\chaves\secrets.env)
```

Se aparecer uma no chat, avisa na hora: essa chave passou a estar exposta e tem
de ser trocada no serviço. Apagar a mensagem não chega.

**Se estiverem a gravar o ecrã, isto faz-se antes ou fora da gravação.** Um
token que aparece num vídeo é um token queimado.

---

## GoHighLevel

Duas coisas: o token e o id da subconta.

**O token** (`GHL_TOKEN`)

1. Entrar na **subconta do cliente**, não na vista de agência (canto superior
   esquerdo, o seletor de conta).
2. **Settings**, na barra da esquerda, no fim.
3. **Private Integrations**.
4. **Create new integration**.
5. Nome: `Relatorio de anuncios`.
6. Marcar os âmbitos de leitura. Os que interessam:
   `contacts.readonly`, `opportunities.readonly`, `locations.readonly`.
7. **Create**, e copiar o token que aparece. **Aparece uma vez só.** Se fechar a
   janela sem copiar, apaga-se e cria-se outro.

**O id da subconta** (`GHL_LOCATION_ID`)

Settings → **Business Profile**, e o id está no topo. Também aparece no próprio
URL do painel, entre `/location/` e a barra seguinte.

Se a integração privada não aparecer no menu, a conta está num plano que não a
tem, ou o utilizador não é admin da subconta. Nesse caso é o dono da conta que
tem de a criar.

---

## Facebook e Instagram (Meta)

Duas coisas: o token e o id da conta de anúncios.

**O token** (`META_TOKEN`)

1. **business.facebook.com** → **Definições da empresa** (o ícone de engrenagem).
2. **Utilizadores** → **Utilizadores de sistema**.
3. **Adicionar**, dar um nome (`Relatorios`), papel **Empregado**.
4. Com o utilizador selecionado: **Adicionar ativos** → **Contas de anúncios** →
   escolher a conta → ligar **Ver desempenho**.
5. **Gerar novo token** → escolher a app → âmbito **`ads_read`** →
   expiração **Nunca**.
6. Copiar. **Aparece uma vez só.**

**O id da conta** (`META_AD_ACCOUNT`)

No Gestor de Anúncios, no seletor de conta em cima, aparece como
`act_1234567890`. Vai com o `act_` à frente.

Dois enganos que custam uma tarde:

- **Utilizador de sistema, não token pessoal.** O pessoal expira em semanas e o
  relatório deixa de correr sem ninguém perceber porquê.
- **A conta de anúncios tem de estar atribuída ao utilizador de sistema.** Sem
  isso o token é válido, responde, e devolve zero contas. Parece avaria e não é.

---

## Confirmar que ficou bom

```
<python> ~/.claude/kit/ferramentas/ghl_meta.py --diagnostico
```

Diz o que cada lado devolveu e o que falta. Corre isto antes de prometer
qualquer relatório.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
