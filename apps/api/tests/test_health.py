from fastapi.testclient import TestClient


def test_health_ok_in_demo_mode(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["demo_mode"] is True
    assert body["providers"] == ["mock"]
