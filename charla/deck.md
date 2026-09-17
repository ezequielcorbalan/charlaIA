# Las diapositivas

El deck original tiene 20 slides y notas del orador en cada una. Está hecho como artifact de Claude, que es una página web, no un PowerPoint.

**No está incluido en este repo** porque el formato es propio de esa plataforma. Lo que sí está es todo su contenido, en [`guion.md`](guion.md): cada slide tiene ahí su texto y sus notas.

## Rehacerlo

Si tenés Claude Code o Claude, pedile que arme el deck a partir del guion. Algo así funciona:

```
Armá una presentación de 20 slides a partir de charla/guion.md. Fondo oscuro, mucho diagrama y poco texto, pensada para proyector. Que cada slide lleve las notas del orador que están en el guion. En castellano rioplatense.
```

Si preferís PowerPoint o Google Slides, el guion se copia y pega igual: está estructurado por slide.

## Qué slides tiene

| # | Slide | Minutos |
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
| 17-18 | Apoyo para cada demo, para tener en pantalla mientras corren | — |
| 19 | Cierre | 3 |
| 20 | Preguntas | — |

Las slides 17 y 18 son las que dejás proyectadas mientras los agentes trabajan. Son tablas de "qué hace el agente" contra "qué ven ustedes", para ir señalando en qué paso está.

## Los diagramas que valen la pena

Si rehacés el deck, estos tres son los que más rinden en el aula:

- **El loop del agente.** Objetivo, pensar, herramienta, resultado, y la flecha que vuelve. Es la idea central de toda la charla.
- **MCP como USB‑C.** Un cliente en el centro y cuatro programas colgando de un bus. Se entiende de un vistazo.
- **La tabla de cuatro columnas.** MCP conecta, skill instruye, agente ejecuta, plugin empaqueta. Resuelve la confusión más común de una.
