import pytest

from models import ObjectResponse, SearchResponse

SEARCH_QUERY = "sunflowers"
INVALID_OBJECT_ID = 999_999_999
EUROPEAN_PAINTINGS_DEPARTMENT_ID = 11


def test_search_by_keyword(client):
    response = client.search(q=SEARCH_QUERY)

    assert response.status_code == 200
    data = SearchResponse.model_validate(response.json())
    assert data.total > 0
    assert len(data.objectIDs) > 0
    assert all(isinstance(object_id, int) for object_id in data.objectIDs)


def test_search_response_structure(client):
    response = client.search(q=SEARCH_QUERY)

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"total", "objectIDs"}

    data = SearchResponse.model_validate(payload)
    assert data.total >= len(data.objectIDs)


def test_search_result_count_limit(client):
    response = client.search(q=SEARCH_QUERY)

    data = SearchResponse.model_validate(response.json())
    assert len(data.objectIDs) <= data.total
    assert len(data.objectIDs) == data.total


def test_search_no_results(client):
    response = client.search(q="xyznonexistentquery12345")

    assert response.status_code == 200
    data = SearchResponse.model_validate(response.json())
    assert data.total == 0
    assert data.objectIDs == []


def test_search_filter_is_highlight(client):
    all_results = SearchResponse.model_validate(client.search(q=SEARCH_QUERY).json())
    filtered = SearchResponse.model_validate(
        client.search(q=SEARCH_QUERY, isHighlight=True).json()
    )

    assert filtered.total <= all_results.total
    assert len(filtered.objectIDs) <= len(all_results.objectIDs)


def test_search_filter_by_department(client):
    response = client.search(q=SEARCH_QUERY, departmentId=EUROPEAN_PAINTINGS_DEPARTMENT_ID)

    assert response.status_code == 200
    data = SearchResponse.model_validate(response.json())
    assert data.total >= 0

    if data.objectIDs:
        object_response = client.get_object(data.objectIDs[0])
        artwork = ObjectResponse.model_validate(object_response.json())
        assert artwork.department == "European Paintings"


def test_search_filter_has_images(client):
    response = client.search(q=SEARCH_QUERY, hasImages=True)

    assert response.status_code == 200
    data = SearchResponse.model_validate(response.json())
    assert data.total > 0
    assert len(data.objectIDs) > 0

    artwork = ObjectResponse.model_validate(client.get_object(data.objectIDs[0]).json())
    assert artwork.primaryImage


@pytest.mark.skip(reason="Met Museum Search API does not support sorting parameters")
def test_search_sorting_not_supported():
    pass


def test_get_object_by_id(client):
    search_data = SearchResponse.model_validate(client.search(q=SEARCH_QUERY).json())
    object_id = search_data.objectIDs[0]

    response = client.get_object(object_id)

    assert response.status_code == 200
    data = ObjectResponse.model_validate(response.json())
    assert data.objectID == object_id
    assert data.title is not None


def test_get_object_not_found(client):
    response = client.get_object(INVALID_OBJECT_ID)

    assert response.status_code == 404
    assert response.json()["message"] == "ObjectID not found"
