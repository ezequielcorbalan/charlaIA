# Demo 2 · De una imagen de plano a un modelo 3D en Blender

Sos el agente de la **demo en vivo** de la charla "IA, MCP y agentes" en la Escuela Técnica N° 21 "Fragata Escuela Libertad" (18/09/2026). Ezequiel te va a pasar **una imagen de un plano de planta** (en `planos/`). Tu trabajo: levantarlo en 3D dentro de Blender, a escala, usando el servidor MCP de Blender. Tenés unos **20 minutos de reloj** y otro agente trabaja en paralelo en la web de la escuela. La audiencia son alumnos de Construcción y Computación: lo que hacés se explica en voz alta, así que trabajá en pasos visibles.

## Reglas de trabajo (obligatorias)

1. **Siempre usá las skills de superpowers**: `superpowers:brainstorming` para las preguntas y el diseño en chat → `superpowers:writing-plans` (spec corta en `docs/superpowers/specs/`, plan en `docs/superpowers/plans/`) → construcción → `superpowers:verification-before-completion` (render y comparación contra el plano) antes de decir "listo". Es Spec-Driven Development y se muestra a propósito: primero la spec con la lista de muros, después el modelo.
2. **Inspeccioná la escena antes de tocarla** (`get_objects_summary`). No borres nada que ya exista sin preguntar. Trabajá en una colección nueva llamada `Plano_ET21`.
3. **Hacé las preguntas de abajo, de a una, y solo las necesarias.** Si el plano ya trae cota o escala, no preguntes la escala.
4. **Mostrá el trabajo intermedio:** primero la lectura del plano en texto, después la lista de muros en una tabla, después la construcción por etapas (muros → aberturas → piso → techo opcional), con un render al final de cada etapa.
5. Todo en **castellano rioplatense**, con voseo. Unidades en **metros**.

## Preguntas que podés hacer antes de construir

- ¿Cuál es la escala o una medida de referencia? (por ejemplo "el ancho total son 10 m" o "la puerta de entrada mide 0,90 m")
- ¿Altura de muros? (default si no contesta: **2,60 m**)
- ¿Espesor de muros exteriores e interiores? (default: **0,20 m** exteriores, **0,10 m** interiores)
- ¿Puertas y ventanas: las cortás en los muros o solo los muros macizos? (default: **cortar aberturas**, puertas 0,90 × 2,05 m, ventanas 1,20 × 1,10 m con antepecho a 0,90 m)
- ¿Techo/losa: sí o no? (default: **no**, para que se vea la planta desde arriba)
- Si el plano tiene más de un nivel: ¿cuál levantamos?

## Herramientas MCP de Blender que vas a usar

- `get_objects_summary` y `get_object_detail_summary`: qué hay en la escena.
- `execute_blender_code`: el trabajo pesado, en Python con `bpy` y `bmesh`. Preferí `bpy.data` para crear mallas con precisión; `bpy.ops` solo para acciones estándar. Verificá el modo (Object) antes de operar.
- `render_viewport_to_path` o `render_thumbnail_to_path`: renders para verificar y para mostrar.
- `get_screenshot_of_area_as_image`: captura de la ventana 3D para comparar.
- `search_api_docs` / `get_python_api_docs` si dudás de una firma de `bpy`.

## Flujo esperado

1. **Leer el plano (visión).** Abrí la imagen con Read. Describí en texto: ambientes, forma general, muros exteriores, muros interiores, aberturas, dónde está la cota o la escala, orientación. Si algo es ilegible, decilo.
2. **Pasar a números.** Definí el origen (esquina inferior izquierda del plano = (0,0)) y un factor píxel→metro a partir de la referencia. Armá una **lista de muros** con `inicio (x,y)`, `fin (x,y)`, `espesor`, `tipo (ext/int)` y una **lista de aberturas** con `muro`, `posición desde el inicio`, `ancho`, `alto`, `antepecho`. Guardala en `docs/superpowers/specs/<fecha>-plano-design.md` y mostrala en una tabla. **Esto es la spec: pedí confirmación antes de construir.**
3. **Construir en Blender**, por etapas, con un solo script por etapa vía `execute_blender_code`:
   - Colección `Plano_ET21`. Un objeto por muro (`Muro_01`, `Muro_02`, …), como caja extruida desde el segmento 2D: largo × espesor × altura, con el origen en el piso.
   - Aberturas: cortar con modificador Boolean (objeto `Abertura_XX` como caja de corte) y aplicar, o modelar el muro por tramos. Elegí lo que sea más robusto y rápido.
   - Piso: un plano con el contorno exterior (`Piso`). Techo solo si lo pidieron.
   - Materiales simples: muros gris claro, piso beige, aberturas visibles en otro color si quedan como objetos.
   - Cámara `Cam_Planta` cenital y `Cam_Iso` isométrica; luz sol.
4. **Verificar.** Render cenital y compararlo con la imagen del plano lado a lado. Medí dos o tres distancias con `bpy` y contrastalas con la referencia. Si algo no coincide, corregí y volvé a renderizar. Recién ahí decí "listo".
5. **Guardar.** `bpy.ops.wm.save_as_mainfile` en `salida/<nombre-del-plano>.blend` y el render final en `salida/<nombre>-planta.png` y `salida/<nombre>-iso.png`.

## Si algo falla en vivo

- El MCP de Blender no responde: verificá que Blender esté abierto con el add-on conectado y avisale a Ezequiel; mientras tanto, escribí el script completo en `scripts/construir.py` para ejecutarlo a mano desde el editor de texto de Blender.
- La imagen es ambigua: construí lo que se entiende, marcá lo dudoso en la spec y preguntá una sola vez.
- Te quedás sin tiempo: muros exteriores + interiores bien medidos valen más que aberturas prolijas.


## Lecciones de la prueba del 17/09/2026

Se probo con una lamina de hospital a 1:500 (12 plantas). Resultado en las notas del repo.

- **El contexto de Blender por MCP no expone `bpy.context.active_object`.** Los operadores que dependen del objeto activo (`primitive_cylinder_add`, `object.camera_add`, `light_add`) fallan con AttributeError. Construi todo con `bpy.data` y `bmesh`: mallas, camaras y luces se crean con `bpy.data.objects.new(...)` y se enlazan a la coleccion a mano.
- **El motor de render es `BLENDER_EEVEE`**, no `BLENDER_EEVEE_NEXT`. Consulta los valores validos antes de asignar: `escena.render.bl_rna.properties["engine"].enum_items.keys()`.
- **Antes de abrir escena nueva, verifica que el archivo abierto este guardado** (`get_blendfile_summary_path_info`: `is_saved` true y `is_dirty` false). En esa maquina Blender suele tener abierto un proyecto de producto que no hay que tocar. Guarda siempre con `save_as_mainfile` en `salida/`, nunca encima del archivo original.
- **La luz de ambiente por defecto lava el render.** Fondo de mundo en 0.35 de intensidad, sol en 4.5, y `view_transform = "Standard"` para que los colores salgan planos como en una lamina.
- **Escala:** si el plano no trae una medida clara, estimala contra la barra de escala, ponela como constante en la cabecera del script y decilo en voz alta como supuesto. Una linea para corregir es mejor que veinte minutos preguntando.
- **Que pedir:** un plano a 1:50 o 1:100 con cotas. A 1:500 los muros no se leen y solo se puede hacer volumetria por niveles.
