# Runbook de la charla ET21 — 18/09/2026

Todo lo que hicimos, con los comandos exactos para repetirlo en vivo. Está pensado para tenerlo abierto en una pantalla mientras hablás.

- **Charla:** 40 a 50 minutos. 15 de teoría, 25 de demo en paralelo, 5 de cierre.
- **Deck:** https://claude.ai/artifact/NkkADoYhKcgXugCkgJFBAL (19 slides, con notas del orador en cada una).
- **Carpeta de trabajo:** este repositorio

---

## 1. Antes de entrar al aula

Checklist de diez minutos. Si algo de esto falla, lo arreglás ahora y no en vivo.

| Qué | Cómo se comprueba | Si falla |
|---|---|---|
| Internet y proyector | Abrí el deck y https://et21.ar | Sin internet: el deck se baja como PDF desde su menú, y la demo 2 anda igual |
| Blender **vacío** | Abrirlo y cerrar el archivo de inicio | Si tiene abierto el proyecto de la carcasa Bloomit, cerralo. Los scripts arrancan de escena vacía |
| Node 20 o más | `node -v` | Verificado: v24.14 |
| Python 3.12 con Pillow | `python -c "import PIL; print(PIL.__version__)"` | Verificado: 12.2 |
| ffmpeg | `ffmpeg -version` | Verificado: 9.0 |
| Cuenta de Cloudflare | `cd demo-web/et21 && npx wrangler whoami` | Verificado el 17/09: sesión activa. Si pide login, `npx wrangler login` |
| Dependencias de la web | `ls demo-web/et21/node_modules` | Verificado. Si falta, `npm --prefix demo-web/et21 install` (30 segundos) |

Dejá **dos ventanas de Claude Code abiertas y listas**, una por demo, cada una en su carpeta:

```bash
cd demo-web
```

```bash
cd demo-blender
```

---

## 2. Los 15 minutos de teoría

El deck lleva las notas del orador en cada slide. La estructura es una escalera de cinco peldaños, cada concepto apoyado en el anterior:

1. **Estado de la IA** (slides 3 y 4). De chat a copiloto a agente. La frase que ordena todo: la IA ahora tiene manos.
2. **Cómo funciona un modelo** (slide 5). Predice la próxima palabra. Sin manos, sin internet, sin memoria. Esos tres límites son lo que resuelve todo lo que sigue.
3. **Herramientas y MCP** (slides 6 a 8). El modelo pide, el programa ejecuta. MCP como el USB‑C de la IA.
4. **Agentes** (slides 9 a 11). El loop. La anatomía. Subagentes en paralelo.
5. **El harness** (slide 12). El modelo es el motor, el harness es el auto. Claude Code, OpenCode, Cursor y Codex son harnesses.
6. **Cómo se hace uno** (slides 13 y 14). Tres niveles, y la tabla que separa MCP, skill, agente y plugin.

La slide 15 es **SDD**, Spec‑Driven Development. Es el puente hacia la demo: los dos agentes van a escribir la spec antes de tocar código, y eso se ve en pantalla.

---

## 3. Demo 1 — el sitio de la escuela

**Estado de partida:** el sitio ya existe y ya está publicado en https://et21.ar. El repo es `ezequielcorbalan/et21`, clonado en `demo-web/et21`, en la rama `deploy-et21-ar`. Todo verificado el 17/09: el sitio responde, el build compila en 7 segundos y la sesión de Cloudflare está activa.

Esto es importante decirlo en voz alta: **la demo no arranca de cero a propósito**. Agarrar un proyecto que ya está es lo que pasa de verdad en el trabajo.

### El prompt

Abrí Claude Code en `demo-web/` y pegá:

```
Seguí CLAUDE.md. El sitio de la escuela ya existe en et21/ y está publicado en et21.ar. Quiero agregarle la página de Taller respetando el diseño y los componentes que ya están, verificarla en el navegador y publicarla. Usá superpowers de punta a punta: brainstorming corto, spec, implementación y verificación con capturas y build verde. Rama nueva a partir de deploy-et21-ar, y pedime permiso antes de pushear o deployar. Tenés 20 minutos.
```

### Qué señalar mientras trabaja

