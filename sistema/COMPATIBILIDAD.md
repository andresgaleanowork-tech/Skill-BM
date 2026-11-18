# En qué plataformas funciona este paquete

Fecha: 21/07/2026 · Autor: Andrés Galeano (NIE Z0002918W)

Respuesta corta: **sí, funciona en ChatGPT, Claude, Gemini y Codex**, porque el paquete está escrito en el formato abierto *Agent Skills* (`SKILL.md` + `references/` + `scripts/` + `assets/`), que desde diciembre de 2025 leen más de cuarenta productos. Pero cada plataforma lo carga a su manera y **no en todas se ejecuta el código**.

---

## Lo que viaja igual a todas partes

Esto es el 90 % del valor y no depende de la plataforma:

- Las **siete skills** con sus reglas: informes, presupuestos, servicios, actas, maquetación, facturas y precios.
- Las **plantillas** HTML de informe, presupuesto y acta.
- La **bitácora** de errores conocidos.

Son archivos de texto. Se pegan o se adjuntan, y funcionan.

## Lo que cambia en cada plataforma

| Plataforma | Cómo se instala | Límite práctico | ¿Ejecuta `calc_energia.py`? |
|---|---|---|---|
| **ChatGPT · Proyecto** | Pegar instrucciones + subir los 10 `.md` como conocimiento | 8.000 caracteres de instrucciones · 10 archivos, 50 MB | Solo con análisis de datos activado |
| **ChatGPT · Custom GPT** | Igual, en el GPT Builder | 8.000 caracteres · 20 archivos de 512 MB | Solo con análisis de datos activado |
| **Claude · Proyecto** | Instrucciones + archivos del proyecto | Sin tope duro de caracteres (compite con el contexto) | Sí, con análisis de datos activado |
| **Claude.ai · Skills** | ZIP con la carpeta `nombre-skill/SKILL.md` en Customize → Skills | Varias skills conviviendo | Sí, con ejecución de código activada |
| **Claude Code** | Copiar la carpeta a `~/.claude/skills/` | Sin límite | Sí, ejecuta scripts de verdad |
| **Codex (OpenAI)** | Copiar a `~/.agents/skills/` | Sin límite | Sí |
| **Gemini · Gems** | Pegar instrucciones cortas + adjuntar los `.md` | ~4.000 caracteres (recomiendan 500–2.000) | No |
| **Copilot / Cursor / VS Code** | Leen `.github/skills/`, `.claude/skills/` o `.agents/skills/` del repositorio | Depende del producto | Depende del producto |

## El problema real: dónde no se ejecuta el código

`calc_energia.py` es la garantía de que las cuentas salen al céntimo, y desde hoy **se niega a calcular mal**: valida periodos, unidades, potencias y consumos, y si se le declara el total impreso en la factura del cliente, no devuelve cifras cuando no cuadra. Donde no hay ejecución de código, el asistente **calcula a mano** siguiendo el protocolo obligatorio de `02_formulas.md` §11 (céntimos enteros, una línea por periodo, doble suma). Ahí sí aparecen errores de redondeo, y por eso el caso de control es obligatorio, no opcional.

**Mitigación ya incluida:** las instrucciones llevan un **caso de control** con cifras conocidas. Si el asistente, en una plataforma sin código, no llega a estas cifras, ha calculado mal y hay que avisarle:

| Control | Valor |
|---|---|
| Factura de origen (Nagini, octubre 2026) | **836,27 €** |
| Mismo mes con Empresa Flex 3.0TD | **638,88 €** |
| Ahorro del mes | **197,39 €** (23,6 %) |

Es la misma comprobación que hace la batería de pruebas en local, que ya son **diez casos: cinco de cálculo correcto y cinco negativos** que comprueban que la calculadora rechaza lo que debe rechazar.

## Instrucciones cortas para plataformas con tope

ChatGPT permite 8.000 caracteres; Gemini, unos 4.000. Para esos casos existe `instrucciones/INSTRUCCIONES_CORTAS.txt`: **4.015 caracteres** con las doce reglas irrenunciables, sin tablas ni ejemplos. Es el mínimo que no se puede recortar sin perder calidad: si se cae la regla 2 (cuadrar la factura) o la 3 (CIF/NIF), el informe deja de ser fiable.

## Lectura de documentos: cada plataforma aporta su OCR

Las tres plataformas principales ya leen imágenes y PDF escaneados, así que el paquete **no necesita
instalar nada** para las facturas que llegan como foto:

| Plataforma | Cómo se le pasa la factura escaneada | Qué se le pide |
|---|---|---|
| ChatGPT | adjuntar la imagen o el PDF y activar análisis de datos | los datos en el JSON de `calc_energia.py` |
| Claude | adjuntar; con análisis de datos activado, además ejecuta el cálculo | lo mismo, y el cálculo lo hace él |
| Gemini | adjuntar la imagen | los datos y el total impreso, para cuadrar |

**La regla que no cambia:** el OCR propone cifras, no las valida. Ninguna cifra se da por buena hasta
que la suma cuadre contra el total impreso en la factura. Si no cuadra, no hay informe. Esa comprobación
es la que convierte un OCR en una herramienta fiable, y vive en `calc_energia.py` (o en el método a mano
de `02_formulas.md` §11 cuando no hay código).

Para uso local o en lote: `tesseract` sobre el PDF (`pdftoppm -r 300` → `tesseract -l spa`) y volver a
pasar el texto por `tools/factura_a_json.py`. Merece la pena si llegan muchas; para una suelta, no.

## Qué NO viaja

- **Datos de clientes.** Facturas, NIF y expedientes se quedan en tu bandeja, no dentro del paquete.
- **`precios.json`.** Los precios son de tu cuenta de Iberdrola: se cargan a mano en cada entorno. Un precio dentro del paquete caduca y además es información del área restringida.
- **La batería de pruebas** (`eval/run.py`), que necesita Python y una carpeta local.

## Recomendación

| Uso | Dónde |
|---|---|
| Día a día con facturas y PDFs | **ChatGPT · Proyecto** (o Custom GPT si lo comparte el equipo) |
| Cálculos que deben cuadrar siempre, con scripts | **Claude Code** o **Codex**, donde el código corre de verdad |
| Compañeros que solo necesitan redactar | Instrucciones cortas + los `.md` adjuntos, en la plataforma que usen |
| Consulta rápida desde el móvil | Custom GPT o Gem con las instrucciones cortas |

## Mantenimiento

Hay **una sola fuente de verdad** (`skills/`) y dos artefactos generados:

```bash
python tools/generar_paquete_chatgpt.py    # reconstruye los 10 .md + plantillas + ZIP
python eval/run.py                          # verifica que nada se ha roto
```

Las instrucciones largas y cortas se editan a mano porque son texto de criterio, no contenido derivado. Si cambia una regla, se cambia en las tres: `skills/`, instrucciones del Proyecto e instrucciones cortas.