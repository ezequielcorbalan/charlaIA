# Casa de 3 ambientes en dúplex — datos del proyecto

Verdad de referencia del plano `casa-3-ambientes-plano.png`. Sirve para dos cosas: corregir el dibujo si hace falta, y comparar contra lo que el agente extrae de la imagen durante la demo. **No se la pases al agente antes de la prueba.**

Origen (0,0) en la esquina exterior suroeste de la casa. X crece al este, Y crece al norte, hacia el fondo. El frente da al sur.

## Lote y ocupación

| Concepto | Medida |
|---|---|
| Lote | 8,00 × 12,50 m = 100,00 m² |
| Retiro de frente | 8,00 × 3,00 = 24,00 m² |
| Huella de la casa | 8,00 × 6,00 = 48,00 m² |
| Patio de fondo | 8,00 × 3,50 = 28,00 m² |
| Cubierta total | 96,00 m² en dos plantas |

## Alturas

| Concepto | Medida |
|---|---|
| Altura libre por planta | 2,60 m |
| Espesor de losa | 0,20 m |
| Nivel de planta alta | +2,80 m |
| Nivel de techo | +5,60 m |
| Muros exteriores y medianeras | 0,20 m |
| Tabiques interiores | 0,10 m |

## Muros, planta baja

Rectángulos en metros, `x0, y0, x1, y1`.

| Muro | x0 | y0 | x1 | y1 | Tipo |
|---|---|---|---|---|---|
| Frente sur | 0,00 | 0,00 | 8,00 | 0,20 | exterior |
| Fondo norte | 0,00 | 5,80 | 8,00 | 6,00 | exterior |
| Medianera oeste | 0,00 | 0,00 | 0,20 | 6,00 | exterior |
| Medianera este | 7,80 | 0,00 | 8,00 | 6,00 | exterior |
| Estar / servicios | 4,60 | 0,20 | 4,70 | 5,80 | interior |
| Estar / cocina | 0,20 | 3,50 | 4,60 | 3,60 | interior |
| Hall / paso | 4,70 | 1,70 | 7,80 | 1,80 | interior |
| Toilette, oeste | 6,10 | 1,80 | 6,20 | 3,00 | interior |
| Toilette, norte | 6,20 | 3,00 | 7,80 | 3,10 | interior |

## Muros, planta alta

| Muro | x0 | y0 | x1 | y1 | Tipo |
|---|---|---|---|---|---|
| Los cuatro exteriores | | | | | iguales a planta baja |
| Dormitorio 1 / dormitorio 2 | 4,20 | 0,20 | 4,30 | 3,20 | interior |
| Dormitorio 1 / paso | 0,20 | 3,40 | 4,20 | 3,50 | interior |
| Dormitorio 2 / paso | 4,30 | 3,10 | 7,80 | 3,20 | interior |
| Baño / paso | 2,60 | 3,50 | 2,70 | 5,80 | interior |
| Paso / escalera | 5,60 | 3,20 | 5,70 | 5,80 | interior |

## Aberturas, planta baja

En la lámina cada una lleva su referencia en un círculo azul, y la planilla de carpinterías repite ancho, alto, antepecho y posición.

| Abertura | Muro | Posición | Luz | Alto | Antepecho |
|---|---|---|---|---|---|
| Puerta de entrada | frente sur | x 5,60 a 6,50 | 0,90 | 2,10 | — |
| Ventana del estar | frente sur | x 1,20 a 3,60 | 2,40 | 1,50 | 0,90 |
| Puerta ventana al patio | fondo norte | x 1,40 a 3,00 | 1,60 | 2,10 | — |
| Puerta hall a estar | estar / servicios | y 0,60 a 1,40 | 0,80 | 2,00 | — |
| Puerta paso a cocina | estar / servicios | y 4,60 a 5,40 | 0,80 | 2,00 | — |
| Puerta de toilette | toilette oeste | y 2,00 a 2,70 | 0,70 | 2,00 | — |
| Vano hall a paso | hall / paso | x 4,90 a 5,90 | 1,00 | 2,10 | — |

## Aberturas, planta alta

