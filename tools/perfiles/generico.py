"""Perfil genérico: la maqueta detallada tipo Nexus/ENERGIA.

Es la base y el último recurso. Reconoce líneas del estilo:

    P4 41,500 kW x 31 Días x 0,01064700 €/kW día
    P4 1154 kWh x 0,294218 €/kWh

y bloques con subtotal impreso (ATR / libre / excesos / bono / alquiler / IEE).
"""
import re
from . import registrar
from ._comun import importe_tras

NUM = r'(-?\d{1,3}(?:\.\d{3})*,\d+|-?\d+,\d+)'
NUM_CANT = r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+(?:,\d+)?)'

RE_IMPORTE = re.compile(NUM + r'\s*€')
RE_POTENCIA = re.compile(r'\bP(\d)\s+' + NUM + r'\s*kW\s*x\s*(\d+)\s*D[íi]as\s*x\s*' + NUM + r'\s*€/kW')
RE_ENERGIA = re.compile(r'\bP(\d)\s+' + NUM_CANT + r'\s*kWh\s*x\s*' + NUM + r'\s*€/kWh')
RE_IEE_TIPO = re.compile(r'(\d+,\d+)\s*%\s*(?:sobre|s/)\s*' + NUM + r'\s*€?')


def a_float(txt):
    return float(str(txt).replace('.', '').replace(',', '.'))


def importe(linea):
    m = RE_IMPORTE.search(linea)
    return a_float(m.group(1)) if m else None


@registrar
class Generico:
    clave = 'generico'
    nombre = 'Maqueta detallada (Nexus/ENERGIA y similares)'
    prioridad = 90

    @staticmethod
    def reconoce(texto):
        return bool(RE_POTENCIA.search(texto) and RE_ENERGIA.search(texto))

    @staticmethod
    def bloques(texto):
        """Bloques por rótulo, con el texto entre un rótulo y el siguiente."""
        rotulos = [
            ('potencia', r'T[eé]rmino\s+Potencia'),
            ('energia_atr', r'T[eé]rmino\s+Energ[íi]a\s+ATR'),
            ('energia_libre', r'T[eé]rmino\s+Energ[íi]a\s+Libre'),
            ('energia', r'T[eé]rmino\s+Energ[íi]a(?!\s+ATR|\s+Libre)'),
            ('autoconsumo', r'Autoconsumo'),
            ('reactiva', r'[Ee]nerg[íi]a\s+[Rr]eactiva'),
            ('excesos', r'Excesos\s+Distribuidora'),
            ('bono', r'Bono\s+social'),
            ('alquiler', r'Alquiler\s+de\s+equipos'),
            ('otros', r'(?:Ajuste|Servicios|Soporte)'),
            ('iee', r'Impuesto\s+sobre\s+la\s+electricidad'),
        ]
        pos = []
        for clave, patron in rotulos:
            m = re.search(patron, texto)
            if m:
                pos.append((m.start(), clave))
        pos.sort()
        salida = {}
        for i, (p, clave) in enumerate(pos):
            fin = pos[i + 1][0] if i + 1 < len(pos) else len(texto)
            salida.setdefault(clave, texto[p:fin])
        return salida

    @classmethod
    def leer(cls, texto, dias_por_defecto=None):
        bloques = cls.bloques(texto)
        avisos, errores, comprobaciones = [], [], []

        potencias, tp, dias = {}, {}, {}
        for per, kw, d, precio in RE_POTENCIA.findall(texto):
            potencias[f'P{per}'] = a_float(kw)
            dias[f'P{per}'] = int(d)
            tp[f'P{per}'] = a_float(precio)
        dias_factura = max(dias.values()) if dias else dias_por_defecto
        unidad_tp = 'dia'

        # OJO: el mismo consumo aparece en el bloque ATR y en el libre (con precios distintos).
        # Los kWh NO se suman entre bloques; los precios sí.
        kwh, te = {}, {}
        for clave in ('energia_atr', 'energia_libre', 'energia'):
            bloque = bloques.get(clave, '')
            if not bloque:
                continue
            suma = 0.0
            for per, k, precio in RE_ENERGIA.findall(bloque):
                per = f'P{per}'
                kwh[per] = max(kwh.get(per, 0), a_float(k))
                te[per] = te.get(per, 0) + a_float(precio)
                suma += a_float(k) * a_float(precio)
            sub = importe(bloque)
            if sub is not None:
                comprobaciones.append({'bloque': clave, 'suma_lineas': round(suma, 2),
                                       'subtotal_factura': round(sub, 2), 'cuadra': abs(suma - sub) <= 0.02})

        autokwh, autoimp = 0.0, 0.0
        for per, k, precio in RE_ENERGIA.findall(bloques.get('autoconsumo', '')):
            autokwh += a_float(k)
            autoimp += a_float(k) * a_float(precio)

        def imp(etiqueta):
            return importe_tras(texto, etiqueta) or 0.0

        m = RE_IEE_TIPO.search(texto)
        iee_tipo = round(a_float(m.group(1)) / 100, 12) if m else 0.0511269632
        iee_base = a_float(m.group(2)) if m else None
        m = re.search(r'Total\s+factura:?\s*' + NUM, texto, re.IGNORECASE)
        total = a_float(m.group(1)) if m else None

        periodos = sorted(set(potencias) | set(kwh))
        salida = {
            'dias': dias_factura, 'periodos': periodos,
            'potencias_kw': {p: potencias.get(p) for p in periodos},
            'tp': {p: tp.get(p, 0) for p in periodos}, 'tp_unidad': unidad_tp,
            'kwh': {p: kwh.get(p, 0) for p in periodos}, 'te': {p: te.get(p, 0) for p in periodos},
            'extras': {'excesos': imp(r'Excesos\s+Distribuidora'),
                       'bono_social': imp(r'Bono\s+social'),
                       'alquiler': imp(r'Alquiler\s+de\s+equipos'),
                       'reactiva': round(imp(r'[Ee]nerg[íi]a\s+[Rr]eactiva'), 2),
                       'otros': round(imp(r'Ajuste\s+(?:de\s+)?[Rr]estricciones')
                                      + imp(r'Soporte\s+Gesti[óo]n'), 2),
                       'autoconsumo_kwh': autokwh,
                       'autoconsumo_precio_actual': round(autoimp / autokwh, 6) if autokwh else 0.0},
            'iee': iee_tipo, 'iee_base_factura': iee_base, 'total_factura': total,
            'notas': ['el bono social va fuera de la base del IEE en esta maqueta (se comprueba después)'],
        }
        if not potencias:
            errores.append('sin líneas de término de potencia reconocibles')
        if not kwh:
            errores.append('sin líneas de energía reconocibles')
        return salida, avisos, errores, comprobaciones
