# Diseño del reporte aprobado el 26 de noviembre de 2026 (lienzo en herramientas/diseno-reporte/).
# generar_rrss.py llama a mensual() y semanal(); los números salen de datos_rrss.py.
import html
import datos_rrss as d

e = html.escape
REDES = ["LinkedIn", "Instagram", "Facebook", "TikTok"]
COL = {"LinkedIn": "#0A66C2", "Instagram": "#E1306C", "Facebook": "#01A86C", "TikTok": "#1D1B2E"}
CORTA = {"LinkedIn": "LinkedIn", "Instagram": "IG", "Facebook": "FB", "TikTok": "TikTok"}
NARANJA = ["#FEF0DE", "#FDE3C4", "#F8A94A", "#D9700A"]
MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# Textos que escribe el equipo (no salen de los datos). Si falta un mes, el reporte arma uno con los datos.
RESUMEN = {
    "2026-11": dict(
        funciono="Reels de Instagram (7.6 % de interacción) y carruseles de Instagram (6.3 %). Sin contar Facebook, la interacción subió a 3.9 % (octubre: 3.6 %).",
        alcance="Reels de Facebook: 75 % de las impresiones del mes, pero solo 0.3 de cada 100 vistas terminó en like o compartido, y ningún comentario.",
        cambiamos="Pasar a reel los estáticos que dependen del copy. Sumar webinars y sesiones en vivo como formato de reconocimiento.",
        repetir="Reels de Instagram, carruseles educativos y webinars o sesiones en vivo.",
        ajustar="Estáticos que dependen del copy: pasarlos a reel. Los que comunican desde la imagen se quedan.",
        probar="En reels de Facebook, cerrar con una pregunta de una palabra para convertir vistas en comentarios.",
    ),
}
# Frase de qué pasó con cada pieza en el reporte semanal: {(inicio de semana, tema): texto}.
NOTA_PIEZA = {
    ("2026-11-16", "N11"): "TikTok trajo 33 de sus 36 interacciones. El mismo reel en Instagram y Facebook casi no movió.",
    ("2026-11-16", "N14"): "En Instagram, 6 de sus 10 interacciones fueron compartidos: la plantilla se comparte. Solo llevaba 2 días al corte.",
    ("2026-11-16", "N12"): "LinkedIn le dio el alcance; Instagram, la mejor tasa con muy pocas impresiones.",
    ("2026-11-16", "N13"): "El mejor de la semana en LinkedIn por tasa (4.8 %), con 1 compartido.",
}

def n(v): return v or 0
def inter(p): return n(p["likes"]) + n(p["com"]) + n(p["sh"])
def suma(ps): return sum(n(p["imp"]) for p in ps), sum(inter(p) for p in ps)
def tasa(ps):
    i, t = suma(ps); return 100 * t / i if i else None
def fi(v): return f"{v:,.0f}"
def fp(v): return "—" if v is None else f"{v:.1f} %"
def fecha(s): return f"{int(s[8:])} {MES[int(s[5:7]) - 1][:3]}"
def sin_hist(ps): return [p for p in ps if p["formato"] != "Historia" and not p["tema"].startswith("HIST")]

def formato(p):
    if p.get("formato_real"): return p["formato_real"]
    f = p["formato"]
    if f in ("Reel", "Video"): return "Reel"
    if f in ("Carrusel", "Álbum", "Documento"): return "Carrusel"
    if f == "Historia": return None
    return "Estático"

def pieza(t):
    if t in d.PIEZA: return d.PIEZA[t]
    return (None, d.TEMAS.get(t, (t,))[0])
def nombre_pieza(t):
    num, nom = pieza(t); return f"{num} · {nom}" if num else nom

# ---------------------------------------------------------------- piezas visuales
def chip_tasa(v, grande=False):
    if v is None: return '<span style="color:#5A5770">—</span>'
    bg, fg = ("#E3F6EE", "#0B5E41") if v >= 3.5 else (("#FDE8E6", "#9B1C14") if v < 1.5 else ("#ECEAF2", "#4A4760"))
    pad = "6px 10px;font-size:18px" if grande else "2px 8px"
    return f'<span style="background:{bg};color:{fg};border-radius:6px;padding:{pad};font-weight:700;white-space:nowrap">{v:.1f} %</span>'

