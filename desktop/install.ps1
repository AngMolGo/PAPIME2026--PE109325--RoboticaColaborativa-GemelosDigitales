$scriptDir = Split-Path $MyInvocation.MyCommand.Path
Set-Location $scriptDir
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Requiere elevación para registrar la tarea programada
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Elevando privilegios para configurar el inicio silencioso..."
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -NoExit -File `"$($MyInvocation.MyCommand.Path)`""
    exit
}

Write-Host "--- Iniciando Instalación ---"

# 1. Crear la carpeta de sincronización
$configFile = Join-Path $scriptDir "config.json"
if (Test-Path $configFile) {
    $config = Get-Content $configFile -Raw | ConvertFrom-Json
    $syncFolder = $config.SyncFolder.HostPath
} else {
    $syncFolder = Join-Path $desktopPath "UR_ws"
}

if (-Not (Test-Path $syncFolder)) {
    Write-Host "Creando la carpeta de sincronización en: $syncFolder"
    try {
        New-Item -ItemType Directory -Force -Path $syncFolder | Out-Null
        Write-Host "Carpeta creada con éxito."
    } catch {
        Write-Host "Error al crear la carpeta. Verifica tus permisos." -ForegroundColor Red
    }
} else {
    Write-Host "La carpeta de sincronización ya existe en: $syncFolder"
}

# 2. Inicializar la Máquina Virtual
Write-Host ""
Write-Host "Iniciando instalación de la máquina virtual con Vagrant..."
Write-Host "Esto puede tardar varios minutos dependiendo de tu conexión y equipo."
$process = Start-Process vagrant -ArgumentList "up" -Wait -NoNewWindow -PassThru
if ($process.ExitCode -ne 0) {
    Write-Host "ERROR: Hubo un problema al crear la máquina virtual. Revisa el texto superior." -ForegroundColor Red
} else {
    Write-Host "¡Máquina virtual creada e inicializada correctamente!" -ForegroundColor Green
}

# 3. Truco de la Tarea Programada para evitar UAC
Write-Host ""
Write-Host "Configurando la Tarea Programada para evitar la pantalla de permisos (UAC)..."
$taskName = "IniciarVagrantTask_PAPIME26"
$targetScript = Join-Path $scriptDir "main.ps1"
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$targetScript`""
# LogonType Interactive asegura que Vagrant vea el entorno del usuario correctamente
$principal = New-ScheduledTaskPrincipal -UserId $currentUser -LogonType Interactive -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0
$task = New-ScheduledTask -Action $action -Principal $principal -Settings $settings

Register-ScheduledTask -TaskName $taskName -InputObject $task -Force | Out-Null
Write-Host "Tarea programada '$taskName' registrada con éxito."

# 4. Crear el acceso directo en el escritorio apuntando a la tarea programada
$shortcutPath = Join-Path $desktopPath "Iniciar Vagrant.lnk"
Write-Host "Creando acceso directo oculto en: $shortcutPath"
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)

# El acceso directo llamará a schtasks para ejecutar la tarea sin preguntar
$Shortcut.TargetPath = "schtasks.exe"
$Shortcut.Arguments = "/run /tn `"$taskName`""
$Shortcut.WorkingDirectory = $scriptDir
# Configuración del icono
$iconFile = Join-Path $scriptDir "icon.ico"
if (Test-Path $iconFile) {
    # Si dejas un archivo 'icon.ico' en la carpeta, usará ese
    $Shortcut.IconLocation = $iconFile
} else {
    # Si no, usa el icono nativo de Windows para una computadora/servidor (imageres.dll, índice 109)
    $Shortcut.IconLocation = "$env:SystemRoot\System32\imageres.dll,109"
}
$Shortcut.WindowStyle = 7 # Minimized
$Shortcut.Description = "Enciende la Máquina Virtual de Vagrant silenciosamente"
$Shortcut.Save()

Write-Host ""
Write-Host "¡Instalación completada exitosamente!"
Write-Host "De ahora en adelante usa el acceso directo 'Iniciar Vagrant' para encenderla de forma 100% invisible."
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
