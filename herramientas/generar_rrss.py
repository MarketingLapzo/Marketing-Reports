# Genera los reportes mensuales de redes orgánicas (rrss/AAAA-MM/index.html y publicaciones.csv)
# a partir de herramientas/datos_rrss.py. Uso: python3 herramientas/generar_rrss.py
import csv, html, os, statistics, sys
sys.path.insert(0, os.path.dirname(__file__))
import datos_rrss as d
# Las historias quedan fuera de estos reportes por ahora (próximamente).
d.P = [p for p in d.P if p["formato"] != "Historia" and p["url"] not in d.BORRADAS]

RAIZ = os.environ.get("SALIDA") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ARTIFACT=1 genera la versión para la página privada de Claude (sin botón de PDF ni enlace al CSV).
MODO_ARTIFACT = os.environ.get("ARTIFACT") == "1"
REDES = ["LinkedIn", "Instagram", "Facebook", "TikTok"]
COLOR = {"LinkedIn": "var(--c-li)", "Instagram": "var(--c-ig)", "Facebook": "var(--c-fb)", "TikTok": "var(--c-tt)"}
FORMA = {"LinkedIn": "cuadro", "Instagram": "circulo", "Facebook": "rombo", "TikTok": "triangulo"}
MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
EXTRAIDO = "23 de noviembre de 2026"
CORTE = "2026-11-22"  # último día con datos

ATIPICOS = set()  # ya no se separa ninguna publicación

MESES = [
    {"clave": "2026-09", "titulo": "Septiembre 2026", "periodo": "1 – 30 sep 2026",
     "nota_periodo": "La primera publicación que registran Metricool y HubSpot es del 19 de septiembre, así que el mes tiene 12 días de actividad."},
    {"clave": "2026-10", "titulo": "Octubre 2026", "periodo": "1 – 31 oct 2026", "nota_periodo": ""},
    {"clave": "2026-11", "titulo": "Noviembre 2026 (parcial)", "periodo": "1 – 22 nov 2026",
     "nota_periodo": "Mes en curso: este reporte se reemplaza con el de noviembre completo a partir del 1 de diciembre."},
]

# Aprendizajes de la atención de mensajes y leads de redes (no salen de las métricas).
APRENDIZAJES_ATENCION = [
 ("18 nov 2026", "<b>Contacto no es lo mismo que lead.</b> Un contacto es alguien que escribe; se vuelve lead cuando ya tenemos sus datos (correo empresarial, teléfono y empresa) y se pasa a Ventas. En Q4 van 10 contactos y 4 leads."),
 ("18 nov 2026", "<b>Si Ventas tarda, el prospecto se queja en público.</b> Un lead de AI Course Builder esperó 16 días su acceso y lo escribió en los comentarios. Al pasar un lead, hay que acordar con Ventas quién lo contacta y por qué medio, y decírselo al prospecto."),
 ("18 nov 2026", "<b>En público, no repetir la misma respuesta.</b> Si ya se dijo «te escribimos por privado para dar seguimiento», la siguiente respuesta debe decir el paso concreto (por ejemplo, que Ventas lo va a llamar)."),
 ("18 nov 2026", "<b>Los mensajes de la página pueden caer en «Solicitudes de mensajes».</b> Si alguien pregunta en público dónde le escribimos, se le dice que fue por Messenger y que revise esa carpeta."),
 ("18 nov 2026", "<b>Al pedir datos por mensaje directo:</b> en viñetas y solo lo necesario (correo empresarial, teléfono y nombre de la empresa), con el aviso de privacidad correcto: lapzo.com/avisodeprivacidad (no lapzo.co)."),
 ("18 nov 2026", "<b>Casi todos los contactos vienen de anuncios.</b> 9 de los 10 contactos llegaron por un anuncio de Facebook. Anotar en la hoja el anuncio de origen (hay 3 pendientes) permite saber cuál trae más leads."),
]

# Aprendizajes de planeación (cómo se arma la parrilla; no salen de las métricas).
APRENDIZAJES_PLANEACION = [
 ("18 nov 2026", "<b>Antes de programar un post en LinkedIn, compararlo con el último que salió.</b> P8 (cursos terminados que no se aplican) chocaba con P15, publicado el 17 nov (cursos que no se terminan): las dos dudan de los cursos completados como medida, usan el formato de «tres» y el mismo cierre. Como en LinkedIn cada post llega a unas 200–300 personas, es probable que sean las mismas. P8 se movió al martes 24 nov."),
 ("18 nov 2026", "<b>Las piezas BOFU Ads no se publican como post orgánico</b>, aunque su Plataforma diga LinkedIn (P5 y P6)."),
 ("18 nov 2026", "<b>Prueba de cierre:</b> P8 cerrará con una pregunta que se contesta con una palabra (aplicación, desempeño o resultados) y sin «Te leemos en comentarios». Sirve para comprobar la hipótesis 3 («Mucho alcance, pero nadie conversa»)."),
]

NOTAS = {  # notas del equipo que no salen de las fuentes de datos
    "2026-10": "Octubre cerró con 19 piezas orgánicas. Aparte, se hicieron 5 anuncios BOFU de AI Course Builder (pagados), que no se incluyen en este reporte porque es solo de redes orgánicas.",
}
NOTAS_DATO = {  # dato extra junto a la nota del equipo (con borde punteado)
    "2026-10": "+5 de TaaS que no se contaron este mes",
}

SEGUIDORES = {  # neto del mes; None = no disponible
    "2026-09": {"Facebook": (26, "2,409 → 2,435"), "Instagram": (26, "29 ganados, 3 perdidos")},
    "2026-10": {"Facebook": (12, "2,435 → 2,447"), "Instagram": (21, "28 ganados, 7 perdidos")},
    "2026-11": {"Facebook": (47, "2,447 → 2,494 al 21 nov"), "Instagram": (23, "29 ganados, 6 perdidos, al 21 nov · 656 seguidores")},
}

APRENDIZAJES = {
 "2026-09": {
  "funciono": [
   "<b>Instagram · carrusel reflexivo (Experta en talento):</b> [[S2|Instagram|«No todos necesitan aprender lo mismo»]] tuvo 16.1 % de interacción y 9 compartidos.",
   "<b>LinkedIn · post reflexivo (Experta en talento):</b> [[S1|LinkedIn|«Lo que no se ve del trabajo de RH»]] llegó a 746 impresiones, la publicación de LinkedIn más vista de septiembre a noviembre.",
   "<b>Instagram · reel de Lapzi (humor):</b> [[S3|Instagram|«Lapzi: ya es viernes»]] tuvo 515 reproducciones, la pieza de Instagram más vista de los tres periodos. Ese día (25 sep) Instagram ganó 10 seguidores, el mejor día del mes.",
  ],
  "no_funciono": [
   "<b>Facebook:</b> 2.2 % de interacción contra 6.2 % de Instagram con las mismas piezas; el álbum se quedó en 1.0 %.",
   "<b>Comentarios:</b> solo 2 en todo el mes, ambos en [[S3|Instagram|el reel de Lapzi]].",
  ],
  "parrilla": [
   "<b>Repetir:</b> carruseles reflexivos del pilar Experta en talento en Instagram y su versión en LinkedIn.",
   "<b>Ajustar:</b> darle a Lapzi un espacio fijo en reels para atraer seguidores.",
   "<b>Ajustar (Facebook):</b> lo de Instagram se comparte también en Facebook; ahí el reel llegó a más gente (311) que la imagen (147) y el álbum (100), así que conviene compartir reels.",
   "<b>Dejar de hacer:</b> nada todavía; con 12 días de datos es pronto para descartar algo.",
  ],
 },
 "2026-10": {
  "funciono": [
   "<b>Modo reflexivo:</b> 3.5 % de interacción contra 2.4 % del educativo, en las cuatro redes juntas.",
   "<b>Un tema en todas las redes:</b> [[O4||«Una misma marca, cientos de experiencias»]] se adaptó en 7 piezas (carrusel, reel, video y post) y sumó 4.6 % de interacción y 26 compartidos; [[O4|TikTok|uno de los videos de TikTok]] tuvo 11 compartidos.",
   "<b>Instagram · reel:</b> 7.5 % de interacción contra 5.3 % de los carruseles.",
   "<b>TikTok:</b> [[O9|TikTok|«La rotación también es una señal»]] tuvo 671 reproducciones, el video más visto de TikTok.",
   "<b>LinkedIn:</b> [[O3|LinkedIn|«Líderes que su equipo seguiría (NOM-035)»]] llegó a 720 impresiones, con 16 likes y 5 compartidos.",
  ],
  "no_funciono": [
   "<b>Facebook:</b> 1.0 % de interacción (álbumes 1.4 %, reels 0.5 %).",
   "<b>Serie DNC 01</b> ([[O8||«¿necesidad o catálogo?»]]): 1.7 % de interacción, la más baja de los temas educativos.",
   "<b>Comentarios:</b> 4 en 53 publicaciones.",
   "<b>Alcance por publicación:</b> se publicó casi 6 veces más que en septiembre y la publicación típica alcanzó menos (mediana en LinkedIn de 646 a 474 impresiones; en Instagram de 282 a 140).",
  ],
  "parrilla": [
   "<b>Repetir:</b> temas reflexivos de Experta en talento y adaptar cada tema fuerte a reel de Instagram, video de TikTok y post de LinkedIn.",
   "<b>Ajustar:</b> cuidar que cada pieza tenga su versión para la red.",
   "<b>Ajustar (Facebook):</b> seguir compartiendo lo de Instagram, pero que cada semana haya al menos un reel: los reels llegaron a 247 personas en promedio contra 115 de los álbumes.",
   "<b>Dejar de hacer:</b> nada claro todavía; ningún formato estuvo tan abajo como para descartarlo.",
  ],
 },
 "2026-11": {
  "funciono": [
   "<b>LinkedIn · documento:</b> [[N9|LinkedIn|la guía de incorporación (onboarding)]] tuvo 3.3 % de interacción; en noviembre solo la superó [[N13|LinkedIn|el post de AI Course Builder del 20 nov]] (4.7 %).",
   "<b>Instagram:</b> reels con 7.5 % y carruseles con 6.4 % de interacción.",
   "<b>Seguidores en Facebook:</b> +47 en 21 días, contra +2 en los mismos días de octubre (+12 en todo el mes). Los días con más seguidores nuevos (+13 el 7 nov y +10 el 10 nov) son los mismos días de los dos reels de Facebook con más reproducciones.",
  ],
  "no_funciono": [
   "<b>Facebook · reels con alcance alto, poca interacción:</b> [[N7|Facebook|«¿Cuántas plataformas abres?»]] (10,377) y [[N6|Facebook|«El talento también merece números»]] (5,749) fueron las publicaciones más vistas de los tres periodos y suman el 70 % de las impresiones del mes, pero tuvieron 0.3 % de interacción.",
   "<b>Comentarios:</b> 0 en publicaciones, aunque varias cerraban con «Te leemos en comentarios».",
  ],
  "parrilla": [
   "<b>Repetir:</b> documentos en LinkedIn y reels en Instagram.",
   "<b>Ajustar:</b> repetir en Facebook la fórmula de los reels [[N6|Facebook|del 7]] y [[N7|Facebook|del 10 de noviembre]] (alcance) y cerrarlos con una pregunta para que la gente reaccione. Cambiar el cierre que pide comentarios por una pregunta más concreta.",
   "<b>Dejar de hacer:</b> cerrar con «Te leemos en comentarios» sin una pregunta concreta: hubo 0 comentarios.",
  ],
 },
}

HIPOTESIS = {
 "2026-11": [
  {"titulo": "Facebook empezó a mostrar los reels a gente que no nos sigue",
   "vemos": "Los reels de Facebook pasaron de 81 a 311 reproducciones en septiembre y octubre a [[N7|Facebook|10,377]] y [[N6|Facebook|5,749]]. Son de 2 a 4 veces más que los 2,447 seguidores de la página. El mismo reel en Instagram tuvo [[N7|Instagram|123]] y en TikTok [[N7|TikTok|180]]. Los días de esos reels (7 y 10 nov) fueron los de más seguidores nuevos en Facebook (+13 y +10).",
   "hipotesis": "El salto no viene solo del contenido, porque la misma pieza no despegó en otras redes. Lo más probable es que Facebook la recomendó a personas fuera de la página: eso explica que la vieran miles, que sumara seguidores y que casi nadie reaccionara (0.3 %), porque es gente que todavía no conoce a Lapzo.",
   "comprobar": "Publicar al menos un reel por semana en Facebook en diciembre y ver si alguno vuelve a pasar de 1,000 reproducciones. En Meta Business Suite, revisar qué parte del alcance de esos reels fue de personas que no siguen la página (Metricool no da ese dato)."},
  {"titulo": "Los reels que despegaron abren con un problema del día a día",
   "vemos": "Los dos que despegaron empiezan con una situación que vive cualquier persona de RH: [[N7|Facebook|«¿Cuántas plataformas necesitas abrir para completar un solo proceso de RH?»]] y [[N6|Facebook|«Las empresas miden sus ventas… ¿qué tan claro tienen cómo está creciendo su gente?»]]. Los reels del 12 y 15 nov se quedaron en [[N8|Facebook|565]] y [[N10|Facebook|290]]: uno abre con una afirmación sobre el sueldo y el otro presenta un producto (AI Course Builder). Pero el del 17 nov ([[N11|Facebook|192]]) también abre con una pregunta («¿Quién en tu equipo es la única persona que sabe cómo se hace algo?») y en seis días no despegó. El del 22 nov ([[N14|Facebook|233]]) abre con una afirmación y lleva un día.",
   "hipotesis": "Un inicio con una pregunta o una situación reconocible hace que la gente se quede los primeros segundos, y eso le da a Facebook la señal para mostrarlo a más personas. Ojo: son solo 6 reels y el del 17 nov no siguió el patrón, así que la pregunta inicial sola no basta y puede ser casualidad.",
   "comprobar": "En diciembre, hacer reels con el mismo tipo de inicio (pregunta sobre un problema cotidiano) y otros que abran con una afirmación o con el producto, y comparar sus reproducciones."},
  {"titulo": "Mucho alcance, pero nadie conversa",
   "vemos": "Noviembre lleva 0 comentarios en 37 publicaciones, aunque varias cerraban con «Te leemos en comentarios». Los dos reels más vistos sumaron más de 16,000 reproducciones y 53 reacciones.",
   "hipotesis": "Una invitación general a comentar no da una razón concreta para responder. Y la gente nueva que llega por los reels todavía no tiene confianza para comentar.",
   "comprobar": "Cerrar con preguntas concretas y fáciles de contestar (por ejemplo, de opción A o B) y contar los comentarios por publicación en diciembre."},
  {"titulo": "Instagram conecta, pero no está llegando a gente nueva",
   "vemos": "Instagram tiene la mejor tasa de interacción (7.1 %), pero la publicación típica llega cada vez a menos personas: 282 en septiembre, 140 en octubre y 77 en lo que va de noviembre. La cuenta suma 23 seguidores en el mes (656 en total).",
   "hipotesis": "Quien ve el contenido es sobre todo gente que ya sigue la cuenta y reacciona bien, pero Instagram no lo está mostrando fuera de ella. Parte de la baja de noviembre puede ser que las publicaciones recientes todavía están sumando vistas.",
   "comprobar": "Cerrar noviembre completo antes de concluir. En diciembre, probar en Instagram el tipo de inicio que funcionó en los reels de Facebook y comparar el alcance."},
  {"titulo": "En LinkedIn, el documento rindió más que los posts",
   "vemos": "La [[N9|LinkedIn|guía de incorporación]] en formato documento tuvo 3.3 % de interacción, contra 2.6 % de los posts (el post de AI Course Builder del 20 nov llegó a 4.7 %). La publicación típica de LinkedIn bajó de 646 impresiones en septiembre a 474 en octubre y 293 en noviembre.",
   "hipotesis": "Los documentos invitan a deslizar y guardar, y eso puede darles más interacción. Pero es un solo documento, así que todavía no es una regla.",
   "comprobar": "Publicar al menos 2 documentos en LinkedIn en diciembre y comparar su tasa con la de los posts."},
 ],
}

n = lambda v: v or 0
def inter(p): return n(p["likes"]) + n(p["com"]) + n(p["sh"])
def tasa(ps):
    i = sum(n(p["imp"]) for p in ps)
    return (100 * sum(inter(p) for p in ps) / i) if i else None
def f_int(v): return "—" if v is None else f"{v:,.0f}"
def f_pct(v): return "—" if v is None else f"{v:.1f} %"
def fecha(s): y, m, dd = s.split("-"); return f"{int(dd)} {MES[int(m)-1][:3]}"
e = html.escape
def tip(*lineas): return e("\n".join(lineas), quote=True)

def desglose(ps):
    """Likes, comentarios y compartidos; None si la fuente no da el dato para ninguna."""
    def suma(k):
        vals = [p[k] for p in ps if p[k] is not None]
        return sum(vals) if vals else None
    return suma("likes"), suma("com"), suma("sh")

