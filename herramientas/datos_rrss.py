# Datos extraídos el 23 nov 2026 (publicaciones hasta el 22 nov; seguidores hasta el 21 nov). LinkedIn: HubSpot Social. Instagram, Facebook, TikTok: Metricool (marca go_lapzo).
# Las cifras de cada publicación son acumuladas al día de extracción.
# None = la fuente no da ese dato ("no disponible").

# Temas: cada tema agrupa la misma pieza publicada en varias redes.
# pilar y modo: clasificación propuesta según el plugin lapzo-contenido-rrss (marca-lapzo), por validar con la hoja de planeación.
TEMAS = {
 "S1": ("Lo que no se ve del trabajo de RH (iceberg)", "Experta en talento", "Reflexiva"),
 "S2": ("No todos necesitan aprender lo mismo", "Experta en talento", "Reflexiva"),
 "S3": ("Lapzi: ya es viernes", "Sin pilar (Lapzi / humor)", "Entretenimiento"),
 "O1": ("IATF 16949 no es una ley", "Confiable", "Educativa"),
 "O2": ("Día Mundial de la Sonrisa y clima laboral", "Experta en talento", "Reflexiva"),
 "O3": ("Líderes que su equipo seguiría (NOM-035)", "Experta en talento", "Reflexiva"),
 "O4": ("Una misma marca, cientos de experiencias (retail)", "Experta en talento", "Reflexiva"),
 "O5": ("Señales de que tu equipo necesita capacitación", "Experta en talento", "Educativa"),
 "O6": ("Lapzi: lista de terrores (spooky season)", "Sin pilar (Lapzi / humor)", "Entretenimiento"),
 "O7": ("Miles de cursos terminados, ¿qué cambió?", "Experta en talento", "Reflexiva"),
 "O8": ("Serie DNC 01: ¿necesidad o catálogo?", "Experta en talento", "Educativa"),
 "O9": ("La rotación también es una señal", "Experta en talento", "Reflexiva"),
 "O10": ("Serie DNC 02: empieza por la brecha", "Experta en talento", "Educativa"),
 "O11": ("Encuéntranos en Instagram", "Sin pilar (aviso)", "Comercial"),
 "O12": ("Tener la información no es tener todo listo", "Innovadora", "Reflexiva"),
 "O13": ("Capacitación vista como gasto (McKinsey)", "Confiable", "Educativa"),
 "O14": ("3 pasos para pasar de la evaluación a la acción", "Experta en talento", "Educativa"),
 "O15": ("Un error no borra tu año (evaluación de desempeño)", "Experta en talento", "Reflexiva"),
 "O16": ("Lapzi: spooky season en RH", "Sin pilar (Lapzi / humor)", "Entretenimiento"),
 "O17": ("Modelo de Kirkpatrick", "Experta en talento", "Educativa"),
 "O18": ("La conversación de crecimiento que nadie abre", "Experta en talento", "Reflexiva"),
 "O19": ("Capacitar por Excel y correo (LMS, demo)", "Innovadora", "Comercial"),
 "N1": ("Ruta de desarrollo en 4 elementos", "Experta en talento", "Educativa"),
 "N2": ("70 % en piloto automático (Gallup)", "Confiable", "Comercial"),
 "N3": ("Capacitar no garantiza que el talento crezca", "Experta en talento", "Educativa"),
 "N4": ("Plan de capacitación 2027 (adelanto WEF)", "Confiable", "Educativa"),
 "N5": ("El 39 % de las habilidades cambiará (WEF)", "Confiable", "Educativa"),
 "N6": ("El talento también merece números", "Experta en talento", "Reflexiva"),
 "N7": ("¿Cuántas plataformas abres para un proceso de RH?", "Innovadora", "Comercial"),
 "N8": ("Un buen sueldo no basta para quedarse", "Experta en talento", "Reflexiva"),
 "N9": ("Ruta de incorporación (onboarding, documento)", "Experta en talento", "Educativa"),
 "N10": ("AI Course Builder", "Innovadora", "Comercial"),
 "N11": ("Conocimiento compartido (quien sabe cómo se hace)", "Experta en talento", "Reflexiva"),
 "N12": ("Por qué tu equipo no termina los cursos", "Experta en talento", "Educativa"),
 "N13": ("Tu empresa documenta lo que sabe (AI Course Builder)", "Innovadora", "Comercial"),
 "N14": ("La mejor encuesta es la que sí mandas", "Experta en talento", "Educativa"),
 "HIST": ("Historia (sin texto en la fuente)", "Sin clasificar", "—"),
 "HISTFB": ("Historia de Facebook (sin texto en la fuente)", "Sin clasificar", "—"),
}

