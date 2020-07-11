
class Cliente:

    def __init__(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.ubicacion = simulacion.utils.generar_ubicacion_cliente()
