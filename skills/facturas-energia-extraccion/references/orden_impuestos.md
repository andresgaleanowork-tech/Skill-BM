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
