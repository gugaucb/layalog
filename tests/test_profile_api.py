import pytest
import json
from fastapi.testclient import TestClient
from layalog.app import app
from layalog.database import init_db

client = TestClient(app)

def test_get_profiles_endpoint():
    response = client.get("/api/profiles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 7
    ids = [p["id"] for p in data]
    assert "web-app-general" in ids
    assert "keycloak-iam" in ids

def test_get_single_profile():
    response = client.get("/api/profiles/keycloak-iam")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Autenticação & Identidade (Keycloak / OAuth)"
    assert "Brute Force Protector" in data["criteria_critica"]

def test_profile_crud_endpoints():
    # 1. Create custom profile with explicit id
    payload = {
        "id": "custom-api-test",
        "name": "Custom API Test Profile",
        "description": "Test profile description",
        "system_context": "Test system context",
        "criteria_baixa": "critério baixa teste",
        "criteria_media": "critério média teste",
        "criteria_critica": "critério crítica teste"
    }
    create_res = client.post("/api/profiles", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["id"] == "custom-api-test"
    assert created["is_builtin"] is False

    # 1b. Create custom profile WITHOUT id in payload (auto-generated ID)
    payload_no_id = {
        "name": "Profile Without Id",
        "description": "Created from UI modal",
        "system_context": "UI context",
        "criteria_baixa": "baixa ui",
        "criteria_media": "media ui",
        "criteria_critica": "critica ui"
    }
    create_no_id_res = client.post("/api/profiles", json=payload_no_id)
    assert create_no_id_res.status_code == 201
    created_no_id = create_no_id_res.json()
    assert created_no_id["id"].startswith("custom-")
    assert created_no_id["name"] == "Profile Without Id"
    client.delete(f"/api/profiles/{created_no_id['id']}")

    # 2. Update custom profile
    update_payload = {
        "name": "Updated Custom API Profile",
        "description": "Updated description",
        "system_context": "Updated context",
        "criteria_baixa": "nova baixa",
        "criteria_media": "nova media",
        "criteria_critica": "nova critica"
    }
    update_res = client.put("/api/profiles/custom-api-test", json=update_payload)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["name"] == "Updated Custom API Profile"
    assert updated["criteria_baixa"] == "nova baixa"

    # 3. Cannot update built-in profile directly
    builtin_update = client.put("/api/profiles/keycloak-iam", json=update_payload)
    assert builtin_update.status_code == 400

    # 4. Clone built-in profile
    clone_res = client.post("/api/profiles/keycloak-iam/clone", json={"name": "Meu Keycloak Custom"})
    assert clone_res.status_code == 201
    cloned = clone_res.json()
    assert cloned["name"] == "Meu Keycloak Custom"
    assert cloned["is_builtin"] is False
    assert cloned["id"] != "keycloak-iam"

    # 5. Delete custom profile
    del_res = client.delete("/api/profiles/custom-api-test")
    assert del_res.status_code == 200
    
    # Clean up cloned
    client.delete(f"/api/profiles/{cloned['id']}")

    # 6. Cannot delete built-in profile
    del_builtin = client.delete("/api/profiles/keycloak-iam")
    assert del_builtin.status_code == 400

def test_analyze_with_specific_profile():
    log_content = (
        "2026-09-28 07:18:59,383 WARN  [org.keycloak.services] (Brute Force Protector) "
        "KC-SERVICES0053: login failure for user 930e369e-4d57-43ea-9f54-7464d050905e from ip 172.16.200.67\n"
    )
    files = {"file": ("keycloak_test.log", log_content.encode("utf-8"), "text/plain")}
    data = {"profile_id": "keycloak-iam"}
    
    res = client.post("/api/analyze", files=files, data=data)
    assert res.status_code == 200
    analysis = res.json()
    assert analysis["id"] is not None
    assert len(analysis["incidents"]) > 0
    
    # Check analysis detail from db
    detail_res = client.get(f"/api/analyses/{analysis['id']}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["profile_id"] == "keycloak-iam"
    assert detail["profile_snapshot"]["profile_name"] == "Autenticação & Identidade (Keycloak / OAuth)"
