# -*- coding: utf-8 -*-
"""
Arma charla/deck.html: una presentacion en un solo archivo que se abre en
cualquier navegador, sin internet y sin instalar nada.

Lee las diapositivas de charla/slides/ y el indice de charla/deck.json.

    python charla/exportar_deck.py
"""

import html
import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(AQUI, "slides")
INDICE = os.path.join(AQUI, "deck.json")
DESTINO = os.path.join(AQUI, "deck.html")


# ----------------------------------------------------------------- iconos
# Los mismos nombres que usan las diapositivas, dibujados como SVG simple.
ICONOS = {
    "Book": '<path d="M4 4h11a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M4 4v14"/>',
    "Tool": '<path d="M15 3a5 5 0 0 0-4.6 7L3 17.4 5.6 20l7.4-7.4A5 5 0 1 0 15 3z"/>',
    "Activity": '<path d="M2 12h4l3 8 4-16 3 8h6"/>',
    "Warning": '<path d="M12 3 2 20h20z"/><path d="M12 9v5"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
    "Lightning": '<path d="M13 2 4 14h6l-1 8 9-12h-6z"/>',
    "Database": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "Lightbulb": '<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z"/>',
    "Lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "Users": '<circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.5a3.2 3.2 0 0 1 0 6"/><path d="M17 14.4a6.5 6.5 0 0 1 4.5 5.6"/>',
}

