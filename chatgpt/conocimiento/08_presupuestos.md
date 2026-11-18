# Presupuestos · B&M


---

---
name: presupuestos-bm
description: >
  Redacta presupuestos de B&M Asesores Energéticos (instalaciones, cargadores de
  vehículo eléctrico, autoconsumo, mantenimiento, contratos técnicos) con la misma
  identidad visual y la misma dinámica comercial que los informes de ahorro. Usar
  cuando se pida un presupuesto, una oferta, un precio de instalación, una
  comparativa frente a otra oferta recibida o la conversión de una visita técnica
  en documento para el cliente.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Presupuestos B&M

Mismo estilo que los informes de ahorro, misma dinámica comercial y el mismo cuidado con los números: **el documento existe para que el cliente diga que sí**, sin que ninguna cifra le dé motivos para desconfiar.

## Presupuestos ajenos: pasar a estilo B&M

Cuando llega una oferta de la competencia o un presupuesto antiguo nuestro, el trabajo es doble: extraer las partidas y **rehacerlo con el estilo y la dinámica comercial de B&M**, comparando con el mismo alcance y con IVA. Nunca se copia el documento ajeno tal cual ni se cambia un precio sin decirlo.

## Regla de oro

Un presupuesto no es una lista de precios: es una oferta cerrada. Todo lo que el cliente necesita para decidir tiene que estar dentro del documento: qué se instala, qué no se incluye, cuánto cuesta, cómo se paga, hasta cuándo vale y qué pasa si el recorrido no es el previsto.

## Estructura (una página, o dos si hay muchas partidas)

1. **Cabecera**: logo B&M, datos fiscales de B&M (Av. Ribera, 8 bajo · 46500 Puerto de Sagunto · 962 674 769 · canalpymes@bmae.es) y logo de Iberdrola solo si el producto lo justifica.
2. **Título del trabajo** en versalitas + la palabra «Presupuesto» como título grande.
3. **Tabla de datos**: nº de oferta, fecha, cliente, NIF/CIF, emplazamiento, contacto.
4. **Descripción y alcance**: equipo concreto (marca y modelo), tipo de instalación, qué incluye en una línea, y las condiciones de viabilidad (suministro y potencia disponibles, recorrido viable, acceso normal).
5. **Desglose económico sin IVA**: partidas numeradas, base imponible, IVA y **total** destacado en verde.
6. **Condiciones de la oferta**: desplazamiento incluido y cómo se valora el exceso, qué no incluye, validez, forma de pago, y el aviso de que la puesta en servicio queda sujeta a comprobaciones de seguridad.
7. **Pie legal** y footer con Andrés Galeano y el número de oferta.

Detalle milimétrico en `references/estructura.md`. Plantilla lista en `assets/presupuesto_base.html`.

## Numeración y datos

- Formato de oferta: `BM-00029` (correlativo de B&M).
- Fecha en formato `DD/MM/AAAA`.
- Validez por defecto: **30 días** salvo indicación expresa.
- Desplazamiento incluido: hasta 40 km de ida desde Puerto de Sagunto; el exceso se valora según tabla interna.
- Nada de precios redondos inventados: cada partida sale del coste real (equipo, material, mano de obra, legalización).
- **Instalación y tramitación van en líneas separadas**: ejecución por un lado y boletín, expediente de Iberdrola o legalización por otro. El alcance de cada servicio está en la skill `servicios-bm`; las tasas y derechos se identifican aparte y los plazos se separan entre tramitación propia y respuesta de terceros.

## Dinámica comercial

- **Lo que ahorra o aporta el cliente va primero**, igual que en los informes de ahorro: si el presupuesto sustituye a una oferta de la competencia, se abre con la comparativa (nuestra cifra frente a la suya, con lo que incluye cada una).
- **Los opcionales se valoran aparte**, nunca escondidos en el total. Si algo es obligatorio por legalización, se dice y se incluye.
- Se distingue siempre lo incluido de lo no incluido: obra civil, altas de suministro, tasas, honorarios de OCA y modificaciones generales no entran salvo que figuren valoradas.
- Si el cliente aporta otra oferta, se compara **con IVA y con el mismo alcance**. Si nos falta algo que el otro incluye, se iguala antes de comparar precios.
- El documento no se cierra con un «no»: si una partida no encaja, se ofrece alternativa, no negativa.

