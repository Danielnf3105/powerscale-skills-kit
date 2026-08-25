# Fase 2: instalar

**Objetivo:** as skills, as fontes, as permissões e o cofre no sítio.

**Pré-condição:** fase 1 feita.

## Passos

1. Corre o instalador:

   ```
   Windows:  powershell -ExecutionPolicy Bypass -File .\instalar.ps1
   Mac:      ./instalar.sh
   ```

2. **Se já existia um `settings.json` ou um `CLAUDE.md`**, o instalador não
   escreve por cima: guarda uma cópia com a data e avisa. Nesse caso lê os dois,
   diz-lhe numa frase o que muda, e junta-os tu. Nunca deixes um ficheiro
   `.novo` órfão à espera que alguém se lembre dele.

3. Confirma que ficou bom:

   ```
   <python> ferramentas/verificar.py --nivel instalacao
   ```

   Tem de sair `0` ou `2`. Se sair `1`, resolve o que aparecer nas linhas
   `[FALHA]` antes de avançar. Cada uma traz a linha do que fazer.

4. Marca a fase:

   ```
   <python> ferramentas/estado.py --marcar instalar=feita
   ```

**Está feita quando:** a verificação de instalação passa.

**Não lhe peças para reiniciar o terminal agora.** Isso é só no fim da fase 6, e
uma vez só. Reiniciar aqui interrompe a conversa a meio por nada.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
