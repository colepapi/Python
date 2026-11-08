import json
import os
import time
import urllib.error
import urllib.request
import uuid


API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "http://127.0.0.1:8501").rstrip("/")


def wait_for(url: str, description: str, timeout: int = 90) -> None:
    deadline = time.monotonic() + timeout
    last_error = "no response"

    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return
                last_error = f"HTTP {response.status}"
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = str(error)
        time.sleep(2)

    raise RuntimeError(f"{description} did not become ready at {url}: {last_error}")


def request_json(
    path: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    token: str | None = None,
    expected_status: int = 200,
) -> dict | list:
    headers = {"Accept": "application/json"}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        f"{API_BASE_URL}{path}",
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response_body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        response_body = error.read()
        raise AssertionError(
            f"{method} {path}: expected HTTP {expected_status}, got HTTP "
            f"{error.code}: {response_body.decode('utf-8', errors='replace')}"
        ) from error

    if status != expected_status:
        raise AssertionError(
            f"{method} {path}: expected HTTP {expected_status}, got HTTP {status}: "
            f"{response_body.decode('utf-8', errors='replace')}"
        )
    return json.loads(response_body)


def main() -> None:
    wait_for(f"{API_BASE_URL}/openapi.json", "FastAPI")
    wait_for(f"{DASHBOARD_URL}/_stcore/health", "Streamlit dashboard")

    registration = request_json(
        "/users/",
        method="POST",
        expected_status=201,
        payload={
            "full_name": "CI Smoke Test",
            "email": f"ci-{uuid.uuid4().hex}@example.com",
            "pin": "482917",
        },
    )
    user_id = registration["user_id"]
    assert len(user_id) == 8 and user_id.isdigit(), "Registration returned an invalid user ID"

    login = request_json(
        "/login",
        method="POST",
        payload={"user_id": user_id, "pin": "482917"},
    )
    token = login["access_token"]

    current_user = request_json("/users/me", token=token)
    assert current_user["user_id"] == user_id, "Authenticated user did not match"

    created_expense = request_json(
        "/expenses",
        method="POST",
        expected_status=201,
        token=token,
        payload={
            "category": "CI Test",
            "subcategory": "Smoke Test",
            "description": "Temporary integration test expense",
            "amount": "12.34",
        },
    )
    expenses = request_json("/expenses", token=token)
    assert any(item["expense_id"] == created_expense["expense_id"] for item in expenses), (
        "Created expense was not returned by the authenticated expenses endpoint"
    )

    print("Smoke test passed: dashboard, registration, login, authentication, and expenses.")


if __name__ == "__main__":
    main()
