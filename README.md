
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
