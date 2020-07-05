from datetime import datetime, timedelta, time


class Reloj(object):

    def __init__(self):
        from Simulacion import Simulacion
        self.dia = Simulacion.TIEMPO_INICIO
        self.cirre_at = time(Simulacion.HORA_DE_CIERRE, Simulacion.MINUTOS_DE_CIERRE)
        self.finaliza_toma_pedidos_at = time(Simulacion.HORA_FIN_TOMA_DE_PEDIDOS,
                                             Simulacion.MINUTOS_FIN_TOMA_DE_PEDIDOS)

    def avanzar(self, minutos):
        self.dia = self.dia + timedelta(minutes=minutos)

    def termino_dia(self):
        return self.dia.time() >= self.cirre_at

    def termino_horario_de_toma_de_pedido(self):
        return self.dia.time() >= self.finaliza_toma_pedidos_at

    def get_diferencia_hora_actual(self, dt_hora):
        horas_parametro = dt_hora.hour
        horas_reloj = self.dia.hour
        minutos_por_hora_parametro = horas_parametro * 60
        minutos_por_hora_reloj = horas_reloj * 60
        return abs((self.dia.minute + minutos_por_hora_reloj) - (dt_hora.minute + minutos_por_hora_parametro))

    def obtener_dt_futuro(self, minutos):
        return self.dia + timedelta(minutes=minutos)