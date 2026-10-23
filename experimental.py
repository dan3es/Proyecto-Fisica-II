"""experimental.py - Series de mediciones físicas con unidades."""
import math
from utils import fmt
import descriptiva

UNIDADES = ["A", "V", "m", "s", "kg", "N", "Ω", "°C", "J", "W", "(otra)"]
CONVERSIONES = {  # nombre: (factor, unidad destino)
    "mA → A": (1e-3, "A"), "µA → A": (1e-6, "A"),
    "mV → V": (1e-3, "V"), "kV → V": (1e3, "V"),
    "mm → m": (1e-3, "m"), "cm → m": (1e-2, "m"), "km → m": (1e3, "m"),
    "ms → s": (1e-3, "s"), "min → s": (60, "s"), "g → kg": (1e-3, "kg"),
}


def convertir(datos, clave):
    factor, destino = CONVERSIONES[clave]
    return [x * factor for x in datos], destino


def analizar_exp(datos, unidad):
    res = descriptiva.analizar(datos, poblacional=False, unidad=unidad)
    n, s, media = res["n"], res["desv"], res["media"]
    u = f" {unidad}" if unidad else ""
    err = s / math.sqrt(n)
    res["error_media"] = err
    res["pasos"].append({
        "titulo": "Error estándar de la media",
        "formula": r"s_{\bar{x}}=\frac{s}{\sqrt{n}}",
        "sustitucion": f"{fmt(s)} / √{n} = {fmt(s)} / {fmt(math.sqrt(n))}",
        "resultado": f"s_x̄ = {fmt(err)}{u}"})
    res["pasos"].append({
        "titulo": "Resultado de la medición",
        "formula": r"x=\bar{x}\pm s_{\bar{x}}",
        "sustitucion": f"{fmt(media)} ± {fmt(err)}",
        "resultado": f"x = ({fmt(media)} ± {fmt(err)}){u}"})
    return res
