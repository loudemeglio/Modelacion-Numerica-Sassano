import numpy as np
from dinamica import calcular_dinamica, longitud_recta
from rk4 import paso_rk4

def simular_trayectoria(controlador, velocidad_inicial_kmh=200.0,
                        paso_tiempo=0.001, tiempo_maximo=30.0):

    velocidad_inicial = velocidad_inicial_kmh * 1000.0 / 3600.0
    estado = np.array([0.0, velocidad_inicial], dtype=float)  # [posicion, velocidad]
    tiempo = 0.0

    tiempos = [tiempo]
    posiciones = [estado[0]]
    velocidades = [estado[1]]
    aceleraciones = []

    def derivadas(t, estado_local):
        posicion_local, velocidad_local = estado_local
        acelerador, freno, usar_drs = controlador(t, posicion_local, velocidad_local)
        return calcular_dinamica(t, estado_local, acelerador, freno, usar_drs)

    while tiempo < tiempo_maximo and estado[0] < longitud_recta:

        derivada_actual = derivadas(tiempo, estado)
        aceleracion_actual = derivada_actual[1]

        estado = paso_rk4(derivadas, tiempo, estado, paso_tiempo)

        if estado[1] < 0.0:
            estado[1] = 0.0
        if estado[0] < 0.0:
            estado[0] = 0.0

        tiempo += paso_tiempo

        tiempos.append(tiempo)
        posiciones.append(estado[0])
        velocidades.append(estado[1])
        aceleraciones.append(aceleracion_actual)

    return (
        np.array(tiempos),
        np.array(posiciones),
        np.array(velocidades),
        np.array(aceleraciones),
    )
