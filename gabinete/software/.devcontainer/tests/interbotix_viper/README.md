# Instalación de packages

Para realizar tests con el robot viper 300 de 6DOF:

1. Descargar las dependencias de paquetes:

```bash
cd ros2_ws # Nos regresamos al directorio principal
vcs import src/interbotix < src/pkg_pe26_launch/tests/interbotix_viper/dependencies.repos --recursive
```