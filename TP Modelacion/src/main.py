import matplotlib.pyplot as plt

from controlador import crear_controlador
from simulacion import simular_trayectoria
from dinamica import velocidad_limite_final

# Distintas trayectorias
parametros_trayectorias = [
    (0.20, 0.60, 4.0),
    (0.25, 0.65, 4.0),
    (0.30, 0.70, 4.0),
    (0.15, 0.55, 3.8),
    (0.10, 0.50, 3.5),
    (0.22, 0.62, 4.2),
    (0.18, 0.58, 3.6),
    (0.28, 0.68, 3.9),
    (0.24, 0.64, 3.7),
    (0.12, 0.52, 3.5),
]

mejor_tiempo = 1e9
mejores_parametros = None
mejor_trayectoria = None

print("Simulando 10 trayectorias...\n")

for (factor_inicio_drs, factor_fin_drs, desaceleracion_max_frenado_g) in parametros_trayectorias:

    controlador = crear_controlador(
        factor_inicio_drs,
        factor_fin_drs,
        desaceleracion_max_frenado_g
    )
    tiempos, posiciones, velocidades, aceleraciones = simular_trayectoria(controlador)

    tiempo_total = tiempos[-1]
    velocidad_final = velocidades[-1]

    print(f"factor_inicio_drs={factor_inicio_drs}, factor_fin_drs={factor_fin_drs}, desaceleracion_max_frenado_g={desaceleracion_max_frenado_g}")
    print(f"  Tiempo total = {tiempo_total:.3f} s")
    print(f"  Velocidad final = {velocidad_final*3.6:.2f} km/h\n")

    # Nos quedamos con la mejor que respete la velocidad final
    if velocidad_final <= velocidad_limite_final and tiempo_total < mejor_tiempo:
        mejor_tiempo = tiempo_total
        mejores_parametros = (factor_inicio_drs, factor_fin_drs, desaceleracion_max_frenado_g)
        mejor_trayectoria = (tiempos, posiciones, velocidades, aceleraciones)

print("\n===========================")
print("MEJOR TRAYECTORIA")
print("Parametros:", mejores_parametros)
print(f"Tiempo total: {mejor_tiempo:.3f} s")
print("===========================\n")

# En caso de encontrar una trayectoria valida, la graficamos, si encontramos mas de una, graficamos la mejor
if mejor_trayectoria is not None:
    tiempos, posiciones, velocidades, aceleraciones = mejor_trayectoria

    plt.figure()
    plt.plot(tiempos, posiciones)
    plt.title("Posicion respecto al tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Posicion [m]")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(tiempos, velocidades)
    plt.title("Velocidad respecto al tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad [m/s]")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(tiempos[:-1], aceleraciones)
    plt.title("Aceleracion respecto al tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Aceleracion [m/s²]")
    plt.grid(True)
    plt.show()
else:
    print("No obtuvimos ninguna trayectoria valida.")
