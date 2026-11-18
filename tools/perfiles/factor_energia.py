"""Perfil Factor Energía.

Maqueta observada:
    Energía Activa (El precio incluye el descuento acordado)   793,16 €
        P3  1728,000x0,141890€/kWh
    Potencia                                                   96,45 €
        P1  18,000x2,053575€/kW mes x0,94
    Energía Reactiva   P3 922,760kVArh x0,062332€/kVArh       100,16 €
    Excesos de Potencia                                        0,26 €
    Ajuste Restricciones Técnicas y SA de REE                  63,55 €
    Subtotal                                                1.053,58 €
    Importe IEE  5,11269632 % s/(1053,58) =                    53,87 €
    Alquiler de Equipo 7,58 € · Soporte Gestión 3,00 €
    Base IVA                                                1.118,03 €
    Importe IVA 21,00 % s/(1118,03) =                        234,79 €
    Total Factura                                           1.352,82 €

Particularidad: el término de potencia va en €/kW·mes y con un descuento por línea (x0,94),
y hay partidas que no son comparables (reactiva, ajuste de REE, soporte de gestión).
"""
import re
from . import registrar

NUM = r'(\d+(?:\.\d{3})*,\d+|\d+,\d+)'
RE_POT_MES = re.compile(r'\bP(\d)\s*(\d+(?:,\d+)?)\s*x\s*' + NUM + r'\s*€/kW\s*mes(?:\s*x\s*(\d+,\d+))?')
RE_ENE = re.compile(r'\bP(\d)\s*(\d+(?:\.\d{3})*(?:,\d+)?)\s*x\s*' + NUM + r'\s*€/kWh')
RE_REACTIVA = re.compile(r'\bP(\d)\s*(\d+(?:,\d+)?)\s*kVArh\s*x\s*' + NUM + r'\s*€/kVArh')
RE_IEE = re.compile(r'5,11269632\s*%\s*s/\(\s*' + NUM)
RE_BASE_IVA = re.compile(r'Base\s+IVA\s+' + NUM)
RE_TOTAL = re.compile(r'Total\s+Factura\s+' + NUM)


def a_float(txt):
    return float(str(txt).replace('.', '').replace(',', '.'))


@registrar
class FactorEnergia:
    clave = 'factor_energia'
    nombre = 'Factor Energía'
    prioridad = 15

    @staticmethod
    def reconoce(texto):
        return '€/kW mes' in texto or 'FACTOR ENERGIA' in texto.upper()

    @classmethod
    def leer(cls, texto, dias_por_defecto=None):
        avisos, errores, comprobaciones = [], [], []
        m = re.search(r'Del\s+(\d{2}/\d{2}/\d{4})\s+al\s+(\d{2}/\d{2}/\d{4})', texto)
        dias = dias_por_defecto
        if m:
            from datetime import datetime
            d1 = datetime.strptime(m.group(1), '%d/%m/%Y')
            d2 = datetime.strptime(m.group(2), '%d/%m/%Y')
            dias = (d2 - d1).days + 1

        potencias, tp = {}, {}
        for per, kw, precio, descuento in RE_POT_MES.findall(texto):
            factor = a_float(descuento) if descuento else 1.0
            potencias[f'P{per}'] = a_float(kw)
            tp[f'P{per}'] = round(a_float(precio) * factor, 9)

        kwh, te = {}, {}
        for per, k, precio in RE_ENE.findall(texto):
            per = f'P{per}'
            kwh[per] = a_float(k)
            te[per] = a_float(precio)

        reactiva = 0.0
        for per, k, precio in RE_REACTIVA.findall(texto):
            reactiva += a_float(k) * a_float(precio)

        def imp(patron, grupo=1):
            m = patron.search(texto)
            return a_float(m.group(grupo)) if m else 0.0

        m = RE_IEE.search(texto)
        iee_base = a_float(m.group(1)) if m else None
        m = RE_BASE_IVA.search(texto)
        base_iva = a_float(m.group(1)) if m else None
        m = RE_TOTAL.search(texto)
        if m:
            total = a_float(m.group(1))
        else:
            # en esta maqueta el total va escrito ANTES de la etiqueta «Total Factura»
            m = re.search(NUM + r'\s*€\s*\n\s*Total\s+Factura', texto)
            total = a_float(m.group(1)) if m else None

        # el ajuste de restricciones de REE viene en una línea aparte y con importe al final
        ajuste_ree = imp(re.compile(r'Ajuste\s+Restricciones[^\n]*\n[^\n]*?' + NUM + r'\s*€'))
        if not ajuste_ree:
            ajuste_ree = imp(re.compile(r'Ajuste\s+Restricciones[^\n]*?' + NUM + r'\s*€'))

        subtotal = None
        m = re.search(r'Subtotal\s+' + NUM + r'\s*€', texto)
        if m:
            subtotal = a_float(m.group(1))
            suma = round(sum(potencias[p] * tp[p] * dias / 30 for p in potencias)
                         + sum(kwh[p] * te[p] for p in kwh) + reactiva
                         + imp(re.compile(r'Excesos\s+de\s+Potencia\s+' + NUM))
                         + ajuste_ree, 2)
            comprobaciones.append({'bloque': 'subtotal', 'suma_lineas': suma,
                                   'subtotal_factura': subtotal, 'cuadra': abs(suma - subtotal) <= 0.05,
                                   'nota': f'potencia en €/kW·mes + energía + reactiva + excesos + ajuste REE ({ajuste_ree} €)'})

        periodos = sorted(set(potencias) | set(kwh))
        salida = {
            'dias': dias, 'periodos': periodos,
            'potencias_kw': {p: potencias.get(p) for p in periodos},
            'tp': {p: tp.get(p, 0) for p in periodos}, 'tp_unidad': 'mes',
            'kwh': {p: kwh.get(p, 0) for p in periodos}, 'te': {p: te.get(p, 0) for p in periodos},
            'extras': {'excesos': imp(re.compile(r'Excesos\s+de\s+Potencia\s+' + NUM)),
                       'bono_social': 0.0,
                       'alquiler': imp(re.compile(r'Alquiler\s+de\s+Equipo\s+' + NUM)),
                       'reactiva': round(reactiva, 2),
                       'otros': round(ajuste_ree, 2),
                       'otros_sin_iee': round(imp(re.compile(r'Soporte\s+Gesti[óo]n\s+' + NUM)), 2),
                       'autoconsumo_kwh': 0.0, 'autoconsumo_precio_actual': 0.0},
            'iee': 0.0511269632, 'iee_base_factura': iee_base,
            'base_iva_factura': base_iva, 'total_factura': total,
            'notas': ['término de potencia en €/kW·mes, convertido a 30 días',
                      'el ajuste de restricciones de REE y la reactiva no generan ahorro por cambio de tarifa'],
        }
        if not potencias:
            errores.append('sin líneas de potencia reconocibles')
        if not kwh:
            errores.append('sin líneas de energía reconocibles')
        return salida, avisos, errores, comprobaciones
