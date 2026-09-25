"""Thin client for restful-api.dev, used as the assignment's permitted API substitute.

Important: this is a separate mock API. It does not expose OrangeHRM's database.
"""
from urllib.parse import quote
import requests

class MockApiClient:
    def __init__(self, base_url: str, timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def create_employee(self, payload: dict) -> tuple[str, dict]:
        response = self.session.post(
            f"{self.base_url}/objects", json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        body = response.json()
        resource_id = body.get("id")
        assert resource_id, f"Create response did not contain id: {body}"
        return str(resource_id), body

    def get_employee(self, resource_id: str) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/objects/{quote(str(resource_id), safe='')}",
            timeout=self.timeout,
        )

    def update_employee(self, resource_id: str, payload: dict) -> dict:
        response = self.session.put(
            f"{self.base_url}/objects/{quote(str(resource_id), safe='')}",
            json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete_employee(self, resource_id: str) -> requests.Response:
        return self.session.delete(
            f"{self.base_url}/objects/{quote(str(resource_id), safe='')}",
            timeout=self.timeout
        )
