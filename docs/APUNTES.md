# Apuntes de Python — PC Monitor

Este documento es mi cuaderno personal de aprendizaje. Las secciones se irán completando únicamente cuando utilicemos esos conceptos en el proyecto.

## 1. Primer programa

El archivo `main.py` contiene una instrucción mínima para comprobar que Python puede ejecutar el proyecto:

```python
print("PC Monitor iniciado correctamente")
```

`print()` es una función integrada de Python que muestra información en la consola. En este primer paso aprendemos a:

- Ejecutar un archivo de Python.
- Mostrar un mensaje en la terminal.
- Usar una cadena de texto entre comillas.

### Ejemplo independiente

```python
print("Hola, Python")
```

## 2. Variables

Una variable es un nombre que usamos para guardar un valor y poder utilizarlo después.
En `main.py` usamos variables para describir el estado del proyecto:

```python
project_name = "PC Monitor"
project_version = 1
is_running = True
```

El signo `=` asigna un valor a una variable. El nombre de la variable debe describir
qué información contiene. En Python se acostumbra escribir nombres compuestos con
`snake_case`, usando guiones bajos.

## 3. Tipos de datos

Python permite guardar distintos tipos de datos. En esta etapa utilizamos:

```python
project_name = "PC Monitor"             # str: texto
project_version = 1                      # int: número entero
is_running = True                        # bool: verdadero o falso
planned_modules = ["CPU", "Memoria RAM"] # list: lista de valores
usage = 42.5                             # float: número decimal
snapshot = {"cpu": 42.5, "memory": 61.2} # dict: pares clave-valor
```

El tipo de dato importa porque determina qué operaciones podemos realizar con él.
Por ejemplo, una lista puede contener varios valores, un `bool` representa un
estado de sí/no y un diccionario permite acceder a valores mediante claves.

## 4. Funciones

Una función es un bloque de código con un nombre que podemos ejecutar cuando lo
necesitemos. Se define con `def` y puede recibir datos mediante parámetros:

```python
def show_project_status(name, version, running, modules):
    print("Proyecto:", name)
    print("Versión:", version)
    print("En ejecución:", running)
    print("Módulos planificados:", modules)
```

Los nombres entre paréntesis son parámetros. Cuando llamamos a la función,
le pasamos argumentos:

```python
show_project_status("PC Monitor", 1, True, ["CPU", "Memoria RAM"])
```

Esta función solo muestra información; otras funciones del proyecto sí usan
`return` para entregar un resultado:

```python
def get_cpu_usage():
    return 42.5
```

También podemos definir valores predeterminados para parámetros:

```python
def run_session(samples=3, delay=2):
    print(samples, delay)
```

Si no enviamos esos argumentos, Python utiliza los valores predeterminados.
Más adelante utilizaremos funciones para obtener datos reales del equipo.

### Conceptos aprendidos hasta ahora

- `print()` muestra información en la consola.
- Las variables guardan valores.
- `str`, `int`, `bool` y `list` son tipos de datos básicos.
- Las funciones agrupan instrucciones reutilizables.
- Los parámetros permiten que una función trabaje con datos variables.

## 5. Condicionales

Los condicionales permiten ejecutar código según una condición. Se escriben con
`if` y, cuando necesitamos la alternativa contraria, usamos `else`:

```python
if is_running:
    execution_status = "Activo"
else:
    execution_status = "Detenido"
```

Python ejecuta solo uno de los dos bloques. La indentación —los espacios al
inicio de cada línea— indica qué instrucciones pertenecen al condicional.

También usamos ciclos `for` para repetir una acción una cantidad determinada de
veces:

```python
for index in range(samples):
    snapshot = collect_snapshot()
```

`range(samples)` genera los índices desde `0` hasta `samples - 1`.

## 6. Imports y módulos

Un módulo es un archivo `.py` que contiene código relacionado. `main.py` importa
una función desde `monitor/system.py`:

```python
from monitor.system import get_system_status
```

La estructura significa: “desde el módulo `monitor.system`, importa la función
`get_system_status`”. Después podemos llamarla como si estuviera definida en
`main.py`.

El archivo `monitor/__init__.py` indica que `monitor` puede utilizarse como un
paquete de módulos.

### `__name__` y `__main__`

Python crea la variable especial `__name__` en cada módulo.

```python
if __name__ == "__main__":
    main()
```

Si ejecutamos `python main.py`, `__name__` vale `"__main__"` y se llama a
`main()`. Si otro archivo importa `main.py`, la condición es falsa y el programa
no se inicia automáticamente. Esto permite reutilizar funciones sin ejecutar
todo el archivo importado.

Los nombres con dobles guiones bajos se conocen informalmente como “dunder”.
Son nombres especiales que Python utiliza para comportamientos internos.

## 7. Manejo de errores

El bloque `try` contiene código que podría producir un error. `except` permite
responder si ese error ocurre:

```python
try:
    print(get_system_status())
except Exception as error:
    print("Ocurrió un error:", error)
```

`error` contiene información sobre el problema. En esta etapa usamos
`Exception` de forma general para aprender la estructura; más adelante será
mejor capturar tipos de error concretos cuando sepamos qué problemas pueden
ocurrir.

Para validar la configuración usamos `raise`:

```python
if samples < 1:
    raise ValueError("samples debe ser mayor que cero")
```

Esto detiene la ejecución y comunica que el valor recibido no es válido.

En las sesiones usamos `finally` para garantizar que el monitor vuelva al estado
detenido incluso si ocurre un error:

```python
try:
    ejecutar_sesion()
finally:
    self.is_running = False
```

