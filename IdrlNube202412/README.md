# Proyecto API REST - FLASk (IDRL Grupo:)
Este proyecto genera las api para el manejo del proyecto IDRL

- Version: 1.0.0

# Ejecución

En una terminal ejecutar:

`cd IdrlNube202412`

Luego ejecutar `docker-compose` de la siguiente manera:

`docker-compose up --build`

## Consumir los servicios
* Utilice postman para consumir los servicios habilitados

* Ruta EndPoint 1 Registro usuarios [POST]:         ```http://localhost:8080/auth/signup```
* Ruta EndPoint 2 Autenticacion[POST]: [POST]:      ```http://localhost:8080/auth/login```
* Ruta EndPoint 3 Retorna tareas por Usr aut [GET]: ```http://localhost:8080/api/task```
* Ruta EndPoint 4 Creacion de tareas [POST]:        ```http://localhost:8080/api/task```
* Ruta EndPoint 5 Retorno de tarea por Id [GET]:    ```http://localhost:8080/api/task/1```
