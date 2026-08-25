# PowerScale Skills Kit, instalador (Windows).
#   powershell -ExecutionPolicy Bypass -File .\instalar.ps1
#   powershell -ExecutionPolicy Bypass -File .\instalar.ps1 -Verificar
#
# Este script nao tem um unico acento de proposito: o PowerShell 5.1 grava
# UTF-8 com BOM e estraga texto acentuado. Tudo o que tem acentos e escrito
# por Python. Aqui so se verificam binarios, se copiam ficheiros e se chama
# o Python.

param([switch]$Verificar)

$ErrorActionPreference = "Stop"
$kit    = $PSScriptRoot
$claude = Join-Path $HOME ".claude"
$skills = Join-Path $claude "skills"
$assets = Join-Path $claude "kit-assets"
$kitdir = Join-Path $claude "kit"
$cofre  = Join-Path $HOME ".config\chaves"
$stamp  = Get-Date -Format "yyyy-MM-dd-HHmm"

function Diz($t)   { Write-Host $t }
function Ok($t)    { Write-Host "  ok     $t" -ForegroundColor Green }
function Falta($t) { Write-Host "  falta  $t" -ForegroundColor Yellow }
function Erro($t)  { Write-Host "  ERRO   $t" -ForegroundColor Red }

Diz ""
Diz "PowerScale Skills Kit"
Diz "====================="
Diz ""

# Tira a marca de "ficheiro vindo da internet", que faz o Windows recusar correr
# o que veio dentro de um ZIP.
try { Get-ChildItem -Path $kit -Recurse -File | Unblock-File -ErrorAction SilentlyContinue } catch {}

# --------------------------------------------------------- 1. a maquina
# ATENCAO ao stub da Microsoft Store: "python.exe" existe no PATH, responde ao
# Get-Command, abre a loja e NAO e um interpretador. Por isso se testa a serio,
# a correr o comando e a ler a versao.
function Achar-Python {
  foreach ($tentativa in @(@("py","-3"), @("python3"), @("python"))) {
    $exe = $tentativa[0]
    $args = @()
    if ($tentativa.Count -gt 1) { $args = $tentativa[1..($tentativa.Count-1)] }
    try {
      $saida = & $exe @args "-V" 2>&1
      if ("$saida" -match "^Python 3") {
        return @{ cmd = (@($exe) + $args) -join " "; exe = $exe; args = $args; versao = "$saida".Trim() }
      }
    } catch {}
  }
  return $null
}

$py = Achar-Python
$emFalta = @()

Diz "A maquina:"
if ($py) { Ok ("Python 3 (" + $py.cmd + ", " + $py.versao + ")") }
else { Falta "Python 3  ->  winget install Python.Python.3.12"; $emFalta += "python" }

foreach ($f in @("claude","node","git","ffmpeg")) {
  if (Get-Command $f -ErrorAction SilentlyContinue) { Ok $f }
  else {
    $como = switch ($f) {
      "claude" { "npm install -g @anthropic-ai/claude-code" }
      "node"   { "winget install OpenJS.NodeJS.LTS" }
      "git"    { "winget install Git.Git" }
      "ffmpeg" { "winget install Gyan.FFmpeg  (so para transcrever calls)" }
    }
    Falta "$f  ->  $como"
    $emFalta += $f
  }
}
Diz ""

if ($Verificar) {
  Diz "Modo verificacao. Nada foi instalado."
  if ($emFalta.Count -gt 0) { Diz ("Em falta: " + ($emFalta -join ", ")) }
  exit 0
}

if (-not $py) {
  Erro "Sem Python 3 nao da para continuar: e ele que escreve o teu CLAUDE.md."
  Diz  "         Instala com: winget install Python.Python.3.12"
  exit 1
}
if (($emFalta -contains "claude") -and (-not (Test-Path $claude))) {
  Erro "Nao encontro o Claude Code nesta maquina."
  exit 1
}

function Py($argumentos) { & $py.exe @($py.args + $argumentos) }

# --------------------------------------------------------- 2. pastas
New-Item -ItemType Directory -Force -Path $skills, $assets, $kitdir, $cofre | Out-Null

