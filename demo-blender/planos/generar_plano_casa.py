# -*- coding: utf-8 -*-
"""
Genera el plano de una casa de 3 ambientes en duplex, lote de 100 m2 de barrio cerrado.
Dibuja dos laminas PNG: una tecnica con cotas (para leer y modelar) y una presentable
con mobiliario.

Todas las medidas estan en metros. El origen (0,0) es la esquina exterior
suroeste de la casa; X crece al este, Y crece al norte (hacia el fondo).
"""

from PIL import Image, ImageDraw, ImageFont
import os

from casa_datos import (
    LOTE_ANCHO, LOTE_FONDO, RETIRO_FRENTE, CASA_ANCHO, CASA_FONDO, PATIO_FONDO,
    MURO_EXT, MURO_INT, ALTURA_LIBRE, NIVEL_PA,
    MUROS_EXT, MUROS_PB, MUROS_PA,
    ABERTURAS_PB, ABERTURAS_PA, AMB_PB, AMB_PA,
    ESC_X0, ESC_X1, ESC_Y0, ESC_Y1,
)

PX = 118          # pixeles por metro
SALIDA = os.path.dirname(os.path.abspath(__file__))

TINTA = (28, 32, 40)
MURO = (38, 42, 52)
GRIS = (122, 130, 142)
GRIS_CLARO = (196, 202, 210)
COTA = (58, 92, 150)
FONDO = (255, 255, 255)
PISO = (247, 246, 242)
MUEBLE = (150, 158, 170)
VERDE = (206, 222, 198)

# La tipografia se busca en Windows, macOS y Linux, en ese orden.
CANDIDATAS = [
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf",
     "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Helvetica.ttc"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
]

F = FB = None
for normal, negrita in CANDIDATAS:
    if os.path.exists(normal) and os.path.exists(negrita):
        F, FB = normal, negrita
        break
if F is None:
    raise SystemExit(
        "No se encontro una tipografia. Edita CANDIDATAS en este archivo y "
        "agrega la ruta de una fuente TrueType de tu sistema."
    )


def fuente(tam, negrita=False):
    return ImageFont.truetype(FB if negrita else F, tam)


class Lienzo:
    """Traduce metros a pixeles y dibuja. El origen esta abajo a la izquierda."""

    def __init__(self, ancho_px, alto_px):
        self.img = Image.new("RGB", (ancho_px, alto_px), FONDO)
        self.d = ImageDraw.Draw(self.img)
        self.ox = 0
        self.oy = 0

    def origen(self, x_px, y_px):
        self.ox, self.oy = x_px, y_px

    def p(self, x, y):
        return (self.ox + x * PX, self.oy - y * PX)

    def rect(self, x0, y0, x1, y1, relleno=None, borde=None, ancho=1):
        a = self.p(x0, y1)
        b = self.p(x1, y0)
        self.d.rectangle([a, b], fill=relleno, outline=borde, width=ancho)

    def linea(self, x0, y0, x1, y1, color=TINTA, ancho=2):
        self.d.line([self.p(x0, y0), self.p(x1, y1)], fill=color, width=ancho)

    def arco(self, cx, cy, r, ini, fin, color=GRIS, ancho=2):
        caja = [self.p(cx - r, cy + r), self.p(cx + r, cy - r)]
        self.d.arc(caja, ini, fin, fill=color, width=ancho)

    def texto(self, x, y, txt, fnt, color=TINTA, centro=True, medio=True):
        px, py = self.p(x, y)
        anc = "mm" if (centro and medio) else ("ma" if centro else "lm")
        self.d.text((px, py), txt, font=fnt, fill=color, anchor=anc)

    def texto_px(self, px, py, txt, fnt, color=TINTA, anchor="mm"):
        self.d.text((px, py), txt, font=fnt, fill=color, anchor=anchor)


