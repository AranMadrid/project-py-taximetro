
# importamos librerías necesarias
import time

# permite crear registros de eventos que ocurren durante la ejecución del programa
import logging

# PASO 2: Importamos json para leer las tarifas del archivo
import json

# PASO 2: Importamos Path para encontrar los archivos
from pathlib import Path

# Creamos un logger (como una libreta) para registrar lo que ocurre en el taxímetro
log = logging.getLogger("taximetro")

# creamos constantes para las tarifas por defecto del taxímetro
TARIFAS_POR_DEFECTO = {
    "tarifa_parado": 0.02,
    "tarifa_movimiento": 0.05
}

# Creamos constantes para las tarifas que se van a usar en el programa
CARPETA = Path(__file__).parent

# configuramos las tarifas por defecto para el taxímetro
CONFIG = CARPETA / "config.json"
LOG = CARPETA / "taximetro.log"

AYUDA = """
Taxímetro digital
 i  iniciar carrera (empieza PARADO)
 p  el taxi está parado
 m  el taxi está en movimiento
 f  finalizar la carrera y ver el total
 a  ver esta ayuda
 s  salir
"""

# PASO 2: Creamos una función para leer las tarifas del JSON
def cargar_tarifas(ruta=CONFIG):
    try:
        # PASO 2: Leemos el archivo y convertimos su contenido en un diccionario
        datos = json.loads(ruta.read_text(encoding="utf-8"))

        # PASO 2: Guardamos las tarifas como números decimales
        tarifas = {
            "tarifa_parado": float(datos["tarifa_parado"]),
            "tarifa_movimiento": float(datos["tarifa_movimiento"])
        }

        # PASO 2: Registramos que hemos leído las tarifas correctamente
        log.info("Tarifas cargadas de %s: %s", ruta, tarifas)

        # PASO 2: Devolvemos las tarifas
        return tarifas

    # PASO 2: Si el archivo falta, está mal escrito o tiene datos incorrectos
    except (OSError, KeyError, ValueError, TypeError) as error:

        # PASO 2: Guardamos un aviso en el log
        log.warning(
            "No se pudo leer %s (%s); uso tarifas por defecto",
            ruta, error
        )

        # PASO 2: Usamos una copia de las tarifas originales
        return dict(TARIFAS_POR_DEFECTO)


# Creamos esta función para que el taxímetro sepa cuánto tiene que cobrar por cada segundo
# PASO 2: Añadimos las tarifas que hemos leído del archivo
def tarifa(estado, tarifas):

    # Si el taxi está parado, devolvemos la tarifa de parada
    if estado == "parado":
        # PASO 2: Buscamos la tarifa de parada en el diccionario
        return tarifas["tarifa_parado"]

    else:
        # Si el taxi no está parado, devolvemos la tarifa de movimiento
        # PASO 2: Buscamos la tarifa de movimiento en el diccionario
        return tarifas["tarifa_movimiento"]


# creamos la funcion para cerrar el tramo de la carrera y calcular el importe
# PASO 2: Añadimos las tarifas para poder calcular el precio
def cerrar_tramo(carrera, tarifas):

    # Calculamos el tiempo transcurrido desde que se inició el tramo.
    ahora = time.monotonic()

    # Calculamos los segundos transcurridos desde el inicio del tramo
    segundos = ahora - carrera["desde"]

    # calculamos el coste del tramo multiplicando los segundos por la tarifa correspondiente al estado del taxi
    # PASO 2: Utilizamos las tarifas del diccionario
    coste = segundos * tarifa(carrera["estado"], tarifas)

    # Sumamos el coste del tramo al importe acumulado de la carrera
    carrera["importe"] += coste

    # Actualizamos el momento de inicio del siguiente tramo
    carrera["desde"] = ahora


# Creamos una función para configurar el logger
def configurar_log():
    logging.basicConfig(
        # PASO 2: Guardamos el log en la misma carpeta del programa
        filename=LOG,
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s %(levelname)s %(message)s"
    )


