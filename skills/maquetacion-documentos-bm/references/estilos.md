# Estilos y trampas de maquetación

## Variables

```
navy        #173d6d
verde       #00a651
verde text  #00894d
rojo        #c04048
fondo kpi   #f0f5f8 / #edf8f1 (verde)
aviso       #fff3e0
nota        #f1f5f8
```

## Tamaños que funcionan (medidos en A4 con 12 mm de margen)

| Elemento | Medida |
|---|---|
| Gráfico de barras apiladas | 7,9 × 1,58 in |
| Gráfico de escenarios | 7,9 × 1,72 in |
| Gráfico de precios por periodo | 7,2 × 1,30 in |
| Bloque hero | valor 46 px, 4 mm de padding |
| Tabla normal | 9,8 px, padding 1,75 mm |
| Tabla compacta | 9,2 px, padding 1,2 mm |
| Cuerpo de texto | 10,4 px, interlineado 1,33 |

## Trampas

1. **Leyenda dentro del gráfico**: en gráficos bajos se solapa con las etiquetas de valor. Colocarla arriba con `bbox_to_anchor=(.5, 1.18)` y subir el `ylim`.
2. **`height` fija en la página**: si el contenido no cabe, el pie se desplaza. Es la causa número uno de páginas en blanco.
3. **Gráficos SVG sin `bbox_inches='tight'`**: dejan márgenes invisibles que rompen la alineación con las tablas.
4. **Tabla que se corta**: pasar la última columna a la fila de totales o mover la tabla a la página siguiente, nunca reducir el cuerpo por debajo de 9 px.
5. **Logo**: usar el PNG en base64 embebido; con rutas externas el preview no lo carga y el PDF depende del sistema de archivos.

## Los logos: dónde están y cómo se usan

Los dos logos viven en esta skill, en `assets/logos/`:

| Archivo | Qué es | Uso |
|---|---|---|
| `bm.png` | logotipo completo B&M Asesores Energéticos, 1075×330 | cabecera de todos los documentos |
| `bm_compacto.jpg` | versión reducida, 260×79 | cuando la cabecera va muy justa de alto |
| `iberdrola.jpg` | logotipo Iberdrola, 1200×296 | cabecera derecha de informes y presupuestos |

**Regla de marca:** las **actas llevan solo el logo de B&M**. Nunca se deja el hueco del otro.

### Cómo se incrustan

Nunca se pegan a mano: las plantillas llevan los marcadores `{{LOGO_BM}}` y `{{LOGO_IB}}` y se
rellenan con un comando, que además los incrusta en base64 para que el HTML resultante sea **un solo
archivo** que se puede enviar por correo o convertir a PDF sin depender de carpetas:

```bash
python tools/rellenar_plantilla.py --tipo informe --datos datos.json --salida /tmp/informe.html
python tools/rellenar_plantilla.py --tipo acta --datos datos.json --salida /tmp/acta.html
```

En un acta el logo de Iberdrola se retira automáticamente, sin dejar hueco.

### En cada plataforma

| Plataforma | Qué hacer con los logos |
|---|---|
| **ChatGPT · Proyecto** | subirlos como archivos del Proyecto; los nombres son `logo_bm.png` y `logo_iberdrola.jpg` |
| **ChatGPT · Custom GPT** | subirlos también como Knowledge |
| **Claude · Proyecto** | adjuntarlos en el proyecto junto a las plantillas |
| **Claude Code / Codex** | ya están dentro de `skills/…/assets/logos/`, no hay que hacer nada |
| **Gemini y plataformas sin archivos adjuntos** | el asistente **no puede incrustar imágenes** en el HTML: genera el documento con el hueco reservado y se pega el logo al exportar. Que lo diga, no que devuelva el marcador a la vista |

Si en una plataforma no se pueden subir los logos, el asistente **no inventa** ni escribe el nombre de
la empresa como sustituto del logotipo: deja la cabecera preparada y lo advierte.