1. Lee el proyecto y te cuenta lo que encontró, sin que nadie le explique nada.
2. Escribe la **spec antes de la primera línea de código**. Esto es la slide 14 en vivo.
3. Saca el contenido real del sitio viejo, `et21.com.ar/academica/taller/`.
4. Se saca capturas solo, ve los errores y los corrige.
5. **Pide permiso antes de publicar.** Momento a remarcar: el sitio es público.

### Comandos útiles

```bash
npm --prefix demo-web/et21 run dev
```

```bash
npm --prefix demo-web/et21 run build
```

```bash
cd demo-web/et21 && npx wrangler deploy
```

### Variantes si preferís otra tarea

Cambiá "la página de Taller" por "la sección de autoridades en institucional" (usa el componente `AuthorityGrid` que ya existe) o por "un post nuevo en el blog". El post es la más rápida, dejala de plan B si el tiempo aprieta.

### Si algo falla

- **El build falla:** mostralo. Que el agente lea el error y lo arregle es la parte más útil de la demo.
- **El deploy falla:** reintentá una vez. Nos pasó un error 500 de la API de Cloudflare al asociar el dominio, y se resolvió en el segundo intento.
- **GitHub no responde:** seguí local y dejá el push para el final.

---

## 4. Demo 2 — del plano al 3D

**Estado de partida:** el plano ya está dibujado, en `demo-blender/planos/casa-3-ambientes-plano.png`. Es una casa de 3 ambientes en dúplex, lote de 8,00 × 12,50 m.

### El prompt

Con Blender abierto y vacío, Claude Code en `demo-blender/`:

```
En planos/casa-3-ambientes-plano.png está el plano de una casa en dúplex. Seguí CLAUDE.md y levantala en 3D en Blender a escala, las dos plantas. Primero leé el plano y mostrame la lista de muros y aberturas como spec, preguntame lo que necesites de a una pregunta, y cuando confirme construí por etapas con renders. Usá superpowers de punta a punta. Tenés 20 minutos.
```

### Qué señalar

1. El agente **lee la imagen** y describe la casa en texto.
2. Arma la lista de muros y aberturas como spec, y **pide confirmación antes de construir**.
3. Construye por etapas, con un render al final de cada una.
4. Verifica midiendo el modelo contra el plano.

`planos/casa-3-ambientes-datos.md` es la verdad de referencia con cada muro en coordenadas. **No se la muestres al agente antes**, es para que vos sigas la demo y controles qué tan bien leyó.

### Si querés cambiar la casa

El plano se regenera entero desde un script:

```bash
python demo-blender/planos/generar_plano_casa.py
```

Todo sale de `demo-blender/planos/casa_datos.py`: lote, muros, aberturas, alturas, ambientes. Cambiar una medida ahí actualiza el plano y el 3D a la vez.

---

## 5. El material de respaldo, ya hecho

Si una demo se cae o el tiempo se va, tenés todo esto listo para mostrar.

### Del hospital, la prueba con una lámina real

La lámina original no está en este repo porque no es nuestra, pero el caso vale la pena contarlo igual.

Sirve para una idea importante: con una lámina a 1:500, el agente extrajo **las doce cotas de nivel con error cero** y fue honesto sobre lo que no podía leer, los tabiques, que a esa escala miden menos de un píxel. Ese contraste enseña más que un modelo que finge exactitud.

### De la casa, el 3D completo

| Archivo | Qué es |
|---|---|
| `ejemplos/casa-frente.png` | El frente desde la calle |
| `ejemplos/casa-aerea-pb.png` | Maqueta sin techo: planta baja |
| `ejemplos/casa-aerea-pa.png` | Maqueta sin techo: planta alta |
| `ejemplos/casa-patio.png` | Contrafrente desde el patio |
| `ejemplos/casa-recorrido.mp4` | Recorrido de 21 segundos por dentro |
| `salida/casa_3_ambientes.blend` | El modelo, se genera al correr los scripts |
| `salida/casa_recorrido.blend` | Igual, con gente, muebles y la cámara animada |

Las dos maquetas aéreas al lado de las dos plantas del plano son la comparación más clara que tenés.

---

## 6. Rehacer el 3D y el video desde cero

Sin abrir Blender, un comando encadena los tres pasos, guarda el .blend y renderiza los 504 cuadros:

```bash
cd demo-blender
```

```bash
blender -b --python scripts/render_recorrido.py
```

Tarda unos siete minutos, menos de un segundo por cuadro. Después se arma el video:

```bash
ffmpeg -y -framerate 24 -i salida/cuadros/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 19 -preset slow -movflags +faststart salida/casa-recorrido.mp4
```

