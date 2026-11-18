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
