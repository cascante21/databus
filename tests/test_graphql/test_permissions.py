import pytest
from django.test import Client
from django.contrib.auth.models import User
import json

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_anonymous_user_blocked(client):
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
    
    assert 'errors' in data
    assert "Authentication required" in str(data['errors'])

