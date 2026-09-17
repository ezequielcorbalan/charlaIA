# Demo 2 · Del plano al 3D

Un agente lee la imagen de un plano de arquitectura, saca las medidas, arma la lista de muros como especificación y construye la casa en Blender.

## Qué hay acá

| Carpeta | Qué es |
|---|---|
| `planos/` | El plano y el archivo del que sale todo |
| `scripts/` | Los cuatro scripts de Blender |
| `ejemplos/` | Renders y video ya hechos, para ver el resultado sin correr nada |
| `salida/` | Donde los scripts dejan lo que generan. Vacía en el repo |
| `CLAUDE.md` | Las reglas que sigue el agente durante la demo |
| `PROMPT.md` | El texto exacto para pegar en vivo |

## El plano

Todo sale de `planos/casa_datos.py`: el lote, los muros, las aberturas, las alturas y los ambientes, en metros. Cambiás una medida ahí y se actualizan el plano y el 3D a la vez.

```bash
python planos/generar_plano_casa.py
```

Deja dos láminas: `casa-3-ambientes-plano.png`, la técnica con cotas y planilla de carpinterías, y `casa-3-ambientes-anteproyecto.png`, con mobiliario.

`planos/casa-3-ambientes-datos.md` es la verdad de referencia, con cada muro en coordenadas. **No se la muestres al agente antes de la demo**: sirve para que vos controles qué tan bien leyó.

## El 3D y el video

Un comando arma la casa, le pone muebles y gente, y renderiza el recorrido completo. Tarda unos siete minutos.

```bash
blender -b --python scripts/render_recorrido.py
```

```bash
ffmpeg -framerate 24 -i salida/cuadros/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 19 salida/casa-recorrido.mp4
```

Los tres pasos por separado, si querés correrlos desde Blender abierto:

1. `scripts/construir_casa_3d.py` — muros, losas, escalera, terreno
2. `scripts/mobiliario_casa.py` — solados, muebles y puertas abiertas
3. `scripts/recorrido_casa.py` — figuras de escala, luces y cámara animada

## Si no tenés el servidor MCP de Blender

La demo funciona igual. El agente escribe el script y vos lo ejecutás desde el editor de texto de Blender. Es menos vistoso, pero más robusto y hasta más claro para explicar qué está pasando.
