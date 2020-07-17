# Simulación de pizzeria
## Modelos y simulaciones

### Como correr el proyecto
Primero, hay que clonar este repositorio a tu computadora:

```bash
$ git clone https://github.com/LucianoAlzugaray/mys-tpfinal.git
```

Luego, utilizando [docker-compose](https://docs.docker.com/compose/install/), levantaremos los contenedores del dashboard con la siguiente instrucción:

```bash
$ docker-compose up -d
```

La primera vez que ejecutemos el comando anterior, descargará las imágenes de los contenedores necesarios. Cuando los contenedores esten levantados, la aplicación correra en [http://localhost:1880](http://localhost:1880).

El siguiente paso es copiar el contenido de flow.json.

Luego ingresar a http://localhost:1880 -> en Menu hamburguesa (situado en la parte superior derecha)-> Import -> Clipboard y pegar el flow.json copiado anteriormente, por último darle al boton 'Import'.

Una vez realizados estos pasos podrá ver en la segunda pestaña de flows el flow creado para la aplicación.

Luego, deberá clickear el botón "Dashboard" (situado en la parte superior derecha, debajo del menú hamburguesa) y en la pestaña "Theme" debe elegir como "Style" la opción "Dark".

Por último, para ver el dashboard deberá presionar el boton "Deploy"(botón rojo situado en la parte superior derecha, al lado del menú hamburguesa) y clickear el botón que es una ventana con una flecha hacia afuera (botón de nueva ventana) que se visualiza al clickear el boton "dashboard" usado anteriormente. 

Una vez hecho esto deberá abrirse una nueva pestaña en el navegador con el dashboard preparado para comenzar la simulación.


Por último, ejecutamos el servidor de la simulación con el comando

```bash
$ python main.py
```

Una vez levantado el servidor, la simulación correra tocando el botón del dashboard.

 ### Correr los tests
 Para correr los tests, ejecutamos el siguiente comando:
```bash
$ python -m unittest discover tests -p '*Test.py'
```

### Otra forma de correr la simulación.

Otra forma para correr la simulación es ejecutar el test "test_simulacion" situado en el archivo "SimulacionE2ETest.py" (linea 9 de SimulacionE2ETest.py).

#####NOTA: 
Si se ejecuta de este modo los valores de entrada son los definidos en el test y no en el dashboard.

### Forma de seleccionar una nueva estrategia
Para elegir una estrategia por defecto de las creadas deberá cambiar en el "test_simulacion" situado en el archivo "SimulacionE2ETest.py" la linea donde se obtiene la configuracion inicial (linea 14 de SimulacionE2ETest.py).

Las estrategias definidas son:
* get_default_configuration
* get_estrategia_con_menor_cantidad_de_pizzas_cargadas_por_horno
* get_estrategia_con_menor_cantidad_de_pizzas_cargadas_por_horno_y_mas_camionetas

#####Ejemplo
Si desea utilizar la estrategia de "get_estrategia_con_menor_cantidad_de_pizzas_cargadas_por_horno", deberá quedarle la linea 14 de "SimulacionE2ETest.py" de la siguiente forma:

        simulacion.configurate(Configuracion.get_estrategia_con_menor_cantidad_de_pizzas_cargadas_por_horno())