| Abertura | Muro | Posición | Luz | Alto | Antepecho |
|---|---|---|---|---|---|
| Ventana dormitorio 1 | frente sur | x 1,40 a 3,20 | 1,80 | 1,50 | 0,90 |
| Ventana dormitorio 2 | frente sur | x 5,20 a 6,80 | 1,60 | 1,50 | 0,90 |
| Ventana del baño | fondo norte | x 0,90 a 1,50 | 0,60 | 1,50 | 0,90 |
| Puerta dormitorio 1 | dormitorio 1 / paso | x 3,20 a 4,00 | 0,80 | 2,00 | — |
| Puerta dormitorio 2 | dormitorio 2 / paso | x 4,60 a 5,40 | 0,80 | 2,00 | — |
| Puerta del baño | baño / paso | y 4,40 a 5,10 | 0,70 | 2,00 | — |
| Vano de paso a escalera | paso / escalera | y 3,25 a 4,25 | 1,00 | 2,05 | — |

## Ambientes

| Planta | Ambiente | Medidas | Superficie |
|---|---|---|---|
| Baja | Estar - comedor | 4,40 × 3,30 | 14,52 m² |
| Baja | Cocina | 4,40 × 2,20 | 9,68 m² |
| Baja | Hall de acceso | 3,10 × 1,50 | 4,65 m² |
| Baja | Toilette | 1,60 × 1,20 | 1,92 m² |
| Baja | Paso | 1,40 × 4,00 | 5,60 m² |
| Baja | Escalera | 2,10 × 2,60 | 5,46 m² |
| Alta | Dormitorio 1 | 4,00 × 3,20 | 12,80 m² |
| Alta | Dormitorio 2 | 3,50 × 2,90 | 10,15 m² |
| Alta | Baño | 2,40 × 2,30 | 5,52 m² |
| Alta | Paso | 2,90 × 2,60 | 7,54 m² |
| Alta | Escalera | 2,10 × 2,60 | 5,46 m² |

## Escalera

En U, dentro de `x 5,70 a 7,80`, `y 3,20 a 5,80`. Dieciséis alzadas de 0,175 m, pedadas de 0,26 m, dos tramos de siete escalones con descanso. Sube contra la medianera este y baja por el tramo oeste.

## Cómo regenerar el plano

```bash
python demo-blender/planos/generar_plano_casa.py
```

Todas las medidas salen de las constantes y las listas del principio del script. Cambiar el lote a 10,00 × 10,00, mover un tabique o agregar una abertura es editar una línea y volver a correrlo.


## Qué se corrigió tras la prueba de lectura del 17/09/2026

Un agente leyó la lámina a ciegas y encontró cuatro fallas reales. Todas están arregladas:

1. **Faltaban el ancho y la posición de las ventanas.** Sin eso no se pueden cortar las aberturas. Se agregó la planilla de carpinterías, con referencia, luz, alto, antepecho y posición de cada abertura respecto del origen, más una marca en círculo sobre cada una en la planta.
2. **El rótulo del toilette quedaba pisado por el barrido de la puerta.** Se corrió a la derecha.
3. **Las cotas verticales estaban dibujadas adentro de la casa**, en texto chico y rotado. Ahora van por fuera y más grandes, y se agregaron cadenas del lado derecho que fijan dónde arrancan los tabiques.
4. **El rótulo del paso contradecía el cuadro de superficies**, porque uno incluía la escalera y el otro no. Ahora el cuadro se calcula de la misma geometría que el dibujo, con el paso y la escalera en filas separadas, así no puede volver a desincronizarse.


## Corrección del 17/09/2026, al modelar el 3D

Al levantar la casa en Blender aparecieron dos errores que el plano solo no dejaba ver:

1. **La escalera no tenía salida en planta alta.** El tabique entre el paso y la caja de escalera no tenía ninguna abertura: se subía y se quedaba encerrado. Se agregó el vano **VA2**, de 1,00 m, en el tabique `x 5,60 a 5,70`, entre `y 3,25` y `y 4,25`.
2. **El segundo tramo chocaba contra la losa.** La escalera subía por el tramo oeste y llegaba debajo del entrepiso. Se invirtieron los tramos: ahora sube contra la medianera este y el segundo tramo desemboca al lado del vano, que es como ya estaba dibujado en el plano.

Las dos cosas se corrigieron en `casa_datos.py`, así que el plano y el 3D quedaron corregidos a la vez. Es un buen ejemplo para la charla: modelar en 3D encuentra errores que en planta pasan desapercibidos.