def dibujar_planta(L, muros_int, aberturas, ambientes, con_escalera, mobiliario=False, sube=True):
    # piso
    L.rect(MURO_EXT, MURO_EXT, CASA_ANCHO - MURO_EXT, CASA_FONDO - MURO_EXT, relleno=PISO)

    # muros llenos
    for x0, y0, x1, y1 in MUROS_EXT + muros_int:
        L.rect(x0, y0, x1, y1, relleno=MURO)

    # aberturas: se vacia el muro y se dibuja el simbolo
    for x0, y0, x1, y1, tipo, giro, ref, alto, antep, desc in aberturas:
        L.rect(x0, y0, x1, y1, relleno=FONDO)
        horizontal = (x1 - x0) > (y1 - y0)
        luz = (x1 - x0) if horizontal else (y1 - y0)

        if tipo == "ventana":
            if horizontal:
                ym = (y0 + y1) / 2
                L.linea(x0, y0, x1, y0, TINTA, 2)
                L.linea(x0, y1, x1, y1, TINTA, 2)
                L.linea(x0, ym, x1, ym, GRIS, 2)
            else:
                xm = (x0 + x1) / 2
                L.linea(x0, y0, x0, y1, TINTA, 2)
                L.linea(x1, y0, x1, y1, TINTA, 2)
                L.linea(xm, y0, xm, y1, GRIS, 2)

        elif tipo == "corrediza":
            ym = (y0 + y1) / 2
            L.linea(x0, y0, x1, y0, TINTA, 2)
            L.linea(x0, y1, x1, y1, TINTA, 2)
            L.linea(x0, ym, x0 + luz * 0.55, ym, TINTA, 4)
            L.linea(x1 - luz * 0.55, ym - 0.04, x1, ym - 0.04, TINTA, 4)

        elif tipo == "puerta":
            if horizontal:
                ym = (y0 + y1) / 2
                if giro == "N":
                    L.linea(x0, ym, x0, ym + luz, TINTA, 3)
                    L.arco(x0, ym, luz, 270, 360)
                else:
                    L.linea(x1, ym, x1, ym - luz, TINTA, 3)
                    L.arco(x1, ym, luz, 90, 180)
            else:
                xm = (x0 + x1) / 2
                if giro == "E":
                    L.linea(xm, y0, xm + luz, y0, TINTA, 3)
                    L.arco(xm, y0, luz, 270, 360)
                else:
                    L.linea(xm, y1, xm - luz, y1, TINTA, 3)
                    L.arco(xm, y1, luz, 90, 180)

        elif tipo == "vano":
            pass

        # marca de referencia, corrida hacia afuera del muro
        if ref:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            if horizontal:
                # en el muro del frente la marca va hacia adentro: afuera se
                # superpone con la cadena de cotas
                en_frente = y0 < 0.01
                fuera = 0.48 if en_frente else (-0.40 if my < CASA_FONDO / 2 else 0.40)
                rx, ry = mx, my + fuera
            else:
                fuera = -0.40 if mx < CASA_ANCHO / 2 else 0.40
                rx, ry = mx + fuera, my
            cxp, cyp = L.p(rx, ry)
            r = 21
            L.d.ellipse([cxp - r, cyp - r, cxp + r, cyp + r], fill=FONDO, outline=COTA, width=2)
            L.d.text((cxp, cyp), ref, font=fuente(17, True), fill=COTA, anchor="mm")

    if con_escalera:
        dibujar_escalera(L, sube)

    if mobiliario:
        dibujar_mobiliario(L, con_escalera)

    # rotulos de ambiente
    for nombre, x0, y0, x1, y1, rx, ry in ambientes:
        cx = rx if rx is not None else (x0 + x1) / 2
        cy = ry if ry is not None else (y0 + y1) / 2
        anc, prof = x1 - x0, y1 - y0
        area = anc * prof
        if nombre == "PASO":
            L.texto(cx, cy + 0.11, nombre, fuente(21, True), TINTA)
            L.texto(cx, cy - 0.20, f"{area:.2f} m2".replace(".", ","), fuente(18), GRIS)
        elif area < 4.0:                       # ambiente chico: tipografia menor
            L.texto(cx, cy + 0.26, nombre, fuente(19, True), TINTA)
            L.texto(cx, cy + 0.02, f"{anc:.2f} x {prof:.2f}".replace(".", ","), fuente(17), GRIS)
            L.texto(cx, cy - 0.22, f"{area:.2f} m2".replace(".", ","), fuente(17), GRIS)
        else:
            L.texto(cx, cy + 0.30, nombre, fuente(25, True), TINTA)
            L.texto(cx, cy, f"{anc:.2f} x {prof:.2f}".replace(".", ","), fuente(21), GRIS)
            L.texto(cx, cy - 0.30, f"{area:.2f} m2".replace(".", ","), fuente(21), GRIS)


