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

#creamos la funcion para cerrar el tramo de la carrera y calcular el importe
def cerrar_tramo(carrera):
    # Calculamos el tiempo transcurrido desde que se inició el tramo.
    ahora = time.monotonic()

    #“Calculamos los segundos transcurridos desde el inicio del tramo
    segundos = ahora - carrera["desde"]
    
    #calculamos el coste del tramo multiplicando los segundos por la tarifa correspondiente al estado del taxi
    coste = segundos * tarifa(carrera["estado"])
    
    # Sumamos el coste del tramo al importe acumulado de la carrera
    carrera["importe"] += coste

    # Actualizamos el momento de inicio del siguiente tramo
    carrera["desde"] = ahora


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
            

        # Si la orden es "s", nos despedimos y salimos del bucle
        elif orden == "s":
            print("Hasta luego.")
            break

        # Si la orden es "a", mostramos la ayuda
        elif orden == "a":
            print(AYUDA)

        
        # Si la orden es "p" o "m", cambiamos el estado del taxi entre parado y movimiento
        elif orden in ("p", "m"):
            
        
            # Cobramos el tramo anterior antes de cambiar el estado
            cerrar_tramo(carrera)

            # Cambiamos el estado según la orden introducida
            carrera["estado"] = "movimiento" if orden == "m" else "parado"

            # Mostramos el estado del taxi y el importe acumulado
            print(f"Estado: {carrera['estado'].upper()}. Llevas {carrera['importe']:.2f} €.")

        
        # Si escribimos "f", queremos terminar la carrera
        elif orden == "f":
            # Calculamos lo que falta por cobrar y lo sumamos al total
            cerrar_tramo(carrera)
            # Mostramos cuánto tiene que pagar el cliente
            print(f"Carrera finalizada. Total a cobrar: {carrera['importe']:.2f} €")
            # Indicamos que ya no hay carrera para poder empezar otra
            carrera = None

            

        # Si no es "s" ni "a", mostramos un mensaje de error
        else:
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")
            



# Ejecutamos la función principal al iniciar el programa
if __name__ == "__main__":
    main()

