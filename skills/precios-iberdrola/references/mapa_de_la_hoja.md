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

- `grep -n \"Empresa Flex\"` sobre el texto extraído del PDF localiza el bloque.
- Cada producto ocupa unas 19-20 líneas: nombre, 6 TP, 6 TE, descuento, excedente, duración y 3 banderas.
- Si un producto no aparece con `grep`, puede estar partido en dos líneas: busca por el nombre sin la gama.
