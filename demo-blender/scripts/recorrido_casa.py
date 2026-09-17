# -*- coding: utf-8 -*-
"""
Saca las casas vecinas, agrega figuras de escala y arma el recorrido animado
por dentro de la casa. Pensado para ejecutarse sobre la escena que deja
construir_casa_3d.py.
"""

import bpy
import bmesh
import math
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
FPS = 24
SEGUNDOS = 21
TOTAL = FPS * SEGUNDOS


# ------------------------------------------------------------------ 1. vecinos
def sacar_vecinos():
    quitados = []
    for nombre in ("Vecino_oeste", "Vecino_este"):
        o = bpy.data.objects.get(nombre)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
            quitados.append(nombre)
    return quitados


# ------------------------------------------------------------------ 2. gente
def material(nombre, color, rugosidad=0.6):
    if nombre in bpy.data.materials:
        return bpy.data.materials[nombre]
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Roughness"].default_value = rugosidad
    m.diffuse_color = (*color, 1.0)
    return m


def _pieza(bm, tipo, **kw):
    if tipo == "esfera":
        bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=8,
                                  radius=kw["r"], matrix=kw["mat"])
    else:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=14,
                              radius1=kw["r0"], radius2=kw["r1"],
                              depth=kw["h"], matrix=kw["mat"])


def persona(nombre, x, y, z_piso, giro=0.0, altura=1.72, color=(0.80, 0.80, 0.82)):
    """Figura de escala sencilla: cabeza, torso, brazos y piernas."""
    from mathutils import Matrix

    k = altura / 1.72
    malla = bpy.data.meshes.new(nombre)
    obj = bpy.data.objects.new(nombre, malla)
    COL.objects.link(obj)
    bm = bmesh.new()

    def T(px, py, pz):
        return Matrix.Translation((px, py, pz))

    # piernas
    for dx in (-0.09, 0.09):
        _pieza(bm, "cono", r0=0.068 * k, r1=0.055 * k, h=0.86 * k,
               mat=T(dx * k, 0, 0.43 * k))
    # cadera y torso
    _pieza(bm, "cono", r0=0.135 * k, r1=0.155 * k, h=0.18 * k, mat=T(0, 0, 0.95 * k))
    _pieza(bm, "cono", r0=0.155 * k, r1=0.175 * k, h=0.44 * k, mat=T(0, 0, 1.26 * k))
    # brazos
    for dx in (-0.21, 0.21):
        _pieza(bm, "cono", r0=0.050 * k, r1=0.042 * k, h=0.52 * k,
               mat=T(dx * k, 0, 1.19 * k))
    # cuello y cabeza
    _pieza(bm, "cono", r0=0.055 * k, r1=0.055 * k, h=0.08 * k, mat=T(0, 0, 1.52 * k))
    _pieza(bm, "esfera", r=0.105 * k, mat=T(0, 0, 1.64 * k))

    bm.to_mesh(malla)
    bm.free()
    obj.location = (x, y, z_piso)
    obj.rotation_euler = (0, 0, math.radians(giro))
    obj.data.materials.append(material(f"Piel_{nombre}", color, 0.55))
    for p in malla.polygons:
        p.use_smooth = True
    return obj


def poblar():
    for o in list(bpy.data.objects):
        if o.name.startswith("Persona_"):
            bpy.data.objects.remove(o, do_unlink=True)
    gente = [
        # planta baja
        ("Persona_estar",   1.10, 1.30, 0.00, 150, 1.74, (0.82, 0.80, 0.78)),
        ("Persona_cocina",  1.05, 4.55, 0.00, 200, 1.66, (0.76, 0.78, 0.82)),
        ("Persona_hall",    7.15, 1.05, 0.00, 250, 1.70, (0.80, 0.76, 0.74)),
        # jardin de acceso
        ("Persona_jardin",  2.60, -1.45, 0.00, 20, 1.76, (0.78, 0.80, 0.78)),
        # planta alta
        ("Persona_dorm1",   1.00, 1.05, D.NIVEL_PA, 120, 1.68, (0.82, 0.78, 0.80)),
        ("Persona_dorm2",   6.55, 1.10, D.NIVEL_PA, 210, 1.62, (0.76, 0.80, 0.80)),
    ]
    creadas = []
    for nombre, x, y, z, giro, alt, col in gente:
        persona(nombre, x, y, z, giro, alt, col)
        creadas.append(nombre)
    return creadas


