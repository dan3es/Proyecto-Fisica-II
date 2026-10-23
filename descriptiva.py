"""descriptiva.py - Estadística descriptiva con fórmula, sustitución y resultado."""
import math
from collections import Counter
from utils import fmt, unir


def moda(datos):
    c = Counter(datos)
    m = max(c.values())
    return [] if m == 1 else sorted(k for k, v in c.items() if v == m)


def analizar(datos, poblacional=False, unidad=""):
    n = len(datos)
    if n < 1:
        raise ValueError("No hay datos para analizar.")
    if n < 2 and not poblacional:
        raise ValueError("La desviación muestral necesita al menos 2 datos.")
    u = f" {unidad}" if unidad else ""
    u2 = f" {unidad}²" if unidad else ""
    s = sorted(datos)
    suma = sum(datos)
    media = suma / n
    mid = n // 2
    mediana = s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2
    mo = moda(datos)
    rango = s[-1] - s[0]
    ss = sum((x - media) ** 2 for x in datos)
    div = n if poblacional else n - 1
    var = ss / div
    sd = math.sqrt(var)
    cv = sd / abs(media) * 100 if media != 0 else None

    pasos = [
        {"titulo": "Media aritmética",
         "formula": r"\bar{x}=\frac{\sum x_i}{n}",
         "sustitucion": f"({unir(datos, ' + ')}) / {n} = {fmt(suma)} / {n}",
         "resultado": f"x̄ = {fmt(media)}{u}"},
        {"titulo": "Mediana",
         "formula": r"\tilde{x}=x_{(n+1)/2}\ \text{(n impar)}\quad \tilde{x}=\frac{x_{n/2}+x_{n/2+1}}{2}\ \text{(n par)}",
         "sustitucion": f"Datos ordenados: {unir(s)}  (n = {n}, {'impar' if n % 2 else 'par'})",
         "resultado": f"Mediana = {fmt(mediana)}{u}"},
        {"titulo": "Moda",
         "formula": r"\text{Valor(es) con mayor frecuencia}",
         "sustitucion": "Frecuencias: " + ", ".join(f"{fmt(k)}→{v}" for k, v in sorted(Counter(datos).items()))[:200],
         "resultado": ("Moda = " + unir(mo) + u) if mo else "No hay moda (todos los valores se repiten igual)"},
        {"titulo": "Rango",
         "formula": r"R = x_{max} - x_{min}",
         "sustitucion": f"{fmt(s[-1])} - {fmt(s[0])}",
         "resultado": f"R = {fmt(rango)}{u}"},
        {"titulo": "Varianza " + ("poblacional" if poblacional else "muestral"),
         "formula": (r"\sigma^2=\frac{\sum (x_i-\mu)^2}{n}" if poblacional
                     else r"s^2=\frac{\sum (x_i-\bar{x})^2}{n-1}"),
         "sustitucion": f"Σ(xi - {fmt(media)})² = {fmt(ss)};  {fmt(ss)} / {div}"
                        + (" (n)" if poblacional else " (n-1)"),
         "resultado": f"{'σ²' if poblacional else 's²'} = {fmt(var)}{u2}"},
        {"titulo": "Desviación estándar " + ("poblacional" if poblacional else "muestral"),
         "formula": r"\sigma=\sqrt{\sigma^2}" if poblacional else r"s=\sqrt{s^2}",
         "sustitucion": f"√{fmt(var)}",
         "resultado": f"{'σ' if poblacional else 's'} = {fmt(sd)}{u}"},
    ]
    interp = (f"Los datos se concentran alrededor de {fmt(media)}{u}; en promedio se alejan "
              f"unos {fmt(sd)}{u} de la media.")
    if cv is not None:
        nivel = "baja" if cv < 10 else "moderada" if cv < 30 else "alta"
        interp += f" El coeficiente de variación es {fmt(cv, 2)} % (dispersión {nivel})."
    return {"n": n, "media": media, "mediana": mediana, "moda": mo, "rango": rango,
            "varianza": var, "desv": sd, "poblacional": poblacional,
            "pasos": pasos, "interpretacion": interp}
