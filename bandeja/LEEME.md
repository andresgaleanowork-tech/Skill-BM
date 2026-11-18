# Bandeja de entrada manual

Todo entra por aquí, a mano. El asistente **no puede ir a buscar nada**: el área de precios
de Iberdrola está bloqueada para usuarios normales y las facturas las envía el cliente.

```
bandeja/
├── precios/        fichas de precios copiadas a mano de la Agencia Ágora
├── facturas/       PDF de facturas recibidas de los clientes
└── presupuestos/   ofertas nuestras o de la competencia que hay que pasar a estilo B&M
```

## 1. Precios (manual, siempre)

1. Abre la hoja de precios en el área de Iberdrola y copia los productos que uses.
2. Rellena una ficha con el formato de `precios/ficha_16112026_ejemplo.txt`.
3. Carga la ficha:

```bash
python tools/cargar_precios.py bandeja/precios/ficha_DDMMAAAA.txt
```

El cargador **rechaza** líneas incompletas (por ejemplo, seis TP cuando la tarifa tiene dos),
guarda `precios.json` con la fecha de la hoja y avisa si algún precio se mueve más de un 25 %
respecto a la carga anterior: casi siempre es un error de copia, no un cambio real.

## 2. Facturas de clientes (manual)

Deja el PDF en `bandeja/facturas/` y normalízalo:

```bash
python tools/normalizar_documento.py bandeja/facturas/factura_cliente.pdf
```

Saca CIF/NIF, CUPS, importes, fechas, potencias y consumos, y avisa si el PDF es un escaneo
sin capa de texto (entonces hay que revisarlo a la vista). **No rellena huecos**: lo que no
está, se pide.

## 3. Presupuestos y documentación (manual)

Lo mismo para un presupuesto nuestro que hay que rehacer, o para una oferta de la competencia
que hay que igualar:

```bash
python tools/normalizar_documento.py bandeja/presupuestos/oferta_competencia.pdf
```

Con eso y la skill `presupuestos-bm` se rehace en estilo B&M, comparando con el mismo alcance
y con IVA.

## Nombre de los archivos

`AAAA-MM-DD_cliente_tipo.pdf` → `2026-11-20_gasoprix_factura.pdf`.
Así la bandeja se ordena sola y no se procesa dos veces lo mismo.