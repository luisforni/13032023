# Prueba técnica t2ó

La tarea consiste en hacer una aplicación que lee datos de una API externa, los almacena y expone información sobre estos datos a través de una API REST.

En este caso vamos a leer los datos de la API de Blockchain.com cuya documentación está disponible aquí: https://api.blockchain.com/v3/

Concretamente leeremos los datos de la llamada GET /l3/{symbol}.

```
git clone https://github.com/luisforni/13032023.git
pip install -r requirements.txt
cd prueba_tecnica
```

Editar `DATABASES` en `prueba_tecnica/settings.py`.

ej. 1 
```
python main.py BTC-USD
```
ej 2, 3 y 4

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Abrir en el navegador `http://127.0.0.1:8000/`

Ej 2: `http://127.0.0.1:8000/estadisticas-compras/?symbol=BTC-USD`

Ej 3: `http://127.0.0.1:8000/estadisticas-ventas/?symbol=BTC-USD`

Ej 4: `http://127.0.0.1:8000/estadisticas-generales/`

## Funcionalidades


### 1. Carga de datos

Un usuario con la aplicación instalada debe poder ejecutar un comando indicando un símbolo compuesto de una criptomoneda y una moneda real (e.g. "BTC-USD") y el sistema debe cargar las órdenes L3 en su base de datos.


### 2. Estadísticas de compras

Como usuario con la aplicación ejecutada, debo poder visitar una URL y obtener las siguientes estadísticas de las órdenes de compra (bids) de un símbolo:

-El valor medio de las órdenes, donde el valor es la cantidad de la orden multiplicado por su precio.

-La orden de compra con mayor valor.

-La orden de compra con menor valor.

-El total de monedas en órdenes.


### 3. Estadísticas de ventas

Como usuario con la aplicación ejecutada, debo poder visitar una URL y obtener las mismas estadísticas que antes pero respecto a las órdenes de venta (asks) de un símbolo.


### 4. Estadísticas generales

Como usuario con la aplicación ejecutada, debo poder visitar una URL y obtener las siguientes estadísticas globales de todos los símbolos:

-Número de órdenes de compra.

-Número de órdenes de venta.

-Valor total de las órdenes de compra.

-Valor total de las órdenes de venta.

-El total de monedas de las órdenes de compra.

-El total de monedas de las órdenes de venta.


