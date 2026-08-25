# PowerScale Skills Kit: esta bem instalado?
#   powershell -ExecutionPolicy Bypass -File .\verificar.ps1
#   powershell -ExecutionPolicy Bypass -File .\verificar.ps1 -Nivel instalacao
param([string]$Nivel = "completo")
$ErrorActionPreference = "Stop"
$kit = $PSScriptRoot
foreach ($t in @(@("py","-3"), @("python3"), @("python"))) {
  $exe = $t[0]; $args = @(); if ($t.Count -gt 1) { $args = $t[1..($t.Count-1)] }
  try {
    $v = & $exe @args "-V" 2>&1
    if ("$v" -match "^Python 3") {
      & $exe @($args + @((Join-Path $kit "ferramentas\verificar.py"), "--nivel", $Nivel))
      exit $LASTEXITCODE
    }
  } catch {}
}
Write-Host "Sem Python 3 nesta maquina. Instala com: winget install Python.Python.3.12" -ForegroundColor Red
exit 1
