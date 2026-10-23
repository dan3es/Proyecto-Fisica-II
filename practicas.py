"""Ejemplos resueltos y generador de prácticas con retroalimentación."""
import importlib
import random

from probabilidad import resolver_normal, resolver_probabilidad_basica, phi
from regresion import calcular_regresion
from interpretacion import comparar_desviaciones, calcular_media_desviaciones

FUNCIONES_MODULOS = {
    "descriptiva": ("descriptiva", "analizar"),
    "experimental": ("experimental", "analizar_exp"),
    "tablas": ("tablas", "tabla_frecuencias"),
}

EJEMPLOS = [
    {
        "id": 1, "modulo": "descriptiva",
        "enunciado": "Mediciones de corriente (A): 2.1, 2.3, 2.2, 2.4 y 2.0. "
                     "Calcula la media, la desviación estándar muestral e interpreta.",
        "datos": {"datos": [2.1, 2.3, 2.2, 2.4, 2.0], "unidad": "A"},
    },
    {
        "id": 2, "modulo": "descriptiva",
        "enunciado": "Edades de un grupo (años): 12, 15, 11, 15, 18, 20, 15, 13. "
                     "Calcula media, mediana, moda, rango y desviación estándar.",
        "datos": {"datos": [12, 15, 11, 15, 18, 20, 15, 13], "unidad": "años"},
    },
    {
        "id": 3, "modulo": "experimental",
        "enunciado": "Periodo de un péndulo (s): 1.42, 1.45, 1.40, 1.44, 1.43, 1.41. "
                     "Expresa el resultado como media ± error de la media.",
        "datos": {"datos": [1.42, 1.45, 1.40, 1.44, 1.43, 1.41], "unidad": "s"},
    },
    {
        "id": 4, "modulo": "tablas",
        "enunciado": "Voltajes medidos (V): 4.8, 5.1, 5.0, 4.9, 5.3, 5.2, 4.7, 5.0, 5.1, "
                     "4.9, 5.4, 5.0, 4.8, 5.2, 5.1. Construye la tabla de frecuencias y el histograma.",
        "datos": {"datos": [4.8, 5.1, 5.0, 4.9, 5.3, 5.2, 4.7, 5.0, 5.1, 4.9, 5.4, 5.0, 4.8, 5.2, 5.1]},
    },
    {
        "id": 5, "modulo": "normal",
        "enunciado": "Las notas de un examen siguen una normal con μ = 70 y σ = 10. "
                     "Calcula la probabilidad de que un estudiante obtenga menos de 85.",
        "datos": {"mu": 70, "sigma": 10, "tipo": "menor", "a": 85},
    },
    {
        "id": 6, "modulo": "normal",
        "enunciado": "La resistencia de ciertos resistores sigue una normal con μ = 100 Ω y σ = 5 Ω. "
                     "Calcula P(95 < X < 110).",
        "datos": {"mu": 100, "sigma": 5, "tipo": "entre", "a": 95, "b": 110, "unidad": "Ω"},
    },
    {
        "id": 7, "modulo": "normal",
        "enunciado": "La vida útil de una batería sigue una normal con μ = 1200 h y σ = 100 h. "
                     "Calcula la probabilidad de que dure más de 1350 h.",
        "datos": {"mu": 1200, "sigma": 100, "tipo": "mayor", "a": 1350, "unidad": "h"},
    },
    {
        "id": 8, "modulo": "probabilidad",
        "enunciado": "Si P(A) = 0.5, P(B) = 0.3 y P(A ∩ B) = 0.1, calcula P(A ∪ B).",
        "datos": {"tipo": "union", "pA": 0.5, "pB": 0.3, "pAyB": 0.1},
    },
    {
        "id": 9, "modulo": "regresion",
        "enunciado": "Ley de Hooke: masa colgada (kg) = 0.1, 0.2, 0.3, 0.4, 0.5 y alargamiento "
                     "del resorte (cm) = 2.1, 4.0, 6.2, 7.9, 10.1. Calcula la recta de regresión y r.",
        "datos": {"x": [0.1, 0.2, 0.3, 0.4, 0.5], "y": [2.1, 4.0, 6.2, 7.9, 10.1],
                  "unidad_x": "kg", "unidad_y": "cm", "x_pred": 0.35},
    },
    {
        "id": 10, "modulo": "regresion",
        "enunciado": "Temperatura (°C) = 20, 30, 40, 50, 60 y resistencia de un alambre (Ω) = "
                     "100.0, 103.9, 108.1, 111.8, 116.2. Calcula r e interpreta.",
        "datos": {"x": [20, 30, 40, 50, 60], "y": [100.0, 103.9, 108.1, 111.8, 116.2],
                  "unidad_x": "°C", "unidad_y": "Ω"},
    },
    {
        "id": 11, "modulo": "interpretacion",
        "enunciado": "Con las mediciones de corriente 2.1, 2.3, 2.2, 2.4 y 2.0 A, "
                     "compara la desviación estándar poblacional con la muestral.",
        "datos": {"datos": [2.1, 2.3, 2.2, 2.4, 2.0], "unidad": "A"},
    },
]


