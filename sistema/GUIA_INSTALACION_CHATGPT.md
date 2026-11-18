# Cómo instalar el paquete en ChatGPT

Dos caminos. El **Proyecto** es el recomendado para uso diario; el **Custom GPT** sirve si quieres compartirlo con compañeros de B&M o invocarlo desde el móvil.

---

## Opción A · Proyecto de ChatGPT (recomendado)

1. En ChatGPT, **Proyectos → Nuevo proyecto**. Nombre: `B&M · Informes de ahorro`.
2. Abre las instrucciones del proyecto y pega el contenido de `chatgpt/INSTRUCCIONES_PROYECTO_SOLO_TEXTO.txt` (5.081 caracteres; el campo admite 8.000, te quedan ~2.900 para añadir reglas propias).
3. **Añadir archivos** y sube las siete piezas de `chatgpt/conocimiento/`:
   - `01_proceso_informes.md`
   - `02_formulas.md`
   - `03_reglas_comerciales.md`
   - `04_errores_conocidos.md`
   - `05_maquetacion.md`
   - `06_facturas_extraccion.md`
   - `07_precios_iberdrola.md`
   - `08_presupuestos.md`
   - `09_servicios.md`
   - `10_actas_entrega.md`
   - `LICENSE.md` (autoría y condiciones de uso)
   Los archivos de código (`calc_energia.py`, `pdf_qa.py`, `informe_base.html`) son opcionales: súbelos también si vas a usar el análisis de datos o quieres que replique la plantilla.
4. Abre un chat **dentro del proyecto** y sube la factura del cliente y la hoja de precios vigente. Ya puedes pedir: «informe de ahorro de esta factura comparada con Empresa Flex».

Límites prácticos del Proyecto: instrucciones de 8.000 caracteres y hasta 10 archivos de conocimiento con 50 MB en total (los archivos no consumen el límite de caracteres).

---

## Opción B · Custom GPT (para compartir con el equipo)

1. **Explorar GPTs → Crear un GPT**.
2. Pega el mismo texto de `INSTRUCCIONES_PROYECTO_SOLO_TEXTO.txt` en el campo **Instrucciones** (límite 8.000 caracteres).
3. En **Conocimiento**, sube los siete `.md`. El límite aquí es más generoso: hasta 20 archivos de 512 MB.
4. Activa **Análisis de datos** si quieres que ejecute `calc_energia.py` y genere los documentos.
5. Guarda y comparte solo con el equipo de B&M (no público: el paquete contiene criterios comerciales internos).

---

## Opción C · Si algún día usas Claude o Codex

Las carpetas de `skills/` ya están en el formato estándar del **Agent Skills** (`SKILL.md` + `references/` + `scripts/` + `assets/`):

- Claude Code: copiar a `~/.claude/skills/`.
- Codex: copiar a `~/.agents/skills/`.
- Claude.ai: comprimir la carpeta de cada skill (el ZIP debe contener `nombre-skill/SKILL.md`) y subirla en Customize → Skills.

No hay que mantener dos versiones: se edita la carpeta de `skills/` y se regenera el paquete de ChatGPT.

---

## Enfoque comercial (regla nº4 de las instrucciones)

Todos los documentos son herramientas de captación: existen para que el cliente contrate con B&M. Está prohibido escribir en un informe que el cliente no debe cambiar a Iberdrola, que «mejor no mueva» un suministro o que «no sale a cuenta» sin ofrecer acto seguido la vía para que sí contrate. Toda dificultad se convierte en palanca: potencia mal dimensionada, reactiva, autoconsumo, agrupar suministros. Los números no se tocan; se cambia el marco.

## Dos recordatorios que el paquete ya lleva dentro

**1. Los precios se cargan a mano, una vez, y se recargan cuando cambian** (cadencia semanal o mensual). El asistente no tiene acceso al área de Iberdrola y no actualiza nada por su cuenta. El control es la antigüedad de la carga: menos de 7 días, normal; entre 7 y 30, avisa antes de un informe importante; más de 30, no emite informe nuevo sin confirmar. Cuando cargues precios nuevos, pídele que recalcule los informes afectados.

**2. Pide siempre factura + SIPS.** El paquete incluye los mensajes tipo para pedirlos juntos y para justificar la limitación cuando solo hay uno. Los tres modos:

| Modo | Datos | Qué entrega | Qué advierte |
|---|---|---|---|
| A | Factura + SIPS | Comparativa y anualización con perfil real | — |
| B | Solo factura | Comparativa del periodo, anualizada como si el año fuera igual | Falta la anualización real |
| C | Solo SIPS | Lo que pagaría con nuestra oferta, con su consumo real | **No se puede afirmar ahorro** |

## El atajo que evita teclear números

Si tienes la factura en PDF con capa de texto (la que se descarga del área de cliente, no una foto), no hay que copiar ni un dato a mano:

```bash
python tools/factura_a_json.py bandeja/facturas/factura.pdf --producto "3.0TD Empresa Flex" --json /tmp/f.json
python skills/informes-ahorro-electrico/scripts/calc_energia.py /tmp/f.json
```

El primer comando extrae potencias, consumos, precios, excesos, bono social, alquiler, autoconsumo e impuestos, **y comprueba cada subtotal contra el que viene impreso en la factura**. Si algo no cuadra, se para y lo dice. El segundo reproduce la factura al céntimo y da la comparativa.

Funciona con la maqueta de las facturas que ya se han procesado; con maquetas de otras comercializadoras rechaza en lugar de inventar. Ver `sistema/MEJORAS.md`, punto 1.

## ¿Y si un compañero usa Claude, Gemini o Codex?

Mismo paquete, distinta puerta. El detalle está en `sistema/COMPATIBILIDAD.md`. Resumen: en Claude Code y Codex se copian las carpetas de `skills/` y **el código se ejecuta de verdad**; en ChatGPT y Claude con proyectos se suben los `.md` como conocimiento y la calculadora solo corre si se activa el análisis de datos; en Gemini y en cualquier plataforma con tope de caracteres se usa `instrucciones/INSTRUCCIONES_CORTAS.txt` (4.015 caracteres) y el asistente calcula a mano, con el caso de control de 836,27 € / 638,88 € como red de seguridad.

## Autoría y licencia

El paquete es obra de **Andrés Galeano** (NIE Z0002918W), que concede su uso a B&M Asesores Energéticos, S.L. Las condiciones —uso gratuito mientras se mantenga la relación profesional y remuneración posterior— están en `LICENSE.md`, que se sube también como archivo de conocimiento del Proyecto. La última línea de las instrucciones remite a él sin extenderse en condiciones.

## Firma variable: cada comercial con sus datos

El paquete lo puede usar cualquier comercial de B&M. En los documentos con firma personal —presupuestos y actas— el **nombre, teléfono y correo del emisor son variables**: la regla nº10 prohíbe dejar por defecto el nombre de otra persona. El contacto general de la empresa acompaña, nunca sustituye.

## Prueba de aceptación

Cuando el Proyecto esté montado, pídele esto y comprueba la respuesta:

> «Factura de Nagini de octubre de 2026, titular RAFAEL TENA SL, CIF B22243935, 3.0TD con 41,5 kW. Compárala con Empresa Flex con la hoja del 16/11/2026.»

Debe dar, sin más indicaciones:

| Resultado | Valor |
|---|---|
| Factura de origen cuadrada al céntimo | 836,27 € |
| Mismo mes con Flex (sin autoconsumo) | 638,88 € |
| Ahorro en el recibo | 197,39 € (23,6 %) |
| Ahorro anual, escenario conservador | 1.997,17 € |
| Con compensación de catálogo 0,02 €/kWh | 2.368,66 € |

Si no llega a esas cifras, el archivo que falta es `02_formulas.md` o `06_facturas_extraccion.md`.

Segunda prueba, para los modos:

> «Solo tengo el SIPS de este cliente, sin factura. Titular con NIF, 3.0TD, 41,5 kW.»

Debe negarse a afirmar ahorro, pedir los datos principales del potencial cliente y ofrecer el coste con nuestra tarifa etiquetado como «modo C».

Tercera prueba, presupuestos y enfoque comercial:

> «Hazme un presupuesto de cargador para Laura Pastor con las mismas partidas que el BM-00029.»

Cuarta prueba, actas y servicios:

> «Hazme un acta de entrega de un portátil y un teléfono para un empleado, con los datos de [comercial].»

Debe salir en una página, solo con el logo de B&M, con el nombre de ese comercial en el bloque «Quien entrega» y en la firma, y con el número de serie en blanco para rellenar a mano.

> «¿Qué incluye un boletín eléctrico y cómo lo presupuesto?»

Debe separar ejecución y tramitación, listar la documentación necesaria, identificar tasas aparte y no prometer plazos que dependan de la administración.

Debe salir con la estructura de una página (cabecera, alcance, desglose sin IVA, condiciones, pie legal), con **IVA al 21 %** y sin inventar partidas. Y si en un informe un suministro secundario no mejora, debe redactarlo como palanca comercial, nunca como «mejor no moverlo».

---

## Cómo mantenerlo

- **Hoja de precios nueva** → actualizar `07_precios_iberdrola.md` y el precio en la instrucción, y volver a subir el archivo. ChatGPT no avisa de que un precio ha caducado: la fecha en el pie del informe es el control.
- **Regla nueva o error detectado** → añadir una línea a `04_errores_conocidos.md`. Es el archivo que más valor acumula con el tiempo.
- **Cambio de producto o de condiciones** → `03_reglas_comerciales.md`.