def cambio(a, b, pct=False, sufijo=""):
    """▲/▼/= con cuánto cambió. pct=True compara puntos de porcentaje."""
    if a is None or b is None: return ""
    dv = a - b
    if pct:
        dv = round(a, 1) - round(b, 1)
        r = dv; umbral = 0.05 * b if b else 0.05
        sube, baja = dv > umbral, dv < -umbral
        txt = f'{"subió" if dv > 0 else "bajó"} {abs(dv):.1f}'
    else:
        r = 100 * dv / b if b else (100 if dv else 0)
        sube, baja = r > 5, r < -5
        txt = f'{"subió" if dv > 0 else "bajó"} {fi(abs(dv))}' + (f" ({r:+.0f} %)" if b else "")
    col = "#0B5E41" if sube else ("#9B1C14" if baja else "#4A4760")
    fl = "▲" if sube else ("▼" if baja else "=")
    return f'<span style="color:{col};font-size:13px">{fl} {txt}{sufijo}</span>'

def nota(titulo, texto):
    return (f'<details style="font-size:13px;color:#5A5770"><summary style="cursor:pointer;font-weight:600;color:#6E3FD8">? {e(titulo)}</summary>'
            f'<p style="margin:6px 0 0;line-height:1.5">{texto}</p></details>')

def tarjeta(contenido, extra=""):
    return f'<div style="background:#FFFFFF;border:1px solid #E6E3F0;border-radius:20px;padding:26px 30px;display:flex;flex-direction:column;gap:14px;{extra}">{contenido}</div>'

def h2(t, sub=""):
    return (f'<div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:22px;font-weight:700">{t}</h2>'
            + (f'<p style="margin:0;font-size:14px;color:#5A5770">{sub}</p>' if sub else "") + '</div>')

def kpi(valor, etiqueta, sub="", cambio_html="", nota_html=""):
    return (f'<div style="background:#FFFFFF;border:1px solid #E6E3F0;border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:6px">'
            f'<p style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.02em">{valor}</p>'
            f'<p style="margin:0;font-size:14px;color:#5A5770">{etiqueta}</p>'
            + (f'<p style="margin:0;font-size:13px;color:#5A5770">{sub}</p>' if sub else "") + cambio_html + nota_html + '</div>')

def vinetas(items):
    return ('<ul style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px;font-size:14px;color:#5A5770;line-height:1.5">'
            + "".join(f'<li><b style="color:#1D1B2E">{t}</b> {x}</li>' for t, x in items) + '</ul>')

def envolver(cuerpo):
    return ('<div class="vn" style="font-family:inherit;color:#1D1B2E;display:flex;flex-direction:column;gap:24px;margin:8px 0 40px">'
            '<style>.vn a{color:#6E3FD8}.vn table td,.vn table th{border:none}</style>' + cuerpo + '</div>')

LEYENDA = ('<div style="display:flex;flex-wrap:wrap;gap:8px;font-size:13px">'
           '<span style="background:#E3F6EE;color:#0B5E41;border-radius:999px;padding:4px 10px;font-weight:600">▲ Mejoró más de 5 %</span>'
           '<span style="background:#FDE8E6;color:#9B1C14;border-radius:999px;padding:4px 10px;font-weight:600">▼ Bajó más de 5 %</span>'
           '<span style="background:#ECEAF2;color:#4A4760;border-radius:999px;padding:4px 10px;font-weight:600">= Se mantuvo</span></div>')

