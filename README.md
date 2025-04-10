# TaskPal
#### To Run Backend
#### Navigate to ```/backend```
#### Run in terminal
```
fastapi dev app/
```

# TaskPal API Documentation

## Overview

TaskPal provides a set of RESTful APIs for managing tasks and collections. The API allows users to perform actions such as logging in, signing up, adding tasks, updating tasks, and managing collections.

## API Version

- **Version**: 1.0
- **OpenAPI Version**: 3.1.0

## Authentication

TaskPal uses token-based authentication. You need to log in with your credentials to obtain a token. After obtaining the token, it must be included in the `Authorization` header of your requests.

## Endpoints

### User Endpoints

#### `POST /api/v1/user/login`
- **Summary**: Login
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
- **Responses**:
200 - will include authentication token in the header, this token will be used in future requests to provide userid
