# Extracción y cuadre de facturas, y lectura de SIPS


---

---
name: facturas-energia-extraccion
description: >
  Extrae y normaliza los datos de una factura eléctrica española (Octopus,
  Iberdrola, Naturgy, Endesa, Nagini, Alcanzia, TotalEnergies…) y comprueba que
  los importes cuadran al céntimo. Usar cuando se pida leer una factura, sacar
  potencias, consumos y precios de un PDF, verificar un recibo o preparar los datos
  de entrada para un informe de ahorro.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Extracción de facturas eléctricas

Objetivo: convertir un PDF de factura en un JSON fiable y **demostrar** que los importes cuadran. Si no cuadra, se reporta la diferencia; no se ajusta a ojo.

## La factura la envía el cliente, no se descarga

No hay acceso a las áreas de cliente de las comercializadoras. La factura llega como PDF adjunto, junto con el SIPS si el cliente lo consigue. De ahí se extraen los datos; lo que no aparezca, se pide.

## Paso 1 · ¿Tiene capa de texto?

- Prueba a extraer texto. Si sale texto legible, se trabaja sobre él.
- Si el PDF es un escaneo (sin texto), renderiza las páginas a imagen y **léelas visualmente**. No intentes adivinar importes.
- Las facturas de comercializadoras pequeñas suelen tener capas de texto desordenadas: los importes aparecen en una columna y los conceptos en otra. Reconstruye por pares concepto-importe.

## Paso 2 · Datos que hay que sacar siempre

1. Titular y **CIF/NIF**.
2. CUPS y dirección del punto de suministro.
3. Comercializadora actual y **nombre comercial de la tarifa**.
4. Tarifa de acceso (2.0TD, 3.0TD, 6.1TD…).
5. Periodo facturado y **número de días**.
6. Potencias contratadas por periodo.
7. Energía consumida por periodo (kWh).
8. Precio de energía por periodo y precio de potencia (con su unidad: €/kW·día o €/kW·año).
9. Conceptos adicionales: excesos, reactiva, bono social, alquiler de contador, autoconsumo, servicios.
10. IEE, IVA (o IGIC/IPSI) y **total**.
11. Fecha de fin de contrato y datos de contacto.

Si el cliente aporta **SIPS** en lugar de (o además de) la factura, aplica `references/sips.md`: consumo por periodo, demanda máxima cuarto-horaria, reactiva y cobertura temporal. El SIPS no trae precios: sin factura no se puede comparar, solo calcular lo que pagaría con nuestra oferta.

## Paso 3 · Cuadrar la factura

Aplica el orden de `references/orden_impuestos.md` y compara con el total del documento. Tolerancia: 0,01 €. Si no cuadra:

- Prueba si el bono social entra o no en la base del IEE (varía por comercializadora).
- Comprueba el signo de la compensación de excedentes.
- Busca un concepto no sujeto a IVA.
- Revisa si el IEE se aplica sobre un importe ya redondeado.

Documenta la variante que cuadra: **esa** es la que se usa después en la comparativa.

## Paso 4 · Devolver el JSON

Sigue el esquema de `references/esquema_json.md` y ejecuta `scripts/extraer_factura.py` como validador si trabajas en un entorno con Python. Marca cada campo con su origen: `pdf` (leído) o `calculado`.

## Avisos que deben aparecer en la salida

- Reactiva penalizada o máxima demandada por encima de la potencia contratada.
- Lecturas estimadas (procedencia «Calculada») que expliquen un consumo raro.
- Regularizaciones, deudas o fianzas incluidas en el importe.
- Servicios y productos (PyS) que no son suministro.

## Recursos

- `references/esquema_json.md`: estructura de salida.
- `references/orden_impuestos.md`: cadena de cálculo y variantes por comercializadora.
- `references/sips.md`: qué se extrae del SIPS y cómo se usa.
- `scripts/extraer_factura.py`: validación de cuadre y normalización.

## Qué pedir al cliente, en este orden

El asistente no busca nada y no puede entrar en las áreas de cliente: lo que no se pide, no existe.

1. **Factura completa del último periodo + SIPS** (fichero de consumos de la distribuidora). Con los dos, el informe es modo A: comparativa del periodo y **anualización con el perfil real**, no una proyección.
2. **Si no hay SIPS: las doce facturas del último año.** El resultado es el mismo, solo cuesta más. La suma de los doce periodos da el consumo anual por periodos.
3. **Si solo hay una factura**: se compara el periodo (modo B) y la cifra anual se declara como proyección de 12 recibos equivalentes. Nunca se presenta como anualización real.

### Cuándo se puede pedir el SIPS y cuándo no

- **Comunidad Valenciana**: la distribuidora es i-DE (grupo Iberdrola) en la práctica totalidad del territorio, así que el SIPS se solicita y se obtiene por el cliente o por nosotros. Es el camino normal.
- **Otras distribuidoras o suministros fuera de la Comunidad Valenciana**: si no hay acceso al SIPS, **se piden las doce facturas**. No se estima.
- **Nunca se anualiza «a ojo»**: si no hay SIPS ni doce facturas, el informe va en modo B y lo dice en la primera página.

La herramienta que lo hace: `python tools/anualizar.py --sips sips.pdf --factura ficha.json --producto "3.0TD Empresa Flex"`. Devuelve el JSON con el consumo anual real, listo para la calculadora.


