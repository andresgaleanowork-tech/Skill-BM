# Proceso de informes de ahorro · B&M


---
---
name: informes-ahorro-electrico
description: >
  Elabora informes de ahorro eléctrico de B&M Asesores Energéticos comparando la
  factura real del cliente con los productos de Iberdrola (Empresa Flex 3.0TD y
  6.1TD, planes 2.0TD). Usar cuando se pida un informe de ahorro, una comparativa
  de tarifa, valorar un cambio de comercializadora o cuantificar cuánto ahorra un
  cliente con su factura de luz, tanto si el titular es CIF como NIF.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Informes de ahorro eléctrico · B&M

Produce un informe de ahorro cerrado y verificable: la factura del cliente cuadrada al céntimo, la comparativa con el producto correcto de Iberdrola, el ahorro separado en hecho / supuesto / proyección y un PDF final. Si un dato no está acreditado, se dice; no se rellena.

## Entradas necesarias

1. Factura eléctrica completa en PDF (todas las páginas) del cliente.
2. **SIPS** (curva de carga del contador), si el cliente puede aportarlo.
3. Titular y **CIF o NIF**: decide qué productos se pueden ofrecer.
4. Hoja de precios de Iberdrola **vigente**, con su fecha.

Para calcular hacen falta, como mínimo, la hoja de precios y **una** fuente de consumo: factura o SIPS. Pide siempre las dos en el mismo mensaje («factura completa y SIPS si es posible») porque el informe completo necesita ambas; hay mensajes tipo listos en `references/plantilla_recepcion.md`. No estimes precios ni consumos.

### Aviso de vigencia de precios (obligatorio)

Los precios se cargan a mano **una vez y se recargan solo cuando cambian**, con una cadencia real semanal o mensual. El asistente no tiene acceso al área de Iberdrola y no actualiza nada por su cuenta. El control es la **antigüedad de la carga**: menos de 7 días, se calcula con normalidad; entre 7 y 30, avisa y pregunta si ha salido hoja nueva antes de un informe importante; más de 30, **no se emite informe nuevo** sin confirmar vigencia. En todo informe consta la fecha de la hoja usada.

## Paso 1 · Clasificar al titular

| Documento | Gama | Productos válidos |
|---|---|---|
| CIF (empresa, sociedad) | Empresa | Empresa Flex, Empresas 10 %TE, Empresa Plus, Especial 15 %TE, Plan Exclusivo 30 %TE |
| NIF/NIE (persona física) | Hogar / autónomo | Impulsa 24h, Plan Exclusivo 15 %TE/TP, Plan Estable, Especial plus, Plan Hogar Especial |

**Nunca** propongas Empresa Flex, Empresas 10 %TE ni Especial 15 %TE a un NIF. Y no llames autónomo a alguien solo por tener NIF: es una persona física con un punto de suministro.

## Paso 2 · Leer la factura y cuadrarla al céntimo

Antes de comparar nada, la factura de origen tiene que reproducirse exactamente. Orden de operaciones:

1. Suma los conceptos que forman la **base del impuesto eléctrico** (potencia, energía, excesos, reactiva, bono social y, si aparece, compensación de excedentes con el signo que aplique la comercializadora).
2. **IEE** = base × 5,11269632 %.
3. Base IVA = base + IEE + alquiler de contador + conceptos no sujetos.
4. **IVA** = base IVA × 21 % (o el impuesto que corresponda: IGIC 7 % en Canarias, IPSI 4 % en Ceuta y Melilla, IEE reducido 0,5 % cuando esté vigente).
5. Total = base IVA + IVA.

Si el total no coincide al céntimo con el de la factura, **para y explica la diferencia** antes de seguir. Un informe que no cuadra la factura de origen no se envía.

Los detalles de reconstrucción por tipo de factura están en `references/formulas.md`.

## Paso 2 bis · Decidir el modo de informe

Según la documentación recibida (detalle en `references/escenarios_de_datos.md`):

| Modo | Datos | Qué se entrega | Qué se advierte |
|---|---|---|---|
| **A · Completo** | Factura + SIPS | Comparativa y **anualización con el perfil real** | — |
| **B · Solo factura** | Factura sin SIPS | Comparativa del periodo, anualizada suponiendo que todo el año se comporta como el periodo facturado, con los precios de esa factura | Falta la anualización real |
| **C · Solo SIPS** | SIPS sin factura | **Coste con nuestra oferta** para su consumo real; no se puede afirmar ahorro | No hay precio actual que comparar |

