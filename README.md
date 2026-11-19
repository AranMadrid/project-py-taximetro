# 🚕 Taxímetro digital

Prototipo de taxímetro desarrollado en Python para TaxiTech Solutions.

**Fase 1: MVP funcional (US-01 a US-04).**

El programa permite iniciar una carrera, cambiar entre parado y movimiento, calcular el importe según el tiempo transcurrido y mostrar el total al finalizar.

También permite empezar nuevas carreras sin cerrar el programa.

## Cómo arrancarlo

Necesitas tener instalado Python 3.10 o superior.

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python taximetro.py
```

## Cómo se usa

Al iniciar el programa aparece un menú de ayuda.

Escribe una de las siguientes letras y pulsa Intro:

| Orden | Qué hace |
|---|---|
| i | Inicia una carrera con el taxi parado |
| p | Indica que el taxi está parado |
| m | Indica que el taxi está en movimiento |
| f | Finaliza la carrera y muestra el total |
| a | Muestra el menú de ayuda |
| s | Sale del programa |

### Tarifas

- **Taxi parado:** 0,02 € por segundo.
- **Taxi en movimiento:** 0,05 € por segundo.

### Cómo se calcula el importe

El programa divide la carrera en tramos según el estado del taxi.

Cuando cambiamos de parado a movimiento, o viceversa, calcula cuánto ha costado el tramo anterior.

Para calcularlo, multiplica los segundos transcurridos por la tarifa correspondiente.

Después suma ese importe al dinero acumulado.

Al finalizar la carrera, calcula el último tramo y muestra el total en euros con dos decimales.

## Decisiones técnicas

- **Python:** lo utilizamos para desarrollar el programa porque permite crear un taxímetro sencillo desde la terminal.
- **Un solo archivo (`taximetro.py`):** mantenemos todo el código en un mismo fichero porque esta primera fase es pequeña y así resulta más fácil entenderlo.
- **`time.monotonic()`:** lo usamos para medir el tiempo transcurrido porque no se ve afectado por cambios en la hora del sistema, a diferencia de `time.time()`.
- **Diccionario `carrera`:** guarda el estado del taxi, cuándo empezó el tramo y cuánto dinero lleva acumulado.
- **Funciones:** utilizamos `tarifa()` y `cerrar_tramo()` para separar el cálculo de las tarifas del resto del programa.
- **Comprobaciones:** evitamos errores cuando el conductor introduce órdenes que no corresponden, como intentar terminar una carrera que no existe.

---

## Fase 2

En esta fase hemos añadido nuevas funciones al taxímetro: podemos cambiar las tarifas sin modificar el código, guardar las carreras, consultar las del día y registrar lo que ocurre en un archivo de log.

También hemos creado pruebas automáticas para comprobar que los cálculos funcionan correctamente.

### Cómo cambiar las tarifas

Las tarifas se guardan en el archivo `config.json`, que está en la misma carpeta que `taximetro.py`.

Su contenido es:

```json
{
    "tarifa_parado": 0.02,
    "tarifa_movimiento": 0.05
}
```

Para cambiar una tarifa, abrimos el archivo, modificamos el precio y guardamos los cambios.

**Las nuevas tarifas se aplican al volver a arrancar el taxímetro**, porque el programa lee el JSON al iniciarse.

Si el archivo no existe o tiene algún error, el taxímetro utiliza las tarifas por defecto para poder seguir funcionando.

### Historial de carreras

Cada vez que terminamos una carrera con la orden `f`, sus datos se guardan automáticamente en `historial.csv`.

Este archivo está en la misma carpeta que `taximetro.py` y guarda la fecha, la hora de inicio, la duración en segundos y el importe total.

Las carreras nuevas se añaden al final, sin borrar las anteriores.

También hemos añadido la orden `h`, que permite ver las carreras realizadas hoy y el dinero total acumulado durante el día.

Si hoy no hay carreras registradas, el programa muestra un mensaje indicándolo.

### Registro de eventos (log)

El archivo `taximetro.log`, situado junto a `taximetro.py`, registra lo que ocurre durante el funcionamiento del programa.

Por ejemplo, cuándo se inicia el taxímetro, cuándo empieza una carrera, los cambios de estado, cuándo se guarda una carrera y los posibles errores o avisos.

Para ver el log en tiempo real desde PowerShell, abrimos una terminal en la carpeta del proyecto y ejecutamos:

```powershell
Get-Content taximetro.log -Wait
```

Así podemos ver los nuevos registros mientras utilizamos el taxímetro en otra terminal.

Para dejar de seguir el log, pulsamos `Ctrl + C`.

### Pruebas automáticas con pytest

Hemos creado el archivo `test_taximetro.py` para comprobar que los cálculos de las tarifas funcionan correctamente.

Primero preparamos un entorno virtual para el proyecto:

```powershell
python -m venv .venv
```

En Windows, lo activamos desde PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Después instalamos pytest:

```powershell
pip install pytest
```

Podemos comprobar la instalación con:

```powershell
python -m pytest --version
```

Para ejecutar todas las pruebas utilizamos:

```powershell
python -m pytest
```

Hemos preparado cuatro pruebas que comprueban:

- Que 10 segundos parado cuestan 0,20 €.
- Que 10 segundos en movimiento cuestan 0,50 €.
- Que el programa lanza un error si recibe segundos negativos.
- Que una carrera mixta de 10 segundos parado y 10 segundos en movimiento cuesta 0,70 €.

También hemos provocado un fallo a propósito para aprender a interpretar los errores que muestra pytest.

**Resultado final: `4 passed`.** Las cuatro pruebas se han superado correctamente.
