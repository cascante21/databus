# Implementación - API GraphQL


### 1. Configuración del esquema
-   Instalado strawberry-graphql-django
-   Agregado a INSTALLED_APPS en settings.py
-   Creada aplicación Django `graphql`
-   Esquema raíz con Query y Mutation en `graphql/schema.py`
-   Endpoint `/graphql/` agregado en urls.py

### 2. Tipos GraphQL
Archivo: `graphql/types.py`
-   AgencyType
-   RouteType
-   StopType
-   TripType
-   StopTimeType

### 3. Consultas
Archivo: `graphql/queries.py`
-   allAgencies (con filtro nameContains)
-   agency(id)
-   allRoutes (con paginación y filtro routeType)
-   allStops (con paginación y filtro nameContains)
-   tripsByRoute(routeId)
-   stopTimesByTrip(tripId)

Características:
-   Filtración implementada
-   Ordenamiento implementado
-   Paginación estilo offset (limit/offset)

### 4. Mutaciones
Archivo: `graphql/mutations.py`
-   createAgency con validación
-   Retorna objeto creado
-   Manejo de errores de validación

### 5. Autenticación y Permisos
-   Autenticación requerida para todas las consultas
-   Autenticación requerida para todas las mutaciones
-   Permisos de staff verificados para mutaciones
-   Respuestas de error 

### 6. Documentación
Archivo: `docs/graphql.md`
-   Ejecución del endpoint
-   Ejemplos de consultas
-   Ejemplos de mutaciones
-   Autenticación
-   Cómo ampliar el esquema
-   Instrucciones de pruebas

### 7. Pruebas
Directorio: `tests/test_graphql/`

#### test_schema.py
-   Esquema se carga correctamente

#### test_queries.py
-   Obtención de objetos
-   Paginación
-   Filtración
-   Casos autorizados y no autorizados

#### test_mutations.py
-   Mutación exitosa
-   Errores de validación
-   Cumplimiento de permisos

#### test_permissions.py
-   Usuarios anónimos bloqueados

## Archivos Creados/Modificados

### Nuevos archivos:
1. graphql/__init__.py
2. graphql/apps.py
3. graphql/types.py
4. graphql/queries.py
5. graphql/mutations.py
6. graphql/schema.py
7. tests/test_graphql/__init__.py
8. tests/test_graphql/test_schema.py
9. tests/test_graphql/test_queries.py
10. tests/test_graphql/test_mutations.py
11. tests/test_graphql/test_permissions.py
12. docs/graphql.md

### Archivos modificados:
1. requirements.txt (agregado strawberry-graphql-django)
2. realtime/settings.py (agregado graphql y strawberry.django a INSTALLED_APPS)
3. realtime/urls.py (agregado endpoint /graphql/)

## Notas

- Permisos: Staff o gtfs.add_agency para mutaciones
