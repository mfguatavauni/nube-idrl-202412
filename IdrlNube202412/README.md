# Proyecto API REST - FLASk (IDRL Grupo:)
Este proyecto genera las api para el manejo del proyecto IDRL


# Ejecución
Favor realizar las siguientes instrucciones:


## Crear el ambiente virtual 
* ```$ python3 -m venv mi-emv```
* ```$ source mi-emv/bin/activate```

## Instalar las dependencias
* ```$ pip install flask``` 
* ```$ pip install flask-restful```
* ```$ pip install flask-marshmallow```
* ```$ pip install flask-jwt-extended```

## Configurar variables de entorno
* ```$ export FLASK_APP=app.py```
* ```$ export FLASK_DEBUG=1```
* ```$ export FLASK_ENV=development```
* pip install flask-cors
* pip install sqlalchemy
* pip install marshmallow-sqlalchemy
* pip install flask_sqlalchemy
* pip install sqlalchemy psycopg2-binary
* pip install Flask-Script
* pip install flask-migrate

## Establecer el repositorio de POSTGRES para obtener la direccion/puerto/usuario/clave

## Validar que la base de datos exista, si no es necesario crearla Manualmente no es necesario tener las tablas solamente la BD
* ```CREATE DATABASE idrl;```

## Realizar el ajuste para conectarse a POSTGRES
* Ubicar en el archivo app.py ```app.config["SQLALCHEMY_DATABASE_URI"]``` y realizar el cambio a los valores de conexion de su base de datos postgres


## Ejecutar
* ```$ python3 app.py```

## Consumir los servicios
* Utilice postman para consumir los servicios habilitados

* Ruta EndPoint 1 Registro usuarios [POST]:         ```http://172.27.208.123:8080/auth/signup```
* Ruta EndPoint 2 Autenticacion[POST]: [POST]:      ```http://172.27.208.123:8080/auth/login```
* Ruta EndPoint 3 Retorna tareas por Usr aut [GET]: ```http://172.27.208.123:8080/api/task```
* Ruta EndPoint 4 Creacion de tareas [POST]:        ```http://172.27.208.123:8080/api/task```
* Ruta EndPoint 5 Retorno de tarea por Id [GET]:    ```http://172.27.208.123:8080/api/task/1```
