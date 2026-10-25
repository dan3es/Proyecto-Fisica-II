"""Interpreta una pregunta escrita en lenguaje natural y la resuelve con los módulos de cálculo."""
import re

import descriptiva
import experimental
import tablas
from interpretacion import comparar_desviaciones
from probabilidad import resolver_normal, resolver_probabilidad_basica
from regresion import calcular_regresion

NUM = r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
SERIE = rf"{NUM}(?:(?:\s*[,;]\s*|\s+y\s+|\s+){NUM})*"

EJEMPLOS_TEXTO = [
    "Con mediciones de corriente (A): 2.1, 2.3, 2.2, 2.4 y 2.0; calcula media, "
    "desviación estándar muestral e interpreta.",
    "Calcula el error de la media de estas mediciones (s): 1.42, 1.45, 1.40, 1.44, 1.43",
    "Tabla de frecuencias e histograma de: 4.8, 5.1, 5.0, 4.9, 5.3, 5.2, 4.7, 5.0, 5.1, 4.9",
    "La nota sigue una distribución normal con media 70 y desviación estándar 10. Calcula P(X < 85).",
    "Correlación y regresión lineal con x = 1, 2, 3, 4, 5 e y = 2, 4, 5, 4, 5",
    "Si P(A) = 0.5, P(B) = 0.3 y P(A ∩ B) = 0.1, calcula la probabilidad de la unión.",
    "Diferencia entre desviación poblacional y muestral de: 2.1, 2.3, 2.2, 2.4, 2.0",
]

AYUDA_GENERAL = (
    "No entendí la pregunta. Indica qué quieres calcular (media, desviación, tabla de frecuencias, "
    "distribución normal, correlación…) y escribe tus datos con punto decimal, por ejemplo: "
    "«media y desviación estándar de 2.1, 2.3, 2.2». También puedes usar las demás pestañas."
)


class NoEntendido(ValueError):
    """La frase no se pudo convertir en un problema que la app sepa resolver."""


def _normalizar(texto):
    t = texto.lower().translate(str.maketrans("áéíóúü", "aeiouu"))
    for origen, destino in {"≤": "<", "≥": ">", "−": "-", "–": "-", "σ": " sigma ", "μ": " mu ",
                            "∪": " union ", "∩": " interseccion ", "²": ""}.items():
        t = t.replace(origen, destino)
    return t


def _numero(texto):
    return float(texto)


def _unidad(texto):
    """Primera unidad escrita entre paréntesis, como (A) o (°C). Ignora P(A), P(B)..."""
    m = re.search(r"(?<![pP])\(\s*([^\d()\s][^()\d]{0,5}?)\s*\)", texto)
    return m.group(1).strip() if m else ""


def _datos(t):
    """La serie de números más larga del texto."""
    series = [re.findall(NUM, m.group(0)) for m in re.finditer(SERIE, t)]
    mejor = max(series, key=len, default=[])
    if len(mejor) < 2:
        raise NoEntendido(
            "No encontré datos suficientes. Escribe al menos 2 números separados por coma, "
            "con punto decimal (por ejemplo: 2.1, 2.3, 2.2)."
        )
    return [_numero(x) for x in mejor]


def _sobrantes(t, datos, k=None):
    """Texto de aviso con los números de la frase que no entraron en la serie de datos."""
    restantes = [_numero(x) for x in re.findall(NUM, t)]
    for x in datos + ([float(k)] if k else []):
        if x in restantes:
            restantes.remove(x)
    if not restantes:
        return ""
    return " Ojo: no usé estos números: " + ", ".join(f"{x:g}" for x in restantes) + "."


def _resumen_datos(datos):
    vista = ", ".join(f"{x:g}" for x in datos[:10]) + (", …" if len(datos) > 10 else "")
    return f"{len(datos)} datos ({vista})"


def _series_xy(t, original):
    marcas = list(re.finditer(r"(?<![a-z])([xy])\s*(?:\(([^)]*)\))?\s*[=:]\s*", t))
    x = next((m for m in marcas if m.group(1) == "x"), None)
    y = next((m for m in marcas if m.group(1) == "y"), None)
    if x is None or y is None:
        raise NoEntendido(
            "Para correlación o regresión escribe las dos series así: x = 1, 2, 3 e y = 2, 4, 5."
        )
    primero, segundo = sorted([x, y], key=lambda m: m.start())
    seg1 = t[primero.end():segundo.start()]
    seg2 = t[segundo.end():]
    series = {primero.group(1): re.findall(NUM, seg1), segundo.group(1): re.findall(NUM, seg2)}
    unidades = {m.group(1): (m.group(2) or "").strip() for m in (x, y)}
    return ([_numero(v) for v in series["x"]], [_numero(v) for v in series["y"]],
            unidades["x"], unidades["y"])


