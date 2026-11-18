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
