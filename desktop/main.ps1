# Cargar ensamblado para las ventanas emergentes (sólo para errores)
Add-Type -AssemblyName PresentationFramework

function Show-Error {
    param([string]$Message)
    [System.Windows.MessageBox]::Show($Message, "Error Crítico - Vagrant", "OK", "Error")
    exit 1
}

$scriptDir = Split-Path $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 1. Leer archivo de configuración
$configFile = Join-Path $scriptDir "config.json"
if (-Not (Test-Path $configFile)) {
    Show-Error "No se encontró el archivo de configuración: config.json"
}

try {
    $config = Get-Content $configFile -Raw | ConvertFrom-Json
} catch {
    Show-Error "El archivo config.json tiene un formato inválido o está corrupto."
}

# 2. Validar el estado de Vagrant de forma silenciosa
try {
    $statusOutput = vagrant status --machine-readable 2>&1
} catch {
    Show-Error "No se pudo ejecutar el comando 'vagrant'. Asegúrate de que Vagrant está instalado y en el PATH."
}

$isRunning = $false

foreach ($line in $statusOutput) {
    if ($line -match "^\d+,default,state,(.+)$") {
        $state = $matches[1]
        if ($state -eq "running") {
            $isRunning = $true
        }
    }
}

# 3. Lógica de encendido o creación
if (-Not $isRunning) {
    # Si no está prendida (ya sea porque está apagada o porque no se ha creado), se hace vagrant up
    # Start-Process con -WindowStyle Hidden ejecutará Vagrant completamente en segundo plano
    $process = Start-Process vagrant -ArgumentList "up" -Wait -WindowStyle Hidden -PassThru

    # Solo mostramos ventana emergente si ocurre un error real que detenga el proceso
    if ($process.ExitCode -ne 0) {
        Show-Error "Ocurrió un error crítico al intentar encender/crear la máquina virtual (Exit Code: $($process.ExitCode)).`n`nAbre una terminal manualmente y corre 'vagrant up' para ver los detalles del error."
    }
}

# 4. Abrir el navegador con la IP configurada
$url = "http://$($config.Network.IP):6080/vnc.html"
Start-Process $url

# 5. Abrir la GUI de Python si no está corriendo
$pythonExe = Join-Path $scriptDir ".venv\Scripts\pythonw.exe"
if (Test-Path $pythonExe) {
    $pyProcesses = Get-WmiObject Win32_Process -Filter "name='python.exe' or name='pythonw.exe'" | Where-Object { $_.CommandLine -match "main\.py" }
    if (-Not $pyProcesses) {
        Start-Process $pythonExe -ArgumentList "main.py" -WorkingDirectory $scriptDir
    }
}

exit 0
