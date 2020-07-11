from datetime import timedelta, time, datetime


class Reloj(object):

    def __init__(self):
        self.termino_dia = False

    def configurate(self, kwargs):
        self.dia = kwargs['dia']
        self.cirre_at = kwargs['hora_cierre']


    def avanzar(self, minutos):
        self.dia = self.dia + timedelta(minutes=minutos)

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
        self.dia = time
        # diferencia_en_minutos = self.get_diferencia_hora_actual(time)
        # self.avanzar(diferencia_en_minutos)

    def terminar_el_dia(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        dia = datetime(year=self.dia.year,
                       month=self.dia.month,
                       day=self.dia.day,
                       hour=simulacion.tiempo_inicio.hour,
                       minute=simulacion.tiempo_inicio.minute,
                       second=0)
        self.avanzar_time(dia + timedelta(days=1))
        self.termino_dia = True

    def iniciar_dia(self):
        self.termino_dia = False

    @property
    def dias_transcurridos(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        return (self.dia - simulacion.tiempo_inicio).days + 1