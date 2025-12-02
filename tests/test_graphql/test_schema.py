import pytest
from graphql_api.schema import schema

@pytest.mark.django_db
def test_schema_loads():
    """Test GraphQL schema ."""
    assert schema is not None
    schema_str = str(schema)
    assert "Query" in schema_str
    assert "Mutation" in schema_str

