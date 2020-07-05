from datetime import datetime, timedelta


class Reloj(object):

    def __init__(self):
        self.dia = None
        from Simulacion import Simulacion
        self.hora_cierre = Simulacion.HORA_DE_CIERRE
        self.minutos_cierre = Simulacion.MINUTOS_DE_CIERRE
        self.hora_fin_toma_de_pedidos = Simulacion.HORA_FIN_TOMA_DE_PEDIDOS
        self.minuto_fin_toma_de_pedidos = Simulacion.MINUTOS_FIN_TOMA_DE_PEDIDOS

    def iniciar_dia(self):
        self.dia = datetime.now()

    def avanzar(self, minutos):
        self.dia = self.dia + timedelta(minutes=minutos)

    def termino_dia(self):
        dt_fin_de_dia = datetime.now()
        dt_fin_de_dia = dt_fin_de_dia.replace(year=dt_fin_de_dia.year,
                                              month=dt_fin_de_dia.month,
                                              day=dt_fin_de_dia.day,
                                              hour=self.hora_cierre,
                                              minute=self.minutos_cierre,
                                              second=0)
        return self.dia > dt_fin_de_dia

    def termino_horario_de_toma_de_pedido(self):
        dt_fin_horario_de_toma_de_pedido = datetime.now()
        dt_fin_horario_de_toma_de_pedido = dt_fin_horario_de_toma_de_pedido.replace(
            year=dt_fin_horario_de_toma_de_pedido.year,
            month=dt_fin_horario_de_toma_de_pedido.month,
            day=dt_fin_horario_de_toma_de_pedido.day,
            hour=self.hora_fin_toma_de_pedidos,
            minute=self.minuto_fin_toma_de_pedidos,
            second=0)

        return self.dia > dt_fin_horario_de_toma_de_pedido

    def get_diferencia_hora_actual(self, dt_hora):
        horas_parametro = dt_hora.hour
        horas_reloj = self.dia.hour
        minutos_por_hora_parametro = horas_parametro * 60
        minutos_por_hora_reloj = horas_reloj * 60
        return abs((self.dia.minute + minutos_por_hora_reloj) - (dt_hora.minute + minutos_por_hora_parametro))
