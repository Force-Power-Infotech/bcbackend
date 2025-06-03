# Drill Groups API Documentation

## Overview
The Drill Groups API allows users to create and manage collections of drills. Each drill group can optionally belong to a specific user and can contain multiple drills. The API now supports public drill groups that don't require authentication to access or create.

## Endpoints

### 1. List Drill Groups

Get all drill groups. No authentication required.

```http
GET /api/v1/drill-groups
```

Query Parameters:
- `skip` (optional): Number of items to skip (default: 0)
- `limit` (optional): Maximum number of items to return (default: 100)

Example Response:
```json
[
  {
    "id": 1,
    "name": "Yash's Drills",
    "description": "My favorite drills for improvement",
    "user_id": 123,
    "created_at": "2025-06-02T10:30:00Z",
    "updated_at": "2025-06-02T10:30:00Z",
    "drills": [
      {
        "id": 1,
        "name": "Forward Defense",
        "description": "Practice forward defensive shots",
        "difficulty": "intermediate"
      }
    ]
  }
]
```

### 2. Create Drill Group

Create a new drill group. No authentication required.

```http
POST /api/v1/drill-groups
```

Request Body:
```json
{
  "name": "Yash's Drills",
  "description": "My favorite drills for improvement",
  "drill_ids": [1, 5, 7],
  "is_public": true,
  "tags": ["beginner", "drive"],
  "difficulty": 2
}
```

All fields except `name` are optional.

Example Response:
```json
{
  "id": 1,
  "name": "Yash's Drills",
  "description": "My favorite drills for improvement",
  "user_id": 123,
  "created_at": "2025-06-02T10:30:00Z",
  "updated_at": "2025-06-02T10:30:00Z",
  "drills": [
    {
      "id": 1,
      "name": "Forward Defense",
      "description": "Practice forward defensive shots"
    }
  ]
}
```

### 3. Get Drill Group

Get details of a specific drill group.

```http
GET /api/v1/drill-groups/{group_id}
```

Example Response:
```json
{
  "id": 1,
  "name": "Yash's Drills",
  "description": "My favorite drills for improvement",
  "user_id": 123,
  "created_at": "2025-06-02T10:30:00Z",
  "updated_at": "2025-06-02T10:30:00Z",
  "drills": [
    {
      "id": 1,
      "name": "Forward Defense",
      "description": "Practice forward defensive shots"
    }
  ]
}
```

### 4. Update Drill Group

Update a drill group's basic information.

```http
PUT /api/v1/drill-groups/{group_id}
```

Request Body:
```json
{
  "name": "Updated Drill Group Name",
  "description": "Updated description"
}
```

Example Response:
```json
{
  "id": 1,
  "name": "Updated Drill Group Name",
  "description": "Updated description",
  "user_id": 123,
  "created_at": "2025-06-02T10:30:00Z",
  "updated_at": "2025-06-02T11:00:00Z",
  "drills": [...]
}
```

### 5. Update Drill Group Drills

Update the drills in a drill group.

```http
PUT /api/v1/drill-groups/{group_id}/drills
```

Query Parameters:
- `drill_ids`: Array of drill IDs to set for the group

Example Request:
```http
PUT /api/v1/drill-groups/1/drills?drill_ids=1&drill_ids=2&drill_ids=3
```

Example Response:
```json
{
  "id": 1,
  "name": "Yash's Drills",
  "description": "My favorite drills for improvement",
  "user_id": 123,
  "created_at": "2025-06-02T10:30:00Z",
  "updated_at": "2025-06-02T11:00:00Z",
  "drills": [
    {
      "id": 1,
      "name": "Forward Defense"
    },
    {
      "id": 2,
      "name": "Pull Shot"
    },
    {
      "id": 3,
      "name": "Cover Drive"
    }
  ]
}
```

### 6. Delete Drill Group

Delete a drill group.

```http
DELETE /api/v1/drill-groups/{group_id}
```

Example Response:
```json
{
  "id": 1,
  "name": "Yash's Drills",
  "description": "My favorite drills for improvement",
  "user_id": 123,
  "created_at": "2025-06-02T10:30:00Z",
  "updated_at": "2025-06-02T10:30:00Z"
}
```

## Integration with Practice Sessions

When creating a practice session, you can include drill groups:

```http
POST /api/v1/practice/sessions
```

Request Body:
```json
{
  "title": "Morning Practice",
  "description": "Practice session using my favorite drills",
  "duration_minutes": 60,
  "location": "Indoor Nets",
  "drill_group_ids": [1, 2],
  "drill_ids": [3, 4]  // Additional individual drills
}
```

The system will automatically include all drills from the specified drill groups along with any individual drills specified.

## June 2025 API Updates

### Authentication Changes
- Authentication is now **optional** for all drill group endpoints 
- Public drill groups can be created and accessed without authentication
- When authenticated, you can still manage your own drill groups as before

### New Drill Group Properties
The drill group model has been extended with these new properties:

- `is_public` (boolean): Whether the drill group is publicly accessible (default: true)
- `difficulty` (integer): The difficulty level from 1-5 (default: 1)
- `tags` (array): A list of string tags for categorization (default: [])

### Example Usage

**Creating a public drill group:**
```http
POST /api/v1/drill-groups

{
  "name": "Public Beginner Drills",
  "description": "A collection of simple drills for beginners",
  "is_public": true,
  "difficulty": 1,
  "tags": ["beginner", "basic", "starter"],
  "drill_ids": [1, 2, 3]
}
```

**Response format:**
```json
{
  "id": 45,
  "name": "Public Beginner Drills",
  "description": "A collection of simple drills for beginners",
  "user_id": null,
  "is_public": true,
  "difficulty": 1,
  "tags": ["beginner", "basic", "starter"],
  "created_at": "2025-06-03T15:30:00Z",
  "updated_at": "2025-06-03T15:30:00Z"
}
```
