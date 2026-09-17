# -*- coding: utf-8 -*-
"""
Arma la escena completa y renderiza el recorrido, sin interfaz.

Uso:
    blender -b --python render_recorrido.py
"""

import bpy
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(os.path.dirname(BASE), "salida")
os.makedirs(SALIDA, exist_ok=True)
PASOS = ("construir_casa_3d.py", "mobiliario_casa.py", "recorrido_casa.py")


def correr(nombre):
    ruta = os.path.join(BASE, nombre)
    ambito = {"__file__": ruta}
    exec(compile(open(ruta, encoding="utf-8").read(), ruta, "exec"), ambito)
    return ambito.get("result")


for paso in PASOS:
    print("  [paso]", paso, "->", correr(paso))

escena = bpy.context.scene
escena.view_settings.exposure = 0.0
escena.eevee.taa_render_samples = 24
escena.eevee.use_shadows = True
for o in bpy.data.objects:
    if o.type == "LIGHT" and o.name.startswith("Luz_"):
        o.data.energy = 26.0 if ("dorm" in o.name or "estar" in o.name) else 18.0
        o.data.shadow_soft_size = 0.5

abiertas = sorted(o.name for o in bpy.data.objects if o.name.startswith("Puerta_abierta_"))
print("  [puertas abiertas]", len(abiertas), abiertas)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(SALIDA, "casa_recorrido.blend"))

escena.render.filepath = os.path.join(SALIDA, "cuadros", "f_")
print("  [render] cuadros", escena.frame_start, "a", escena.frame_end,
      "->", escena.render.filepath)
bpy.ops.render.render(animation=True)
print("  [render] terminado")