---

# Cadena de cálculo y variantes

## Orden

```
base IEE = potencia + energía + excesos + reactiva + bono social ± compensación de excedentes
IEE      = base IEE × 5,11269632 %
base IVA = base IEE + IEE + alquiler de contador + conceptos no sujetos que sí llevan IVA
IVA      = base IVA × 21 %
total    = base IVA + IVA
```

## Variantes observadas en facturas reales

| Comercializadora | Particularidad |
|---|---|
| Octopus | El bono social entra en la base del IVA pero no siempre en la del IEE; la compensación de excedentes puede no restarse de la base. Comprobar cuál cuadra. |
| Nagini / comercializadoras pequeñas | La base del IEE excluye el bono social y el alquiler; el autoconsumo se resta de la base. |
| Iberdrola | Base limpia: potencia + energía + excesos + reactiva + bono social. |
| Canarias / Ceuta y Melilla | IGIC 7 % o IPSI 4 % en lugar de IVA. No convertir. |
| IEE reducido | 0,5 % cuando la norma vigente lo establece (por ejemplo, medidas de 2026). Se aplica a las mismas bases. |

## Errores típicos al reconstruir

1. Aplicar IVA sobre la base sin IEE.
2. Sumar el alquiler de contador a la base del IEE.
3. Restar la compensación de excedentes de la base del IEE cuando la comercializadora no lo hace.
4. Usar el precio medio de energía cuando la factura trae periodos distintos.
5. Confundir €/kW·día con €/kW·año en la potencia.


---

# Esquema de salida

```json
{
  "titular": {"nombre": "", "documento": "", "tipo_documento": "CIF|NIF"},
  "suministro": {"cups": "", "direccion": "", "tarifa_acceso": "3.0TD", "distribuidora": ""},
  "comercializadora": {"nombre": "", "referencia_contrato": "", "producto": "", "fin_contrato": "AAAA-MM-DD"},
  "periodo": {"desde": "AAAA-MM-DD", "hasta": "AAAA-MM-DD", "dias": 31, "procedencia_lectura": "real|calculada"},
  "potencias_kw": [0,0,0,0,0,0],
  "kwh": {"P1":0,"P2":0,"P3":0,"P4":0,"P5":0,"P6":0},
  "precios": {
    "tp": [0,0,0,0,0,0],
    "tp_unidad": "dia|anio",
    "te": [0,0,0,0,0,0]
  },
  "conceptos": {
    "potencia_eur": 0, "energia_eur": 0, "excesos_eur": 0, "reactiva_eur": 0,
    "autoconsumo_eur": 0, "bono_social_eur": 0, "alquiler_eur": 0, "servicios_eur": 0,
    "iee_eur": 0, "iva_eur": 0, "total_eur": 0
  },
  "impuestos": {"iee_tipo": 0.0511269632, "iva_tipo": 0.21, "otro": null},
  "alertas": ["reactiva penalizada", "demanda máxima > potencia contratada", "lectura estimada"],
  "cuadre": {"total_factura": 0, "total_calculado": 0, "diferencia": 0, "ok": true}
}
```

Reglas:

- Importes en euros con dos decimales; precios con seis decimales.
- `tp_unidad` es obligatorio: confundir €/kW·día con €/kW·año multiplica o divide por 365 el coste de potencia.
- Los campos que no aparezcan en la factura van a `null`, no a cero.
- `alertas` se rellena siempre, aunque esté vacío.


---

# SIPS: curva de carga del contador

El SIPS es el archivo de la distribuidora con las medidas cuarto-horarias. Es la fuente que convierte una proyección en una anualización.

## Qué se extrae

| Dato | Para qué sirve |
|---|---|
| Consumo por periodo tarifario (P1…P6) y por hora | Reparto real de energía y estacionalidad |
| Potencia máxima demandada por periodo (cuarto-horaria) | Detectar sobredimensionamiento y riesgo de excesos |
| Energía reactiva por periodo | Ver si procede compensar |
| Fechas cubiertas y huecos | Saber si el año está completo |
| Tipo de medida (tipo 4 con ICP o maxímetro) | Aplicar el cálculo de excesos correcto |

## Comprobaciones al recibirlo

1. **Cobertura temporal**: ¿365 días completos? Si faltan meses, la anualización no es anual.
2. **CUPS correcto**: el SIPS debe ser del mismo CUPS que la factura. Un SIPS de otro suministro invalida el informe.
3. **Unidades**: la energía en kWh por cuarto de hora; la potencia en kW (media cuarto-horaria), no en kWh.
4. **Reactiva**: si la factura y el SIPS discrepan, no se recomienda compensación hasta resolverlo.
5. **Demanda por encima de la potencia contratada**: indica excesos reales; se cuantifican, no se ocultan.

## Uso en el informe

- **Con factura + SIPS (modo A)**: se anualiza con el perfil real y se valora con los precios acreditados en la factura. Es el informe de referencia.
- **Solo SIPS (modo C)**: se calcula el coste con nuestra oferta para ese consumo real. No se puede afirmar ahorro porque falta el precio actual.
- En ambos casos, si el SIPS es de un periodo y los precios de otro, se declara como supuesto.