# (fecha, red, formato, tema, impresiones, likes, comentarios, compartidos, url)
P = []
def add(fecha, red, formato, tema, imp, likes, com, sh, url): P.append(dict(fecha=fecha, red=red, formato=formato, tema=tema, imp=imp, likes=likes, com=com, sh=sh, url=url))

# Instagram · publicaciones del feed (impresiones = Views; compartidos: Metricool solo los da en algunas)
IG = "https://www.instagram.com/p/"
for f, code, fmt, t, imp, l, c, s in [
 ("2026-11-19","Df5wBNiiHwI","Carrusel","N12",42,4,0,None),
 ("2026-11-09","Dfh1UskoDfT","Carrusel","N5",99,5,0,None),
 ("2026-11-05","DfYL81JFEeK","Carrusel","N5",77,5,0,None),
 ("2026-11-05","DfX82R8IBWR","Carrusel","N4",78,4,0,None),
 ("2026-11-04","DfTVYbdmwpY","Carrusel","N3",65,5,0,None),
 ("2026-10-31","DfKsnm5inps","Carrusel","O19",108,4,0,None),
 ("2026-10-28","DfC9VtWAhJR","Carrusel","O14",103,3,0,None),
 ("2026-10-28","DfCu7xMGwos","Imagen","O17",55,5,0,None),
 ("2026-10-26","De9xKiZI906","Carrusel","O10",117,6,0,1),
 ("2026-10-15","Dehhvo-Ah_-","Carrusel","O8",88,4,0,None),
 ("2026-10-12","DeaV9ppgKr0","Carrusel","O7",130,6,0,None),
 ("2026-10-07","DeNYdzxgVAw","Carrusel","O5",157,7,0,None),
 ("2026-10-06","DeKmjHllWU_","Carrusel","O4",150,10,1,6),
 ("2026-10-03","DeCnzn6oH8h","Carrusel","O3",196,12,0,None),
 ("2026-10-02","Dd_96ZJoPNH","Carrusel","O2",301,10,0,2),
 ("2026-09-22","DdmjWsnDc7H","Carrusel","S2",124,11,0,9),
 ("2026-09-19","Ddc1bKyF6FC","Imagen","S1",282,13,0,4),
]: add(f,"Instagram",fmt,t,imp,l,c,s,IG+code+"/")

# Instagram · reels (impresiones = Views)
for f, code, t, imp, l, c, s in [
 ("2026-11-17","Df2Ulj1FLvr","N11",60,2,0,0),
 ("2026-11-12","DfqIlNID-xu","N10",153,8,0,1),
 ("2026-11-12","Dfpq6FADxuv","N8",73,6,0,0),
 ("2026-11-10","DfkWDK8DV7Z","N7",123,9,0,0),
 ("2026-11-07","Dfcj3vzjTeV","N6",72,6,0,0),
 ("2026-10-27","DfA4KbwP94t","O16",109,6,0,0),
 ("2026-10-27","DfAQdroFf8f","O15",104,7,0,1),
 ("2026-10-24","De3Cay1AbCM","O4",203,11,0,8),
 ("2026-10-21","DevNwUTMv6I","O12",190,10,0,5),
 ("2026-10-16","DeiixqTPvXo","O9",227,14,0,4),
 ("2026-10-08","DePkMrQxbkc","O6",224,12,1,0),
 ("2026-09-25","DduT_CtsIG8","S3",515,13,2,5),
]: add(f,"Instagram","Reel",t,imp,l,c,s,"https://www.instagram.com/reel/"+code+"/")

