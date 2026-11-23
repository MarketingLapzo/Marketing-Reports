# Marketing Reports · Lapzo

Reportes de marketing de Lapzo publicados como páginas estáticas (GitHub Pages).

| Reporte | Ruta | Periodo |
|---|---|---|
| OKRs de contenido Q4 2026 | [`okrs/`](okrs/) | Avance de los 5 resultados clave, actualizado cada lunes |
| Leads de redes (atendidos por Marketing) | [`leads/`](leads/) | Q4 2026, desde la hoja «Registro de leads orgánicos (redes)» · sin datos de contacto |
| Redes sociales · reporte semanal | [`rrss/semanal/2026-11-16/`](rrss/semanal/2026-11-16/) | 16 – 22 nov 2026 (comparado con 9 – 15 nov) |
| Redes sociales · reporte semanal | [`rrss/semanal/2026-11-10/`](rrss/semanal/2026-11-10/) | 10 – 16 nov 2026 (comparado con 3 – 9 nov) |
| Redes sociales orgánicas · noviembre 2026 (parcial) | [`rrss/2026-11/`](rrss/2026-11/) | 1 – 22 nov 2026 (se reemplaza con el mes completo en diciembre) |
| Redes sociales orgánicas · octubre 2026 | [`rrss/2026-10/`](rrss/2026-10/) | 1 – 31 oct 2026 |
| Redes sociales orgánicas · septiembre 2026 | [`rrss/2026-09/`](rrss/2026-09/) | 1 – 30 sep 2026 (actividad desde el 19 sep) |

Cada carpeta de redes trae la página del reporte (`index.html`) y el detalle de cada publicación
en `publicaciones.csv`, que se abre en Excel o Google Sheets.
Los reportes de Meta Ads irán en `meta-ads/AAAA-MM/`. Las historias de Instagram y Facebook todavía no se incluyen en los reportes (próximamente).

## Aprendizajes

Lo que aprendemos de cada reporte se registra en [`APRENDIZAJES.md`](APRENDIZAJES.md).

## Cómo verlos

El sitio tiene una **portada** (`index.html`) con las cifras del mes en curso y tarjetas para cada reporte, un **menú fijo** en todas las páginas, una página de **aprendizajes e hipótesis** (`aprendizajes/`) y un botón **Descargar PDF** en cada reporte. Todo se genera con `python3 herramientas/generar_rrss.py`.

- **GitHub Pages:** en *Settings → Pages*, elige *Deploy from a branch*, la rama `main` y la carpeta `/ (root)`. El índice queda en `https://marketinglapzo.github.io/Marketing-Reports/`.
- **En local:** abre `index.html` en el navegador. Las páginas no necesitan internet.

## Datos

Cada reporte es una instantánea: los datos van incrustados en la página al momento de generarla.
Interacciones = likes + comentarios + compartidos; tasa de interacción = interacciones ÷ impresiones.

| Red | Fuente | Nota |
|---|---|---|
| LinkedIn | HubSpot (Social) | HubSpot no da clics ni seguidores: aparecen como "no disponible". |
| Instagram, Facebook, TikTok | Metricool (marca go_lapzo) | Lo que Metricool no tiene y HubSpot sí (por ejemplo, comentarios y compartidos de reels de Facebook) se completa con HubSpot y se marca «de HubSpot». Metricool no tiene historial de seguidores de TikTok. |
| Meta Ads (pagado) | Facebook Ads | |

Los reportes de redes se generan con `herramientas/generar_rrss.py` (seguidores, aprendizajes y diseño)
a partir de `herramientas/datos_rrss.py` (publicaciones y su clasificación por pilar y modo).
