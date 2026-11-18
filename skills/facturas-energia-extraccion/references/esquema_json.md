# Esquema de salida

```json
{
  "titular": {"nombre": "", "documento": "", "tipo_documento": "CIF|NIF"},
  "suministro": {"cups": "", "direccion": "", "tarifa_acceso": "3.0TD", "distribuidora": ""},
  "comercializadora": {"nombre": "", "referencia_contrato": "", "producto": "", "fin_contrato": "AAAA-MM-DD"},
  "periodo": {"desde": "AAAA-MM-DD", "hasta": "AAAA-MM-DD", "dias": 31, "procedencia_lectura": "real|calculada"},
  "potencias_kw": [0,0,0,0,0,0],
  "kwh": {"P1":0,"P2":0,"P3":0,"P4":0,"P5":0,"P6":0},
  "precios": {
    "tp": [0,0,0,0,0,0],
    "tp_unidad": "dia|anio",
    "te": [0,0,0,0,0,0]
  },
  "conceptos": {
    "potencia_eur": 0, "energia_eur": 0, "excesos_eur": 0, "reactiva_eur": 0,
    "autoconsumo_eur": 0, "bono_social_eur": 0, "alquiler_eur": 0, "servicios_eur": 0,
    "iee_eur": 0, "iva_eur": 0, "total_eur": 0
  },
  "impuestos": {"iee_tipo": 0.0511269632, "iva_tipo": 0.21, "otro": null},
  "alertas": ["reactiva penalizada", "demanda máxima > potencia contratada", "lectura estimada"],
  "cuadre": {"total_factura": 0, "total_calculado": 0, "diferencia": 0, "ok": true}
}
```

Reglas:

- Importes en euros con dos decimales; precios con seis decimales.
- `tp_unidad` es obligatorio: confundir €/kW·día con €/kW·año multiplica o divide por 365 el coste de potencia.
- Los campos que no aparezcan en la factura van a `null`, no a cero.
- `alertas` se rellena siempre, aunque esté vacío.
