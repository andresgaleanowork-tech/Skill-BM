# Documentación de mantenimiento

Aquí vive el **por qué** de las cosas: las decisiones tomadas, lo que se descartó y por qué, y las
métricas que dicen si el paquete mejora de verdad. El paquete que se usa a diario está en la raíz y
en `skills/`.

| Documento | Para qué sirve |
|---|---|
| [GUIA_INSTALACION_CHATGPT.md](GUIA_INSTALACION_CHATGPT.md) | instalar el paquete en ChatGPT, con las pruebas de aceptación |
| [COMPATIBILIDAD.md](COMPATIBILIDAD.md) | qué funciona en ChatGPT, Claude, Gemini y Codex, y qué se degrada |
| [PERFILES_FACTURA.md](PERFILES_FACTURA.md) | lectura de facturas por comercializadora y cómo añadir una nueva |
| [MEJORAS.md](MEJORAS.md) | qué falta, por orden de valor, y las cuatro métricas de control |
| [COMO_EVOLUCIONA.md](COMO_EVOLUCIONA.md) | los mecanismos que evitan el deterioro del paquete |
| [PLAN_SKILLS_BM.md](PLAN_SKILLS_BM.md) | plan original de las siete skills |

## Los logos

Están en `skills/maquetacion-documentos-bm/assets/logos/` y se copian al paquete de ChatGPT:

| Archivo | Origen |
|---|---|
| `bm.png` (1075×330) | logotipo de B&M en alta resolución, el que ya usaba la skill |
| `bm_compacto.jpg` (260×79) | extraído de los informes emitidos, para cabeceras con poco alto |
| `iberdrola.jpg` (1200×296) | **extraído de vuestros propios informes**: es el logotipo oficial que ya se venía usando, ampliado 4× para impresión |

Se eligió el logo de los informes y **no** uno descargado de internet porque es el que está aprobado y
en uso. El vectorial que circula por ahí es la versión apilada y con otra gama de color: no vale.

Si alguien consigue el logotipo de Iberdrola en vectorial (EPS o SVG **horizontal, con el texto a la
derecha**), basta con sustituir `iberdrola.jpg` manteniendo el nombre: el programa lo coge solo y no
hay que tocar ninguna plantilla.

## Las decisiones que no conviene revisar sin motivo

- **Todo entra a mano.** El área de precios de Iberdrola está bloqueada para usuarios normales: no
  hay descarga automática posible. Cualquier intento de extraerla es trabajo perdido.
- **Los precios se cargan una vez y se recargan cuando cambian**, con cadencia semanal o mensual.
  El control es la antigüedad de la carga, no un calendario.
- **Un perfil de factura por comercializadora.** Cada una factura distinto y un lector único se
  equivoca en todas.
- **El documento vende, no disuade.** Son herramientas de captación: la honestidad va en los datos,
  nunca en recomendar que el cliente no cambie.
- **Los cálculos no los hace el modelo.** Los hace `calc_energia.py`, que se niega a dar cifras si la
  factura no cuadra. Donde no hay ejecución de código, manda el protocolo de cálculo a mano de
  `02_formulas.md` con su caso de control.