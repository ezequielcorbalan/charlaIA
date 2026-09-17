# -*- coding: utf-8 -*-
"""
Levanta en Blender la casa de 3 ambientes en duplex a partir de la MISMA
geometria con la que se dibuja el plano (modulo casa_datos).

Los muros se arman por tramos macizos alrededor de cada abertura, sin
modificadores booleanos: es deterministico y no depende del contexto de Blender.
"""

import bpy
import bmesh
import math
import os
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
import importlib
importlib.reload(D)

COL_NOMBRE = "Casa_3_Ambientes"

# ------------------------------------------------------------------ utilidades


def limpiar_escena():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for bloque in (bpy.data.meshes, bpy.data.materials, bpy.data.curves,
                   bpy.data.cameras, bpy.data.lights):
        for dato in list(bloque):
            if dato.users == 0:
                bloque.remove(dato)


def coleccion(nombre):
    if nombre in bpy.data.collections:
        return bpy.data.collections[nombre]
    col = bpy.data.collections.new(nombre)
    bpy.context.scene.collection.children.link(col)
    return col


def material(nombre, color, rugosidad=0.65, alpha=1.0, metalico=0.0):
    if nombre in bpy.data.materials:
        return bpy.data.materials[nombre]
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Roughness"].default_value = rugosidad
    b.inputs["Metallic"].default_value = metalico
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        try:
            b.inputs["Transmission Weight"].default_value = 0.9
        except KeyError:
            pass
        mat.blend_method = "BLEND"
    mat.diffuse_color = (*color, alpha)
    return mat


CAJAS = []


def caja(nombre, x0, y0, z0, x1, y1, z1, mat, col):
    """Crea un prisma recto entre dos esquinas opuestas."""
    if x1 - x0 <= 1e-6 or y1 - y0 <= 1e-6 or z1 - z0 <= 1e-6:
        return None
    malla = bpy.data.meshes.new(nombre)
    obj = bpy.data.objects.new(nombre, malla)
    col.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0)
        v.co.y = y0 + (v.co.y + 0.5) * (y1 - y0)
        v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    bm.to_mesh(malla)
    bm.free()
    obj.data.materials.append(mat)
    CAJAS.append(obj)
    return obj


# ------------------------------------------------------- muros con aberturas


def aberturas_del_muro(muro, aberturas):
    x0, y0, x1, y1 = muro
    propias = []
    for a in aberturas:
        ax0, ay0, ax1, ay1 = a[0], a[1], a[2], a[3]
        if (ax0 >= x0 - 1e-6 and ax1 <= x1 + 1e-6
                and ay0 >= y0 - 1e-6 and ay1 <= y1 + 1e-6):
            propias.append(a)
    return propias


def construir_muro(muro, aberturas, z_base, alto, mat_muro, mat_vidrio,
                   mat_carpinteria, col, prefijo):
    """Arma un muro por tramos macizos, dejando el hueco de cada abertura."""
    x0, y0, x1, y1 = muro
    horizontal = (x1 - x0) >= (y1 - y0)
    propias = sorted(aberturas_del_muro(muro, aberturas),
                     key=lambda a: a[0] if horizontal else a[1])

    def tramo(u_ini, u_fin, zi, zf, sufijo):
        if horizontal:
            caja(f"{prefijo}_{sufijo}", u_ini, y0, zi, u_fin, y1, zf, mat_muro, col)
        else:
            caja(f"{prefijo}_{sufijo}", x0, u_ini, zi, x1, u_fin, zf, mat_muro, col)

    u0, u1 = (x0, x1) if horizontal else (y0, y1)
    cursor = u0
    n = 0
    for a in propias:
        ax0, ay0, ax1, ay1, tipo, giro, ref, h_ab, antep, desc = a
        a_ini, a_fin = (ax0, ax1) if horizontal else (ay0, ay1)
        antep = antep or 0.0
        n += 1

        if a_ini - cursor > 1e-6:
            tramo(cursor, a_ini, z_base, z_base + alto, f"macizo{n}")
        if antep > 1e-6:                                   # antepecho
            tramo(a_ini, a_fin, z_base, z_base + antep, f"antepecho{n}")
        if alto - (antep + h_ab) > 1e-6:                   # dintel
            tramo(a_ini, a_fin, z_base + antep + h_ab, z_base + alto, f"dintel{n}")

        # hoja: vidrio para ventanas, tablero para puertas
        if tipo in ("ventana", "corrediza"):
            mat, esp = mat_vidrio, 0.03
        elif tipo == "puerta":
            mat, esp = mat_carpinteria, 0.05
        else:
            mat = None
        if mat:
            zc0, zc1 = z_base + antep + 0.02, z_base + antep + h_ab - 0.02
            if horizontal:
                ym = (y0 + y1) / 2
                caja(f"{prefijo}_{ref}", a_ini + 0.04, ym - esp / 2, zc0,
                     a_fin - 0.04, ym + esp / 2, zc1, mat, col)
            else:
                xm = (x0 + x1) / 2
                caja(f"{prefijo}_{ref}", xm - esp / 2, a_ini + 0.04, zc0,
                     xm + esp / 2, a_fin - 0.04, zc1, mat, col)
        cursor = a_fin

    if u1 - cursor > 1e-6:
        tramo(cursor, u1, z_base, z_base + alto, "macizo_fin")