def dibujar_escalera(L, sube=True):
    pedadas = 7
    ancho_tramo = (ESC_X1 - ESC_X0 - MURO_INT) / 2      # 1.00
    largo = pedadas * 0.26                               # 1.82
    # tramo de subida, contra la medianera este
    x0 = ESC_X0 + ancho_tramo + MURO_INT
    for i in range(pedadas + 1):
        y = ESC_Y0 + i * 0.26
        L.linea(x0, y, ESC_X1, y, GRIS, 2)
    # descanso
    L.rect(ESC_X0, ESC_Y0 + largo, ESC_X1, ESC_Y1, relleno=None, borde=GRIS_CLARO, ancho=2)
    # tramo de bajada
    for i in range(pedadas + 1):
        y = ESC_Y0 + i * 0.26
        L.linea(ESC_X0, y, ESC_X0 + ancho_tramo, y, GRIS, 2)
    # linea de eje con flecha de subida
    ejex = ESC_X0 + ancho_tramo + MURO_INT + ancho_tramo / 2
    L.linea(ejex, ESC_Y0 + 0.15, ejex, ESC_Y0 + largo + 0.55, TINTA, 2)
    L.linea(ejex, ESC_Y0 + largo + 0.55, ejex - 0.12, ESC_Y0 + largo + 0.35, TINTA, 2)
    L.linea(ejex, ESC_Y0 + largo + 0.55, ejex + 0.12, ESC_Y0 + largo + 0.35, TINTA, 2)
    L.texto(ESC_X0 + ancho_tramo / 2, ESC_Y0 + 0.95, "SUBE" if sube else "BAJA", fuente(17, True), GRIS)
    L.texto((ESC_X0 + ESC_X1) / 2, ESC_Y1 - 0.42, "16 alz. 0,175", fuente(16), GRIS)


def dibujar_mobiliario(L, es_pb):
    g = (138, 148, 164)
    if es_pb:
        # estar: sofa y mesa
        L.rect(0.45, 0.45, 2.55, 1.30, borde=g, ancho=3)
        L.rect(0.95, 1.60, 2.05, 2.30, borde=g, ancho=3)
        L.rect(2.90, 1.90, 4.35, 3.25, borde=g, ancho=3)      # mesa comedor
        # cocina: mesada en L
        L.rect(0.20, 5.20, 3.20, 5.80, relleno=None, borde=g, ancho=3)
        L.rect(0.20, 3.60, 0.85, 5.20, relleno=None, borde=g, ancho=3)
        L.rect(1.60, 5.20, 2.20, 5.80, borde=g, ancho=3)      # bacha
        # toilette
        L.rect(6.35, 1.95, 6.85, 2.60, borde=g, ancho=3)
        L.rect(7.20, 2.55, 7.70, 2.95, borde=g, ancho=3)
    else:
        # dormitorio 1: cama de dos plazas
        L.rect(1.20, 1.55, 2.80, 3.35, borde=g, ancho=3)
        L.rect(0.30, 0.30, 4.10, 0.90, borde=g, ancho=3)      # placard
        # dormitorio 2: cama de una plaza
        L.rect(4.45, 1.60, 5.35, 3.00, borde=g, ancho=3)
        L.rect(6.60, 0.30, 7.70, 3.00, borde=g, ancho=3)      # placard
        # bano
        L.rect(0.30, 4.55, 1.05, 5.70, borde=g, ancho=3)      # banera
        L.rect(1.60, 5.25, 2.15, 5.70, borde=g, ancho=3)      # lavatorio
        L.rect(2.00, 3.65, 2.50, 4.30, borde=g, ancho=3)      # inodoro


def cadena_cotas(L, tramos, base, vertical=False, offset=0.55, fnt=None, marcar_total=True):
    """Dibuja una cadena de cotas. tramos = [(inicio, fin, etiqueta), ...]"""
    fnt = fnt or fuente(20, True)
    for ini, fin, etq in tramos:
        if vertical:
            x = base + offset
            L.linea(x, ini, x, fin, COTA, 2)
            for y in (ini, fin):
                L.linea(x - 0.07, y, x + 0.07, y, COTA, 2)
                L.linea(base, y, x, y, GRIS_CLARO, 1)
            px, py = L.p(x - 0.13, (ini + fin) / 2)
            txt = Image.new("RGBA", (190, 34), (0, 0, 0, 0))
            ImageDraw.Draw(txt).text((95, 17), etq, font=fnt, fill=COTA, anchor="mm")
            txt = txt.rotate(90, expand=True)
            L.img.paste(txt, (int(px - txt.width / 2), int(py - txt.height / 2)), txt)
        else:
            y = base - offset
            L.linea(ini, y, fin, y, COTA, 2)
            for x in (ini, fin):
                L.linea(x, y - 0.07, x, y + 0.07, COTA, 2)
                L.linea(x, base, x, y, GRIS_CLARO, 1)
            L.texto((ini + fin) / 2, y + 0.16, etq, fnt, COTA)


