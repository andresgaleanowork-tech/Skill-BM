# Escenarios según los datos disponibles

## 0. Regla previa: la hoja de precios se carga a mano y tiene fecha

Los precios se cargan **una vez y se recargan solo cuando cambian** (cadencia semanal o mensual). El asistente no accede al área de Iberdrola: la ficha la aporta el usuario.

La referencia no es el calendario, es la antigüedad de la carga:

| Antigüedad de la carga | Qué se hace |
|---|---|
| Menos de 7 días | Se calcula con normalidad |
| Entre 7 y 30 días | Se avisa y se pregunta si ha salido hoja nueva antes de un informe importante |
| Más de 30 días | No se emite informe nuevo sin confirmar la vigencia |

En todo informe y presupuesto consta la **fecha de la hoja** usada. Si la hoja cambia a mitad de un informe, se recalcula entero; nunca se mezclan dos cargas.

## 1. Pedir siempre factura **y** SIPS

Al pedir documentación, se piden las dos cosas en el mismo mensaje:

> «Envíame las facturas completas y, si puedes, el SIPS (curva de carga del contador). Con las dos cosas el informe es completo; con una sola, también se puede hacer, pero con las limitaciones que te indico.»

El SIPS aporta lo que la factura no tiene: reparto horario real, demanda máxima por periodo, reactiva y excesos. Es lo que convierte una proyección en una anualización.

## 2. Los tres modos de informe

| Modo | Datos que hay | Qué se entrega | Qué se advierte |
|---|---|---|---|
| **A · Completo** | Factura + SIPS | Informe completo: verificación de la factura, comparativa por periodo y **anualización con el perfil real** de consumo y demanda | Nada relevante: es el informe de referencia |
| **B · Solo factura** | Factura, sin SIPS | Verificación de la factura y comparativa del periodo facturado, **anualizada suponiendo que todo el año se comporta como el periodo de la factura y con los precios de esa factura** | Falta la anualización real: no hay curva ni estacionalidad. La cifra anual es una proyección a 12 recibos equivalentes |
| **C · Solo SIPS** | SIPS, sin factura | **Lo que el cliente pagaría con nuestra oferta** con su consumo real, periodo a periodo | **No se puede afirmar ahorro**: falta el precio actual. Se entrega coste con nuestra tarifa, no comparativa |

Nunca se presenta el modo B o C como si fuera el modo A. La falta de datos se dice en la primera página, no en una nota al pie.

## 3. Modo B · solo factura

1. Verifica la factura al céntimo.
2. Compara el periodo facturado con el producto elegible.
3. Para la cifra anual: **supuesto declarado** — «se aplica el mismo patrón de consumo y los mismos precios del periodo facturado a los doce meses». Si el periodo es de verano, se advierte que el peso de P6 en invierno será mayor.
4. Etiqueta la cifra como proyección orientativa.

## 4. Modo C · solo SIPS

Antes de calcular, pide **los datos principales del potencial cliente**:

- Titular y CIF/NIF (decide la gama de producto).
- CUPS y dirección del suministro.
- Tarifa de acceso y potencias contratadas (si no vienen en el SIPS).
- Distribuidora y, si lo sabe, comercializadora y producto actuales.
- Fecha aproximada del último cambio de tarifa y si tiene permanencia.

Con eso se entrega:

- Consumo por periodos y demanda máxima reales.
- **Coste con nuestra oferta** para ese consumo (potencia + energía + excesos + impuestos).
- Si el cliente aporta el precio que paga, entonces sí se calcula el ahorro; si no, se dice claramente: «esto es lo que pagarías con nosotros, no cuánto ahorras».

Frase tipo para el cliente: «Con tus consumos reales, con nuestra tarifa pagarías X €/año. Para decirte cuánto ahorras necesito una factura con tu precio actual.»

## 5. Coherencia entre fuentes

- Perfil de consumo del SIPS con precios actuales de una factura de otro periodo: **se puede**, pero se declara.
- Consumo de la factura con demanda máxima del SIPS: se declara igual.
- Un informe nunca mezcla datos de dos suministros ni de dos titulares.
- Si el SIPS y la factura discrepan en reactiva o en demanda, no se recomienda nada (ni compensación ni cambio de potencia) hasta resolver la discrepancia.
