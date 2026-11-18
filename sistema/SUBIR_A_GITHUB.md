# Cómo subir esto a GitHub

Fecha: 21/07/2026 · Autor: Andrés Galeano (NIE Z0002918W)

Dos caminos. El primero es para quien no ha usado git nunca; el segundo, si ya lo tienes instalado.

---

## Antes de nada: qué NO va a subir

Ya está resuelto en `.gitignore`, pero conviene saberlo:

| Qué | Por qué se queda fuera |
|---|---|
| `precios.json` | precios del área de Iberdrola: caducan y son información restringida |
| `bandeja/precios/*.txt` | lo mismo |
| facturas, SIPS y presupuestos de `bandeja/` | datos personales de clientes (RGPD) |
| `metricas/indice_informes.csv` | clientes, CIF, CUPS e importes |
| informes, presupuestos y actas generados | entregables de cliente |

Si alguna vez necesitas subir una factura de muestra para enseñar cómo funciona un perfil nuevo,
**anónima primero**: cambia titular, CIF, CUPS, dirección e importes.

---

## Camino 1 · Sin instalar nada (GitHub Desktop o la web)

1. Crea el repositorio en GitHub: **New repository** → nombre `skills-bm` → **Private** →
   sin README ni licencia (ya los trae la carpeta) → Create.
2. Instala **GitHub Desktop** (gratis, Windows y macOS) y entra con tu cuenta.
3. **File → Add local repository** → selecciona esta carpeta. Si dice que no es un repositorio,
   acepta **create a repository**.
4. Escribe el resumen del primer commit: `Paquete inicial de skills B&M` → **Commit to main**.
5. **Publish repository**. Deja marcado **Keep this code private**.

Hecho. A partir de aquí, cada cambio son dos clics: **Commit** y **Push**.

---

## Camino 2 · Con git desde la consola

```bash
cd ruta/a/esta/carpeta

git init -b main
git add .
git commit -m "Paquete inicial de skills B&M: 7 skills, 15 pruebas y lectura de facturas"

# crea antes el repositorio vacío en GitHub y copia aquí su URL
git remote add origin https://github.com/TU-USUARIO/skills-bm.git
git push -u origin main
```

Si te pide usuario y contraseña, la contraseña **no vale**: GitHub exige un *token* o, mejor,
configurar una clave SSH.

### Con token (lo más rápido)

1. GitHub → **Settings → Developer settings → Personal access tokens → Tokens (classic)** →
   Generate new token → marca `repo` → copia el token (solo se ve una vez).
2. En el `push`, cuando pida contraseña, pega el token.

### Con clave SSH (lo cómodo a la larga)

```bash
ssh-keygen -t ed25519 -C "tu-correo@ejemplo.com"    # Enter a todo
cat ~/.ssh/id_ed25519.pub                            # copia la salida
# GitHub → Settings → SSH and GPG keys → New SSH key → pega
git remote set-url origin git@github.com:TU-USUARIO/skills-bm.git
```

---

## Primera comprobación después de subirlo

En otro ordenador, o en una carpeta limpia:

```bash
git clone https://github.com/TU-USUARIO/skills-bm.git
cd skills-bm
pip install pymupdf
cp precios.ejemplo.json precios.json     # y rellena con la hoja del día
python eval/run.py                       # tiene que dar todo en verde
```

En Windows basta con hacer doble clic en `comprobar.bat`.

Si `eval/run.py` da algún caso en rojo, **no entregues documentos** hasta arreglarlo.

---

## Cómo trabajar a partir de aquí

| Cuándo | Qué hacer |
|---|---|
| Cambias una regla o un texto | edita en `skills/`, luego `python tools/generar_paquete_chatgpt.py`, luego `python eval/run.py` |
| Cambian los precios | `python tools/cargar_precios.py bandeja/precios/ficha_AAAAMMDD.txt` (**no se sube**) |
| Añades una comercializadora | nuevo perfil en `tools/perfiles/` + un caso en `eval/casos.json` |
| Encuentras un error en un informe real | una línea nueva en `metricas/bitacora.md` **antes** de corregir el documento |
| Entregas un informe | `python tools/indice_informes.py --anadir ...` (el índice **no se sube**) |

Antes de cada push:

```bash
python eval/run.py
git status        # comprueba que no aparece ningún PDF, ni precios.json, ni el índice
```

---

## Si el repositorio va a ser compartido con más comerciales

- **Privado** mientras el paquete sea la ventaja competitiva de B&M.
- Cada comercial clona el repo y pone **su nombre y sus datos** en el emisor de los documentos: el
  paquete no trae el nombre de nadie por defecto.
- El `LICENSE.md` deja claro quién es el autor y las condiciones. No lo borres al hacer fork.
- Si alguien va a tocar el código, mejor una rama por persona y una revisión antes de `main`. Con
  `eval/run.py` en verde como condición para aceptar el cambio.