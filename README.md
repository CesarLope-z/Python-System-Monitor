# PC Monitor

Herramienta de línea de comandos escrita en Python para aprender a monitorear información básica de una computadora.

## Objetivo

Construir progresivamente un proyecto real para portafolio, empezando por una estructura sencilla y agregando funcionalidades de monitoreo de forma incremental.

## Estado actual

El proyecto contiene una base educativa de consola con variables, condicionales,
funciones, módulos, manejo básico de errores y una clase coordinadora. Actualmente
recopila el uso de CPU y memoria RAM, genera alertas configurables y guarda
reportes de texto y JSON.

## Estructura del proyecto

```text
pc-monitor/
├── main.py
├── monitor/
│   ├── __init__.py
│   ├── cpu.py
│   ├── memory.py
│   ├── disk.py
│   ├── network.py
│   ├── pc_monitor.py
│   ├── report.py
│   └── system.py
├── reports/
├── docs/
│   └── APUNTES.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Tecnologías

- Python 3
- Entorno virtual de Python (`.venv`)
- psutil

## Instalación

1. Clona o descarga este repositorio.
2. Crea y activa un entorno virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

> Nota: en el entorno usado para preparar esta versión, Python 3.14 no pudo incluir `pip` automáticamente al crear `.venv`. Si ocurre en otra instalación, utiliza un `pip` compatible para instalar las dependencias dentro del entorno virtual.

## Uso

Con el entorno virtual activado, ejecuta:

```powershell
python main.py
```

La versión actual muestra el nombre, el autor, la versión, el estado de ejecución,
los límites configurados, el uso de CPU y el uso de memoria RAM. Durante una
sesión puede mostrar alertas, calcular promedios y máximos, y guardar:

- Un reporte legible en `reports/system_report.txt`.
- El historial completo y el resumen en `reports/session.json`.

Salida esperada:

```text
Proyecto: PC Monitor
Autor: Cesar Lopez
Versión: 1
Estado: Detenido
Módulos planificados: ['CPU', 'Memoria RAM', 'Discos']
Sistema: status: OK

Reporte guardado en: reports\system_report.txt
Contenido del reporte:
PC Monitor - Reporte básico
Uso de CPU: 12.3%
Uso de memoria RAM: 48.7%
Fecha y hora: 2026-09-18T22:39:28

Resumen de la sesión: {'samples': 3, 'cpu_average': 45.2, 'cpu_max': 81.4, 'memory_average': 48.7, 'memory_max': 50.1}
Sesión JSON guardada en: reports\session.json
```

## Roadmap

- [x] Crear la primera función de monitoreo de CPU.
- [x] Agregar información de memoria RAM.
- [ ] Agregar información de discos.
- [ ] Agregar información del sistema y la red.
- [x] Incorporar alertas de CPU y memoria.
- [x] Generar reportes.
- [ ] Evaluar una interfaz gráfica y almacenamiento de datos.

## Aprendizaje

El archivo [docs/APUNTES.md](docs/APUNTES.md) funciona como cuaderno personal para registrar los conceptos de Python utilizados durante el desarrollo.