# ------------------------------------------------------------------ escalera


def construir_escalera(col, mat):
    """Escalera en U: sube por el tramo oeste y baja por el este."""
    ancho = (D.ESC_X1 - D.ESC_X0 - D.MURO_INT) / 2      # 1.00
    x_oeste0, x_oeste1 = D.ESC_X0, D.ESC_X0 + ancho
    x_este0, x_este1 = D.ESC_X1 - ancho, D.ESC_X1
    n_tramo = 8
    y_giro = D.ESC_Y0 + n_tramo * D.ESC_PEDADA          # 5.28

    for i in range(1, n_tramo + 1):            # primer tramo, contra la medianera este
        y_i = D.ESC_Y0 + (i - 1) * D.ESC_PEDADA
        caja(f"Escalon_{i:02d}", x_este0, y_i, 0.0,
             x_este1, y_i + D.ESC_PEDADA, i * D.ESC_ALZADA, mat, col)

    z_descanso = n_tramo * D.ESC_ALZADA                 # 1.40
    caja("Escalera_descanso", D.ESC_X0, y_giro, 0.0,
         D.ESC_X1, D.ESC_Y1, z_descanso, mat, col)

    for j in range(1, n_tramo + 1):            # segundo tramo, llega al vano del paso
        y_f = y_giro - (j - 1) * D.ESC_PEDADA
        caja(f"Escalon_{n_tramo + j:02d}", x_oeste0, y_f - D.ESC_PEDADA, 0.0,
             x_oeste1, y_f, z_descanso + j * D.ESC_ALZADA, mat, col)


# ------------------------------------------------------------------ escena


