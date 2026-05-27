import pytest
from models import SearchResponse, ObjectResponse, DepartmentsResponse


def test_search(client):
    r = client.search(q="sunflowers")
    assert r.status_code == 200
    data = SearchResponse.model_validate(r.json())
    assert isinstance(data.total, int)


def test_object(client):
    search = client.search(q="sunflowers").json()
    object_id = search["objectIDs"][0]

    r = client.get_object(object_id)
    assert r.status_code == 200

    data = ObjectResponse.model_validate(r.json())
    assert data.objectID == object_id


def test_departments(client):
    r = client.get_departments()
    assert r.status_code == 200
    data = DepartmentsResponse.model_validate(r.json())
    assert len(data.departments) > 0
