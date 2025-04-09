import pytest
from fastapi.testclient import TestClient
from main import app
import os
from pymongo import MongoClient

client = TestClient(app)

# Test data
TEST_BUG = {
    "bug_id": "TEST-001",
    "title": "Test Bug",
    "description": "This is a test bug",
    "status": "Pending"
}

TEST_CLIENT = {
    "client_id": "TEST-CLIENT-001",
    "name": "Test Client"
}

TEST_EMPLOYEE = {
    "employee_id": "TEST-EMP-001",
    "name": "Test Employee",
    "bugs_completed": 0,
    "bugs_pending": 0
}

def setup_module(module):
    """Setup test environment"""
    # Use a test database
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test_bugtracker_db"

def teardown_module(module):
    """Cleanup test environment"""
    # Drop test database
    mongo_client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
    mongo_client.drop_database("test_bugtracker_db")

# Client Tests
def test_create_bug():
    response = client.post("/client/bugs/create", json=TEST_BUG)
    assert response.status_code == 200
    assert response.json()["message"] == "Bug created successfully"

def test_create_duplicate_bug():
    response = client.post("/client/bugs/create", json=TEST_BUG)
    assert response.status_code == 200
    assert "already exists" in response.json()["message"].lower()

# Manager Tests
def test_create_client():
    response = client.post("/manager/client/create", json=TEST_CLIENT)
    assert response.status_code == 200
    assert response.json()["message"] == "Client created successfully"

def test_create_employee():
    response = client.post("/manager/employee/create", json=TEST_EMPLOYEE)
    assert response.status_code == 200
    assert response.json()["message"] == "Employee created successfully"

def test_list_employees():
    response = client.get("/manager/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_list_clients():
    response = client.get("/manager/clients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_assign_bug():
    response = client.post("/manager/bugs/assign", json={
        "bug_id": TEST_BUG["bug_id"],
        "employee_id": TEST_EMPLOYEE["employee_id"]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Bug assigned successfully"

# Employee Tests
def test_list_employee_bugs():
    response = client.get(f"/employee/{TEST_EMPLOYEE['employee_id']}/bugs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_bug_status():
    response = client.post(
        f"/employee/{TEST_EMPLOYEE['employee_id']}/bugs/update",
        json={
            "bug_id": TEST_BUG["bug_id"],
            "status": "In Progress"
        }
    )
    assert response.status_code == 200
    assert "updated to status" in response.json()["message"] 