# --------------------------------------------------------- 3. skills
# O que ela tiver alterado e guardado antes de escrever por cima.
$guardadas = Join-Path $kitdir "skills-alteradas"
$alteradas = 0
Get-ChildItem (Join-Path $kit "skills") -Directory | ForEach-Object {
  $destino = Join-Path $skills $_.Name
  if (Test-Path $destino) {
    $antes  = (Get-ChildItem $destino -Recurse -File | Get-FileHash | Select-Object -ExpandProperty Hash) -join ""
    $agora  = (Get-ChildItem $_.FullName -Recurse -File | Get-FileHash | Select-Object -ExpandProperty Hash) -join ""
    if ($antes -ne $agora) {
      $alvo = Join-Path $guardadas $stamp
      New-Item -ItemType Directory -Force -Path $alvo | Out-Null
      Copy-Item $destino (Join-Path $alvo $_.Name) -Recurse -Force -ErrorAction SilentlyContinue
      $alteradas++
    }
    Remove-Item $destino -Recurse -Force
  }
  Copy-Item $_.FullName $destino -Recurse
}
if ($alteradas -gt 0) { Ok "$alteradas skill(s) que tinhas mexido: copia em $guardadas\$stamp" }

$esperado = (Get-ChildItem (Join-Path $kit "skills") -Directory | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }).Count
$instaladas = 0
Get-ChildItem (Join-Path $kit "skills") -Directory | ForEach-Object {
  if (Test-Path (Join-Path (Join-Path $skills $_.Name) "SKILL.md")) { $instaladas++ }
}
if ($instaladas -ne $esperado) {
  Erro "instalei $instaladas skills mas o kit tem $esperado. Nao continues sem perceber porque."
  exit 1
}
Ok "$instaladas skills em $skills"

# --------------------------------------------------------- 4. assets
Copy-Item (Join-Path $kit "assets\*") $assets -Recurse -Force
Ok "fontes e logotipos em $assets"

# --------------------------------------------------------- 5. o processo
# Vai para ~/.claude/kit para o arranque sobreviver a mudares esta pasta de
# sitio, ou a apaga-la depois de instalar.
foreach ($p in @("processo","modelo","ferramentas")) {
  $destino = Join-Path $kitdir $p
  if (Test-Path $destino) { Remove-Item $destino -Recurse -Force }
  Copy-Item (Join-Path $kit $p) $destino -Recurse
}
foreach ($f in @("PROCESSO.md","manifesto.json","VERSAO")) {
  if (Test-Path (Join-Path $kit $f)) { Copy-Item (Join-Path $kit $f) $kitdir -Force }
}
Ok "processo e ferramentas em $kitdir"

# --------------------------------------------------------- 6. permissoes
$settings = Join-Path $claude "settings.json"
if (Test-Path $settings) {
  Copy-Item $settings "$settings.backup-$stamp"
  Falta "ja tinhas um settings.json (copia em settings.json.backup-$stamp)"
  Diz   "         O Claude junta os dois na fase de instalacao. Nao fica nada por fundir."
} else {
  Copy-Item (Join-Path $kit "settings.json") $settings
  Ok "permissoes instaladas"
}

# --------------------------------------------------------- 7. cofre
$secrets = Join-Path $cofre "secrets.env"
if (-not (Test-Path $secrets)) {
  # Escrito por Python para nao levar BOM.
  Py @((Join-Path $kit "ferramentas\estado.py"), "--mostrar") | Out-Null
  [System.IO.File]::WriteAllText($secrets, "# Uma chave por linha, NOME=valor. Nunca colar chaves no chat.`n", (New-Object System.Text.UTF8Encoding($false)))
  Ok "cofre de chaves criado em $secrets"
} else {
  Ok "cofre de chaves ja existia"
}
# So o utilizador atual le o cofre. E o equivalente ao chmod 600 do Mac.
try {
  & icacls $secrets /inheritance:r /grant:r "$($env:USERNAME):(R,W)" | Out-Null
} catch { Falta "nao consegui restringir as permissoes do cofre" }

# --------------------------------------------------------- 8. estado
$estado = Join-Path $kit "ferramentas\estado.py"
$versao = "?"
if (Test-Path (Join-Path $kit "VERSAO")) { $versao = (Get-Content (Join-Path $kit "VERSAO") -Raw).Trim() }
Py @($estado, "--definir", "python_cmd=$($py.cmd)")   | Out-Null
Py @($estado, "--definir", "kit_caminho=$kit")        | Out-Null
Py @($estado, "--definir", "kit_versao=$versao")      | Out-Null
Py @($estado, "--definir", "origem=zip")              | Out-Null
Py @($estado, "--marcar", "instalar=feita")           | Out-Null
Ok "estado da instalacao gravado"

Diz ""
Diz "Instalado. O Claude continua daqui: fase seguinte em PROCESSO.md."
Diz "PowerScale Skills Kit  |  powerscale.pro"
Diz ""
