from datetime import datetime

from models.TipoPizza import TipoPizza


class Configuracion:
    PIZZAS_POR_HORNO = 20
    PEDIDOS_POR_HORA = 20
    HORNOS_POR_CAMIONETA = 1
    CANTIDAD_DE_CAMIONETAS = 4
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

    @classmethod
    def get_estrategia_con_menor_cantidad_de_pizzas_cargadas_por_horno(cls):
        return {
            "inicio": cls.INICIO,
            "fin": cls.FIN,
            "volverAlRestaurante": cls.VOLVER_AL_RESTAURANTE,
            "pedidosPorHora": cls.PEDIDOS_POR_HORA,
            "hornosPorCamioneta": cls.HORNOS_POR_CAMIONETA,
            "pizzasPorHorno": 10,
            "cantidadCamionetas": cls.CANTIDAD_DE_CAMIONETAS,
            "cantidadExperimentos": cls.CANTIDAD_DE_EXPERIMENTOS,
            "tipos_de_pizza": cls.TIPOS_PIZZA_DISPONIBLES
        }

    @classmethod
    def get_estrategia_con_menor_cantidad_de_pizzas_cargadas_por_horno_y_mas_camionetas(cls):
        return {
            "inicio": cls.INICIO,
            "fin": cls.FIN,
            "volverAlRestaurante": cls.VOLVER_AL_RESTAURANTE,
            "pedidosPorHora": cls.PEDIDOS_POR_HORA,
            "hornosPorCamioneta": cls.HORNOS_POR_CAMIONETA,
            "pizzasPorHorno": 10,
            "cantidadCamionetas": 8,
            "cantidadExperimentos": cls.CANTIDAD_DE_EXPERIMENTOS,
            "tipos_de_pizza": cls.TIPOS_PIZZA_DISPONIBLES
        }

    @classmethod
    def get_estrategia_de_prueba(cls):
        return {
            "inicio": cls.INICIO,
            "fin": datetime.strptime('4/1/20 23:00:00', '%d/%m/%y %H:%M:%S'),
            "volverAlRestaurante": cls.VOLVER_AL_RESTAURANTE,
            "pedidosPorHora": 5,
            "hornosPorCamioneta": cls.HORNOS_POR_CAMIONETA,
            "pizzasPorHorno": 5,
            "cantidadCamionetas": 2,
            "cantidadExperimentos": cls.CANTIDAD_DE_EXPERIMENTOS,
            "tipos_de_pizza": cls.TIPOS_PIZZA_DISPONIBLES
        }
