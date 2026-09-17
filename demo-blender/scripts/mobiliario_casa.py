# -*- coding: utf-8 -*-
"""
Solados y mobiliario de la casa, con la distribucion de la lamina de
anteproyecto. Se ejecuta despues de construir_casa_3d.py.
"""

import bpy
import bmesh
import sys

import os

# Rutas relativas al propio archivo: el repo funciona en cualquier maquina.
try:
    AQUI = os.path.dirname(os.path.abspath(__file__))
except NameError:                      # pegado a mano en el editor de Blender
    AQUI = os.path.dirname(os.path.abspath(bpy.data.filepath)) or os.getcwd()
RAIZ = os.path.dirname(AQUI)           # demo-blender/
RUTA_DATOS = os.path.join(RAIZ, "planos")
SALIDA = os.path.join(RAIZ, "salida")
os.makedirs(SALIDA, exist_ok=True)

if RUTA_DATOS not in sys.path:
    sys.path.append(RUTA_DATOS)
import casa_datos as D

COL = bpy.data.collections["Casa_3_Ambientes"]
PA = D.NIVEL_PA
E = D.MURO_EXT


def mat(nombre, color, rug=0.6):
    m = bpy.data.materials.get(nombre)
    if m is None:
        m = bpy.data.materials.new(nombre)
        m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Roughness"].default_value = rug
    m.diffuse_color = (*color, 1.0)
    return m


def caja(nombre, x0, y0, z0, x1, y1, z1, material):
    if nombre in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[nombre], do_unlink=True)
    malla = bpy.data.meshes.new(nombre)
    o = bpy.data.objects.new(nombre, malla)
    COL.objects.link(o)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0)
        v.co.y = y0 + (v.co.y + 0.5) * (y1 - y0)
        v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    bm.to_mesh(malla)
    bm.free()
    o.data.materials.append(material)
    return o


def solados():
    madera = mat("Piso_madera", (0.46, 0.31, 0.19), 0.55)
    porcelanato = mat("Piso_porcelanato", (0.60, 0.58, 0.55), 0.35)
    caja("Piso_PB_estar", E, E, 0.0, 4.60, 3.50, 0.016, madera)
    caja("Piso_PB_servicios", 4.70, E, 0.0, 7.80, 5.80, 0.016, porcelanato)
    caja("Piso_PB_cocina", E, 3.60, 0.0, 4.60, 5.80, 0.016, porcelanato)
    caja("Piso_PA_dorm1", E, E, PA, 4.20, 3.40, PA + 0.016, madera)
    caja("Piso_PA_dorm2", 4.30, E, PA, 7.80, 3.10, PA + 0.016, madera)
    # el solado NO puede cubrir el hueco de la escalera
    caja("Piso_PA_servicios", E, 3.50, PA, D.ESC_X0 - D.MURO_INT, 5.80, PA + 0.016, porcelanato)
    caja("Piso_PA_paso_sur", 2.70, 3.20, PA, D.ESC_X0 - D.MURO_INT, 3.50, PA + 0.016, porcelanato)
    # paredes apenas mas calidas que el cielorraso, si no la esquina no se lee
    mat("Tabique", (0.90, 0.885, 0.86), 0.80)
    mat("Muro_exterior", (0.93, 0.915, 0.89), 0.75)


