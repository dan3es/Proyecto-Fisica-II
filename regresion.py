"""Correlación y regresión lineal simple."""
import math

import numpy as np
from matplotlib.figure import Figure

from ayudas import fmt, num, numero, lista_de_numeros


def _ecuacion(a, b):
    signo = "+" if b >= 0 else "−"
    return f"ŷ = {fmt(a)} {signo} {fmt(abs(b))}·x"


def _fuerza(r):
    r = abs(r)
    if r >= 0.9:
        return "muy fuerte"
    if r >= 0.7:
        return "fuerte"
    if r >= 0.4:
        return "moderada"
    if r >= 0.2:
        return "débil"
    return "muy débil o nula"


def _grafica(x, y, a, b, unidad_x, unidad_y, x_pred, y_pred):
    fig = Figure(figsize=(7, 4))
    ax = fig.subplots()
    ax.scatter(x, y, label="Datos")
    xs = np.linspace(min(x), max(x), 100)
    ax.plot(xs, a + b * xs, label=_ecuacion(a, b))
    if x_pred is not None:
        ax.scatter([x_pred], [y_pred], marker="*", s=150, label="Predicción")
    ax.set_xlabel(f"x ({unidad_x})" if unidad_x else "x")
    ax.set_ylabel(f"y ({unidad_y})" if unidad_y else "y")
    ax.set_title("Diagrama de dispersión y recta de regresión")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def calcular_regresion(x, y, unidad_x="", unidad_y="", x_pred=None):
    x = lista_de_numeros(x, "los datos de x")
    y = lista_de_numeros(y, "los datos de y")

    if len(x) != len(y):
        raise ValueError(
            f"x tiene {len(x)} datos y y tiene {len(y)}. Deben tener la misma cantidad."
        )
    n = len(x)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 pares de datos.")
    if len(set(x)) == 1:
        raise ValueError("Todos los valores de x son iguales; no se puede calcular la recta.")
    if len(set(y)) == 1:
        raise ValueError("Todos los valores de y son iguales; la correlación r no está definida.")

    advertencias = []
    if n < 3:
        advertencias.append("Con solo 2 puntos la recta pasa exacta por ambos y r siempre vale ±1.")
    elif n < 5:
        advertencias.append("Hay pocos datos (n < 5); la correlación es poco confiable.")

    sx = sum(x)
    sy = sum(y)
    sxy = sum(xi * yi for xi, yi in zip(x, y))
    sxx = sum(xi ** 2 for xi in x)
    syy = sum(yi ** 2 for yi in y)
    media_x = sx / n
    media_y = sy / n

    num_b = n * sxy - sx * sy
    den_x = n * sxx - sx ** 2
    den_y = n * syy - sy ** 2

    b = num_b / den_x
    a = media_y - b * media_x
    r = num_b / math.sqrt(den_x * den_y)
    r2 = r ** 2

    formulas = [
        "r = [ nΣxy − ΣxΣy ] / √{ [ nΣx² − (Σx)² ] · [ nΣy² − (Σy)² ] }",
        "b = [ nΣxy − ΣxΣy ] / [ nΣx² − (Σx)² ]",
        "a = ȳ − b·x̄",
        "ŷ = a + b·x",
        "r² = coeficiente de determinación",
    ]
    sustitucion = [
        f"b = [ {n}·{num(sxy)} − {num(sx)}·{num(sy)} ] / [ {n}·{num(sxx)} − ({num(sx)})² ]"
        f" = {num(num_b)} / {num(den_x)} = {fmt(b)}",
        f"a = {fmt(media_y)} − {fmt(b)}·{fmt(media_x)} = {fmt(a)}",
        f"r = {num(num_b)} / √( {num(den_x)} · {num(den_y)} ) = {fmt(r)}",
        f"r² = ({fmt(r)})² = {fmt(r2)}",
    ]
    pasos = [
        f"n = {n} pares de datos.",
        f"Σx = {num(sx)},  Σy = {num(sy)},  Σxy = {num(sxy)},  Σx² = {num(sxx)},  Σy² = {num(syy)}.",
        f"Medias: x̄ = {fmt(media_x)},  ȳ = {fmt(media_y)}.",
        f"Pendiente: b = {fmt(b)}.  Intercepto: a = {fmt(a)}.",
        f"Ecuación de la recta: {_ecuacion(a, b)}.",
        f"Correlación: r = {fmt(r)}.",
    ]

    y_pred = None
    if x_pred is not None and not (isinstance(x_pred, str) and x_pred.strip() == ""):
        x_pred = numero(x_pred, "el valor de x a predecir")
        y_pred = a + b * x_pred
        sustitucion.append(
            f"Predicción: ŷ({num(x_pred)}) = {fmt(a)} + {fmt(b)}·{num(x_pred)} = {fmt(y_pred)}"
        )
        pasos.append(f"Predicción: para x = {num(x_pred)} se estima y = {fmt(y_pred)}.")
        if x_pred < min(x) or x_pred > max(x):
            advertencias.append(
                "El valor a predecir está fuera del rango de los datos (extrapolación); "
                "la predicción puede no ser confiable."
            )
    else:
        x_pred = None

    sentido = "positiva" if r > 0 else "negativa"
    tendencia = "aumentar" if b > 0 else "disminuir"
    if unidad_x and unidad_y:
        cambio = f"por cada 1 {unidad_x} que aumenta x, y cambia en promedio {fmt(b)} {unidad_y}."
    else:
        cambio = f"por cada unidad que aumenta x, y cambia en promedio {fmt(b)} unidades."
    interpretacion = (
        f"Hay una correlación lineal {_fuerza(r)} y {sentido} (r = {fmt(r)}): "
        f"cuando x aumenta, y tiende a {tendencia}. "
        f"Según r² = {fmt(r2)}, el {fmt(r2 * 100, 1)} % de la variación de y se explica "
        f"por la relación lineal con x. En la recta, {cambio} "
        "Recuerda que correlación no implica causalidad."
    )

    return {
        "titulo": "Correlación y regresión lineal simple",
        "formulas": formulas,
        "sustitucion": sustitucion,
        "pasos": pasos,
        "resultado": f"{_ecuacion(a, b)}   |   r = {fmt(r)}   |   r² = {fmt(r2)}",
        "interpretacion": interpretacion,
        "advertencias": advertencias,
        "grafica": _grafica(x, y, a, b, unidad_x, unidad_y, x_pred, y_pred),
        "valores": {"r": r, "r2": r2, "a": a, "b": b, "y_pred": y_pred},
    }


def mostrar():
    import streamlit as st
    from utils import parsear_datos
    from ayudas import mostrar_resultado

    c1, c2 = st.columns(2)
    tx = c1.text_area("Datos de x (decimales con punto)", "1, 2, 3, 4, 5", key="r_x")
    ty = c2.text_area("Datos de y (decimales con punto)", "2, 4, 5, 4, 5", key="r_y")
    c3, c4, c5 = st.columns(3)
    ux = c3.text_input("Unidad de x (opcional)", "", key="r_ux")
    uy = c4.text_input("Unidad de y (opcional)", "", key="r_uy")
    xp = c5.text_input("Predecir y para x = (opcional)", "", key="r_xp")
    if st.button("Calcular", key="b_regresion"):
        x, err_x = parsear_datos(tx, 2)
        y, err_y = parsear_datos(ty, 2)
        if err_x:
            st.error("Datos de x: " + err_x)
        elif err_y:
            st.error("Datos de y: " + err_y)
        else:
            try:
                mostrar_resultado(calcular_regresion(x, y, ux, uy, xp))
            except ValueError as e:
                st.error(str(e))
