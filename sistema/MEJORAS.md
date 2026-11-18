# Qué mejorar en el paquete, por orden de valor

Fecha: 21/07/2026 · Autor: Andrés Galeano (NIE Z0002918W)

Criterio de orden: **primero lo que puede hacer que un informe salga mal, después lo que ahorra tiempo, al final lo que da imagen.** Todo lo que ya está hecho está abajo, en «Lo que ya no hace falta».

---

## 1. Lectura automática de facturas · HECHO PARA CUATRO COMERCIALIZADORAS

`tools/factura_a_json.py` + `tools/perfiles/`. Cada comercializadora factura distinto y por eso hay
un perfil por cada una, con comprobación contra los subtotales impresos:

| Perfil | Factura de prueba | Resultado |
|---|---|---|
| genérico (Nexus/ENERGIA) | TENA SL | 836,27 € al céntimo |
| Iberdrola Clientes | TURBINSA | 195,54 € al céntimo |
| Octopus | 2.0TD de Tena Porta | 75,24 € con 2 céntimos declarados |
| Factor Energía | EUDAMONIA | 1.352,82 € al céntimo |

**Lo que queda abierto:** Naturgy, Endesa, Repsol, TotalEnergies, Holaluz, Podo y el resto. Cada una
necesita una factura real de muestra y su perfil. El procedimiento está en `sistema/PERFILES_FACTURA.md` y es
de veinte minutos por comercializadora. Mientras no haya perfil, el programa **rechaza**: no inventa.

## 2. SIPS → anualización real · HECHO

`tools/anualizar.py`. Tres caminos, en este orden:

1. **SIPS** (consumos de la distribuidora) → perfil real por periodos. En la Comunidad Valenciana la
   distribuidora es i-DE, así que se pide y se obtiene.
2. **Doce facturas del último año** → el mismo resultado sumando los doce periodos.
3. **Una sola factura** → proyección declarada, nunca presentada como anualización real.

Probado con un SIPS real: 15.007 kWh anuales, coste actual 4.880,55 €, con Empresa Flex 4.690,66 €,
**ahorro 189,89 € calculado, no proyectado**. Es el caso `ANUAL-SIPS` de la batería.

## 3. OCR para facturas escaneadas · PENDIENTE, IMPACTO DIRECTO

Una parte de lo que envían los clientes son fotos o escaneos sin capa de texto. Hoy se avisa y se revisa a ojo. Con `tesseract` + preprocesado (enderezar, binarizar) se convierte en lectura asistida **con la cifra marcada como no fiable hasta que el subtotal cuadre**.

Regla que debe respetar: el OCR nunca rellena un campo que no se haya podido verificar contra un subtotal impreso. La tentación de «leer rápido» es justo la que produce informes malos.

Coste: bajo-medio. Requiere instalar `tesseract` y `pdf2image` en el entorno donde se ejecute.

## 4. Ficha de precios que se genera sola desde el área de Iberdrola · NO SE PUEDE, Y ESTÁ BIEN

El área está bloqueada: descartado y anotado en la bitácora para que nadie lo reintente. Lo que sí se puede mejorar es la **ficha de entrada**: hoy se copia a mano en un `.txt` con un formato fijo. Un formulario mínimo (o una plantilla de hoja de cálculo) que valide al pegar reduciría el error humano del paso más crítico.

## 5. Índice de informes emitidos · HECHO

No hay registro de qué informe se emitió a quién y con qué hoja de precios. Con un `indice.csv` (cliente, CIF, CUPS, fecha, hoja usada, ahorro, producto) se gana:

- poder responder «¿qué le mandé a este cliente en marzo?» sin buscar en el correo;
- detectar clientes a los que conviene volver a llamar;
- saber qué informes hay que rehacer cuando cambia la hoja de precios.

Coste: bajo. Es una tabla y una línea al entregar.

## 6. Instrucciones por bloques · PENDIENTE, BAJO

Las instrucciones del Proyecto van por 7.992 de 8.000 caracteres. Cualquier regla nueva obliga a recortar. La solución es un archivo `11_reglas_de_oro.md` dentro del conocimiento con lo que puede vivir ahí, dejando en las instrucciones solo lo que debe estar siempre presente. Se pierde algo de fuerza (el conocimiento se consulta, no se obedece), así que solo cuando haga falta de verdad.

## 7. Conector propio (MCP) · FUTURO, NO AHORA

Un servidor MCP daría herramientas reales al asistente: «lee esta factura», «dame los precios del producto X», «genera el PDF». Elimina el paso de pegar y subir archivos. Pero exige infraestructura, claves y mantenimiento, y el paquete ya funciona sin ello. Solo tiene sentido si lo usan varias personas a diario.

## 8. Plantillas de documento final · PARCIAL

Existen las plantillas HTML y `pdf_qa.py` valida el PDF. Falta:

- prueba visual automática (comparar el PDF generado con una referencia página a página) para detectar pies desplazados sin abrirlo;
- una versión `.docx` de presupuesto y acta, porque muchos clientes piden editable.

---

## Lo que ya no hace falta (hecho y verificado)

| Mecanismo | Estado |
|---|---|
| Fuente única de conocimiento y generación del paquete | hecho, `tools/generar_paquete_chatgpt.py` |
| Carga manual de precios validada | hecho, `tools/cargar_precios.py` |
| Control de antigüedad de precios | hecho, `tools/estado_precios.py` |
| Calculadora que se niega a calcular mal | hecho, `calc_energia.py` con validación y cuadre obligatorio |
| Factura PDF → JSON → cálculo | hecho para una maqueta, `tools/factura_a_json.py` |
| Normalizador de documentos entrantes | hecho, `tools/normalizar_documento.py` |
| Batería de pruebas, incluidas negativas | hecho, `eval/run.py` (11 casos) |
| Bitácora de correcciones | hecho, `metricas/bitacora.md` |

## Las cuatro métricas que dicen si esto mejora de verdad

1. **Informes devueltos o corregidos** por cada diez emitidos. Objetivo: menos de uno.
2. **Tiempo desde que llega la factura hasta que el informe está listo.** Objetivo: menos de 20 minutos.
3. **Facturas que necesitan tecleo manual** frente a las que se leen solas. Objetivo: por debajo del 20 %.
4. **Casos de la batería en verde.** Objetivo: 100 % siempre; un rojo bloquea la entrega.
