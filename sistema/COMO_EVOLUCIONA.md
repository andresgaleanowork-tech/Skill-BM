# Cómo hacer que el paquete evolucione y sea más eficiente

Fecha: 21/07/2026 · Paquete de skills B&M · Autor: Andrés Galeano (NIE Z0002918W)

El problema de un paquete de instrucciones es que envejece: los precios cambian, aparecen productos nuevos, un informe sale mal y el error no se aprende. Este documento describe **los cuatro mecanismos que ya están construidos** para que mejore solo, y las líneas de trabajo siguientes.

---

## 1. Una sola fuente de verdad (ya hecho)

Antes había dos versiones: las carpetas `skills/` y el paquete de conocimiento de ChatGPT, mantenidas a mano. Eso garantiza que un día digan cosas distintas.

Ahora se edita **solo** `skills/` y se ejecuta:

```bash
python tools/generar_paquete_chatgpt.py
```

Reconstruye los diez documentos de conocimiento, copia las plantillas y los scripts, y regenera `zips/paquete_chatgpt_bm.zip`. Verificado: 71.358 caracteres en 10 archivos.

**Ahorro:** una edición en un sitio, no en dos. Se acabó el «esto lo cambié pero en ChatGPT no».

---

## 2. Carga manual asistida de precios (ya hecho)

El área de precios de Iberdrola está bloqueada para usuarios normales, así que **no hay descarga automática posible**: los precios se copian a mano. Lo que sí se puede automatizar es todo lo de después, que es donde se cuelan los errores.

Se rellena una ficha de texto:

```
3.0TD Empresa Flex | TP: 20,376927 10,617621 4,481534 3,886333 2,513851 1,442287 | TE: 0,253955 0,209968 0,180518 0,157978 0,149284 0,152954
2.0TD Plan Estable | TP: 38,99 38,99 | TE: 0,206533
```

```bash
python tools/cargar_precios.py bandeja/precios/ficha_16112026.txt
python tools/estado_precios.py          # ¿sigue vigente esta carga?
```

La cadencia real es **semanal o mensual**: se carga una vez y se recarga solo cuando cambian los precios. Por eso el control no es un calendario, es la antigüedad de la carga: menos de 7 días se trabaja con normalidad, entre 7 y 30 se avisa antes de un informe importante, y por encima de 30 días no se emite un informe nuevo sin confirmar.

Qué hace el cargador, y por qué ahorra trabajo:

- **Rechaza** líneas incoherentes: seis TP en una tarifa de dos, un TE de menos, una coma mal puesta.
- **Guarda la fecha de la hoja** en `precios.json` y deja una ficha legible en `metricas/precios/`.
- **Avisa si un precio se mueve más de un 25 %** respecto a la carga anterior: casi siempre es un dedazo al copiar, no un cambio real de tarifa.
- Admite solo los productos que se usan: no hay que copiar los 63 de la hoja.

**Ahorro:** la actualización de precios deja de ser un copy-paste sin control y pasa a ser un copy-paste validado.

## 3. Batería de pruebas (ya hecho)

```bash
python eval/run.py
```

Cinco casos, todos en verde ahora mismo:

| Caso | Qué garantiza |
|---|---|
| `RT-OCT` | La factura de Rafael Tena se reproduce al céntimo (836,27 €) y el mismo mes con Flex da 638,88 €, ahorro 197,39 € |
| `RT-POT` | La potencia de Flex coincide con la de la factura (152,68 €) |
| `PRECIOS-FLEX30` | La extracción de Empresa Flex 3.0TD coincide con la hoja vigente |
| `PRECIOS-FLEX61` | Igual para Empresa Flex 6.1TD |
| `PRECIOS-2TD` | La extracción de 2.0TD (un solo periodo de energía) funciona |

**Por qué importa:** cuando cambies una regla, un precio o la fórmula de excesos, el comando te dice en dos segundos si has roto algo. Sin esto, el error aparece en la factura de un cliente.

