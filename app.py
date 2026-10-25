"""app.py - Interfaz principal. Ejecutar con: streamlit run app.py"""
import importlib
import streamlit as st
from utils import parsear_datos, fmt
import descriptiva, experimental, tablas

NOMBRE_APP = "LIDNIA"
INTEGRANTES = ["Valery Ivonne Amaya Jorge", 
               "Darlene Josabet Santizo Carrillo"]
ASIGNATURA = "Física II"
SECCION = "Sección A"

st.set_page_config(page_title=NOMBRE_APP, page_icon="📋", layout="wide")
st.title(f"📋 {NOMBRE_APP}")
st.caption("Asistente virtual de Física II  |  " + " y ".join(INTEGRANTES)
    + f"  |  {ASIGNATURA}  |  {SECCION}  |  Universidad Mariano Gálvez de Guatemala")

EJEMPLO = "2.1, 2.3, 2.2, 2.4, 2.0"


def mostrar_resultado(res):
    """Muestra fórmula, sustitución y resultado de cada paso."""
    for p in res["pasos"]:
        with st.container(border=True):
            st.markdown(f"**{p['titulo']}**")
            st.latex(p["formula"])
            st.write("Sustitución: " + p["sustitucion"])
            st.success(p["resultado"])
        if res.get("interpretacion"):
        st.info("💡 " + res["interpretacion"])


def entrada(clave, minimo=2):
    texto = st.text_area("Datos (separados por coma, espacio o salto de línea; decimales con punto)",
                         value=EJEMPLO, key=clave)
    st.caption("Usa punto como decimal (2.5, no 2,5); la coma separa datos.")
    return parsear_datos(texto, minimo)


def cargar_modulo(nombre):
    """Carga la función mostrar() de un módulo; si falla, muestra un aviso."""
    try:
        return importlib.import_module(nombre).mostrar
    except Exception as e:
        return lambda: st.info(f"Módulo '{nombre}' aún no disponible ({e}).")


pregunta, *tabs = st.tabs(["Pregunta", "Descriptiva", "Datos experimentales", "Tablas y gráficas",
                           "Probabilidad", "Regresión", "Práctica", "Interpretación"])

with pregunta:
    cargar_modulo("interprete")()

with tabs[0]:
    datos, err = entrada("d_desc")
    tipo = st.radio("Tipo de datos", ["Muestra (÷ n−1)", "Población (÷ n)"], horizontal=True)
    pedidas = st.multiselect("Qué calcular", descriptiva.MEDIDAS, default=descriptiva.MEDIDAS)
    if st.button("Calcular", key="b_desc"):
        if err:
            st.error(err)
        elif not pedidas:
            st.error("Elige al menos una medida.")
        else:
            res = descriptiva.analizar(datos, poblacional=tipo.startswith("Pob"))
            mostrar_resultado(descriptiva.filtrar(res, pedidas))

with tabs[1]:
    datos, err = entrada("d_exp")
    c1, c2 = st.columns(2)
    sel = c1.selectbox("Unidad", experimental.UNIDADES)
    otra = c2.text_input("Si elegiste (otra), escríbela") if sel == "(otra)" else ""
    unidad = otra if sel == "(otra)" else sel
    conv = st.selectbox("Convertir antes de calcular (opcional)",
                        ["Ninguna"] + list(experimental.CONVERSIONES))
    if st.button("Calcular", key="b_exp"):
        if err:
            st.error(err)
        else:
            if conv != "Ninguna":
                datos, unidad = experimental.convertir(datos, conv)
                st.caption(f"Datos convertidos: {', '.join(fmt(x) for x in datos)} {unidad}")
            mostrar_resultado(experimental.analizar_exp(datos, unidad))

with tabs[2]:
    datos, err = entrada("d_tab")
    k = st.number_input("Número de clases (0 = automático, regla de Sturges)", 0, 30, 0)
    if st.button("Construir tabla", key="b_tab"):
        if err:
            st.error(err)
        else:
            try:
                df, info = tablas.tabla_frecuencias(datos, int(k) or None)
                for linea in info["pasos"]:
                    st.write("• " + linea)
                st.dataframe(df, hide_index=True)
                st.pyplot(tablas.histograma(datos, info["bordes"]))
            except ValueError as e:
                st.error(str(e))

with tabs[3]:
    cargar_modulo("probabilidad")()
with tabs[4]:
    cargar_modulo("regresion")()
with tabs[5]:
    cargar_modulo("practicas")()
with tabs[6]:
    cargar_modulo("interpretacion")()

    