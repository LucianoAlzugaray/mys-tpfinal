class SimulacionEvent(object):

    def __init__(self, hora):
        self.actividades = []
        self.hora = hora

    def attach(self, actividad):
        self.actividades.append(actividad)
        return self

    def detach(self, actividad) -> None:
        self.actividades.remove(actividad)

    def notify(self) -> None:
        for actividad in self.actividades:
            actividad.run(self)

    def to_dict(self):
        return {
            "id": id(self),
            "tipo": self.__class__,
            "ubicacion": "" if not hasattr(self,'ubicacion') else self.ubicacion,
            "hora": self.hora
        }