En el modo C, pide los datos principales del potencial cliente (titular, CIF/NIF, CUPS, tarifa de acceso, potencias, distribuidora y, si lo sabe, producto y precio actuales) antes de calcular. El informe se presenta como «lo que pagarías con nosotros», nunca como ahorro.

## Paso 3 · Elegir el producto y comparar

1. Mismo CUPS, mismas potencias, mismo periodo, mismo consumo. Solo cambia el precio.
2. Compara con **el producto propio del titular** y, si procede, con el alternativo de su gama. Como máximo dos escenarios, o el informe deja de ser una recomendación.
3. Calcula TE y TP por periodo, no en bloque.
4. **No toques las potencias** salvo que el cliente lo pida expresamente. Si detectas sobredimensionamiento, dilo en una línea y ofrece revisarlo aparte.
5. Excesos de potencia (medida tipo 4) sin tolerancia automática: `Σ max(Pd − Pc, 0) × días × tep`.
6. Fórmulas, tep y casos por tarifa en `references/formulas.md`.

## Paso 4 · Separar hecho, supuesto y proyección

- **[DATO REAL]**: lo que dice la factura o el catálogo, con fecha.
- **[SUPUESTO]**: lo que se extrapola (reparto de periodos, consumo anual, precio futuro del autoconsumo). Se declara y se justifica por qué es conservador.
- **[PROYECCIÓN]**: la cifra anual. Se etiqueta siempre como «proyección orientativa / 12 recibos equivalentes», nunca como histórico.

Cuando haya dos escenarios, la **cifra grande del informe es la conservadora**: la que se sostiene solo con lo acreditado. El escenario favorable se muestra, pero etiquetado.

## Paso 4 bis · Enfoque comercial: el informe vende, no disuade

El informe es una **herramienta comercial de captación**. Su objetivo es que el cliente contrate con B&M. La honestidad está en los números, no en desanimar al cliente.

- **Nunca** escribas en el informe que el cliente no debe cambiar a Iberdrola, que «mejor no mover» un suministro o que «no sale a cuenta» contratar sin ofrecer inmediatamente la vía para que sí lo haga.
- Si un producto concreto no le conviene, **no es un no**: es una palanca. Redacta en positivo y con salida:
  - Energía: «aquí está tu ahorro de X €».
  - Potencia mal dimensionada: «aquí hay X €/año adicionales; lo ajustamos nosotros».
  - Suministros secundarios que hoy no mejoran: «los estudiamos en conjunto con el principal, porque juntos cambia la negociación».
  - Autoconsumo, reactiva, excesos: cada una es una línea de trabajo nuestra, no una razón para no contratar.
- Cada página termina en una acción que B&M puede ejecutar. Si una sección no tiene acción comercial posible, se reescribe o se elimina.
- Los números no se tocan: se cambia el marco. Un ahorro del 20 % se presenta como 1.997,17 € al año en la cuenta del cliente, no como «solo un 20 %».
- La cifra que manda es la **conservadora y verificable**; se puede añadir el escenario favorable, nunca sustituirla.

## Paso 5 · Escribir el informe

Contenido mínimo: portada con el ahorro en grande, verificación del recibo, comparativa por concepto, proyección anual con supuestos a la vista, y una página de propuesta con condiciones y calendario. Para la maquetación, sigue la skill `maquetacion-documentos-bm`.

Tono: comercial pero factual. Sin emojis. Nada de «subida» para describir una diferencia entre estructuras de precio distintas: se llama diferencia de tarifas.

## Paso 6 · Verificar antes de entregar

Ejecuta `scripts/pdf_qa.py` sobre el PDF y **abre el documento y revísalo a la vista**: los pies de página pueden desaparecer aunque el número de páginas sea correcto. Checklist en `references/checklist_final.md`. Comprueba además: fecha de la hoja de precios vigente, modo de informe declarado (A, B o C) y ausencia de afirmaciones de ahorro cuando solo hay SIPS. Si algo falla, no se entrega.

## Errores que ya hemos cometido y no se repiten

