import base64
import json
from pathlib import Path
from time import time_ns

import pytest

from api.mock_api_client import MockApiClient
from config import settings
from pages.login_page import LoginPage
from pages.pim_page import PimPage

ROOT = Path(__file__).resolve().parents[1]

def load_employee_data():
    return json.loads((ROOT / "data" / "employee.json").read_text(encoding="utf-8"))

def materialize_profile_picture():
    encoded = (ROOT / "assets" / "profile.png.base64").read_text(encoding="utf-8").strip()
    settings.artifact_dir.mkdir(parents=True, exist_ok=True)
    path = settings.artifact_dir / "profile.png"
    path.write_bytes(base64.b64decode(encoded))
    return path.resolve()

@pytest.mark.e2e
def test_employee_lifecycle(driver):
    """Create, edit, cross-check via permitted mock API, delete, and logout."""
    data = load_employee_data()
    employee_id = str(time_ns())[-8:]
    full_name = f"{data['first_name']} {data['last_name']}"
    login = LoginPage(driver, settings.timeout)
    pim = PimPage(driver, settings.timeout)
    api = MockApiClient(settings.api_base_url)

    login.open(f"{settings.base_url.rstrip('/')}/web/index.php/auth/login")
    login.login(settings.username, settings.password)

    pim.open_add_employee()
    employee_number = pim.add_employee(
        data["first_name"], data["last_name"], employee_id, materialize_profile_picture()
    )
    assert employee_number > 0, "OrangeHRM did not return a valid employee record number"

    # The public test API is a separate API substitute; it does not query OrangeHRM.
    initial_payload = {
        "name": full_name,
        "data": {"employee_id": employee_id, "employee_number": employee_number}
    }
    api_id, created = api.create_employee(initial_payload)
    assert str(created["data"]["employee_id"]) == employee_id
    get_created = api.get_employee(api_id)
    assert get_created.status_code == 200, f"API GET after create returned {get_created.status_code}"
    created_body = get_created.json()
    assert created_body["name"] == full_name
    assert str(created_body["data"]["employee_id"]) == employee_id

    pim.update_job(employee_id, data["job_title"], data["employment_status"])
    updated_payload = {
        "name": full_name,
        "data": {
            "employee_id": employee_id,
            "employee_number": employee_number,
            "job_title": data["job_title"],
            "employment_status": data["employment_status"]
        }
    }
    updated = api.update_employee(api_id, updated_payload)
    assert updated["name"] == full_name
    assert updated["data"]["job_title"] == data["job_title"]
    assert updated["data"]["employment_status"] == data["employment_status"]

    get_updated = api.get_employee(api_id)
    assert get_updated.status_code == 200, f"API GET after update returned {get_updated.status_code}"
    updated_body = get_updated.json()
    assert str(updated_body["data"]["employee_id"]) == employee_id
    assert updated_body["data"]["job_title"] == data["job_title"]
    assert updated_body["data"]["employment_status"] == data["employment_status"]

    pim.delete_employee(employee_id)
    deleted = api.delete_employee(api_id)
    assert deleted.status_code in (200, 204), f"API delete returned {deleted.status_code}"
    get_deleted = api.get_employee(api_id)
    assert get_deleted.status_code == 404, (
        f"Expected API resource to be absent after deletion; got {get_deleted.status_code}"
    )

    login.logout(settings.base_url)
