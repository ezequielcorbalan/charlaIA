# Charla: IA, MCP y agentes

Material completo de una charla de 45 minutos sobre inteligencia artificial, MCP y agentes, para alumnos de escuela técnica. Está armada y probada para las orientaciones de **Computación** y **Construcción**, pero sirve para cualquier curso de secundaria o terciario.

Se dio por primera vez en la Escuela Técnica N° 21 D.E. 10 "Fragata Escuela Libertad", en Buenos Aires.

**Está todo acá: el guion, las dos demos en vivo y los archivos para que funcionen.** Podés usarlo tal cual, cambiar las demos por las tuyas, o tomar solo las partes que te sirvan.

---

## Qué incluye

| Carpeta | Qué hay |
|---|---|
| [`charla/guion.md`](charla/guion.md) | El guion de los 15 minutos de teoría, minuto a minuto |
| [`charla/deck.md`](charla/deck.md) | Cómo rehacer las diapositivas |
| [`RUNBOOK.md`](RUNBOOK.md) | El operativo del día: checklist previo, qué decir en cada momento, qué hacer si algo falla |
| [`demo-web/`](demo-web/) | Demo 1: un agente que trabaja sobre un sitio web real y lo publica |
| [`demo-blender/`](demo-blender/) | Demo 2: un agente que lee un plano de arquitectura y lo levanta en 3D |

## La idea de la charla

Quince minutos de teoría, veinticinco de demostración en vivo y cinco de cierre. La teoría es una escalera de seis escalones, cada uno apoyado en el anterior:

1. **Dónde está la IA hoy.** De chat a copiloto a agente. La frase que ordena todo: la IA ahora tiene manos.
2. **Cómo funciona un modelo.** Predice la próxima palabra. No ejecuta nada, no ve internet, no recuerda. Esos tres límites son lo que resuelve todo lo que viene después.
3. **Herramientas y MCP.** El modelo pide, el programa ejecuta. MCP es el estándar que los conecta.
4. **Agentes.** Un loop: objetivo, pensar, usar una herramienta, mirar el resultado, repetir.
5. **El harness.** Si el modelo es el motor, el harness es el auto. Claude Code, OpenCode, Cursor y Codex son harnesses: el modelo puede ser el mismo y el resultado cambia.
6. **Cómo se hace uno**, y en qué se diferencia de una skill, un plugin y un servidor MCP.

Después arrancan las dos demos **al mismo tiempo**, en dos pantallas, mientras vos seguís hablando. Que los alumnos vean dos agentes trabajando en paralelo es la mitad del impacto.

## Las dos demos

### Demo 1: un sitio web real

Un agente agarra el sitio de la escuela, que **ya existe**, le agrega una página respetando el diseño que ya tiene, la verifica en el navegador y la publica.

Esto es deliberado: no arranca de cero. Agarrar un proyecto que ya está es lo que pasa de verdad en el trabajo, y muestra algo que impresiona más que escribir código desde cero, que es un agente **entendiendo un proyecto ajeno sin que nadie le explique nada**.

### Demo 2: de un plano a un modelo 3D

Un agente lee la imagen de un plano de arquitectura, saca las medidas, arma la lista de muros como especificación, pide confirmación y recién entonces construye la casa en Blender.

Para alumnos de construcción es la demo más fuerte, porque el agente hace exactamente lo que ellos aprenden a hacer: leer un plano y pasarlo a volumen.

---

## Cómo lo adaptás a tu escuela

### Lo mínimo

Cambiá el nombre de la escuela y los datos del orador en el guion, y usá el resto tal cual. El plano de la casa y los archivos 3D ya están hechos y probados.

### La demo web, con tu sitio

`demo-web/CLAUDE.md` está escrito para el sitio de la ET21. Para usarlo con el tuyo, cambiá tres cosas en ese archivo:

1. La dirección del repositorio y dónde está clonado.
2. La descripción del proyecto: qué tecnología usa, qué páginas tiene, qué colores y tipografías hay que respetar.
3. Dónde se publica.

Si tu escuela no tiene sitio, la demo funciona igual creando uno de cero. Es menos impactante, pero más fácil de preparar.

### La demo 3D, con otra casa