Ver `references/errores_conocidos.md`. Los cinco que más caro salen: potencias cambiadas sin pedirlo, tolerancia del 5 % en excesos, descuentos aplicados dos veces, precios de una hoja caducada y argumentos de venta sin datos.

## Recursos

- `references/formulas.md`: cálculo por tarifa, tep, excesos, reactiva, autoconsumo.
- `references/escenarios_de_datos.md`: modos A/B/C, qué pedir en cada caso, aviso de vigencia de precios y coherencia entre fuentes.
- `references/plantilla_recepcion.md`: mensajes tipo para pedir factura y SIPS, y para justificar la limitación cuando solo hay uno.
- `references/reglas_comerciales.md`: gamas, productos y qué se puede ofrecer a cada titular.
- `references/checklist_final.md`: verificación de 8 puntos.
- `references/errores_conocidos.md`: registro de fallos y su corrección.
- `scripts/calc_energia.py`: calculadora determinista de factura y comparativa.
- `scripts/pdf_qa.py`: control de tamaño de página y de integridad del PDF.
- `assets/informe_base.html`: plantilla de informe a cuatro páginas.


---

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


---

# Mensaje tipo para pedir la documentación

## Primer contacto (pedir todo a la vez)

> Hola [nombre]:
>
> Para hacerte el informe de ahorro con números reales necesito dos cosas:
>
> 1. **Las facturas completas** (todas las páginas, no solo el resumen) de los últimos recibos.
> 2. **El SIPS**, que es el fichero de consumos horarios que puedes descargar de la web o la app de tu distribuidora, o pedir a tu comercializadora. Tarda un minuto y es lo que me permite calcular tu ahorro con tu consumo real, hora a hora.
>
> Con las dos cosas te digo exactamente cuánto ahorras. Con una sola también puedo trabajar, pero con una limitación que te explico abajo.
>
> Si no encuentras el SIPS, dímelo y seguimos solo con la factura.

## Si solo hay factura (modo B)

> Con la factura puedo calcular tu ahorro, pero **la cifra anual es una proyección**: supongo que todos los meses te comportas como el mes facturado. Si tu consumo cambia mucho entre invierno y verano, el número se moverá. Con el SIPS lo clavo.

## Si solo hay SIPS (modo C)

> Con tus consumos reales te puedo decir **exactamente lo que pagarías con nuestra tarifa**. Lo que no puedo decirte todavía es cuánto ahorras, porque para eso necesito ver el precio que pagas ahora. ¿Me pasas una factura? Con ella cierro la comparativa.
>
> Mientras tanto, necesito estos datos para prepararte la propuesta:
> - Titular y CIF o NIF
> - CUPS y dirección del suministro
> - Tarifa de acceso y potencias contratadas
> - Distribuidora
> - Comercializadora y producto actuales, si los sabes
> - Si tienes permanencia y hasta cuándo

## Recordatorio de precios (cuando toque, no cada día)

> Nota interna: el informe está calculado con la hoja de precios del [fecha]. Los precios se actualizan cada semana o cada mes: si ha salido una nueva, mándamela y recalculo el informe entero antes de enviarlo.


---

# Checklist final antes de enviar un informe

0. **La hoja de precios es la vigente y su fecha consta en el documento.** Si la carga tiene más de 30 días, se ha pedido confirmación; entre 7 y 30, se ha avisado.
1. La factura de origen se reproduce **al céntimo** (base IEE → IEE → base IVA → IVA → total). Si no hay factura (modo C), consta expresamente que no se puede afirmar ahorro.
2. El producto comparado es válido para el documento del titular (CIF o NIF).
3. La hoja de precios está citada en el informe con su fecha.
4. Las potencias del cliente no se han modificado (o consta la petición expresa).
5. Ningún descuento está aplicado dos veces ni sumado sobre un precio que ya lo incluye.
6. Cada cifra está clasificada como dato real, supuesto o proyección; la cifra grande es la conservadora.
7. El **modo de informe está declarado** en la primera página: A (factura + SIPS), B (solo factura) o C (solo SIPS), con su limitación.
8. El PDF tiene el número de páginas previsto, tamaño A4 y **los pies de página visibles** (revisión a la vista, no solo por número de páginas).
9. Firma, contacto y aviso de vigencia de la oferta correctos; sin emojis; sin promesas no acreditadas.