
"""Tests de la lógica de tarifas (fase 2). Ejecutar con: python -m pytest"""
import pytest

from taximetro import importe_tramo

TARIFAS = {"tarifa_parado": 0.02, "tarifa_movimiento": 0.05}

def test_parado_10_segundos():
    assert importe_tramo(10, "parado", TARIFAS) == pytest.approx(0.20)

def test_movimiento_10_segundos():
    assert importe_tramo(10, "movimiento", TARIFAS) == pytest.approx(0.50)

def test_segundos_negativos_dan_error():
    with pytest.raises(ValueError):
        importe_tramo(-1, "parado", TARIFAS)

# PASO 6: Comprobamos una carrera que combina parada y movimiento
# El taxi está 10 segundos parado y 10 segundos en movimiento
# Sumamos los dos importes y comprobamos que el total es 0.70 €
def test_carrera_mixta_suma_tramos():
    parado = importe_tramo(10, "parado", TARIFAS)
    movimiento = importe_tramo(10, "movimiento", TARIFAS)
    total = parado + movimiento

    assert total == pytest.approx(0.70)