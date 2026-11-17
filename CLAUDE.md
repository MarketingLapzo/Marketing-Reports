# Instrucciones para Claude · Marketing-Reports (Lapzo)

Quien trabaja aquí es la Content & Social Media Specialist de Lapzo. No programa:
explícale todo en español, sin jerga técnica, y encárgate tú de Git.

## De dónde salen los datos

| Red | Fuente | Nota |
|---|---|---|
| **LinkedIn** | **HubSpot** (Social) | Nunca desde Metricool (ahí requiere plan de pago). HubSpot no da clics ni seguidores: márcalos como "no disponible". |
| **Instagram, Facebook, TikTok** | **Metricool** (conector MCP) | Si Metricool no está conectado, avisa y pide conectarlo en claude.ai → Connectors y abrir un chat nuevo. No uses otra fuente en su lugar. |
| **Meta Ads (pagado)** | Conector de Facebook Ads | |

- Nunca inventes ni estimes cifras. Si un dato no existe en la fuente, dilo.
- Mismas definiciones para todas las redes:
  - Interacciones = likes + comentarios + compartidos.
  - Tasa de interacción = interacciones ÷ impresiones.
- Periodo por defecto: el mes calendario anterior completo.

## Dónde se guarda cada cosa

- Reporte de redes orgánicas: `rrss/AAAA-MM/`
- Reportes de Meta Ads: `meta-ads/AAAA-MM/`
- Lo aprendido de cada mes: `APRENDIZAJES.md` (lo más reciente arriba)
- Cada reporte nuevo se agrega a la tabla del `README.md`.

## Al terminar un trabajo: SIEMPRE preguntar antes de subir

Cuando termines un reporte o un análisis, **pregunta cada vez**:

> "¿Subimos a `main` el reporte y lo aprendido?"

- Si dice que sí: guarda el reporte en su carpeta del mes, agrega los aprendizajes
  a `APRENDIZAJES.md`, actualiza el `README.md` y sube todo directo a `main`
  (no dejes ramas sueltas `claude/...`). Confirma con el link de lo que quedó.
- Si dice que no: no subas nada y recuérdale que lo hecho se pierde al cerrar el chat.
- Nunca subas a `main` sin esa confirmación.

## Cruce con la parrilla

Al analizar, clasifica cada publicación por **pilar y formato** según el repo/plugin
`Lapzo-contenido-RRSS`. Los aprendizajes deben decir qué tipo de contenido repetir,
ajustar o dejar de hacer, para usarlos al armar la parrilla del mes siguiente.
