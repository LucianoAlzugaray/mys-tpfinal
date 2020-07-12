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