def construir():
    limpiar_escena()
    CAJAS.clear()
    col = coleccion(COL_NOMBRE)

    m_muro = material("Muro_exterior", (0.92, 0.90, 0.86), 0.75)
    m_interior = material("Tabique", (0.95, 0.94, 0.91), 0.80)
    m_losa = material("Losa", (0.80, 0.78, 0.75), 0.85)
    m_vidrio = material("Vidrio", (0.62, 0.76, 0.84), 0.08, alpha=0.30)
    m_carp = material("Carpinteria", (0.36, 0.26, 0.18), 0.55)
    m_esc = material("Escalera", (0.86, 0.84, 0.80), 0.70)
    m_techo = material("Techo", (0.34, 0.36, 0.40), 0.80)
    m_cesped = material("Cesped", (0.44, 0.60, 0.34), 0.95)
    m_solado = material("Solado", (0.78, 0.76, 0.72), 0.90)
    m_vecino = material("Vecino", (0.72, 0.70, 0.67), 0.85)

    # --- losa de planta baja
    caja("Losa_PB", 0, 0, -D.ESPESOR_LOSA, D.CASA_ANCHO, D.CASA_FONDO, 0.0, m_losa, col)

    # --- muros de planta baja
    for i, muro in enumerate(D.MUROS_EXT):
        construir_muro(muro, D.ABERTURAS_PB, 0.0, D.ALTURA_LIBRE,
                       m_muro, m_vidrio, m_carp, col, f"PB_Ext{i + 1}")
    for i, muro in enumerate(D.MUROS_PB):
        construir_muro(muro, D.ABERTURAS_PB, 0.0, D.ALTURA_LIBRE,
                       m_interior, m_vidrio, m_carp, col, f"PB_Int{i + 1}")

    # --- entrepiso, con el vacio de la escalera
    z0, z1 = D.ALTURA_LIBRE, D.NIVEL_PA
    vx0, vx1 = D.ESC_X0, D.ESC_X1
    vy0, vy1 = D.ESC_Y0, D.ESC_Y1
    caja("Entrepiso_oeste", 0, 0, z0, vx0, D.CASA_FONDO, z1, m_losa, col)
    caja("Entrepiso_sur", vx0, 0, z0, vx1, vy0, z1, m_losa, col)
    caja("Entrepiso_norte", vx0, vy1, z0, vx1, D.CASA_FONDO, z1, m_losa, col)

    # --- muros de planta alta
    for i, muro in enumerate(D.MUROS_EXT):
        construir_muro(muro, D.ABERTURAS_PA, D.NIVEL_PA, D.ALTURA_LIBRE,
                       m_muro, m_vidrio, m_carp, col, f"PA_Ext{i + 1}")
    for i, muro in enumerate(D.MUROS_PA):
        construir_muro(muro, D.ABERTURAS_PA, D.NIVEL_PA, D.ALTURA_LIBRE,
                       m_interior, m_vidrio, m_carp, col, f"PA_Int{i + 1}")

    # --- losa de techo
    caja("Techo", -0.15, -0.15, D.NIVEL_PA + D.ALTURA_LIBRE,
         D.CASA_ANCHO + 0.15, D.CASA_FONDO + 0.15, D.ALTURA_TOTAL, m_techo, col)

    construir_escalera(col, m_esc)

    # --- terreno: retiro al sur, patio al norte
    caja("Terreno", -0.4, -D.RETIRO_FRENTE - 0.4, -0.45,
         D.LOTE_ANCHO + 0.4, D.CASA_FONDO + D.PATIO_FONDO + 0.4, -0.20, m_cesped, col)
    caja("Solado_acceso", 5.30, -D.RETIRO_FRENTE, -0.20, 6.80, 0.0, -0.17, m_solado, col)
    caja("Solado_patio", 1.20, D.CASA_FONDO, -0.20, 3.40, D.CASA_FONDO + 1.80, -0.17,
         m_solado, col)

    # --- vecinos, para que se lea que esta entre medianeras
    caja("Vecino_oeste", -7.8, 0, -0.20, -0.02, D.CASA_FONDO, D.ALTURA_TOTAL, m_vecino, col)
    caja("Vecino_este", D.CASA_ANCHO + 0.02, 0, -0.20, D.CASA_ANCHO + 7.8,
         D.CASA_FONDO, D.ALTURA_TOTAL, m_vecino, col)

    return col


def iluminar_y_encuadrar(col):
    from mathutils import Vector

    escena = bpy.context.scene

    datos_sol = bpy.data.lights.new("Sol", type="SUN")
    datos_sol.energy = 4.0
    datos_sol.angle = math.radians(1.5)
    sol = bpy.data.objects.new("Sol", datos_sol)
    col.objects.link(sol)
    sol.location = (-14, -18, 22)
    sol.rotation_euler = (math.radians(50), 0, math.radians(-38))

    mundo = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    escena.world = mundo
    mundo.use_nodes = True
    fondo = mundo.node_tree.nodes["Background"]
    fondo.inputs[0].default_value = (0.58, 0.72, 0.88, 1.0)
    fondo.inputs[1].default_value = 0.55

    def camara(nombre, pos, mira, lente=42.0, orto=None):
        datos = bpy.data.cameras.new(nombre)
        if orto:
            datos.type = "ORTHO"
            datos.ortho_scale = orto
        else:
            datos.lens = lente
        cam = bpy.data.objects.new(nombre, datos)
        col.objects.link(cam)
        cam.location = pos
        direccion = Vector(mira) - Vector(pos)
        cam.rotation_euler = direccion.to_track_quat("-Z", "Y").to_euler()
        return cam

    camara("Cam_Frente", (16.5, -15.0, 8.0), (3.4, 2.4, 1.9), lente=45)
    camara("Cam_Patio", (-7.5, 14.5, 7.5), (4.0, 3.6, 1.8), lente=45)
    camara("Cam_Aerea", (10.5, -9.0, 15.5), (4.0, 3.0, 1.4), lente=48)

    escena.camera = bpy.data.objects["Cam_Frente"]
    escena.render.resolution_x = 1800
    escena.render.resolution_y = 1150
    motores = escena.render.bl_rna.properties["engine"].enum_items.keys()
    for candidato in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if candidato in motores:
            escena.render.engine = candidato
            break
    escena.view_settings.view_transform = "Standard"
    escena.view_settings.look = "None"


col = construir()
iluminar_y_encuadrar(col)

result = {
    "objetos": len(col.objects),
    "cajas": len(CAJAS),
    "altura_total": D.ALTURA_TOTAL,
    "camaras": [o.name for o in col.objects if o.type == "CAMERA"],
}
