import pytest
from django.test import Client
from django.contrib.auth.models import User
from gtfs.models import Feed
import json

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="password", is_staff=True)

@pytest.fixture
def normal_user(db):
    return User.objects.create_user(username="user", password="password")

@pytest.fixture
def feed(db):
    return Feed.objects.create(feed_id="feed-1")

@pytest.mark.django_db
def test_create_agency_mutation(client, staff_user, feed):
    client.force_login(staff_user)
    mutation = """
        mutation {
            createAgency(
                feedId: "feed-1",
                agencyId: "new-agency",
                name: "New Agency",
                url: "http://new.com",
                timezone: "UTC"
            ) {
                agencyName
            }
        }
    """
    response = client.post(
        '/graphql/',
        json.dumps({'query': mutation}),
        content_type='application/json'
    )
    data = json.loads(response.content)
    
    assert 'errors' not in data
    assert data['data']['createAgency']['agencyName'] == "New Agency"

@pytest.mark.django_db
def test_create_agency_permission_denied(client, normal_user, feed):
    client.force_login(normal_user)
    mutation = """
        mutation {
            createAgency(
                feedId: "feed-1",
                agencyId: "new-agency",
                name: "New Agency",
                url: "http://new.com",
                timezone: "UTC"
            ) {
                agencyName
            }
        }
    """
    response = client.post(
        '/graphql/',
        json.dumps({'query': mutation}),
        content_type='application/json'
    )
    data = json.loads(response.content)
    
    assert 'errors' in data
    assert "No autorizado" in str(data['errors'])
