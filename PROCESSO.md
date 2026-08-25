# O processo de arranque

Índice das fases. Quem lê isto é o Claude, não a pessoa.

Lê **uma fase de cada vez**, quando entras nela. Não leias as seguintes: o
processo é para ser executado passo a passo com uma pessoa do outro lado, não
lido de uma ponta à outra e despachado em bloco.

## Regras de conduta (valem nas oito fases)

1. **Corres tu os comandos.** Ela não escreve nenhum. Se lhe apeteceu escrever
   um comando, o processo falhou.
2. **Um passo de cada vez.** Uma frase a dizer o que vais fazer, fazes, mostras
   a prova, avanças. Nunca cinco comandos de rajada.
3. **Nunca a deixes bloqueada.** Se falha, diagnosticas e resolves. Só a chamas
   quando é mesmo da pessoa (uma password, um clique, uma decisão).
4. **Português simples.** "Vou buscar as fontes", não "vou copiar os assets para
   o diretório de destino".
5. **Não assumas que ficou feito.** Verifica com um comando e mostra o resultado.
6. **Português de Portugal. Zero travessão.**
7. **Grava o estado ao fim de cada fase.** Se a conversa morrer, a seguinte
   retoma onde ias, e a pessoa não repete nada.

## As fases

| # | Fase | Ficheiro | O que produz | Está feita quando |
|---|---|---|---|---|
| 0 | Preparar | `processo/0-preparar.md` | sabemos que máquina é esta | `estado.json` existe com o SO e o comando do Python |
| 1 | Pré-requisitos | `processo/1-prerrequisitos.md` | o que falta, instalado | Python 3 e Claude respondem |
| 2 | Instalar | `processo/2-instalar.md` | skills, fontes, permissões, cofre | `verificar.py --nivel instalacao` sai 0 |
| 3 | Descobrir | `processo/3-descobrir.md` | o retrato do negócio | `perfil.descoberta.fonte` preenchido |
| 4 | Entrevista | `processo/4-entrevista.md` | o perfil da pessoa | `estado.py --falta` não devolve nada |
| 5 | Perfil | `processo/5-perfil.md` | o `CLAUDE.md` da pessoa e as pastas | o ficheiro tem o nome e a oferta lá dentro |
| 6 | Verificar | `processo/6-verificar.md` | PRONTO, e a imagem de prova | `verificar.py --nivel completo` sai 0 ou 2 |
| 7 | Primeiro trabalho | `processo/7-primeiro-trabalho.md` | uma coisa real feita | existe um entregável que a pessoa pode usar hoje |

Se alguma coisa falhar, `processo/problemas.md` antes de lhe perguntares seja o
que for.

## Como saber onde estás

```
<python> ~/.claude/kit/ferramentas/estado.py --mostrar
```

Mostra as fases feitas, a próxima, e o que falta no perfil. É a primeira coisa a
correr em qualquer sessão em que retomes isto.

## O reinício da sessão

As skills só são lidas quando a sessão do Claude arranca. Por isso o reinício
pede-se **uma vez só, no fim da fase 6**, e nunca antes.

Depois do reinício ninguém precisa de se lembrar de nada: reabre-se o Claude na
pasta, tu lês o estado, vês as fases 0 a 6 feitas e continuas na 7 sozinho.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