# Creamos la función principal
def main():

    # Configuramos el logger para que registre los eventos en un archivo
    configurar_log()

    # Registramos un mensaje de información indicando que el taxímetro ha arrancado
    log.info("Arranque del taxímetro")

    # PASO 2: Cargamos las tarifas una sola vez al iniciar el programa
    tarifas = cargar_tarifas()

    # Mostramos la ayuda al iniciar el programa
    print(AYUDA)

    carrera = None

    # None significa que todavía no hay ninguna carrera iniciada
    # Creamos un bucle para pedir órdenes al conductor
    # strip() quita los espacios al inicio y al final
    # lower() convierte las letras a minúsculas
    while True:

        orden = input("Introduce una orden: ").strip().lower()

        if orden == "i":

            # Comprobamos si ya hay una carrera iniciada
            # is not None significa que ya existe una carrera
            if carrera is not None:

                # Si ya hay una, avisamos de que primero debe terminarla
                print("Ya hay una carrera en curso. Finalízala con 'f'.")

                # Volvemos a pedir una orden sin borrar la carrera
                # continue hace que el programa vuelva al principio del while
                continue

            # Si no hay ninguna carrera, empezamos una nueva
            carrera = {
                "estado": "parado",
                "desde": time.monotonic(),
                "importe": 0.0
            }

            # Registramos un mensaje de información indicando que se ha iniciado una carrera
            log.info("Carrera iniciada")

            # Mostramos un mensaje indicando que la carrera ha comenzado y que el taxi está parado
            print("Carrera iniciada. El taxi está PARADO.")

        # Si la orden es "s", nos despedimos y salimos del bucle
        elif orden == "s":

            # Comprobamos si todavía hay una carrera sin terminar
            if carrera is not None:

                # Si la hay, avisamos de que primero debemos terminarla
                print("Hay una carrera en curso. Finalízala con 'f' antes de salir.")

                # Volvemos a pedir otra orden sin cerrar el programa
                continue

            # Registramos un mensaje de información indicando que el taxímetro se ha cerrado
            log.info("Cierre del taxímetro")

            print("Hasta luego.")
            break

        # Si la orden es "a", mostramos la ayuda
        elif orden == "a":
            print(AYUDA)

        # Si la orden es "p" o "m", cambiamos el estado del taxi entre parado y movimiento
        elif orden in ("p", "m"):

            # Comprobamos si todavía no hay ninguna carrera iniciada
            # is None significa que no existe ninguna carrera
            if carrera is None:

                # Avisamos de que primero tenemos que iniciar una carrera
                print("Primero inicia una carrera con 'i'.")

                # Volvemos a pedir otra orden sin hacer ningún cambio
                continue

            # Guardamos el estado que corresponde a la letra introducida
            # Si pulsamos "m", será movimiento; si pulsamos "p", será parado
            estado_nuevo = "movimiento" if orden == "m" else "parado"

            # Comprobamos si el taxi ya está en ese mismo estado
            if carrera["estado"] == estado_nuevo:

                # Si ya está en ese estado, mostramos un aviso
                print(f"El taxi ya está en estado '{estado_nuevo}'.")

                # No cambiamos nada y volvemos a pedir una orden
                continue

            # Cobramos el tramo anterior antes de cambiar el estado
            # PASO 2: Pasamos las tarifas para calcular el tramo
            cerrar_tramo(carrera, tarifas)

            # Cambiamos el estado según la orden introducida
            carrera["estado"] = "movimiento" if orden == "m" else "parado"

            # Registramos un mensaje de información indicando el cambio de estado y el importe acumulado
            log.info(
                "Cambio de estado a %s (%.2f € acumulados)",
                carrera["estado"],
                carrera["importe"]
            )

            # Mostramos el estado del taxi y el importe acumulado
            print(f"Estado: {carrera['estado'].upper()}. Llevas {carrera['importe']:.2f} €.")

        # Si escribimos "f", queremos terminar la carrera
        elif orden == "f":

            # Comprobamos si hay alguna carrera que podamos finalizar
            if carrera is None:

                # Si no hay carrera, mostramos un aviso
                print("No hay ninguna carrera en curso.")

                # Volvemos a pedir otra orden sin hacer ningún cambio
                continue

            # Calculamos lo que falta por cobrar y lo sumamos al total
            # PASO 2: Pasamos las tarifas para calcular el último tramo
            cerrar_tramo(carrera, tarifas)

            # Registramos un mensaje de información indicando que la carrera ha finalizado y el importe total
            log.info("Carrera finalizada: %.2f €", carrera["importe"])

            # Mostramos cuánto tiene que pagar el cliente
            print(f"Carrera finalizada. Total a cobrar: {carrera['importe']:.2f} €")

            # Indicamos que ya no hay carrera para poder empezar otra
            carrera = None

        # Si no reconocemos la orden, mostramos un mensaje de error
        else:

            # Registramos un mensaje de advertencia indicando que se ha introducido una orden desconocida
            log.warning("Orden desconocida: %r", orden)

            # Mostramos un mensaje indicando que la orden no es válida y recordamos que se puede ver la ayuda con "a"
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")


# Ejecutamos la función principal al iniciar el programa
if __name__ == "__main__":
    main()
