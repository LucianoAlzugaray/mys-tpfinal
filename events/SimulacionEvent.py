class SimulacionEvent(object):

    def __init__(self, time):
        self.actividades = []
        self.time = time

    def attach(self, actividad):
        self.actividades.append(actividad)
        return self

    def detach(self, actividad) -> None:
        self.actividades.remove(actividad)

    def notify(self) -> None:
        for actividad in self.actividades:
            actividad.run(self)