def desg_html(ps, compacto=False):
    l, c, sh = desglose(ps)
    if compacto:
        return (f'<span class="dg" data-tip="{tip(f"Likes: {f_int(l)}", f"Comentarios: {f_int(c)}", f"Compartidos: {f_int(sh)}")}">'
                f'<i>♥</i>{f_int(l)} <i>💬</i>{f_int(c)} <i>↗</i>{f_int(sh)}</span>')
    return f'♥ {f_int(l)} likes · 💬 {f_int(c)} comentarios · ↗ {f_int(sh)} compartidos'

def resumen(ps):
    return dict(n=len(ps), imp=sum(n(p["imp"]) for p in ps), int=sum(inter(p) for p in ps),
                com=sum(n(p["com"]) for p in ps), sh=sum(n(p["sh"]) for p in ps), er=tasa(ps),
                med=statistics.median([n(p["imp"]) for p in ps if p["formato"] != "Historia"] or [0]) if ps else None)

def marca(red, x, y, r, extra=""):
    """Marca con forma distinta por red (identidad no depende solo del color)."""
    st = f'style="fill:{COLOR[red]}" class="mk" {extra}'
    f = FORMA[red]
    if f == "circulo": return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" {st}/>'
    if f == "cuadro": return f'<rect x="{x-r*.9:.1f}" y="{y-r*.9:.1f}" width="{r*1.8:.1f}" height="{r*1.8:.1f}" rx="1.5" {st}/>'
    if f == "rombo": return f'<path d="M{x:.1f},{y-r*1.2:.1f}L{x+r*1.2:.1f},{y:.1f}L{x:.1f},{y+r*1.2:.1f}L{x-r*1.2:.1f},{y:.1f}Z" {st}/>'
    return f'<path d="M{x:.1f},{y-r*1.2:.1f}L{x+r*1.15:.1f},{y+r*.85:.1f}L{x-r*1.15:.1f},{y+r*.85:.1f}Z" {st}/>'

def leyenda(redes=REDES):
    sw = lambda r: f'<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">{marca(r, 7, 7, 5)}</svg>'
    return '<div class="legend">' + "".join(f'<span>{sw(r)}{r}</span>' for r in redes) + "</div>"

def tip_pub(p):
    t = tasa([p])
    return tip(f'{d.TEMAS[p["tema"]][0]}', f'{p["red"]} · {p["formato"]} · {fecha(p["fecha"])}',
               f'{f_int(p["imp"])} impresiones · {f_int(inter(p))} interacciones · {f_pct(t)}',
               "")

DEST_ACTUAL = {}
def calcular_destacados(ps):
    """Top 3 del mes en vistas, interacciones y tasa (tasa solo entre publicaciones con vistas al menos típicas)."""
    base = [p for p in ps if p["formato"] != "Historia"]
    med = statistics.median([n(p["imp"]) for p in base] or [0])
    out = {}
    for etq, cls, key, pool in [("★ Top vistas", "t-v", lambda p: n(p["imp"]), base),
                                ("★ Top interacciones", "t-i", lambda p: inter(p), base),
                                ("★ Top tasa", "t-r", lambda p: tasa([p]) or 0, [p for p in base if n(p["imp"]) >= med])]:
        for p in sorted(pool, key=lambda p: -key(p))[:3]:
            out.setdefault(p["url"], []).append((etq, cls))
    DEST_ACTUAL.clear(); DEST_ACTUAL.update(out)

def fuente_tag(p):
    if p.get("fuente") == "HubSpot":
        return ' <span class="src" data-tip="Metricool no registró esta publicación; el dato viene de HubSpot.">dato de HubSpot</span>'
    if p.get("hs"):
        return f' <span class="src" data-tip="Metricool no da {p["hs"]} de este formato; esos números vienen de HubSpot.">{p["hs"]} de HubSpot</span>'
    return ""

def url_pieza(tema, red=None, mes=None):
    """Enlace a la versión con más impresiones de una pieza (opcional: de una red y un mes)."""
    v = [p for p in d.P if p["tema"] == tema and (not red or p["red"] == red) and (not mes or p["fecha"][:7] == mes)]
    v = v or [p for p in d.P if p["tema"] == tema]
    return max(v, key=lambda p: n(p["imp"]))["url"] if v else None

def enlazar(txt, mes):
    import re
    def rep(m):
        t, r, label = m.group(1), m.group(2) or None, m.group(3)
        u = url_pieza(t, r, mes)
        return f'<a href="{e(u)}" target="_blank" rel="noopener">{label}</a>' if u else label
    return re.sub(r"\[\[([A-Z0-9]+)\|([A-Za-z]*)\|(.+?)\]\]", rep, txt)

def dest_badges(p):
    return "".join(f' <span class="tag {c}">{t}</span>' for t, c in DEST_ACTUAL.get(p["url"], []))

INICIAL = {"LinkedIn": "LI", "Instagram": "IG", "Facebook": "FB", "TikTok": "TT"}
TINTA = {"LinkedIn": "#0d2236", "Instagram": "#fff", "Facebook": "#fff", "TikTok": "#fff"}

def tabla_publicaciones(ps):
    """Agrupada por pieza (tema): fila de resumen y debajo una fila por red donde se publicó."""
    base = [p for p in ps if p["formato"] != "Historia"]
    med_imp = {r: statistics.median([n(p["imp"]) for p in base if p["red"] == r] or [0]) for r in REDES}
    med_er = {r: statistics.median([tasa([p]) or 0 for p in base if p["red"] == r] or [0]) for r in REDES}
    vals = sorted([n(p["imp"]) for p in ps], reverse=True) + [1, 1, 1]
    mx_imp = vals[2] * 1.25 if vals[0] > 4 * vals[2] else vals[0]
    mx_er = max([tasa([p]) or 0 for p in ps] + [0.1])
    grupos = {}
    for p in ps: grupos.setdefault(p["tema"], []).append(p)
    cuerpos = []
    for t, v in sorted(grupos.items(), key=lambda kv: -sum(n(p["imp"]) for p in kv[1])):
        nom, pil, modo = d.TEMAS[t]
        if t == "HIST": nom = "Historias de Instagram"
        v = sorted(v, key=lambda p: (REDES.index(p["red"]), p["fecha"]))
        ti, tn = sum(n(p["imp"]) for p in v), sum(inter(p) for p in v)
        redes_txt = ", ".join(r for r in REDES if any(p["red"] == r for p in v))
        chips = "".join(f'<a href="{e(max([p for p in v if p["red"] == r], key=lambda p: n(p["imp"]))["url"])}" target="_blank" rel="noopener" data-tip="Abrir en {r}"><span class="chip" style="background:{COLOR[r]};color:{TINTA[r]};text-shadow:none">{INICIAL[r]}</span></a>' for r in REDES if any(p["red"] == r for p in v))
        u_top = max(v, key=lambda p: n(p["imp"]))["url"]
        filas = [f'<tr class="grp-h"><td colspan="2">{chips}</td><td class="t"><a class="pz" href="{e(u_top)}" target="_blank" rel="noopener" data-tip="Abrir la versión con más impresiones"><b>{e(nom)}</b></a><div class="small">{"" if t == "HIST" else e(pil) + " · " + e(modo) + " · "}{len(v)} {"pieza" if len(v) == 1 else "piezas"} en {redes_txt}</div></td>'
                 f'<td class="l"><b>{f_int(ti)}</b> <span class="small">en total</span></td><td class="l"><b>{f_pct(tasa(v))}</b> <span class="small">en total</span></td><td class="l"><b>{f_int(tn)}</b><div>{desg_html(v, True)}</div></td></tr>']
        for p in v:
            i, tt = n(p["imp"]), tasa([p]) or 0
            wi = min(100, 100 * i / mx_imp); wt = 100 * tt / mx_er
            filas.append(
                f'<tr class="sub{" dest" if p["url"] in DEST_ACTUAL else ""}" data-red="{p["red"]}" data-imp="{i}" data-int="{inter(p)}" data-fecha="{p["fecha"]}">'
                f'<td><span class="chip" style="background:{COLOR[p["red"]]};color:{TINTA[p["red"]]};text-shadow:none">{INICIAL[p["red"]]}</span></td>'
                f'<td class="l">{fecha(p["fecha"])}</td>'
                f'<td class="t"><a href="{e(p["url"])}" target="_blank" rel="noopener">{p["red"]} · {p["formato"]}</a>{fuente_tag(p)}{dest_badges(p)}</td>'
                f'<td class="bar"><div class="track"><div class="fill{" over" if i > mx_imp else ""}" style="width:{wi:.1f}%;background:{COLOR[p["red"]]}"></div></div><span>{f_int(i)}</span></td>'
                f'<td class="bar"><div class="track"><div class="fill" style="width:{wt:.1f}%;background:{COLOR[p["red"]]}"></div></div><span>{f_pct(tt)}</span></td>'
                f'<td class="l"><b>{f_int(inter(p))}</b><div>{desg_html([p], True)}</div></td></tr>')
        cuerpos.append(f'<tbody class="grp">{"".join(filas)}</tbody>')
    botones = '<button class="on" data-f="">Todas</button>' + "".join(f'<button data-f="{r}"><span class="chip" style="background:{COLOR[r]};color:{TINTA[r]};text-shadow:none">{INICIAL[r]}</span>{r}</button>' for r in REDES)
    orden = '<label class="small">Ordenar por <select class="ord"><option value="imp">Impresiones</option><option value="er">Tasa de interacción</option><option value="int">Interacciones</option><option value="fecha">Fecha</option></select></label>'
    return (f'<div class="pubs"><div class="ctrl"><div class="seg">{botones}</div>{orden}</div>'
            f'<div class="scroll"><table class="ptab"><thead><tr><th>Red</th><th class="l">Fecha</th><th class="l">Pieza y red</th><th class="l">Impresiones</th><th class="l">Tasa de interacción</th><th class="l">Interacciones</th></tr></thead>'
            f'{"".join(cuerpos)}</table></div></div>')

def calendario_mes(ps, clave):
    import calendar
    y, m = int(clave[:4]), int(clave[5:])
    semanas = calendar.Calendar(firstweekday=0).monthdayscalendar(y, m)
    por_dia = {}
    for p in ps: por_dia.setdefault(int(p["fecha"][8:]), []).append(p)
    cab = "".join(f'<div class="dow">{x}</div>' for x in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"])
    celdas = []
    for sem in semanas:
        for dd in sem:
            if dd == 0: celdas.append('<div class="day out"></div>'); continue
            if f"{clave}-{dd:02d}" > CORTE: celdas.append(f'<div class="day future"><b>{dd}</b></div>'); continue
            q = por_dia.get(dd, [])
            if not q: celdas.append(f'<div class="day empty pick" data-day="{clave}-{dd:02d}"><b>{dd}</b></div>'); continue
            chips = ""
            for r in REDES:
                k = sum(1 for p in q if p["red"] == r)
                if k: chips += f'<span class="chip" style="background:{COLOR[r]};color:{TINTA[r]};text-shadow:none">{INICIAL[r]}{"×" + str(k) if k > 1 else ""}</span>'
            lista = [f'{fecha(f"{clave}-{dd:02d}")}: {len(q)} publicaciones'] + [f'· {p["red"]} {p["formato"].lower()}: {d.TEMAS[p["tema"]][0]}' for p in sorted(q, key=lambda p: REDES.index(p["red"]))]
            celdas.append(f'<div class="day pick" data-day="{clave}-{dd:02d}" data-tip="{tip(*lista)}"><b>{dd}</b><div class="chips">{chips}</div></div>')
    dias_con = len(por_dia); tot = min(calendar.monthrange(y, m)[1], int(CORTE[8:]) if CORTE[:7] == clave else 99)
    return f'<div class="cal">{cab}{"".join(celdas)}</div>', dias_con, tot

FORMATOS_RED = {
    "LinkedIn": ["Post", "Documento"],
    "Instagram": ["Reel", "Carrusel", "Imagen"],
    "Facebook": ["Reel", "Álbum", "Imagen", "Enlace"],
    "TikTok": ["Video"],
}

def formatos_por_red(ps, clave):
    """Una tarjeta por red con todos sus formatos y sus métricas, aunque no hayan funcionado."""
    tarjetas = []
    for r in REDES:
        q = [p for p in ps if p["red"] == r]
        filas_d = []
        for f in FORMATOS_RED[r] + sorted({p["formato"] for p in q} - set(FORMATOS_RED[r])):
            v = [p for p in q if p["formato"] == f]
            if not v:
                filas_d.append((f, None, "No se registraron historias (ni en Metricool ni en HubSpot)" if f == "Historia" else "No se publicó este mes"))
                continue
            imp = sum(n(p["imp"]) for p in v)
            filas_d.append((f, dict(n=len(v), imp=imp, prom=imp / len(v), int=sum(inter(p) for p in v), er=tasa(v), dg=desg_html(v, True)), ""))
        con = [x for x in filas_d if x[1]]
        mx_prom = max([x[1]["prom"] for x in con] + [1]); mx_er = max([x[1]["er"] or 0 for x in con] + [0.1])
        mejor_prom = max(con, key=lambda x: x[1]["prom"])[0] if len(con) > 1 else None
        mejor_er = max(con, key=lambda x: x[1]["er"] or 0)[0] if len(con) > 1 else None
        peor_er = min(con, key=lambda x: x[1]["er"] or 0)[0] if len(con) > 2 else None
        filas = []
        for f, m, nota in sorted(filas_d, key=lambda x: -(x[1]["er"] or 0) if x[1] else 1):
            if not m:
                filas.append(f'<tr class="vacio"><th scope="row">{f}</th><td colspan="4" class="l small">{nota}</td></tr>'); continue
            tags = ""
            if f == mejor_er: tags += '<span class="tag t-i">Mejor tasa</span>'
            if f == mejor_prom: tags += '<span class="tag t-v">Más alcance</span>'
            if f == peor_er and f != mejor_prom: tags += '<span class="tag t-down">Tasa más baja</span>'
            filas.append(
                f'<tr><th scope="row">{f}{("<div class=tags>" + tags + "</div>") if tags else ""}</th><td class="num">{m["n"]}</td>'
                f'<td class="bar"><div class="track sm"><div class="fill" style="width:{100*m["prom"]/mx_prom:.1f}%;background:{COLOR[r]}"></div></div><span>{f_int(m["prom"])}</span></td>'
                f'<td class="l"><b>{f_int(m["int"])}</b><div>{m["dg"]}</div></td>'
                f'<td class="bar"><div class="track sm"><div class="fill" style="width:{100*(m["er"] or 0)/mx_er:.1f}%;background:{COLOR[r]}"></div></div><span>{f_pct(m["er"])}</span></td></tr>')
        tarjetas.append(f'<div class="card net" style="border-top-color:{COLOR[r]}"><h3>{r}</h3><div class="scroll flat"><table class="ftab"><thead><tr><th>Formato</th><th>Pub.</th><th class="l">Impresiones promedio</th><th class="l">Interacciones (♥ likes · 💬 comentarios · ↗ compartidos)</th><th class="l">Tasa</th></tr></thead><tbody>{"".join(filas)}</tbody></table></div></div>')
    return '<div class="fgrid">' + "".join(tarjetas) + "</div>"

def barras_h(items, fmt=f_pct, ancho=680, lw=230):
    """items: (etiqueta, valor, color, detalle). Barras horizontales ordenadas."""
    items = [it for it in items if it[1] is not None]
    rw, bh, gap = 64, 18, 10
    corta = lambda t: t if len(t) * 7.4 < lw - 8 else t[: int((lw - 8) / 7.4) - 1] + "…"
    H = len(items) * (bh + gap) + 4
    mx = max([it[1] for it in items] + [0.0001])
    o = [f'<svg viewBox="0 0 {ancho} {H}" class="chart{" wide" if ancho > 500 else ""}" role="img">']
    for i, it in enumerate(items):
        lab, v, col, det = it[:4]; url = it[4] if len(it) > 4 else None
        y = i * (bh + gap) + 2; w = max(2, (ancho - lw - rw) * v / mx)
        o.append(f'<g data-tip="{tip(lab, det)}"><text x="0" y="{y+13}" class="lab">{e(corta(lab))}</text>'
                 f'<rect x="{lw}" y="{y}" width="{w:.1f}" height="{bh}" rx="3" style="fill:{col}"/>'
                 f'<text x="{lw+w+6:.1f}" y="{y+13}" class="val">{fmt(v)}</text><rect x="0" y="{y-4}" width="{ancho}" height="{bh+8}" class="hit"/></g>')
        if url: o[-1] = f'<a href="{e(url)}" target="_blank" rel="noopener">{o[-1]}</a>'
    o.append("</svg>")
    return "".join(o)

def seguidores_dia(clave):
    """Seguidores netos por día: Facebook e Instagram en filas (misma escala)."""
    dias = sorted(k for k in d.FB_TOTAL if k[:7] == clave)
    fb = {k: d.FB_TOTAL[k] - d.FB_TOTAL[prev] for prev, k in zip(sorted(d.FB_TOTAL)[:-1], sorted(d.FB_TOTAL)[1:]) if k[:7] == clave}
    ig = {k: v[0] - v[1] for k, v in d.IG_DIA.items() if k[:7] == clave}
    ult = int(dias[-1][8:]) if dias else 30
    import calendar
    ultimo = calendar.monthrange(int(clave[:4]), int(clave[5:]))[1]
    W, ml, mr, rh = 680, 82, 12, 84
    H = rh * 2 + 46
    mx = max([abs(v) for v in list(fb.values()) + list(ig.values())] + [1])
    X = lambda dd: ml + (dd - 1) / ultimo * (W - ml - mr)
    bw = (W - ml - mr) / ultimo - 2
    o = [f'<svg viewBox="0 0 {W} {H}" class="chart wide" role="img" aria-label="Seguidores netos por día">']
    for i, (red, serie) in enumerate([("Facebook", fb), ("Instagram", ig)]):
        base = 8 + rh * i + rh - 14
        o.append(f'<text x="0" y="{base-rh/2+10}" class="lab">{red}</text><line x1="{ml}" x2="{W-mr}" y1="{base}" y2="{base}" class="axis"/>')
        for k, v in sorted(serie.items()):
            dd = int(k[8:]); h = (rh - 26) * abs(v) / mx
            y = base - h if v >= 0 else base
            o.append(f'<g class="pick" data-day="{k}" data-tip="{tip(red + " · " + fecha(k), f"{v:+d} seguidores netos", "Haz clic para ver qué se publicó")}"><rect x="{X(dd)+1:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h,1):.1f}" rx="2" style="fill:{COLOR[red]}"/>'
                     + (f'<text x="{X(dd)+1+bw/2:.1f}" y="{y-3:.1f}" text-anchor="middle" class="val dval">+{v}</text>' if v > 0 else f'<text x="{X(dd)+1+bw/2:.1f}" y="{base+max(h,1)+11:.1f}" text-anchor="middle" class="val dval neg">{v}</text>' if v < 0 else "")
                     + f'<rect x="{X(dd):.1f}" y="{base-rh+16}" width="{bw+2:.1f}" height="{rh-10}" class="hit"/></g>')
    for dd in range(1, ultimo + 1):
        if dd == 1 or dd % 5 == 0: o.append(f'<text x="{X(dd)+1+bw/2:.1f}" y="{H-6}" text-anchor="middle" class="tick">{dd}</text>')
    o.append("</svg>")
    return "".join(o)

def datos_dias(ps, clave):
    import json
    fb = {k: d.FB_TOTAL[k] - d.FB_TOTAL[prev] for prev, k in zip(sorted(d.FB_TOTAL)[:-1], sorted(d.FB_TOTAL)[1:]) if k[:7] == clave}
    ig = {k: v[0] - v[1] for k, v in d.IG_DIA.items() if k[:7] == clave}
    out = {}
    for k in sorted(set(fb) | set(ig) | {p["fecha"] for p in ps}):
        out[k] = {"t": fecha(k), "fb": fb.get(k), "ig": ig.get(k), "p": [
            {"r": p["red"], "f": p["formato"], "n": d.TEMAS[p["tema"]][0], "i": f_int(p["imp"]), "x": f_pct(tasa([p])), "u": p["url"], "a": [t for t, _ in DEST_ACTUAL.get(p["url"], [])]}
            for p in sorted([p for p in ps if p["fecha"] == k], key=lambda p: REDES.index(p["red"]))]}
    mejor = max(out, key=lambda k: (out[k]["fb"] or 0) + (out[k]["ig"] or 0)) if out else ""
    return json.dumps(out, ensure_ascii=False).replace("</", "<\\/"), mejor

def barras_mes(meses, valor, etiqueta):
    W, H, ml, mb, mt = 440, 200, 8, 28, 22
    vals = [[valor(m, r) for r in REDES] for m in meses]
    mx = max([v or 0 for fila in vals for v in fila] + [1])
    gw = (W - ml) / len(meses); bw = min(34, (gw - 24) / len(REDES))
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(etiqueta)}" class="chart">']
    for i, m in enumerate(meses):
        x0 = ml + i * gw + (gw - bw * len(REDES)) / 2
        for j, r in enumerate(REDES):
            v = vals[i][j]; x = x0 + j * bw
            if v is None:
                out.append(f'<text x="{x+bw/2:.1f}" y="{H-mb-5}" text-anchor="middle" class="val">n/d</text>'); continue
            h = (H - mb - mt) * v / mx; y = H - mb - h
            out.append(f'<g data-tip="{tip(r + " · " + m["titulo"], f"{v:,.0f}")}"><rect x="{x+2:.1f}" y="{y:.1f}" width="{bw-4:.1f}" height="{h:.1f}" rx="3" style="fill:{COLOR[r]}"/>'
                       f'<text x="{x+bw/2:.1f}" y="{y-5:.1f}" text-anchor="middle" class="val">{v:,.0f}</text></g>')
        out.append(f'<text x="{ml+i*gw+gw/2:.1f}" y="{H-8}" text-anchor="middle" class="lab">{e(m["titulo"].replace(" 2026", ""))}</text>')
    out.append(f'<line x1="{ml}" x2="{W}" y1="{H-mb}" y2="{H-mb}" class="axis"/></svg>')
    return "".join(out)

