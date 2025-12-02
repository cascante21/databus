import pytest
from django.test import Client
from django.contrib.auth.models import User
from gtfs.models import Agency, Feed, Route, Stop
import json

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def feed(db):
    return Feed.objects.create(feed_id="feed-1")

@pytest.fixture
def agency(db, feed):
    return Agency.objects.create(
        feed=feed,
        agency_id="agency-1",
        agency_name="Test Agency",
        agency_url="http://example.com",
        agency_timezone="UTC"
    )

@pytest.fixture
def route(db, feed, agency):
    return Route.objects.create(
        feed=feed,
        route_id="route-1",
        agency_id="agency-1",
        route_short_name="R1",
        route_long_name="Route 1",
        route_type=3
    )

@pytest.fixture
def stop(db, feed):
    return Stop.objects.create(
        feed=feed,
        stop_id="stop-1",
        stop_name="Test Stop",
        stop_lat=9.9,
        stop_lon=-84.1
    )

@pytest.mark.django_db
def test_query_requires_auth(client):
    query = """
        query {
            allAgencies {
                agencyName
            }
        }
    """
    response = client.post(
        '/graphql/',
        {'query': query},
        content_type='application/json'
    )
    data = json.loads(response.content)
    assert 'errors' in data
    assert 'Authentication required' in str(data['errors'])

@pytest.mark.django_db
def test_all_agencies_query(client, user, agency):
    client.force_login(user)
    query = """
        query {
            allAgencies {
                agencyName
            }
        }
    """
    response = client.post(
        '/graphql/',
        json.dumps({'query': query}),
        content_type='application/json'
    )
    data = json.loads(response.content)
    
    assert 'errors' not in data
    assert len(data['data']['allAgencies']) == 1
    assert data['data']['allAgencies'][0]['agencyName'] == "Test Agency"

@pytest.mark.django_db
def test_agencies_filter(client, user, feed):
    client.force_login(user)
    Agency.objects.create(
        feed=feed,
        agency_id="agency-2",
        agency_name="Bus Company",
        agency_url="http://bus.com",
        agency_timezone="UTC"
    )
    Agency.objects.create(
        feed=feed,
        agency_id="agency-3",
        agency_name="Train Company",
        agency_url="http://train.com",
        agency_timezone="UTC"
    )
    
    query = """
        query {
            allAgencies(nameContains: "Bus") {
                agencyName
            }
        }
    """
    response = client.post(
        '/graphql/',
        json.dumps({'query': query}),
        content_type='application/json'
    )
    data = json.loads(response.content)
    
    assert 'errors' not in data
    assert len(data['data']['allAgencies']) == 1
    assert data['data']['allAgencies'][0]['agencyName'] == "Bus Company"

@pytest.mark.django_db
def test_routes_pagination(client, user, feed, agency):
    for i in range(15):
        Route.objects.create(
            feed=feed,
            route_id=f"route-{i}",
            agency_id="agency-1",
            route_short_name=f"R{i}",
            route_long_name=f"Route {i}",
            route_type=3
        )
    
    client.force_login(user)
    query = """
        query {
            allRoutes(limit: 5, offset: 0) {
                routeShortName
            }
        }
    """
    response = client.post(
        '/graphql/',
        json.dumps({'query': query}),
        content_type='application/json'
    )
    data = json.loads(response.content)
    
    assert 'errors' not in data
    assert len(data['data']['allRoutes']) == 5
