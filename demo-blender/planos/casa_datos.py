# -*- coding: utf-8 -*-
"""
Geometria de la casa de 3 ambientes en duplex. Sin dependencias, para que la
importen tanto el generador del plano como el constructor 3D de Blender y no
puedan desincronizarse.

Todas las medidas en metros. Origen (0,0) en la esquina exterior suroeste de la
casa. X crece al este, Y crece al norte (hacia el fondo). El frente da al sur.
"""

# ------------------------------------------------------------------ lote
LOTE_ANCHO = 8.00
LOTE_FONDO = 12.50
RETIRO_FRENTE = 3.00
CASA_ANCHO = 8.00
CASA_FONDO = 6.00
PATIO_FONDO = LOTE_FONDO - RETIRO_FRENTE - CASA_FONDO   # 3.50

# ------------------------------------------------------------------ alturas
MURO_EXT = 0.20
MURO_INT = 0.10
ALTURA_LIBRE = 2.60
ESPESOR_LOSA = 0.20
NIVEL_PA = ALTURA_LIBRE + ESPESOR_LOSA                  # 2.80
ALTURA_TOTAL = NIVEL_PA + ALTURA_LIBRE + ESPESOR_LOSA   # 5.60

# ------------------------------------------------------------------ muros
# (x0, y0, x1, y1)
MUROS_EXT = [
    (0.00, 0.00, CASA_ANCHO, MURO_EXT),                      # frente, sur
    (0.00, CASA_FONDO - MURO_EXT, CASA_ANCHO, CASA_FONDO),   # fondo, norte
    (0.00, 0.00, MURO_EXT, CASA_FONDO),                      # medianera oeste
    (CASA_ANCHO - MURO_EXT, 0.00, CASA_ANCHO, CASA_FONDO),   # medianera este
]

MUROS_PB = [
    (4.60, 0.20, 4.70, 5.80),     # estar y cocina / servicios
    (0.20, 3.50, 4.60, 3.60),     # estar / cocina
    (4.70, 1.70, 7.80, 1.80),     # hall / paso
    (6.10, 1.80, 6.20, 3.00),     # toilette, muro oeste
    (6.20, 3.00, 7.80, 3.10),     # toilette, muro norte
]

MUROS_PA = [
    (4.20, 0.20, 4.30, 3.20),     # dormitorio 1 / dormitorio 2
    (0.20, 3.40, 4.20, 3.50),     # dormitorio 1 / paso
    (4.30, 3.10, 7.80, 3.20),     # dormitorio 2 / paso y escalera
    (2.60, 3.50, 2.70, 5.80),     # bano / paso
    (5.60, 3.20, 5.70, 5.80),     # paso / escalera
]

# --------------------------------------------------------------- aberturas
# (x0, y0, x1, y1, tipo, giro, referencia, alto, antepecho, descripcion)
# tipo: "puerta" | "ventana" | "vano" | "corrediza"
ABERTURAS_PB = [
    (5.60, 0.00, 6.50, 0.20, "puerta", "N", "P1", 2.10, None, "Puerta de entrada"),
    (1.20, 0.00, 3.60, 0.20, "ventana", None, "V1", 1.50, 0.90, "Ventana del estar"),
    (1.40, 5.80, 3.00, 6.00, "corrediza", None, "PV1", 2.10, None, "Puerta ventana al patio"),
    (4.60, 0.60, 4.70, 1.40, "puerta", "O", "P2", 2.00, None, "Hall a estar"),
    (4.60, 4.60, 4.70, 5.40, "puerta", "O", "P3", 2.00, None, "Paso a cocina"),
    (6.10, 2.00, 6.20, 2.70, "puerta", "E", "P4", 2.00, None, "Toilette"),
    (4.90, 1.70, 5.90, 1.80, "vano", None, "VA1", 2.10, None, "Vano de hall a paso"),
]

ABERTURAS_PA = [
    (1.40, 0.00, 3.20, 0.20, "ventana", None, "V2", 1.50, 0.90, "Ventana dormitorio 1"),
    (5.20, 0.00, 6.80, 0.20, "ventana", None, "V3", 1.50, 0.90, "Ventana dormitorio 2"),
    (0.90, 5.80, 1.50, 6.00, "ventana", None, "V4", 1.50, 0.90, "Ventana del bano"),
    (3.20, 3.40, 4.00, 3.50, "puerta", "S", "P5", 2.00, None, "Dormitorio 1"),
    (4.60, 3.10, 5.40, 3.20, "puerta", "S", "P6", 2.00, None, "Dormitorio 2"),
    (2.60, 4.40, 2.70, 5.10, "puerta", "E", "P7", 2.00, None, "Bano"),
    (5.60, 3.25, 5.70, 4.25, "vano", None, "VA2", 2.05, None, "Vano de paso a escalera"),
]

# --------------------------------------------------------------- ambientes
# (nombre, x0, y0, x1, y1, x_rotulo, y_rotulo)
AMB_PB = [
    ("ESTAR - COMEDOR", 0.20, 0.20, 4.60, 3.50, None, None),
    ("COCINA",          0.20, 3.60, 4.60, 5.80, None, None),
    ("HALL",            4.70, 0.20, 7.80, 1.70, 7.00, 0.95),
    ("TOILETTE",        6.20, 1.80, 7.80, 3.00, 7.25, 2.40),
    ("PASO",            4.70, 1.80, 6.10, 5.80, 5.15, 4.60),
]

AMB_PA = [
    ("DORMITORIO 1",  0.20, 0.20, 4.20, 3.40, None, None),
    ("DORMITORIO 2",  4.30, 0.20, 7.80, 3.10, None, None),
    ("BAÑO",          0.20, 3.50, 2.60, 5.80, None, None),
    ("PASO",          2.70, 3.20, 5.60, 5.80, 4.10, 4.40),
]

# --------------------------------------------------------------- escalera
ESC_X0, ESC_X1 = 5.70, 7.80
ESC_Y0, ESC_Y1 = 3.20, 5.80
ESC_ALZADAS = 16
ESC_ALZADA = NIVEL_PA / ESC_ALZADAS        # 0.175
ESC_PEDADA = 0.26
ESC_PEDADAS_TRAMO = 7
