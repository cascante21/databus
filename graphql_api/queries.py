import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AgencyType, RouteType, StopType, TripType, StopTimeType
from gtfs import models

def check_auth(info: Info):
    if not info.context.request.user.is_authenticated:
        raise Exception("Authentication required")

@strawberry.type
class Query:
    @strawberry.field
    def all_agencies(self, info: Info, name_contains: Optional[str] = None) -> List[AgencyType]:
        check_auth(info)
        queryset = models.Agency.objects.all()
        if name_contains:
            queryset = queryset.filter(agency_name__icontains=name_contains)
        return queryset.order_by('agency_name')

    @strawberry.field
    def agency(self, info: Info, id: strawberry.ID) -> Optional[AgencyType]:
        check_auth(info)
        return models.Agency.objects.filter(pk=id).first()

    @strawberry.field
    def all_routes(self, info: Info, limit: int = 10, offset: int = 0, route_type: Optional[int] = None) -> List[RouteType]:
        check_auth(info)
        queryset = models.Route.objects.all()
        if route_type is not None:
            queryset = queryset.filter(route_type=route_type)
        return queryset.order_by('route_sort_order', 'route_id')[offset:offset+limit]

    @strawberry.field
    def all_stops(self, info: Info, limit: int = 10, offset: int = 0, name_contains: Optional[str] = None) -> List[StopType]:
        check_auth(info)
        queryset = models.Stop.objects.all()
        if name_contains:
            queryset = queryset.filter(stop_name__icontains=name_contains)
        return queryset.order_by('stop_name')[offset:offset+limit]

    @strawberry.field
    def trips_by_route(self, info: Info, route_id: str) -> List[TripType]:
        check_auth(info)
        return models.Trip.objects.filter(route_id=route_id)

    @strawberry.field
    def stop_times_by_trip(self, info: Info, trip_id: str) -> List[StopTimeType]:
        check_auth(info)
        return models.StopTime.objects.filter(trip_id=trip_id).order_by('stop_sequence')