def lamina_tecnica():
    W, H = 3100, 2780
    L = Lienzo(W, H)
    d = L.d

    # ---------------- rotulo
    d.rectangle([0, 0, W, 108], fill=(244, 245, 247))
    d.line([(0, 108), (W, 108)], fill=GRIS_CLARO, width=2)
    L.texto_px(56, 44, "CASA DE 3 AMBIENTES EN DUPLEX", fuente(34, True), TINTA, "lm")
    L.texto_px(56, 80, "Barrio cerrado  ·  lote de 8,00 x 12,50 m = 100,00 m2", fuente(23), GRIS, "lm")
    L.texto_px(W - 56, 44, "PLANTAS  ·  VER ESCALA GRAFICA", fuente(28, True), TINTA, "rm")
    L.texto_px(W - 56, 80, "Medidas en metros  ·  cotas exteriores a filo de muro", fuente(21), GRIS, "rm")

    BASE = 1140          # linea de nivel 0,00 de las dos plantas

    # ---------------- planta baja
    L.origen(360, BASE)
    L.texto_px(360, 212, "PLANTA BAJA", fuente(32, True), TINTA, "lm")
    L.texto_px(360, 252, "nivel +0,00   ·   superficie cubierta 48,00 m2", fuente(21), GRIS, "lm")
    dibujar_planta(L, MUROS_PB, ABERTURAS_PB, AMB_PB, con_escalera=True)

    cadena_cotas(L, [(0.00, 4.60, "4,60"), (4.60, 6.10, "1,50"), (6.10, 8.00, "1,90")], 0.00)
    cadena_cotas(L, [(0.00, 8.00, "8,00")], 0.00, offset=1.15, fnt=fuente(24, True))
    cadena_cotas(L, [(0.00, 3.50, "3,50"), (3.50, 6.00, "2,50")], 0.00, vertical=True, offset=-0.55, fnt=fuente(23, True))
    cadena_cotas(L, [(0.00, 6.00, "6,00")], 0.00, vertical=True, offset=-1.15, fnt=fuente(27, True))
    cadena_cotas(L, [(0.00, 1.70, "1,70"), (1.70, 3.10, "1,40"), (3.10, 6.00, "2,90")],
                 8.00, vertical=True, offset=0.55, fnt=fuente(23, True))

    # ---------------- planta alta
    L.origen(1760, BASE)
    L.texto_px(1760, 212, "PLANTA ALTA", fuente(32, True), TINTA, "lm")
    L.texto_px(1760, 252, "nivel +2,80   ·   superficie cubierta 48,00 m2", fuente(21), GRIS, "lm")
    dibujar_planta(L, MUROS_PA, ABERTURAS_PA, AMB_PA, con_escalera=True, sube=False)

    cadena_cotas(L, [(0.00, 4.20, "4,20"), (4.20, 8.00, "3,80")], 0.00)
    cadena_cotas(L, [(0.00, 8.00, "8,00")], 0.00, offset=1.15, fnt=fuente(24, True))
    cadena_cotas(L, [(0.00, 3.40, "3,40"), (3.40, 6.00, "2,60")], 0.00, vertical=True, offset=-0.55, fnt=fuente(23, True))
    cadena_cotas(L, [(0.00, 6.00, "6,00")], 0.00, vertical=True, offset=-1.15, fnt=fuente(27, True))
    cadena_cotas(L, [(0.00, 3.10, "3,10"), (3.10, 6.00, "2,90")],
                 8.00, vertical=True, offset=0.55, fnt=fuente(23, True))

    # ---------------- implantacion, abajo a la derecha y sin pisar las plantas
    L.origen(2530, 2700)
    esc = 0.40
    px_guardado = globals()["PX"]
    globals()["PX"] = int(px_guardado * esc)
    L.texto_px(2530, 2060, "IMPLANTACION", fuente(26, True), TINTA, "lm")
    L.rect(0, 0, LOTE_ANCHO, LOTE_FONDO, relleno=VERDE, borde=TINTA, ancho=3)
    L.rect(0, RETIRO_FRENTE, LOTE_ANCHO, RETIRO_FRENTE + CASA_FONDO, relleno=(228, 228, 224), borde=MURO, ancho=4)
    L.texto(LOTE_ANCHO / 2, RETIRO_FRENTE + CASA_FONDO / 2, "CASA", fuente(19, True), TINTA)
    L.texto(LOTE_ANCHO / 2, RETIRO_FRENTE / 2 + 0.25, "RETIRO", fuente(15), (90, 110, 86))
    L.texto(LOTE_ANCHO / 2, RETIRO_FRENTE / 2 - 0.35, "3,00", fuente(15), (90, 110, 86))
    L.texto(LOTE_ANCHO / 2, RETIRO_FRENTE + CASA_FONDO + PATIO_FONDO / 2 + 0.25, "PATIO", fuente(15), (90, 110, 86))
    L.texto(LOTE_ANCHO / 2, RETIRO_FRENTE + CASA_FONDO + PATIO_FONDO / 2 - 0.35, "3,50", fuente(15), (90, 110, 86))
    cadena_cotas(L, [(0.00, LOTE_ANCHO, "8,00")], 0.00, offset=0.75, fnt=fuente(19, True))
    cadena_cotas(L, [(0.00, LOTE_FONDO, "12,50")], LOTE_ANCHO, vertical=True, offset=0.75, fnt=fuente(19, True))
    globals()["PX"] = px_guardado

    # ---------------- cuadro de superficies
    x0, y0 = 360, 1500
    ESC_AREA = (ESC_X1 - ESC_X0) * (ESC_Y1 - ESC_Y0)

    def filas_de(ambientes, titulo):
        out = [(titulo, "", "")]
        for nombre, ax0, ay0, ax1, ay1, _, _ in ambientes:
            anc, prof = ax1 - ax0, ay1 - ay0
            med = "" if nombre == "PASO" else f"{anc:.2f} x {prof:.2f}".replace(".", ",")
            out.append((nombre.capitalize(), med, f"{anc * prof:.2f}".replace(".", ",")))
        out.append(("Escalera", f"{ESC_X1 - ESC_X0:.2f} x {ESC_Y1 - ESC_Y0:.2f}".replace(".", ","),
                    f"{ESC_AREA:.2f}".replace(".", ",")))
        return out

    filas = filas_de(AMB_PB, "PLANTA BAJA") + filas_de(AMB_PA, "PLANTA ALTA")
    d.text((x0, y0 - 42), "SUPERFICIES", font=fuente(26, True), fill=TINTA)
    yy = y0
    for nombre, med, area in filas:
        es_titulo = area == ""
        fnt = fuente(21, True) if es_titulo else fuente(20)
        col = TINTA if es_titulo else (70, 76, 88)
        if es_titulo:
            yy += 12
            d.line([(x0, yy - 8), (x0 + 660, yy - 8)], fill=GRIS_CLARO, width=2)
        d.text((x0, yy), nombre, font=fnt, fill=col)
        if not es_titulo:
            d.text((x0 + 380, yy), med, font=fnt, fill=GRIS)
            d.text((x0 + 660, yy), area, font=fnt, fill=col, anchor="ra")
        yy += 34

    # totales
    yy += 14
    d.line([(x0, yy - 8), (x0 + 660, yy - 8)], fill=TINTA, width=3)
    for etq, val in [("Cubierta total", "96,00 m2"), ("Patio", "28,00 m2"), ("Retiro de frente", "24,00 m2")]:
        d.text((x0, yy), etq, font=fuente(21, True), fill=TINTA)
        d.text((x0 + 660, yy), val, font=fuente(21, True), fill=TINTA, anchor="ra")
        yy += 34

    # ---------------- datos de obra
    x1 = 1150
    d.text((x1, y0 - 42), "DATOS DE OBRA", font=fuente(26, True), fill=TINTA)
    datos = [
        ("Muros exteriores y medianeras", "0,20 m"),
        ("Tabiques interiores", "0,10 m"),
        ("Altura libre por planta", "2,60 m"),
        ("Nivel de planta alta", "+2,80 m"),
        ("Espesor de losa", "0,20 m"),
        ("Altura total de la casa", "5,60 m"),
        ("Puertas interiores", "0,80 x 2,00 m"),
        ("Puerta de toilette y baño", "0,70 x 2,00 m"),
        ("Puerta de entrada", "0,90 x 2,10 m"),
        ("Ventanas, antepecho", "0,90 m"),
        ("Ventanas, altura de hoja", "1,50 m"),
        ("Puerta ventana al patio", "1,60 x 2,10 m"),
    ]
    yy = y0
    for etq, val in datos:
        d.text((x1, yy), etq, font=fuente(20), fill=(70, 76, 88))
        d.text((x1 + 560, yy), val, font=fuente(20, True), fill=TINTA, anchor="ra")
        yy += 34

    # ---------------- planilla de carpinterias, generada de la geometria
    x2 = 1900
    d.text((x2, y0 - 42), "PLANILLA DE CARPINTERIAS", font=fuente(26, True), fill=TINTA)
    enc = [("Ref", 0), ("Abertura", 78), ("Ancho x alto", 470), ("Antep.", 700), ("Ubicacion", 820)]
    yy = y0
    for etq, dx in enc:
        d.text((x2 + dx, yy), etq, font=fuente(19, True), fill=GRIS)
    yy += 30
    d.line([(x2, yy - 6), (x2 + 1140, yy - 6)], fill=TINTA, width=2)
    yy += 8

    for planta, lista in (("PB", ABERTURAS_PB), ("PA", ABERTURAS_PA)):
        for ax0, ay0, ax1, ay1, tipo, giro, ref, alto, antep, desc in lista:
            horizontal = (ax1 - ax0) > (ay1 - ay0)
            luz = (ax1 - ax0) if horizontal else (ay1 - ay0)
            if horizontal:
                ubic = f"muro y={ay0:.2f}, x desde {ax0:.2f}"
            else:
                ubic = f"muro x={ax0:.2f}, y desde {ay0:.2f}"
            fila = [
                (f"{ref}", 0),
                (f"{desc} ({planta})", 78),
                (f"{luz:.2f} x {alto:.2f}", 470),
                (f"{antep:.2f}" if antep else "-", 700),
                (ubic, 820),
            ]
            for txt, dx in fila:
                negr = dx == 0
                d.text((x2 + dx, yy), txt.replace(".", ","), font=fuente(19, negr),
                       fill=COTA if negr else (70, 76, 88))
            yy += 31

    d.text((x2, yy + 12), "Ancho = luz libre.  Ubicacion referida al origen en la esquina exterior suroeste.",
           font=fuente(18), fill=GRIS)

    # ---------------- corte esquematico con las alturas
    cx0, cy0 = 420, 2700           # esquina inferior izquierda del corte, en pixeles
    esc_c = 58                      # pixeles por metro del corte
    d.text((cx0 - 50, cy0 - 400), "CORTE A - A", font=fuente(26, True), fill=TINTA)

    def cp(x, z):
        return (cx0 + x * esc_c, cy0 - z * esc_c)

    LOSA = 0.20
    # terreno
    d.line([cp(-0.6, 0), cp(8.6, 0)], fill=TINTA, width=3)
    # muros de las dos plantas
    for x in (0.00, 7.80):
        d.rectangle([cp(x, 5.60), cp(x + 0.20, 0)], fill=MURO)
    # losa de planta alta y losa de techo
    d.rectangle([cp(0, 2.80), cp(8.00, 2.60)], fill=MURO)
    d.rectangle([cp(0, 5.60), cp(8.00, 5.40)], fill=MURO)
    # pisos
    d.rectangle([cp(0.20, 2.60), cp(7.80, 0)], fill=None, outline=GRIS_CLARO, width=2)
    d.rectangle([cp(0.20, 5.40), cp(7.80, 2.80)], fill=None, outline=GRIS_CLARO, width=2)
    d.text(cp(4.0, 1.30), "PLANTA BAJA", font=fuente(20, True), fill=GRIS, anchor="mm")
    d.text(cp(4.0, 4.10), "PLANTA ALTA", font=fuente(20, True), fill=GRIS, anchor="mm")
    d.text(cp(4.0, 0.95), "altura libre 2,60", font=fuente(17), fill=GRIS, anchor="mm")
    d.text(cp(4.0, 3.75), "altura libre 2,60", font=fuente(17), fill=GRIS, anchor="mm")

    # cotas de nivel a la derecha
    for z, etq in [(0.00, "+0,00  piso planta baja"),
                   (2.60, "+2,60  cielorraso"),
                   (2.80, "+2,80  piso planta alta"),
                   (5.40, "+5,40  cielorraso"),
                   (5.60, "+5,60  nivel de techo")]:
        x0p, y0p = cp(8.00, z)
        d.line([(x0p, y0p), (x0p + 46, y0p)], fill=COTA, width=2)
        d.polygon([(x0p + 46, y0p), (x0p + 60, y0p - 7), (x0p + 60, y0p + 7)], fill=COTA)
        d.text((x0p + 70, y0p), etq, font=fuente(19, True), fill=COTA, anchor="lm")

    # ---------------- escala grafica: DEBE coincidir con el dibujo de las plantas
    ex, ey = 1460, 2450
    d.text((ex, ey - 48), "ESCALA GRAFICA", font=fuente(20, True), fill=TINTA)
    upp = PX          # mismos pixeles por metro que las plantas
    for i in range(3):
        color = TINTA if i % 2 == 0 else FONDO
        d.rectangle([ex + i * upp, ey, ex + (i + 1) * upp, ey + 24], fill=color, outline=TINTA, width=2)
    for i, val in enumerate(["0", "1", "2", "3 m"]):
        d.text((ex + i * upp, ey + 46), val, font=fuente(19), fill=TINTA, anchor="ma")

    nx, ny = 1510, 2610
    d.ellipse([nx - 42, ny - 42, nx + 42, ny + 42], outline=TINTA, width=3)
    d.polygon([(nx, ny - 34), (nx - 14, ny + 15), (nx, ny + 4), (nx + 14, ny + 15)], fill=TINTA)
    d.text((nx + 68, ny), "NORTE  ·  el frente da al sur", font=fuente(21), fill=GRIS, anchor="lm")

    d.text((56, H - 38), "Dibujo generado para la charla de la ET21 del 18/09/2026.  Cotas exteriores a filo de muro.",
           font=fuente(19), fill=GRIS)

    ruta = os.path.join(SALIDA, "casa-3-ambientes-plano.png")
    L.img.save(ruta)
    return ruta