def _parametros_normal(t):
    mu = re.search(rf"(?:\bmu\b|media(?: poblacional)?)\s*(?:=|:|de|es|igual a)?\s*({NUM})", t)
    sigma = re.search(
        rf"(?:sigma|desviaci[oó]n(?: est[aá]ndar| t[ií]pica)?)\s*(?:=|:|de|es|igual a)?\s*({NUM})", t)
    if not mu or not sigma:
        raise NoEntendido(
            "Para la distribución normal indica la media y la desviación estándar, "
            "por ejemplo: «media 70 y desviación estándar 10»."
        )
    entre = (re.search(rf"p\(\s*({NUM})\s*<\s*x\s*<\s*({NUM})\s*\)", t)
             or re.search(rf"entre\s+({NUM})\s+y\s+({NUM})", t))
    mayor = (re.search(rf"p\(\s*x\s*>\s*({NUM})", t)
             or re.search(rf"(?:m[aá]s de|mayor(?:es)? (?:que|a|de)|supere|supera|exceda|excede|"
                          rf"por encima de|superior a)\s+({NUM})", t))
    menor = (re.search(rf"p\(\s*x\s*<\s*({NUM})", t)
             or re.search(rf"(?:menos de|menor(?:es)? (?:que|a|de)|inferior a|por debajo de)\s+({NUM})", t))
    args = {"mu": _numero(mu.group(1)), "sigma": _numero(sigma.group(1))}
    if entre:
        args.update(tipo="entre", a=_numero(entre.group(1)), b=_numero(entre.group(2)))
    elif mayor:
        args.update(tipo="mayor", a=_numero(mayor.group(1)))
    elif menor:
        args.update(tipo="menor", a=_numero(menor.group(1)))
    else:
        raise NoEntendido(
            "Indica qué probabilidad calcular: P(X < 85), P(X > 85) o P(95 < X < 110)."
        )
    return args


def _valor_p(t, patron):
    m = re.search(patron + rf"\s*(?:=|:|es|vale)?\s*({NUM})", t)
    return _numero(m.group(1)) if m else None


def _parametros_basica(t):
    pa = _valor_p(t, r"p\(\s*a\s*\)")
    pb = _valor_p(t, r"p\(\s*b\s*\)")
    pab = _valor_p(t, r"p\(\s*a\s*(?:interseccion|y|and)\s*b\s*\)")
    if "condicional" in t or re.search(r"p\(\s*a\s*\|\s*b\s*\)", t) or "dado que" in t:
        return {"tipo": "condicional", "pAyB": pab, "pB": pb}
    if "independiente" in t:
        return {"tipo": "independientes", "pA": pa, "pB": pb}
    if "union" in t or re.search(r"p\(\s*a\s*u\s*b\s*\)", t):
        return {"tipo": "union", "pA": pa, "pB": pb, "pAyB": pab}
    if "complemento" in t or "no ocurra" in t:
        return {"tipo": "complemento", "pA": pa}
    fav = re.search(rf"favorables?\s*[=:]?\s*({NUM})", t) or re.search(rf"({NUM})\s*(?:casos\s*)?favorables?", t)
    tot = re.search(rf"totales?\s*[=:]?\s*({NUM})", t) or re.search(rf"({NUM})\s*(?:casos\s*)?totales?", t)
    if fav and tot:
        return {"tipo": "clasica", "favorables": _numero(fav.group(1)), "total": _numero(tot.group(1))}
    raise NoEntendido(
        "Para probabilidad básica indica P(A), P(B) y el tipo (unión, independientes, condicional, "
        "complemento) o los casos favorables y totales."
    )