PLANTILLA = """<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__</title>
__FUENTES__
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; height:100%; background:#0a0d14; overflow:hidden;
               font-family:'IBM Plex Sans', system-ui, sans-serif; }
  /* El lienzo mide 1920x1080 y casi siempre es mas grande que la ventana.
     Centrarlo con grid o flex no sirve: el centrado se calcula ANTES de la
     escala y la diapositiva queda corrida y cortada. Se ancla al centro y se
     corre con translate, que si ocurre junto con la escala. */
  #escenario { position:fixed; inset:0; overflow:hidden; }
  #pista { position:absolute; left:50%; top:50%; width:1920px; height:1080px;
           transform-origin:center center; box-shadow:0 30px 80px rgba(0,0,0,.6); }
  /* cada diapositiva trae su propio display en el atributo style, que le gana
     a una regla normal: por eso el !important */
  section { position:absolute; inset:0; width:1920px; height:1080px; overflow:hidden; }
  section:not(.activa) { display:none !important; }
  /* los bloques con alto propio no deben encogerse: si no, los diagramas
     con coordenadas absolutas quedan comprimidos y se cortan abajo */
  section > * { flex-shrink:0; }
  section aside { display:none; }
  h1,h2,h3,p,ul,ol { margin:0; }
  ul,ol { padding-left:1.3em; }
  li { margin:.15em 0; }
  table { border-collapse:collapse; width:100%; }
  th,td { padding:.35em .6em; text-align:left; border:1px solid rgba(255,255,255,.10); }
  x-icon { display:inline-block; }
  x-icon svg { width:100%; height:100%; display:block; fill:none;
               stroke:currentColor; stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round; }

  /* barra inferior */
  #barra { position:fixed; left:0; right:0; bottom:0; height:44px; display:flex; align-items:center;
           gap:18px; padding:0 18px; background:rgba(10,13,20,.92); color:#8b95a8;
           font-size:13px; border-top:1px solid rgba(255,255,255,.08); z-index:20; }
  #barra button { background:transparent; border:1px solid rgba(255,255,255,.18); color:#c7cedb;
                  border-radius:7px; padding:5px 11px; font-size:13px; cursor:pointer;
                  font-family:inherit; }
  #barra button:hover { background:rgba(255,255,255,.08); }
  #contador { font-variant-numeric:tabular-nums; color:#e6eaf2; }
  #titulo-slide { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

  /* notas del orador */
  #notas { position:fixed; right:0; top:0; bottom:44px; width:420px; background:#12161f;
           border-left:1px solid rgba(255,255,255,.10); padding:26px 28px; overflow:auto;
           color:#c7cedb; font-size:15px; line-height:1.6; display:none; z-index:19; }
  #notas.visible { display:block; }
  #notas h4 { margin:0 0 14px; font-size:12px; letter-spacing:2px; text-transform:uppercase;
              color:#f5b942; font-weight:600; }
  body.con-notas #escenario { right:420px; }

  @media print { #barra, #notas { display:none !important; } }
</style>
</head>
<body>
<div id="escenario"><div id="pista">
__SLIDES__
</div></div>

<div id="notas"><h4>Notas del orador</h4><div id="notas-texto"></div></div>

<div id="barra">
  <span id="contador">1 / __TOTAL__</span>
  <span id="titulo-slide"></span>
  <button id="btn-anterior">&larr;</button>
  <button id="btn-siguiente">&rarr;</button>
  <button id="btn-notas">Notas (N)</button>
  <button id="btn-pantalla">Pantalla completa (F)</button>
</div>

<script>
(function () {
  const ICONOS = __ICONOS__;
  const NOTAS = __NOTAS__;
  const TITULOS = __TITULOS__;

  // ---- iconos
  document.querySelectorAll('x-icon').forEach(function (el) {
    const d = ICONOS[el.getAttribute('name')] || '<circle cx="12" cy="12" r="9"/>';
    el.innerHTML = '<svg viewBox="0 0 24 24">' + d + '</svg>';
  });

  // ---- conectores
  function num(el, attr) { const v = el.getAttribute(attr); return v === null ? null : parseFloat(v); }

  function puntos(x1, y1, x2, y2, ruta) {
    if (ruta === 'hv') return [[x1, y1], [x2, y1], [x2, y2]];
    if (ruta === 'vh') return [[x1, y1], [x1, y2], [x2, y2]];
    if (ruta === 'elbow') {
      return Math.abs(x2 - x1) >= Math.abs(y2 - y1)
        ? [[x1, y1], [(x1 + x2) / 2, y1], [(x1 + x2) / 2, y2], [x2, y2]]
        : [[x1, y1], [x1, (y1 + y2) / 2], [x2, (y1 + y2) / 2], [x2, y2]];
    }
    return [[x1, y1], [x2, y2]];
  }

  function flecha(pa, pb, grosor) {
    const dx = pb[0] - pa[0], dy = pb[1] - pa[1];
    const L = Math.hypot(dx, dy) || 1;
    const ux = dx / L, uy = dy / L, t = grosor * 3.4;
    const bx = pb[0] - ux * t, by = pb[1] - uy * t;
    const px = -uy * t * 0.52, py = ux * t * 0.52;
    return (bx + px) + ',' + (by + py) + ' ' + pb[0] + ',' + pb[1] + ' ' + (bx - px) + ',' + (by - py);
  }

  function dibujarConector(el) {
    const est = getComputedStyle(el);
    const color = est.color || '#888';
    const grosor = parseFloat(est.borderTopWidth) || 2;
    const guion = est.borderTopStyle === 'dashed' ? '10 8'
                : est.borderTopStyle === 'dotted' ? '2 6' : '';
    const cabeza = el.getAttribute('head') || 'end';
    const x1 = num(el, 'x1');

    if (x1 !== null) {                       // conector con coordenadas
      const padre = el.parentElement;
      if (getComputedStyle(padre).position === 'static') padre.style.position = 'relative';
      const W = padre.clientWidth, H = padre.clientHeight;
      const ps = puntos(x1, num(el, 'y1'), num(el, 'x2'), num(el, 'y2'),
                        el.getAttribute('route') || 'straight');
      let svg = '<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" '
              + 'style="position:absolute;left:0;top:0;overflow:visible;pointer-events:none">'
              + '<polyline points="' + ps.map(function (p) { return p.join(','); }).join(' ') + '" '
              + 'fill="none" stroke="' + color + '" stroke-width="' + grosor + '" '
              + 'stroke-linecap="round" stroke-linejoin="round"'
              + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '/>';
      if (cabeza === 'end' || cabeza === 'both') {
        svg += '<polygon points="' + flecha(ps[ps.length - 2], ps[ps.length - 1], grosor) + '" fill="' + color + '"/>';
      }
      if (cabeza === 'both') {
        svg += '<polygon points="' + flecha(ps[1], ps[0], grosor) + '" fill="' + color + '"/>';
      }
      el.style.position = 'absolute';
      el.style.left = '0'; el.style.top = '0';
      el.innerHTML = svg + '</svg>';
    } else {                                 // conector suelto, dentro de una fila
      const W = parseFloat(est.width) || 48, H = Math.max(grosor * 5, 20);
      el.style.display = 'inline-block';
      el.style.height = H + 'px';
      el.style.flex = '0 0 ' + W + 'px';
      const fin = [W, H / 2], ini = [0, H / 2];
      el.innerHTML = '<svg width="' + W + '" height="' + H + '" style="overflow:visible;display:block">'
        + '<line x1="0" y1="' + H / 2 + '" x2="' + (W - grosor * 3) + '" y2="' + H / 2 + '" '
        + 'stroke="' + color + '" stroke-width="' + grosor + '" stroke-linecap="round"/>'
        + (cabeza === 'none' ? '' : '<polygon points="' + flecha(ini, fin, grosor) + '" fill="' + color + '"/>')
        + '</svg>';
    }
  }

  // ---- preparar cada diapositiva
  // Los conectores se dibujan con la diapositiva VISIBLE: si esta en display:none
  // su contenedor mide cero y las lineas salen de tamano cero.
  // Despues se achica el bloque de diagrama si la diapositiva pasa de 1080, con
  // transform, para que los conectores ya dibujados escalen junto con las cajas.
  document.querySelectorAll('#pista > section').forEach(function (s) {
    s.classList.add('activa');
    s.querySelectorAll('x-connector').forEach(dibujarConector);
    const exceso = s.scrollHeight - 1080;
    if (exceso > 1) {
      const bloques = Array.from(s.children).filter(function (el) {
        return el.tagName === 'DIV' && parseFloat(getComputedStyle(el).height) > 200;
      });
      const host = bloques.sort(function (a, b) { return b.offsetHeight - a.offsetHeight; })[0];
      if (host) {
        const alto = host.offsetHeight;
        const k = Math.max(0.5, (alto - exceso) / alto);
        host.style.transformOrigin = 'top center';
        host.style.transform = 'scale(' + k + ')';
        host.style.marginBottom = (-(alto - alto * k)) + 'px';
      }
    }
    s.classList.remove('activa');
  });

  // ---- navegacion
  const slides = Array.from(document.querySelectorAll('#pista > section'));
  const pista = document.getElementById('pista');
  const contador = document.getElementById('contador');
  const tituloSlide = document.getElementById('titulo-slide');
  const notas = document.getElementById('notas');
  const notasTexto = document.getElementById('notas-texto');
  let actual = 0;

  function mostrar(i) {
    actual = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (s, n) { s.classList.toggle('activa', n === actual); });
    contador.textContent = (actual + 1) + ' / ' + slides.length;
    tituloSlide.textContent = TITULOS[actual] || '';
    notasTexto.textContent = NOTAS[actual] || 'Esta diapositiva no tiene notas.';
    location.hash = String(actual + 1);
    encajar();
  }

  function encajar() {
    const esc = document.getElementById('escenario').getBoundingClientRect();
    const k = Math.min(esc.width / 1920, esc.height / 1080) * 0.98;
    pista.style.transform = 'translate(-50%, -50%) scale(' + k + ')';
  }

  document.getElementById('btn-siguiente').onclick = function () { mostrar(actual + 1); };
  document.getElementById('btn-anterior').onclick = function () { mostrar(actual - 1); };
  document.getElementById('btn-notas').onclick = function () {
    notas.classList.toggle('visible');
    document.body.classList.toggle('con-notas');
    encajar();
  };
  document.getElementById('btn-pantalla').onclick = function () {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen();
  };

  document.addEventListener('keydown', function (e) {
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].indexOf(e.key) >= 0) { mostrar(actual + 1); e.preventDefault(); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].indexOf(e.key) >= 0) { mostrar(actual - 1); e.preventDefault(); }
    else if (e.key === 'Home') mostrar(0);
    else if (e.key === 'End') mostrar(slides.length - 1);
    else if (e.key === 'n' || e.key === 'N') document.getElementById('btn-notas').click();
    else if (e.key === 'f' || e.key === 'F') document.getElementById('btn-pantalla').click();
  });

  window.addEventListener('resize', encajar);
  const inicio = parseInt(location.hash.replace('#', ''), 10);
  mostrar(isNaN(inicio) ? 0 : inicio - 1);
})();
</script>
</body>
</html>
"""


