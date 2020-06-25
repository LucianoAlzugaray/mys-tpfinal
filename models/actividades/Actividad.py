from abc import ABCMeta, abstractmethod
from events.SimulacionEvent import SimulacionEvent


class Actividad(metaclass=ABCMeta):

    def run(self, evento: SimulacionEvent):
        self._ejecutar(evento)

    @abstractmethod
    def _ejecutar(self, evento):
        pass
