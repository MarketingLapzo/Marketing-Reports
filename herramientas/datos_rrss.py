# Datos extraídos el 17 nov 2026. LinkedIn: HubSpot Social. Instagram, Facebook, TikTok: Metricool (marca go_lapzo).
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
 "HIST": ("Historia (sin texto en la fuente)", "Sin clasificar", "—"),
 "HISTFB": ("Historia de Facebook (sin texto en la fuente)", "Sin clasificar", "—"),
}

# (fecha, red, formato, tema, impresiones, likes, comentarios, compartidos, url)
P = []
def add(fecha, red, formato, tema, imp, likes, com, sh, url): P.append(dict(fecha=fecha, red=red, formato=formato, tema=tema, imp=imp, likes=likes, com=com, sh=sh, url=url))

# Instagram · publicaciones del feed (impresiones = Views; compartidos: Metricool solo los da en algunas)
IG = "https://www.instagram.com/p/"
for f, code, fmt, t, imp, l, c, s in [
 ("2026-11-09","Dfh1UskoDfT","Carrusel","N5",90,5,0,None),
 ("2026-11-05","DfYL81JFEeK","Carrusel","N5",73,5,0,None),
 ("2026-11-05","DfX82R8IBWR","Carrusel","N4",74,4,0,None),
 ("2026-11-04","DfTVYbdmwpY","Carrusel","N3",59,5,0,None),
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
 ("2026-11-12","DfqIlNID-xu","N10",142,8,0,1),
 ("2026-11-12","Dfpq6FADxuv","N8",70,4,0,0),
 ("2026-11-10","DfkWDK8DV7Z","N7",121,9,0,0),
 ("2026-11-07","Dfcj3vzjTeV","N6",69,6,0,0),
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
 ("2026-11-09","1666734045157277","Álbum","N5",55,0,0,0),
 ("2026-11-05","1662444362252912","Álbum","N5",62,1,0,1),
 ("2026-11-05","1662366418927373","Álbum","N4",60,1,0,1),
 ("2026-11-04","1660338059130209","Álbum","N3",117,3,0,1),
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
 ("2026-11-15","1853456759298291","N10",266,2,0,0),
 ("2026-11-12","1770762847367790","N8",549,1,0,0),
 ("2026-11-10","2424825538289478","N7",10365,31,0,0),
 ("2026-11-07","990593957434490","N6",5744,21,0,1),
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
 ("2026-11-12","7707400839622708501","N10",1,0,0,0),
 ("2026-11-12","7707349358710295816","N8",83,1,0,0),
 ("2026-11-10","7706582004640402708","N7",157,2,0,0),
 ("2026-11-09","7706225961062157588","N6",184,8,0,0),
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
 ("2026-11-13","ugcPost:7526721887725453312","Post","N10",156,4,0,0),
 ("2026-11-12","ugcPost:7526708442032410624","Post","N8",271,9,0,0),
 ("2026-11-12","ugcPost:7526689422331822080","Documento","N9",209,7,0,1),
 ("2026-11-09","ugcPost:7525606405127446528","Post","N5",276,3,0,0),
 ("2026-11-09","ugcPost:7525587134225780736","Post","N5",38,1,0,0),
 ("2026-11-05","ugcPost:7524216742357663745","Post","N5",112,2,0,2),
 ("2026-11-05","ugcPost:7524214147534868480","Post","N4",289,6,0,0),
 ("2026-11-03","share:7523416823611158528","Post","N2",315,6,0,1),
 ("2026-11-02","share:7523065861415350273","Post","N1",248,8,0,0),
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
 "2026-11-13": 2493, "2026-11-14": 2493, "2026-11-15": 2494, "2026-11-16": 2494,
}
# Instagram: (ganados, perdidos) por día. Metricool no tiene el 15 y 16 nov.
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
 "2026-11-13": (0,0), "2026-11-14": (1,0),
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
