# Skills de B&M Asesores Energéticos

Paquete de conocimiento y herramientas para que un asistente de IA (ChatGPT, Claude, Gemini, Codex)
produzca **informes de ahorro eléctrico, comparativas de tarifa, presupuestos, propuestas de
servicios y actas de entrega** con la marca de B&M, colaborador de Iberdrola.

La regla que lo gobierna todo: **ninguna cifra se entrega si la factura de origen no se ha
reproducido antes al céntimo.** El paquete no solo pide corrección: la comprueba sola y se niega a
calcular cuando los datos no cuadran.

---

## Qué hay aquí

```
skills/                 7 skills en formato abierto (SKILL.md + references + scripts + assets)
  informes-ahorro-electrico/    informe de ahorro, modos A/B/C, fórmulas, calculadora
  facturas-energia-extraccion/  lectura y cuadre de facturas, SIPS, anualización
  precios-iberdrola/            catálogo, elegibilidad CIF/NIF, vigencia de precios
  presupuestos-bm/              presupuestos con la misma dinámica comercial
  servicios-bm/                 boletines, expedientes de Iberdrola, legalizaciones
  actas-entrega-bm/             actas de entrega y devolución de bienes
  maquetacion-documentos-bm/    identidad, plantillas, QA del PDF
tools/                  utilidades de línea de comandos
  factura_a_json.py             factura PDF → JSON de cálculo (con perfiles por comercializadora)
  perfiles/                     cómo factura cada comercializadora
  anualizar.py                  SIPS o doce facturas → consumo anual real
  cargar_precios.py             ficha de precios → precios.json, con validación
  estado_precios.py             antigüedad de la carga de precios
  normalizar_documento.py       documento recibido → datos, avisos y lo que falta
  indice_informes.py            qué se emitió, a quién y con qué hoja de precios
  rellenar_plantilla.py         plantilla + datos → HTML con los logos incrustados
  generar_paquete_chatgpt.py    skills → conocimiento para ChatGPT + ZIP
eval/                   batería de 17 pruebas, 5 de ellas negativas
chatgpt/                paquete listo para el Proyecto o el Custom GPT
instrucciones/          versión corta de las instrucciones (4.000 caracteres)
sistema/                documentación de mantenimiento y decisiones
metricas/               bitácora de correcciones
bandeja/                carpetas de entrada (vacías: los datos de cliente no se suben)
comprobar.bat / .sh     comprobación completa: pruebas, precios y documentos desfasados
```

## Instalación en dos minutos

```bash
git clone <este-repo> && cd <este-repo>
pip install pymupdf                     # única dependencia obligatoria
cp precios.ejemplo.json precios.json    # y rellena los precios de tu hoja
python eval/run.py                      # cálculo, precios y pruebas negativas
```

En Windows basta con doble clic en **`comprobar.bat`**: instala lo que falte, pasa las pruebas, mira
la antigüedad de los precios y avisa de los informes que usan una hoja vieja.

**Sobre los casos omitidos:** las pruebas que necesitan una factura real (`PDF-TURBINSA`,
`PDF-OCTOPUS`, `PDF-FACTOR`, `ANUAL-SIPS`) aparecen como `[OMITE]` en un clon limpio, porque esas
facturas identifican a clientes y no se suben. **No es un fallo**: los casos de cálculo, precios y las
cinco pruebas negativas se evalúan siempre. Cómo recuperar los omitidos con muestras anónimas está en
`bandeja/facturas/LEEME.md`.

Si algún caso evaluado sale en rojo, no entregues nada hasta arreglarlo.

## El flujo de trabajo, de la factura al informe

```bash
# 1. La factura llega en PDF (de cualquier comercializadora)
python tools/factura_a_json.py bandeja/facturas/factura.pdf \
    --producto "3.0TD Empresa Flex" --json /tmp/ficha.json

# 2. ¿Hay SIPS? Anualización REAL. Si no, doce facturas. Si no, proyección declarada.
python tools/anualizar.py --sips bandeja/facturas/sips.pdf \
    --factura /tmp/ficha.json --producto "3.0TD Empresa Flex" --json /tmp/anual.json

# 3. Cálculo (se niega a dar cifras si la factura no cuadra)
python skills/informes-ahorro-electrico/scripts/calc_energia.py /tmp/anual.json

# 4. El documento, con los logos ya dentro (en actas, solo el de B&M)
python tools/rellenar_plantilla.py --tipo informe --datos /tmp/datos.json --salida /tmp/informe.html

# 5. Al entregar el documento, se anota en el índice
python tools/indice_informes.py --anadir --cliente "..." --hoja 2026-11-16 --ahorro 1997.17
```

En ChatGPT, Claude o Gemini el paso 1 puede hacerlo el propio asistente: se le adjunta la factura
—también si es una foto— y devuelve el JSON. La comprobación sigue siendo la misma.

## Las cuatro comprobaciones que evitan el desastre

| Comprobación | Dónde vive | Qué hace si falla |
|---|---|---|
| La factura se reproduce al céntimo | `calc_energia.py` | no devuelve cifras (código 3) |
| Los subtotales impresos cuadran | perfiles de factura | rechaza el documento |
| Los datos son coherentes (periodos, unidades, potencias) | `calc_energia.py` | no calcula (código 2) |
| La hoja de precios está vigente | `estado_precios.py` | avisa o bloquea según antigüedad |

## Estado y mantenimiento

- **17 casos** en `eval/run.py`, cinco de ellos negativos: comprueban que el sistema **rechaza** lo que
  debe rechazar. En un clon limpio se evalúan 12 y los 5 que necesitan factura real quedan omitidos.
- **Los dos logos están dentro**: `skills/maquetacion-documentos-bm/assets/logos/` (`bm.png`,
  `iberdrola.jpg`) y también viajan al paquete de ChatGPT. `rellenar_plantilla.py` los incrusta en el
  HTML y, en las actas, retira el de Iberdrola sin dejar hueco.
- Cuatro comercializadoras leídas automáticamente y verificadas: Nexus/ENERGIA, Iberdrola Clientes,
  Octopus y Factor Energía. Ver `sistema/PERFILES_FACTURA.md`.
- Las instrucciones del Proyecto están en **7.388 de 8.000** caracteres; la versión corta en
  **3.998 de 4.000**.

```bash
python tools/generar_paquete_chatgpt.py   # tras editar cualquier skill
python eval/run.py                        # antes de entregar cualquier cosa
```

## Antes de subir cambios: lo que no puede acabar aquí

`.gitignore` ya excluye estas rutas. **No las fuerces con `git add -f`:**

| Qué | Por qué |
|---|---|
| `precios.json` y las fichas de `bandeja/precios/` | precios del área de Iberdrola, caducan |
| facturas, SIPS y presupuestos de `bandeja/` | datos personales de clientes (RGPD) |
| `metricas/indice_informes.csv` | contiene clientes, CIF, CUPS e importes |
| documentos generados (informes, presupuestos, actas) | son entregables de cliente |

La forma segura de añadir una factura de muestra para un perfil nuevo está en
`sistema/PERFILES_FACTURA.md`: se usa en local mientras se escribe el perfil y **no se sube**.

## Licencia y autoría

Obra de **Andrés Galeano** (NIE Z0002918W), cedida a B&M Asesores Energéticos, S.L. mientras dure
la relación. Condiciones completas en [LICENSE.md](LICENSE.md).

Los documentos generados para clientes se emiten a nombre del **comercial que los firma**, con sus
datos: cualquier comercial de B&M usa estas skills con su propio nombre, teléfono y correo.