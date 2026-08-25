# Fase 0: preparar

**Objetivo:** saber que máquina é esta antes de lhe tocar.

**Pré-condição:** nenhuma. É por aqui que se começa.

## Passos

1. Diz-lhe, numa frase, o que vai acontecer: "vou instalar o kit, fazer-te umas
   perguntas sobre o teu negócio, e no fim fazemos já uma coisa a sério. Uns 20
   minutos. Não precisas de escrever nada."

2. Vê onde estás e o que é esta máquina:

   ```
   Windows:  systeminfo | findstr /B /C:"OS Name"  ;  $PSVersionTable.PSVersion
   Mac:      sw_vers ; echo $SHELL
   ```

3. Descobre a pasta de documentos real. **No Windows pode estar redirecionada
   para o OneDrive**, e é aí que a pasta de trabalho dela deve nascer, não numa
   `Documents` local que nunca sincroniza.

   ```
   Windows:  [Environment]::GetFolderPath("MyDocuments")
   Mac:      echo "$HOME/Documents"
   ```

4. Grava o que descobriste:

   ```
   <python> ferramentas/estado.py --responder maquina.so="Windows 11"
   <python> ferramentas/estado.py --responder maquina.terminal="PowerShell"
   <python> ferramentas/estado.py --responder maquina.gestor_pacotes="winget"
   <python> ferramentas/estado.py --marcar preparar=feita
   ```

**Está feita quando:** o `estado.json` existe e sabes o sistema operativo, o
terminal e onde ficam os documentos dela.

<!-- powerscale-skills-kit -->

---

Distribuído no **PowerScale Skills Kit** · powerscale.pro
