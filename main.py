from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
import uvicorn
import os

app = FastAPI()

# MongoDB setup
mongodb_url = os.getenv("MONGODB_URL", "mongodb://admin:password@localhost:27017")
client = MongoClient(mongodb_url)

# Helper function to get database for a specific group
def get_group_db(group_id: str):
    db_name = f"bugtracker_group_{group_id}"
    return client[db_name]

# Helper to serialize ObjectId
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# Pydantic models
class Employee(BaseModel):
    employee_id: str
    name: str
    bugs_completed: int = 0
    bugs_pending: int = 0

class Bug(BaseModel):
    bug_id: str
    title: str
    description: str
    status: str = "Pending"

class Manager(BaseModel):
    manager_id: str
    name: str

class Client(BaseModel):
    client_id: str
    name: str

# Routes

@app.get("/")
async def root():
    return {"message": "Welcome to the Bug Tracker"}

# --------------------- CLIENT ---------------------

@app.post("/{group_id}/client/bugs/create")
async def create_bug(group_id: str, bug: Bug):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    bug_collection.insert_one(bug.model_dump())
    if bug_collection.find_one({"bug_id": bug.bug_id}):
        return {"message": "Bug created successfully"}
    return {"message": "Bug creation failed"}

# --------------------- MANAGER ---------------------

@app.post("/{group_id}/manager/client/create")
async def create_client(group_id: str, client_data: Client):
    db = get_group_db(group_id)
    client_collection = db["client_collection"]
    if client_collection.find_one({"client_id": client_data.client_id}):
        return {"message": "Client already exists"}
    client_collection.insert_one(client_data.model_dump())
    if client_collection.find_one({"client_id": client_data.client_id}):
        return {"message": "Client created successfully"}
    return {"message": "Client creation failed"}

@app.post("/{group_id}/manager/employee/create")
async def create_employee(group_id: str, employee: Employee):
    db = get_group_db(group_id)
    employee_collection = db["employee_collection"]
    if employee_collection.find_one({"employee_id": employee.employee_id}):
        return {"message": "Employee already exists"}
    employee_collection.insert_one(employee.model_dump())
    return {"message": "Employee created successfully"}

@app.get("/{group_id}/manager/employees")
async def list_employees(group_id: str):
    db = get_group_db(group_id)
    employee_collection = db["employee_collection"]
    return [serialize_doc(emp) for emp in employee_collection.find()]

@app.get("/{group_id}/manager/clients")
async def list_clients(group_id: str):
    db = get_group_db(group_id)
    client_collection = db["client_collection"]
    return [serialize_doc(client) for client in client_collection.find()]

@app.post("/{group_id}/manager/bugs/assign")
async def assign_bug(group_id: str, bug_id: str, employee_id: str):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    employee_collection = db["employee_collection"]
    
    if bug_collection.find_one({"bug_id": bug_id}):
        bug_collection.update_one(
            {"bug_id": bug_id},
            {"$set": {"employee_id": employee_id}}
        )
        employee_collection.update_one(
            {"employee_id": employee_id},
            {"$inc": {"bugs_pending": 1}}
        )
        return {"message": "Bug assigned successfully"}
    return {"message": "Bug assignment failed"}

@app.get("/{group_id}/manager/bugs")
async def list_bugs(group_id: str):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    return [serialize_doc(bug) for bug in bug_collection.find()]

# --------------------- EMPLOYEE ---------------------

@app.get("/{group_id}/employee/{employee_id}/bugs")
async def list_employee_bugs(group_id: str, employee_id: str):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    return [serialize_doc(bug) for bug in bug_collection.find({"employee_id": employee_id})]

@app.get("/{group_id}/employee/{employee_id}/bugs/completed")
async def list_completed_bugs(group_id: str, employee_id: str):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    return [serialize_doc(bug) for bug in bug_collection.find({"employee_id": employee_id, "status": "Completed"})]

@app.get("/{group_id}/employee/{employee_id}/bugs/pending")
async def list_pending_bugs(group_id: str, employee_id: str):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    return [serialize_doc(bug) for bug in bug_collection.find({"employee_id": employee_id, "status": "Pending"})]

@app.post("/{group_id}/employee/{employee_id}/bugs/update")
async def update_bug_status(group_id: str, employee_id: str, bug_id: str, status: str):
    db = get_group_db(group_id)
    bug_collection = db["bug_collection"]
    employee_collection = db["employee_collection"]
    
    bug_collection.update_one(
        {"bug_id": bug_id, "employee_id": employee_id},
        {"$set": {"status": status}}
    )
    employee_collection.update_one(
        {"employee_id": employee_id},
        {"$inc": {"bugs_completed": 1}}
    )
    return {"message": f"Bug {bug_id} updated to status {status}"}

# --------------------- MAIN ---------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
