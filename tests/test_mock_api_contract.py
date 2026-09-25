import pytest
from api.mock_api_client import MockApiClient
from config import settings

@pytest.mark.api
def test_mock_api_create_update_delete_contract():
    """Exercise the mock API's create/read/update/delete contract with assertions."""
    client = MockApiClient(settings.api_base_url)
    payload = {"name": "API Contract Employee", "data": {"employee_id": "API-TEST-001"}}
    resource_id, created = client.create_employee(payload)
    try:
        assert created["id"] == resource_id
        fetched = client.get_employee(resource_id)
        assert fetched.status_code == 200
        assert fetched.json()["data"]["employee_id"] == "API-TEST-001"

        updated_payload = {"name": "API Contract Employee", "data": {
            "employee_id": "API-TEST-001", "job_title": "QA Engineer"
        }}
        updated = client.update_employee(resource_id, updated_payload)
        assert updated["data"]["job_title"] == "QA Engineer"

        fetched_updated = client.get_employee(resource_id)
        assert fetched_updated.status_code == 200
        assert fetched_updated.json()["data"]["job_title"] == "QA Engineer"
    finally:
        deleted = client.delete_employee(resource_id)
        assert deleted.status_code in (200, 204), f"Unexpected delete status: {deleted.status_code}"
    assert client.get_employee(resource_id).status_code == 404
