# Bug Tracker Microservice - Data Models

## Bug
```json
{
    "bug_id": "string",
    "title": "string",
    "description": "string",
    "status": "string",
    "employee_id": "string" (optional)
}
```

## Employee
```json
{
    "employee_id": "string",
    "name": "string",
    "bugs_completed": "integer",
    "bugs_pending": "integer"
}
```

## Client
```json
{
    "client_id": "string",
    "name": "string"
}
``` 