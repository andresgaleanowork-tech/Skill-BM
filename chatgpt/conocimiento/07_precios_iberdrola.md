# Precios de Iberdrola · localización y vigencia


---

---
name: precios-iberdrola
description: >
  Localiza y verifica precios en la Hoja de Precios de Iberdrola (Agencia Ágora):
  Empresa Flex, Empresas 10 %TE, Empresa Plus, planes 2.0TD, 3.0TD y 6.xTD, con
  fechas de vigencia y reglas de elegibilidad por CIF o NIF. Usar cuando se pida un
  precio, comparar productos del catálogo, actualizar una hoja de precios o
  comprobar si un plan sigue vigente.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Precios de Iberdrola · localización y vigencia

## Carga manual (el área de Iberdrola está bloqueada)

Nadie de B&M puede descargar la hoja por su cuenta: el área de precios de Iberdrola está restringida. Los precios **se copian a mano** y se pegan en una ficha:

```
3.0TD Empresa Flex | TP: 20,376927 10,617621 4,481534 3,886333 2,513851 1,442287 | TE: 0,253955 0,209968 0,180518 0,157978 0,149284 0,152954
2.0TD Plan Estable | TP: 38,99 38,99 | TE: 0,206533
```

`tools/cargar_precios.py` valida que el número de periodos encaje con la tarifa, guarda la fecha de la hoja y avisa si un precio se mueve más de un 25 % respecto a la carga anterior (casi siempre es un error de copia). Si el usuario no pega los precios, se piden: no se estiman.

## Regla de oro

**La hoja caduca.** Cada hoja sustituye a la anterior por completo. Nunca se mezclan precios de dos hojas distintas, y nunca se reutiliza un informe anterior sin recalcular con la hoja vigente. El informe debe citar la fecha de la hoja usada.

## Cadencia de la carga (semanal o mensual)

Los precios se cargan **una vez** y se vuelven a cargar **solo cuando cambian**, con una cadencia real de una semana a un mes. No hay que perseguir la hoja cada día.

- La carga se hace a mano en una ficha y queda con **fecha de hoja** y **fecha de carga**.
- El control no es un calendario, es la **antigüedad de la carga**:
  - menos de 7 días → al día, sin acción;
  - entre 7 y 30 días → revisar antes de un informe importante, preguntando al usuario si ha salido hoja nueva;
  - más de 30 días → **no emitir un informe nuevo** sin confirmar vigencia.
- En cada informe y presupuesto figura la fecha de la hoja usada. Un informe emitido con una hoja anterior sigue siendo válido como fotografía de su fecha, pero no se reenvía a un cliente sin actualizar.
- El asistente **no actualiza precios por su cuenta**: no tiene acceso al área de Iberdrola. Los aporta el usuario.

## Paso 1 · Identificar la hoja vigente

- Comprueba la fecha de la portada («última actualización del documento»).
- Si el usuario aporta una hoja nueva: se reemplaza el archivo, se genera un resumen y **se recalculan** los informes afectados.
- Guarda siempre el resumen junto a la hoja, con la fecha en el nombre: `Resumen_Precios_DDMMAAAA.txt`.

## Paso 2 · Encontrar el producto

La hoja tiene 12 páginas: portada, índice, tarifas eléctricas (2.0TD, 3.0TD, 6.xTD, AT) y Productos y Servicios. Cada fila de producto trae, en este orden: nombre, TP de P1 a P6 (€/kW·año), TE de P1 a P6 (€/kWh), descuentos, duración, condiciones y precio de excedentes.

El mapa por página y por columnas está en `references/mapa_de_la_hoja.md`.

## Paso 3 · Comprobar elegibilidad antes de cotizar

| Documento | Productos |
|---|---|
| CIF | Empresa Flex, Empresas 10 %TE, Empresa Plus, Especial 15 %TE, Exclusivo 30 %TE |
| NIF/NIE | Impulsa 24h, Exclusivo 15 %TE/TP, Estable, Especial plus, Hogar Especial, Solar, Vehículo Eléctrico |

Un plan de la gama Empresa ofrecido a un NIF no se puede contratar: es un error que se detecta en el informe del cliente, no en la hoja.

## Paso 4 · Distinguir descuento de precio final

