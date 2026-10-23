"""Formato y validación de datos para probabilidad, regresión, interpretación y prácticas."""
import math

DECIMALES = 4


def fmt(x, d=DECIMALES):
    """Número con d decimales: 0.158113 -> '0.1581'."""
    return f"{x:.{d}f}"


def num(x):
    """Número sin ceros de más: 70.0 -> '70', 2.25 -> '2.25'."""
    return f"{x:g}"


def par(x):
    """Pone paréntesis si el número es negativo: -3 -> '(-3)'."""
    return f"({num(x)})" if x < 0 else num(x)


def numero(valor, nombre):
    """Convierte un valor a float o lanza ValueError con mensaje claro."""
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        raise ValueError(f"Falta el valor de {nombre}.")
    try:
        n = float(str(valor).replace(",", ".")) if isinstance(valor, str) else float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{nombre} debe ser un número (se recibió '{valor}').")
    if math.isnan(n) or math.isinf(n):
        raise ValueError(f"{nombre} no es un número válido.")
    return n


def probabilidad(valor, nombre):
    """Valida que el valor sea una probabilidad (entre 0 y 1)."""
    p = numero(valor, nombre)
    if p < 0 or p > 1:
        raise ValueError(f"{nombre} debe estar entre 0 y 1 (se recibió {num(p)}).")
    return p


def lista_de_numeros(valores, nombre="los datos"):
    """Convierte una lista a lista de floats, validando cada elemento."""
    if valores is None:
        raise ValueError(f"Faltan {nombre}.")
    if isinstance(valores, str):
        raise ValueError(
            f"{nombre} debe ser una lista de números, no un texto. "
            "Usa la función de lectura de utils.py para convertir el texto."
        )
    try:
        lista = list(valores)
    except TypeError:
        raise ValueError(f"{nombre} debe ser una lista de números.")
    if len(lista) == 0:
        raise ValueError(f"No hay valores en {nombre}.")
    resultado = []
    for i, v in enumerate(lista, start=1):
        try:
            n = float(v)
        except (TypeError, ValueError):
            raise ValueError(f"El dato {i} de {nombre} ('{v}') no es un número.")
        if math.isnan(n) or math.isinf(n):
            raise ValueError(f"El dato {i} de {nombre} no es un número válido.")
        resultado.append(n)
    return resultado


def mostrar_resultado(res):
    """Muestra un resultado con título, fórmulas, sustitución, pasos e interpretación."""
    import streamlit as st

    st.subheader(res["titulo"])
    for adv in res.get("advertencias", []):
        st.warning("⚠️ " + adv)
    st.markdown("**Fórmulas**")
    st.code("\n".join(res["formulas"]), language="text")
    st.markdown("**Sustitución de valores**")
    st.code("\n".join(res["sustitucion"]), language="text")
    st.markdown("**Procedimiento**")
    for paso in res["pasos"]:
        st.write("• " + paso)
    st.success("✅ Resultado final:  " + res["resultado"])
    st.info("💡 " + res["interpretacion"])
    if res.get("grafica") is not None:
        st.pyplot(res["grafica"])


def mostrar_pasos(res):
    """Muestra una lista de pasos, cada uno con su fórmula en LaTeX."""
    import streamlit as st

    for p in res["pasos"]:
        with st.container(border=True):
            st.markdown(f"**{p['titulo']}**")
            st.latex(p["formula"])
            st.write("Sustitución: " + p["sustitucion"])
            st.success(p["resultado"])
    st.info("💡 " + res["interpretacion"])