# ---------------------------------------------------------------- Comparación pareja con el mes en curso
# Mientras un mes va a medias, los meses anteriores se cuentan solo hasta el mismo día (del 1 al día del corte).
def dia_corte(): return int(CORTE[8:])
def dia_seg():
    """Último día del mes en curso con datos de seguidores de Facebook e Instagram."""
    k = [x for x in d.FB_TOTAL if x[:7] == CORTE[:7]] + [x for x in d.IG_DIA if x[:7] == CORTE[:7]]
    return min(int(max(k)[8:]), dia_corte()) if k else dia_corte()
def recortar(m, hasta):
    """Copia de un mes que solo cuenta del 1 al día `hasta`."""
    return dict(m, hasta=hasta, hasta_seg=min(hasta, dia_seg()), titulo=m["titulo"].replace(" 2026", "") + f" 2026 (1–{hasta})")
def del_mes(p, m):
    return p["fecha"][:7] == m["clave"] and (not m.get("hasta") or int(p["fecha"][8:]) <= m["hasta"])
def seg_de(m, r):
    """Seguidores netos de un mes (o de sus primeros días, si viene recortado). None = no disponible."""
    if not m.get("hasta_seg"):
        return (SEGUIDORES[m["clave"]].get(r) or (None,))[0]
    a, b = f'{m["clave"]}-01', f'{m["clave"]}-{m["hasta_seg"]:02d}'
    fb, ig = seg_rango(a, b)
    if r == "Facebook": return sum(fb.values()) if fb else None
    if r == "Instagram": return sum(ig.values()) if ig else None
    return None
def meses_parejos(hasta_idx):
    """Meses hasta `hasta_idx`; si el último va a medias, los anteriores se recortan al mismo día."""
    ms = MESES[: hasta_idx + 1]
    if ms[-1]["clave"] != CORTE[:7]: return ms
    return [recortar(m, dia_corte()) for m in ms[:-1]] + [dict(ms[-1], hasta_seg=None)]

