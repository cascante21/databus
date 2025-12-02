import strawberry
from strawberry.types import Info
from django.core.exceptions import ValidationError
from gtfs.models import Agency, Feed
from .types import AgencyType

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_agency(
        self,
        info: Info,
        feed_id: str,
        agency_id: str,
        name: str,
        url: str,
        timezone: str,
        lang: str = "es"
    ) -> AgencyType:
        user = info.context.request.user
        if not user.is_authenticated or not (user.is_staff or user.has_perm('gtfs.add_agency')):
            raise Exception("No autorizado")

        try:
            feed = Feed.objects.get(feed_id=feed_id)
        except Feed.DoesNotExist:
            raise Exception(f"Feed {feed_id} no existe")

        agency = Agency(
            feed=feed,
            agency_id=agency_id,
            agency_name=name,
            agency_url=url,
            agency_timezone=timezone,
            agency_lang=lang
        )
        try:
            agency.full_clean()
            agency.save()
        except ValidationError as e:
            raise Exception(str(e))
            
        return agency
