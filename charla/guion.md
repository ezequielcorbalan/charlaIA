# Guion de la charla

Cuarenta y cinco minutos. Quince de teoría, veinticinco de demo en vivo, cinco de cierre.

El deck que acompaña este guion tiene las mismas notas en cada slide. Acá están juntas para que las leas de corrido.

---

## Apertura · 1 minuto

Presentate y hacé la promesa de la charla: en cuarenta minutos van a entender qué es un agente de inteligencia artificial, y van a ver dos trabajando al mismo tiempo, uno armando un sitio web y otro levantando un plano en 3D.

Pediles que guarden las preguntas para el final, pero que si algo no se entiende levanten la mano.

**Arrancá las dos demos ahora**, antes de la teoría. Van a estar trabajando mientras hablás, y eso es parte del efecto.

---

## 1 · Dónde está la IA hoy · 3 minutos

Preguntá quién usó ChatGPT o Gemini. Van a levantar la mano casi todos. Eso es la etapa **chat**: le preguntás, te responde, todo queda en la ventana de texto.

Después vino el **copiloto**, que vive dentro del editor de código y sugiere mientras escribís. Sugiere, pero vos apretás el botón.

Hoy la etapa es el **agente**: le das un objetivo y lo cumple usando programas de verdad. Los modelos actuales trabajan varias horas seguidas en una misma tarea.

> El cambio no es que la IA sea más inteligente. Es que ahora **tiene manos**.

Tres cosas cambiaron para que eso fuera posible: el contexto se volvió enorme, así que le podés dar un proyecto entero; aprendió a usar herramientas, así que toca programas reales; y trabaja sola, planifica, prueba, ve el error y lo corrige.

Bajalo a las dos orientaciones. En computación ya se usa para escribir, probar y publicar software. En construcción, para leer planos, calcular cómputos, armar modelos y presupuestar. Las dos demos de hoy son exactamente eso.

---

## 2 · Cómo funciona un modelo · 2 minutos

Acá conviene desmitificar.

Un modelo es una función que recibe texto y devuelve la próxima palabra probable, muchas veces seguidas. Es impresionante lo que sale de ahí, pero tiene tres límites duros:

- **No tiene manos.** No ejecuta nada por sí solo.
- **No tiene internet.** Solo ve lo que le pasás en la conversación.
- **No tiene memoria.** Cerrás la ventana y se olvidó de todo.

> Todo lo que sigue en esta charla es darle manos, ojos y memoria.

Esos tres límites son el esqueleto del resto de la explicación. Si se entiende esto, lo demás cae solo.

---

## 3 · Herramientas y MCP · 4 minutos

### Herramientas

El modelo no ejecuta nada. Lo que hace es **escribir un pedido** con un formato acordado, por ejemplo "leer el archivo index.html". Un programa aparte lee ese pedido, lo ejecuta de verdad y le devuelve el resultado como texto. El modelo sigue con ese resultado en la conversación.

Insistí en el punto: **las manos las pone el programa, no el modelo**. Eso es justamente lo que lo hace controlable, porque el programa decide qué herramientas le da y cuáles le pide permiso.

### MCP

Antes de MCP, cada herramienta se conectaba a cada IA de forma distinta. Como cuando cada celular tenía su propio cargador.

MCP, Model Context Protocol, es el USB‑C: un programa expone sus funciones como servidor, y cualquier cliente las enchufa. Es un estándar abierto que adoptó toda la industria.

Un servidor MCP ofrece tres cosas: **tools**, que son acciones; **resources**, que son datos para leer; y **prompts**, que son recetas para tareas comunes.

Lo importante para ellos: cualquiera puede escribir un servidor MCP en unas decenas de líneas. Si en la escuela tienen un sistema propio, le pueden poner un servidor MCP y cualquier agente lo va a poder usar.

---

## 4 · Agentes · 3 minutos

Esta es **la** idea de la charla.

Un agente no es un modelo más grande. Es un modelo con herramientas metido en un **loop**: recibe un objetivo, piensa qué falta, usa una herramienta, mira el resultado y vuelve a pensar. Repite hasta que el objetivo está cumplido.

Cada vuelta del loop es una llamada al modelo. La diferencia con el chat es que el resultado de la herramienta **vuelve solo**, sin que vos copies y pegues.

Un agente tiene cuatro piezas: **instrucciones**, que dicen quién es y cómo trabaja; **herramientas**, que dicen qué puede tocar; **memoria**, que es la conversación más los archivos donde anota lo que aprende; y **permisos**, que dicen qué hace solo y qué pregunta antes.

> Un agente bueno no es el que hace de todo. Es el que tiene una tarea clara, pocas herramientas y límites.

Y un agente puede lanzar otros agentes. Cada uno con su propia conversación, sus herramientas y su tarea. Es lo que están viendo en las dos pantallas: dos subagentes en paralelo que no saben que el otro existe.

---

## 5 · El harness · 2 minutos

Acá hay una palabra que conviene que se lleven, porque explica algo que si no queda dando vueltas.

Si el modelo es el motor, el **harness** es el auto entero: el chasis, la caja, el volante y los pedales. Es el programa que envuelve al modelo y hace que sea usable.

