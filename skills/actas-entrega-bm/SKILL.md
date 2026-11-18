---
name: actas-entrega-bm
description: >
  Redacta actas de entrega y devolución de bienes de la empresa (portátiles,
  teléfonos, vehículos, llaves, mandos, EPI, documentación) para que las firme un
  empleado o un tercero, en PDF y DOCX. Usar cuando se pida un acta de entrega, un
  acta de devolución, un recibo de material, o documentar la retirada de un equipo
  al finalizar una relación laboral o un servicio.
license: Propietaria · Andrés Galeano · ver LICENSE.md
metadata:
  author: Andrés Galeano (NIE Z0002918W)
  owner: Andrés Galeano
  licensee: B&M Asesores Energéticos, S.L.
  version: "1.0"
---

# Actas de entrega y devolución · B&M

Un acta hace dos cosas: deja constancia de qué se entrega y **protege a B&M** si el bien no vuelve. Es un documento breve, de una página, que firma quien entrega y quien recibe.

## Usa los datos del comercial que emite, no los de Andrés

Este documento **no es exclusivo de Andrés Galeano**: cualquier comercial de B&M lo emite con **su nombre, su teléfono y su correo**. Si no constan, pídelos antes de generar el documento.

- Bloque «Quien entrega»: `[Nombre del comercial] · B&M Asesores Energéticos, S.L.`
- Firma: pie con el nombre del comercial y **el contacto general de la empresa** (Av. Ribera, 8 bajo · 46500 Puerto de Sagunto (Valencia) · info@bmae.es · 962 674 769).
- Nunca dejes el nombre de otro comercial por defecto ni firmes con el de Andrés si el acta la emite otra persona.

## Estructura (una página)

1. **Cabecera**: logo B&M, línea navy y epígrafe «DOCUMENTO DE ENTREGA Y RECEPCIÓN».
2. **Título**: `ACTA DE ENTREGA` o `ACTA DE DEVOLUCIÓN`, con un subtítulo que describa el acto en una línea.
3. **Datos del acto**: fecha, lugar, quién entrega, quién recibe (en blanco para firmar a mano si aún no se conoce).
4. **Elementos entregados**: tabla con nº, elemento, descripción y cantidad.
5. **Detalle del equipo principal** (si lo hay): modelo, procesador o características, **número de serie** y accesorios, con líneas en blanco para completar a mano.
6. **Manifestación**: cuatro o cinco compromisos, en este orden: uso adecuado y custodia; devolución cuando se requiera o al terminar la relación; carácter personal e intransferible de llaves y mandos; comunicación inmediata de avería, pérdida o sustracción; la entrega no transmite la propiedad.
7. **Observaciones**: recuadro en blanco.
8. **Firmas**: dos columnas, ENTREGA (con el nombre del comercial) y RECIBE (en blanco), cada una con línea de firma.
9. **Pie**: razón social, dirección, correo, teléfono y «Página 1 de 1».

## Reglas

- **Nunca inventes números de serie, modelos ni importes**: si no constan, se dejan líneas en blanco para rellenar en el acto.
- Si el acta es de **devolución**, invierte el sentido: quien entrega es el empleado o tercero y quien recibe es B&M. La manifestación cambia a «los elementos se devuelven en el estado que se describe» y se añade un campo de estado (correcto / con desperfectos / no devuelto).
- Los elementos de varios tipos se agrupan por naturaleza (informático, acceso, vehículo, documentación) sin cambiar la numeración.
- Una página. Si hay muchos elementos, se reduce la descripción, no la letra.
- Se entrega en **PDF para firmar** y en **DOCX para editar** si el cliente lo pide.
- El logo: **solo B&M**. En actas no va el logo de Iberdrola.

## Ejemplos de elementos

Portátil (marca, modelo, nº de serie, cargador, caja) · teléfono móvil y SIM · vehículo (matrícula, kilómetros, documentación, tarjeta de combustible) · llaves de oficina o nave · mando de alarma · mando de puerta automática · EPI · herramientas · tarjeta de visita o de acceso · documentación y expedientes.

## Verificación

1. Sentido correcto: ENTREGA lo de B&M y RECIBE la persona, o al contrario si es devolución.
2. Nombre del comercial emisor correcto en el bloque «Quien entrega» y en la firma.
3. Una página, sin cortes, con pie visible.
4. Campos que no constan, en blanco para rellenar a mano.

## Recursos

- `references/acta_entrega.md`: bloques y textos legales completos, versión entrega y versión devolución.
- `assets/acta_base.html`: plantilla de una página con la identidad de B&M, preparada para PDF y DOCX.