# Instagram · historias (impresiones; comentarios = respuestas; no tienen likes ni compartidos)
for f, sid, imp, rep in [
 ("2026-11-13","4029749194189752957",20,0),
 ("2026-11-12","4029081315516986121",14,0),
 ("2026-11-12","4028952089673473698",16,1),
 ("2026-11-11","4027805611177500103",26,0),
 ("2026-11-09","4026734250887733017",18,0),
 ("2026-11-03","4022479480853733607",86,0),
 ("2026-11-03","4022407933645097120",13,0),
]: add(f,"Instagram","Historia","HIST",imp,None,rep,None,"https://www.instagram.com/stories/go_lapzo/"+sid)

# Facebook · publicaciones (impresiones totales; todas orgánicas: pagadas = 0)
FB = "https://facebook.com/1659210192576329/posts/"
for f, pid, fmt, t, imp, l, c, s in [
 ("2026-11-19","1676746467489368","Álbum","N12",19,0,0,0),
 ("2026-11-09","1666734045157277","Álbum","N5",73,0,0,0),
 ("2026-11-05","1662444362252912","Álbum","N5",68,1,0,1),
 ("2026-11-05","1662366418927373","Álbum","N4",65,1,0,1),
 ("2026-11-04","1660338059130209","Álbum","N3",125,3,0,1),
 ("2026-10-31","1656986249465390","Álbum","O19",109,1,0,0),
 ("2026-10-28","1653953933101955","Álbum","O14",97,1,0,0),
 ("2026-10-28","1653852399778775","Imagen","O17",91,1,0,1),
 ("2026-10-26","1651956736635008","Álbum","O10",71,0,0,0),
 ("2026-10-19","1645325167298165","Enlace","O11",106,2,0,0),
 ("2026-10-15","1641576804339668","Álbum","O8",89,0,0,0),
 ("2026-10-15","1641576361006379","Álbum","O8",176,1,0,0),
 ("2026-10-12","1638714897959192","Álbum","O7",118,1,0,0),
 ("2026-10-07","1634010671762948","Álbum","O5",111,3,0,0),
 ("2026-10-06","1633033865193962","Álbum","O4",130,3,0,0),
 ("2026-10-03","1630223915474957","Álbum","O3",109,2,0,0),
 ("2026-10-02","1629259882238027","Álbum","O2",116,2,0,0),
 ("2026-10-01","1627492942414721","Imagen","O1",110,2,0,0),
 ("2026-09-22","1619661989864483","Álbum","S2",100,1,0,0),
 ("2026-09-19","1616375173526498","Imagen","S1",147,3,0,1),
]: add(f,"Facebook",fmt,t,imp,l,c,s,FB+pid)

# Facebook · reels (impresiones = reproducciones; Metricool no da comentarios ni compartidos de reels)
# comentarios y compartidos: Metricool no los da para reels de Facebook; se completan con HubSpot.
for f, rid, t, imp, l, c, sh in [
 ("2026-11-22","2521736088316301","N14",250,1,0,0),
 ("2026-11-17","28606914692319621","N11",192,1,0,0),
 ("2026-11-15","1853456759298291","N10",290,2,0,0),
 ("2026-11-12","1770762847367790","N8",565,1,0,0),
 ("2026-11-10","2424825538289478","N7",10377,31,0,0),
 ("2026-11-07","990593957434490","N6",5749,21,0,1),
 ("2026-10-27","1742927086807213","O16",309,1,0,0),
 ("2026-10-27","1649745909896037","O15",81,0,0,0),
 ("2026-10-24","1799093927847494","O4",236,2,0,0),
 ("2026-10-21","1134557822371263","O12",251,1,0,0),
 ("2026-10-16","2529511920904184","O9",308,2,0,0),
 ("2026-10-08","2719688528428910","O6",295,2,0,0),
 ("2026-09-25","2107238866571121","S3",311,6,0,1),
]:
    add(f,"Facebook","Reel",t,imp,l,c,sh,"https://www.facebook.com/reel/"+rid+"/"); P[-1]["hs"] = "comentarios y compartidos"

