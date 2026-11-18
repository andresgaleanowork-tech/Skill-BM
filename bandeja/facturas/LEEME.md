# Bandeja de facturas

Aquí se dejan las facturas que envían los clientes (PDF con capa de texto, no fotos) y los
ficheros SIPS de la distribuidora.

**No se sube nada de esta carpeta al repositorio**: son datos personales de clientes (RGPD).
Está excluida en `.gitignore`.

```bash
python tools/factura_a_json.py bandeja/facturas/factura.pdf --producto "3.0TD Empresa Flex" --json /tmp/ficha.json
python tools/anualizar.py --sips bandeja/facturas/sips.pdf --factura /tmp/ficha.json \
    --producto "3.0TD Empresa Flex" --json /tmp/anual.json
```

## Las pruebas que necesitan una factura de muestra

Tres casos de `eval/run.py` (`PDF-TURBINSA`, `PDF-OCTOPUS`, `PDF-FACTOR`) y uno de anualización
(`ANUAL-SIPS`) usan facturas reales como muestra. **Esas facturas no pueden estar en el repositorio**
porque identifican a clientes concretos. En un clon limpio esos casos aparecen como `[OMITE]`, que no
es un fallo: el resto de la batería sigue comprobando el cálculo, los perfiles de precio y las cinco
pruebas negativas.

### Cómo recuperarlos con datos anónimos

Deja en esta carpeta una factura de la misma comercializadora con los datos personales cambiados a
mano —titular, CIF/NIF, CUPS, dirección e importes— y guarda sus nuevas cifras en `eval/casos.json`.
Regla para crearlas: el total impreso tiene que seguir cuadrando con la suma de sus líneas, o el caso
no sirve. En cuanto existan, `eval/run.py` los vuelve a evaluar en vez de omitirlos.

## Añadir una comercializadora nueva

1. Deja aquí una factura de esa comercializadora.
2. Copia el perfil más parecido de `tools/perfiles/` y ajusta sus expresiones regulares.
3. Comprueba que cuadra con el total impreso antes de dar el perfil por bueno.
4. Añade el caso a `eval/casos.json`.
5. **Borra la factura del cliente antes del commit.**