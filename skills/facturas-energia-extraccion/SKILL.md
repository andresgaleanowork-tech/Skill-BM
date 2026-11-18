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
