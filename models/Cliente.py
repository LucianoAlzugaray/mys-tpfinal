
class Cliente:

    def __init__(self):
        from Simulacion import Simulacion
        self.ubicacion = Simulacion().utils.generar_ubicacion_cliente()

    def to_dict(self):
        return {
            "id": id(self),
            "ubicacion": self.ubicacion
        }