### Ejemplo independiente

```python
try:
    number = int("texto")
except ValueError:
    print("El valor no se puede convertir a entero")
```

## 8. Archivos

Python puede crear, escribir y leer archivos. Usamos `Path` de la librería
estándar `pathlib` para representar una ruta:

```python
from pathlib import Path

report_path = Path("reports") / "system_report.txt"
report_path.write_text("Reporte", encoding="utf-8")
contenido = report_path.read_text(encoding="utf-8")
```

El operador `/` de `Path` une partes de una ruta de forma portable. `write_text()`
guarda texto y `read_text()` lo recupera. Especificamos `encoding="utf-8"` para
trabajar correctamente con caracteres como `ó` y `í`.

Antes de guardar creamos la carpeta si hace falta:

```python
report_path.parent.mkdir(exist_ok=True)
```

`exist_ok=True` evita que Python produzca un error si la carpeta ya existe.

### JSON

JSON es un formato de texto común para guardar datos estructurados. Python puede
convertir diccionarios y listas a JSON con `json.dumps()` y leerlos de nuevo con
`json.loads()`:

```python
import json

data = {"cpu": 42.5, "memory": 61.2}
text = json.dumps(data, indent=4)
data_again = json.loads(text)
```

PC Monitor guarda el historial y el resumen de una sesión en
`reports/session.json`. Cada muestra es un diccionario dentro de una lista.

### Datos de disco

`psutil.disk_usage()` recibe una ruta y devuelve información del espacio de la
partición que contiene esa ruta:

```python
usage = psutil.disk_usage(".")
print(usage.total, usage.used, usage.free, usage.percent)
```

Los valores de espacio vienen expresados en bytes. PC Monitor los convierte a
gigabytes para hacer el reporte más legible.

## 9. Librerías externas

Una librería externa es código creado por terceros que instalamos aparte de
Python. En este proyecto usamos `psutil` para consultar información del equipo:

```python
import psutil

cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
```

La dependencia se registra en `requirements.txt`:

```text
psutil==7.2.2
```

Fijar la versión ayuda a que diferentes instalaciones utilicen una versión
conocida. Se instala con:

```powershell
pip install -r requirements.txt
```

### Formateo de texto con f-strings

Para insertar valores dentro de texto usamos f-strings:

```python
usage = 42.567
message = f"Uso de CPU: {usage:.1f}%"
```

`.1f` indica que el número se muestra con un decimal.

El proyecto también utiliza módulos de la biblioteca estándar, que no necesitan
instalación externa:

- `datetime` para fechas y horas.
- `time` para esperar entre muestras.
- `statistics` para calcular promedios.
- `json` para guardar datos estructurados.

### Información del sistema

La librería estándar `platform` permite consultar datos del sistema operativo:

```python
import platform

operating_system = platform.system()
release = platform.release()
machine = platform.machine()
```

Usamos `socket.gethostname()` para obtener el nombre del equipo. Para calcular el
tiempo encendido restamos la hora de inicio del sistema a la hora actual:

```python
uptime_seconds = time.time() - psutil.boot_time()
```

La función `divmod()` ayuda a convertir segundos en días, horas, minutos y
segundos.

### Información de red

`socket.gethostbyname()` obtiene una dirección IPv4 asociada al hostname. Para
conocer todas las interfaces usamos `psutil.net_if_addrs()`:

```python
for name, addresses in psutil.net_if_addrs().items():
    print(name, addresses)
```

También usamos `psutil.net_io_counters()` para consultar los bytes enviados y
recibidos desde el inicio del sistema. Estos contadores son acumulados; no
representan la velocidad instantánea de la conexión.

Los resultados se convierten a diccionarios y listas antes de agregarlos al
historial, porque esos tipos pueden serializarse directamente a JSON.

### Procesos

`psutil.process_iter()` permite recorrer los procesos activos. Le pasamos una
lista de atributos para solicitar solo los datos que necesitamos:

```python
for process in psutil.process_iter(["pid", "name", "memory_percent"]):
    print(process.info)
```

Un proceso puede terminar justo mientras lo consultamos o puede no permitir
acceso a sus datos. Por eso `monitor/processes.py` captura errores como
`NoSuchProcess`, `AccessDenied` y `ZombieProcess`, y continúa con el siguiente.

Los procesos se ordenan por `memory_percent` y se conserva únicamente la
cantidad solicitada mediante `limit`.

## 10. Programación orientada a objetos

La programación orientada a objetos permite agrupar datos y comportamientos
relacionados dentro de una clase. En el proyecto usamos la clase `PCMonitor`:

```python
class PCMonitor:
    def __init__(self, name, report_path):
        self.name = name
        self.report_path = report_path

    def get_name(self):
        return self.name
```

`class` define una clase. `__init__` es un método especial que Python ejecuta
cuando se crea un objeto. `self` representa el objeto actual y permite guardar
datos en sus atributos.

Creamos un objeto pasando argumentos al constructor:

```python
monitor = PCMonitor("PC Monitor", report_path)
```

En este caso `monitor` es un objeto de tipo `PCMonitor`. Sus métodos se llaman
con punto:

```python
monitor.save_current_report()
```

La clase `PCMonitor` coordina las funciones existentes de CPU, memoria, sistema
y reportes. La clase no necesita conocer todos los detalles internos de cada
módulo; delega cada responsabilidad en la función correspondiente.

### Diferencia entre función y método

Una función puede existir por sí sola:

```python
get_cpu_usage()
```

Un método es una función definida dentro de una clase y normalmente trabaja con
los atributos del objeto:

```python
monitor.create_report()
```
