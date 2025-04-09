# Bug Tracker Microservice - API Endpoints

## 1. Client Operations

### Create a Bug
```http
POST /client/bugs/create
Content-Type: application/json

{
    "bug_id": "string",
    "title": "string",
    "description": "string",
    "status": "string" (default: "Pending")
}
```

## 2. Manager Operations

### Create a Client
```http
POST /manager/client/create
Content-Type: application/json

{
    "client_id": "string",
    "name": "string"
}
```

### Create an Employee
```http
POST /manager/employee/create
Content-Type: application/json

{
    "employee_id": "string",
    "name": "string",
    "bugs_completed": "integer" (default: 0),
    "bugs_pending": "integer" (default: 0)
}
```

### List All Employees
```http
GET /manager/employees
```

### List All Clients
```http
GET /manager/clients
```

### Assign Bug to Employee
```http
POST /manager/bugs/assign
Content-Type: application/json

{
    "bug_id": "string",
    "employee_id": "string"
}
```

### List All Bugs
```http
GET /manager/bugs
```

## 3. Employee Operations

### List Employee's Bugs
```http
GET /employee/{employee_id}/bugs
```

### List Completed Bugs
```http
GET /employee/{employee_id}/bugs/completed
```

### List Pending Bugs
```http
GET /employee/{employee_id}/bugs/pending
```

### Update Bug Status
```http
POST /employee/{employee_id}/bugs/update
Content-Type: application/json

{
    "bug_id": "string",
    "status": "string"
}
``` 