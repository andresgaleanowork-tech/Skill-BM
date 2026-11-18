# Fórmulas de cálculo eléctrico · B&M


---

# Fórmulas de cálculo · B&M Asesores Energéticos

Todo se calcula **sin impuestos** primero y se aplican impuestos al final, una sola vez.

## 1. Término de potencia

`coste potencia = Σ (P_contratada_i × TP_i × días / 365)`

- Las potencias se toman tal cual figuran en la factura. No se modifican salvo petición expresa del cliente.
- 3.0TD y 6.xTD: potencias **no decrecientes** `P1 ≤ P2 ≤ P3 ≤ P4 ≤ P5 ≤ P6`, con al menos una > 15 kW.
- En 2.0TD hay dos periodos (punta y valle).

## 2. Término de energía

`coste energía = Σ (kWh_i × TE_i)`

- Se compara periodo a periodo, nunca con un precio medio.
- Si la factura del cliente trae el coste de energía desglosado en peajes + cargos + margen, se suma todo para obtener el TE real por periodo, que es el comparable con el TE del catálogo.
- En los productos de Iberdrola el TE ya incluye peajes y cargos: **no añadas peajes ni cargos encima de una TE completa**.

## 3. Excesos de potencia (medida tipo 4)

Sin tolerancia automática del 5 %: se factura todo lo que exceda.

`coste excesos = Σ max(Pd_i − Pc_i, 0) × días × tep_i`

tep 3.0TD 2026 (Resolución CNMC 18/12/2025, BOE-A-2025-26348):
P1 0,171373 · P2 0,090584 · P3 0,028721 · P4 0,021891 · P5 0,006142 · P6 0,006142 €/kWh

## 4. Energía reactiva

- Solo si el contador registra reactiva inducida por encima del límite legal (para 3.0TD, 33 % de la activa en cada periodo).
- El precio de la reactiva es el mismo en cualquier comercializadora porque es un cargo regulado: **no genera ahorro por cambio de tarifa**, pero se cuantifica para que el cliente lo sepa.
- Si la factura y los datos del contador (SIPS) discrepan, no recomiendes compensación: primero hay que resolver la discrepancia.

## 5. Autoconsumo y compensación de excedentes

- La compensación simplificada reduce la base del impuesto eléctrico, no es un descuento comercial.
- El precio de compensación varía por comercializadora: compáralo siempre con el que el cliente tiene **acreditado en factura**, no con el de catálogo.
- Si el precio de destino no está confirmado, la cifra principal del informe no computa autoconsumo y los escenarios se muestran aparte.

## 6. Impuestos

| Concepto | Tipo | Base |
|---|---|---|
| Impuesto eléctrico (IEE) | 5,11269632 % | potencia + energía + excesos + reactiva + bono social ± compensación |
| IVA | 21 % | base + IEE + alquiler de contador + no sujetos |
| IGIC (Canarias) | 7 % | sustituye al IVA |
| IPSI (Ceuta y Melilla) | 4 % | sustituye al IVA |
| IEE reducido | 0,5 % | solo cuando la norma vigente lo establezca |

Respetar siempre el impuesto que aplica la fuente: no conviertas una factura con IGIC a IVA.

## 7. Qué se aísla antes de comparar

No forms parte del ahorro estas partidas; si aparecen, se explican aparte:

- Deudas y regularizaciones de periodos anteriores.
- Depósitos y garantías.
- Canjes, saldos promocionales y monederos (tipo Solar Wallet).
- Servicios y productos (PyS) contratados.
- Ajustes por lectura estimada.

## 8. Verificación al céntimo

Reproduce la factura del cliente con sus propios precios. Debe dar exactamente el mismo total. Si no cuadra, busca: (a) una compensación que la comercializadora esté tratando con signo contrario, (b) un concepto exento o no sujeto, (c) un redondeo intermedio. Documenta el criterio que cuadra y úsalo en todo el informe.

---

## 11. Si no puedes ejecutar la calculadora: protocolo de cálculo a mano

Un modelo de lenguaje se equivoca al multiplicar y al sumar listas largas, sobre todo al arrastrar decimales. Cuando no haya ejecución de código (Gemini, Copilot, una web sin análisis de datos), este es el procedimiento obligatorio. No es orientativo.

1. **Trabaja siempre en céntimos enteros.** Convierte cada precio a céntimos (0,253955 €/kWh → 25,3955 c€/kWh). Si trabajas en euros con seis decimales, el redondeo se acumula y la factura deja de cuadrar.
2. **Un producto de cada vez, una línea por periodo, y escribe el resultado de cada línea antes de pasar a la siguiente.** Nada de calcular todo «mentalmente» y presentarlo de golpe.
3. **Ninguna fila se calcula de cabeza si tiene más de dos cifras significativas.** Muestra la operación: `1154 kWh × 29,6845 c€ = 342,56 €`. Si no puedes escribir la multiplicación, no puedes escribir el resultado.
4. **Comprueba la suma por dos vías:** sumando los periodos en orden ascendente y en orden descendente. Si los dos totales no coinciden, hay un error de arrastre.
5. **Aplica los impuestos al final y una sola vez**, en este orden: base IEE → IEE 5,11269632 % → base IVA (más alquiler) → IVA 21 %. Nunca impuestos por periodo.
6. **Cuadra contra el total impreso en la factura.** Si no cuadra al céntimo, no presentes la comparativa: di qué parte no cuadra y pide el dato que falta.
7. **Declara la comprobación en el documento:** «factura de origen reproducida al céntimo: 836,27 €» o «reproducida con una diferencia de 0,03 € por redondeo del alquiler». La segunda frase también vale; lo que no vale es no decir nada.

### Caso de control obligatorio

Antes de entregar cualquier informe, reproduce este caso con las fórmulas. Si no llegas a estas cifras, el método está mal y hay que parar:

| Concepto | Valor |
|---|---|
| Factura Nagini 3.0TD, octubre 2026 (41,5 kW × 6, 2.128 kWh, excesos 9,89 €, bono 0,77 € fuera de la base, alquiler 11,01 €, autoconsumo 1.217 kWh × 0,10 €) | **836,27 €** |
| Mismo mes con Empresa Flex 3.0TD de la hoja 16/11/2026 | **638,88 €** |
| Ahorro | **197,39 €** (23,6 %) |

Una diferencia de céntimos en el control es un error de método, no de redondeo: los redondeos de este caso están fijados a la media unidad al alza (ROUND_HALF_UP) sobre cada línea.

## 12. Errores de cálculo que ya se han producido

| Error | Cómo se detecta | Cómo se evita |
|---|---|---|
| Confundir €/kW·año con €/kW·día (factor 365) | La potencia sale 365 veces mayor o menor de lo razonable | La calculadora exige `tp_unidad` explícito y rechaza el cálculo sin él |
| Aplicar IVA a la base antes de sumar el IEE | El total queda un 5 % corto | Orden fijo: base IEE → IEE → base IVA → IVA |
| Sumar peajes y cargos sobre una TE de catálogo | El ahorro desaparece o se vuelve negativo | En Iberdrola el TE ya los incluye |
| Periodos traspuestos entre factura y catálogo | Un periodo con consumo y precio 0 | La calculadora rechaza el caso: consumo > 0 con TE = 0 es imposible |
| Restar la compensación de excedentes del total en vez de integrarla | El total no cuadra con la factura | Se integra en la base, con su signo |
| Promediar el precio de la energía | El ahorro cambia según el reparto real de consumos | Periodo a periodo, siempre |