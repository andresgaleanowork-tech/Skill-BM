---
name: servicios-bm
description: >
  Describe y presupuesta los servicios técnicos y documentales de B&M Asesores
  Energéticos: boletines eléctricos, expedientes de Iberdrola, legalizaciones,
  altas y modificaciones de suministro, y la gestión e instalación asociada. Usar
  cuando se pregunte qué servicios ofrece B&M, qué incluye un boletín o un
  expediente, qué documentación hace falta para legalizar una instalación, o cómo
  se presupuesta la tramitación además de la instalación.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Servicios de B&M: boletines, expedientes y legalizaciones

Además del suministro de energía y de las instalaciones, B&M **tramita la documentación** que hace falta para que la instalación funcione legalmente y para que Iberdrola la reconozca. Es un servicio que se cobra aparte de la instalación y que casi ningún competidor explica con claridad.

## Regla de oro

**Los precios y los plazos dependen de la instalación, de la comunidad autónoma y del estado del expediente.** No se inventan: se piden los datos de la instalación y, si no se pueden cerrar, se presupuesta en dos tramos: «tramitación incluida» o «sujeta a valoración tras revisión del expediente».

## Servicios del catálogo

### 1. Boletín eléctrico (certificado de instalación)

Documento que emite un instalador autorizado y que certifica que la instalación cumple el Reglamento Electrotécnico de Baja Tensión.

- **Qué incluye B&M**: visita y comprobación de la instalación, mediciones (aislamiento, tierra, continuidad), cumplimentación del boletín, registro ante el órgano competente de la comunidad autónoma y entrega del certificado al cliente y a la distribuidora.
- **Qué necesita**: datos del titular, CUPS, potencia, superficie, uso del local y croquis o esquema unifilar si existe.
- **Qué no incluye** (salvo que se valore): corrección de defectos detectados, obra civil, adecuación de cuadros, sustitución de protecciones.

### 2. Expediente de Iberdrola (alta, modificación o legalización)

Gestión completa ante la distribuidora y el comercializador para que el punto de suministro quede reflejado con la potencia y las condiciones correctas.

- **Qué incluye**: apertura del expediente, presentación de documentación (boletín, contrato de acceso, permiso de obra o licencia cuando se exige), seguimiento con la distribuidora, respuesta a requerimientos y cierre del expediente con el nuevo contrato de acceso.
- **Qué necesita**: boletín en vigor, potencias solicitadas, CUPS, datos del titular y, en su caso, licencia de actividad o certificado de eficiencia energética.
- **Qué no incluye**: tasas y derechos de la administración, inspecciones de OCA, obra civil.

### 3. Legalizaciones y altas

- Legalización de instalaciones nuevas o reformadas.
- Altas de suministro y reactivaciones.
- Modificaciones de potencia, cambio de tarifa de acceso, cambio de titular.
- Regularización de instalaciones sin boletín en vigor.

### 4. Gestión e instalación asociada

B&M puede ejecutar la instalación que el expediente necesita (cuadros, protecciones, líneas, puntos de recarga, autoconsumo) y tramitar su legalización en el mismo encargo. Cuando la instalación la hace un tercero, B&M puede limitarse a la tramitación.

## Cómo se presupuesta

1. **Separar siempre dos líneas**: ejecución de la instalación y tramitación documental. Si se presenta todo junto, el cliente no entiende qué está pagando.
2. **La tramitación depende del alcance**: no cuesta lo mismo un boletín de una vivienda que la legalización de una nave con inspección de OCA.
3. **Tasas y derechos** se presentan como «a cargo del cliente» o repercutidos con su justificante, nunca como margen oculto.
4. **Plazos**: se da un plazo de **tramitación** y otro de **respuesta de la administración o de la distribuidora**, que no depende de B&M. Nunca se garantiza la fecha de resolución.
5. Si el expediente llega con defectos, se documenta y se presupuesta su corrección aparte.

## Qué documentos se usan

- **Presupuesto** para valorar la instalación y la tramitación (skill `presupuestos-bm`).
- **Contrato** cuando se trata de mantenimiento o de un servicio recurrente.
- **Acta de entrega** cuando se entrega al cliente documentación, boletín o expediente cerrado (skill `actas-entrega-bm`).
- **Informe de ahorro** cuando el servicio incluye además optimización de la tarifa (skill `informes-ahorro-electrico`).

## Lo que no se hace

- Prometer que la legalización «sale seguro» sin revisar la instalación.
- Presentar el boletín como un trámite automático: si la instalación no cumple, no hay boletín.
- Dar por cerrado un expediente sin la confirmación de la distribuidora.
- Incluir en el precio las tasas sin identificarlas.

## Recursos

- `references/servicios.md`: descripción larga de cada servicio, documentación necesaria y exclusiones.
- `references/textos_comerciales.md`: cómo explicar cada servicio al cliente en dos o tres frases.
