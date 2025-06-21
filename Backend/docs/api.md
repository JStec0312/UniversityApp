# API Documentation

This document describes the API endpoints provided by the UniversityApp backend.

## Authentication

*Note: Authentication system is planned for future implementation*

## Base URL

```
http://localhost:8000/api
```

## User Management

### Get User

```
GET /users/{user_id}
```

Retrieves a user by ID.

**Response**
```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "verified": true,
  "university_id": 1,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### Create User

```
POST /users
```

Creates a new user.

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "display_name": "John Doe",
  "university_id": 1
}
```

**Response**
```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "verified": false,
  "university_id": 1,
  "created_at": "2025-06-21T00:00:00Z",
  "updated_at": "2025-06-21T00:00:00Z"
}
```

### Update User

```
PUT /users/{user_id}
```

Updates an existing user.

**Request Body**
```json
{
  "display_name": "John Updated",
  "university_id": 2
}
```

### Delete User

```
DELETE /users/{user_id}
```

Deletes a user by ID.

## Student Management

### Get Student

```
GET /students/{student_id}
```

Retrieves a student by ID.

**Response**
```json
{
  "id": 1,
  "user_id": 1,
  "faculty_id": 1,
  "major_id": 1,
  "graduation_year": 2026,
  "student_id_number": "S12345",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z",
  "user": {
    "id": 1,
    "email": "student@example.com",
    "display_name": "John Student",
    "verified": true
  }
}
```

### Create Student

```
POST /students
```

Creates a new student profile.

**Request Body**
```json
{
  "user_id": 1,
  "faculty_id": 1,
  "major_id": 1,
  "graduation_year": 2026,
  "student_id_number": "S12345"
}
```

## News Management

### Get All News

```
GET /news
```

Retrieves all news items, with optional pagination.

**Query Parameters**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "title": "New Campus Building",
      "content": "The university is opening a new campus building...",
      "university_id": 1,
      "created_at": "2025-06-01T00:00:00Z",
      "updated_at": "2025-06-01T00:00:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 10
}
```

### Get News Item

```
GET /news/{news_id}
```

Retrieves a specific news item by ID.

## Event Management

### Get All Events

```
GET /events
```

Retrieves all events, with optional pagination and filtering.

**Query Parameters**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `upcoming`: If true, returns only future events (default: false)

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Career Fair",
      "description": "Annual university career fair...",
      "start_time": "2025-10-15T10:00:00Z",
      "end_time": "2025-10-15T16:00:00Z",
      "location": "Main Campus Hall",
      "university_id": 1,
      "created_at": "2025-06-01T00:00:00Z",
      "updated_at": "2025-06-01T00:00:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "limit": 10
}
```

### RSVP to Event

```
POST /events/{event_id}/rsvp
```

Registers a user for an event.

**Request Body**
```json
{
  "user_id": 1,
  "status": "attending"
}
```

## Forum Management

### Get Forum Posts

```
GET /forum
```

Retrieves forum posts, with optional pagination and filtering.

**Query Parameters**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `category`: Filter by category (optional)

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Study Group for CS101",
      "content": "Looking for students to join a study group for CS101...",
      "category": "academic",
      "user_id": 1,
      "created_at": "2025-06-01T00:00:00Z",
      "updated_at": "2025-06-01T00:00:00Z",
      "user": {
        "id": 1,
        "display_name": "John Student"
      }
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

### Create Forum Post

```
POST /forum
```

Creates a new forum post.

**Request Body**
```json
{
  "title": "Study Group for CS101",
  "content": "Looking for students to join a study group for CS101...",
  "category": "academic",
  "user_id": 1
}
```

## Discount Management

### Get All Discounts

```
GET /discounts
```

Retrieves all student discounts, with optional pagination.

**Query Parameters**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Campus Bookstore 20% Off",
      "description": "Get 20% off at the campus bookstore with your student ID",
      "valid_from": "2025-06-01T00:00:00Z",
      "valid_to": "2025-12-31T23:59:59Z",
      "university_id": 1,
      "created_at": "2025-06-01T00:00:00Z",
      "updated_at": "2025-06-01T00:00:00Z"
    }
  ],
  "total": 8,
  "page": 1,
  "limit": 10
}
```

## Error Responses

The API uses standard HTTP status codes to indicate the success or failure of requests.

### Common Error Codes

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "detail": "Error message describing the issue"
}
```

For validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
