# Instrucciones para Claude · Marketing-Reports (Lapzo)

Quien trabaja aquí es la Content & Social Media Specialist de Lapzo. No programa:
explícale todo en español, sin jerga técnica, y encárgate tú de Git.

## De dónde salen los datos

| Red | Fuente | Nota |
|---|---|---|
| **LinkedIn** | **HubSpot** (Social) | Nunca desde Metricool (ahí requiere plan de pago). HubSpot no da clics ni seguidores: márcalos como "no disponible". |
| **Instagram, Facebook, TikTok** | **Metricool** (conector MCP) | Si Metricool no está conectado, avisa y pide conectarlo en claude.ai → Connectors y abrir un chat nuevo. No uses otra fuente en su lugar. Si Metricool sí está conectado pero le falta un dato o una publicación que HubSpot sí tiene (por ejemplo, comentarios y compartidos de reels de Facebook o historias), complétalo con HubSpot y márcalo en el reporte como «de HubSpot». Lo mismo si Metricool se queda atrás en una publicación (no se ha actualizado y da una cifra mucho menor que HubSpot, por ejemplo menos de la mitad o 0): usa la de HubSpot, márcala «de HubSpot» y anota en el reporte qué pasó. Las diferencias pequeñas en reels de Facebook no cuentan: Metricool da reproducciones y HubSpot impresiones. |
| **Meta Ads (pagado)** | Conector de Facebook Ads | |

- Nunca inventes ni estimes cifras. Si un dato no existe en la fuente, dilo.
- No descargues ni abras archivos de video de Metricool (ni de otra fuente) para medir su duración u otro dato. La usuaria lo autorizó solo una vez, el 23 de noviembre de 2026, para los reels de noviembre. En adelante, la duración de los reels de Instagram y Facebook se marca "no disponible", salvo que usen el mismo archivo que su TikTok o que la usuaria la dé.
- Mismas definiciones para todas las redes:
  - Interacciones = likes + comentarios + compartidos.
  - Tasa de interacción = interacciones ÷ impresiones.
- Periodo por defecto: el mes calendario anterior completo.

## Dónde se guarda cada cosa

- Reporte de redes orgánicas: `rrss/AAAA-MM/`
- Reportes de Meta Ads: `meta-ads/AAAA-MM/`
- Lo aprendido de cada mes: `APRENDIZAJES.md` (lo más reciente arriba)
- Cada reporte nuevo se agrega a la tabla del `README.md`.

## Chats de reportes con dos repos

En los chats de reportes se abren dos repos, los dos en su rama `main`:

| Repo | Papel | ¿Se modifica? |
|---|---|---|
| **Marketing-Reports** (este) | Donde se trabaja: reportes, leads, aprendizajes y el sitio. | Sí, con la regla de abajo. |
| **Lapzo-contenido-RRSS** | Referencia: pilares, formatos, voz de marca, cómo se responde y reglas del registro de leads. Manda sobre el plugin instalado. | Solo si un aprendizaje cambia cómo se hace el contenido o cómo se responde: se propone el cambio en la skill que corresponde y se sube solo con visto bueno. |

- Lo que mide (cifras, hipótesis, qué funcionó) va solo en Marketing-Reports.
- Lo que cambia la forma de trabajar (una respuesta aprobada, una regla del registro, un formato que se deja) va también en Lapzo-contenido-RRSS.
- Al preguntar si se sube, nombra siempre de qué repo es el `main`: "¿Subimos al `main` de Marketing-Reports…?" o "¿Subimos al `main` de Lapzo-contenido-RRSS…?". Si son los dos, pregunta por los dos.

## Al terminar un trabajo: SIEMPRE preguntar antes de subir

Cuando termines un reporte o un análisis, **pregunta cada vez**:

> "¿Subimos al `main` de Marketing-Reports el reporte y lo aprendido?"

- Si dice que sí: guarda el reporte en su carpeta del mes, agrega los aprendizajes
  a `APRENDIZAJES.md`, actualiza el `README.md` y sube todo directo a `main`
  (no dejes ramas sueltas `claude/...`). Confirma con el link de lo que quedó.
- Si dice que no: no subas nada y recuérdale que lo hecho se pierde al cerrar el chat.
- Nunca subas a `main` sin esa confirmación.

## OKRs de contenido (pestaña `okrs/`)

La pestaña OKRs muestra el avance del plan de OKRs Q4 2026 de la usuaria. Se regenera con `python3 herramientas/generar_rrss.py`; los números fijos están en `OKR` de `herramientas/datos_rrss.py`.

- **KR1 · Piezas al mes** (meta 25+/mes, 75 en el trimestre; línea base 5): una pieza cuenta una vez aunque salga en varias redes. Los anuncios BOFU se suman por mes en `OKR["bofu"]` (octubre: 5 de AI Course Builder). Las 5 piezas de TaaS de octubre no cuentan y se muestran como dato punteado («+5 de TaaS que no se contaron este mes»); las nuevas de TaaS (P24 a P28) cuentan cuando se publiquen.
- **KR2 · Engagement**: se muestra como % de crecimiento de las interacciones totales (todas las redes) del mes en curso contra los mismos días del mes anterior (del 1 al día del corte), con la gráfica de interacciones totales por semana y los comentarios del mes. Lo que importa es que vaya subiendo y que haya comentarios (decidido el 23 nov 2026; antes era promedio por publicación).
- **KR3 · Leads** (meta 1+/semana): cuenta como lead cada contacto de la hoja «Registro de leads orgánicos (redes)» que ya tiene teléfono o correo (o ambos), haya tenido seguimiento de Ventas o no. Sin teléfono ni correo sigue siendo contacto.
- **KR4 · Reporte semanal** (meta 100 %): cada semana con reporte guardado en `rrss/semanal/` cuenta, desde el 10 de noviembre de 2026.
- **KR5 · Edición de video automatizada**: cumplido al 100 % (confirmado el 23 de noviembre de 2026). Solo cambia si la usuaria dice otra cosa.
- Cada lunes, con «Corre la semana», se actualiza la pestaña y en el resumen se pregunta si hubo anuncios BOFU nuevos para sumarlos.
- No se escriben notas sobre acuerdos con el líder: solo el dato.

## Cruce con la parrilla

Al analizar, clasifica cada publicación por **pilar y formato** según el repo/plugin
`Lapzo-contenido-RRSS`. Los aprendizajes deben decir qué tipo de contenido repetir,
ajustar o dejar de hacer, para usarlos al armar la parrilla del mes siguiente.

## Skills y reglas de contenido

Para pilares, tipos de contenido, formatos y cómo leer la hoja
"Planeación y Seguimiento de Contenidos", usa **solo** el plugin `lapzo-contenido-rrss`.

- Si hay duda o el plugin parece desactualizado, manda lo que diga el repo
  `MarketingLapzo/Lapzo-contenido-RRSS` (rama `main`).
- No uses otras skills de Lapzo: `lapzo-context`, `manual-rrss-lapzo`, `lapzo-design`,
  `lapzo-rrss-referencia`, `lapzo-ads-copy`, `lapzo-icps`, `calendario-industrias-lapzo`,
  `lapzo-outbound-*`, `lapzo-mkt-brief-daily`.