def resolver_ejemplo(ejemplo):
    """Resuelve un ejemplo o una práctica llamando al módulo que corresponde."""
    modulo = ejemplo["modulo"]
    datos = ejemplo["datos"]
    if modulo == "normal":
        return resolver_normal(**datos)
    if modulo == "probabilidad":
        return resolver_probabilidad_basica(**datos)
    if modulo == "regresion":
        return calcular_regresion(**datos)
    if modulo == "interpretacion":
        return comparar_desviaciones(**datos)
    if modulo in FUNCIONES_MODULOS:
        archivo, nombre = FUNCIONES_MODULOS[modulo]
        try:
            funcion = getattr(importlib.import_module(archivo), nombre)
        except (ImportError, AttributeError):
            raise ValueError(
                f"El módulo '{archivo}' o su función '{nombre}' todavía no está disponible."
            )
        return funcion(**datos)
    raise ValueError(f"Módulo desconocido: {modulo}")


TIPOS_PRACTICA = {
    "media_desviacion": "Media y desviación estándar muestral",
    "normal": "Probabilidad con distribución normal",
    "correlacion": "Correlación y regresión lineal",
}

_CONTEXTOS_MEDICION = [
    ("la longitud de una varilla", "cm", 50.0, 6.0),
    ("la masa de una muestra", "g", 200.0, 20.0),
    ("el tiempo de recorrido de un carrito", "s", 12.0, 3.5),
    ("la temperatura de un líquido", "°C", 25.0, 5.0),
]

_CONTEXTOS_NORMAL = [
    ("la resistencia de un lote de resistores", "Ω", 100.0, 5.0),
    ("la vida útil de una batería", "h", 500.0, 40.0),
    ("la rapidez de un móvil", "m/s", 20.0, 2.5),
    ("la masa de piezas fabricadas", "g", 250.0, 8.0),
]

_CONTEXTOS_REGRESION = [
    ("la masa colgada", "kg", "el alargamiento del resorte", "cm", 20.0),
    ("la temperatura", "°C", "la resistencia del alambre", "Ω", 0.4),
    ("el tiempo", "s", "la distancia recorrida", "m", 3.0),
]


def generar_practica(tipo=None, semilla=None):
    """Crea un ejercicio nuevo. tipo: una clave de TIPOS_PRACTICA (o None = al azar)."""
    rng = random.Random(semilla)
    if tipo is None:
        tipo = rng.choice(list(TIPOS_PRACTICA))
    if tipo not in TIPOS_PRACTICA:
        raise ValueError(f"Tipo de práctica no reconocido: {tipo}")

    if tipo == "media_desviacion":
        return _practica_media_desviacion(rng)
    if tipo == "normal":
        return _practica_normal(rng)
    return _practica_correlacion(rng)


def _practica_media_desviacion(rng):
    que, unidad, centro, amplitud = rng.choice(_CONTEXTOS_MEDICION)
    for _ in range(100):
        n = rng.randint(5, 8)
        datos = [round(centro + rng.uniform(-amplitud, amplitud), 1) for _ in range(n)]
        c = calcular_media_desviaciones(datos)
        if c["s"] >= 0.8:
            break
    lista = ", ".join(str(x) for x in datos)
    return {
        "tipo": "media_desviacion",
        "modulo": "interpretacion",
        "datos": {"datos": datos, "unidad": unidad},
        "enunciado": f"Se midió {que} ({unidad}) y se obtuvo: {lista}. "
                     "Calcula la media y la desviación estándar muestral.",
        "preguntas": [
            {"clave": "media", "texto": f"Media (en {unidad}, 2 decimales)", "tol": 0.01},
            {"clave": "s", "texto": f"Desviación estándar muestral s (en {unidad}, 2 decimales)", "tol": 0.01},
        ],
        "respuestas_correctas": {"media": c["media"], "s": c["s"]},
        "pistas": {
            "media": [(sum(datos), "Ese valor parece la suma de los datos; falta dividir entre n.")],
            "s": [(c["sigma"], "Parece que dividiste entre n. La desviación muestral divide entre (n − 1)."),
                  (c["sc"] / (c["n"] - 1), "Esa es la varianza (s²); falta sacar la raíz cuadrada."),
                  (c["sc"], "Ese valor es la suma de cuadrados; falta dividir entre (n − 1) y sacar la raíz.")],
        },
    }