def interpretar(texto):
    """Devuelve {"modulo", "args", "entendido"} o lanza NoEntendido."""
    if not texto or not texto.strip():
        raise NoEntendido("Escribe una pregunta o tus datos.")
    t = _normalizar(texto)
    unidad = _unidad(texto)
    u = f", unidad {unidad}" if unidad else ""

    # 1) Distribución normal
    if ("normal" in t or re.search(rf"p\(\s*(?:x|{NUM}\s*<\s*x)", t)
            or (re.search(r"\bmu\b", t) and "sigma" in t)):
        args = _parametros_normal(t)
        if args["tipo"] == "entre":
            prob = f"P({args['a']:g} < X < {args['b']:g})"
        else:
            prob = f"P(X {'<' if args['tipo'] == 'menor' else '>'} {args['a']:g})"
        if unidad:
            args["unidad"] = unidad
        return {"modulo": "normal", "args": args,
                "entendido": f"Distribución normal con μ = {args['mu']:g}, σ = {args['sigma']:g}; calcular {prob}."}

    # 2) Probabilidad básica
    if re.search(r"p\(\s*[ab]\s*[)|]", t) or "favorable" in t:
        args = _parametros_basica(t)
        return {"modulo": "probabilidad", "args": args,
                "entendido": f"Probabilidad básica, tipo «{args['tipo']}»."}

    # 3) Correlación y regresión
    if any(p in t for p in ("correlaci", "regresi", "recta", "dispersi", "pendiente")):
        x, y, ux, uy = _series_xy(t, texto)
        return {"modulo": "regresion",
                "args": {"x": x, "y": y, "unidad_x": ux, "unidad_y": uy},
                "entendido": f"Correlación y regresión lineal con {len(x)} datos en x y {len(y)} en y."}

    # 4) Tabla de frecuencias / histograma
    if any(p in t for p in ("frecuencia", "histograma", "tabla")):
        datos = _datos(t)
        k = re.search(r"(\d+)\s*clases", t)
        args = {"datos": datos}
        if k:
            args["k"] = int(k.group(1))
        return {"modulo": "tablas", "args": args,
                "entendido": f"Tabla de frecuencias e histograma de {_resumen_datos(datos)}."
                + _sobrantes(t, datos, args.get("k"))}

    claves_estadistica = ("media", "promedio", "mediana", "moda", "rango", "varianza",
                          "desviaci", "estad", "error", "incertidumbre", "calcula")
    if not any(p in t for p in claves_estadistica):
        raise NoEntendido(AYUDA_GENERAL)
    datos = _datos(t)

    # 5) Desviación poblacional vs. muestral
    if ("poblacional" in t and "muestral" in t) or "diferencia" in t:
        return {"modulo": "interpretacion", "args": {"datos": datos, "unidad": unidad},
                "entendido": f"Comparar desviación poblacional y muestral de {_resumen_datos(datos)}{u}."
                + _sobrantes(t, datos)}

    # 6) Datos experimentales (error de la media)
    if "error" in t or "incertidumbre" in t:
        return {"modulo": "experimental", "args": {"datos": datos, "unidad": unidad},
                "entendido": f"Datos experimentales con {_resumen_datos(datos)}{u}: media ± error de la media."
                + _sobrantes(t, datos)}

    # 7) Estadística descriptiva
    poblacional = "poblacional" in t and "muestral" not in t
    tipo = "poblacional" if poblacional else "muestral"
    return {"modulo": "descriptiva",
            "args": {"datos": datos, "poblacional": poblacional, "unidad": unidad},
            "entendido": f"Estadística descriptiva con {_resumen_datos(datos)}{u}; desviación {tipo}."
                + _sobrantes(t, datos)}


def ejecutar(plan):
    """Llama al módulo de cálculo. Devuelve (formato, resultado)."""
    modulo, args = plan["modulo"], dict(plan["args"])
    if modulo == "normal":
        return "diccionario", resolver_normal(**args)
    if modulo == "probabilidad":
        return "diccionario", resolver_probabilidad_basica(**args)
    if modulo == "regresion":
        return "diccionario", calcular_regresion(**args)
    if modulo == "interpretacion":
        return "diccionario", comparar_desviaciones(**args)
    if modulo == "descriptiva":
        return "pasos", descriptiva.analizar(**args)
    if modulo == "experimental":
        return "pasos", experimental.analizar_exp(**args)
    df, info = tablas.tabla_frecuencias(args["datos"], args.get("k"))
    return "tabla", (df, info, args["datos"])


def mostrar():
    import streamlit as st
    from ayudas import mostrar_resultado, mostrar_pasos

    st.markdown("Escribe tu pregunta o tus datos y el asistente la resolverá paso a paso.")
    with st.expander("¿Qué puedo escribir? (ejemplos)"):
        for ejemplo in EJEMPLOS_TEXTO:
            st.markdown("- " + ejemplo)
    texto = st.text_area("Pregunta o problema", value=EJEMPLOS_TEXTO[0], height=120, key="q_texto")
    if not st.button("Resolver", key="b_pregunta"):
        return
    try:
        plan = interpretar(texto)
    except NoEntendido as e:
        st.warning(str(e))
        return
    st.info("Entendí: " + plan["entendido"])
    try:
        formato, res = ejecutar(plan)
    except ValueError as e:
        st.error(str(e))
        return
    if formato == "diccionario":
        mostrar_resultado(res)
    elif formato == "pasos":
        mostrar_pasos(res)
    else:
        df, info, datos = res
        for linea in info["pasos"]:
            st.write("• " + linea)
        st.dataframe(df, hide_index=True)
        st.pyplot(tablas.histograma(datos, info["bordes"]))
