"""utils.py - Lectura y validación de datos. Lo usan todos los módulos."""
import re
import math


def parsear_datos(texto, minimo=1):
    """Convierte '2.1, 2.3  2.2\n2.4' en [2.1, 2.3, 2.2, 2.4].
    Devuelve (datos, error). Si hay error, datos es None."""
    if texto is None or not texto.strip():
        return None, "El campo está vacío. Ingresa al menos un número."
    tokens = [t for t in re.split(r"[,;\s]+", texto.strip()) if t]
    datos, malos = [], []
    for t in tokens:
        try:
            x = float(t)
            if not math.isfinite(x):
                raise ValueError
            datos.append(x)
        except ValueError:
            malos.append(t)
    if malos:
        return None, "Valores no numéricos: " + ", ".join(malos) + \
            ". Usa punto decimal (2.5) y separa con comas, espacios o saltos de línea."
    if len(datos) < minimo:
        return None, f"Se necesitan al menos {minimo} datos (ingresaste {len(datos)})."
    return datos, None


def fmt(x, d=4):
    """Formatea un número: redondea a d decimales sin ceros sobrantes."""
    if abs(x) <= 1e-18:
        return "0"
    if abs(x) < 0.001:
        return f"{x:.4g}"
    s = f"{x:.{d}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def unir(valores, sep=", ", limite=12):
    """Une valores en texto; si son muchos, abrevia con '...'."""
    t = [fmt(v) for v in valores]
    if len(t) > limite:
        t = t[:limite] + ["..."]
    return sep.join(t)
