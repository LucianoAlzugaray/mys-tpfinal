from events.SimulacionEvent import SimulacionEvent


class CamionetaRegresaARestauranteEvent(SimulacionEvent):

    def __init__(self, camioneta, time):
        super().__init__(time)
        self.camioneta = camioneta