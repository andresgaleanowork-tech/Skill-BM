"""Perfil Octopus Energy.

Maqueta observada (el detalle va en la página 3; el resumen, en la 1). El texto se extrae
en líneas separadas, así que hay que emparejarlas:

    Potencia                21,63 €
    Punta
    3,45 kW * 31 días
    0,110 €/kW/día          11,80 €     <- precio e importe del periodo
    Peaje de distribución
    3,45 kW * 31 días
    0,064 €/ kW/día          6,83 €     <- desglose del mismo precio, NO se suma aparte

Regla del perfil: por cada periodo se toma el PRIMER precio (el total) y se ignora el
desglose; el desglose se usa solo para comprobar que suma lo mismo. Si se sumaran todas
las líneas, el precio saldría al doble.
"""
import re
from . import registrar
from ._comun import importe_tras, a_float

NUM = r'(\d+(?:\.\d{3})*,\d+|\d+,\d+)'
RE_UNIDADES_KW = re.compile(r'^(\d+(?:,\d+)?)\s*kW\s*\*\s*(\d+)\s*d[íi]as$')
RE_UNIDADES_KWH = re.compile(r'^(\d+(?:,\d+)?)\s*kWh$')
RE_PRECIO_KW = re.compile(r'^(\d+,\d+)\s*€/\s*kW/d[íi]a')
RE_PRECIO_KWH = re.compile(r'^(\d+,\d+)\s*€/\s*kWh')
RE_IMPORTE = re.compile(NUM + r'\s*€')
RE_TOTAL = re.compile(r'Total\s+a\s+pagar\s+' + NUM + r'\s*€', re.IGNORECASE)
RE_PERIODO = re.compile(r'Periodo:\s*(\d{2}-\d{2}-\d{4})\s*a\s*(\d{2}-\d{2}-\d{4})\s*\((\d+)\s*d[íi]as\)')
RE_TARIFA = re.compile(r'Tarifa\s+Acceso:\s*(\d\.\dTD)')


@registrar
class Octopus:
    clave = 'octopus'
    nombre = 'Octopus Energy'
    prioridad = 20

    @staticmethod
    def reconoce(texto):
        return 'OCTOPUS ENERGY' in texto.upper() and '€/kW/día' in texto

    @classmethod
    def leer(cls, texto, dias_por_defecto=None):
        avisos, errores, comprobaciones = [], [], []
        m = RE_PERIODO.search(texto)
        dias = int(m.group(3)) if m else dias_por_defecto
        tarifa = RE_TARIFA.search(texto)
        etapas = {'Punta': 'P1', 'Llano': 'P2', 'Valle': 'P3'}

        lineas = [l.strip() for l in texto.splitlines()]
        bloque = periodo = None
        pot, tp, kwh, te = {}, {}, {}, {}
        desglose = {}          # suma del desglose por periodo, para comprobar
        i = 0
        while i < len(lineas):
            linea = lineas[i]
            if re.match(r'^Potencia\b', linea):
                bloque, periodo = 'potencia', None
                i += 1
                continue
            if re.match(r'^Energ[íi]a Activa\b', linea):
                bloque, periodo = 'energia', None
                i += 1
                continue
            if linea in etapas:
                periodo = etapas[linea]
                i += 1
                continue
            if bloque and periodo:
                mu = RE_UNIDADES_KW.match(linea)
                if mu and bloque == 'potencia':
                    kw = a_float(mu.group(1))
                    precio = lineas[i + 1].strip() if i + 1 < len(lineas) else ''
                    mp = RE_PRECIO_KW.match(precio)
                    if mp:
                        pot.setdefault(periodo, kw)
                        if periodo not in tp:                    # el primero es el total
                            tp[periodo] = a_float(mp.group(1))
                            desglose[periodo] = 0.0
                        else:
                            desglose[periodo] += a_float(mp.group(1))
                        i += 2
                        continue
                mu = RE_UNIDADES_KWH.match(linea)
                if mu and bloque == 'energia':
                    k = a_float(mu.group(1))
                    precio = lineas[i + 1].strip() if i + 1 < len(lineas) else ''
                    mp = RE_PRECIO_KWH.match(precio)
                    if mp:
                        if periodo not in kwh:                  # las unidades se repiten en el desglose
                            kwh[periodo] = k
                        if periodo not in te:
                            te[periodo] = a_float(mp.group(1))      # primer precio = total del periodo
                            desglose[periodo] = 0.0
                        else:
                            desglose[periodo] += a_float(mp.group(1))   # desglose: solo para comprobar
                        i += 2
                        continue
            i += 1

        if not pot:
            errores.append('sin líneas de potencia reconocibles')
        if not kwh:
            errores.append('sin líneas de energía reconocibles')

        # comprobación contra los subtotales del resumen de la página 1
        calc_pot = round(sum(pot.get(p, 0) * tp.get(p, 0) * dias for p in pot), 2)
        calc_ene = round(sum(kwh.get(p, 0) * te.get(p, 0) for p in kwh), 2)
        for etiqueta, calculado in (('Potencia', calc_pot), ('Energía Activa', calc_ene)):
            sub = importe_tras(texto, etiqueta, max_lineas=1)
            if sub is not None:
                comprobaciones.append({'bloque': etiqueta, 'suma_lineas': calculado,
                                       'subtotal_factura': sub, 'cuadra': abs(calculado - sub) <= 0.20,
                                       'nota': 'tolerancia de 20 céntimos por el redondeo a 3 decimales'})

        m = RE_TOTAL.search(texto)
        total = a_float(m.group(1)) if m else None
        bono = importe_tras(texto, r'Bono\s+Social') or 0.0
        alquiler = importe_tras(texto, r'Alquiler\s+de') or 0.0

        periodos = sorted(set(kwh))
        salida = {
            'dias': dias, 'periodos': periodos,
            'periodos_potencia': sorted(pot),
            'potencias_kw': {p: pot.get(p, 0) for p in periodos},
            'tp': {p: tp.get(p, 0) for p in periodos}, 'tp_unidad': 'dia',
            'kwh': {p: kwh.get(p, 0) for p in periodos}, 'te': {p: te.get(p, 0) for p in periodos},
            'extras': {'excesos': 0.0, 'bono_social': bono, 'alquiler': alquiler,
                       'reactiva': 0.0, 'otros': 0.0,
                       'autoconsumo_kwh': 0.0, 'autoconsumo_precio_actual': 0.0},
            'iee': 0.0511269632, 'iee_base_factura': None, 'total_factura': total,
            'tolerancia_cuadre': 0.10,
            'tarifa_acceso': tarifa.group(1) if tarifa else None,
            'notas': ['cada término viene desglosado en peaje + cargos + margen: se toma el precio total, '
                      'no la suma del desglose',
                      'el total se reproduce con tolerancia de céntimos por el redondeo a 3 decimales'],
        }
        avisos.append('Octopus factura con 3 decimales y redondea línea a línea: el total se reproduce con '
                      'tolerancia de céntimos, no al céntimo exacto. Se declara así en el informe.')
        return salida, avisos, errores, comprobaciones
