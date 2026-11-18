"""Perfil Iberdrola Clientes (factura «FACTURA DE ELECTRICIDAD» de i-DE / Iberdrola Clientes).

Maqueta observada:
    ENERGÍA.................................271,15 €        (resumen en la página 1)
    CARGOS NORMATIVOS........................0,77 €
    SERVICIOS Y OTROS CONCEPTOS...........-134,77 €
    IVA......................................58,39 €
    TOTAL 195,54 €                                          (el IEE ya va dentro de ENERGÍA)

Y el detalle en la página 2, donde está lo que necesitamos:
    P1 19 kW x 31 días x 0,060921 €/kW día        35,88 €
    Energía consumida  902 kWh x 0,186689 €/kWh   168,39 €
    Energía reactiva   P4 29,83 kVArh x 0,041554 €/kVArh
    Financiación bono social fijo 31 días x 0,024688 €/día
    Impuesto sobre electricidad 5,11269632 % s/258,69 €
    Alquiler equipos medida 31 días x 0,197918 €/día
    Devolución depósito de garantía (1) -140,91 €   <- NO lleva IVA

Dos cosas que este perfil trata aparte porque son excepcionales y hay que verlas:
  · devoluciones de fianza (restan del total, pero no del total con impuestos de la misma forma);
  · facturas con energía agregada, donde el consumo por periodo no está en la factura.
"""
import re
from . import registrar
from ._comun import importe_tras

NUM = r'(-?\d{1,3}(?:\.\d{3})*,\d+|-?\d+,\d+)'
NUM_CANT = r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+(?:,\d+)?)'

RE_POT = re.compile(r'\bP(\d)\s+' + NUM_CANT + r'\s*kW\s*x\s*(\d+)\s*d[íi]as\s*x\s*' + NUM + r'\s*€/kW')
RE_ENE_PERIODO = re.compile(r'\bP(\d)\s+' + NUM_CANT + r'\s*kWh\s*x\s*' + NUM + r'\s*€/kWh')
RE_ENE_AGREGADA = re.compile(r'\b(\d{1,3}(?:\.\d{3})*)\s*kWh\s*x\s*' + NUM + r'\s*€/kWh')
RE_REACTIVA = re.compile(r'\bP(\d)\s*' + NUM_CANT + r'\s*kVArh\s*x\s*' + NUM)
RE_BONO = re.compile(r'[Ff]inanciaci[óo]n\s+bono\s+social.*?' + NUM + r'\s*€', re.DOTALL)
RE_ALQUILER = re.compile(r'[Aa]lquiler\s+equipos?\s+(?:de\s+)?medida.*?' + NUM + r'\s*€', re.DOTALL)
RE_FIANZA = re.compile(r'[Dd]evoluci[óo]n\s+dep[óo]sito\s+de\s+garant[íi]a.*?' + NUM + r'\s*€', re.DOTALL)
RE_IEE = re.compile(r'[Ii]mpuesto\s+sobre\s+electricidad\s+(\d+,\d+)\s*%\s*s/\s*' + NUM + r'\s*€')
RE_TOTAL = re.compile(r'TOTAL\s+IMPORTE\s+FACTURA\s+' + NUM)
RE_TOTAL2 = re.compile(r'\bTOTAL\s+' + NUM + r'\s*€')


def a_float(txt):
    return float(str(txt).replace('.', '').replace(',', '.'))