def muebles():
    tapiz = mat("Tapizado", (0.34, 0.38, 0.44), 0.85)
    madera = mat("Madera_mueble", (0.40, 0.27, 0.17), 0.5)
    blanco = mat("Laca_blanca", (0.90, 0.90, 0.88), 0.4)
    tela = mat("Ropa_cama", (0.78, 0.76, 0.72), 0.85)
    mesada = mat("Mesada", (0.26, 0.27, 0.29), 0.3)
    sanit = mat("Sanitario", (0.95, 0.95, 0.94), 0.25)

    # estar comedor
    caja("Sofa_base", 0.40, 0.45, 0.06, 2.55, 1.30, 0.42, tapiz)
    caja("Sofa_respaldo", 0.40, 0.45, 0.42, 2.55, 0.72, 0.82, tapiz)
    caja("Mesa_ratona", 0.95, 1.65, 0.06, 2.05, 2.30, 0.40, madera)
    caja("Mesa_comedor", 2.95, 1.95, 0.72, 4.35, 3.20, 0.77, madera)
    for i, (sx, sy) in enumerate([(3.15, 1.60), (3.95, 1.60), (3.15, 3.30), (3.95, 3.30)]):
        caja(f"Silla_{i}", sx - 0.21, sy - 0.21, 0.0, sx + 0.21, sy + 0.21, 0.45, madera)
        caja(f"Silla_resp_{i}", sx - 0.21, sy - 0.21, 0.45, sx + 0.21, sy - 0.15, 0.92, madera)
    caja("Mueble_tv", 0.25, 2.95, 0.0, 0.62, 4.30, 0.50, blanco)

    # cocina
    caja("Mesada_norte", 0.22, 5.18, 0.0, 3.30, 5.78, 0.90, blanco)
    caja("Mesada_norte_top", 0.22, 5.16, 0.90, 3.30, 5.78, 0.94, mesada)
    caja("Mesada_oeste", 0.22, 3.62, 0.0, 0.82, 5.18, 0.90, blanco)
    caja("Mesada_oeste_top", 0.20, 3.62, 0.90, 0.84, 5.18, 0.94, mesada)
    caja("Alacena", 0.22, 5.42, 1.50, 3.10, 5.78, 2.20, blanco)
    caja("Heladera", 3.55, 5.10, 0.0, 4.25, 5.78, 1.80, blanco)

    # toilette
    caja("Inodoro_tl", 7.35, 1.95, 0.0, 7.72, 2.55, 0.42, sanit)
    caja("Lavatorio_tl", 6.30, 2.62, 0.78, 6.85, 2.96, 0.90, sanit)

    # dormitorio 1
    caja("Cama1_base", 1.15, 1.45, 0.05 + PA, 2.75, 3.35, 0.42 + PA, madera)
    caja("Cama1_colchon", 1.15, 1.45, 0.42 + PA, 2.75, 3.35, 0.62 + PA, tela)
    caja("Cama1_respaldo", 1.15, 3.32, 0.05 + PA, 2.75, 3.40, 1.05 + PA, madera)
    caja("Placard1", 0.25, 0.28, PA, 4.15, 0.88, 2.25 + PA, blanco)
    caja("Mesa_luz1", 2.85, 2.95, PA, 3.30, 3.38, 0.48 + PA, madera)

    # dormitorio 2
    caja("Cama2_base", 4.45, 1.55, 0.05 + PA, 5.40, 3.00, 0.42 + PA, madera)
    caja("Cama2_colchon", 4.45, 1.55, 0.42 + PA, 5.40, 3.00, 0.60 + PA, tela)
    caja("Escritorio2", 6.95, 0.30, 0.72 + PA, 7.75, 1.60, 0.76 + PA, madera)
    caja("Placard2", 6.55, 2.10, PA, 7.75, 3.05, 2.25 + PA, blanco)

    # bano
    caja("Banera", 0.25, 4.45, PA, 1.05, 5.70, 0.55 + PA, sanit)
    caja("Lavatorio_b", 1.55, 5.35, 0.78 + PA, 2.20, 5.75, 0.90 + PA, sanit)
    caja("Inodoro_b", 1.95, 3.62, PA, 2.35, 4.22, 0.42 + PA, sanit)


solados()
muebles()

result = {"objetos": len(COL.objects)}


def abrir_puertas():
    """Deja las hojas de puerta abiertas a 90 grados, sobre la jamba.

    Si quedan cerradas la camara del recorrido las atraviesa y se ve un
    rectangulo marron a pantalla completa.
    """
    carp = mat("Carpinteria", (0.36, 0.26, 0.18), 0.55)
    esp = 0.05
    for prefijo, lista, z_base in (("PB", D.ABERTURAS_PB, 0.0),
                                   ("PA", D.ABERTURAS_PA, PA)):
        for x0, y0, x1, y1, tipo, giro, ref, alto, antep, desc in lista:
            if tipo != "puerta":
                continue
            for o in list(bpy.data.objects):          # borra la hoja cerrada
                if o.name.startswith(prefijo) and o.name.endswith("_" + ref):
                    bpy.data.objects.remove(o, do_unlink=True)

            z0, z1 = z_base + 0.02, z_base + alto - 0.02
            horizontal = (x1 - x0) > (y1 - y0)
            luz = (x1 - x0) if horizontal else (y1 - y0)
            nombre = f"Puerta_abierta_{prefijo}_{ref}"

            if horizontal:                             # muro a lo largo de X
                eje_y = (y0 + y1) / 2                  # eje del muro
                bisagra_x = x0 + 0.01
                if giro == "N":
                    caja(nombre, bisagra_x, eje_y, z0,
                         bisagra_x + esp, eje_y + luz - 0.04, z1, carp)
                else:
                    caja(nombre, bisagra_x, eje_y - luz + 0.04, z0,
                         bisagra_x + esp, eje_y, z1, carp)
            else:                                      # muro a lo largo de Y
                eje_x = (x0 + x1) / 2
                bisagra_y = y0 + 0.01
                if giro == "E":
                    caja(nombre, eje_x, bisagra_y, z0,
                         eje_x + luz - 0.04, bisagra_y + esp, z1, carp)
                else:
                    caja(nombre, eje_x - luz + 0.04, bisagra_y, z0,
                         eje_x, bisagra_y + esp, z1, carp)


abrir_puertas()
