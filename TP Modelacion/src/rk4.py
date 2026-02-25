import numpy as np

def paso_rk4(funcion_derivadas, tiempo, estado, paso_tiempo):
    k1 = funcion_derivadas(tiempo, estado)
    k2 = funcion_derivadas(tiempo + 0.5 * paso_tiempo, estado + 0.5 * paso_tiempo * k1)
    k3 = funcion_derivadas(tiempo + 0.5 * paso_tiempo, estado + 0.5 * paso_tiempo * k2)
    k4 = funcion_derivadas(tiempo + paso_tiempo,       estado + paso_tiempo * k3)

    return estado + (paso_tiempo / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