## Nunca

- Inventar equipos, modelos, potencias, plazos, legalizaciones ni precios.
- Presentar como incluido algo que depende de una visita o de un trámite.
- Prometer fechas de ejecución que dependan de terceros (distribuidora, Industria, OCA).
- Omitir el IVA o enseñar un total sin impuestos como si fuera el precio final.

## Verificación antes de enviar

1. Aritmética: las partidas suman la base imponible; IVA al 21 % (o IGIC/IPSI si corresponde); total correcto al céntimo.
2. Nº de oferta, fecha, cliente y NIF correctos.
3. Alcance y exclusiones coinciden con lo hablado en la visita.
4. Validez y forma de pago explícitas.
5. Revisión a la vista del PDF: página completa, sin cortes, con pie visible.

## Recursos

- `references/estructura.md`: bloques, textos legales y partidas tipo por especialidad.
- `assets/presupuesto_base.html`: plantilla con la identidad de B&M.
- Skill `servicios-bm`: alcance, documentación y exclusiones de boletines, expedientes y legalizaciones.


---

# Estructura y textos tipo

## Bloques y orden

| # | Bloque | Contenido |
|---|---|---|
| 1 | Cabecera | Logo B&M a la izquierda; razón social, dirección, teléfono y correo a la derecha |
| 2 | Título | Especialidad en versalitas (p. ej. «SUMINISTRO E INSTALACIÓN DE PUNTO DE RECARGA PARA VEHÍCULO ELÉCTRICO») y «Presupuesto» en grande |
| 3 | Datos | Nº de oferta · Fecha · Cliente · NIF/CIF · Emplazamiento · Contacto |
| 4 | Descripción y alcance | Equipo (marca y modelo), tipo de instalación, qué incluye, condiciones de viabilidad |
| 5 | Desglose económico | Partidas + base imponible + IVA + total |
| 6 | Condiciones | Desplazamiento, exclusiones, legalización, validez, pago, seguridad |
| 7 | Pie legal y firma | Aviso de documento sin validez contractual hasta aceptación; contacto |

## Textos tipo

**Descripción y alcance**
> [Equipo, marca y modelo] · [potencia] [monofásico/trifásico].
> Instalación en [emplazamiento] · hasta [X] m incluidos.
> Incluye equipo, [control dinámico], línea y canalización superficial, protecciones, montaje, pruebas y puesta en servicio.
> Sujeto a suministro y potencia disponibles, recorrido viable y condiciones de acceso normales.

**Condiciones de la oferta**
- Incluye desplazamiento hasta 40 km de ida desde Puerto de Sagunto. El exceso se valora según tabla interna.
- No incluye obra civil, altas de suministro, modificaciones generales de la instalación ni medios especiales.
- Legalización incluida solamente cuando figure valorada expresamente en el desglose.
- Instalaciones técnicamente especiales y modificaciones de alcance se presupuestarán aparte.
- Validez de la oferta: 30 días salvo indicación expresa. Importes sujetos a verificación del recorrido.
- Pago según condiciones acordadas por escrito. La puesta en servicio queda sujeta a comprobaciones de seguridad.

**Pie legal**
> B&M ASESORES ENERGÉTICOS, S.L. · Oferta sujeta a aceptación del cliente. Documento sin validez contractual hasta firma o confirmación escrita.

## Partidas tipo por especialidad

**Punto de recarga VE**
Equipo + instalación base · Metros adicionales de recorrido · Suplemento por dificultad · Desplazamiento adicional · Documentación y legalización (opcional) · Trabajos adicionales.

**Autoconsumo FV**
Módulos (marca, modelo y potencia) · Estructura · Inversor · Protecciones DC y AC · Cableado · Monitorización · Batería (si procede) · Proyecto y legalización · Mano de obra y desplazamiento.

**Mantenimiento / contrato técnico**
Visitas anuales · Alcance de cada visita · Urgencias y su tarifa · Materiales incluidos · Renovación.

## Comparativa frente a otra oferta

Cuando el cliente aporta un presupuesto de la competencia, la tabla se hace **con IVA y con el mismo alcance**, y se marca la fila ganadora. Si el otro incluye algo que nosotros no, se iguala antes de comparar; si nosotros incluimos algo que el otro no (una batería, una monitorización, la legalización), se resalta en una columna propia.