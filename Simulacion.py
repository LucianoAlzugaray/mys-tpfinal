from models.Dia import Dia

class Simulacion:
    experimentos = 10
    dias_a_simular = 365
    horas_por_dia = 12
    minutos_maximo = 60 * horas_por_dia
    dias_corridos=[]
    cantidad_camionetas = 4

    def correr_simulacion(self):
        #Correr simulacion
        for experimento in range(self.experimentos):
            #por cada dia, generar un nuevo objeto dia y correrlo
            for dia in range(self.dias_a_simular):
                nuevo_dia = Dia(minutos_maximo, self.cantidad_camionetas)
                nuevo_dia.correr()
            #  guarda el dia en una lista de dias corridos.
            self.dias_corridos.append(nuevo_dia)

    def obtener_datos(self):
        # Obtener datos finales
        # retorna datos en np array o como sea
        pass
