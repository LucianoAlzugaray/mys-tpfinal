from datetime import timedelta, time, datetime


class Reloj(object):

    def __init__(self):
        from Simulacion import Simulacion
        self.dia = Simulacion().tiempo_inicio
        self.cirre_at = time(Simulacion.HORA_DE_CIERRE, Simulacion.MINUTOS_DE_CIERRE)
        self.finaliza_toma_pedidos_at = time(Simulacion.HORA_FIN_TOMA_DE_PEDIDOS,
                                             Simulacion.MINUTOS_FIN_TOMA_DE_PEDIDOS)

    def avanzar(self, minutos):
        self.dia = self.dia + timedelta(minutes=minutos)

    def termino_dia(self):
        return self.dia.time() >= self.cirre_at

    def termino_horario_de_toma_de_pedido(self):
        return self.dia.time() >= self.finaliza_toma_pedidos_at

    ''' Recibe una fecha y hora (datetime) y devuevle la diferencia en minutos con la hora actual.'''
    def get_diferencia_hora_actual(self, dt_hora):
        horas_parametro = dt_hora.hour
        horas_reloj = self.dia.hour
        minutos_por_hora_parametro = horas_parametro * 60
        minutos_por_hora_reloj = horas_reloj * 60
        return abs((self.dia.minute + minutos_por_hora_reloj) - (dt_hora.minute + minutos_por_hora_parametro))

    '''Dada una cantidad de minutos devuelve el datetime de ese momento.'''
    def obtener_dt_futuro(self, minutos):
        return self.dia + timedelta(minutes=minutos)

    '''Avanza el reloj hasta un datetime recibido por parametro'''
    def avanzar_time(self, time: datetime):
        diferencia_en_minutos = self.get_diferencia_hora_actual(time)
        self.avanzar(diferencia_en_minutos)