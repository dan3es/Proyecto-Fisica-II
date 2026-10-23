"""tablas.py - Tabla de frecuencias e histograma."""
import math
from bisect import bisect_right
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils import fmt


def sturges(n):
    return math.ceil(1 + 3.322 * math.log10(n))


def tabla_frecuencias(datos, k=None):
    n = len(datos)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 datos para una tabla de frecuencias.")
    mn, mx = min(datos), max(datos)
    if mx == mn:
        raise ValueError("Todos los datos son iguales; no se pueden formar clases.")
    k = k or sturges(n)
    amp = (mx - mn) / k
    # Límites de clase redondeados para que un dato que cae justo en un límite
    # (p. ej. 4.84) no se clasifique mal por el error de punto flotante.
    bordes = [round(mn + i * amp, 9) for i in range(k + 1)]
    bordes[-1] = mx
    frec = [0] * k
    for x in datos:
        frec[min(bisect_right(bordes, x) - 1, k - 1)] += 1
    filas, acum = [], 0
    for i in range(k):
        li, ls = bordes[i], bordes[i + 1]
        acum += frec[i]
        filas.append({"Clase": i + 1,
                      "Intervalo": f"[{fmt(li, 3)} , {fmt(ls, 3)}{']' if i == k - 1 else ')'}",
                      "Marca de clase": round((li + ls) / 2, 4),
                      "f": frec[i], "fr": round(frec[i] / n, 4),
                      "F": acum, "Fr": round(acum / n, 4)})
    info = {"k": k, "amplitud": amp, "bordes": bordes,
            "pasos": [f"Rango = {fmt(mx)} - {fmt(mn)} = {fmt(mx - mn)}",
                      f"Clases (Sturges): k = 1 + 3.322·log10({n}) ≈ {k}",
                      f"Amplitud: A = Rango / k = {fmt(mx - mn)} / {k} = {fmt(amp)}"]}
    return pd.DataFrame(filas), info


def histograma(datos, bordes, unidad=""):
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.hist(datos, bins=bordes, edgecolor="black", color="#4C78A8")
    ax.set_xlabel(f"Valor ({unidad})" if unidad else "Valor")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Histograma")
    plt.close(fig)
    return fig
