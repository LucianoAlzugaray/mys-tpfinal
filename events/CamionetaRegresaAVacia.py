from .SimulacionEvent import SimulacionEvent


class CamionetaRegresaVaciaEvent(SimulacionEvent):

    def __init__(self, camioneta, hora):
        super().__init__(hora)
        self.camioneta = camioneta
        self.pedido = None

