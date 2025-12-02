import strawberry
from strawberry import auto
from typing import List, Optional
from gtfs import models

@strawberry.django.type(models.Agency)
class AgencyType:
    id: auto
    agency_id: auto
    agency_name: auto
    agency_url: auto
    agency_timezone: auto
    agency_lang: auto
    agency_phone: auto
    agency_fare_url: auto
    agency_email: auto

@strawberry.django.type(models.Route)
class RouteType:
    id: auto
    route_id: auto
    agency_id: auto
    route_short_name: auto
    route_long_name: auto
    route_desc: auto
    route_type: auto
    route_url: auto
    route_color: auto
    route_text_color: auto
    route_sort_order: auto

@strawberry.django.type(models.Stop)
class StopType:
    id: auto
    stop_id: auto
    stop_code: auto
    stop_name: auto
    stop_desc: auto
    stop_lat: auto
    stop_lon: auto
    zone_id: auto
    stop_url: auto
    location_type: auto
    parent_station: auto
    stop_timezone: auto
    wheelchair_boarding: auto
    platform_code: auto

@strawberry.django.type(models.Trip)
class TripType:
    id: auto
    trip_id: auto
    route_id: auto
    service_id: auto
    trip_headsign: auto
    trip_short_name: auto
    direction_id: auto
    block_id: auto
    shape_id: auto
    wheelchair_accessible: auto
    bikes_allowed: auto

@strawberry.django.type(models.StopTime)
class StopTimeType:
    id: auto
    trip_id: auto
    arrival_time: auto
    departure_time: auto
    stop_id: auto
    stop_sequence: auto
    stop_headsign: auto
    pickup_type: auto
    drop_off_type: auto
    shape_dist_traveled: auto
    timepoint: auto