Claude Code, OpenCode, Cursor, Codex y Aider son harnesses. **El modelo puede ser el mismo, y el resultado es distinto**, porque el harness es el que hace todo el trabajo alrededor:

- **Arma el pedido.** Decide qué entra en la conversación y en qué orden.
- **Maneja el contexto.** Cuando se llena, resume lo viejo para que el agente no pierda el hilo.
- **Ejecuta las herramientas** y le devuelve el resultado al modelo.
- **Aplica los permisos.** Qué corre solo, qué te pregunta.
- **Pone la interfaz**, el historial y la posibilidad de interrumpir.

La comparación que se entiende: un buen piloto con un auto malo pierde. **Elegir el harness importa tanto como elegir el modelo**, y por eso hay tantos proyectos compitiendo en esa capa.

Si preguntan cuál usar: la charla usa Claude Code, pero todo lo que están viendo se puede hacer con cualquiera de los otros.

---

## 6 · Cómo se hace un agente · 3 minutos

Tres formas, de fácil a difícil.

**Nivel 1, sin programar.** Un archivo de texto con el nombre, la descripción, qué herramientas puede usar y las instrucciones. Eso ya es un agente. Cualquiera de ellos lo puede escribir hoy.

**Nivel 2, unas líneas.** El Agent SDK es el mismo motor del harness, como librería de Python o TypeScript. Con diez líneas tenés un agente con herramientas de archivos y terminal.

**Nivel 3, el loop a mano.** Contra la API directa. Escribís vos el loop: llamás al modelo, si pide una herramienta la ejecutás y le devolvés el resultado, hasta que deja de pedir.

Los tres hacen lo mismo. Lo que cambia es cuánto control querés.

### La confusión más común

Cuatro palabras que se mezclan todo el tiempo. Cuatro verbos para separarlas:

| | Qué hace | Analogía |
|---|---|---|
| **MCP** | Conecta el modelo con un programa | El enchufe USB‑C |
| **Skill** | Le enseña a hacer una tarea | El manual de procedimientos |
| **Agente** | Ejecuta el loop hasta cumplir el objetivo | El empleado que hace el trabajo |
| **Plugin** | Empaqueta todo lo anterior para distribuirlo | La caja de herramientas |

Un agente **usa** skills y servidores MCP. Un plugin **los distribuye** para que otro los instale con un clic.

---

## 7 · Cómo se trabaja: SDD · 1 minuto

Spec‑Driven Development, o desarrollo guiado por especificación. Es la forma de trabajar con agentes que más se impuso.

En vez de decir "hacé la web" y rezar, el agente primero **pregunta**, después escribe una **especificación** con el objetivo, los límites y el criterio de éxito, arma un **plan** de pasos chicos, recién entonces **codea**, y al final **verifica** con evidencia.

El motivo es simple: un agente rápido con un pedido vago produce mucho código equivocado, muy rápido. La especificación es el contrato, lo que vos sabés del problema escrito antes de que el agente toque nada.

Para los de construcción, la analogía es directa: es el pliego antes de la obra.

Conectalo con lo que está pasando en las pantallas: los dos agentes van a mostrar la especificación antes de la primera línea de código. En la demo del plano, van a ver la lista de muros antes del primer muro.

---

## Demo en vivo · 25 minutos

Volvé a las pantallas. El detalle de qué señalar en cada momento está en `RUNBOOK.md`.

Lo que no hay que dejar pasar:

- El agente **entiende un proyecto ajeno** sin que nadie le explique nada.
- Escribe la **especificación antes de codear**.
- Se saca **capturas solo**, ve los errores y los corrige.
- **Pide permiso antes de publicar**.

Y si algo falla, mostralo. Que el agente lea un error y lo arregle es la parte más útil de toda la demostración.

---

## Cierre · 3 minutos

Sin dramatismo, y esto es importante: la herramienta **no reemplaza** saber programar ni saber de obra. Los multiplica. El que sabe le saca mucho más.

Para computación: el trabajo ya no es tipear código, es saber qué pedir, revisar lo que vuelve y entender por qué funciona.

Para construcción: planos, cómputos, modelos y presupuestos se van a hacer con estas herramientas. El que conoce la obra es el único que puede decir si lo que hizo la IA está bien o mal.

Tres pasos para empezar esta semana:

1. Instalen un agente de código y pídanle que les explique un proyecto que ya tengan.
2. Escriban un agente de nivel 1: un archivo de texto con una tarea chica y clara.
3. **Revisen todo lo que produce.** La IA se equivoca con muchísima seguridad, y el criterio lo ponen ustedes.

---

## Preguntas frecuentes

**¿Me va a sacar el trabajo?** Cambia el trabajo. El que sabe usar la herramienta queda mejor parado que el que no.

**¿Es gratis?** Los chats tienen planes gratuitos. Los agentes de código suelen ser pagos, y hay opciones abiertas.

**¿Puede romper algo?** Sí, por eso existen los permisos. Borrar y publicar siempre se preguntan.

**¿Qué harness conviene?** Probá dos o tres. Cambian rápido y la elección depende de con qué te sientas cómodo.

**¿Cómo aprendo?** Empezá por el nivel 1 y trabajá con especificación desde el primer día.
