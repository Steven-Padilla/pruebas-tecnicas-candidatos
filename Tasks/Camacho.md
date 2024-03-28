# Prueba técnica - Desarrollo backend con Python usando Flask

**Fecha:** 2024-03-28

**Duración:** Sin límite de tiempo 

**Herramientas/Tecnologías:**

* Flask
* Python

## Descripción

El tarea consiste en desarrollar una API RESTful que permita a los usuarios gestionar la información del cliente. La API debe tener las siguientes funcionalidades:

1. Registro de usuarios nuevos y ya existentes.
2. Edición de usuarios.
3. Listar a todos los usuarios

**SOLO USAR PETICIONES GET Y POST (segun se requiera)**

## Instrucciones para la prueba

- Crear el archivo "Route" dentro de `src/routes` siguiendo la estructura de [/src/routes/CourtRoutes.py](../src/routes/CourtRoutes.py)
- Crear el archivo "Service" dentro de `src/services` siguiendo la estructura de [/src/services/CourtService.py](../src/services/CourtService.py)
- Crear el endpoint en el archivo [src/\_\_init\_\_.py](../src/__init__.py) siguiendo los ejemplos dentro de este mismo archivo

### Proceso para consultar información del usuario

```mermaid
graph TD;
    A(Buscar ID en bdgpXXX.usuarios) --> B(Obtener ID);
    B --> C(Buscar ID en bdcentral.usuarios_central);
    C --> D(Obtener información del usuario solo si tiene estatus 'activo');
```

### Proceso para registrar información del usuario

```mermaid
graph TD;
    A(Buscar celular en bdcentral.usuarios_central) --> |Celular encontrado| B[Obtener ID del usuario];
    B --> |ID obtenido| C(Buscar ID en bdgpXXX.usuarios);
    C --> |ID encontrado| D("Retornar 'Este usuario ya esta registrado'");
    C --> |ID no encontrado| E(Crear registro en bdgpXXX.usuarios);
    E --> F[Crear la relacion en bdcentral.usuarios_empresa];
    F --> H[Retornar la información del nuevo usuario]
    A --> |Celular no encontrado| G(Ingresar información en bdcentral.usuarios_central);
    G --> E

```