def main():
    indice = json.load(io.open(INDICE, encoding="utf-8"))
    partes, notas, titulos = [], [], []

    for sid in indice["order"]:
        ruta = os.path.join(SLIDES, sid + ".html")
        if not os.path.exists(ruta):
            print("  falta la diapositiva:", sid)
            continue
        s = io.open(ruta, encoding="utf-8").read().strip()

        m = re.search(r"<aside>(.*?)</aside>", s, re.S)
        notas.append(re.sub(r"\s+", " ", m.group(1)).strip() if m else "")
        s = re.sub(r"<aside>.*?</aside>", "", s, flags=re.S)

        t = re.search(r"<h[12][^>]*>(.*?)</h[12]>", s, re.S)
        titulos.append(re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else sid)

        partes.append(s)

    fuentes = "\n".join(
        '<link rel="stylesheet" href="%s">' % html.escape(f["href"])
        for f in indice.get("faces", {}).values() if f.get("href")
    )

    salida = (PLANTILLA
              .replace("__TITULO__", html.escape(indice.get("title", "Presentación")))
              .replace("__FUENTES__", fuentes)
              .replace("__SLIDES__", "\n".join(partes))
              .replace("__TOTAL__", str(len(partes)))
              .replace("__ICONOS__", json.dumps(ICONOS, ensure_ascii=False))
              .replace("__NOTAS__", json.dumps(notas, ensure_ascii=False))
              .replace("__TITULOS__", json.dumps(titulos, ensure_ascii=False)))

    io.open(DESTINO, "w", encoding="utf-8").write(salida)
    print("%d diapositivas -> %s (%.0f KB)"
          % (len(partes), DESTINO, os.path.getsize(DESTINO) / 1024))


if __name__ == "__main__":
    main()
