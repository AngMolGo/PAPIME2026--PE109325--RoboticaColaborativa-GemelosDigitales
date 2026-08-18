# =========================================================
# ETAPA 1: "builder" (Tu taller de desarrollo y compilación)
# =========================================================
# Le ponemos el "apellido" AS builder para poder llamarlo después
FROM ros:humble AS builder

# Evitar que apt-get pida confirmaciones interactivas
ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar las herramientas base que pedía el script (sin borrar repositorios)
RUN apt-get update && apt-get install -yq \
    curl \
    wget \
    gnupg \
    lsb-release \
    openssl \
    build-essential \
    git \
    python3-pip \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    python3-colcon-common-extensions \
    build-essential \
    software-properties-common \
    # Instalación de package oficial de UR para ROS2.
    ros-humble-ur \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws
COPY . /ros2_ws/

# 3. Instalamos dependencias y compilamos
RUN apt-get update && rosdep install --from-paths src --ignore-src -y
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install


### La etapa de runtime será problema del Ángel del futuro :v

# =========================================================
# ETAPA 2: "runtime" (El producto final empacado)
# =========================================================
# Empezamos desde una imagen limpia y ultraligera que NO tiene compiladores
FROM ros:humble-ros-core AS runtime

WORKDIR /ros2_ws

# LA MAGIA OCURRE AQUÍ:
# Viajamos en el tiempo a la Etapa 1 (builder) y le "robamos"
# EXCLUSIVAMENTE la carpeta donde quedaron los binarios ya compilados.
COPY --from=builder /ros2_ws/install /ros2_ws/install

# Configuramos cómo debe arrancar el robot
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["ros2", "launch", "7dof_surgical_core", "robot_orquestador.launch.py"]

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
