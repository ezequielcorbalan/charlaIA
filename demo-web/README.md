# Demo 1 · El sitio de la escuela

Un agente agarra un sitio web que **ya existe**, le agrega una página respetando el diseño que ya tiene, la verifica en el navegador y la publica.

## Por qué no arranca de cero

A propósito. Agarrar un proyecto que ya está es lo que pasa de verdad en el trabajo, y muestra algo que impresiona más que escribir código nuevo: el agente **entiende un proyecto ajeno** sin que nadie le explique nada.

## Qué hay acá

| Archivo | Qué es |
|---|---|
| `CLAUDE.md` | Las reglas que sigue el agente durante la demo |
| `PROMPT.md` | El texto exacto para pegar en vivo |

El sitio en sí **no está en este repo**: vive en el suyo. Acá solo están las instrucciones.

## Para usarlo con el sitio de tu escuela

`CLAUDE.md` está escrito para el sitio de la ET21, que es Astro con Tailwind publicado en Cloudflare. Cambiá tres cosas:

1. **De dónde sale el repo** y dónde lo clonás.
2. **La descripción del proyecto**: qué tecnología usa, qué páginas tiene, qué colores y tipografías hay que respetar. Esto es lo más importante, porque es lo que hace que el agente no invente un diseño nuevo.
3. **Dónde se publica** y con qué comando.

Las reglas de trabajo, que son el resto del archivo, sirven tal cual: rama nueva, especificación antes del código, verificación con capturas, permiso antes de publicar.

## Si tu escuela no tiene sitio

La demo funciona creando uno de cero. Es menos impactante, porque se pierde la parte de entender un proyecto ajeno, pero es más fácil de preparar y el resto del guion no cambia.
