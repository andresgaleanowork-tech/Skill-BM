# Bandeja de precios

Aquí se deja la ficha de precios copiada a mano del área de Iberdrola (o del correo que la
trae). Un archivo de texto por carga, con el formato de `ficha_16112026_ejemplo.txt`.

Las fichas **no se suben al repositorio**: están en `.gitignore` porque contienen precios del
área de cliente y caducan.

```bash
python tools/cargar_precios.py bandeja/precios/ficha_16112026.txt
```