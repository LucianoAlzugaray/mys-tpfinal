from datetime import datetime

from models.TipoPizza import TipoPizza


class Configuracion:
    PIZZAS_POR_HORNO = 40
    PEDIDOS_POR_HORA = 20
    HORNOS_POR_CAMIONETA = 1
    CANTIDAD_DE_CAMIONETAS = 4
    VOLVER_AL_RESTAURANTE = False
    CANTIDAD_DE_EXPERIMENTOS = 10
    FIN = datetime.strptime('31/12/20 23:00:00', '%d/%m/%y %H:%M:%S')
    INICIO = datetime.strptime('1/1/20 11:00:00', '%d/%m/%y %H:%M:%S')
    TIPOS_PIZZA_DISPONIBLES = [TipoPizza.ANANA, TipoPizza.CALABRESA, TipoPizza.FUGAZZETA, TipoPizza.MOZZARELLA, TipoPizza.NAPOLITANA]

    @classmethod
    def get_default_configuration(cls):
        return {
            "inicio": cls.INICIO,
            "fin": cls.FIN,
            "volverAlRestaurante": cls.VOLVER_AL_RESTAURANTE,
            "pedidosPorHora": cls.PEDIDOS_POR_HORA,
            "hornosPorCamioneta": cls.HORNOS_POR_CAMIONETA,
            "pizzasPorHorno": cls.PIZZAS_POR_HORNO,
            "cantidadCamionetas": cls.CANTIDAD_DE_CAMIONETAS,
            "cantidadExperimentos": cls.CANTIDAD_DE_EXPERIMENTOS,
            "tipos_de_pizza": cls.TIPOS_PIZZA_DISPONIBLES
        }
