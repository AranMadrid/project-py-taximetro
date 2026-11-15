
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

# Creamos la función principal
def main():
    # Mostramos los resultados de la ayuda
    print(AYUDA)

    # Creamos un bucle para pedir órdenes al conductor
    # strip() quita los espacios al inicio y al final
    # lower() convierte las letras a minúsculas
    while True:
        orden = input("Introduce una orden: ").strip().lower()

        # Si la orden es "s", nos despedimos y salimos del bucle
        if orden == "s":
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

