# Bitácora de correcciones y mejoras

Una línea por aprendizaje. Formato: `fecha · documento · qué pasó · qué se cambió en el paquete`.
El objetivo es que **ningún error se repita dos veces** y que el paquete mejore con cada informe real.

| Fecha | Documento / caso | Qué pasó | Cambio en el paquete |
|---|---|---|---|
| 2026-07-21 | Informe RAFAEL TENA | Los pies de página se desplazaban a una quinta hoja aunque el número de páginas fuera correcto | Checklist con revisión visual obligatoria + regla de compactar antes de reducir letra (`05_maquetacion`) |
| 2026-07-21 | Informe RAFAEL TENA | El bono social no entraba en la base del IEE de la factura de origen (variante por comercializadora) | `calc_energia.py` con parámetro `bono_social_en_base_iee` + caso de prueba RT-OCT |
| 2026-07-21 | Informe RAFAEL TENA | La página de suministros secundarios decía «mejor no moverlos»: era un análisis, no una herramienta comercial | Regla nº4 «el documento vende, no disuade» y reescritura de la página |
| 2026-07-21 | Hojas de precios | Se reutilizaban precios de la hoja anterior | Carga manual validada (`cargar_precios.py`), control de antigüedad y casos de prueba por producto. El área de Iberdrola está bloqueada: no hay descarga automática |
| 2026-07-21 | Informes con solo factura o solo SIPS | Se presentaba la proyección como si fuera anualización real | Modos A/B/C declarados en la primera página (`escenarios_de_datos`) |
| 2026-07-21 | Flujo de trabajo real | Los precios y las facturas llegan a mano: nada se puede descargar | Bandeja de entrada, `cargar_precios.py`, `normalizar_documento.py` y regla «tú no buscas nada» |
| 2026-07-21 | Cadencia de precios | El recordatorio de 48-72 h no reflejaba la realidad (cambian cada semana o mes) | Control por antigüedad de la carga: 7 días normal, 7-30 avisar, +30 pedir confirmación (`estado_precios.py`) |
| 2026-07-21 | Cálculo | El asistente podía dar una cifra aunque la factura no cuadrase | calc_energia.py se niega a calcular con datos incoherentes (código 2) y bloquea la entrega si el total no cuadra con la factura real (código 3); 5 casos negativos en eval |
| 2026-07-21 | Cálculo a mano | Sin ejecución de código se calculaba de memoria y se arrastraban redondeos | Protocolo obligatorio en formulas.md §11: céntimos enteros, una línea por periodo, doble suma y caso de control de 836,27 € |
| 2026-07-21 | Lectura de facturas | Teclear a mano los datos de la factura: el punto donde se cuelan los errores | tools/factura_a_json.py lee el PDF, comprueba los subtotales impresos y genera el JSON de cálculo; caso FACT-PDF en eval |
| 2026-07-21 | Facturas de otras comercializadoras | Un solo lector no sirve: cada comercializadora factura distinto (ATR+libre, energía agregada, peajes desglosados, €/kW·mes con descuento) | Perfiles en tools/perfiles/ (genérico, Iberdrola Clientes, Octopus, Factor Energía), cada uno con comprobación contra los subtotales impresos y su caso en eval |
| 2026-07-21 | Anualización | Se anualizaba con 12 recibos equivalentes cuando el cliente podía dar el SIPS | tools/anualizar.py: SIPS o doce facturas → anualización real; sin SIPS se piden las doce facturas, no se estima |
| 2026-07-21 | 2.0TD | La calculadora exigía los mismos periodos de potencia y de energía; en 2.0TD son 2 y 3 | Soporte de N periodos de potencia y M de energía, y de €/kW·mes |

## Cómo se usa

1. Cuando un informe real revele un fallo, se añade una línea **antes** de corregir el documento del cliente.
2. Si el fallo es de cálculo o de precio, se añade un caso a `eval/casos.json`.
3. Si el fallo es de redacción o de criterio comercial, se convierte en una regla en la skill correspondiente.
4. Cada tres meses: se revisan las líneas repetidas. Una regla que se repite tres veces debe subir a las instrucciones del Proyecto.