# TikTok · videos (impresiones = Views)
for f, vid, t, imp, l, c, s in [
 ("2026-11-12","7707400839622708501","N10",535,14,0,1),
 ("2026-11-12","7707349358710295816","N8",464,11,0,0),
 ("2026-11-10","7706582004640402708","N7",180,2,0,0),
 ("2026-11-09","7706225961062157588","N6",189,8,0,0),
 ("2026-10-28","7701743114481929493","O15",599,13,0,0),
 ("2026-10-28","7701741158275353876","O4",169,7,0,0),
 ("2026-10-27","7701466327608823060","O4",215,7,0,11),
 ("2026-10-27","7701460908668669205","O16",99,2,0,0),
 ("2026-10-19","7698450686626794772","O9",671,20,0,2),
 ("2026-10-09","7694741663297621268","O6",127,4,0,1),
 ("2026-09-25","7689512251581091092","S3",292,13,0,0),
]: add(f,"TikTok","Video",t,imp,l,c,s,"https://www.tiktok.com/@go_lapzo/video/"+vid)

# Publicaciones que Metricool no registró y HubSpot sí (fecha en UTC, igual que Metricool).
def add_hs(*a):
    add(*a); P[-1]["fuente"] = "HubSpot"
for f, red, fmt, t, imp, l, c, sh, url in [
 ("2026-11-22","Instagram","Reel","N14",78,4,0,6,"https://www.instagram.com/reel/DgD7fVREbJQ/"),
 ("2026-11-19","TikTok","Video","N11",462,33,0,0,"https://www.tiktok.com/@go_lapzo/video/7709920922492357908"),  # Metricool se quedó en 66 reproducciones
 ("2026-11-22","TikTok","Video","N14",0,0,0,0,"https://www.tiktok.com/@go_lapzo/video/7711025537925319988"),
 ("2026-10-28","Facebook","Publicación","O17",21,1,0,0,"https://www.facebook.com/613311597166199/posts/1653199913177357"),
 ("2026-10-26","Facebook","Publicación","O10",4,0,0,0,"https://www.facebook.com/613311597166199/posts/1651319543365394"),
 ("2026-10-15","Facebook","Publicación","O8",5,0,0,0,"https://www.facebook.com/613311597166199/posts/1641453464352002"),
 ("2026-11-05","Facebook","Publicación","N6",0,0,0,0,"https://www.facebook.com/1146024434586491"),
 ("2026-10-28","Instagram","Publicación","O17",40,4,0,None,"https://www.instagram.com/p/DfBGDxRDjBf/"),
 ("2026-10-26","Instagram","Publicación","O10",23,3,0,None,"https://www.instagram.com/p/De8IvGFlG9H/"),
 ("2026-10-27","Instagram","Reel","O16",2,0,0,0,"https://www.instagram.com/reel/DfAzXiOAJB6/"),
]: add_hs(f,red,fmt,t,imp,l,c,sh,url)
# Historias de Instagram antes del 3 nov (Metricool no las tiene). Comentarios = respuestas.
for f, sid, imp, rep in [
 ("2026-10-29","4018941631341013105",15,0), ("2026-10-27","4017475420924489222",11,0), ("2026-10-27","4017459014316889886",15,0),
 ("2026-10-27","4016845524962413857",10,1), ("2026-10-26","4016598725405124741",15,0), ("2026-10-24","4014689840611201752",19,0),
 ("2026-10-22","4013230358387512898",11,0), ("2026-10-21","4012487949232687562",19,0), ("2026-10-16","4008919856657033582",17,0),
 ("2026-10-16","4008892912556332635",22,1), ("2026-10-12","4006611554266005613",17,0),
]: add_hs(f,"Instagram","Historia","HIST",imp,None,rep,None,"https://www.instagram.com/stories/go_lapzo/"+sid)
# Historias de Facebook (Metricool no las tiene)
for f, sid in [
 ("2026-11-15","UzpfSVNDOjIyMTY1NTE4NTg4OTQxNDU="), ("2026-11-12","UzpfSVNDOjEwODA4OTc2OTQ5NzgyOTM="), ("2026-11-12","UzpfSVNDOjEzOTY2MzAwMTIyODE2MzY="),
 ("2026-11-12","UzpfSVNDOjEwMTM3MjY5MDUxMDQ1NTA="), ("2026-11-11","UzpfSVNDOjIyMjAwMDk2MjIyNDk3NjE="), ("2026-11-10","UzpfSVNDOjE0NjE2NzYzOTI1ODA2ODk="),
 ("2026-11-07","UzpfSVNDOjE0MjQ0MjAzODk4NjEyNjY="), ("2026-11-05","UzpfSVNDOjE4NjM0OTU0OTc5ODU4MDM="), ("2026-11-05","UzpfSVNDOjE0NjYxMzU4OTg4MTM0NjQ="),
]: add_hs(f,"Facebook","Historia","HISTFB",0,None,0,0,"https://facebook.com/stories/100537761776921/"+sid+"/?view_single=1")

