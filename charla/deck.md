# Las diapositivas

Veinte diapositivas con notas del orador en cada una. Están en el repositorio de dos formas.

## 1. Para dar la charla: `deck.html`

Un solo archivo que se abre en cualquier navegador. No necesita internet ni instalar nada.

```
charla/deck.html
```

Bajalo, hacé doble clic y listo.

| Tecla | Qué hace |
|---|---|
| Flecha derecha, espacio, Enter | Avanzar |
| Flecha izquierda, retroceso | Volver |
| Inicio, Fin | Primera y última |
| **N** | Mostrar u ocultar las notas del orador |
| **F** | Pantalla completa |

La barra de abajo tiene los mismos botones, por si preferís el mouse. El número de diapositiva queda en la dirección del navegador, así que podés recargar sin perder el lugar, o abrir una diapositiva concreta con `deck.html#12`.

Las notas aparecen en un panel a la derecha. Si proyectás con pantalla extendida, abrí el archivo dos veces: una en el proyector a pantalla completa y otra en tu monitor con las notas abiertas.

## 2. Para editarlas: `slides/`

Cada diapositiva es un archivo HTML suelto en `charla/slides/`, y `charla/deck.json` dice en qué orden van y qué tipografías usan.

Después de cambiar algo, volvé a armar el archivo único:

```bash
python charla/exportar_deck.py
```

### Cómo está hecha una diapositiva

Cada archivo tiene un solo `<section>` sobre un lienzo fijo de 1920 × 1080 píxeles, con todos los estilos en el atributo `style`. El `<aside>` del final son las notas del orador: no se dibujan en la diapositiva, van al panel lateral.

```html
<section id="ejemplo" style="background:#0E1320; color:#F3F0E8; padding:128px; display:flex; flex-direction:column; gap:40px">
  <h2 style="font-size:72px">Un título</h2>
  <p style="font-size:28px">Un párrafo.</p>
  <aside>Lo que decís mientras se ve esta diapositiva.</aside>
</section>
```

Hay dos elementos propios que el exportador dibuja por vos:

- `<x-icon name="Book">` es un ícono. Los disponibles son Book, Tool, Activity, Warning, Lightning, Database, Lightbulb, Lock y Users. Para agregar otro, sumá su dibujo al diccionario `ICONOS` de `exportar_deck.py`.
- `<x-connector x1="0" y1="0" x2="100" y2="50">` es una flecha entre dos puntos, para los diagramas. Acepta `route` (`straight`, `hv`, `vh`, `elbow`) y `head` (`end`, `both`, `none`). Sin coordenadas y con un ancho, queda como una flecha suelta para separar cajas en una fila.

Si una diapositiva queda más alta que 1080, el exportador achica su bloque más grande para que entre. Lo hace con `transform`, así que los diagramas no se desalinean.

## 3. Si preferís PowerPoint

El texto de cada diapositiva está también en [`guion.md`](guion.md), ordenado y con las notas. Se copia y pega.

## Qué diapositivas hay

| # | Diapositiva | Minutos |
|---|---|---|
| 1 | Portada | 1 |
| 2 | Agenda | 0,5 |
| 3-4 | Dónde está la IA hoy | 3 |
| 5 | Cómo funciona un modelo | 2 |
| 6-8 | Herramientas y MCP | 4 |
| 9-11 | Agentes, anatomía y subagentes | 3 |
| 12 | El harness | 2 |
| 13-14 | Cómo se hace un agente, y la tabla comparativa | 3 |
| 15 | SDD, primero la especificación | 1 |
| 16 | Transición a la demo | — |
| 17-18 | Apoyo para cada demo | — |
| 19 | Cierre | 3 |
| 20 | Preguntas | — |

Las diapositivas 17 y 18 son las que dejás proyectadas mientras los agentes trabajan. Son tablas de "qué hace el agente" contra "qué ven ustedes", para ir señalando en qué paso está.

## Los tres diagramas que más rinden

Si rehacés el deck o lo adaptás, estos son los que mejor funcionan en el aula:

- **El loop del agente.** Objetivo, pensar, herramienta, resultado, y la flecha que vuelve. Es la idea central de toda la charla.
- **MCP como USB‑C.** Un cliente a la izquierda y cuatro programas colgando de un bus. Se entiende de un vistazo.
- **La tabla de cuatro columnas.** MCP conecta, skill instruye, agente ejecuta, plugin empaqueta. Resuelve la confusión más común de una.