Cuando cambie la hoja de precios a propósito, se actualiza `eval/casos.json` **conscientemente** y se anota en la bitácora. Un caso que falla y no se actualiza es un aviso, no una molestia.

---

## 4. Bitácora de correcciones (ya hecho)

`metricas/bitacora.md` recoge una línea por aprendizaje: qué pasó y qué se cambió en el paquete. Ya tiene las cinco correcciones reales de esta semana (pies de página, bono social en la base del IEE, «mejor no moverlos», precios caducados y modos A/B/C).

Se alimenta desde la conversación con:

```bash
python tools/registrar_correccion.py "Informe ACME" "Se usó el precio de la hoja anterior" "Regla de vigencia reforzada"
```

Y ese archivo **viaja al paquete de ChatGPT** dentro de `04_errores_conocidos.md`, así que el asistente lee sus propios errores antes de entregar.

**Regla de maduración:** una corrección que se repite tres veces deja de ser un caso y sube a las instrucciones del Proyecto. Así el paquete se afina solo con el uso.

---

## 5. Siguientes líneas de trabajo (no hechas, por orden de rentabilidad)

### a) Normalización automática de lo que llega (hecho en parte)
`tools/normalizar_documento.py` ya saca CIF/NIF/NIE, CUPS, importes, fechas, potencias, consumos y porcentajes de cualquier PDF o TXT que se deje en la bandeja, y avisa si el PDF es un escaneo sin capa de texto. Es la primera mitad del trabajo manual: la otra mitad, convertir eso en el documento con estilo B&M, la hacen las skills.

Lo que falta: **lectura de tablas** con `pdfplumber` para facturas de comercializadoras pequeñas con columnas desordenadas, y OCR opcional (`tesseract`) para los escaneos. Eso convertiría veinte minutos de tecleo en dos de revisión.

### b) Instrucciones del Proyecto generadas por bloques
Hoy las instrucciones son un texto de 7.109 caracteres que se pega a mano. Se pueden generar desde `chatgpt/instrucciones/bloques/*.md` con un script que avise si se pasa de 8.000 caracteres. Ventaja: cambiar una regla no obliga a reescribir todo el bloque.

### c) Registro de informes emitidos
Un índice (`metricas/indices/informes.csv`) con fecha, cliente, producto recomendado, ahorro calculado y si se cerró. Sirve para tres cosas: no repetir un informe ya hecho, medir qué producto convierte mejor y detectar clientes con hoja de precios antigua.

### d) Enlace ligero entre documentos
Hoy el paquete son instrucciones y una calculadora: el asistente hace las cuentas y redacta, pero los PDF los generas aparte. Un MCP propio con tres herramientas —calcular, verificar y renderizar— daría cifras deterministas y PDFs reales sin salir de la conversación. Es la evolución natural, pero exige mantener un servicio: solo tiene sentido si el volumen de informes crece.

### e) Versión y control de cambios
Añadir `\"version\"` en cada `SKILL.md` (ya está en `metadata`) y un `CHANGELOG.md` por skill. Con el tiempo permitirá saber qué versión generó cada informe entregado.

---

## 6. Qué medir para saber si mejora

Sin métricas, «eficiencia» es una sensación. Cuatro números, anotados en `metricas/indices/`:

| Métrica | Objetivo | Cómo se mide |
|---|---|---|
| Tiempo por informe | bajar de 20 min a 10 | hora de recepción de la factura y hora de envío |
| Correcciones tras la primera entrega | tender a 0 | líneas de la bitácora por informe |
| Errores de precio detectados en revisión | 0 | casos que fallan en `eval/run.py` |
| Informes que acaban en contratación | subir | índice de informes emitidos |

---

## Resumen

Ya está construido lo que evita el deterioro: **fuente única**, **extracción automática de precios**, **diez pruebas de aceptación, cinco de ellas negativas** y **bitácora que viaja al asistente**. Lo que falta es lo que aumenta capacidad: lectura de facturas, registro de informes y, si el volumen lo justifica, un conector propio.