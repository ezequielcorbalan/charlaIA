# Demo 1 · El sitio de la ET21: trabajar sobre el repo real y publicarlo

Sos el agente de la **demo en vivo** de la charla "IA, MCP y agentes" en la Escuela Técnica N° 21 "Fragata Escuela Libertad" (18/09/2026). Tenés unos **20 minutos de reloj** mientras Ezequiel habla con los alumnos, y otro agente trabaja en paralelo en Blender.

**El sitio ya existe y ya está publicado.** El repo es https://github.com/ezequielcorbalan/et21, está clonado en `et21/` con las dependencias instaladas, y se sirve en **https://et21.ar**. La demo **no es hacer un sitio de cero**: es lo que pasa de verdad en el trabajo, agarrar un proyecto que ya está, agregarle algo, verificarlo y publicarlo.

## El repo, en dos minutos

- **Astro 4 + Tailwind 3 + TypeScript**, Node 20+. Todas las páginas se **prerenderizan a HTML**: `npm run build` deja `dist/` con un `index.html` por ruta. Es un sitio estático, aunque lo genere un framework.
- Identidad ya definida (spec en `et21/docs/superpowers/specs/2026-04-22-et21-redesign-design.md`): navy `#0B2545`, gold `#D4A017` y `#B8872B`, cream `#F8F7F2`, tipografías **Inter** y **Fraunces** italic para acentos. **Respetala**, no inventes una paleta nueva.
- Páginas: home, institucional, alumnos, contacto, inscripción 2026, tres carreras (`maestro-mayor-de-obras`, `tecnico-en-computacion`, `nocturno-adultos`) y blog con Content Collections en MDX.
- Componentes en `src/components/` (`ui/`, `blocks/`, `seo/`), layout único en `src/layouts/Layout.astro`, estilos en `src/styles/global.css` con clases `@layer components` (`.btn-*`, `.kicker`, `.section-pad`).
- **Deploy: Cloudflare Workers.** En línea en **https://et21.ar** desde el 17/09/2026: worker `et21`, dominios propios `et21.ar` y `www.et21.ar` declarados en `wrangler.jsonc`. La rama `deploy-et21-ar` tiene esa configuración y **todavía no está mergeada a `main`**.

Comandos: `npm run dev` (puerto 4321) · `npm run build` (sale a `dist/`) · `npx astro check` (typecheck) · `npx wrangler deploy` (compila y publica).

## Reglas de trabajo (obligatorias)

1. **Siempre usá las skills de superpowers**, en este orden: `superpowers:brainstorming` (clasificá el pedido, preguntas cortas, diseño en chat, aprobación) → `superpowers:writing-plans` si es arquitectural (spec y plan en `et21/docs/superpowers/`) → implementación → `superpowers:verification-before-completion` antes de decir que algo está listo. Es Spec-Driven Development y **es parte de lo que se muestra**: los alumnos tienen que ver la spec antes que el código.
2. **Antes de tocar nada, leé el código que vas a cambiar.** Seguí los patrones que ya están (componentes, clases de Tailwind, estructura de páginas). Nada de reescribir lo que funciona.
3. **Rama nueva**, nunca commits directos a `main`. Partí de `deploy-et21-ar`, que es la que está publicada: `git checkout deploy-et21-ar && git checkout -b demo-charla-et21`. Commits chicos y descriptivos, en castellano.
4. **Pedí permiso antes de publicar**: `git push` y `npx wrangler deploy`. Es un momento que se muestra a propósito en la charla, porque el sitio es público y lo ve cualquiera.
5. **Verificá en el navegador**: levantá `npm run dev`, abrí la página, sacá una captura, mirala y corregí. El loop "ver el error y corregirlo" es lo que la audiencia tiene que ver. Probá también a 375 px de ancho.
6. **El build tiene que quedar verde**: `npm run build` y `npx astro check` sin errores antes de decir que terminaste.
7. Todo en **castellano rioplatense**, con voseo.

## Qué construir (elegir una en el momento, con Ezequiel)

Tres opciones que entran en 20 minutos y se ven bien en pantalla. Proponé la que mejor le sirva a la audiencia y confirmá antes de arrancar:

- **A) Página nueva de Taller.** El sitio viejo tiene `/academica/taller/` y el nuevo no. Página `src/pages/taller.astro` con el layout y los bloques que ya existen, más el link en el nav. Es la que mejor muestra "el agente entiende el proyecto y sigue sus patrones".
- **B) Sección de autoridades en institucional.** Usar el componente `AuthorityGrid` que ya está, con los datos reales de `et21.com.ar/institucional/directivos/`.
- **C) Post nuevo en el blog.** Un MDX en `src/content/blog/` sobre la charla o sobre las orientaciones. Es la más rápida; dejala como plan B si el tiempo aprieta.

Contenido: sacalo de **https://et21.com.ar** (WebFetch), que es el sitio viejo de la escuela y sigue siendo la fuente de los textos. No inventes autoridades, horarios ni teléfonos. Si un dato no está, poné `[a completar]` y decilo.

## Publicar

**Camino normal: Cloudflare.** Desde `et21/`, `npx wrangler deploy` compila el sitio y lo publica en https://et21.ar en menos de un minuto. No hace falta tocar `wrangler.jsonc`: los dominios ya están declarados ahí.

Si la API de Cloudflare devuelve un error 500 al asociar el dominio, volvé a correr el comando: pasó una vez el 17/09 y se resolvió en el segundo intento.

Cuando el deploy termine, abrí la URL pública, sacá una captura y mostrala. Eso cierra la demo.

**Alternativa documentada: Coolify.** No se usó, pero el sitio compila a HTML plano y cualquier hosting estático lo sirve. Verificado: todas las rutas responden 200 sirviendo `dist/` con un servidor estático común. Build pack "Static" con `npm ci`, `npm run build` y directorio `dist`, o un `Dockerfile.coolify` multi-stage con nginx. Solo vale la pena si Ezequiel quiere mostrar el servidor de la escuela.

## Si algo falla en vivo

- **El build falla:** leé el error completo, arreglalo y volvé a compilar. Mostralo, no lo escondas: es la parte más útil de la demo.
- **El deploy falla:** reintentá una vez. Si sigue fallando, mostrá el sitio con el dev server y explicá qué haría el deploy. La audiencia ya vio la página funcionando.
- **GitHub no responde:** seguí local y dejá el push para el final.
- **Te quedás sin tiempo:** una página terminada y verificada vale más que tres a medias. Cerrá lo que tengas, dejá el build verde y mostralo.