def _practica_normal(rng):
    que, unidad, mu, sigma = rng.choice(_CONTEXTOS_NORMAL)
    k = rng.choice([-1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.0])
    a = round(mu + k * sigma, 2)
    tipo_prob = rng.choice(["menor", "mayor"])
    z = (a - mu) / sigma
    p = phi(z) if tipo_prob == "menor" else 1 - phi(z)
    signo = "<" if tipo_prob == "menor" else ">"
    return {
        "tipo": "normal",
        "modulo": "normal",
        "datos": {"mu": mu, "sigma": sigma, "tipo": tipo_prob, "a": a, "unidad": unidad},
        "enunciado": f"{que.capitalize()} sigue una distribución normal con μ = {mu:g} {unidad} "
                     f"y σ = {sigma:g} {unidad}. Calcula P(X {signo} {a:g}).",
        "preguntas": [
            {"clave": "z", "texto": "Valor de z (2 decimales)", "tol": 0.011},
            {"clave": "p", "texto": "Probabilidad (3 decimales, entre 0 y 1)", "tol": 0.002},
        ],
        "respuestas_correctas": {"z": z, "p": p},
        "pistas": {
            "z": [(-z, "Revisa el signo: z = (x − μ)/σ, con x menos la media.")],
            "p": [(1 - p, "Parece que calculaste la cola contraria; revisa si piden P(X < a) o P(X > a)."),
                  (z, "Ese valor es z; falta convertirlo en probabilidad con la tabla normal Φ(z).")],
        },
    }


def _practica_correlacion(rng):
    nx, ux, ny, uy, pend = rng.choice(_CONTEXTOS_REGRESION)
    n = rng.randint(5, 6)
    for _ in range(100):
        x = [float(i) for i in range(1, n + 1)]
        y = [round(rng.uniform(-1, 1) * pend + pend * xi + 2, 1) for xi in x]
        if len(set(y)) > 1:
            break
    res = calcular_regresion(x, y)
    r, b = res["valores"]["r"], res["valores"]["b"]
    xs = ", ".join(f"{v:g}" for v in x)
    ys = ", ".join(f"{v:g}" for v in y)
    return {
        "tipo": "correlacion",
        "modulo": "regresion",
        "datos": {"x": x, "y": y, "unidad_x": ux, "unidad_y": uy},
        "enunciado": f"Se midió {nx} (x, en {ux}): {xs}; y {ny} (y, en {uy}): {ys}. "
                     "Calcula el coeficiente de correlación r y la pendiente b de la recta de regresión.",
        "preguntas": [
            {"clave": "r", "texto": "Coeficiente de correlación r (3 decimales)", "tol": 0.006},
            {"clave": "b", "texto": f"Pendiente b (en {uy}/{ux}, 2 decimales)", "tol": 0.011},
        ],
        "respuestas_correctas": {"r": r, "b": b},
        "pistas": {
            "r": [(-r, "Revisa el signo de r: debe coincidir con el signo de la pendiente."),
                  (r ** 2, "Ese valor parece r²; para r falta sacar la raíz cuadrada (con el signo de b).")],
            "b": [(r, "Ese valor es r, no la pendiente. b = [nΣxy − ΣxΣy] / [nΣx² − (Σx)²].")],
        },
    }


def _a_numero(valor):
    """Convierte lo que escribió el estudiante a float (acepta coma decimal). None si no es número."""
    if valor is None:
        return None
    try:
        return float(str(valor).strip().replace(",", "."))
    except ValueError:
        return None


