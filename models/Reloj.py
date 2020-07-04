from datetime import datetime, timedelta
from dateutil.parser import parse

class Reloj(object):

    def __init__(self,hora_cierre, minutos_cierre, hora_fin_toma_de_pedidos,minuto_fin_toma_de_pedidos):
        self.dia = None
        self.hora_cierre = hora_cierre
        self.minutos_cierre = minutos_cierre
        self.hora_fin_toma_de_pedidos = hora_fin_toma_de_pedidos
        self.minuto_fin_toma_de_pedidos = minuto_fin_toma_de_pedidos

    def iniciar_dia(self):
        self.dia = datetime.now()

    def avanzar(self, minutos):
        self.dia = self.dia + timedelta(minutes=minutos)

    def termino_dia(self):
        if ((self.dia.minute >= self.minutos_cierre) or (self.dia.hour > self.hora_cierre) and (
                self.dia.hour == self.hora_cierre)):
            return True
        return False

    def termino_horario_de_toma_de_pedido(self):
        if ((self.dia.minute >= self.minuto_fin_toma_de_pedidos) or (self.dia.hour > self.hora_fin_toma_de_pedidos)
                and (self.dia.hour == self.hora_fin_toma_de_pedidos)):
            return True
        return False

    def get_diferencia_hora_actual(self, dt_hora):
     horas_parametro = dt_hora.hour
     horas_reloj = self.dia.hour
     minutos_por_hora_parametro = horas_parametro*60
     minutos_por_hora_reloj = horas_reloj*60
     return abs((self.dia.minute + minutos_por_hora_reloj) - (dt_hora.minute + minutos_por_hora_parametro))