# ---------------------------------------------------------------- Sección de videos
def es_video(p): return p["formato"] in ("Reel", "Video")
def seccion_videos(ps, periodo="del mes"):
    vs = sorted([p for p in ps if es_video(p)], key=lambda p: -n(p["imp"]))
    if not vs: return ""
    V = lambda p, k: d.VIDEO.get(p["url"], {}).get(k)
    seg_max = max([v for p in vs for v in (V(p, "dur"), V(p, "prom")) if v] + [10])
    escala = int(-(-seg_max // 10) * 10)  # redondeado hacia arriba a decenas
    pct = lambda v: f"{100 * v / escala:.2f}%"
    marcas = "".join(f'<span style="left:{pct(t)}">{t} s</span>' for t in range(0, escala + 1, 10))
    filas = []
    for p in vs:
        prom, dur, q3 = V(p, "prom"), V(p, "dur"), V(p, "quedan3")
        if prom is not None and dur:
            barra = f'<i class="vt" style="width:{pct(dur)}"><i class="vf" style="width:{100 * min(prom, dur) / dur:.1f}%;background:{COLOR[p["red"]]}"></i></i>'
            txt = f'Vieron <b>{prom:.1f} s</b> de {dur:g} s ({100 * prom / dur:.0f} % del video)'
        elif prom is not None:
            barra = f'<i class="vt sin" style="width:100%"><i class="vf" style="width:{pct(prom)};background:{COLOR[p["red"]]}"></i></i>'
            txt = f'Vieron <b>{prom:.1f} s</b> en promedio · no sabemos cuánto dura'
        elif dur:
            barra = f'<i class="vt" style="width:{pct(dur)}"></i>'
            txt = f'Dura {dur:g} s · Metricool no da cuánto lo vieron'
        else:
            barra = ''; txt = 'Sin datos de reproducción en Metricool'
        extra = f' <span class="tag t-v">{q3:.0f} % pasa de los 3 s</span>' if q3 is not None else ""
        filas.append(
            f'<div class="vrow"><div class="vn"><span class="chip" style="background:{COLOR[p["red"]]}">{INICIAL[p["red"]]}</span> '
            f'<a href="{e(p["url"])}" target="_blank" rel="noopener">{e(d.TEMAS[p["tema"]][0])}</a>'
            f'<div class="small">{fecha(p["fecha"])} · <b>{f_int(p["imp"])}</b> reproducciones · {f_pct(tasa([p]))} de interacción</div></div>'
            f'<div class="vb"><div class="vtrack">{barra}</div><div class="small">{txt}{extra}</div></div></div>')
    f1 = lambda v, fmt: "—" if v is None else fmt(v)
    tfilas = [f'<tr><td class="l">{p["red"]}</td><td>{fecha(p["fecha"])}</td><td class="t">{e(d.TEMAS[p["tema"]][0])}</td><td>{f_int(p["imp"])}</td><td>{f_pct(tasa([p]))}</td>'
              f'<td>{f1(V(p, "prom"), lambda v: f"{v:.1f} s")}</td><td>{f1(V(p, "dur"), lambda v: f"{v:g} s")}</td><td>{f1(V(p, "quedan3"), lambda v: f"{v:.1f} %")}</td><td>{f1(V(p, "guard"), lambda v: f"{v:,}")}</td></tr>' for p in vs]
    return (f'<h2>Videos</h2>\n<p class="lead">¿Cuánto de cada video ve la gente? Los reels y TikToks {periodo}, de más a menos reproducciones.</p>\n'
            '<div class="card"><div class="vleg"><span><i class="vt mini"></i> gris: lo que dura el video</span>'
            '<span><i class="vt mini"><i class="vf" style="width:40%;background:var(--muted)"></i></i> color: segundos que lo vieron en promedio</span>'
            '<span><i class="vt mini sin"></i> punteado: no sabemos cuánto dura</span></div>'
            f'<div class="vrow vhead"><div class="vn"></div><div class="vb"><div class="vscale">{marcas}</div></div></div>'
            + "".join(filas) +
            tabla(["Red", "Fecha", "Pieza", "Reproducciones", "Tasa", "Tiempo promedio visto", "Duración", "Pasa de los 3 s", "Guardados"], tfilas)
            + '<p class="small">De Metricool: tiempo promedio visto (Instagram y Facebook), qué parte de las vistas pasa de los primeros 3 segundos y guardados (solo Instagram), y duración (TikTok). '
            'La duración de los reels de Instagram y Facebook de noviembre se leyó del archivo de video en Metricool (o es la de su TikTok cuando usan el mismo archivo); los anteriores al 9 de noviembre no tienen archivo ahí. Metricool no da la retención completa, el porcentaje que vio el video completo ni de dónde llegaron las vistas de TikTok.</p></div>')

def dato_nota(c): return f' <span class="src">{e(NOTAS_DATO[c])}</span>' if c in NOTAS_DATO else ""

def tabla(cab, filas):
    return f'<details><summary>Ver tabla</summary><div class="scroll"><table><thead><tr>{"".join(f"<th>{c}</th>" for c in cab)}</tr></thead><tbody>{"".join(filas)}</tbody></table></div></details>'

def pagina(idx):
    import calendar
    M = MESES[idx]; clave = M["clave"]; previos = meses_parejos(idx)
    ps = [p for p in d.P if p["fecha"][:7] == clave]
    calcular_destacados(ps)
    R = resumen(ps); sin = [p for p in ps if p["url"] not in ATIPICOS]
    seg = SEGUIDORES[clave]; hay_atip = len(sin) != len(ps)
    ultimo = calendar.monthrange(int(clave[:4]), int(clave[5:]))[1]

    # Evolución
    filas = []
    for r in REDES:
        celdas = []
        for m in previos:
            q = [p for p in d.P if del_mes(p, m) and p["red"] == r]
            s = resumen(q); sg = seg_de(m, r)
            celdas.append(f'<td>{s["n"]}</td><td>{f_int(s["imp"])}</td><td>{f_pct(s["er"])}</td><td>{f_int(s["med"])}</td><td>{f"{sg:+d}" if sg is not None else "no disp."}</td>')
        filas.append(f'<tr><th scope="row">{r}</th>{"".join(celdas)}</tr>')
    cab1 = "".join(f'<th colspan="5" class="grp">{e(m["titulo"])}</th>' for m in previos)
    cab2 = "<th>Pub.</th><th>Impr.</th><th>Tasa</th><th>Mediana</th><th>Seguidores</th>" * len(previos)
    evol_tabla = f'<details><summary>Ver tabla de evolución</summary><div class="scroll"><table class="evo"><thead><tr><th></th>{cab1}</tr><tr><th>Red</th>{cab2}</tr></thead><tbody>{"".join(filas)}</tbody></table></div></details>'
    imp_mes = lambda m, r: sum(n(p["imp"]) for p in d.P if del_mes(p, m) and p["red"] == r and p["url"] not in ATIPICOS)
    er_mes = lambda m, r: tasa([p for p in d.P if del_mes(p, m) and p["red"] == r and p["url"] not in ATIPICOS])
    med_mes = lambda m, r: resumen([p for p in d.P if del_mes(p, m) and p["red"] == r])["med"]
    seg_mes = seg_de
    fmt1 = lambda v: f"{v:.1f}"

    def barras_mes_pct(meses):
        W, H, ml, mb, mt = 440, 200, 8, 28, 22
        vals = [[er_mes(m, r) for r in REDES] for m in meses]; mx = max([v or 0 for f in vals for v in f] + [1])
        gw = (W - ml) / len(meses); bw = min(34, (gw - 24) / len(REDES)); o = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Tasa de interacción por mes">']
        for i, m in enumerate(meses):
            x0 = ml + i * gw + (gw - bw * len(REDES)) / 2
            for j, r in enumerate(REDES):
                v = vals[i][j] or 0; x = x0 + j * bw; h = (H - mb - mt) * v / mx; y = H - mb - h
                o.append(f'<g data-tip="{tip(r + " · " + m["titulo"], f_pct(v))}"><rect x="{x+2:.1f}" y="{y:.1f}" width="{bw-4:.1f}" height="{h:.1f}" rx="3" style="fill:{COLOR[r]}"/><text x="{x+bw/2:.1f}" y="{y-5:.1f}" text-anchor="middle" class="val">{v:.1f}</text></g>')
            o.append(f'<text x="{ml+i*gw+gw/2:.1f}" y="{H-8}" text-anchor="middle" class="lab">{e(m["titulo"].replace(" 2026", ""))}</text>')
        o.append(f'<line x1="{ml}" x2="{W}" y1="{H-mb}" y2="{H-mb}" class="axis"/></svg>'); return "".join(o)

    # Por red
    tarjetas = []
    for r in REDES:
        q = [p for p in ps if p["red"] == r]; s = resumen(q); sg = seg.get(r)
        tarjetas.append(f'''<div class="card net" style="border-top-color:{COLOR[r]}"><h3>{r}</h3>
<dl><div><dt>Publicaciones</dt><dd>{s["n"]}</dd></div><div><dt>Impresiones</dt><dd>{f_int(s["imp"])}</dd></div>
<div><dt>Interacciones</dt><dd>{f_int(s["int"])}</dd></div><div><dt>Tasa</dt><dd>{f_pct(s["er"])}</dd></div><div style="grid-column:span 2"><dt>Desglose</dt><dd class="dd">{desg_html(q, True)}</dd></div>
<div><dt>Mediana por publicación</dt><dd>{f_int(s["med"])}</dd></div><div><dt>Seguidores</dt><dd>{("+" + str(sg[0])) if sg else "no disponible"}</dd></div></dl>
<p class="small">{e(sg[1]) if sg else ("HubSpot no da seguidores." if r == "LinkedIn" else "Metricool no tiene historial de seguidores de TikTok.")}</p></div>''')

    def grupo(clave_fn, color_fn, ancho_g=680, lw_g=230):
        g = {}
        for p in ps: g.setdefault(clave_fn(p), []).append(p)
        base = [p for p in ps if p["url"] not in ATIPICOS]
        items, filas = [], []
        for k, v in g.items():
            v2 = [p for p in v if p["url"] not in ATIPICOS]
            items.append((k, tasa(v2), color_fn(k), f'{len(v)} publicaciones · {f_int(sum(n(p["imp"]) for p in v))} impresiones · {f_int(sum(inter(p) for p in v))} interacciones'))
            filas.append(f'<tr><th scope="row">{e(k)}</th><td>{len(v)}</td><td>{f_int(sum(n(p["imp"]) for p in v))}</td><td>{f_int(sum(inter(p) for p in v))}</td><td>{f_pct(tasa(v))}</td></tr>')
        items.sort(key=lambda it: -(it[1] or 0))
        return barras_h(items, ancho=ancho_g, lw=lw_g) + tabla(["", "Pub.", "Impr.", "Interacc.", "Tasa"], filas)

    acento = "var(--mono)"
    pilares = grupo(lambda p: d.TEMAS[p["tema"]][1], lambda k: acento, 440, 190)
    modos = grupo(lambda p: d.TEMAS[p["tema"]][2], lambda k: acento, 440, 190)

    # Temas
    temas = {}
    for p in ps: temas.setdefault(p["tema"], []).append(p)
    trows = []
    for t, v in sorted(temas.items(), key=lambda kv: -sum(inter(p) for p in kv[1])):
        nom, pil, modo = d.TEMAS[t]
        piezas = ", ".join(sorted(set(f'{p["red"]} {p["formato"].lower()}' for p in v)))
        trows.append(f'<tr><th scope="row"><a href="{e(max(v, key=lambda p: n(p["imp"]))["url"])}" target="_blank" rel="noopener">{e(nom)}</a></th><td class="l">{e(pil)}</td><td class="l">{e(modo)}</td><td class="small t">{e(piezas)}</td><td>{f_int(sum(n(p["imp"]) for p in v))}</td><td>{f_int(sum(inter(p) for p in v))}</td><td>{f_pct(tasa(v))}</td></tr>')
    temas_items = sorted([(d.TEMAS[t][0], sum(inter(p) for p in v), acento, f'{d.TEMAS[t][1]} · {d.TEMAS[t][2]} · {len(v)} piezas · {f_pct(tasa(v))} · clic para abrir la versión con más impresiones', max(v, key=lambda p: n(p["imp"]))["url"]) for t, v in temas.items() if t != "HIST"], key=lambda it: -it[1])[:10]
    temas_html = barras_h(temas_items, fmt=lambda v: f"{v:,.0f}") + tabla(["Tema", "Pilar", "Modo", "Piezas", "Impr.", "Interacc.", "Tasa"], trows)

    # Top 10 por interacciones
    top_int = sorted(ps, key=lambda p: (-inter(p), -n(p["imp"])))[:10]
    top_items = [(d.TEMAS[p["tema"]][0], inter(p), COLOR[p["red"]], f'{p["red"]} · {p["formato"]} · {fecha(p["fecha"])} · {f_int(p["imp"])} impresiones · {f_pct(tasa([p]))} · clic para abrir', p["url"]) for p in top_int]
    top_imp = sorted(ps, key=lambda p: -n(p["imp"]))[:10]
    top_filas = [f'<tr><td>{fecha(p["fecha"])}</td><td class="l">{p["red"]}</td><td class="l">{p["formato"]}</td><td class="t">{e(d.TEMAS[p["tema"]][0])}{dest_badges(p)}</td><td>{f_int(p["imp"])}</td><td>{f_int(p["likes"])}</td><td>{f_int(p["com"])}</td><td>{f_int(p["sh"])}</td><td>{f_pct(tasa([p]))}</td><td><a href="{e(p["url"])}" target="_blank" rel="noopener">Ver</a></td></tr>' for p in top_imp]

    cal_html, cal_dias, cal_tot = calendario_mes(ps, clave)
    mprev = previos[-2] if idx > 0 else None
    prev = [p for p in d.P if mprev and del_mes(p, mprev)]
    RP = resumen(prev) if prev else None
    nom_prev = (MESES[idx - 1]["titulo"].split(" ")[0].lower() + (f" (1–{mprev['hasta']})" if mprev.get("hasta") else "")) if idx > 0 else ""
    def delta(a, b, pct=False):
        if b is None: return '<div class="dl neu">Primer mes con datos</div>'
        dv = a - b
        if pct: txt = f"{dv:+.1f} puntos"
        else: txt = f"{dv:+,.0f}"
        cls = "up" if dv > 0 else "down" if dv < 0 else "neu"
        flecha = "▲" if dv > 0 else "▼" if dv < 0 else "="
        return f'<div class="dl {cls}">{flecha} {txt} vs {nom_prev}</div>'
    l_, c_, s_ = desglose(ps)
    seg_txt = lambda r: (f' <span class="small">· {nom_prev}: {seg_de(dict(mprev, hasta_seg=min(mprev["hasta"], dia_seg())) if mprev.get("hasta") else mprev, r):+d}</span>' if mprev and seg_de(mprev, r) is not None else "")
    seg_lines = "".join(f'<div>{r} <b>+{v[0]}</b>' + seg_txt(r) + "</div>" for r, v in seg.items())
    parcial = (f'<p class="small">Comparación pareja: {MES[int(clave[5:]) - 1]} va al día {dia_corte()}, así que los meses anteriores se cuentan solo del 1 al {dia_corte()} (seguidores, del 1 al {dia_seg()}). Septiembre tiene poca actividad en esos días porque la primera publicación es del 19.</p>' if clave == CORTE[:7] else "")
    nota_mes = f'<div class="card nota-eq"><b>Nota del equipo:</b> {e(NOTAS[clave])}{dato_nota(clave)}</div>' if clave in NOTAS else ""
    kpis_html = f"""<div class="kpis">
<div class="card kpi"><div class="v">{R["n"]}</div><div class="l">publicaciones</div>{delta(R["n"], RP["n"] if RP else None)}</div>
<div class="card kpi"><div class="v">{f_int(R["imp"])}</div><div class="l">veces que se vieron nuestras publicaciones (impresiones)</div>{delta(R["imp"], RP["imp"] if RP else None)}</div>
<div class="card kpi wide2"><div class="v">{f_int(R["int"])}</div><div class="l">reacciones (interacciones)</div>
<div class="brk"><span><b>♥ {f_int(l_)}</b> {"like" if l_ == 1 else "likes"}</span><span><b>💬 {f_int(c_)}</b> {"comentario" if c_ == 1 else "comentarios"}</span><span><b>↗ {f_int(s_)}</b> {"compartido" if s_ == 1 else "compartidos"}</span></div>{delta(R["int"], RP["int"] if RP else None)}</div>
<div class="card kpi half"><div class="v">{(R["er"] or 0):.1f} <span class="u">de cada 100</span></div><div class="l">personas que vieron una publicación reaccionaron (tasa de interacción)</div>{delta(R["er"] or 0, RP["er"] if RP else None, pct=True)}</div>
<div class="card kpi half"><div class="v2">{seg_lines}</div><div class="l">seguidores nuevos (LinkedIn y TikTok: no disponible)</div></div>
</div>{parcial}{nota_mes}"""
    dias_json, dia_inicial = datos_dias(ps, clave)
    A = APRENDIZAJES[clave]
    li = lambda xs: "".join(f"<li>{enlazar(x, clave)}</li>" for x in xs)
    hip = HIPOTESIS.get(clave, [])
    hipotesis_html = ("<h2>Conclusiones e hipótesis</h2><p class=\"lead\">Posibles explicaciones de lo que muestran los datos. Son hipótesis: hay que comprobarlas con la parrilla del siguiente mes.</p><div class=\"hips\">"
        + "".join(f'<div class="card hip"><h3>{i}. {e(h["titulo"])}</h3><p><span class="hl v">Lo que vemos</span>{enlazar(h["vemos"], clave)}</p><p><span class="hl h">Posible explicación</span>{enlazar(h["hipotesis"], clave)}</p><p><span class="hl c">Cómo comprobarlo</span>{enlazar(h["comprobar"], clave)}</p></div>' for i, h in enumerate(hip, 1))
        + "</div>") if hip else ""
    seg_txt = "<br>".join(f'{r} <b>+{v[0]}</b>' for r, v in seg.items())
    nav = " · ".join(f'<a href="../{m["clave"]}/"{" aria-current=page" if m["clave"] == clave else ""}>{e(m["titulo"])}</a>' for m in MESES)
    atip_kpi = ""
    nota_atip = ""

    return f'''<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redes Lapzo · {e(M["titulo"])}</title>
<style>
:root{{--bg:#f5f7fa;--fg:#16202e;--muted:#5d6878;--panel:#fff;--line:#dfe4ec;--grid:#eceff4;--accent:#6b3fd4;--dest-bg:#fff7d6;--mono:#4cc3a2;--td:#b23b3b;--tv:#5b3cc4;--ti:#1d7a46;--tr:#b4540a;
--c-li:#4ba3e3;--c-ig:#c2417a;--c-fb:#2f6fb5;--c-tt:#64309e;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0f141b;--fg:#e8edf4;--muted:#9aa5b5;--panel:#171e28;--line:#2a3442;--grid:#222b37;--accent:#a98bff;--dest-bg:#2e2a14;--mono:#5fd1b1;--td:#f08c8c;--tv:#b9a2ff;--ti:#6fd39a;--tr:#f5a35c;
--c-li:#3f99d4;--c-ig:#d0507f;--c-fb:#2f5cb0;--c-tt:#9d5bd8;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f141b;--fg:#e8edf4;--muted:#9aa5b5;--panel:#171e28;--line:#2a3442;--grid:#222b37;--accent:#a98bff;--dest-bg:#2e2a14;--mono:#5fd1b1;--td:#f08c8c;--tv:#b9a2ff;--ti:#6fd39a;--tr:#f5a35c;
--c-li:#3f99d4;--c-ig:#d0507f;--c-fb:#2f5cb0;--c-tt:#9d5bd8;color-scheme:dark}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:1040px;margin:0 auto;padding-block:32px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}} a{{color:var(--accent)}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
h1{{font-size:34px;font-weight:600;margin:6px 0 4px}} h2{{font-size:22px;margin:44px 0 4px}} h3{{margin:0 0 8px;font-size:17px}}
.lead{{color:var(--muted);margin:0 0 12px}} nav{{margin:10px 0 24px;font-size:14px}} nav a[aria-current]{{font-weight:700;color:var(--fg);text-decoration:none}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}} .kpi.half{{grid-column:span 2}} @media (max-width:760px){{.kpis{{grid-template-columns:1fr 1fr}}}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}
.kpi .v{{font-size:28px;font-weight:600}} .kpi .v .u{{font-size:14px;font-weight:500;color:var(--muted)}} .kpi.wide2{{grid-column:span 2}} .brk{{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:8px;font-size:14px}} .dl{{font-size:12.5px;margin-top:8px;font-weight:600}} .dl.up{{color:var(--ti)}} .dl.down{{color:var(--td)}} .dl.neu{{color:var(--muted);font-weight:500}} .dg{{white-space:nowrap;font-size:13px}} .dg i{{font-style:normal;margin:0 2px 0 8px;opacity:.8}} .dg i:first-child{{margin-left:0}} @media (max-width:640px){{.kpi.wide2{{grid-column:auto}}}} .kpi .v2{{font-size:17px;line-height:1.5;margin-bottom:2px}} .kpi .l{{color:var(--muted);font-size:13px}}
.nets{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}} .net{{border-top:4px solid}}
dl{{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;margin:0}} dt{{color:var(--muted);font-size:12px}} dd{{margin:0;font-weight:600}}
.small{{font-size:13px;color:var(--muted)}}
.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(420px,100%),1fr));gap:12px}} .chart{{width:100%;height:auto;display:block;overflow:visible}}
.chart .val,.chart .tick{{font-size:11px;fill:var(--muted)}} .chart .dval{{font-size:10px;fill:var(--fg);font-weight:600}} .chart .dval.neg{{fill:#b23b3b}} .chart .lab{{font-size:12.5px;fill:var(--fg)}} .chart .quad{{font-size:12px;fill:var(--muted);font-style:italic;stroke:var(--panel);stroke-width:4px;paint-order:stroke;stroke-linejoin:round}}
.chart .axis{{stroke:var(--line)}} .chart .grid{{stroke:var(--grid)}} .chart .ref{{stroke:var(--muted);stroke-dasharray:4 4;opacity:.7}}
.chart .mk{{stroke:var(--panel);stroke-width:1.5}} .chart .hit{{fill:transparent}} .chart a:hover .mk,.chart g:hover rect{{filter:brightness(1.12)}} .chart a{{cursor:pointer}} .chart a:hover .lab{{text-decoration:underline}}
.legend{{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:var(--muted);margin:4px 0 8px}} .legend span{{display:inline-flex;align-items:center;gap:5px}}
details{{margin-top:10px}} summary{{cursor:pointer;color:var(--accent);font-size:14px}}
.scroll{{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:12px;margin-top:8px}}
table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{padding:8px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}
th:first-child,td:first-child,tbody th,th.l,td.l{{text-align:left}} thead th{{color:var(--muted);font-weight:600;font-size:12px}} tbody tr:last-child>*{{border-bottom:0}}
.evo .grp{{text-align:center;border-left:1px solid var(--line)}} td.t{{white-space:normal;min-width:180px;text-align:left}} tbody th{{white-space:normal;min-width:180px;font-weight:500}}
.learn{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}} .learn ul{{margin:0;padding-left:18px}} .learn li{{margin-bottom:8px}}
.note{{border-left:4px solid var(--accent)}} .rs{{margin:0;padding-left:18px}} .rs li{{margin-bottom:8px}} .rs a{{color:inherit;text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:2px}}
.hips{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(460px,100%),1fr));gap:12px}} .hip p{{margin:8px 0 0;font-size:14.5px}} .hip a{{color:inherit;text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:2px}}
.hl{{display:block;font-size:11.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-bottom:2px}} .hl.v{{color:var(--muted)}} .hl.h{{color:var(--tv)}} .hl.c{{color:var(--ti)}}
.ctrl{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;margin-bottom:8px}}
.seg{{display:flex;flex-wrap:wrap;gap:6px}} .seg button{{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:5px 12px;cursor:pointer;display:inline-flex;gap:6px;align-items:center}}
.seg button.on{{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}} select{{font:inherit;font-size:13px;padding:4px 6px;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--fg)}}
.chip{{display:inline-block;color:#fff;text-shadow:0 0 1px rgba(0,0,0,.35);font-size:11px;font-weight:700;border-radius:5px;padding:1px 5px;line-height:1.5}}
.ptab td{{vertical-align:middle}} .ptab tbody.grp{{border-top:10px solid var(--bg)}} .ptab tr.grp-h td{{background:var(--grid);border-bottom:0;padding-top:10px;padding-bottom:10px}} .ptab tr.grp-h .chip{{margin-right:3px}} .ptab a.pz{{color:var(--fg);text-decoration:none}} .ptab a.pz:hover{{text-decoration:underline}} .learn a{{color:inherit;text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:2px}}
.ptab tr.sub td{{padding-top:6px;padding-bottom:6px}} .ptab tr.sub.dest td{{background:var(--dest-bg)}} .tag{{display:inline-block;margin-left:4px;font-size:11px;font-weight:600;border-radius:999px;padding:1px 7px;white-space:nowrap;border:1px solid}} .t-v{{color:var(--tv);border-color:var(--tv)}} .t-i{{color:var(--ti);border-color:var(--ti)}} .t-r{{color:var(--tr);border-color:var(--tr)}} .ptab tr.sub td.t a{{font-weight:400}} .ptab tr.sub td:first-child{{padding-left:22px}} .ptab td.num b{{font-size:15px}} .ptab td.t{{min-width:180px}} .ptab td.t a{{color:var(--fg);text-decoration:none;font-weight:500}} .ptab td.t a:hover{{text-decoration:underline}}
.ptab .bar{{min-width:130px;text-align:left}} .track{{display:inline-block;vertical-align:middle;width:66px;height:10px;background:var(--grid);border-radius:5px;overflow:hidden;margin-right:8px}}
.fill{{height:100%;border-radius:5px}} .fill.over{{background-image:repeating-linear-gradient(135deg,transparent 0 4px,rgba(255,255,255,.45) 4px 6px)!important}}
.est{{font-size:12.5px;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1px solid var(--line)}} .est.up{{color:#1d7a46;border-color:#9fd6b4}} .est.down{{color:#b23b3b;border-color:#efb3b3}} .est.mix,.est.neu{{color:var(--muted)}}
@media (prefers-color-scheme:dark){{.est.up{{color:#6fd39a;border-color:#2f6b47}} .est.down{{color:#f08c8c;border-color:#6b2f2f}}}}
.cal{{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}} .dow{{font-size:12px;color:var(--muted);text-align:center;padding-bottom:2px}}
.day{{min-height:74px;border:1px solid var(--line);border-radius:10px;padding:6px;background:var(--panel)}} .day b{{font-size:12px;font-weight:600}}
.day.empty{{background:var(--grid);border-color:transparent}} .day.empty b{{color:var(--muted);font-weight:400}} .day.out{{border:0;background:transparent}} .day.future{{border:1px dashed var(--line);background:transparent}} .day.future b{{color:var(--muted);font-weight:400}}
.day .chips{{display:flex;flex-wrap:wrap;gap:3px;margin-top:4px}} .day:not(.empty):not(.out):hover{{border-color:var(--accent)}}
@media (max-width:640px){{.day{{min-height:58px;padding:4px}} .day .chip{{font-size:9.5px;padding:0 3px}}}}
.pick{{cursor:pointer}} g.pick.sel rect:not(.hit){{stroke:var(--fg);stroke-width:2}} .day.sel{{outline:2px solid var(--accent);outline-offset:1px}}
.dia{{margin-top:12px;border-top:1px solid var(--line);padding-top:12px}} .dia-h{{margin-bottom:6px}} .dia-l{{list-style:none;padding:0;margin:0;display:grid;gap:8px}}
.dia-l li{{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}} .dia-l a{{font-weight:500;color:var(--fg)}}
.fgrid{{display:grid;grid-template-columns:1fr;gap:12px}} .scroll.flat{{border:0;border-radius:0;margin:0;background:transparent}}
.ftab th,.ftab td{{padding:7px 6px}} .ftab tbody th{{min-width:0}} .ftab .tags{{margin-top:3px;margin-left:-4px}} .ftab .bar{{min-width:150px;white-space:nowrap;text-align:left}} .ftab td.l{{text-align:left}} .track.sm{{width:110px}} .ftab tbody th{{width:200px}} .ftab tr.vacio td{{white-space:normal}} .ftab{{table-layout:auto}} .ftab tr.vacio th,.ftab tr.vacio td{{color:var(--muted)}}
.t-down{{color:var(--td);border-color:var(--td)}} .src{{display:inline-block;margin-left:4px;font-size:11px;color:var(--muted);border:1px dashed var(--line);border-radius:999px;padding:0 7px;white-space:nowrap}}
@media (max-width:640px){{.card{{overflow-x:auto}} .chart.wide{{min-width:600px}}}}
.top{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--panel);border-bottom:1px solid var(--line)}} .top-in{{max-width:1040px;margin:0 auto;padding-block:10px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
.brand{{font-weight:700;color:var(--fg);text-decoration:none;margin-right:auto}} .menu{{display:flex;flex-wrap:wrap;gap:4px}} .menu a{{font-size:13.5px;color:var(--muted);text-decoration:none;padding:5px 10px;border-radius:999px}} .menu a:hover{{background:var(--grid);color:var(--fg)}} .menu a[aria-current]{{background:var(--fg);color:var(--bg)}}
.pdf{{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:5px 12px;cursor:pointer}} .pdf:hover{{border-color:var(--accent)}}
.reps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:12px}} a.card.rep{{color:inherit;text-decoration:none;display:flex;flex-direction:column;gap:6px}} a.card.rep:hover{{border-color:var(--accent)}} a.card.rep h3{{margin:4px 0 0}} .rep .tag{{margin-left:0;align-self:flex-start}}
.mini{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:4px 0}} .mini b{{display:block;font-size:20px}} .mini span{{font-size:12px;color:var(--muted)}} .hl-txt{{font-size:13.5px;margin:2px 0}} .go{{margin-top:auto;color:var(--accent);font-size:13.5px;font-weight:600}}
section.mes{{margin-bottom:28px}} .nota-sutil{{margin-top:10px;max-width:80ch}} .nota-eq.urg{{border-left-color:var(--td)}} .nota-eq{{margin-top:12px;border-left:4px solid var(--tr);font-size:14.5px}} .nota-mini{{font-size:13px;margin:2px 0;padding:6px 8px;border-radius:8px;background:var(--grid)}} .learn{{margin-top:12px}} h3.sub{{margin:18px 0 8px}} h2 .small{{font-weight:400;margin-left:8px}}
@media print{{.top,.pdf,details summary,.ctrl{{display:none!important}} details>*{{display:block}} body{{background:#fff}} .kpi,.net,.hip,.learn .card,tbody.grp,.rep{{break-inside:avoid}} .scroll{{overflow:visible}} main{{padding-top:0}} #tip{{display:none}}}}
.vrow{{display:grid;grid-template-columns:minmax(200px,1fr) 2fr;gap:6px 16px;align-items:center;padding:10px 0;border-bottom:1px solid var(--line)}} .vrow.vhead{{padding:0 0 2px;border:0}} .vn a{{color:var(--fg);font-weight:500;text-decoration:none}} .vn a:hover{{text-decoration:underline}} .vtrack{{height:16px;margin-bottom:4px}} .vt{{display:block;height:16px;background:var(--grid);border-radius:4px;overflow:hidden}} .vt.sin{{background:transparent;outline:1.5px dashed var(--muted);outline-offset:-1.5px}} .vf{{display:block;height:100%}} .vscale{{position:relative;height:16px;font-size:11px;color:var(--muted)}} .vscale span{{position:absolute;transform:translateX(-50%);white-space:nowrap}} .vscale span:first-child{{transform:none}} .vscale span:last-child{{transform:translateX(-100%)}} .vleg{{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:13px;color:var(--muted);margin-bottom:12px}} .vleg span{{display:inline-flex;align-items:center;gap:6px}} .vt.mini{{display:inline-block;width:46px;height:10px;vertical-align:middle}} .vt.mini .vf{{display:block}} @media (max-width:640px){{.vrow{{grid-template-columns:1fr}}}}
#tip{{position:fixed;pointer-events:none;background:var(--fg);color:var(--bg);font-size:13px;line-height:1.4;padding:8px 10px;border-radius:8px;max-width:300px;white-space:pre-line;opacity:0;transition:opacity .1s;z-index:9}}
</style></head><body>{barra_nav('../../', clave)}<main>
<div class="eyebrow">Lapzo · Redes sociales orgánicas</div>
<h1>{e(M["titulo"])}</h1>
<p class="lead">{e(M["periodo"])} · LinkedIn, Instagram, Facebook y TikTok · datos extraídos el {EXTRAIDO}</p>
{f'<p class="small">{e(M["nota_periodo"])}</p>' if M["nota_periodo"] else ""}

{kpis_html}
{atip_kpi}

<h2>Cómo le fue a cada publicación</h2>
<p class="lead">♥ likes · 💬 comentarios · ↗ compartidos. Un guion (—) significa que la red no da ese dato. Cada bloque es una pieza: arriba su total y debajo cómo le fue en cada red donde se publicó. Filtra por red, cambia el orden y haz clic en la red para abrir la publicación.</p>
{tabla_publicaciones(ps)}
<p class="small">Etiquetas: <span class="tag t-v">★ Top vistas</span> <span class="tag t-i">★ Top interacciones</span> <span class="tag t-r">★ Top tasa</span> marcan las 3 publicaciones del mes que más destacaron en cada medida. Si una barra va rayada es porque se sale de la escala.</p>

<h2>Cuándo publicamos</h2>
<p class="lead">{cal_dias} de {cal_tot} días con al menos una publicación. Pasa el cursor sobre un día para ver qué se publicó.</p>
<div class="card">{cal_html}</div>

<h2>Las 10 con más interacción</h2>
<p class="lead">Likes + comentarios + compartidos. El color indica la red.</p>
<div class="card">{leyenda()}{barras_h(top_items, fmt=lambda v: f"{v:,.0f}")}
{tabla(["Fecha", "Red", "Formato", "Tema (top 10 por impresiones)", "Impr.", "Likes", "Coment.", "Compart.", "Tasa", ""], top_filas)}</div>

{seccion_videos(ps, "del mes")}

<h2>Evolución mes a mes</h2>
<p class="lead">Cómo cambia cada red desde septiembre.{f" Para comparar parejo, cada mes se cuenta del 1 al {dia_corte()}." if clave == CORTE[:7] else ""}</p>
<div class="charts">
<div class="card"><h3>Impresiones</h3>{leyenda()}{barras_mes(previos, imp_mes, "Impresiones por mes y red")}</div>
<div class="card"><h3>Tasa de interacción (%)</h3>{leyenda()}{barras_mes_pct(previos)}</div>
<div class="card"><h3>Impresiones de la publicación típica</h3>{leyenda()}{barras_mes(previos, med_mes, "Mediana de impresiones por publicación")}<p class="small">Mediana: no la infla un solo éxito.</p></div>
<div class="card"><h3>Seguidores nuevos</h3>{leyenda()}{barras_mes(previos, seg_mes, "Seguidores netos por mes y red")}<p class="small">n/d: LinkedIn y TikTok no tienen el dato.</p></div>
</div>
{evol_tabla}

<h2>Seguidores día por día</h2>
<p class="lead">Seguidores ganados menos perdidos en cada día. <b>Haz clic en cualquier día</b> (aquí o en el calendario) para ver qué se publicó ese día.</p>
<div class="card">{seguidores_dia(clave)}<p class="small">LinkedIn y TikTok no tienen el dato. Instagram y Facebook llegan al 21 nov.</p>
<div id="dia" class="dia" aria-live="polite"></div></div>

<h2>Cada red este mes</h2>
<div class="nets">{"".join(tarjetas)}</div>

<h2>Qué tipo de contenido funcionó</h2>
<p class="lead">Tasa de interacción por pilar, modo y formato. Pilar y modo según el plugin de contenido de Lapzo (marca-lapzo): es una clasificación propuesta, valídala con la hoja de planeación.</p>
<div class="charts">
<div class="card"><h3>Por pilar</h3>{pilares}</div>
<div class="card"><h3>Por modo de comunicación</h3>{modos}</div>
</div>
<h3 style="margin-top:20px">Por red y formato</h3>
<p class="small">Todos los formatos de cada red, de la mejor a la peor tasa de interacción. Impresiones promedio = cuánta gente vio, en promedio, cada publicación de ese formato. «Publicación» = publicación que solo registró HubSpot, que no indica el formato. Ojo: si un formato tiene 1 o 2 publicaciones, su resultado puede ser casualidad. En LinkedIn, HubSpot no indica el formato; el documento se identificó por su texto.</p>
{formatos_por_red(ps, clave)}
<div class="card" style="margin-top:12px"><h3>Temas con más interacción</h3><p class="small">Cada tema suma todas sus versiones en las distintas redes.</p>{temas_html}</div>
{nota_atip}

{hipotesis_html}
<h2>Qué hacer con esto</h2>
<div class="learn">
<div class="card"><h3>Qué funcionó</h3><ul>{li(A["funciono"])}</ul></div>
<div class="card"><h3>Qué no funcionó</h3><ul>{li(A["no_funciono"])}</ul></div>
<div class="card note"><h3>Para la parrilla del siguiente mes</h3><ul>{li(A["parrilla"])}</ul></div>
</div>

<h2>Cómo se calculan estas cifras</h2>
<div class="card small">
<p><b>Fuentes:</b> LinkedIn sale de HubSpot Social. Instagram, Facebook y TikTok salen de Metricool (marca go_lapzo); lo que Metricool no tiene y HubSpot sí se completa con HubSpot y se marca con la etiqueta «de HubSpot»: comentarios y compartidos de los reels de Facebook, y una publicación de Kirkpatrick en Facebook que Metricool no registró. Las publicaciones que se borraron y se volvieron a subir no se cuentan. Seguidores: Metricool; Facebook trae el total diario e Instagram los ganados y perdidos por día.</p>
<p><b>Definiciones:</b> interacciones = likes + comentarios + compartidos; tasa de interacción = interacciones ÷ impresiones. Impresiones = vistas en Instagram, impresiones en Facebook y LinkedIn, reproducciones en reels de Facebook y en TikTok.</p>
<p><b>Historias:</b> las historias de Instagram y Facebook no se incluyen en este reporte; se agregarán más adelante.</p>
<p><b>Lo que no está disponible en ninguna fuente:</b> clics y seguidores de LinkedIn; compartidos de la mayoría de carruseles e imágenes de Instagram; historial de seguidores de TikTok. Se muestran con «—» y cuentan como 0 en las sumas.</p>
<p><b>Ojo:</b> las cifras de cada publicación son acumuladas al {EXTRAIDO}; las más recientes todavía siguen sumando. {"El detalle de cada publicación está en el archivo publicaciones.csv del repositorio." if MODO_ARTIFACT else 'El detalle de cada publicación está en <a href="publicaciones.csv">publicaciones.csv</a>.'}</p>
</div>
</main>
<div id="tip" role="tooltip"></div>
<script type="application/json" id="dias">{dias_json}</script>
<script>
(function(){{var t=document.getElementById('tip');
function show(ev){{var el=ev.target.closest('[data-tip]');if(!el){{t.style.opacity=0;return}}
t.textContent=el.getAttribute('data-tip');t.style.opacity=1;var x=ev.clientX+14,y=ev.clientY+14;
var w=t.offsetWidth,h=t.offsetHeight;if(x+w>innerWidth-8)x=ev.clientX-w-14;if(y+h>innerHeight-8)y=ev.clientY-h-14;t.style.left=x+'px';t.style.top=y+'px'}}
document.addEventListener('pointermove',show);
document.querySelectorAll('.pubs').forEach(function(w){{var tab=w.querySelector('table'),f='';
function apply(){{var k=w.querySelector('.ord').value;var gs=[].slice.call(tab.tBodies);
gs.forEach(function(g){{var imp=0,it=0,fe='9',vis=0;[].forEach.call(g.querySelectorAll('tr.sub'),function(r){{var ok=!f||r.dataset.red===f;r.style.display=ok?'':'none';if(ok){{vis++;imp+=+r.dataset.imp;it+=+r.dataset.int;if(r.dataset.fecha<fe)fe=r.dataset.fecha}}}});
g.style.display=vis?'':'none';g._k={{imp:imp,int:it,er:imp?it/imp:0,fecha:fe}}}});
gs.sort(function(a,b){{return k==='fecha'?(a._k.fecha<b._k.fecha?-1:1):(b._k[k]-a._k[k])}});gs.forEach(function(g){{tab.appendChild(g)}})}}
w.querySelectorAll('.seg button').forEach(function(b){{b.onclick=function(){{f=b.dataset.f;w.querySelectorAll('.seg button').forEach(function(x){{x.classList.toggle('on',x===b)}});apply()}}}});
w.querySelector('.ord').onchange=apply;}});
var D=JSON.parse(document.getElementById('dias').textContent),C={{LinkedIn:'var(--c-li)',Instagram:'var(--c-ig)',Facebook:'var(--c-fb)',TikTok:'var(--c-tt)'}},I={{LinkedIn:'LI',Instagram:'IG',Facebook:'FB',TikTok:'TT'}},box=document.getElementById('dia');
function el(t,c,x){{var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}}
function sg(v){{return v==null?'sin dato':(v>0?'+':'')+v}}
function pick(k){{var o=D[k];if(!o)return;box.replaceChildren();
document.querySelectorAll('.pick').forEach(function(p){{p.classList.toggle('sel',p.dataset.day===k)}});
var h=el('div','dia-h');h.appendChild(el('b',null,o.t));h.appendChild(el('span','small',' · Seguidores nuevos: Facebook '+sg(o.fb)+' · Instagram '+sg(o.ig)));box.appendChild(h);
if(!o.p.length){{box.appendChild(el('p','small','No se publicó nada este día.'));return}}
var ul=el('ul','dia-l');o.p.forEach(function(p){{var li=el('li');var c=el('span','chip',I[p.r]);c.style.background=C[p.r];c.style.color={{LinkedIn:'#0d2236',TikTok:'#fff'}}[p.r]||'#fff';c.style.textShadow='none';li.appendChild(c);
var a=el('a',null,p.n);a.href=p.u;a.target='_blank';a.rel='noopener';li.appendChild(a);(p.a||[]).forEach(function(t){{li.appendChild(el('span','tag '+{{'★ Top vistas':'t-v','★ Top interacciones':'t-i','★ Top tasa':'t-r'}}[t],t))}});li.appendChild(el('span','small',' '+p.r+' · '+p.f+' · '+p.i+' impresiones · '+p.x+' de interacción'));ul.appendChild(li)}});box.appendChild(ul);
box.appendChild(el('p','small','Ojo: un seguidor nuevo también puede venir de una publicación de días anteriores.'))}}
document.querySelectorAll('.pick').forEach(function(p){{p.addEventListener('click',function(){{pick(p.dataset.day);if(p.classList.contains('day'))box.scrollIntoView({{behavior:'smooth',block:'nearest'}})}})}});
pick('{dia_inicial}');document.addEventListener('pointerleave',function(){{t.style.opacity=0}});}})();
</script>
</body></html>'''

# ---------------------------------------------------------------- Reporte semanal
SEMANAS = [("2026-11-10", "2026-11-16", "2026-11-03", "2026-11-09"), ("2026-11-16", "2026-11-22", "2026-11-09", "2026-11-15")]
# Avisos de cada semana sobre datos que las fuentes todavía no actualizan (clave: lunes de la semana).
AVISOS_SEMANA = {
 "2026-11-16": [
  "<b>Cifra de HubSpot en TikTok:</b> para el video de «Conocimiento compartido» (19 nov), Metricool se quedó en 66 reproducciones y 9 likes, sin actualizarse. Se usa la de HubSpot: 462 reproducciones y 33 likes.",
  "<b>Ojo con «La mejor encuesta es la que sí mandas» (22 nov):</b> salió el domingo y Metricool aún no tiene sus cifras de Instagram ni de TikTok. Instagram se completó con HubSpot; el TikTok aparece con 0 porque ninguna de las dos fuentes lo ha actualizado.",
 ],
}

def _dias_rango(a, b):
    import datetime as dt
    d0 = dt.date.fromisoformat(a); d1 = dt.date.fromisoformat(b)
    return [(d0 + dt.timedelta(i)).isoformat() for i in range((d1 - d0).days + 1)]

def seg_rango(a, b):
    """Seguidores netos en el rango: Facebook por total diario, Instagram por ganados - perdidos."""
    ks = sorted(d.FB_TOTAL)
    fb = {k: d.FB_TOTAL[k] - d.FB_TOTAL[prev] for prev, k in zip(ks[:-1], ks[1:]) if a <= k <= b}
    ig = {k: v[0] - v[1] for k, v in d.IG_DIA.items() if a <= k <= b}
    return fb, ig

def pagina_semana(a, b, pa, pb):
    import re, json
    ps = [p for p in d.P if a <= p["fecha"] <= b]
    prev = [p for p in d.P if pa <= p["fecha"] <= pb]
    calcular_destacados(ps)
    R, RP = resumen(ps), resumen(prev)
    fb, ig = seg_rango(a, b)
    fbp, igp = seg_rango(pa, pb)
    dias = _dias_rango(a, b)

    def delta(x, y, pct=False):
        dv = x - y
        cls = "up" if dv > 0 else "down" if dv < 0 else "neu"
        fl = "▲" if dv > 0 else "▼" if dv < 0 else "="
        txt = f"{dv:+.1f} puntos" if pct else f"{dv:+,.0f}"
        return f'<div class="dl {cls}">{fl} {txt} vs semana anterior</div>'

    l_, c_, s_ = desglose(ps)
    piezas, piezas_p = len({p["tema"] for p in ps}), len({p["tema"] for p in prev})
    ig_fin = max(ig) if ig else b
    kpis = (
        '<div class="kpis">'
        f'<div class="card kpi"><div class="v">{piezas}</div><div class="l">piezas únicas ({R["n"]} publicaciones contando cada red)</div>{delta(piezas, piezas_p)}</div>'
        f'<div class="card kpi"><div class="v">{f_int(R["imp"])}</div><div class="l">veces que se vieron nuestras publicaciones (impresiones)</div>{delta(R["imp"], RP["imp"])}</div>'
        f'<div class="card kpi wide2"><div class="v">{f_int(R["int"])}</div><div class="l">reacciones (interacciones)</div>'
        f'<div class="brk"><span><b>♥ {f_int(l_)}</b> likes</span><span><b>💬 {f_int(c_)}</b> comentarios</span><span><b>↗ {f_int(s_)}</b> compartidos</span></div>{delta(R["int"], RP["int"])}</div>'
        f'<div class="card kpi half"><div class="v">{(R["er"] or 0):.1f} <span class="u">de cada 100</span></div><div class="l">personas que vieron una publicación reaccionaron (tasa de interacción)</div>{delta(R["er"] or 0, RP["er"] or 0, True)}</div>'
        f'<div class="card kpi half"><div class="v2"><div>Facebook <b>{sum(fb.values()):+d}</b> <span class="small">· semana anterior {sum(fbp.values()):+d}</span></div>'
        f'<div>Instagram <b>{sum(ig.values()):+d}</b> <span class="small">· semana anterior {sum(igp.values()):+d} (Instagram llega al {fecha(ig_fin)})</span></div></div>'
        '<div class="l">seguidores nuevos (LinkedIn y TikTok: no disponible)</div></div>'
        '</div>'
    )

    # Seguidores por día (7 días)
    W, ml, mr, rh = 680, 82, 12, 84
    H = rh * 2 + 46
    mx = max([abs(v) for v in list(fb.values()) + list(ig.values())] + [1])
    X = lambda i: ml + i / len(dias) * (W - ml - mr)
    bw = (W - ml - mr) / len(dias) - 10
    o = [f'<svg viewBox="0 0 {W} {H}" class="chart wide" role="img" aria-label="Seguidores netos por día">']
    for j, (red, serie) in enumerate([("Facebook", fb), ("Instagram", ig)]):
        base = 8 + rh * j + rh - 14
        o.append(f'<text x="0" y="{base-rh/2+10}" class="lab">{red}</text><line x1="{ml}" x2="{W-mr}" y1="{base}" y2="{base}" class="axis"/>')
        for i, k in enumerate(dias):
            cx = X(i) + 5 + bw / 2
            if k not in serie:
                o.append(f'<text x="{cx:.1f}" y="{base-4}" text-anchor="middle" class="val">sin dato</text>')
                continue
            v = serie[k]
            h = (rh - 26) * abs(v) / mx
            y = base - h if v >= 0 else base
            if v > 0:
                lab = f'<text x="{cx:.1f}" y="{y-3:.1f}" text-anchor="middle" class="val dval">+{v}</text>'
            elif v < 0:
                lab = f'<text x="{cx:.1f}" y="{base+max(h,1)+11:.1f}" text-anchor="middle" class="val dval neg">{v}</text>'
            else:
                lab = ""
            o.append(f'<g class="pick" data-day="{k}" data-tip="{tip(red + " · " + fecha(k), f"{v:+d} seguidores netos", "Haz clic para ver qué se publicó")}">'
                     f'<rect x="{X(i)+5:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h,1):.1f}" rx="3" style="fill:{COLOR[red]}"/>{lab}'
                     f'<rect x="{X(i):.1f}" y="{base-rh+16}" width="{bw+10:.1f}" height="{rh-10}" class="hit"/></g>')
    dsem = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    for i, k in enumerate(dias):
        o.append(f'<text x="{X(i)+5+bw/2:.1f}" y="{H-6}" text-anchor="middle" class="tick">{dsem[i % 7]} {int(k[8:])}</text>')
    o.append("</svg>")
    seg_svg = "".join(o)

    dd = {}
    for k in dias:
        dd[k] = {"t": fecha(k), "fb": fb.get(k), "ig": ig.get(k), "p": [
            {"r": p["red"], "f": p["formato"], "n": d.TEMAS[p["tema"]][0], "i": f_int(p["imp"]), "x": f_pct(tasa([p])),
             "u": p["url"], "a": [t for t, _ in DEST_ACTUAL.get(p["url"], [])]}
            for p in sorted([p for p in ps if p["fecha"] == k], key=lambda p: REDES.index(p["red"]))]}
    mejor = max(dd, key=lambda k: (dd[k]["fb"] or 0) + (dd[k]["ig"] or 0))

    # Tarjetas por red
    tarjetas = []
    for r in REDES:
        q = [p for p in ps if p["red"] == r]
        qp = [p for p in prev if p["red"] == r]
        s1, s0 = resumen(q), resumen(qp)
        tarjetas.append(
            f'<div class="card net" style="border-top-color:{COLOR[r]}"><h3>{r}</h3><dl>'
            f'<div><dt>Publicaciones</dt><dd>{s1["n"]} <span class="small">(antes {s0["n"]})</span></dd></div>'
            f'<div><dt>Impresiones</dt><dd>{f_int(s1["imp"])} <span class="small">(antes {f_int(s0["imp"])})</span></dd></div>'
            f'<div><dt>Interacciones</dt><dd>{f_int(s1["int"])} <span class="small">(antes {f_int(s0["int"])})</span></dd></div>'
            f'<div><dt>Tasa</dt><dd>{f_pct(s1["er"])} <span class="small">(antes {f_pct(s0["er"])})</span></dd></div>'
            f'<div style="grid-column:span 2"><dt>Desglose</dt><dd class="dd">{desg_html(q, True)}</dd></div></dl></div>')

    # Resumen automático
    top_i = max(ps, key=lambda p: n(p["imp"]))
    med = statistics.median([n(x["imp"]) for x in ps])
    top_t = max([p for p in ps if n(p["imp"]) >= med], key=lambda p: tasa([p]) or 0)
    lnk = lambda p: f'<a href="{e(p["url"])}" target="_blank" rel="noopener">«{e(d.TEMAS[p["tema"]][0])}»</a>'
    primeras = {}
    for p in ps:
        if p["tema"] not in {x["tema"] for x in prev}:
            primeras[p["tema"]] = min(primeras.get(p["tema"], "9"), p["fecha"])
    nuevas = list(primeras.values())
    mejor_fb = max(fb, key=fb.get)
    resumen_b = [
        f'<b>Más vista:</b> {lnk(top_i)} en {top_i["red"]} · {top_i["formato"].lower()}, con {f_int(top_i["imp"])} impresiones ({f_pct(tasa([top_i]))} de interacción).',
        f'<b>Mejor tasa de interacción</b> (entre las que tuvieron al menos las vistas típicas de la semana): {lnk(top_t)} en {top_t["red"]} · {top_t["formato"].lower()}, con {f_pct(tasa([top_t]))} ({f_int(top_t["imp"])} impresiones).',
        f'<b>Seguidores:</b> Facebook {sum(fb.values()):+d} (semana anterior {sum(fbp.values()):+d}); el mejor día fue el {fecha(mejor_fb)} con {fb[mejor_fb]:+d}. Instagram {sum(ig.values()):+d} (semana anterior {sum(igp.values()):+d}).',
        f'<b>Conversación:</b> {f_int(c_)} comentarios en {R["n"]} publicaciones.',
        f'<b>Ritmo:</b> {piezas} piezas esta semana contra {piezas_p} la semana anterior' + (f'; la última pieza nueva salió el {fecha(max(nuevas))}.' if nuevas else '.'),
    ]
    resumen_b += AVISOS_SEMANA.get(a, [])

    # Plantilla: reutiliza los estilos y scripts de la página mensual
    base_html = pagina(len(MESES) - 1)
    estilo = re.search(r"<style>.*?</style>", base_html, re.S).group(0)
    scripts = base_html[base_html.index('<div id="tip"'):]
    datos = json.dumps(dd, ensure_ascii=False).replace("</", "<\\/")
    scripts = re.sub(r'<script type="application/json" id="dias">.*?</script>',
                     lambda m: '<script type="application/json" id="dias">' + datos + '</script>', scripts, flags=re.S)
    scripts = re.sub(r"pick\('[0-9-]*'\);", lambda m: f"pick('{mejor}');", scripts)
    titulo = f"Semana del {int(a[8:])} al {fecha(b)} {b[:4]}"
    return (
        '<!doctype html>\n<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>Redes Lapzo · {titulo}</title>\n{estilo}</head><body>{barra_nav("../../../", "sem-" + a)}<main>\n'
        '<div class="eyebrow">Lapzo · Redes sociales orgánicas · reporte semanal</div>\n'
        f'<h1>{titulo}</h1>\n'
        f'<p class="lead">Lunes {fecha(a)} a domingo {fecha(b)} · comparado con la semana del {fecha(pa)} al {fecha(pb)} · datos extraídos el {EXTRAIDO}</p>\n'
        f'{kpis}\n'
        '<h2>Resumen de la semana</h2>\n'
        f'<div class="card"><ul class="rs">{"".join(f"<li>{x}</li>" for x in resumen_b)}</ul></div>\n'
        '<h2>Seguidores día por día</h2>\n'
        '<p class="lead">Seguidores ganados menos perdidos. <b>Haz clic en cualquier día</b> para ver qué se publicó.</p>\n'
        f'<div class="card">{seg_svg}<div id="dia" class="dia" aria-live="polite"></div></div>\n'
        '<h2>Cómo le fue a cada publicación</h2>\n'
        '<p class="lead">Cada bloque es una pieza: arriba su total y debajo cómo le fue en cada red. Haz clic en el nombre o en la red para abrir la publicación.</p>\n'
        f'{tabla_publicaciones(ps)}\n'
        '<p class="small">Etiquetas: <span class="tag t-v">★ Top vistas</span> <span class="tag t-i">★ Top interacciones</span> <span class="tag t-r">★ Top tasa</span> marcan las 3 publicaciones de la semana que más destacaron en cada medida.</p>\n'
        + seccion_videos(ps, "de la semana") + '\n'
        '<h2>Cada red esta semana</h2>\n'
        f'<div class="nets">{"".join(tarjetas)}</div>\n'
        '<h2>Cómo se calculan estas cifras</h2>\n'
        '<div class="card small">\n'
        '<p>Mismas fuentes y definiciones que el reporte mensual: LinkedIn de HubSpot; Instagram, Facebook y TikTok de Metricool, completando con HubSpot lo que falta. Interacciones = likes + comentarios + compartidos; tasa = interacciones ÷ impresiones. No incluye historias.</p>\n'
        f'<p><b>Ojo:</b> las cifras de cada publicación son acumuladas al {EXTRAIDO}. Las publicaciones de esta semana llevan pocos días y todavía siguen sumando, así que la comparación favorece a la semana anterior.</p>\n'
        '</div>\n</main>\n' + scripts)

# ---------------------------------------------------------------- Mini sitio: menú, portada y aprendizajes
def barra_nav(raiz, activo):
    """Menú fijo arriba, igual en todas las páginas. raiz = ruta relativa a la carpeta principal."""
    links = [("inicio", "Inicio", "index.html")]
    links += [(m["clave"], m["titulo"][:3] + (" (parcial)" if "parcial" in m["titulo"] else ""), f'rrss/{m["clave"]}/index.html') for m in MESES]
    links += [(f"sem-{a}", f"Semana {int(a[8:])}–{int(b[8:])} {MES[int(b[5:7])-1][:3]}", f"rrss/semanal/{a}/index.html") for a, b, _, _ in SEMANAS]
    links += [("leads", "Leads", "leads/index.html")]
    links += [("aprendizajes", "Aprendizajes", "aprendizajes/index.html")]
    links += [("okrs", "OKRs", "okrs/index.html")]
    items = "".join(f'<a href="{raiz}{u}"{" aria-current=page" if k == activo else ""}>{e(t)}</a>' for k, t, u in links)
    return (f'<header class="top"><div class="top-in"><a class="brand" href="{raiz}index.html">Lapzo · Reportes</a>'
            f'<nav class="menu">{items}</nav>'
            + ("" if MODO_ARTIFACT else '<button class="pdf" onclick="window.print()" title="Guardar esta página como PDF">Descargar PDF</button>')
            + '</div></header>')

def _estilo_y_scripts():
    import re
    base_html = pagina(len(MESES) - 1)
    estilo = re.search(r"<style>.*?</style>", base_html, re.S).group(0)
    return estilo

def _texto_plano(html_txt):
    import re
    return re.sub(r"<[^>]+>", "", re.sub(r"\[\[[A-Z0-9]+\|[A-Za-z]*\|(.+?)\]\]", r"\1", html_txt))

def stats_mes(clave):
    ps = [p for p in d.P if p["fecha"][:7] == clave]
    R = resumen(ps)
    R["piezas"] = len({p["tema"] for p in ps})
    R["seg"] = SEGUIDORES[clave]
    R["desg"] = desglose(ps)
    return R

def pagina_inicio():
    estilo = _estilo_y_scripts()
    ult = MESES[-1]; ant = MESES[-2]
    S = stats_mes(ult["clave"])
    mant = meses_parejos(len(MESES) - 1)[-2]
    psa = [p for p in d.P if del_mes(p, mant)]
    SA = resumen(psa); SA["piezas"] = len({p["tema"] for p in psa})
    na = ant["titulo"].split(" ")[0] + (f" (1–{mant['hasta']})" if mant.get("hasta") else " completo")
    l_, c_, s_ = S["desg"]
    ref = lambda txt: f'<div class="dl neu">{txt}</div>'
    seg_lines = "".join(f'<div>{r} <b>+{v[0]}</b> <span class="small">· {na.lower()}: {seg_de(mant, r):+d}</span></div>' for r, v in S["seg"].items())
    kpis = (
        '<div class="kpis">'
        f'<div class="card kpi"><div class="v">{S["piezas"]}</div><div class="l">piezas únicas ({S["n"]} publicaciones contando cada red)</div>{ref(f"{na}: {SA['piezas']} piezas")}</div>'
        f'<div class="card kpi"><div class="v">{f_int(S["imp"])}</div><div class="l">veces que se vieron nuestras publicaciones</div>{ref(f"{na}: {f_int(SA['imp'])}")}</div>'
        f'<div class="card kpi wide2"><div class="v">{f_int(S["int"])}</div><div class="l">reacciones</div>'
        f'<div class="brk"><span><b>♥ {f_int(l_)}</b> likes</span><span><b>💬 {f_int(c_)}</b> comentarios</span><span><b>↗ {f_int(s_)}</b> compartidos</span></div>{ref(f"{na}: {f_int(SA['int'])}")}</div>'
        f'<div class="card kpi half"><div class="v">{(S["er"] or 0):.1f} <span class="u">de cada 100</span></div><div class="l">personas que vieron una publicación reaccionaron</div>{ref(f"{na}: {(SA['er'] or 0):.1f} de cada 100")}</div>'
        f'<div class="card kpi half"><div class="v2">{seg_lines}</div><div class="l">seguidores nuevos (LinkedIn y TikTok: no disponible)</div></div>'
        '</div>')

    tarjetas = []
    for m in reversed(MESES):
        st = stats_mes(m["clave"])
        dest = _texto_plano(APRENDIZAJES[m["clave"]]["funciono"][0])
        seg = " · ".join(f'{r} +{v[0]}' for r, v in st["seg"].items())
        tarjetas.append(
            f'<a class="card rep" href="rrss/{m["clave"]}/index.html"><span class="tag t-v">Mensual</span><h3>{e(m["titulo"])}</h3>'
            f'<p class="small">{e(m["periodo"])}</p>'
            f'<div class="mini"><div><b>{st["piezas"]}</b><span>piezas</span></div><div><b>{f_int(st["imp"])}</b><span>impresiones</span></div><div><b>{f_pct(st["er"])}</b><span>tasa</span></div></div>'
            f'<p class="small">Seguidores: {seg}</p><p class="hl-txt">{e(dest)}</p>'
            + (f'<p class="nota-mini">{e(NOTAS[m["clave"]])}{dato_nota(m["clave"])}</p>' if m["clave"] in NOTAS else "")
            + '<span class="go">Ver reporte →</span></a>')
    for a, b, pa, pb in reversed(SEMANAS):
        ps = [p for p in d.P if a <= p["fecha"] <= b]
        R = resumen(ps); fb, ig = seg_rango(a, b)
        tarjetas.insert(0,
            f'<a class="card rep" href="rrss/semanal/{a}/index.html"><span class="tag t-i">Semanal</span><h3>Semana del {int(a[8:])} al {fecha(b)}</h3>'
            f'<p class="small">Comparada con la semana del {fecha(pa)} al {fecha(pb)}</p>'
            f'<div class="mini"><div><b>{len({p["tema"] for p in ps})}</b><span>piezas</span></div><div><b>{f_int(R["imp"])}</b><span>impresiones</span></div><div><b>{f_pct(R["er"])}</b><span>tasa</span></div></div>'
            f'<p class="small">Seguidores: Facebook {sum(fb.values()):+d} · Instagram {sum(ig.values()):+d}</p><span class="go">Ver reporte →</span></a>')
    n_l = len(d.LEADS); n_v = sum(1 for x in d.LEADS if x[5] in ("Pasado a Ventas", "Reescalado a Ventas"))
    tarjetas.append(f'<a class="card rep" href="leads/index.html"><span class="tag t-down">Leads</span><h3>Leads de redes</h3>'
                    f'<p class="small">Personas que escribieron por redes y cuántas se convirtieron en lead (Q4 2026).</p>'
                    f'<div class="mini"><div><b>{n_l}</b><span>contactos</span></div><div><b>{n_v}</b><span>leads</span></div><div><b>{n_l-n_v}</b><span>por convertir</span></div></div>'
                    '<span class="go">Ver leads →</span></a>')
    tarjetas.append('<a class="card rep" href="aprendizajes/index.html"><span class="tag t-r">Para la parrilla</span><h3>Aprendizajes e hipótesis</h3>'
                    '<p class="small">Qué repetir, qué ajustar y qué dejar de hacer, mes por mes, y las hipótesis por comprobar.</p><span class="go">Ver aprendizajes →</span></a>')

    imp_mes = lambda m, r: sum(n(p["imp"]) for p in d.P if del_mes(p, m) and p["red"] == r)
    seg_mes = seg_de
    parejos = meses_parejos(len(MESES) - 1)
    return (
        '<!doctype html>\n<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>Reportes de redes Lapzo</title>\n{estilo}</head><body>{barra_nav("", "inicio")}<main>\n'
        '<div class="eyebrow">Lapzo · Marketing</div>\n<h1>Reportes de redes sociales</h1>\n'
        f'<p class="lead">LinkedIn, Instagram, Facebook y TikTok · datos al {EXTRAIDO}</p>\n'
        f'<h2>Así vamos en {ult["titulo"].split(" ")[0].lower()} <span class="small">(al día {int(CORTE[8:])})</span></h2>\n{kpis}\n'
        '<h2>Reportes</h2>\n'
        f'<div class="reps">{"".join(tarjetas)}</div>\n'
        '<h2>Evolución</h2>\n<div class="charts">'
        f'<div class="card"><h3>Impresiones por mes</h3>{leyenda()}{barras_mes(parejos, imp_mes, "Impresiones por mes y red")}</div>'
        f'<div class="card"><h3>Seguidores nuevos por mes</h3>{leyenda()}{barras_mes(parejos, seg_mes, "Seguidores nuevos por mes y red")}<p class="small">n/d: LinkedIn y TikTok no tienen el dato.</p></div>'
        '</div>\n</main>\n'
        '<div id="tip" role="tooltip"></div>\n<script>\n(function(){var t=document.getElementById("tip");\n'
        'document.addEventListener("pointermove",function(ev){var el=ev.target.closest("[data-tip]");if(!el){t.style.opacity=0;return}'
        't.textContent=el.getAttribute("data-tip");t.style.opacity=1;var x=ev.clientX+14,y=ev.clientY+14;'
        'if(x+t.offsetWidth>innerWidth-8)x=ev.clientX-t.offsetWidth-14;if(y+t.offsetHeight>innerHeight-8)y=ev.clientY-t.offsetHeight-14;'
        't.style.left=x+"px";t.style.top=y+"px"});})();\n</script>\n</body></html>')

def pagina_aprendizajes():
    estilo = _estilo_y_scripts()
    li = lambda xs, clave: "".join(f"<li>{enlazar(x, clave)}</li>" for x in xs)
    bloques = []
    for m in reversed(MESES):
        c = m["clave"]; st = stats_mes(c); A = APRENDIZAJES[c]
        seg = " · ".join(f'{r} +{v[0]}' for r, v in st["seg"].items())
        hip = HIPOTESIS.get(c, [])
        hip_html = ("<h3 class=\"sub\">Hipótesis por comprobar</h3><div class=\"hips\">"
                    + "".join(f'<div class="card hip"><h3>{i}. {e(h["titulo"])}</h3><p><span class="hl v">Lo que vemos</span>{enlazar(h["vemos"], c)}</p><p><span class="hl h">Posible explicación</span>{enlazar(h["hipotesis"], c)}</p><p><span class="hl c">Cómo comprobarlo</span>{enlazar(h["comprobar"], c)}</p></div>' for i, h in enumerate(hip, 1))
                    + "</div>") if hip else ""
        bloques.append(
            f'<section class="mes"><h2>{e(m["titulo"])} <a class="small" href="../rrss/{c}/index.html">ver reporte →</a></h2>'
            f'<p class="lead">{st["piezas"]} piezas · {st["n"]} publicaciones · {f_int(st["imp"])} impresiones · {f_pct(st["er"])} de tasa · seguidores: {seg}</p>'
            + (f'<div class="card nota-eq"><b>Nota del equipo:</b> {e(NOTAS[c])}{dato_nota(c)}</div>' if c in NOTAS else "")
            + '<div class="learn">'
            f'<div class="card"><h3>Qué funcionó</h3><ul>{li(A["funciono"], c)}</ul></div>'
            f'<div class="card"><h3>Qué no funcionó</h3><ul>{li(A["no_funciono"], c)}</ul></div>'
            f'<div class="card note"><h3>Para la parrilla del siguiente mes</h3><ul>{li(A["parrilla"], c)}</ul></div>'
            f'</div>{hip_html}</section>')
    return (
        '<!doctype html>\n<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>Lapzo · Aprendizajes de redes</title>\n{estilo}</head><body>{barra_nav("../", "aprendizajes")}<main>\n'
        '<div class="eyebrow">Lapzo · Redes sociales</div>\n<h1>Aprendizajes e hipótesis</h1>\n'
        '<p class="lead">Lo que nos enseñó cada mes, para armar la parrilla del siguiente. Lo más reciente va arriba. La clasificación por pilar y modo es una propuesta: valídala con la hoja de planeación.</p>\n'
        + ('<section class="mes"><h2>Atención de mensajes y leads <a class="small" href="../leads/index.html">ver leads →</a></h2>'
           '<p class="lead">Lo aprendido al responder comentarios y mensajes y al pasar leads a Ventas.</p>'
           '<div class="card"><ul class="rs">' + "".join(f'<li>{t} <span class="small">· {f}</span></li>' for f, t in APRENDIZAJES_ATENCION) + '</ul></div></section>'
           if APRENDIZAJES_ATENCION else "")
        + ('<section class="mes"><h2>Planeación de LinkedIn</h2>'
           '<p class="lead">Lo aprendido al armar la parrilla.</p>'
           '<div class="card"><ul class="rs">' + "".join(f'<li>{t} <span class="small">· {f}</span></li>' for f, t in APRENDIZAJES_PLANEACION) + '</ul></div></section>'
           if APRENDIZAJES_PLANEACION else "")
        + "".join(bloques) + '\n</main></body></html>')

# ---------------------------------------------------------------- Página de OKRs
def pagina_okrs():
    import datetime as dt
    O = d.OKR; estilo = _estilo_y_scripts()
    hoy = dt.date.fromisoformat(CORTE)
    ini = dt.date.fromisoformat(O["inicio"])
    lunes0 = ini - dt.timedelta(ini.weekday())
    semanas = []
    k = lunes0
    while k + dt.timedelta(6) <= hoy:
        semanas.append((k, k + dt.timedelta(6))); k += dt.timedelta(7)
    et = lambda a: (lambda x: f"{x.day} {MES[x.month-1][:3]}")(max(a, ini))
    estado = lambda cls, txt: f'<span class="okr-st {cls}">{txt}</span>'
    def barra(v, meta, color="var(--accent)"):
        w = max(0, min(100, 100 * v / meta)) if meta else 0
        return f'<div class="okr-bar"><div style="width:{w:.1f}%;background:{color}"></div></div>'
    def columnas(items, meta=None, base=None, fmt=lambda v: f"{v:,.0f}", nombre=""):
        W, H, ml, mb, mt, mr = 680, 190, 8, 30, 22, 92
        mx = max([v for _, v in items if v is not None] + [meta or 0, 1]) * 1.1
        gw = (W - ml - mr) / max(len(items), 1); bw = min(46, gw - 12)
        Y = lambda v: H - mb - (H - mb - mt) * v / mx
        o = [f'<svg viewBox="0 0 {W} {H}" class="chart wide" role="img" aria-label="{e(nombre)}">']
        for ref, cls, txt in [(meta, "ref", "meta"), (base, "ref base", "línea base")]:
            if ref is not None:
                o.append(f'<line x1="{ml}" x2="{W-mr+6}" y1="{Y(ref):.1f}" y2="{Y(ref):.1f}" class="{cls}"/><text x="{W-mr+10}" y="{Y(ref)+4:.1f}" class="tick">{txt}: {fmt(ref)}</text>')
        for i, (lab, v) in enumerate(items):
            x = ml + i * gw + (gw - bw) / 2
            if v is None:
                o.append(f'<text x="{x+bw/2:.1f}" y="{H-mb-5}" text-anchor="middle" class="val">sin datos</text>')
            else:
                ok = meta is not None and v >= meta
                o.append(f'<g data-tip="{tip(lab, fmt(v))}"><rect x="{x:.1f}" y="{Y(v):.1f}" width="{bw:.1f}" height="{H-mb-Y(v):.1f}" rx="3" style="fill:{"var(--ti)" if ok else "var(--accent)"}"/>'
                         f'<text x="{x+bw/2:.1f}" y="{Y(v)-5:.1f}" text-anchor="middle" class="val">{fmt(v)}</text></g>')
            o.append(f'<text x="{x+bw/2:.1f}" y="{H-10}" text-anchor="middle" class="tick">{e(lab)}</text>')
        o.append(f'<line x1="{ml}" x2="{W-mr+6}" y1="{H-mb}" y2="{H-mb}" class="axis"/></svg>')
        return "".join(o)

    meses_q = [("2026-10", "Octubre"), ("2026-11", "Noviembre"), ("2026-12", "Diciembre")]
    hay = lambda c: c <= CORTE[:7]
    # KR1 · piezas al mes (piezas únicas orgánicas + anuncios BOFU)
    org = {c: len({p["tema"] for p in d.P if p["fecha"][:7] == c and p["fecha"] >= O["inicio"]}) for c, _ in meses_q}
    kr1 = {c: org[c] + O["bofu"].get(c, 0) for c, _ in meses_q}
    trim = sum(kr1[c] for c, _ in meses_q if hay(c))
    mes_act = CORTE[:7]; v_act = kr1[mes_act]
    st1 = estado("ok", "Cumplido este mes") if v_act >= O["kr1_meta_mes"] else estado("mid", f"Faltan {O['kr1_meta_mes'] - v_act} piezas para 25 este mes")
    kr1_html = (f'<div class="okr-big"><b>{trim}</b> de {O["kr1_meta_trim"]} piezas en el trimestre</div>{barra(trim, O["kr1_meta_trim"])}'
                + columnas([(n + (f" (al {int(CORTE[8:])})" if c == mes_act else ""), kr1[c] if hay(c) else None) for c, n in meses_q], O["kr1_meta_mes"], O["kr1_base"], nombre="Piezas por mes")
                + '<p class="small">' + " · ".join(f'{n}: {org[c]} orgánicas' + (f' + {O["bofu"][c]} anuncios BOFU de AI Course Builder' if c in O["bofu"] else "") + dato_nota(c) for c, n in meses_q if hay(c))
                + '. Una pieza cuenta una vez aunque salga en varias redes. Los anuncios BOFU de noviembre se suman cuando se confirme cuántos fueron.</p>')
    # KR2 · interacciones promedio por publicación, semana a semana
    def prom(ps): return (sum(inter(p) for p in ps) / len(ps)) if ps else None
    sem2 = [(et(a), prom([p for p in d.P if a.isoformat() <= p["fecha"] <= b.isoformat() and p["fecha"] >= O["inicio"]])) for a, b in semanas]
    mes2 = {c: prom([p for p in d.P if p["fecha"][:7] == c]) for c, _ in meses_q if hay(c)}
    com_mes = {c: sum(n(p["com"]) for p in d.P if p["fecha"][:7] == c) for c, _ in meses_q if hay(c)}
    v2 = mes2[mes_act]
    st2 = estado("ok", "Cumplido") if v2 >= O["kr2_meta"] else (estado("mid", "Arriba de la línea base, lejos de la meta") if v2 > O["kr2_base"] else estado("bad", "En la línea base o abajo"))
    kr2_html = (f'<div class="okr-big"><b>{v2:.1f}</b> interacciones por publicación en {MES[int(mes_act[5:])-1]} · meta {O["kr2_meta"]}</div>{barra(v2, O["kr2_meta"])}'
                + columnas(sem2, O["kr2_meta"], O["kr2_base"], fmt=lambda v: f"{v:.1f}", nombre="Interacciones por publicación cada semana")
                + '<p class="small">Semana a semana (lunes a domingo). Todas las redes; interacciones = likes + comentarios + compartidos. '
                + " · ".join(f'{n}: {mes2[c]:.1f} por publicación, {com_mes[c]} comentarios' for c, n in meses_q if hay(c)) + '.</p>')
    com_txt = estado("ok", "Hay comentarios este mes") if com_mes[mes_act] > 0 else estado("bad", "0 comentarios este mes")
    # KR3 · leads por semana (todo lo registrado en la hoja de leads)
    sem3 = [(et(a), sum(1 for x in d.LEADS if a.isoformat() <= x[0] <= b.isoformat())) for a, b in semanas]
    cumple = sum(1 for _, v in sem3 if v >= O["kr3_meta_sem"])
    tot3 = sum(1 for x in d.LEADS if x[0] >= O["inicio"])
    st3 = estado("ok", "Todas las semanas") if cumple == len(sem3) else estado("mid", f"{cumple} de {len(sem3)} semanas con al menos 1 lead")
    kr3_html = (f'<div class="okr-big"><b>{tot3}</b> leads en Q4 · {cumple} de {len(sem3)} semanas cumplen la meta de 1 por semana</div>{barra(cumple, len(sem3))}'
                + columnas(sem3, O["kr3_meta_sem"], None, nombre="Leads por semana")
                + f'<p class="small">Fuente: {e(d.LEADS_FUENTE)}, leída el {e(d.LEADS_LEIDO)}. Cuenta todo lo que registraste, haya tenido seguimiento de Ventas o no. '
                + f'{sum(1 for x in d.LEADS if x[5] in ("Pasado a Ventas", "Reescalado a Ventas"))} ya se pasaron a Ventas. Detalle en <a href="../leads/index.html">Leads</a>.</p>')
    # KR4 · reporte semanal entregado
    fallas = 0
    for (a0, b0, _, _), (a1, _, _, _) in zip(SEMANAS[:-1], SEMANAS[1:]):
        fallas += max(0, (dt.date.fromisoformat(a1) - dt.date.fromisoformat(b0)).days - 1) // 7
    esperadas = len(SEMANAS) + fallas; pct4 = 100 * len(SEMANAS) / esperadas if esperadas else 0
    st4 = estado("ok", "Al 100 %") if pct4 >= 100 else estado("mid", f"{pct4:.0f} %")
    kr4_html = (f'<div class="okr-big"><b>{len(SEMANAS)} de {esperadas}</b> semanas con reporte ({pct4:.0f} %)</div>{barra(pct4, 100)}'
                + '<ul class="rs">' + "".join(f'<li>✓ <a href="../rrss/semanal/{a}/index.html">Semana del {fecha(a)} al {fecha(b)}</a></li>' for a, b, _, _ in SEMANAS) + '</ul>'
                + '<p class="small">Cuenta desde que arrancó el reporte semanal (10 nov). Cada lunes se suma la semana anterior.</p>')
    # KR5 · edición de video automatizada
    kr5_html = (f'<div class="okr-big"><b>{O["kr5_pct"]} %</b> de las piezas de video con el proceso automatizado</div>{barra(O["kr5_pct"], 100, "var(--ti)")}'
                f'<p class="small">{e(O["kr5_nota"])}</p>')
    tarjeta = lambda kr, tit, st, metrica, base, meta, cuerpo: (
        f'<section class="card okr"><div class="okr-h"><span class="okr-kr">{kr}</span><h3>{e(tit)}</h3>{st}</div>'
        f'<dl class="okr-dl"><div><dt>Métrica</dt><dd>{e(metrica)}</dd></div><div><dt>Línea base</dt><dd>{e(base)}</dd></div><div><dt>Meta</dt><dd>{e(meta)}</dd></div></dl>{cuerpo}</section>')
    cards = "".join([
        tarjeta("KR1", "Aumentar el volumen de piezas de contenido", st1, "Piezas publicadas al mes", "5 piezas (septiembre)", "25 o más al mes · 75 en el trimestre", kr1_html),
        tarjeta("KR2", "Mejorar el engagement de las piezas", st2 + com_txt, "Interacciones promedio por publicación", "~5 por publicación, 0 comentarios", "~15 por publicación · comentarios > 0", kr2_html),
        tarjeta("KR3", "Generar leads desde redes sociales", st3, "Leads registrados por semana", "0 (septiembre)", "1 o más por semana", kr3_html),
        tarjeta("KR4", "Establecer el reporte semanal de desempeño", st4, "% de semanas con reporte entregado", "Sin reporte semanal", "100 % desde que arrancó", kr4_html),
        tarjeta("KR5", "Implementar la edición de video automatizada", estado("ok", "Cumplido"), "Proceso implementado y en uso", "0 % (edición manual)", "100 % de las piezas", kr5_html),
    ])
    css = ('<style>.okr{margin-bottom:14px} .okr-h{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;margin-bottom:10px} .okr-h h3{margin:0;flex:1 1 260px} '
           '.okr-kr{font-size:12px;font-weight:700;color:#fff;background:var(--accent);border-radius:6px;padding:2px 8px} '
           '.okr-st{font-size:12.5px;font-weight:600;border-radius:999px;padding:2px 10px;border:1px solid} .okr-st.ok{color:var(--ti)} .okr-st.mid{color:var(--tr)} .okr-st.bad{color:var(--td)} '
           '.okr-dl{grid-template-columns:repeat(3,1fr);margin-bottom:12px} @media (max-width:640px){.okr-dl{grid-template-columns:1fr}} '
           '.okr-big{font-size:15px;margin:6px 0} .okr-big b{font-size:26px;margin-right:4px} '
           '.okr-bar{height:10px;background:var(--grid);border-radius:5px;overflow:hidden;margin:4px 0 12px} .okr-bar div{height:100%;border-radius:5px} '
           '.chart .ref.base{stroke-dasharray:2 4}</style>')
    return (
        '<!doctype html>\n<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>Lapzo · OKRs de contenido Q4 2026</title>\n{estilo}{css}</head><body>{barra_nav("../", "okrs")}<main>\n'
        '<div class="eyebrow">Lapzo · Mi plan de OKRs · Q4 2026</div>\n<h1>Escala tu producción de contenido sin perder calidad</h1>\n'
        '<p class="lead">Pasa de 5 a 25+ piezas mensuales, mejora el engagement, genera leads desde redes sociales y establece tu medición semanal y tus procesos con IA, de octubre a diciembre.</p>\n'
        f'<p class="small">Avance al {fecha(CORTE)} {CORTE[:4]} · se actualiza cada lunes con el reporte semanal.</p>\n'
        f'{cards}\n</main>\n<div id="tip" role="tooltip"></div>\n<script>\n(function(){{var t=document.getElementById("tip");\n'
        'document.addEventListener("pointermove",function(ev){var el=ev.target.closest("[data-tip]");if(!el){t.style.opacity=0;return}'
        't.textContent=el.getAttribute("data-tip");t.style.opacity=1;var x=ev.clientX+14,y=ev.clientY+14;if(x+t.offsetWidth>innerWidth-8)x=ev.clientX-t.offsetWidth-14;'
        'if(y+t.offsetHeight>innerHeight-8)y=ev.clientY-t.offsetHeight-14;t.style.left=x+"px";t.style.top=y+"px"});})();\n</script>\n</body></html>')

# ---------------------------------------------------------------- Página de leads
def pagina_leads():
    from collections import Counter, OrderedDict
    estilo = _estilo_y_scripts()
    def grupo(pz):
        if "AI Course Builder" in pz: return "Anuncio de AI Course Builder"
        if "universidad corporativa" in pz: return "Anuncio de universidad corporativa"
        if "Elearning" in pz: return "Anuncio Elearning"
        return "Mensaje directo sin anuncio"
    L = [dict(fecha=f, red=r, origen=o, pieza=pz, grupo=grupo(pz), interes=i, estado=es, a=a) for f, r, o, pz, i, es, a in d.LEADS]
    tot = len(L)
    en_ventas = ("Pasado a Ventas", "Reescalado a Ventas")
    pasados = [x for x in L if x["estado"] in en_ventas]
    pend = [x for x in L if x["estado"] not in en_ventas]
    anuncio = [x for x in L if x["origen"] == "Anuncio"]
    md = [x for x in L if x["origen"] != "Anuncio"]
    meses = OrderedDict()
    for x in sorted(L, key=lambda x: x["fecha"]):
        k = MES[int(x["fecha"][5:7]) - 1].capitalize()
        meses[k] = meses.get(k, 0) + 1
    reesc = sum(1 for x in pasados if x["estado"] == "Reescalado a Ventas")
    kpis = (
        '<div class="kpis">'
        f'<div class="card kpi"><div class="v">{tot}</div><div class="l">contactos: personas que escribieron por redes</div>'
        f'<div class="dl neu">{" · ".join(f"{k}: {v}" for k, v in meses.items())}</div></div>'
        f'<div class="card kpi"><div class="v">{len(pasados)}</div><div class="l">leads: ya tenemos sus datos y se pasaron a Ventas</div>'
        f'<div class="dl neu">{round(100*len(pasados)/tot)} % de los contactos se convirtió en lead' + (f' · {reesc} reescalado' if reesc else '') + '</div></div>'
        f'<div class="card kpi"><div class="v">{len(pend)}</div><div class="l">contactos por convertir en lead</div><div class="dl neu">faltan sus datos, su respuesta o un seguimiento</div></div>'
        f'<div class="card kpi"><div class="v">{len(anuncio)} <span class="u">de {tot}</span></div><div class="l">contactos que llegaron por un anuncio</div><div class="dl neu">{len(md)} por mensaje directo sin anuncio</div></div>'
        '</div>')

    def barras(clave, color="var(--mono)"):
        cnt = Counter(x[clave] for x in L)
        items = [(k, v, color, f"{v} {'contacto' if v == 1 else 'contactos'}") for k, v in cnt.most_common()]
        return barras_h(items, fmt=lambda v: f"{v:,.0f}", ancho=440, lw=230)

    color_estado = {"Pasado a Ventas": "var(--ti)", "Reescalado a Ventas": "var(--td)", "Esperando datos": "var(--tr)", "Esperando respuesta": "var(--tr)", "Pendiente de seguimiento": "var(--td)"}
    cnt_est = Counter(x["estado"] for x in L)
    estados = barras_h([(k, v, color_estado.get(k, "var(--mono)"), f"{v} {'contacto' if v == 1 else 'contactos'}") for k, v in cnt_est.most_common()],
                       fmt=lambda v: f"{v:,.0f}", ancho=440, lw=200)

    clase_est = {"Pasado a Ventas": "up", "Reescalado a Ventas": "down", "Esperando datos": "mix", "Esperando respuesta": "mix", "Pendiente de seguimiento": "down"}
    filas = "".join(
        f'<tr><td>{fecha(x["fecha"])}</td><td class="l">{x["red"]}</td><td class="l">{e(x["origen"])}</td><td class="t">{e(x["pieza"])}</td>'
        f'<td class="l">{e(x["interes"])}</td><td class="l"><span class="est {clase_est.get(x["estado"], "neu")}">{e(x["estado"])}</span></td>'
        f'<td class="l">{"✓ Lead" if x["estado"] in en_ventas else "Aún no"}</td><td class="l">{e(x["a"]) or "—"}</td></tr>'
        for x in sorted(L, key=lambda x: (x["fecha"], x["estado"])))
    tabla_l = ('<div class="scroll"><table><thead><tr><th>Fecha</th><th class="l">Red</th><th class="l">Cómo llegó</th><th class="l">Pieza o anuncio de origen</th>'
               '<th class="l">Interés</th><th class="l">Estado</th><th class="l">¿Es lead?</th><th class="l">Pasado a</th></tr></thead>'
               f'<tbody>{filas}</tbody></table></div>')

    n_acb = sum(1 for x in L if x["interes"] == "AI Course Builder")
    n_cya = sum(1 for x in L if "CyA" in x["interes"])
    n_dia = Counter(x["fecha"] for x in L).most_common(1)[0]
    lect = [
        f'<b>{n_dia[1]} de los {tot} contactos llegaron el {fecha(n_dia[0])}</b>, casi todos por anuncios de AI Course Builder y de universidad corporativa.',
        f'<b>Lo que más piden:</b> AI Course Builder ({n_acb}) y universidad corporativa (CyA, {n_cya}).',
        f'<b>{len(pend)} contactos todavía no son leads:</b> {cnt_est.get("Esperando datos", 0)} esperando sus datos, {cnt_est.get("Esperando respuesta", 0)} esperando respuesta y {cnt_est.get("Pendiente de seguimiento", 0)} pendiente de seguimiento. Conseguir sus datos esta semana los convierte en leads para Ventas.',
        f'<b>Todos llegaron por Facebook.</b> Ningún contacto se registró desde Instagram, LinkedIn ni TikTok en este periodo.',
        'En la hoja, 3 contactos tienen marcado «[PENDIENTE: link]» del anuncio de origen. Completarlo ayuda a saber qué anuncio trae más contactos y leads.',
    ]
    return (
        '<!doctype html>\n<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>Leads de redes Lapzo</title>\n{estilo}</head><body>{barra_nav("../", "leads")}<main>\n'
        '<div class="eyebrow">Lapzo · Redes sociales · leads</div>\n<h1>Leads de redes</h1>\n'
        f'<p class="lead">Personas que escribieron por redes y que Marketing atendió y registró · Q4 2026 · leído el {d.LEADS_LEIDO}</p>\n'
        '<p class="small">Un <b>contacto</b> es alguien que escribió. Se vuelve <b>lead</b> cuando ya recopilamos sus datos y se pasa a Ventas.</p>\n'
        f'{kpis}\n'
        '<h2>Lectura rápida</h2>\n'
        f'<div class="card"><ul class="rs">{"".join(f"<li>{x}</li>" for x in lect)}</ul></div>\n'
        '<h2>De dónde vienen y qué piden</h2>\n<div class="charts">'
        f'<div class="card"><h3>Estado</h3>{estados}</div>'
        f'<div class="card"><h3>Interés</h3>{barras("interes")}</div>'
        f'<div class="card"><h3>Cómo llegaron</h3>{barras("origen")}</div>'
        f'<div class="card"><h3>Anuncio o mensaje de origen</h3>{barras("grupo")}</div>'
        '</div>\n'
        '<h2>Cada contacto</h2>\n'
        '<p class="lead">Sin nombres, correos ni teléfonos: esos datos están en la hoja de registro.</p>\n'
        f'{tabla_l}\n'
        + "".join(f'<p class="small nota-sutil"><b>Nota:</b> {e(t)}</p>' for _, t in d.LEADS_URGENTES)
        + '<h2>De dónde salen estos datos</h2>\n'
        f'<div class="card small"><p>Hoja de Google «{e(d.LEADS_FUENTE)}», llenada a mano por Marketing. Solo incluye los contactos que se registraron ahí; '
        'los que llegan por formularios o landings se cuentan en HubSpot y no aparecen aquí. Aunque la hoja se llama «leads orgánicos», '
        'varios llegaron a partir de un anuncio: la columna «Cómo llegó» lo indica.</p></div>\n'
        '</main>\n'
        '<div id="tip" role="tooltip"></div>\n<script>\n(function(){var t=document.getElementById("tip");\n'
        'document.addEventListener("pointermove",function(ev){var el=ev.target.closest("[data-tip]");if(!el){t.style.opacity=0;return}'
        't.textContent=el.getAttribute("data-tip");t.style.opacity=1;var x=ev.clientX+14,y=ev.clientY+14;'
        'if(x+t.offsetWidth>innerWidth-8)x=ev.clientX-t.offsetWidth-14;if(y+t.offsetHeight>innerHeight-8)y=ev.clientY-t.offsetHeight-14;'
        't.style.left=x+"px";t.style.top=y+"px"});})();\n</script>\n</body></html>')

def csv_mes(clave):
    ruta = os.path.join(RAIZ, "rrss", clave, "publicaciones.csv")
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "red", "formato", "tema", "pilar", "modo", "impresiones", "likes", "comentarios", "compartidos", "interacciones", "tasa_%", "fuente", "enlace"])
        for p in sorted([p for p in d.P if p["fecha"][:7] == clave], key=lambda p: (p["fecha"], p["red"])):
            nom, pil, modo = d.TEMAS[p["tema"]]; t = tasa([p])
            w.writerow([p["fecha"], p["red"], p["formato"], nom, pil, modo, p["imp"],
                        "" if p["likes"] is None else p["likes"], "" if p["com"] is None else p["com"],
                        "" if p["sh"] is None else p["sh"], inter(p), "" if t is None else round(t, 1), "HubSpot" if p.get("fuente") else ("Metricool + HubSpot (" + p["hs"] + ")" if p.get("hs") else ("HubSpot" if p["red"] == "LinkedIn" else "Metricool")), p["url"]])

if __name__ == "__main__":
    for i, M in enumerate(MESES):
        os.makedirs(os.path.join(RAIZ, "rrss", M["clave"]), exist_ok=True)
        with open(os.path.join(RAIZ, "rrss", M["clave"], "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(i))
        csv_mes(M["clave"])
        print("ok", M["clave"])
    with open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_inicio())
    os.makedirs(os.path.join(RAIZ, "aprendizajes"), exist_ok=True)
    with open(os.path.join(RAIZ, "aprendizajes", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_aprendizajes())
    os.makedirs(os.path.join(RAIZ, "leads"), exist_ok=True)
    with open(os.path.join(RAIZ, "leads", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_leads())
    os.makedirs(os.path.join(RAIZ, "okrs"), exist_ok=True)
    with open(os.path.join(RAIZ, "okrs", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_okrs())
    print("ok portada, aprendizajes, leads y OKRs")
    for a, b, pa, pb in SEMANAS:
        carpeta = os.path.join(RAIZ, "rrss", "semanal", a)
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina_semana(a, b, pa, pb))
        print("ok semana", a)
