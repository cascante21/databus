# API GraphQL Databús

## Configuración

La API utiliza `strawberry-graphql-django`.

Endpoint: `/graphql/`

## Ejecución

Para ejecutar el servidor:

```bash
python manage.py runserver
```

Acceda a `/graphql/` para la interfaz GraphiQL.

## Autenticación

Se requiere autenticación para todas las operaciones. Utilice los mecanismos de autenticación de Django (Session, Token o JWT).

Para usar con JWT, incluya el header:
```
Authorization: Bearer <token>
```

## Consultas

### Agencias

Obtener todas las agencias, con filtrado opcional por nombre:

```graphql
query {
  allAgencies(nameContains: "Bus") {
    id
    agencyName
    agencyUrl
    agencyTimezone
  }
}
```

Obtener una agencia por ID:

```graphql
query {
  agency(id: "1") {
    agencyName
    agencyUrl
  }
}
```

### Rutas

Soporta paginación mediante `limit` y `offset`, y filtrado por tipo de ruta:

```graphql
query {
  allRoutes(limit: 20, offset: 0, routeType: 3) {
    routeShortName
    routeLongName
    routeType
  }
}
```

### Paradas

Soporta paginación mediante `limit` y `offset`, y filtrado por nombre:

```graphql
query {
  allStops(limit: 50, offset: 0, nameContains: "Centro") {
    stopName
    stopLat
    stopLon
  }
}
```

### Viajes por Ruta

```graphql
query {
  tripsByRoute(routeId: "route-1") {
    tripId
    tripHeadsign
    directionId
  }
}
```

### Horarios de Parada por Viaje

```graphql
query {
  stopTimesByTrip(tripId: "trip-1") {
    stopSequence
    arrivalTime
    departureTime
  }
}
```

## Mutaciones

### Crear Agencia

Solo personal autorizado o usuarios con el permiso `gtfs.add_agency`.

```graphql
mutation {
  createAgency(
    feedId: "feed-1",
    agencyId: "agency-1",
    name: "Nueva Agencia",
    url: "http://example.com",
    timezone: "America/Costa_Rica",
    lang: "es"
  ) {
    id
    agencyName
  }
}
```

La mutación devuelve el objeto creado o un error de validación si los datos son inválidos.

## Cómo ampliar el esquema

1. Agregar nuevos tipos en `graphql/types.py`
2. Agregar nuevas consultas en `graphql/queries.py`
3. Agregar nuevas mutaciones en `graphql/mutations.py`
4. Actualizar el esquema en `graphql/schema.py` si es necesario

Ejemplo de nuevo tipo:

```python
@strawberry.django.type(models.Calendar)
class CalendarType:
    id: auto
    service_id: auto
    monday: auto
    tuesday: auto
```

## Pruebas

Ejecutar las pruebas:

```bash
pytest tests/test_graphql/
```