# LinkedIn · HubSpot (HubSpot no distingue formato ni da clics)
LI = "https://www.linkedin.com/feed/update/urn:li:"
for f, urn, fmt, t, imp, l, c, s in [
 ("2026-11-20","share:7529572846990233600","Post","N13",170,8,0,0),
 ("2026-11-17","ugcPost:7526773977382338560","Post","N12",322,7,0,0),
 ("2026-11-13","ugcPost:7526721887725453312","Post","N10",205,5,0,0),
 ("2026-11-12","ugcPost:7526708442032410624","Post","N8",293,9,0,0),
 ("2026-11-12","ugcPost:7526689422331822080","Documento","N9",246,7,0,1),
 ("2026-11-09","ugcPost:7525606405127446528","Post","N5",304,5,0,1),
 ("2026-11-09","ugcPost:7525587134225780736","Post","N5",38,1,0,0),
 ("2026-11-05","ugcPost:7524216742357663745","Post","N5",112,2,0,2),
 ("2026-11-05","ugcPost:7524214147534868480","Post","N4",314,7,0,0),
 ("2026-11-03","share:7523416823611158528","Post","N2",331,6,0,1),
 ("2026-11-02","share:7523065861415350273","Post","N1",258,8,0,0),
 ("2026-10-28","share:7521238796965707776","Post","O17",448,11,0,2),
 ("2026-10-28","share:7521220528045711360","Post","O18",380,12,0,3),
 ("2026-10-27","ugcPost:7520880599151194112","Post","O15",287,5,0,1),
 ("2026-10-27","ugcPost:7520875103484628993","Post","O14",327,11,0,0),
 ("2026-10-26","ugcPost:7520620606992723968","Post","O9",303,9,0,1),
 ("2026-10-26","share:7520508174320300032","Post","O13",216,5,0,0),
 ("2026-10-19","ugcPost:7518021934752792576","Post","O10",606,9,2,0),
 ("2026-10-14","ugcPost:7516164252156657664","Post","O8",584,9,0,0),
 ("2026-10-13","ugcPost:7515825487068225536","Post","O7",547,11,0,1),
 ("2026-10-07","ugcPost:7513638080789024768","Post","O5",532,8,0,0),
 ("2026-10-06","ugcPost:7513381161449144320","Post","O4",499,7,0,1),
 ("2026-10-05","ugcPost:7512962578621300737","Post","O3",720,16,0,5),
 ("2026-09-22","ugcPost:7508255084040970240","Post","S2",545,6,0,1),
 ("2026-09-21","share:7507816108410699777","Post","S1",746,8,0,0),
]: add(f,"LinkedIn",fmt,t,imp,l,c,s,LI+urn)

