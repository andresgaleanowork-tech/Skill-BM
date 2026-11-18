# Maquetación de documentos · B&M


---

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


---

# Estilos y trampas de maquetación

## Variables

```
navy        #173d6d
verde       #00a651
verde text  #00894d
rojo        #c04048
fondo kpi   #f0f5f8 / #edf8f1 (verde)
aviso       #fff3e0
nota        #f1f5f8
```

## Tamaños que funcionan (medidos en A4 con 12 mm de margen)

| Elemento | Medida |
|---|---|
| Gráfico de barras apiladas | 7,9 × 1,58 in |
| Gráfico de escenarios | 7,9 × 1,72 in |
| Gráfico de precios por periodo | 7,2 × 1,30 in |
| Bloque hero | valor 46 px, 4 mm de padding |
| Tabla normal | 9,8 px, padding 1,75 mm |
| Tabla compacta | 9,2 px, padding 1,2 mm |
| Cuerpo de texto | 10,4 px, interlineado 1,33 |

## Trampas

1. **Leyenda dentro del gráfico**: en gráficos bajos se solapa con las etiquetas de valor. Colocarla arriba con `bbox_to_anchor=(.5, 1.18)` y subir el `ylim`.
2. **`height` fija en la página**: si el contenido no cabe, el pie se desplaza. Es la causa número uno de páginas en blanco.
3. **Gráficos SVG sin `bbox_inches='tight'`**: dejan márgenes invisibles que rompen la alineación con las tablas.
4. **Tabla que se corta**: pasar la última columna a la fila de totales o mover la tabla a la página siguiente, nunca reducir el cuerpo por debajo de 9 px.
5. **Logo**: usar el PNG en base64 embebido; con rutas externas el preview no lo carga y el PDF depende del sistema de archivos.

## Los logos: dónde están y cómo se usan

Los dos logos viven en esta skill, en `assets/logos/`:

| Archivo | Qué es | Uso |
|---|---|---|
| `bm.png` | logotipo completo B&M Asesores Energéticos, 1075×330 | cabecera de todos los documentos |
| `bm_compacto.jpg` | versión reducida, 260×79 | cuando la cabecera va muy justa de alto |
| `iberdrola.jpg` | logotipo Iberdrola, 1200×296 | cabecera derecha de informes y presupuestos |

**Regla de marca:** las **actas llevan solo el logo de B&M**. Nunca se deja el hueco del otro.

### Cómo se incrustan

Nunca se pegan a mano: las plantillas llevan los marcadores `{{LOGO_BM}}` y `{{LOGO_IB}}` y se
rellenan con un comando, que además los incrusta en base64 para que el HTML resultante sea **un solo
archivo** que se puede enviar por correo o convertir a PDF sin depender de carpetas:

```bash
python tools/rellenar_plantilla.py --tipo informe --datos datos.json --salida /tmp/informe.html
python tools/rellenar_plantilla.py --tipo acta --datos datos.json --salida /tmp/acta.html
```

En un acta el logo de Iberdrola se retira automáticamente, sin dejar hueco.

### En cada plataforma

| Plataforma | Qué hacer con los logos |
|---|---|
| **ChatGPT · Proyecto** | subirlos como archivos del Proyecto; los nombres son `logo_bm.png` y `logo_iberdrola.jpg` |
| **ChatGPT · Custom GPT** | subirlos también como Knowledge |
| **Claude · Proyecto** | adjuntarlos en el proyecto junto a las plantillas |
| **Claude Code / Codex** | ya están dentro de `skills/…/assets/logos/`, no hay que hacer nada |
| **Gemini y plataformas sin archivos adjuntos** | el asistente **no puede incrustar imágenes** en el HTML: genera el documento con el hueco reservado y se pega el logo al exportar. Que lo diga, no que devuelva el marcador a la vista |

Si en una plataforma no se pueden subir los logos, el asistente **no inventa** ni escribe el nombre de
la empresa como sustituto del logotipo: deja la cabecera preparada y lo advierte.