- Algunos productos publican el precio **antes** de descuento y el descuento aparte («20 % s/Te»).
- Otros ya traen el precio final.
- La oferta propia de 2.0TD de B&M (TE 0,0999 €/kWh con el 15 % ya incluido; TP 45,49/28,49) **no admite otro descuento encima**.
- Si dudas, calcula el precio con y sin descuento y compara con la factura del cliente: el que cuadre es el que se está aplicando.

## Paso 5 · Entregar el resumen

Formato de salida: tabla por producto con TP, TE, descuento, duración y fecha de la hoja; y una frase con el efecto práctico (cuánto sube o baja respecto a la hoja anterior, en €/kWh y en euros por cada 100 kWh).

## Recursos

- `references/mapa_de_la_hoja.md`: dónde está cada cosa en la hoja.
- `references/productos.md`: catálogo de productos con su gama, duración y condiciones.
- `assets/resumen_precios_plantilla.txt`: plantilla del resumen que se guarda junto a cada hoja.


---

# Mapa de la Hoja de Precios

Estructura típica (12 páginas, versión de 16/11/2026):

| Página | Contenido |
|---|---|
| 1 | Portada con la fecha de actualización. **Aquí se lee la vigencia.** |
| 2 | Índice / en blanco |
| 3 | 2.0TD (todas las variantes _2 y _3), 2.0TD Eventual y comienzo de 3.0TD |
| 4 | 3.0TD, 6.1TD, 6.2TD, 6.3TD, 6.4TD, RL.1 a RL.6 (gas) |
| 5-6 | Productos y Servicios (PyS) con precios con IVA, IGIC e IPSI |
| 7-12 | Anexos y páginas sin texto |

## Orden de columnas en las filas de producto

```
nombre del producto
TP P1 … TP P6        €/kW·año
TE P1 … TE P6        €/kWh   (en 2.0TD: punta y valle, o punta/llano/valle)
descuento            texto libre: «15% s/Te», «20% s/Te (+5% si ACP)»…
precio excedentes    €/kWh
duración             12m / 24m / 60m / 120m
mercado libre / GdO, energía verde S/N, canal prescriptor S/N
```

Las filas de 2.0TD añaden las columnas de precio en €/kW·día para punta y valle.

## Cómo buscar rápido

- `grep -n "Empresa Flex"` sobre el texto extraído del PDF localiza el bloque.
- Cada producto ocupa unas 19-20 líneas: nombre, 6 TP, 6 TE, descuento, excedente, duración y 3 banderas.
- Si un producto no aparece con `grep`, puede estar partido en dos líneas: busca por el nombre sin la gama.


---

# Catálogo de productos

## Gama Empresa (solo CIF)

| Producto | Tarifas | Duración | Nota |
|---|---|---|---|
| Empresa Flex | 3.0TD, 6.1TD | 12 m | Referencia. Sin descuentos cruzados |
| Empresas 10 %TE | 3.0TD, 6.1TD | 12 m | 10 % sobre energía |
| Empresa Plus | 3.0TD, 6.1TD | 12 m | Descuento adicional por volumen > 40 MWh/a |
| Plan Especial 15 %TE | 3.0TD, 6.1TD | 12 m | Precio base más alto con 15 % |
| Plan Exclusivo 30 %TE | 3.0TD | 12 m | Volumen alto |
| Plan Regantes | 3.0TD, 6.1TD | 12 m | Riegos |

## Persona física / NIF

| Producto | Tarifas | Duración | Nota |
|---|---|---|---|
| Impulsa 24h | 2.0TD, 3.0TD | 12 m | 20 % s/Te |
| Plan Exclusivo 15 %TE/TP | 2.0TD | 12 m | 15 % en energía y potencia |
| Plan Estable | 2.0TD | 60 m / 12 m | 15 % s/Te |
| Especial plus 15 %TE | 2.0TD | 12 m | 15 % s/Te |
| Plan Hogar Especial | 2.0TD | 36 m / 12 m | 15 % s/Te |
| Plan Solar | 2.0TD | 12 m | Precios distintos punta/valle, excedentes 0,06 |

## Indexados y temporales

- Plan OMIE (0, 1, 2, 3, Obras, Comunidades): precio ligado a PVPC + margen; TP fijos.
- Eventual / Temporal: para obras y suministros provisionales, sin impuesto eléctrico en el precio mostrado.