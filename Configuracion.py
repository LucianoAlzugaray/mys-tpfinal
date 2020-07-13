from datetime import datetime

from models.TipoPizza import TipoPizza


class Configuracion:
    PIZZAS_POR_HORNO = 5
    PEDIDOS_POR_HORA = 20
    HORNOS_POR_CAMIONETA = 1
    CANTIDAD_DE_CAMIONETAS = 40
    VOLVER_AL_RESTAURANTE = False
    CANTIDAD_DE_EXPERIMENTOS = 1
    FIN = datetime.strptime('1/2/20 23:00:00', '%d/%m/%y %H:%M:%S')
    INICIO = datetime.strptime('1/1/20 11:00:00', '%d/%m/%y %H:%M:%S')
    TIPOS_PIZZA_DISPONIBLES = [
        {'tipo': TipoPizza.ANANA, 'probabilidad': 0.05},
        {'tipo': TipoPizza.CALABRESA, 'probabilidad': 0.20},
        {'tipo': TipoPizza.NAPOLITANA, 'probabilidad': 0.55},
        {'tipo': TipoPizza.FUGAZZETA, 'probabilidad': 0.75},
        {'tipo': TipoPizza.MOZZARELLA, 'probabilidad': 1}
    ]

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