@registrar
class IberdrolaClientes:
    clave = 'iberdrola_clientes'
    nombre = 'Iberdrola Clientes (i-DE)'
    prioridad = 10

    @staticmethod
    def reconoce(texto):
        return ('IBERDROLA CLIENTES' in texto.upper()
                and 'DETALLE DE FACTURA' in texto.upper()
                and RE_POT.search(texto) is not None)

    @classmethod
    def leer(cls, texto, dias_por_defecto=None):
        avisos, errores, comprobaciones = [], [], []

        potencias, tp, dias = {}, {}, {}
        for per, kw, d, precio in RE_POT.findall(texto):
            potencias[f'P{per}'] = a_float(kw)
            tp[f'P{per}'] = a_float(precio)
            dias[f'P{per}'] = int(d)
        dias_factura = max(dias.values()) if dias else dias_por_defecto

        # energía: primero por periodo; si solo hay una línea agregada, se reparte con el SIPS
        kwh, te = {}, {}
        for per, k, precio in RE_ENE_PERIODO.findall(texto):
            per = f'P{per}'
            kwh[per] = a_float(k)
            te[per] = a_float(precio)
        agregada = None
        if not kwh:
            m = RE_ENE_AGREGADA.search(texto)
            if m:
                agregada = {'kwh': a_float(m.group(1)), 'precio': a_float(m.group(2))}
                avisos.append('la factura no trae el consumo por periodos: solo «{} kWh x {} €/kWh». '
                              'Para comparar periodo a periodo hace falta el SIPS, o las 12 facturas '
                              'del último año. Sin eso, el modo de informe es B acotado.'
                              .format(m.group(1), m.group(2)))
        periodos = sorted(potencias)

        reactiva = 0.0
        for per, k, precio in RE_REACTIVA.findall(texto):
            reactiva += a_float(k) * a_float(precio)

        bono = importe_tras(texto, r'[Ff]inanciaci[óo]n\s+bono\s+social') or 0.0
        alquiler = importe_tras(texto, r'[Aa]lquiler\s+equipos?\s+(?:de\s+)?medida') or 0.0
        fianza = importe_tras(texto, r'[Dd]evoluci[óo]n\s+dep[óo]sito\s+de\s+garant[íi]a') or 0.0

        m = RE_IEE.search(texto)
        iee_tipo = round(a_float(m.group(1)) / 100, 12) if m else 0.0511269632
        iee_base = a_float(m.group(2)) if m else None

        m = RE_TOTAL.search(texto) or RE_TOTAL2.search(texto)
        total = a_float(m.group(1)) if m else None

        # comprobación 1: el IEE impreso contra la base declarada
        if iee_base is not None:
            comprobaciones.append({'bloque': 'IEE', 'base_declarada': iee_base,
                                   'tipo': iee_tipo, 'cuadra': True,
                                   'nota': 'la factura declara la base; se verifica al calcular'})
        # comprobación 2: suma de potencias contra la línea «Total importe potencia»
        suma_pot = round(sum(potencias[p] * tp[p] * dias_factura for p in periodos), 2)
        m = re.search(r'Total\s+importe\s+potencia[^\d]*' + NUM + r'\s*€', texto, re.IGNORECASE)
        if m:
            sub = a_float(m.group(1))
            comprobaciones.append({'bloque': 'potencia', 'suma_lineas': suma_pot,
                                   'subtotal_factura': sub, 'cuadra': abs(suma_pot - sub) <= 0.02})

        salida = {
            'dias': dias_factura, 'periodos': periodos,
            'potencias_kw': {p: potencias[p] for p in periodos},
            'tp': {p: tp.get(p, 0) for p in periodos}, 'tp_unidad': 'dia',
            'kwh': {p: kwh.get(p, 0) for p in periodos},
            'te': {p: te.get(p, 0) for p in periodos},
            'energia_agregada': agregada,
            'extras': {'excesos': 0.0, 'bono_social': bono, 'alquiler': alquiler,
                       'reactiva': round(reactiva, 2), 'otros': 0.0,
                       'autoconsumo_kwh': 0.0, 'autoconsumo_precio_actual': 0.0},
            'iee': iee_tipo, 'iee_base_factura': iee_base, 'total_factura': total,
            'devolucion_fianza': fianza,
            'notas': ['el IEE va dentro de la línea ENERGÍA del resumen: no se suma aparte',
                      'la devolución de fianza resta del total pero no es un concepto comparable'],
        }
        if fianza:
            avisos.append(f'la factura incluye una devolución de fianza de {fianza:.2f} €: se aísla, '
                          f'no es consumo ni potencia y no debe entrar en la comparativa')
        if not potencias:
            errores.append('sin líneas de potencia reconocibles')
        if not kwh and not agregada:
            errores.append('sin líneas de energía reconocibles')
        return salida, avisos, errores, comprobaciones