Los tres pasos, por si querés correrlos sueltos desde el Blender abierto:

1. `scripts/construir_casa_3d.py` — muros, losas, escalera, terreno
2. `scripts/mobiliario_casa.py` — solados, muebles y puertas abiertas
3. `scripts/recorrido_casa.py` — figuras de escala, luces de sala y cámara animada

Para cambiar el recorrido, los puntos están al principio de `scripts/recorrido_casa.py`, uno por línea: fracción del recorrido, posición de la cámara y hacia dónde mira.

---

## 7. Las trampas, todas las que pisamos

Están acá para que no te sorprendan en vivo. Cada una nos costó tiempo.

### De Blender por MCP

- **No existe `bpy.context.active_object`.** Todo operador que dependa del objeto activo falla con AttributeError: `primitive_cylinder_add`, `object.camera_add`, `light_add`. Hay que construir con `bpy.data` y `bmesh`, creando los objetos con `bpy.data.objects.new(...)` y enlazándolos a la colección a mano.
- **El motor se llama `BLENDER_EEVEE`**, no `BLENDER_EEVEE_NEXT`. Conviene consultar los valores válidos antes de asignar.
- **Blender 5 cambió las curvas de animación.** `action.fcurves` ya no existe: ahora están en capas y slots. `recorrido_casa.py` tiene una función que funciona con las dos APIs.
- **Esta compilación no tiene salida de video.** `FFMPEG` no está en el enum de formatos. Por eso se renderizan PNG y se arman con ffmpeg.
- **Antes de abrir escena nueva, verificá que lo abierto esté guardado.** Y guardá siempre con `save_as_mainfile` en `salida/`, nunca encima del archivo original.

### De iluminación

- **Con el sol en 5,0 y vista Standard todo se recorta a blanco puro** y desaparecen las sombras. Los valores que funcionan afuera: sol 2,1, relleno 0,35, fondo de mundo 0,28.
- **Adentro, 110 W en un ambiente de cuatro por tres metros lo quema.** Van 26 W en dormitorios y estar, 18 W en el resto.
- **Para el contrafrente hay que mover el sol al norte**, si no queda a contraluz.
- **Sin solados el interior es una caja blanca sin referencias.** Con piso de madera y porcelanato se lee.

### De la animación

- **Las puertas cerradas se atraviesan** y se ve un rectángulo marrón a pantalla completa. `abrir_puertas()` rehace cada hoja girada noventa grados.
- **El solado de planta alta tapaba el hueco de la escalera.** El entrepiso estructural estaba bien, el piso de porcelanato lo cubría entero.
- **La caja de escalera no tiene nada que mirar de costado.** La cámara tiene que subir mirando hacia abajo a los escalones.
- **Lente de 21 mm.** Con menos ángulo no se lee un ambiente chico.

---

## 8. Dos historias que valen para contar

### El agente auditó su propio material

Antes de la charla le di la lámina a un agente sin decirle nada y le pedí que la leyera. No solo sacó las medidas: **verificó que las cadenas de cotas cerraran entre sí** y marcó cuatro cosas que faltaban. La más grave, que no había ancho ni posición de ninguna ventana, así que se podían trazar los muros pero no cortar las aberturas. Todo eso está corregido en el plano actual, con la planilla de carpinterías.

Lo que enseña: el agente fue honesto sobre lo que no podía deducir, en vez de inventar los datos.

### Modelar encontró errores que el plano escondía

Al armar el recorrido aparecieron dos fallas que en planta eran invisibles. La caja de escalera **no tenía salida en planta alta**, subías y quedabas encerrado. Y el tramo de subida **desembocaba contra la losa** del entrepiso.

Lo que enseña, y para alumnos de construcción vale oro: hay errores que un plano no delata y que aparecen apenas intentás caminar el espacio. Es la respuesta a por qué se modela.

---

## 9. Qué quedó pendiente

- **Exportar el deck a .pptx** como respaldo. Se baja desde el menú del propio deck.
- **Mergear la rama `deploy-et21-ar` a `main`** en el repo de la web, o abrir el pull request: https://github.com/ezequielcorbalan/et21/pull/new/deploy-et21-ar
- **Coolify** quedó documentado en `demo-web/CLAUDE.md` como alternativa, pero no se usó. Solo vale la pena si querés mostrar el servidor de la escuela.
