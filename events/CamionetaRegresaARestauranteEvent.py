from events.SimulacionEvent import SimulacionEvent


class CamionetaRegresaARestauranteEvent(SimulacionEvent):

    def __init__(self, camioneta, hora):
        super().__init__(hora)
        self.camioneta = camioneta
