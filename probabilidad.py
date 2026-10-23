"""Probabilidad básica y distribución normal."""
import math

import numpy as np
from matplotlib.figure import Figure

from ayudas import fmt, num, par, numero, probabilidad


def phi(z):
    """Φ(z) = P(Z <= z) para la normal estándar (usa la función de error)."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _grafica_normal(mu, sigma, tipo, a, b, unidad):
    xs = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    ys = np.exp(-0.5 * ((xs - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))
    if tipo == "menor":
        zona = xs <= a
    elif tipo == "mayor":
        zona = xs >= a
    else:
        zona = (xs >= a) & (xs <= b)
    fig = Figure(figsize=(7, 3.5))
    ax = fig.subplots()
    ax.plot(xs, ys)
    ax.fill_between(xs, ys, where=zona, alpha=0.4, label="Probabilidad buscada")
    ax.axvline(mu, linestyle="--", linewidth=1, label="Media (μ)")
    ax.set_title(f"Distribución normal (μ = {num(mu)}, σ = {num(sigma)})")
    ax.set_xlabel(f"x ({unidad})" if unidad else "x")
    ax.set_ylabel("Densidad")
    ax.legend()
    fig.tight_layout()
    return fig


def resolver_normal(mu, sigma, tipo, a, b=None, unidad=""):
    """Resuelve P(X < a), P(X > a) o P(a < X < b) para X ~ N(mu, sigma)."""
    mu = numero(mu, "la media (μ)")
    sigma = numero(sigma, "la desviación estándar (σ)")
    if sigma <= 0:
        raise ValueError("La desviación estándar σ debe ser mayor que 0.")
    if tipo not in ("menor", "mayor", "entre"):
        raise ValueError("El tipo debe ser 'menor', 'mayor' o 'entre'.")
    a = numero(a, "el valor a")

    advertencias = []
    u = f" {unidad}" if unidad else ""
    formulas = ["z = (x − μ) / σ"]
    sustitucion = []
    pasos = []

    if tipo == "entre":
        if b is None or (isinstance(b, str) and b.strip() == ""):
            raise ValueError("Para P(a < X < b) falta el valor de b.")
        b = numero(b, "el valor b")
        if a > b:
            a, b = b, a
            advertencias.append("a era mayor que b; se intercambiaron para que a < b.")
        za = (a - mu) / sigma
        zb = (b - mu) / sigma
        p = phi(zb) - phi(za)
        formulas.append("P(a < X < b) = Φ(z_b) − Φ(z_a)")
        sustitucion.append(f"z_a = ({num(a)} − {par(mu)}) / {num(sigma)} = {fmt(za)}")
        sustitucion.append(f"z_b = ({num(b)} − {par(mu)}) / {num(sigma)} = {fmt(zb)}")
        pasos.append(f"Estandarizar: z_a = {fmt(za, 2)} y z_b = {fmt(zb, 2)}.")
        pasos.append(
            f"Con la tabla normal (z a 2 decimales): Φ({fmt(zb, 2)}) = {fmt(phi(round(zb, 2)))} "
            f"y Φ({fmt(za, 2)}) = {fmt(phi(round(za, 2)))}."
        )
        pasos.append(f"Restar: P = {fmt(phi(zb))} − {fmt(phi(za))} = {fmt(p)}.")
        resultado = f"P({num(a)} < X < {num(b)}) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
        interpretacion = (
            f"Aproximadamente el {fmt(p * 100, 2)} % de los valores de X están "
            f"entre {num(a)}{u} y {num(b)}{u}."
        )
        zs = [za, zb]
        valores = {"z": za, "z_b": zb, "p": p}
    else:
        za = (a - mu) / sigma
        sustitucion.append(f"z = ({num(a)} − {par(mu)}) / {num(sigma)} = {fmt(za)}")
        pasos.append(f"Estandarizar: z = {fmt(za, 2)}.")
        pasos.append(
            f"Con la tabla normal (z a 2 decimales): Φ({fmt(za, 2)}) = {fmt(phi(round(za, 2)))}."
        )
        if tipo == "menor":
            p = phi(za)
            formulas.append("P(X < a) = P(Z < z) = Φ(z)")
            pasos.append(f"P(X < {num(a)}) = Φ({fmt(za, 2)}) = {fmt(p)}.")
            resultado = f"P(X < {num(a)}) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
            interpretacion = (
                f"Aproximadamente el {fmt(p * 100, 2)} % de los valores de X "
                f"son menores que {num(a)}{u}."
            )
        else:
            p = 1 - phi(za)
            formulas.append("P(X > a) = 1 − Φ(z)")
            pasos.append(
                f"P(X > {num(a)}) = 1 − Φ({fmt(za, 2)}) = 1 − {fmt(phi(za))} = {fmt(p)}."
            )
            resultado = f"P(X > {num(a)}) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
            interpretacion = (
                f"Aproximadamente el {fmt(p * 100, 2)} % de los valores de X "
                f"son mayores que {num(a)}{u}."
            )
        zs = [za]
        valores = {"z": za, "p": p}

    if any(abs(z) > 4 for z in zs):
        advertencias.append(
            "Un valor está a más de 4 desviaciones de la media; "
            "la probabilidad correspondiente es prácticamente 0 o 1."
        )

    return {
        "titulo": f"Distribución normal: X ~ N(μ = {num(mu)}, σ = {num(sigma)})",
        "formulas": formulas,
        "sustitucion": sustitucion,
        "pasos": pasos,
        "resultado": resultado,
        "interpretacion": interpretacion,
        "advertencias": advertencias,
        "grafica": _grafica_normal(mu, sigma, tipo, a, b, unidad),
        "valores": valores,
    }


def resolver_probabilidad_basica(tipo, favorables=None, total=None,
                                 pA=None, pB=None, pAyB=None):
    """tipo: clasica, complemento, union, independientes o condicional."""
    advertencias = []

    if tipo == "clasica":
        fav = numero(favorables, "los casos favorables")
        tot = numero(total, "los casos totales")
        if tot <= 0 or tot != int(tot) or fav != int(fav):
            raise ValueError("Los casos favorables y totales deben ser enteros, y el total mayor que 0.")
        if fav < 0 or fav > tot:
            raise ValueError("Los casos favorables deben estar entre 0 y el total de casos.")
        p = fav / tot
        titulo = "Probabilidad clásica"
        formulas = ["P(A) = casos favorables / casos totales"]
        sustitucion = [f"P(A) = {num(fav)} / {num(tot)}"]
        pasos = ["Se asume que todos los resultados son igualmente probables."]
        resultado = f"P(A) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
        interpretacion = (
            f"De cada 100 repeticiones, se espera que A ocurra unas {fmt(p * 100, 1)} veces."
        )

    elif tipo == "complemento":
        pa = probabilidad(pA, "P(A)")
        p = 1 - pa
        titulo = "Probabilidad del complemento"
        formulas = ["P(no A) = 1 − P(A)"]
        sustitucion = [f"P(no A) = 1 − {num(pa)}"]
        pasos = ["El evento y su complemento suman siempre 1."]
        resultado = f"P(no A) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
        interpretacion = f"La probabilidad de que A NO ocurra es {fmt(p * 100, 2)} %."

    elif tipo == "union":
        pa = probabilidad(pA, "P(A)")
        pb = probabilidad(pB, "P(B)")
        if pAyB is None or (isinstance(pAyB, str) and pAyB.strip() == ""):
            pab = 0.0
            advertencias.append(
                "No se dio P(A ∩ B); se asumió 0 (eventos mutuamente excluyentes)."
            )
        else:
            pab = probabilidad(pAyB, "P(A ∩ B)")
        if pab > min(pa, pb):
            raise ValueError("P(A ∩ B) no puede ser mayor que P(A) ni que P(B).")
        p = pa + pb - pab
        titulo = "Probabilidad de la unión"
        formulas = ["P(A ∪ B) = P(A) + P(B) − P(A ∩ B)"]
        sustitucion = [f"P(A ∪ B) = {num(pa)} + {num(pb)} − {num(pab)}"]
        pasos = ["Se resta la intersección para no contarla dos veces."]
        resultado = f"P(A ∪ B) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
        interpretacion = f"La probabilidad de que ocurra A, B o ambos es {fmt(p * 100, 2)} %."

    elif tipo == "independientes":
        pa = probabilidad(pA, "P(A)")
        pb = probabilidad(pB, "P(B)")
        p = pa * pb
        titulo = "Intersección de eventos independientes"
        formulas = ["P(A ∩ B) = P(A) · P(B)"]
        sustitucion = [f"P(A ∩ B) = {num(pa)} · {num(pb)}"]
        pasos = ["Esta fórmula solo es válida si A y B son independientes."]
        resultado = f"P(A ∩ B) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
        interpretacion = f"La probabilidad de que ocurran A y B juntos es {fmt(p * 100, 2)} %."
        advertencias.append("Se asume que A y B son independientes.")

    elif tipo == "condicional":
        pab = probabilidad(pAyB, "P(A ∩ B)")
        pb = probabilidad(pB, "P(B)")
        if pb == 0:
            raise ValueError("P(B) no puede ser 0 en una probabilidad condicional.")
        if pab > pb:
            raise ValueError("P(A ∩ B) no puede ser mayor que P(B).")
        p = pab / pb
        titulo = "Probabilidad condicional"
        formulas = ["P(A | B) = P(A ∩ B) / P(B)"]
        sustitucion = [f"P(A | B) = {num(pab)} / {num(pb)}"]
        pasos = ["Se restringe el espacio muestral a los casos en que B ya ocurrió."]
        resultado = f"P(A | B) = {fmt(p)}  ({fmt(p * 100, 2)} %)"
        interpretacion = f"Sabiendo que B ocurrió, la probabilidad de A es {fmt(p * 100, 2)} %."

    else:
        raise ValueError(
            "Tipo no reconocido. Usa: clasica, complemento, union, independientes o condicional."
        )

    return {
        "titulo": titulo,
        "formulas": formulas,
        "sustitucion": sustitucion,
        "pasos": pasos,
        "resultado": resultado,
        "interpretacion": interpretacion,
        "advertencias": advertencias,
        "grafica": None,
        "valores": {"p": p},
    }


def mostrar():
    import streamlit as st
    from ayudas import mostrar_resultado

    modo = st.radio("¿Qué quieres resolver?",
                    ["Distribución normal", "Probabilidad básica"],
                    horizontal=True, key="prob_modo")

    if modo == "Distribución normal":
        c1, c2, c3 = st.columns(3)
        mu = c1.text_input("Media (μ)", "70", key="n_mu")
        sigma = c2.text_input("Desviación estándar (σ)", "10", key="n_sigma")
        unidad = c3.text_input("Unidad (opcional)", "", key="n_unidad")
        opciones = {"P(X < a)": "menor", "P(X > a)": "mayor", "P(a < X < b)": "entre"}
        eleccion = st.selectbox("Probabilidad a calcular", list(opciones), key="n_tipo")
        tipo = opciones[eleccion]
        c4, c5 = st.columns(2)
        a = c4.text_input("Valor a", "85", key="n_a")
        b = c5.text_input("Valor b (solo para P(a < X < b))", "", key="n_b") if tipo == "entre" else None
        if st.button("Calcular", key="b_normal"):
            try:
                mostrar_resultado(resolver_normal(mu, sigma, tipo, a, b, unidad))
            except ValueError as e:
                st.error(str(e))
    else:
        etiquetas = {
            "Probabilidad clásica: favorables / totales": "clasica",
            "Complemento: P(no A)": "complemento",
            "Unión: P(A ∪ B)": "union",
            "Eventos independientes: P(A ∩ B)": "independientes",
            "Condicional: P(A | B)": "condicional",
        }
        eleccion = st.selectbox("Tipo de ejercicio", list(etiquetas), key="pb_tipo")
        tipo = etiquetas[eleccion]
        args = {}
        if tipo == "clasica":
            c1, c2 = st.columns(2)
            args["favorables"] = c1.text_input("Casos favorables", "6", key="pb_fav")
            args["total"] = c2.text_input("Casos totales", "36", key="pb_tot")
        elif tipo == "complemento":
            args["pA"] = st.text_input("P(A)", "0.3", key="pb_pa1")
        elif tipo == "union":
            c1, c2, c3 = st.columns(3)
            args["pA"] = c1.text_input("P(A)", "0.5", key="pb_pa2")
            args["pB"] = c2.text_input("P(B)", "0.3", key="pb_pb2")
            args["pAyB"] = c3.text_input("P(A ∩ B) (vacío = excluyentes)", "0.1", key="pb_pab2")
        elif tipo == "independientes":
            c1, c2 = st.columns(2)
            args["pA"] = c1.text_input("P(A)", "0.5", key="pb_pa3")
            args["pB"] = c2.text_input("P(B)", "0.4", key="pb_pb3")
        else:
            c1, c2 = st.columns(2)
            args["pAyB"] = c1.text_input("P(A ∩ B)", "0.1", key="pb_pab4")
            args["pB"] = c2.text_input("P(B)", "0.4", key="pb_pb4")
        if st.button("Calcular", key="b_basica"):
            try:
                mostrar_resultado(resolver_probabilidad_basica(tipo, **args))
            except ValueError as e:
                st.error(str(e))
