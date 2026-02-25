from dinamica import longitud_recta, velocidad_limite_final, velocidad_limite_inicial, gravedad

def crear_controlador(factor_inicio_drs, factor_fin_drs, desaceleracion_max_frenado_g):
    desaceleracion_max_frenado = desaceleracion_max_frenado_g * gravedad
    posicion_inicio_drs = factor_inicio_drs * longitud_recta
    posicion_fin_drs = factor_fin_drs * longitud_recta

    # Velocidad objetivo un poco menor que el límite final para tener margen
    margen_seguridad_kmh = 10.0
    velocidad_objetivo_frenado = velocidad_limite_final - margen_seguridad_kmh * 1000.0 / 3600.0

    def controlador(tiempo, posicion, velocidad):
        usar_drs = posicion_inicio_drs <= posicion <= posicion_fin_drs

        distancia_restante = longitud_recta - posicion

        acelerador = 1.0
        freno = 0.0

        if velocidad < 1.0:
            return 1.0, 0.0, usar_drs

        if velocidad > velocidad_limite_inicial:
            acelerador = 0.5

        if velocidad > velocidad_objetivo_frenado:
            distancia_frenado_necesaria = (
                    (velocidad**2 - velocidad_objetivo_frenado**2)
                    / (2.0 * desaceleracion_max_frenado)
            )
        else:
            distancia_frenado_necesaria = 0.0

        if distancia_restante <= distancia_frenado_necesaria * 1.05:
            acelerador = 0.0
            freno = 1.0

        return acelerador, freno, usar_drs

    return controlador
