# Viabilidad de convertir este flujo en Skills · B&M Asesores Energéticos

Fecha: 21/07/2026 · Autor: Andrés Galeano (canalpymes@bmae.es)

---

## 1. Qué es una Skill, en una frase

Una **Skill** es una carpeta con un archivo `SKILL.md` que contiene:

- **Frontmatter** (metadatos): `name` y `description`. Es lo único que el asistente ve al arrancar, y decide si la skill se activa o no.
- **Cuerpo**: instrucciones en Markdown, en pasos.
- **Carpetas opcionales**: `scripts/` (código que se ejecuta sin cargarse entero en contexto), `references/` (documentación que se lee solo cuando hace falta), `assets/` (plantillas, logos, CSS).

La idea clave: el conocimiento pesado **no ocupa contexto hasta que se usa**. Eso es exactamente lo que necesita un flujo como el nuestro, donde el 90 % del texto son reglas que solo aplican en el momento del cálculo.

---

## 2. Veredicto: viable, y con una condición

| Bloque de conocimiento | ¿Se puede encapsular? | Comentario |
|---|---|---|
| Reglas comerciales (CIF vs NIF, gama Empresa, planes elegibles) | **Sí, alto valor** | Texto puro, estable, es donde más errores se cometen |
| Metodología de cálculo (TE/TP, excesos, reactiva, IEE, IVA, autoconsumo) | **Sí, alto valor** | Incluye las fórmulas y el orden de operaciones |
| Verificación al céntimo (cuadrar la factura original) | **Sí, alto valor** | Es el sello de calidad del informe; debe ser paso obligatorio |
| Maquetación (CSS, navy #173d6d, verde #00a651, logos, pies, tarjetas KPI) | **Sí, como `assets/` + checklist** | El CSS y los logos viajan en la carpeta |
| Generadores (`Scripts/build_*.py`) | **Sí, como `scripts/`** | Se ejecutan; no hace falta leerlos |
| Catálogo de precios vigente | **Parcial** | Caduca. La skill debe **exigir** verificar la hoja del día antes de calcular |
| Facturas y datos de clientes | **No** | Datos personales y ficheros pesados: se quedan fuera de la skill |
| Dependencias (weasyprint, pymupdf, matplotlib) | **No** | Se instalan en el entorno, la skill solo puede recordar el comando |

**La condición:** una skill no es un chat con memoria. Es un **manual de procedimiento**. Si esperas que además recuerde conversaciones o el estado de cada cliente, eso no lo hace; para eso está el workspace y los JSON de cálculo (`revision_*/calc.json`).

---

## 3. La decisión importante: no una skill, cuatro

Una sola skill gigante falla por dos motivos: la descripción se vuelve ambigua y acaba activándose en tareas donde no toca, o no activándose en la que toca. El estándar premia skills pequeñas con **descripciones disjuntas**.

### Skill 1 · `informes-ahorro-electrico` (la más valiosa)
- **Cuándo se activa:** «informe de ahorro», «comparativa de tarifa», «¿merece la pena cambiar de comercializadora?», «cuánto ahorra este cliente».
- **Contenido:** reglas CIF/NIF, elección de producto, cálculo de TE/TP por periodo, excesos sin tolerancia del 5 %, reactiva, IEE/IVA, autoconsumo y compensación, separación **[DATO REAL] / supuesto / proyección**, verificación al céntimo de la factura de origen.
- **`references/`:** `reglas_comerciales.md`, `formulas.md`, `casos_por_tarifa.md` (2.0TD, 3.0TD, 6.1TD), `errores_conocidos.md` (los que ya hemos corregido: pies que desaparecen, potencias que no se tocan, argumento de «subida» sin datos…).
- **`scripts/`:** `pdf_qa.py`, `calc_energia.py`.

### Skill 2 · `maquetacion-documentos-bm`
- **Cuándo se activa:** cualquier entregable con marca B&M (informe, presupuesto, contrato, acta).
- **Contenido:** identidad visual, estructura de página, tono, firma, sin emojis, regla del logo único cuando se pide «solo B&M», QA visual obligatorio.
- **`assets/`:** `logos/`, `estilos.css`, plantillas HTML base.

### Skill 3 · `facturas-energia-extraccion`
- **Cuándo se activa:** «lee esta factura», «saca los datos de este PDF», «cuadra esta factura».
- **Contenido:** lectura de PDF con o sin capa de texto, reconstrucción de IEE/IVA, detección de anomalías (reactiva, excesos, autoconsumo, regularizaciones), devolución de JSON normalizado.
- **`scripts/`:** extractor y validador de cuadre.

### Skill 4 · `precios-iberdrola`
- **Cuándo se activa:** «precios», «hoja de precios», «¿cuánto está Flex?», «actualiza el catálogo».
- **Contenido:** cómo localizar el producto correcto en la hoja de 12 páginas, regla de vigencia y fecha, plantilla de resumen, aviso de productos que caducan.
- **`references/`:** `mapa_de_la_hoja.md` (qué hay en cada página y columna).

---

## 4. Estructura de una skill lista para subir

```
informes-ahorro-electrico/
├── SKILL.md
├── references/
│   ├── reglas_comerciales.md
│   ├── formulas.md
│   └── errores_conocidos.md
├── scripts/
│   ├── calc_energia.py
│   └── pdf_qa.py
└── assets/
    └── plantilla_informe.html
```

Se comprime la carpeta (el ZIP debe contener `nombre-skill/SKILL.md`, no un `SKILL.md` suelto) y se sube en **Customize → Skills**. En Claude Code basta con dejarla en `~/.claude/skills/`.

**Borrador de frontmatter:**

```yaml
---
name: informes-ahorro-electrico
description: >
  Elabora informes de ahorro eléctrico de B&M Asesores Energéticos comparando la
  factura actual del cliente con los productos de Iberdrola (Empresa Flex 3.0TD y
  6.1TD, planes 2.0TD). Usar cuando se pida un informe de ahorro, una comparativa
  de tarifa, valorar un cambio de comercializadora o cuantificar el ahorro de una
  factura de luz, tanto para CIF como para NIF.
---
```

---

## 5. Riesgos y cómo los controlamos

| Riesgo | Control |
|---|---|
| **Precios caducados** (la hoja cambia cada pocas semanas) | La skill no guarda precios como verdad: exige la hoja vigente y la fecha en el pie del informe |
| Descripciones solapadas → se activa la skill equivocada | Una skill = una tarea; frases disparadoras distintas y verificadas |
| Sobreajuste a clientes concretos | Los ejemplos con nombres reales van fuera; dentro, casos genéricos |
| Datos personales | Ninguna factura ni NIF dentro de la skill |
| Exceso de confianza en el cálculo | Paso de verificación al céntimo y checklist final de 8 puntos, obligatorios |
| Dependencias no instaladas | Primer paso: comprobar e instalar `weasyprint`, `pymupdf`, `matplotlib` |

---

## 6. Plan de implantación en tres pasos

1. **Piloto (1 skill).** `informes-ahorro-electrico` con el caso Rafael Tena como prueba de aceptación: debe reproducir 1.997,17 € / 2.368,66 € / 3.854,60 € sin que se le indique nada más.
2. **Segunda (maquetación)**, que es la que evita los retoques de última hora en pies y saltos de página.
3. **Las dos de soporte** (`facturas-energia-extraccion`, `precios-iberdrola`), que se usan en todas las demás.

Coste estimado de los tres pasos: una sesión de trabajo por skill, revisable después de cada informe real.

---

## 7. Lo que sigue abierto

- **«Dividir cursos / glaucode»**: he interpretado que se refiere a *dividir el conocimiento de este chat en bloques* y a **Claude Code** como destino de instalación. Si era otra cosa («cursos» = formación para clientes, «glaucode» = otro producto), dímelo y rehago el punto 3.
- **Nivel de detalle:** puedo escribir las skills para uso interno (con nuestras mañas y excepciones) o para que las use cualquier compañero de B&M sin contexto previo. Son documentos distintos.
