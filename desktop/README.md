### Requisitos

1. Windows Pro (Pro, Enterprise o Education)

---

### Instalación de VM

1. Habilitar Hyper-V. En la termina de PowerShell (con permisos de administrador):
``` PowerShell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

2. Instalar [Vagrant](https://developer.hashicorp.com/vagrant/install). (Al teminar de instalar se necesita reiniciar la computadora)

3. **Configuración Inicial:** 
Antes de levantar la máquina virtual, puedes personalizar la red y las especificaciones editando el archivo `config.json`. En este archivo puedes definir:
* **IP de la VM:** (Ej. `192.168.0.200`)
* **MAC Address:** Para reservar la IP en tu router.
* **Bridge:** El nombre de tu switch virtual de Hyper-V (Ej. `RedPuente`).
* **SyncFolder:** La ruta en Windows que se sincronizará con la VM.

4. **Instalación Rápida (Crear accesos directos):**
Para no tener que usar la consola manualmente cada vez, da clic derecho sobre el archivo `install.ps1` y selecciona **"Ejecutar con PowerShell"**.
Este script automáticamente:
* Verificará y creará la carpeta de sincronización en tu escritorio.
* Creará un acceso directo llamado **"Iniciar Vagrant"** en tu escritorio.

---

### Uso de la VM

Para iniciar o encender la máquina virtual, simplemente haz **doble clic en el acceso directo "Iniciar Vagrant"** que se creó en tu escritorio.

* Este acceso directo te pedirá permisos de administrador (requerido por Hyper-V).
* Verificará el estado de tu máquina.
* Si no existe, la creará (`vagrant up`). Si ya existe y está apagada, la encenderá.
* Te arrojará ventanas informativas avisándote si ocurrió algún error o si se encendió exitosamente.

Alternativamente, puedes ejecutar el script principal directamente desde PowerShell:
```powershell
.\main.ps1
```

### Notas Adicionales

* Si la VM ya está activa y solo quieres aplicar cambios recientes del playbook de Ansible sin reiniciar la máquina, puedes ejecutar en la terminal (dentro de esta carpeta):
  ```powershell
  vagrant provision
  ```
* Para revisar que la VM se creó correctamente y está corriendo, puedes ejecutar en PowerShell (como administrador):
  ```powershell
  Get-VM
  ```
  O verificar visualmente desde el **Administrador de Hyper-V**.