Todo el plano sale de un solo archivo: [`demo-blender/planos/casa_datos.py`](demo-blender/planos/casa_datos.py). Ahí están el lote, los muros, las aberturas, las alturas y los ambientes, en metros.

Cambiás una medida, corrés el generador, y **el plano y el modelo 3D se actualizan los dos**. No pueden contradecirse porque leen lo mismo.

```bash
python demo-blender/planos/generar_plano_casa.py
```

---

## Qué necesitás instalado

| Para qué | Qué |
|---|---|
| Las dos demos | Un agente de código. La charla usa Claude Code, pero el guion sirve igual con otro |
| Dibujar el plano | Python 3.10 o más, con Pillow (`pip install pillow`) |
| El modelo 3D | Blender 4.2 o más. Probado en 5.1 |
| Armar el video | ffmpeg, solo si querés rehacer el recorrido |
| La demo web | Node 20 o más, y lo que use tu sitio |

Para manejar Blender desde el agente hace falta un servidor MCP de Blender. Si no lo tenés, la demo funciona igual: el agente escribe el script y lo ejecutás vos desde Blender. Es menos mágico pero más robusto, y para explicar qué está pasando incluso es mejor.

---

## Probar que todo anda, antes de la charla

### El plano

```bash
python demo-blender/planos/generar_plano_casa.py
```

Deja dos láminas en `demo-blender/planos/`: la técnica con cotas y la de anteproyecto con mobiliario.

### El modelo 3D y el video

Un solo comando arma la casa, le pone muebles y gente, y renderiza el recorrido completo. Tarda unos siete minutos.

```bash
blender -b --python demo-blender/scripts/render_recorrido.py
```

Deja los cuadros en `demo-blender/salida/cuadros/`. Para armar el video:

```bash
ffmpeg -framerate 24 -i demo-blender/salida/cuadros/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 19 demo-blender/salida/casa-recorrido.mp4
```

En `demo-blender/ejemplos/` están los resultados ya hechos, por si querés verlos sin correr nada, o tenerlos de respaldo si una demo se cae en vivo.

---

## Lo que aprendimos preparándola

Estas dos cosas son, para nosotros, lo más valioso que salió de todo el proceso. Valen más que cualquier demo que salga bien.

### El agente auditó su propio material

Antes de la charla le dimos el plano a un agente sin decirle nada y le pedimos que lo leyera. No solo sacó las medidas: **verificó que las cadenas de cotas cerraran entre sí** y marcó cuatro cosas que faltaban. La más grave, que no había ancho ni posición de ninguna ventana, así que se podían trazar los muros pero no cortar las aberturas.

Lo importante: fue honesto sobre lo que no podía deducir, en lugar de inventar los datos que faltaban. Eso es exactamente lo que hay que enseñarles a esperar de estas herramientas.

### Modelar encontró errores que el plano escondía

Al armar el recorrido en 3D aparecieron dos fallas que en planta eran invisibles: la caja de escalera **no tenía salida en el piso de arriba**, subías y quedabas encerrado; y el tramo de subida **desembocaba contra la losa**.

Para alumnos de construcción esto vale oro. Es la respuesta concreta a por qué se modela: hay errores que un plano no delata y que aparecen apenas intentás caminar el espacio.

---

## Las trampas técnicas

`RUNBOOK.md` tiene la lista completa de las doce cosas que nos costaron tiempo. Leelas **antes** de la charla, no durante. Las tres que más probablemente te toquen:

- **Blender por MCP no expone el objeto activo.** Los operadores que dependen de él fallan. Hay que construir con la API de datos.
- **Con el sol muy fuerte y la vista en Standard, todo se recorta a blanco puro** y desaparecen las sombras. El render parece roto y no lo está.
- **Si el agente atraviesa puertas cerradas en un recorrido**, se ve un rectángulo de color a pantalla completa. Las hojas tienen que quedar abiertas.

---

## Licencia y créditos

Usalo, cambialo y compartilo libremente. Si lo das en tu escuela y le hacés mejoras, un pull request es bienvenido: la idea es que el material vaya mejorando de escuela en escuela.

Preparado por Ezequiel Corbalán para la ET N° 21 "Fragata Escuela Libertad", septiembre de 2026.
