import numpy as np
import math

# fisica del auto

masa = 800.0                        # kg
densidad_aire = 1.19                # kg/m^3
area_frontal = 1.4                  # m^2
gravedad = 9.80665                  # m/s^2
coef_rozamiento_neumaticos = 1.6    # μ
coef_downforce = 1.5                # C_L
coef_arrastre_sin_drs = 0.85        # C_D sin DRS
coef_arrastre_con_drs = 0.70        # C_D con DRS

caballo_de_fuerza_a_watt = 745.7
potencia_maxima_hp = 950.0
potencia_maxima = potencia_maxima_hp * caballo_de_fuerza_a_watt  # W

longitud_recta = 640.0               # m
aceleracion_maxima = 6.0 * gravedad

velocidad_limite_inicial = 240.0 * 1000.0 / 3600.0  # 240 km/h
velocidad_limite_final  = 225.0 * 1000.0 / 3600.0   # 225 km/h


def calcular_dinamica(tiempo, estado, acelerador, freno, usar_drs):
    posicion, velocidad = estado

    if velocidad < 0.0:
        velocidad = 0.0

    coef_arrastre = coef_arrastre_con_drs if usar_drs else coef_arrastre_sin_drs


    fuerza_normal = masa * gravedad + 0.5 * densidad_aire * coef_downforce * area_frontal * velocidad**2

    fuerza_adherencia = coef_rozamiento_neumaticos * fuerza_normal

    fuerza_arrastre = 0.5 * densidad_aire * coef_arrastre * area_frontal * velocidad**2

    eps = 1e-3
    velocidad_segura = max(velocidad, eps)
    fuerza_motor_teorica = acelerador * potencia_maxima / velocidad_segura
    fuerza_motor = min(fuerza_motor_teorica, fuerza_adherencia)

    fuerza_frenado = freno * fuerza_adherencia

    aceleracion = (fuerza_motor - fuerza_arrastre - fuerza_frenado) / masa

    if abs(aceleracion) > aceleracion_maxima:
        aceleracion = math.copysign(aceleracion_maxima, aceleracion)

    return np.array([velocidad, aceleracion], dtype=float)
