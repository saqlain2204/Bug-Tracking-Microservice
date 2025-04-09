# Bug Tracker Microservice - Usage Examples

## Creating a Bug
```bash
curl -X POST http://localhost:8000/client/bugs/create \
  -H "Content-Type: application/json" \
  -d '{
    "bug_id": "BUG-001",
    "title": "Login Button Not Working",
    "description": "The login button is not responding to clicks"
  }'
```

## Creating a Client
```bash
curl -X POST http://localhost:8000/manager/client/create \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT-001",
    "name": "Acme Corporation"
  }'
```

## Creating an Employee
```bash
curl -X POST http://localhost:8000/manager/employee/create \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP-001",
    "name": "John Doe",
    "bugs_completed": 0,
    "bugs_pending": 0
  }'
```

## Listing All Bugs
```bash
curl http://localhost:8000/manager/bugs
```

## Assigning a Bug to an Employee
```bash
curl -X POST http://localhost:8000/manager/bugs/assign \
  -H "Content-Type: application/json" \
  -d '{
    "bug_id": "BUG-001",
    "employee_id": "EMP-001"
  }'
```

## Updating Bug Status
```bash
curl -X POST http://localhost:8000/employee/EMP-001/bugs/update \
  -H "Content-Type: application/json" \
  -d '{
    "bug_id": "BUG-001",
    "status": "In Progress"
  }'
```

## Viewing Employee's Bugs
```bash
curl http://localhost:8000/employee/EMP-001/bugs
``` 