# ---------------------------------------------------------------- reporte mensual
def mensual(M, previos, del_mes, corte):
    """M: mes a reportar; previos: meses para comparar, ya recortados a los mismos días (el último es M)."""
    clave = M["clave"]; mp = previos[-2] if len(previos) > 1 else None
    hasta = int(corte[8:]) if clave == corte[:7] else 31
    ps = sin_hist([p for p in d.P if del_mes(p, previos[-1])])
    pp = sin_hist([p for p in d.P if mp and del_mes(p, mp)])
    I, T = suma(ps); IP, TP = suma(pp); er, erp = tasa(ps), tasa(pp)
    nomp = mp["titulo"].split(" ")[0].lower() if mp else ""
    O = d.OKR
    org = O.get("kr1_org", {}).get(clave, len({p["tema"] for p in ps})); bofu = O.get("bofu", {}).get(clave, 0); tot = org + bofu
    R = RESUMEN.get(clave, {})
    out = []

    # Resumen
    fmts = {}
    for p in ps:
        f = formato(p)
        if f: fmts.setdefault((p["red"], f), []).append(p)
    ranking = sorted(((tasa(v), k, suma(v)[0]) for k, v in fmts.items() if suma(v)[0] >= 100), key=lambda x: -x[0])
    peso = sorted(((suma(v)[0], k, tasa(v)) for k, v in fmts.items()), key=lambda x: -x[0])
    auto_f = "; ".join(f"{f} de {r} ({v:.1f} %)" for v, (r, f), _ in ranking[:2]) + "."
    auto_a = (f"{peso[0][1][1]} de {peso[0][1][0]}: {100 * peso[0][0] / I:.0f} % de las impresiones del mes, con {fp(peso[0][2])} de interacción."
              if peso and I else "")
    bloque = lambda t, c, x: f'<div style="display:flex;flex-direction:column;gap:8px"><p style="margin:0;font-size:13px;font-weight:600;color:{c}">{t}</p><p style="margin:0;font-size:16px;line-height:1.5">{x}</p></div>'
    out.append('<section style="background:#1D1B2E;color:#FFFFFF;border-radius:20px;padding:26px 30px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px">'
               + bloque("Qué funcionó", "#7DF5C9", R.get("funciono", auto_f))
               + bloque("Qué dio alcance, pero poca interacción", "#FFB4A8", R.get("alcance", auto_a))
               + (bloque("Qué cambiamos el siguiente mes", "#C7A4FF", R["cambiamos"]) if "cambiamos" in R else "")
               + '</section>')

    # Tarjetas
    pfb = [p for p in ps if p["red"] != "Facebook"]; ppfb = [p for p in pp if p["red"] != "Facebook"]
    out.append(LEYENDA)
    out.append('<section style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">'
               + kpi(f'{tot} <span style="font-size:15px;font-weight:500;color:#5A5770">piezas</span>', f"{org} publicadas (únicas) + {bofu} anuncios BOFU",
                     cambio_html=(f'<span style="font-size:13px;font-weight:600;color:#0B5E41">✅ Meta del mes: {O["kr1_meta_mes"]}</span>' if tot >= O["kr1_meta_mes"] else f'<span style="font-size:13px;color:#5A5770">Meta del mes: {O["kr1_meta_mes"]}</span>'),
                     nota_html=nota("Qué es una pieza única", "Un diseño cuenta una vez aunque salga en varias redes. Si cambia de formato (por ejemplo, carrusel en Instagram y un estático dedicado al copy en LinkedIn), cuenta como otra pieza. Los anuncios BOFU son piezas pagadas para conseguir leads; si también salen en orgánico, cuentan una sola vez."))
               + kpi(fi(I), "impresiones", f"{nomp}: {fi(IP)}" if mp else "", cambio(I, IP) if mp else "",
                     nota("Qué son las impresiones", "Las veces que se vio una publicación, aunque sea la misma persona varias veces. En reels de Facebook es el número de reproducciones."))
               + kpi(fi(T), "interacciones", f"{nomp}: {fi(TP)}" if mp else "", cambio(T, TP) if mp else "",
                     nota("Qué cuenta como interacción", "Likes + comentarios + compartidos, en las cuatro redes."))
               + kpi(fp(er), "tasa de interacción", f"{nomp}: {fp(erp)}" if mp else "", cambio(er, erp, True) if mp else "",
                     nota("Qué es la tasa y por qué cambió",
                          f"Interacciones ÷ impresiones: de cada 100 veces que se vio algo, cuántas tuvieron like, comentario o compartido. "
                          + (f"Sin Facebook en los dos meses: {fp(tasa(pfb))} este mes contra {fp(tasa(ppfb))} en {nomp}." if mp else "")))
               + '</section>')

    # Del contenido al lead
    lm = [l for l in d.LEADS if l[0][:7] == clave]
    contactos, leads = len(lm), sum(1 for l in lm if l[7]); leads_ad = sum(1 for l in lm if l[7] and l[2] == "Anuncio")
    pasos = [(tot, "piezas", "#6E3FD8", 160), (I, "impresiones", "#8B5CF6", 132), (T, "interacciones", "#A78BFA", 100),
             (contactos, "contactos (escribieron)", "#C4B5FD", 70), (leads, "leads (dieron teléfono o correo)", "#01A86C", 44)]
    out.append(tarjeta(h2("Del contenido al lead", "Cada paso del mes, de lo que publicamos a quién nos dejó sus datos.")
        + '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;align-items:end">'
        + "".join(f'<div style="display:flex;flex-direction:column;gap:8px"><div style="height:{h}px;background:{c};border-radius:10px"></div><p style="margin:0;font-size:24px;font-weight:700">{fi(v)}</p><p style="margin:0;font-size:13px;color:#5A5770">{t}</p></div>' for v, t, c, h in pasos)
        + '</div>'
        + f'<p style="margin:0;font-size:14px;color:#5A5770">Contactos y leads al {e(d.LEADS_LEIDO)}. {leads_ad} de los {leads} leads llegaron por un anuncio.</p>'
        + nota("Contacto o lead", "Contacto: alguien que escribió o comentó pidiendo información. Lead: un contacto que ya dio teléfono o correo.")))

    # Por plataforma, mes contra mes
    def red_mes(m, r):
        q = sin_hist([p for p in d.P if del_mes(p, m) and p["red"] == r]); return suma(q)[0], tasa(q)
    cab = "".join(f'<th style="padding:8px;font-weight:600">{e(m["titulo"].split(" ")[0][:3].lower())}</th>' for m in previos)
    filas, vin = "", []
    for r in REDES:
        vals = [red_mes(m, r) for m in previos]
        (iu, tu), (ia, ta) = vals[-1], (vals[-2] if len(vals) > 1 else (None, None))
        cel_i = "".join(f'<td style="padding:8px">{fi(i)}</td>' for i, _ in vals[:-1]) + f'<td style="padding:8px"><b>{fi(iu)}</b> {cambio(iu, ia)}</td>'
        cel_t = "".join(f'<td style="padding:8px">{fp(t)}</td>' for _, t in vals[:-1]) + f'<td style="padding:8px"><b>{fp(tu)}</b> {cambio(tu, ta, True)}</td>'
        filas += f'<tr style="border-top:1px solid #E6E3F0"><td style="padding:10px 8px 10px 0;font-weight:700;color:{COL[r]}">{r}</td>{cel_i}{cel_t}</tr>'
        if ia is not None:
            vin.append((f"{r} ({fi(ia)} → {fi(iu)} impresiones):", f"tasa de {fp(ta)} a {fp(tu)}."))
    out.append(tarjeta(h2("Por plataforma, mes contra mes", f"Del 1 al {hasta} de cada mes." if hasta < 31 else "")
        + f'<div style="overflow-x:auto"><table style="width:100%;min-width:720px;border-collapse:collapse;font-size:14px"><thead><tr style="text-align:left;color:#5A5770;font-size:12px"><th></th><th colspan="{len(previos)}" style="padding:0 8px">Impresiones</th><th colspan="{len(previos)}" style="padding:0 8px">Tasa de interacción</th></tr>'
        + f'<tr style="text-align:left;color:#5A5770"><th style="padding:8px 8px 8px 0">Red</th>{cab}{cab}</tr></thead><tbody>{filas}</tbody></table></div>'
        + vinetas(vin)))

    # Interacciones por mes
    tot_m = [suma(sin_hist([p for p in d.P if del_mes(p, m)]))[1] for m in previos]
    mx = max([suma(sin_hist([p for p in d.P if del_mes(p, m) and p["red"] == r]))[1] for m in previos for r in REDES] + [1])
    grupos, vin2 = "", []
    for r in REDES:
        vs = [suma(sin_hist([p for p in d.P if del_mes(p, m) and p["red"] == r]))[1] for m in previos]
        barras = "".join(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1"><span style="font-size:13px;font-weight:{700 if k == len(vs) - 1 else 500}">{v}</span>'
            f'<div style="width:100%;max-width:48px;height:{max(v / mx * 170, 2):.0f}px;background:{NARANJA[k + 4 - len(vs)] if len(vs) <= 4 else NARANJA[-1]};border-radius:6px 6px 0 0"></div>'
            f'<span style="font-size:12px;color:#5A5770">{e(previos[k]["titulo"][:3])}</span></div>' for k, v in enumerate(vs))
        ch = cambio(vs[-1], vs[-2]) if len(vs) > 1 else ""
        grupos += (f'<div style="display:flex;flex-direction:column;gap:8px"><div style="display:flex;gap:8px;align-items:flex-end;height:220px">{barras}</div>'
                   f'<p style="margin:0;font-size:15px;font-weight:700;color:{COL[r]}">{r}</p><p style="margin:0;font-size:13px">{ch} {"vs " + nomp if ch else ""}</p></div>')
        if len(vs) > 1:
            ia, ta = red_mes(previos[-2], r); iu, tu = red_mes(previos[-1], r)
            vin2.append((f"{r} ({vs[-2]} → {vs[-1]}):", f"impresiones de {fi(ia)} a {fi(iu)}; tasa de {fp(ta)} a {fp(tu)}."))
    tot_html = "".join(
        f'<div><p style="margin:0;font-size:13px;color:#5A5770">{e(m["titulo"][:3])}</p><p style="margin:0;font-size:{30 if k == len(previos) - 1 else 22}px;font-weight:700;color:{"#1D1B2E" if k == len(previos) - 1 else "#8A86A0"}">{fi(tot_m[k])}'
        + (f' <span style="font-size:14px;font-weight:400">{cambio(tot_m[k], tot_m[k - 1])}</span>' if k == len(previos) - 1 and k else "") + '</p></div>'
        for k, m in enumerate(previos))
    out.append(tarjeta('<div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;align-items:flex-end">'
        + h2("Interacciones por mes", "Likes + comentarios + compartidos" + (f", del 1 al {hasta} de cada mes." if hasta < 31 else "."))
        + f'<div style="display:flex;gap:28px;align-items:baseline">{tot_html}</div></div>'
        + f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:28px">{grupos}</div>' + vinetas(vin2)))

    # Impresiones por red, mes a mes
    mult = ""
    for r in REDES:
        vals = [red_mes(m, r) for m in previos]; mxr = max([i for i, _ in vals] + [1])
        barras = "".join(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1"><span style="font-size:12px;font-weight:600">{fi(i)}</span>'
            f'<div style="width:100%;max-width:44px;height:{max(i / mxr * 110, 2):.0f}px;background:{COL[r]};border-radius:6px 6px 0 0"></div>'
            f'<span style="font-size:12px;color:#5A5770">{e(previos[k]["titulo"][:3])}</span><span style="font-size:12px;font-weight:600;color:#4A4760">{fp(t)}</span></div>'
            for k, (i, t) in enumerate(vals))
        mult += f'<div style="display:flex;flex-direction:column;gap:8px"><p style="margin:0;font-size:14px;font-weight:700">{r}</p><div style="display:flex;gap:6px;align-items:flex-end;height:180px">{barras}</div></div>'
    out.append(tarjeta(h2("Impresiones por red, mes a mes", "Cada red con su propia escala. Abajo de cada barra, la tasa de interacción.")
        + f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px">{mult}</div>'
        + nota("Cómo leerla", "La altura es el alcance (impresiones); el porcentaje es qué tanto reaccionó la gente.")))

    # Por formato
    ff = {}
    for p in pp:
        f = formato(p)
        if f: ff.setdefault((p["red"], f), []).append(p)
    orden = lambda k: (REDES.index(k[0]), k[1])
    filas = ""
    for k in sorted(fmts, key=orden):
        tu, ta = tasa(fmts[k]), tasa(ff[k]) if k in ff else None
        filas += (f'<tr style="border-top:1px solid #E6E3F0"><td style="padding:10px 8px 10px 0"><b style="color:{COL[k[0]]}">{k[0]}</b> · {e(k[1])}</td>'
                  f'<td style="padding:8px">{fp(ta)}</td><td style="padding:8px"><b>{fp(tu)}</b> {cambio(tu, ta, True) if ta is not None else ""}</td></tr>')
    out.append(tarjeta(h2("Por formato") + f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px"><thead><tr style="text-align:left;color:#5A5770"><th style="padding:8px 8px 8px 0">Red · formato</th><th style="padding:8px">Tasa {nomp[:3]}</th><th style="padding:8px">Tasa {e(M["titulo"][:3].lower())}</th></tr></thead><tbody>{filas}</tbody></table></div>'
        + f'<p style="margin:0;font-size:13px;color:#5A5770">— = ese formato no se usó en {nomp} en los mismos días. Tasa = interacciones ÷ impresiones. En LinkedIn el carrusel se sube como PDF.</p>'))

    # Top 3 y mucho alcance
    def card(k, p, buena):
        t = tasa([p]); bg, fg = ("#E3F6EE", "#0B5E41") if buena else ("#FDE8E6", "#9B1C14")
        return (f'<a href="{e(p["url"] or "#")}" target="_blank" style="display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:12px;align-items:center;padding:12px 14px;border:1px solid #E6E3F0;border-radius:12px;text-decoration:none;color:#1D1B2E">'
                f'<span style="font-size:20px;font-weight:700;color:#8A86A0">{k}</span><span style="display:flex;flex-direction:column;gap:4px;min-width:0"><span style="font-size:15px;font-weight:600">{e(nombre_pieza(p["tema"]))}</span>'
                f'<span style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:12px;color:#5A5770"><span style="background:{COL[p["red"]]};color:#FFFFFF;border-radius:999px;padding:1px 8px;font-weight:600">{p["red"]} · {e((formato(p) or "").lower())}</span>{fi(n(p["imp"]))} impresiones · {inter(p)} {"interacción" if inter(p) == 1 else "interacciones"}</span></span>'
                f'<span style="background:{bg};color:{fg};border-radius:8px;padding:6px 10px;font-size:18px;font-weight:700">{t:.1f} %</span></a>')
    con = [p for p in ps if n(p["imp"]) >= 100]
    top = sorted(con, key=lambda p: -tasa([p]))[:3]
    bajo = sorted([p for p in con if tasa([p]) < 1.5], key=lambda p: -n(p["imp"]))[:3]
    out.append(tarjeta(h2("Top 3 del mes", "Mejor tasa de interacción, con 100 impresiones o más. Toca una para abrirla.")
        + '<div style="display:flex;flex-direction:column;gap:8px">' + "".join(card(k + 1, p, True) for k, p in enumerate(top)) + '</div>'
        + (h2("Mucho alcance, poca interacción", "Las publicaciones con más impresiones y menos de 1.5 % de interacción.")
           + '<div style="display:flex;flex-direction:column;gap:8px">' + "".join(card(k + 1, p, False) for k, p in enumerate(bajo)) + '</div>' if bajo else "")))

    # Por pieza
    pz = {}
    for p in ps: pz.setdefault(p["tema"], []).append(p)
    mxp = max([suma(v)[1] for v in pz.values()] + [1]); filas = ""
    for t, v in sorted(pz.items(), key=lambda kv: (-suma(kv[1])[1], suma(kv[1])[0])):
        i, it = suma(v); f0 = min(p["fecha"] for p in v)
        rep = {r for r in REDES if sum(1 for p in v if p["red"] == r) > 1}
        links = " · ".join(f'<a href="{e(p["url"] or "#")}" target="_blank">{CORTA[p["red"]]} {e((formato(p) or "").lower())}{" (" + fecha(p["fecha"]) + ")" if p["red"] in rep else ""}</a>'
                           for p in sorted(v, key=lambda p: (REDES.index(p["red"]), p["fecha"])))
        filas += (f'<tr style="border-top:1px solid #E6E3F0"><td style="padding:10px 8px 10px 0"><b>{e(nombre_pieza(t))}</b><br><span style="font-size:12px;color:#5A5770">{fecha(f0)} · {links}</span></td>'
                  f'<td style="padding:8px;width:30%"><div style="display:flex;align-items:center;gap:8px"><div style="height:12px;width:{max(it / mxp * 100, 2):.0f}%;background:#6E3FD8;border-radius:6px"></div><b>{it}</b></div></td>'
                  f'<td style="padding:8px">{fi(i)}</td><td style="padding:8px">{chip_tasa(tasa(v))}</td></tr>')
    out.append(tarjeta(h2("Por pieza", f"Las {len(pz)} piezas orgánicas con datos al corte, sumando todas las redes donde salió cada una. Ordenadas por interacciones. Toca la red para abrir la publicación.")
        + f'<div style="overflow-x:auto"><table style="width:100%;min-width:720px;border-collapse:collapse;font-size:14px"><thead><tr style="text-align:left;color:#5A5770"><th style="padding:8px 8px 8px 0">Pieza</th><th style="padding:8px">Interacciones</th><th style="padding:8px">Impresiones</th><th style="padding:8px">Tasa de interacción<br><span style="font-size:12px;font-weight:400">interacciones ÷ impresiones</span></th></tr></thead><tbody>{filas}</tbody></table></div>'
        + nota("Qué es la tasa y sus colores", "Interacciones (likes + comentarios + compartidos) entre impresiones, sumando todas las redes de la pieza. Verde: 3.5 % o más. Gris: entre 1.5 % y 3.5 %. Rojo: menos de 1.5 %. Las historias no se cuentan como pieza.")))

    # Orgánico vs BOFU
    out.append(tarjeta('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px">'
        + f'<div style="display:flex;flex-direction:column;gap:8px"><h2 style="margin:0;font-size:20px;font-weight:700">Orgánico</h2><p style="margin:0;font-size:15px;line-height:1.5">{org} piezas únicas. Da alcance y reconocimiento: {fi(I)} impresiones.</p></div>'
        + f'<div style="display:flex;flex-direction:column;gap:8px"><h2 style="margin:0;font-size:20px;font-weight:700">Anuncios BOFU</h2><p style="margin:0;font-size:15px;line-height:1.5">{bofu} {e(O.get("bofu_txt", {}).get(clave, "anuncios BOFU"))}. Los anuncios trajeron {leads_ad} de los {leads} leads del mes.</p></div></div>'))

    # Parrilla
    if "repetir" in R:
        caja = lambda t, c, x: f'<div style="background:#FFFFFF;border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:6px"><p style="margin:0;font-size:13px;font-weight:600;color:{c}">{t}</p><p style="margin:0;font-size:15px;line-height:1.5">{x}</p></div>'
        out.append('<section style="background:#EFE8FF;border-radius:20px;padding:26px 30px;display:flex;flex-direction:column;gap:14px">'
                   + '<h2 style="margin:0;font-size:22px;font-weight:700">Para la parrilla del siguiente mes</h2>'
                   + '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px">'
                   + caja("Repetir", "#0B5E41", R["repetir"]) + caja("Ajustar", "#6E3FD8", R["ajustar"]) + caja("Probar", "#9B1C14", R["probar"]) + '</div></section>')
    return envolver("".join(out))

# ---------------------------------------------------------------- reporte semanal
def semanal(a, b, pa, pb, corte):
    ps = sin_hist([p for p in d.P if a <= p["fecha"] <= b]); pp = sin_hist([p for p in d.P if pa <= p["fecha"] <= pb])
    I, T = suma(ps); IP, TP = suma(pp); er, erp = tasa(ps), tasa(pp)
    temas = sorted({p["tema"] for p in ps}, key=lambda t: pieza(t)[0] or t)
    pfb = [p for p in ps if p["red"] != "Facebook"]; ppfb = [p for p in pp if p["red"] != "Facebook"]
    out = [LEYENDA]
    out.append('<section style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">'
        + kpi(str(len(temas)), "piezas nuevas", e(", ".join(pieza(t)[0] or d.TEMAS.get(t, (t,))[0] for t in temas)))
        + kpi(fi(I), "impresiones", f"semana anterior: {fi(IP)}", cambio(I, IP))
        + kpi(fi(T), "interacciones", f"semana anterior: {fi(TP)}", cambio(T, TP))
        + kpi(fp(er), "tasa de interacción", f"semana anterior: {fp(erp)}", cambio(er, erp, True)) + '</section>')
    out.append(nota("Comparación sin Facebook", f"Los reels de Facebook pueden subir mucho las impresiones con poca interacción. Sin Facebook en las dos semanas: {fi(suma(pfb)[0])} impresiones y {fp(tasa(pfb))} esta semana contra {fi(suma(ppfb)[0])} y {fp(tasa(ppfb))} la anterior. Lo más reciente lleva menos días acumulando."))
    nets = ""
    for r in REDES:
        q = [p for p in ps if p["red"] == r]; qp = [p for p in pp if p["red"] == r]
        i, t = suma(q); tr, tp = tasa(q), tasa(qp)
        nets += (f'<div style="border:1px solid #E6E3F0;border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px;border-top:5px solid {COL[r]}">'
                 f'<p style="margin:0;font-size:15px;font-weight:700">{r}</p><p style="margin:0;font-size:13px;color:#5A5770">{fi(i)} impresiones · {t} interacciones</p>'
                 f'<p style="margin:0;font-size:14px">{chip_tasa(tr)} <span style="font-size:12px;color:#5A5770">antes {fp(tp)}</span></p>{cambio(tr, tp, True)}</div>')
    out.append(tarjeta(h2("Por red") + f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px">{nets}</div>'))
    cards = ""
    pz = {}
    for p in ps: pz.setdefault(p["tema"], []).append(p)
    COLS = "150px minmax(0,1fr) 90px 80px"
    for t, v in sorted(pz.items(), key=lambda kv: -suma(kv[1])[1]):
        i, it = suma(v); mx = max([inter(p) for p in v] + [1]); fs = sorted({p["fecha"] for p in v})
        rows = "".join(
            f'<a href="{e(p["url"] or "#")}" target="_blank" style="display:grid;grid-template-columns:{COLS};gap:12px;align-items:center;padding:8px 10px;border-radius:10px;text-decoration:none;color:#1D1B2E;background:#FAF9FD">'
            f'<span style="display:flex;flex-direction:column"><b style="font-size:14px;color:{COL[p["red"]]}">{p["red"]}</b><span style="font-size:12px;color:#5A5770">{e(formato(p) or "")}{" · " + fecha(p["fecha"]) if sum(1 for q in v if q["red"] == p["red"]) > 1 else ""}</span></span>'
            f'<span style="display:flex;align-items:center;gap:8px"><span style="height:12px;width:{max(inter(p) / mx * 100, 2):.0f}%;background:{COL[p["red"]]};border-radius:6px"></span><b style="font-size:14px">{inter(p)}</b></span>'
            f'<span style="font-size:13px;color:#5A5770">{fi(n(p["imp"]))} imp.</span>{chip_tasa(tasa([p])) if n(p["imp"]) else "sin datos"}</a>'
            for p in sorted(v, key=lambda p: (REDES.index(p["red"]), p["fecha"])))
        nt = NOTA_PIEZA.get((a, t), "")
        cards += tarjeta(
            f'<div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:baseline"><div><p style="margin:0;font-size:17px;font-weight:700">{e(nombre_pieza(t))}</p><p style="margin:2px 0 0;font-size:13px;color:#5A5770">{fecha(fs[0])}{" al " + fecha(fs[-1]) if len(fs) > 1 else ""}</p></div>'
            f'<p style="margin:0;font-size:14px;color:#5A5770">Total: <b style="color:#1D1B2E">{it} interacciones</b> · {fi(i)} impresiones · {chip_tasa(tasa(v))}</p></div>'
            f'<div style="display:grid;grid-template-columns:{COLS};gap:12px;padding:0 10px;font-size:12px;color:#5A5770"><span>Red</span><span>Interacciones</span><span>Impresiones</span><span>Tasa</span></div>'
            f'<div style="display:flex;flex-direction:column;gap:6px">{rows}</div>'
            + (f'<p style="margin:0;font-size:14px;color:#5A5770">{e(nt)}</p>' if nt else ""), "padding:22px 26px;gap:12px")
    out.append('<section style="display:flex;flex-direction:column;gap:14px">' + h2("Cada pieza, red por red", "Ordenadas por interacciones. La barra compara las redes dentro de la misma pieza. Toca una red para abrir la publicación.") + cards + '</section>')
    return envolver("".join(out))
