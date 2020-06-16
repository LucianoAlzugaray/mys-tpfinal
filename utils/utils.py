import numpy as np
import math
import random

## Obtiene una velocidad probabilistica para cargar pizzas
def velocidad_carga_pizza():
    return np.random.exponential(1 / 10)


## Obtiene un tiempo de entrega probabilistico
def tiempo_entrega():
    return np.random.exponential(1 / 10)


## Obtiene si se convenció al cliente o no de cambiar el tipo de pizza
def cliente_convencido():
    return np.random.binomial(1, 0.3) == 1


## Obtiene pedidos generados en una hora
def pedidos_generados():
    return np.random.poisson(20)


## Obtiene el minuto  de un pedido en una hora
def pedido_en_hora():
    return math.trunc(random.uniform(0, 60))


## Genera tipo de pizza aleatorio
## TODO : pizzas_no_disponibles ? cuando no existe pizza en ninguna camioneta
## se tiene que asegurar que la nueva pizza no sea la misma que ya pidio
def generar_tipo_de_pizza():
    opcion = random.random()
    if (opcion < 0.05):
        return 'anana'
    elif (opcion < 0.20):
        return 'calabresa'
    elif (opcion < 0.55):
        return 'mozzarella'
    elif (opcion < 0.75):
        return 'fugazzeta'
    else:
        return 'napolitana'


## Obtiene una ubicación del cliente aleatoria
def generar_ubicacion_cliente():
    ubicacion = np.random.normal(0, 10, 2)
    return ubicacion * 100  ##Para que quede como maximo 2000 como en el gráfico de bruno