# Seguidores (Metricool), día por día.
# Facebook: total de seguidores al cierre de cada día.
FB_TOTAL = {
 "2026-08-31": 2409,
 "2026-09-01": 2410, "2026-09-02": 2411, "2026-09-03": 2412, "2026-09-04": 2413, "2026-09-05": 2414, "2026-09-06": 2414,
 "2026-09-07": 2415, "2026-09-08": 2415, "2026-09-09": 2416, "2026-09-10": 2417, "2026-09-11": 2418, "2026-09-12": 2418,
 "2026-09-13": 2419, "2026-09-14": 2421, "2026-09-15": 2422, "2026-09-16": 2423, "2026-09-17": 2424, "2026-09-18": 2430,
 "2026-09-19": 2433, "2026-09-20": 2433, "2026-09-21": 2433, "2026-09-22": 2431, "2026-09-23": 2431, "2026-09-24": 2433,
 "2026-09-25": 2434, "2026-09-26": 2434, "2026-09-27": 2434, "2026-09-28": 2435, "2026-09-29": 2435, "2026-09-30": 2435,
 "2026-10-01": 2435, "2026-10-02": 2435, "2026-10-03": 2435, "2026-10-04": 2435, "2026-10-05": 2435, "2026-10-06": 2435,
 "2026-10-07": 2435, "2026-10-08": 2435, "2026-10-09": 2435, "2026-10-10": 2435, "2026-10-11": 2435, "2026-10-12": 2434,
 "2026-10-13": 2435, "2026-10-14": 2436, "2026-10-15": 2436, "2026-10-16": 2436, "2026-10-17": 2436, "2026-10-18": 2436,
 "2026-10-19": 2437, "2026-10-20": 2438, "2026-10-21": 2437, "2026-10-22": 2436, "2026-10-23": 2437, "2026-10-24": 2437,
 "2026-10-25": 2438, "2026-10-26": 2441, "2026-10-27": 2442, "2026-10-28": 2443, "2026-10-29": 2445, "2026-10-30": 2445,
 "2026-10-31": 2447,
 "2026-11-01": 2447, "2026-11-02": 2450, "2026-11-03": 2454, "2026-11-04": 2454, "2026-11-05": 2456, "2026-11-06": 2456,
 "2026-11-07": 2469, "2026-11-08": 2470, "2026-11-09": 2473, "2026-11-10": 2483, "2026-11-11": 2488, "2026-11-12": 2490,
 "2026-11-13": 2493, "2026-11-14": 2492, "2026-11-15": 2492, "2026-11-16": 2492, "2026-11-17": 2495,
 "2026-11-18": 2495, "2026-11-19": 2495, "2026-11-20": 2494, "2026-11-21": 2494,
}
# Instagram: (ganados, perdidos) por día.
IG_DIA = {
 "2026-09-01": (0,0), "2026-09-02": (0,0), "2026-09-03": (0,0), "2026-09-04": (1,0), "2026-09-05": (1,1), "2026-09-06": (0,1),
 "2026-09-07": (0,0), "2026-09-08": (1,0), "2026-09-09": (1,0), "2026-09-10": (4,0), "2026-09-11": (2,0), "2026-09-12": (1,0),
 "2026-09-13": (1,0), "2026-09-14": (0,0), "2026-09-15": (1,0), "2026-09-16": (0,0), "2026-09-17": (0,0), "2026-09-18": (2,1),
 "2026-09-19": (0,0), "2026-09-20": (1,0), "2026-09-21": (0,0), "2026-09-22": (0,0), "2026-09-23": (0,0), "2026-09-24": (0,0),
 "2026-09-25": (10,0), "2026-09-26": (1,0), "2026-09-27": (1,0), "2026-09-28": (0,0), "2026-09-29": (1,0), "2026-09-30": (0,0),
 "2026-10-01": (0,1), "2026-10-02": (2,1), "2026-10-03": (0,0), "2026-10-04": (0,0), "2026-10-05": (1,0), "2026-10-06": (0,0),
 "2026-10-07": (0,0), "2026-10-08": (4,0), "2026-10-09": (2,0), "2026-10-10": (2,0), "2026-10-11": (1,0), "2026-10-12": (0,0),
 "2026-10-13": (0,0), "2026-10-14": (0,0), "2026-10-15": (1,0), "2026-10-16": (0,0), "2026-10-17": (0,1), "2026-10-18": (0,1),
 "2026-10-19": (1,0), "2026-10-20": (1,0), "2026-10-21": (0,0), "2026-10-22": (0,0), "2026-10-23": (1,0), "2026-10-24": (2,0),
 "2026-10-25": (1,0), "2026-10-26": (1,1), "2026-10-27": (2,0), "2026-10-28": (3,1), "2026-10-29": (3,0), "2026-10-30": (0,1),
 "2026-10-31": (0,0),
 "2026-11-01": (1,0), "2026-11-02": (4,0), "2026-11-03": (2,1), "2026-11-04": (4,0), "2026-11-05": (2,2), "2026-11-06": (1,0),
 "2026-11-07": (1,0), "2026-11-08": (0,0), "2026-11-09": (0,0), "2026-11-10": (0,0), "2026-11-11": (4,0), "2026-11-12": (3,0),
 "2026-11-13": (0,0), "2026-11-14": (1,0), "2026-11-15": (1,1), "2026-11-16": (3,0), "2026-11-17": (0,0),
 "2026-11-18": (1,0), "2026-11-19": (1,2), "2026-11-20": (0,0), "2026-11-21": (0,0),
}

