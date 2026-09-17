# Prompt para pegar en vivo (demo 2)

Antes de empezar: abrir Blender **vacío** con el add-on MCP conectado. No dejes abierto el proyecto de la carcasa Bloomit.

El plano ya está listo en `planos/casa-3-ambientes-plano.png`. Es una casa en dúplex de 3 ambientes sobre un lote de 100 m² de barrio cerrado, con cotas, corte e implantación.

Abrí Claude Code en la carpeta `demo-blender/` y pegá esto:

```
En planos/casa-3-ambientes-plano.png está el plano de una casa en dúplex. Seguí CLAUDE.md y levantala en 3D en Blender a escala, las dos plantas. Primero leé el plano y mostrame la lista de muros y aberturas como spec, preguntame lo que necesites de a una pregunta, y cuando confirme construí por etapas con renders. Usá superpowers de punta a punta. Tenés 20 minutos.
```

## Lo que el agente debería sacar solo del dibujo

No hace falta que le digas nada de esto, está todo rotulado en la lámina. Lo tenés en `planos/casa-3-ambientes-datos.md` para controlarlo mientras trabaja.

- Casa de 8,00 × 6,00 m, muros exteriores de 0,20 y tabiques de 0,10
- Altura libre 2,60, planta alta a +2,80, techo a +5,60
- Planta baja: estar-comedor, cocina, hall y toilette
- Planta alta: dos dormitorios y baño
- Aberturas con luz, alto y antepecho en el cuadro de datos de obra

**No le muestres `casa-3-ambientes-datos.md` antes de la prueba.** Ese archivo es la verdad de referencia: sirve para comparar después y para que vos sigas la demo sin perderte.

## Si querés cambiar la casa

El plano se regenera entero desde un script. Cambiar el lote, mover un tabique o agregar una abertura es editar una línea:

```bash
python planos/generar_plano_casa.py
```
