# Fase 5: escrever o perfil

**Objetivo:** o ficheiro de instruções dela, e as pastas onde vai trabalhar.

**Pré-condição:** fase 4 feita.

## Passos

1. Escreve o `CLAUDE.md`:

   ```
   <python> ferramentas/gerar_perfil.py
   ```

   O que sai fica entre `<!-- kit:inicio -->` e `<!-- kit:fim -->`. **Tudo o que
   ela escrever fora desses marcadores sobrevive** a uma nova geração. É por
   isso que se pode voltar a correr isto sem medo.

   Se faltar alguma resposta, o comando recusa e diz qual. Volta à fase 4 para
   essa, e só para essa.

2. **Lê o que saiu** e mostra-lhe as duas ou três linhas que mais importam: quem
   ele acha que ela é, o que vende, e os travões. É o momento de ela corrigir.

3. Cria as pastas de trabalho, dentro da pasta de documentos real dela (atenção
   ao OneDrive no Windows):

   ```
   <Negócio>/
     clientes/
       <cliente>/
         voz.md          Voice Bible, skill voz-de-marca
         calls/
         copy/
         ads/
         pagina/
     meu/                o negócio dela
   ```

   **Só as pastas dos clientes que existem hoje.** Pasta vazia a mais é ruído.
   As chaves nunca vão para aqui: vivem no cofre.

   ```
   <python> ferramentas/estado.py --responder maquina.pasta_trabalho="C:\Users\...\Documents\Negocio"
   ```

4. Marca a fase:

   ```
   <python> ferramentas/estado.py --marcar perfil=feita
   ```

**Está feita quando:** o `~/.claude/CLAUDE.md` fala dela pelo nome, diz o que ela
vende, e não tem um único marcador por preencher.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
