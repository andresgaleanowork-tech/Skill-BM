"""Perfiles de lectura de facturas por comercializadora.

Cada comercializadora maqueta su factura a su manera y, sobre todo, **factura distinto**:

- Nexus/ENERGIA: parte el precio en «Energía ATR» + «Energía Libre» (hay que sumarlos).
- Iberdrola Clientes: da la energía en una sola línea «902 kWh x 0,186689 €/kWh» y aplica
  el bono social como «Financiación bono social fijo».
- Octopus: desglosa cada término en peaje + cargos + margen, con 3 decimales y redondeo por
  línea, así que el subtotal impreso no coincide con el cálculo exacto.
- Factor Energía: término de potencia en €/kW·mes con un descuento (x0,94) por línea, y
  partidas que no son comparables (reactiva, ajuste de restricciones de REE, soporte).

Regla de oro: un perfil **nunca rellena un dato que no pueda verificar** contra un subtotal
impreso. Si no cuadra, se para y lo dice. Vale más un rechazo que un informe mal.
"""

REGISTRO = {}


def registrar(clase):
    REGISTRO[clase.clave] = clase
    return clase


def elegir(texto):
    """Devuelve el perfil que reconoce la factura, o None si no hay ninguno."""
    detectados = [c for c in REGISTRO.values() if c.reconoce(texto)]
    if not detectados:
        return None
    detectados.sort(key=lambda c: c.prioridad)
    return detectados[0]


def por_clave(clave):
    return REGISTRO.get(clave)


# importar aquí abajo registra los perfiles
from . import generico          # noqa: E402,F401
from . import iberdrola_clientes  # noqa: E402,F401
from . import octopus           # noqa: E402,F401
from . import factor_energia    # noqa: E402,F401
