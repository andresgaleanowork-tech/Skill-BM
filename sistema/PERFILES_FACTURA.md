# Lectura de facturas por comercializadora

Fecha: 21/07/2026 · Autor: Andrés Galeano (NIE Z0002918W)

Iberdrola es lo que vendemos, pero **lo que llega a la mesa es de todo el mercado**. Cada
comercializadora maqueta la factura a su manera y, más importante, **factura distinto**: no es
un problema de diseño, es de aritmética. Este documento dice qué está cubierto, qué falta y cómo
se añade una comercializadora nueva.

## Por qué no vale un lector único

| Comercializadora | Cómo factura | Qué hay que hacer |
|---|---|---|
| **Nexus / ENERGIA** | parte el precio en «Energía ATR» + «Energía Libre» | sumar los dos precios, **no** los kWh (son los mismos) |
| **Iberdrola Clientes** | energía en una sola línea «902 kWh x 0,186689 €/kWh»; el IEE va dentro de ENERGÍA; devolución de fianza que resta **después** de impuestos | energía agregada + fianza al final |
| **Octopus** | cada término desglosado en peaje + cargos + margen, 3 decimales, redondeo por línea | tomar el primer precio de cada periodo; tolerancia de céntimos |
| **Factor Energía** | potencia en €/kW·mes con descuento por línea (x0,94); reactiva y ajuste de REE aparte | convertir mes → días; aislar lo no comparable |

Un lector único se equivoca en las cuatro. Por eso hay un **perfil por comercializadora** en
`tools/perfiles/`, y una comprobación contra los subtotales impresos en cada uno.

## Lo que está cubierto y verificado

Cuatro facturas reales, las cuatro reproducidas:

| Perfil | Factura de prueba | Resultado |
|---|---|---|
| `generico` | ENERGIA 26100237 (RAFAEL TENA SL) | **836,27 €** al céntimo |
| `iberdrola_clientes` | FACTURA TURBINSA | **195,54 €** al céntimo |
| `octopus` | factura de Rafael Tena Porta, 2.0TD | **75,24 €** con 2 céntimos de diferencia declarados |
| `factor_energia` | EUDAMONIA SA | **1.352,82 €** al céntimo |

Las cuatro están en `eval/casos.json` (`FACT-PDF`, `PDF-TURBINSA`, `PDF-OCTOPUS`, `PDF-FACTOR`)
y se comprueban en cada `python eval/run.py`.

## Cómo se añade una comercializadora nueva

1. Guarda una factura real en `bandeja/facturas/ejemplos/`.
2. Copia el perfil que más se parezca y cámbiale `clave`, `nombre` y `reconoce()`.
3. Ajusta las expresiones regulares a sus líneas. **Nunca** des por bueno un importe sin
   comprobarlo contra el subtotal impreso.
4. Añade un caso a `eval/casos.json` con el total real de esa factura.
5. `python eval/run.py` tiene que quedarse en verde.

Lo importante no es que lea: es que **rechace** cuando no cuadre. Un perfil que devuelve cifras
sin comprobarlas es peor que no tener perfil.

## Regla de tolerancia

| Situación | Tolerancia | Cómo se declara |
|---|---|---|
| Reproduce al céntimo | 0,01 € | «factura de origen reproducida al céntimo» |
| Comercializadora que redondea por línea (Octopus) | 0,10 € declarados en el perfil | la diferencia **se escribe en el informe**, no se oculta |
| Fuera de tolerancia | — | no se entrega ninguna cifra |

## Lo que falta

- **Naturgy, Endesa, Repsol, TotalEnergies, Holaluz, Podo…** cada una necesitará su perfil y una
  factura real de muestra. Sin factura real no se escribe el perfil: se adivina, y adivinar aquí
  es un informe mal.
- **Facturas escaneadas o fotos**: no se leen con este programa. La vía es el OCR que ya traen
  ChatGPT, Claude y Gemini, con la misma regla: sin cuadre contra el total impreso, no hay cifras.
- **Facturas de gas**: mismo enfoque, otro perfil (el gas no tiene IEE sino impuesto sobre
  hidrocarburos).
