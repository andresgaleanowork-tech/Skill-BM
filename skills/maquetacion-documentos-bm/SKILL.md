---
name: maquetacion-documentos-bm
description: >
  Aplica la identidad visual y la estructura de B&M Asesores Energéticos a
  cualquier entregable: informes de ahorro, presupuestos, contratos y actas en PDF
  o DOCX (informes de ahorro, presupuestos, contratos, actas). Usar siempre que se genere un documento con marca B&M, cuando se pida
  «con los logos», «solo con el logo de B&M», o cuando haya que revisar pies de
  página, saltos de página y formato A4 antes de enviar.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Maquetación de documentos B&M

Un documento de B&M se reconoce por tres cosas: la cabecera con los logos, el bloque verde del dato principal y un pie de página que no se mueve nunca de sitio.

## Identidad

| Elemento | Valor |
|---|---|
| Navy corporativo | `#173d6d` |
| Verde corporativo | `#00a651` (texto y acentos: `#00894d`) |
| Rojo de comparación (tarifa actual) | `#c04048` |
| Papel | A4 vertical, 210 × 297 mm, márgenes 12 mm laterales |
| Tipografía | Arial 10,4 px de cuerpo; títulos navy de 25 px |
| Logos | B&M a la izquierda, Iberdrola a la derecha, 33 × 11 mm, `object-fit: contain` |
| Emojis | Prohibidos |

## Regla del logo

- Por defecto: **B&M + Iberdrola**.
- Si el cliente pide «solo con el logo de B&M» (actas de entrega, seguimiento de presupuestos), se quita el de Iberdrola. Nunca se deja el hueco.

## Dos familias de documento, un solo estilo

| Familia | Extensión | Cierre |
|---|---|---|
| Informe de ahorro | 4 páginas | Propuesta con calendario y ahorro en euros |
| Presupuesto | 1 página (2 si hay muchas partidas) | Total con IVA, condiciones, validez y pie legal |
| Acta de entrega / devolución | 1 página | Elementos, manifestación y doble firma |

Todas comparten cabecera, paleta, tarjetas y tono comercial: el cliente debe reconocer que los documentos vienen de la misma casa. Para presupuestos, sigue `presupuestos-bm`; para actas, `actas-entrega-bm`.

## Firma: el documento lo firma el comercial que lo emite

Andrés Galeano es el referente, pero **cualquier comercial de B&M emite con su nombre**. En los documentos con firma personal (actas, presupuestos) el nombre, teléfono y correo del emisor son variables; el contacto general de la empresa puede acompañar, nunca sustituir al del comercial. No dejes un nombre fijo por defecto.

## Estructura de un informe (4 páginas)

1. El ahorro en grande: cifra conservadora en el bloque verde, tres tarjetas KPI, tabla de qué se compara y cadena de verificación.
2. Verificación del recibo: gráfico de barras apiladas por concepto + tabla concepto a concepto + comparativa de precio por periodo.
3. Proyección anual: gráfico de escenarios, tabla anual, supuestos numerados y aviso de lo que no se afirma.
4. Propuesta: tabla de actuaciones con resultado y condición, nota de precios y bloque de contacto.

## Pies de página: el problema recurrente

Los pies van **posicionados de forma absoluta** dentro de una sección de altura fija (`position:absolute; bottom:8mm`). Si el contenido de una página crece, WeasyPrint parte la sección en dos hojas y el pie aparece pero el contenido se desborda, dejando una página casi vacía con el pie al final.

Reglas:

- No fijar `height` en el contenedor salvo que el contenido esté medido.
- Compactar antes de reducir: gráficos de 1,6 mm de alto efectivo, tablas `tight` con 1,2 mm de padding.
- Si sobra contenido, **quitar una sección**, no encoger la letra.
- Verificar siempre a la vista. Que el PDF tenga 4 páginas no significa que estén bien: un pie puede haberse ido a una quinta hoja.

## Firma y contacto

Andrés Galeano · Comercial Pymes · B&M Asesores Energéticos, S.L.
Colaborador de Iberdrola · 671 681 039 · canalpymes@bmae.es · Oficina 962 674 769 Ext. 5003

## Recursos

- `assets/informe_base.html`: plantilla de cuatro páginas con las ranuras marcadas entre llaves. Sustituir los `{{...}}` y renderizar con WeasyPrint.
- `references/estilos.md`: variables CSS, tamaños de los gráficos y errores de maquetación con su corrección.