# Publicaciones que se borraron y se volvieron a subir (revisado con el equipo el 17 nov 2026).
# No se cuentan en los reportes.
BORRADAS = {
 "https://facebook.com/1659210192576329/posts/1641576804339668",
 "https://www.facebook.com/613311597166199/posts/1641453464352002",
 "https://www.facebook.com/613311597166199/posts/1651319543365394",
 "https://www.facebook.com/1146024434586491",
 "https://www.instagram.com/p/De8IvGFlG9H/",
 "https://www.instagram.com/p/DfBGDxRDjBf/",
 "https://www.instagram.com/reel/DfAzXiOAJB6/",
 "https://www.linkedin.com/feed/update/urn:li:ugcPost:7524216742357663745",
 "https://www.linkedin.com/feed/update/urn:li:ugcPost:7525587134225780736",
}

# Leads de redes atendidos por Marketing. Fuente: hoja «Registro de leads orgánicos (redes)», pestaña Q4 2026
# (leída el 23 nov 2026). Sin nombres, correos ni teléfonos: esos datos se quedan en la hoja.
# (fecha, red, origen, pieza o anuncio de origen, interés, estado, pasado a, ¿es lead?)
# Es lead si en la hoja tiene teléfono o correo (o ambos), haya tenido seguimiento o no.
# Leads que necesitan atención: (fecha del lead, texto). Sin datos de contacto.
LEADS_URGENTES = [
 ("2026-11-02", "El lead de Imagen Creativa (2 nov, por mensaje a un anuncio) pidió demo de AI Course Builder y una propuesta para 250 cursos. "
  "Hace unas dos semanas se le dio seguimiento y se pasó a Fer, pero a 16 días del primer contacto sigue sin demo habilitada. "
  "El 18 nov comentó en público «¡Sigo esperando mi acceso!». Se reescaló a Ricardo Garza (leads), que está en contacto con Fernando Núñez (líder de ventas)."),
]
LEADS_FUENTE = "Registro de leads orgánicos (redes) · pestaña Q4 2026"
LEADS_LEIDO = "23 de noviembre de 2026"
LEADS = [
 ("2026-10-13", "Facebook", "Mensaje directo", "Mensaje directo (sin anuncio)", "Información general", "Pasado a Ventas", "Julio", True),
 ("2026-11-02", "Facebook", "Anuncio", "Mensaje directo a un anuncio (Facebook)", "AI Course Builder", "Reescalado a Ventas", "Ricardo Garza → Fernando Núñez", True),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio Elearning", "Universidad corporativa (CyA)", "Pasado a Ventas", "Julio", True),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de universidad corporativa", "Universidad corporativa (CyA)", "Pasado a Ventas", "Julio", True),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de AI Course Builder (por mensaje directo)", "AI Course Builder", "Esperando datos", "", False),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de universidad corporativa", "Universidad corporativa (CyA)", "Esperando datos", "", False),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de universidad corporativa", "Por aclarar (hosting)", "Esperando respuesta", "", False),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de AI Course Builder", "AI Course Builder", "Esperando datos", "", False),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de AI Course Builder", "AI Course Builder", "Esperando datos", "", False),
 ("2026-11-17", "Facebook", "Anuncio", "Anuncio de AI Course Builder (otro diseño)", "AI Course Builder", "Pendiente de seguimiento", "", False),
]