def evaluar_respuesta(practica, respuestas):
    """Compara las respuestas del estudiante con las correctas y da retroalimentación."""
    detalle = []
    puntaje = 0
    for pregunta in practica["preguntas"]:
        clave = pregunta["clave"]
        correcto = practica["respuestas_correctas"][clave]
        tol = pregunta["tol"]
        usuario = _a_numero(respuestas.get(clave))

        if usuario is None:
            ok = False
            mensaje = "Escribe un número (usa punto o coma decimal)."
        elif abs(usuario - correcto) <= tol:
            ok = True
            mensaje = "¡Correcto!"
            puntaje += 1
        else:
            ok = False
            mensaje = "No coincide. Revisa el procedimiento y vuelve a intentarlo."
            for valor_alt, pista in practica["pistas"].get(clave, []):
                if abs(usuario - valor_alt) <= tol:
                    mensaje = pista
                    break
        detalle.append({"clave": clave, "texto": pregunta["texto"],
                        "correcto": ok, "mensaje": mensaje})
    return {"puntaje": puntaje, "total": len(practica["preguntas"]), "detalle": detalle}


def resolver_practica(practica):
    """Solución completa (fórmula, sustitución, pasos...) de una práctica generada."""
    return resolver_ejemplo(practica)


def _mostrar_ejemplo(ej):
    """Resuelve un ejemplo y lo muestra con el formato que corresponda a su módulo."""
    import streamlit as st
    from ayudas import mostrar_resultado, mostrar_pasos

    res = resolver_ejemplo(ej)
    if ej["modulo"] in ("descriptiva", "experimental"):
        mostrar_pasos(res)
    elif ej["modulo"] == "tablas":
        import tablas
        df, info = res
        for linea in info["pasos"]:
            st.write("• " + linea)
        st.dataframe(df, hide_index=True)
        st.pyplot(tablas.histograma(ej["datos"]["datos"], info["bordes"]))
    else:
        mostrar_resultado(res)


def mostrar():
    import streamlit as st
    from ayudas import mostrar_resultado

    modo = st.radio("¿Qué quieres hacer?",
                    ["Ver ejemplos resueltos", "Generar una práctica"],
                    horizontal=True, key="pr_modo")

    if modo == "Ver ejemplos resueltos":
        opciones = {f"Ejemplo {e['id']} ({e['modulo']})": e for e in EJEMPLOS}
        nombre = st.selectbox("Elige un ejemplo", list(opciones), key="pr_ejemplo")
        ej = opciones[nombre]
        st.markdown("**Enunciado:** " + ej["enunciado"])
        if st.button("Resolver paso a paso", key="b_ejemplo"):
            try:
                _mostrar_ejemplo(ej)
            except ValueError as e:
                st.error(str(e))
        return

    tipos = {nombre: clave for clave, nombre in TIPOS_PRACTICA.items()}
    elegido = st.selectbox("Tipo de práctica", list(tipos), key="pr_tipo")
    if st.button("🎲 Generar nueva práctica", key="b_generar"):
        st.session_state["practica"] = generar_practica(tipos[elegido])
        st.session_state["practica_n"] = st.session_state.get("practica_n", 0) + 1
        st.session_state.pop("practica_eval", None)

    practica = st.session_state.get("practica")
    if practica is None:
        st.info("Pulsa «Generar nueva práctica» para recibir un ejercicio con datos nuevos.")
        return

    n = st.session_state.get("practica_n", 0)
    st.markdown("**Ejercicio:** " + practica["enunciado"])
    respuestas = {}
    for pregunta in practica["preguntas"]:
        respuestas[pregunta["clave"]] = st.text_input(
            pregunta["texto"], key=f"resp_{n}_{pregunta['clave']}")

    if st.button("Revisar mis respuestas", key="b_revisar"):
        st.session_state["practica_eval"] = evaluar_respuesta(practica, respuestas)

    evaluacion = st.session_state.get("practica_eval")
    if evaluacion:
        st.markdown(f"**Puntaje: {evaluacion['puntaje']} de {evaluacion['total']}**")
        for d in evaluacion["detalle"]:
            if d["correcto"]:
                st.success(f"{d['texto']}: {d['mensaje']}")
            else:
                st.error(f"{d['texto']}: {d['mensaje']}")
        with st.expander("Ver la solución paso a paso"):
            try:
                mostrar_resultado(resolver_practica(practica))
            except ValueError as e:
                st.error(str(e))
