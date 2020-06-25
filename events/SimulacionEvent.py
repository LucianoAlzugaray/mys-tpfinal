class SimulacionEvent(object):

    def __init__(self, hora):
        self.actividades = []
        self.hora = hora

    def attach(self, actividad) -> None:
        self.actividades.append(actividad)

    def detach(self, actividad) -> None:
        self.actividades.remove(actividad)

    def notify(self) -> None:
        for actividad in self.actividades:
            actividad.run(self)
