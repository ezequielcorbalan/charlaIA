# Prompt para pegar en vivo (demo 1)

Ya está listo: el repo clonado en `demo-web/et21`, `npm install` corrido, el build verificado y el sitio publicado en https://et21.ar.

Abrí Claude Code en la carpeta `demo-web/` y pegá esto:

```
Seguí CLAUDE.md. El sitio de la escuela ya existe en et21/ y está publicado en et21.ar. Quiero agregarle la página de Taller respetando el diseño y los componentes que ya están, verificarla en el navegador y publicarla. Usá superpowers de punta a punta: brainstorming corto, spec, implementación y verificación con capturas y build verde. Rama nueva a partir de deploy-et21-ar, y pedime permiso antes de pushear o deployar. Tenés 20 minutos.
```

Si preferís otra tarea, cambiá "la página de Taller" por "la sección de autoridades en institucional" o "un post nuevo en el blog sobre las orientaciones".

## Comandos útiles durante la demo

```bash
npm --prefix demo-web/et21 run dev
```

```bash
npm --prefix demo-web/et21 run build
```

```bash
cd demo-web/et21 && npx wrangler deploy
```
