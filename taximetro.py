#importamos librerías necesarias
import time
#creamos constantes para las tarifas de parada y movimiento
TARIFA_PARADO = 0.02
TARIFA_MOVIMIENTO = 0.05
# Creamos el menú de ayuda, con sus opciones disponibles
AYUDA = """
Taxímetro digital
 i  iniciar carrera (empieza PARADO)
 p  el taxi está parado
 m  el taxi está en movimiento
 f  finalizar la carrera y ver el total
 a  ver esta ayuda
 s  salir
"""

#Creamos esta función para que el taxímetro sepa cuánto tiene que cobrar por cada segundo
def tarifa(estado):
    # Si el taxi está parado, devolvemos la tarifa de parada
    if estado == "parado":
        return TARIFA_PARADO
    else:
    # Si el taxi no está parado, devolvemos la tarifa de movimiento
        return TARIFA_MOVIMIENTO

# Creamos la función principal
def main():
    # Mostramos los resultados de la ayuda
    print(AYUDA)

#
    carrera = None

    # Creamos un bucle para pedir órdenes al conductor
    # strip() quita los espacios al inicio y al final
    # lower() convierte las letras a minúsculas
    while True:
        orden = input("Introduce una orden: ").strip().lower()

        if orden == "i":
            # Si la orden es "i", iniciamos una nueva carrera
            carrera = {
                "estado": "parado",
                "desde": time.monotonic(),
                "importe": 0.0
            }
            print("Carrera iniciada. El taxi está PARADO.")
            print(carrera)

        # Si la orden es "s", nos despedimos y salimos del bucle
        elif orden == "s":
            print("Hasta luego.")
            break

        # Si la orden es "a", mostramos la ayuda
        elif orden == "a":
            print(AYUDA)

        # Si no es "s" ni "a", mostramos un mensaje de error
        else:
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")


# Ejecutamos la función principal al iniciar el programa
if __name__ == "__main__":
    main()