# Datos de video (Metricool, extraídos el 23 nov 2026). Clave: enlace de la publicación.
# prom = tiempo promedio visto (s); quedan3 = % de vistas que pasan de los 3 primeros segundos (Instagram);
# guard = guardados (Instagram); dur = duración del video en s (TikTok). Lo que la red no da, no se pone.
VIDEO = {}
for code, prom, q3, g in [
 ("Df2Ulj1FLvr",3.401,6.1,0), ("DfqIlNID-xu",5.612,15.7,1), ("Dfpq6FADxuv",7.909,35.3,0), ("DfkWDK8DV7Z",10.694,19.5,0),
 ("Dfcj3vzjTeV",5.045,27.7,0), ("DfA4KbwP94t",7.652,23.3,2), ("DfAQdroFf8f",9.363,21.4,0), ("De3Cay1AbCM",7.192,20.6,3),
 ("DevNwUTMv6I",8.624,27.7,3), ("DeiixqTPvXo",11.405,29.6,2), ("DePkMrQxbkc",5.778,25.3,3), ("DduT_CtsIG8",4.617,23.2,3),
]: VIDEO["https://www.instagram.com/reel/"+code+"/"] = dict(prom=prom, quedan3=q3, guard=g)
for rid, prom in [
 ("2521736088316301",2), ("28606914692319621",3), ("1853456759298291",3), ("1770762847367790",5), ("2424825538289478",4),
 ("990593957434490",4), ("1742927086807213",2), ("1649745909896037",4), ("1799093927847494",2), ("1134557822371263",3),
 ("2529511920904184",5), ("2719688528428910",3), ("2107238866571121",3),
]: VIDEO["https://www.facebook.com/reel/"+rid+"/"] = dict(prom=prom)
for vid, dur in [
 ("7709920922492357908",23), ("7707400839622708501",21), ("7707349358710295816",23), ("7706582004640402708",32),
 ("7706225961062157588",31), ("7701743114481929493",33), ("7701741158275353876",37), ("7701466327608823060",37),
 ("7701460908668669205",17), ("7698450686626794772",36), ("7694741663297621268",17), ("7689512251581091092",19),
]: VIDEO["https://www.tiktok.com/@go_lapzo/video/"+vid] = dict(dur=dur)
# Mismo archivo de video que su TikTok (según lo programado en Metricool): misma duración.
for url, dur in [("https://www.instagram.com/reel/Dfpq6FADxuv/",23), ("https://www.facebook.com/reel/1770762847367790/",23)]:
    VIDEO[url]["dur"] = dur
# Duración leída del archivo de video en Metricool (autorizado solo para estas piezas, 23 nov 2026; no se guardó copia).
for url, dur in [
 ("https://www.instagram.com/reel/DfkWDK8DV7Z/",32.5), ("https://www.facebook.com/reel/2424825538289478/",32.5),
 ("https://www.instagram.com/reel/DfqIlNID-xu/",21.2), ("https://www.facebook.com/reel/1853456759298291/",21.2),
 ("https://www.instagram.com/reel/Df2Ulj1FLvr/",23.5), ("https://www.facebook.com/reel/28606914692319621/",23.5),
 ("https://www.instagram.com/reel/DgD7fVREbJQ/",33.0), ("https://www.facebook.com/reel/2521736088316301/",33.0),
]: VIDEO.setdefault(url, {})["dur"] = dur

# OKRs Q4 2026 de la Content & Social Media Specialist (del PDF «Mi plan de OKRs», compartido el 23 nov 2026).
OKR = dict(
    inicio="2026-10-01", fin="2026-12-31",
    kr1_base=5, kr1_meta_mes=25, kr1_meta_trim=75,
    # Anuncios BOFU (pagados) que también cuentan como piezas en KR1, por mes. Octubre: nota del equipo.
    bofu={"2026-10": 5},
    kr2_base=5, kr2_meta=15,
    kr3_meta_sem=1,
    kr4_inicio="2026-11-10",
    kr5_pct=100, kr5_nota="Confirmado por la usuaria el 23 nov 2026: todas las piezas de video ya se editan con el proceso automatizado.",
)
