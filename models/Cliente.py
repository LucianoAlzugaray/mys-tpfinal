
class Cliente:

    def __init__(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.ubicacion = simulacion.utils.generar_ubicacion_cliente()

    def to_dict(self):
        return {
            "id": id(self),
            "ubicacion": self.ubicacion
        }