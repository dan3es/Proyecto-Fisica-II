"""Desviación estándar poblacional vs. muestral."""
import math

from ayudas import fmt, num, lista_de_numeros


def calcular_media_desviaciones(datos):
    """Devuelve n, media, suma de cuadrados (sc), sigma (÷n) y s (÷n−1)."""
    datos = lista_de_numeros(datos, "los datos")
    n = len(datos)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 datos para calcular la desviación estándar muestral.")
    media = sum(datos) / n
    sc = sum((x - media) ** 2 for x in datos)
    return {
        "n": n,
        "media": media,
        "sc": sc,
        "sigma": math.sqrt(sc / n),
        "s": math.sqrt(sc / (n - 1)),
    }


def comparar_desviaciones(datos, unidad=""):
    datos = lista_de_numeros(datos, "los datos")
    c = calcular_media_desviaciones(datos)
    n, media, sc, sigma, s = c["n"], c["media"], c["sc"], c["sigma"], c["s"]
    u = f" {unidad}" if unidad else ""

    advertencias = []
    if len(set(datos)) == 1:
        advertencias.append("Todos los datos son iguales, por eso ambas desviaciones valen 0.")
    if n < 10:
        advertencias.append(
            f"Con n = {n} datos la diferencia entre ambas desviaciones es notable; "
            "por eso importa elegir la correcta."
        )

    pasos = [f"Media: x̄ = {fmt(media)}{u}  (n = {n})."]
    for i, x in enumerate(datos[:10], start=1):
        pasos.append(f"x{i} = {num(x)}  →  (x{i} − x̄)² = {fmt((x - media) ** 2, 6)}")
    if n > 10:
        pasos.append(f"... (se omiten {n - 10} datos más en esta lista).")
    pasos.append(f"Suma de cuadrados: Σ(xᵢ − x̄)² = {fmt(sc, 6)}.")

    formulas = [
        "Poblacional:  σ = √( Σ(xᵢ − x̄)² / n )",
        "Muestral:  s = √( Σ(xᵢ − x̄)² / (n − 1) )",
    ]
    sustitucion = [
        f"σ = √( {fmt(sc, 6)} / {n} ) = {fmt(sigma)}{u}",
        f"s = √( {fmt(sc, 6)} / {n - 1} ) = {fmt(s)}{u}",
    ]

    interpretacion = (
        f"σ = {fmt(sigma)}{u} se usa cuando los {n} datos son TODA la población "
        f"(se midió todo lo que interesa). s = {fmt(s)}{u} se usa cuando los datos son "
        "una MUESTRA de un conjunto mayor, como en la mayoría de los experimentos: "
        "al dividir entre (n − 1) se corrige que la muestra tiende a subestimar la "
        f"dispersión real. Aquí s es {fmt((s / sigma - 1) * 100 if sigma > 0 else 0, 1)} % mayor que σ; "
        "al crecer n la diferencia se vuelve despreciable."
    )

    return {
        "titulo": "Desviación estándar: poblacional vs. muestral",
        "formulas": formulas,
        "sustitucion": sustitucion,
        "pasos": pasos,
        "resultado": f"σ (poblacional) = {fmt(sigma)}{u}   |   s (muestral) = {fmt(s)}{u}",
        "interpretacion": interpretacion,
        "advertencias": advertencias,
        "grafica": None,
        "valores": c,
    }


def mostrar():
    import streamlit as st
    from utils import parsear_datos
    from ayudas import mostrar_resultado

    texto = st.text_area("Datos (separados por coma, espacio o salto de línea; decimales con punto)",
                         "2.1, 2.3, 2.2, 2.4, 2.0", key="i_datos")
    unidad = st.text_input("Unidad (opcional)", "A", key="i_unidad")
    if st.button("Comparar", key="b_interp"):
        datos, err = parsear_datos(texto, 2)
        if err:
            st.error(err)
        else:
            try:
                mostrar_resultado(comparar_desviaciones(datos, unidad))
            except ValueError as e:
                st.error(str(e))