# --------------------------------------------------------------- 3. recorrido
# (fraccion del recorrido, posicion de camara, punto al que mira)
OJO_PB = 1.62
OJO_PA = D.NIVEL_PA + 1.62

RECORRIDO = [
    (0.00, (6.05, -8.60, 1.75), (6.05,  0.00, 1.60)),   # llegando por la calle
    (0.07, (6.05, -4.20, 1.70), (6.05,  0.40, 1.50)),   # jardin de acceso
    (0.12, (6.05, -1.00, OJO_PB), (6.05,  2.40, 1.45)), # frente a la puerta
    (0.16, (6.05,  0.75, OJO_PB), (6.30,  2.60, 1.45)), # entrando al hall
    (0.20, (6.20,  1.20, OJO_PB), (4.00,  1.00, 1.45)), # gira hacia el estar
    (0.25, (4.65,  1.05, OJO_PB), (2.00,  1.20, 1.10)), # cruza la puerta P2
    (0.30, (3.30,  1.45, OJO_PB), (1.20,  0.95, 0.95)), # el sofa
    (0.35, (2.35,  2.45, OJO_PB), (2.45,  0.25, 1.25)), # ventana del frente
    (0.40, (3.60,  2.60, OJO_PB), (4.05,  2.55, 0.85)), # mesa de comedor
    (0.45, (4.60,  1.25, OJO_PB), (5.50,  2.20, 1.45)), # vuelve hacia el paso
    (0.50, (5.40,  2.60, OJO_PB), (5.30,  5.20, 1.45)), # paso
    (0.55, (5.20,  4.95, OJO_PB), (2.80,  4.90, 1.30)), # cruza la puerta P3
    (0.60, (3.30,  4.60, OJO_PB), (1.30,  5.55, 1.05)), # mesada de la cocina
    (0.64, (2.60,  4.45, OJO_PB), (2.20,  6.80, 1.25)), # puerta ventana al patio
    (0.68, (4.85,  4.60, OJO_PB), (6.40,  3.90, 1.20)), # va hacia la escalera
    (0.72, (6.15,  3.55, OJO_PB), (7.25,  4.60, 0.55)), # pie de la escalera
    (0.76, (6.30,  3.95, 2.30),   (7.20,  5.05, 0.85)), # sube mirando los escalones
    (0.80, (6.35,  4.20, 3.30),   (7.10,  5.25, 1.30)), # ve el descanso desde arriba
    (0.84, (6.28,  4.05, 4.20),   (6.15,  3.10, 3.30)), # gira hacia el vano
    (0.87, (6.05,  3.62, OJO_PA), (4.30,  3.85, 4.25)), # cruza el vano al paso
    (0.91, (4.10,  3.90, OJO_PA), (3.50,  1.90, 4.15)), # mira al dormitorio 1
    (0.95, (2.70,  2.15, OJO_PA), (1.80,  2.40, 3.55)), # cama del dormitorio 1
    (0.98, (4.55,  3.55, OJO_PA), (5.40,  1.80, 4.05)), # gira al dormitorio 2
    (1.00, (5.85,  2.05, OJO_PA), (5.20,  0.80, 3.60)), # dormitorio 2
]


