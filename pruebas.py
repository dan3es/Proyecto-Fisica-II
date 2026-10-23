"""Pruebas de los cálculos con valores conocidos. Ejecutar con: python pruebas.py"""
import statistics

import descriptiva
import experimental
import tablas
from interpretacion import comparar_desviaciones
from probabilidad import resolver_normal, resolver_probabilidad_basica
from regresion import calcular_regresion
from practicas import EJEMPLOS, TIPOS_PRACTICA, generar_practica, evaluar_respuesta, resolver_ejemplo

pruebas = 0


def comprobar(nombre, obtenido, esperado, tolerancia=1e-4):
    global pruebas
    pruebas += 1
    assert abs(obtenido - esperado) <= tolerancia, f"{nombre}: {obtenido} != {esperado}"
    print(f"OK  {nombre}: {obtenido:.4f}")


corrientes = [2.1, 2.3, 2.2, 2.4, 2.0]
d = descriptiva.analizar(corrientes, unidad="A")
comprobar("Media de las corrientes", d["media"], 2.2)
comprobar("Desviación muestral", d["desv"], 0.1581)
comprobar("Desviación muestral (statistics)", d["desv"], statistics.stdev(corrientes))
comprobar("Desviación poblacional", descriptiva.analizar(corrientes, poblacional=True)["desv"], 0.1414)
comprobar("Error de la media", experimental.analizar_exp(corrientes, "A")["error_media"], 0.0707)

comprobar("Comparación σ", comparar_desviaciones(corrientes, "A")["valores"]["sigma"], 0.1414)
comprobar("Comparación s", comparar_desviaciones(corrientes, "A")["valores"]["s"], 0.1581)

reg = calcular_regresion([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])["valores"]
comprobar("Regresión: intercepto a", reg["a"], 2.2)
comprobar("Regresión: pendiente b", reg["b"], 0.6)
comprobar("Regresión: correlación r", reg["r"], 0.7746)

comprobar("Normal: P(Z < 1.96)", resolver_normal(0, 1, "menor", 1.96)["valores"]["p"], 0.9750)
comprobar("Normal: P(-1 < Z < 1)", resolver_normal(0, 1, "entre", -1, 1)["valores"]["p"], 0.6827)
comprobar("Normal: P(X > 85), μ=70, σ=10", resolver_normal(70, 10, "mayor", 85)["valores"]["p"], 0.0668)
comprobar("Unión P(A ∪ B)", resolver_probabilidad_basica("union", pA=0.5, pB=0.3, pAyB=0.1)["valores"]["p"], 0.7)

df, info = tablas.tabla_frecuencias([4.8, 5.1, 5.0, 4.9, 5.3, 5.2, 4.7, 5.0, 5.1, 4.9, 5.4, 5.0, 4.8, 5.2, 5.1])
comprobar("Tabla de frecuencias: suma de f", df["f"].sum(), 15)

for tipo in TIPOS_PRACTICA:
    p = generar_practica(tipo, semilla=1)
    correctas = {k: f"{v:.4f}" for k, v in p["respuestas_correctas"].items()}
    comprobar(f"Generador '{tipo}': respuestas correctas", evaluar_respuesta(p, correctas)["puntaje"], len(correctas))

for ej in EJEMPLOS:
    resolver_ejemplo(ej)
comprobar("Ejemplos resueltos sin error", len(EJEMPLOS), 11)

for entrada, mensaje in [(lambda: calcular_regresion([1, 2, 3], [1, 2]), "misma cantidad"),
                         (lambda: resolver_normal(0, 0, "menor", 1), "mayor que 0"),
                         (lambda: resolver_probabilidad_basica("complemento", pA=1.5), "entre 0 y 1")]:
    try:
        entrada()
        raise AssertionError("debía lanzar un error")
    except ValueError as e:
        assert mensaje in str(e)
        pruebas += 1
        print(f"OK  Aviso de error: {e}")

print(f"\nTodas las pruebas pasaron ({pruebas}).")