def lamina_presentacion():
    W, H = 3100, 1340
    L = Lienzo(W, H)
    d = L.d

    d.rectangle([0, 0, W, 108], fill=(30, 42, 58))
    L.texto_px(56, 44, "CASA DE 3 AMBIENTES EN DUPLEX", fuente(34, True), (250, 250, 248), "lm")
    L.texto_px(56, 80, "Barrio cerrado  ·  100 m2 de lote  ·  96 m2 cubiertos", fuente(23), (168, 186, 204), "lm")
    L.texto_px(W - 56, 62, "ANTEPROYECTO", fuente(28, True), (212, 160, 23), "rm")

    L.origen(360, 1120)
    L.texto_px(360, 250, "PLANTA BAJA", fuente(32, True), TINTA, "lm")
    L.texto_px(360, 290, "Estar-comedor, cocina, toilette   ·   48,00 m2", fuente(21), GRIS, "lm")
    dibujar_planta(L, MUROS_PB, ABERTURAS_PB, AMB_PB, con_escalera=True, mobiliario=True)
    cadena_cotas(L, [(0.00, 8.00, "8,00")], 0.00, offset=0.55, fnt=fuente(24, True))
    cadena_cotas(L, [(0.00, 6.00, "6,00")], 0.00, vertical=True, offset=0.55, fnt=fuente(24, True))

    L.origen(1760, 1120)
    L.texto_px(1760, 250, "PLANTA ALTA", fuente(32, True), TINTA, "lm")
    L.texto_px(1760, 290, "Dos dormitorios y baño completo   ·   48,00 m2", fuente(21), GRIS, "lm")
    dibujar_planta(L, MUROS_PA, ABERTURAS_PA, AMB_PA, con_escalera=True, mobiliario=True, sube=False)
    cadena_cotas(L, [(0.00, 8.00, "8,00")], 0.00, offset=0.55, fnt=fuente(24, True))
    cadena_cotas(L, [(0.00, 6.00, "6,00")], 0.00, vertical=True, offset=0.55, fnt=fuente(24, True))

    d.text((56, H - 42), "Mobiliario indicativo. Medidas en metros.", font=fuente(19), fill=GRIS)

    ruta = os.path.join(SALIDA, "casa-3-ambientes-anteproyecto.png")
    L.img.save(ruta)
    return ruta


if __name__ == "__main__":
    a = lamina_tecnica()
    b = lamina_presentacion()
    print(a)
    print(b)