def curvas_de(obj):
    """Devuelve las fcurves del objeto, sirva la API vieja o la de capas."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    accion = ad.action
    if hasattr(accion, "fcurves"):
        return list(accion.fcurves)
    salida = []
    slot = getattr(ad, "action_slot", None)
    for capa in accion.layers:
        for tira in capa.strips:
            bolsa = None
            if slot is not None:
                try:
                    bolsa = tira.channelbag(slot)
                except (TypeError, RuntimeError):
                    bolsa = None
            if bolsa is None and getattr(tira, "channelbags", None):
                bolsa = tira.channelbags[0]
            if bolsa is not None:
                salida.extend(bolsa.fcurves)
    return salida


def armar_recorrido():
    escena = bpy.context.scene

    # objetivo al que apunta la camara
    objetivo = bpy.data.objects.get("Objetivo_recorrido")
    if objetivo is None:
        objetivo = bpy.data.objects.new("Objetivo_recorrido", None)
        objetivo.empty_display_size = 0.2
        COL.objects.link(objetivo)

    cam_datos = bpy.data.cameras.new("Cam_Recorrido")
    cam_datos.lens = 21.0            # gran angular, para interiores chicos
    cam_datos.clip_start = 0.03
    cam = bpy.data.objects.get("Cam_Recorrido")
    if cam:
        bpy.data.objects.remove(cam, do_unlink=True)
    cam = bpy.data.objects.new("Cam_Recorrido", cam_datos)
    COL.objects.link(cam)

    c = cam.constraints.new("TRACK_TO")
    c.target = objetivo
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"

    cam.animation_data_clear()
    objetivo.animation_data_clear()

    for frac, pos, mira in RECORRIDO:
        f = 1 + round(frac * (TOTAL - 1))
        cam.location = pos
        cam.keyframe_insert("location", frame=f)
        objetivo.location = mira
        objetivo.keyframe_insert("location", frame=f)

    for obj in (cam, objetivo):
        for fc in curvas_de(obj):
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = "AUTO_CLAMPED"
                kp.handle_right_type = "AUTO_CLAMPED"
            fc.update()

    escena.camera = cam
    escena.frame_start = 1
    escena.frame_end = TOTAL
    escena.render.fps = FPS
    return cam


# ----------------------------------------------------------------- 4. salida
def configurar_video():
    escena = bpy.context.scene
    r = escena.render
    r.resolution_x = 1280
    r.resolution_y = 720
    r.resolution_percentage = 100
    # esta compilacion de Blender no trae salida de video: se sacan cuadros
    # PNG y se arman despues con ffmpeg
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    r.image_settings.compression = 20
    r.filepath = os.path.join(SALIDA, "cuadros", "f_")
    escena.eevee.taa_render_samples = 24      # el video no necesita 128
    return r.filepath


def luz_interior():
    """Con el techo puesto, el interior queda oscuro: se agregan luces de sala."""
    puntos = [
        ("Luz_estar", (2.40, 1.80, 2.35), 110.0),
        ("Luz_cocina", (2.40, 4.70, 2.35), 90.0),
        ("Luz_hall", (6.20, 1.00, 2.35), 70.0),
        ("Luz_paso_pb", (5.40, 3.60, 2.35), 60.0),
        ("Luz_escalera", (6.75, 4.60, 2.30), 60.0),
        ("Luz_dorm1", (2.20, 1.80, D.NIVEL_PA + 2.35), 100.0),
        ("Luz_dorm2", (6.00, 1.70, D.NIVEL_PA + 2.35), 90.0),
        ("Luz_paso_pa", (4.10, 4.30, D.NIVEL_PA + 2.35), 70.0),
        ("Luz_bano", (1.40, 4.65, D.NIVEL_PA + 2.35), 60.0),
    ]
    creadas = []
    for nombre, pos, energia in puntos:
        if nombre in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nombre], do_unlink=True)
        d = bpy.data.lights.new(nombre, type="POINT")
        d.energy = energia
        d.shadow_soft_size = 0.35
        o = bpy.data.objects.new(nombre, d)
        COL.objects.link(o)
        o.location = pos
        creadas.append(nombre)
    return creadas


quitados = sacar_vecinos()
gente = poblar()
luces = luz_interior()
cam = armar_recorrido()
ruta = configurar_video()

result = {
    "vecinos_quitados": quitados,
    "personas": gente,
    "luces_interiores": len(luces),
    "fotogramas": TOTAL,
    "duracion_s": SEGUNDOS,
    "salida": ruta,
}
