# BowlsAce API Documentation

This document provides comprehensive documentation for the BowlsAce backend API, including all available endpoints, request parameters, response formats, and authentication requirements.

## Base URL

All API requests should be prefixed with the base URL:

```
https://your-domain.com/api/v1
```

## Postman Collection Setup

To help you get started with API testing, we've created a Postman collection that includes all the endpoints with example requests.

### Import the Collection

1. Download the [BowlsAce API Postman Collection](https://example.com/bowlsace-api-collection.json)
2. In Postman, click "Import" and select the downloaded file
3. Once imported, you'll see all available endpoints organized by category

### Environment Setup

Create an environment in Postman with the following variables:

| Variable      | Initial Value                | Description                         |
|---------------|------------------------------|-------------------------------------|
| `base_url`    | `https://your-domain.com/api/v1` | The base URL of the API            |
| `access_token`| `[empty]`                    | Will be populated after login       |

### Authentication Setup

The collection includes a "Login" request that automatically sets the `access_token` environment variable upon successful authentication:

1. Navigate to the "Auth" folder in the collection
2. Find and open the "Login" request
3. Update the request body with your credentials
4. Send the request
5. Upon success, the `access_token` will be automatically stored in your environment

All subsequent requests will automatically use this token for authentication.

## Authentication

Most endpoints require authentication using JWT tokens. The authentication flow works as follows:

### Authentication Headers

For protected endpoints, include an Authorization header with a Bearer token:

```
Authorization: Bearer <your_access_token>
```

### Authentication Endpoints

#### Register

```
POST /auth/register
```

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "phone_number": "+1234567890",
  "full_name": "User Name"
}
```

**Response:** 
```json
{
  "id": 123,
  "email": "user@example.com",
  "username": "username",
  "full_name": "User Name",
  "phone_number": "+1234567890",
  "is_active": true,
  "is_admin": false
}
```

**Status Codes:**
- 200: Success
- 400: User with this email/username/phone already exists

#### Request OTP

```
POST /auth/request-otp
```

Request a one-time password for phone verification.

**Request Body:**
```json
{
  "phone_number": "+1234567890"
}
```

**Response:**
```json
{
  "message": "OTP sent to +1234567890",
  "success": true
}
```

**Status Codes:**
- 200: Success
- 400: Invalid phone number

#### Verify OTP

```
POST /auth/verify-otp
```

Verify the one-time password sent to the phone.

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "otp": "123456"
}
```

**Response:**
```json
{
  "message": "OTP verified successfully",
  "success": true
}
```

**Status Codes:**
- 200: Success
- 400: Invalid or expired OTP

#### Complete Registration

```
POST /auth/register/complete
```

Complete the registration process after OTP verification.

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "otp": "123456",
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "full_name": "User Name"
}
```

**Response:**
```json
{
  "id": 123,
  "email": "user@example.com",
  "username": "username",
  "full_name": "User Name",
  "phone_number": "+1234567890",
  "is_active": true,
  "is_admin": false
}
```

**Status Codes:**
- 200: Success
- 400: Invalid OTP, user exists, or validation error

#### Login

```
POST /auth/login
```

Authenticate and receive an access token.

**Request Body (form data):**
```
username: your_username_or_email
password: your_password
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- 200: Success
- 401: Invalid credentials

## User Endpoints

### Get Current User

```
GET /users/me
```

Get the profile of the currently authenticated user.

**Authentication Required:** Yes

**Response:**
```json
{
  "id": 123,
  "email": "user@example.com",
  "username": "username",
  "full_name": "User Name",
  "phone_number": "+1234567890",
  "is_active": true,
  "is_admin": false
}
```

**Status Codes:**
- 200: Success
- 401/403: Not authenticated

### Update Current User

```
PUT /users/me
```

Update the profile of the currently authenticated user.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "password": "new_password" // Optional
}
```

**Response:** Updated user object

**Status Codes:**
- 200: Success
- 401/403: Not authenticated

### Get User By ID

```
GET /users/{user_id}
```

Get a specific user by ID (admin only, or own profile).

**Authentication Required:** Yes

**Response:** User object

**Status Codes:**
- 200: Success
- 403: Forbidden (not admin and not own profile)
- 404: User not found

## Practice Session Endpoints

### Create Practice Session

```
POST /practice/sessions
```

Create a new practice session.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "name": "Morning Practice",
  "location": "Lawn Bowl Club",
  "notes": "Working on draw shots",
  "duration_minutes": 60
}
```

**Response:** Created session object

**Status Codes:**
- 200: Success
- 401/403: Not authenticated

### List Practice Sessions

```
GET /practice/sessions
```

Get all practice sessions for the current user.

**Authentication Required:** Yes

**Query Parameters:**
- skip (int): Number of records to skip (default: 0)
- limit (int): Max number of records to return (default: 100)

**Response:** Array of session objects

**Status Codes:**
- 200: Success
- 401/403: Not authenticated

### Get Practice Session

```
GET /practice/sessions/{session_id}
```

Get details of a specific practice session with statistics.

**Authentication Required:** Yes

**Response:**
```json
{
  "id": 123,
  "name": "Morning Practice",
  "location": "Lawn Bowl Club",
  "notes": "Working on draw shots",
  "duration_minutes": 60,
  "user_id": 456,
  "created_at": "2023-01-01T12:00:00",
  "shot_count": 25,
  "average_accuracy": 7.8,
  "drill_count": 3
}
```

**Status Codes:**
- 200: Success
- 403: Not authorized to view this session
- 404: Session not found

### Update Practice Session

```
PUT /practice/sessions/{session_id}
```

Update an existing practice session.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "name": "Updated Name",
  "notes": "Updated notes"
}
```

**Response:** Updated session object

**Status Codes:**
- 200: Success
- 403: Not authorized to modify this session
- 404: Session not found

### Delete Practice Session

```
DELETE /practice/sessions/{session_id}
```

Delete a practice session.

**Authentication Required:** Yes

**Status Codes:**
- 204: Success (No Content)
- 403: Not authorized to delete this session
- 404: Session not found

## Drill Endpoints

### List Drills

```
GET /drill
```

Get all available drills.

**Query Parameters:**
- skip (int): Number of records to skip (default: 0)
- limit (int): Max number of records to return (default: 100)
- search (string, optional): Search term for drill name/description
- difficulty (int, optional): Filter by difficulty level

**Response:** Array of drill objects

**Status Codes:**
- 200: Success

### Create Drill

```
POST /drill
```

Create a new drill.

**Request Body:**
```json
{
  "name": "Draw to Jack",
  "description": "Practice drawing bowls to the jack",
  "difficulty": 3,
  "target_score": 10,
  "session_id": 123,
  "type": "DRAW",
  "duration_minutes": 15
}
```

**Response:** Created drill object

**Status Codes:**
- 200: Success
- 422: Validation error

### Get Drill

```
GET /drill/{drill_id}
```

Get details of a specific drill.

**Response:** Drill object

**Status Codes:**
- 200: Success
- 404: Drill not found

### Update Drill

```
PUT /drill/{drill_id}
```

Update an existing drill.

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "difficulty": 4
}
```

**Response:** Updated drill object

**Status Codes:**
- 200: Success
- 404: Drill not found

### Delete Drill

```
DELETE /drill/{drill_id}
```

Delete a drill.

**Response:** Deleted drill object

**Status Codes:**
- 200: Success
- 404: Drill not found

## Drill Group Endpoints

### List Drill Groups

```
GET /drill-groups
```

Get all available drill groups.

**Query Parameters:**
- skip (int): Number of records to skip (default: 0)
- limit (int): Max number of records to return (default: 100)

**Response:** Array of drill group objects

**Status Codes:**
- 200: Success

### Create Drill Group

```
POST /drill-groups
```

Create a new drill group.

**Authentication:** Optional (if authenticated, associates with user)

**Request Body:**
```json
{
  "name": "Draw Shot Training",
  "description": "A collection of drills for improving draw shots",
  "drill_ids": [1, 2, 3],
  "is_public": true,
  "tags": ["beginner", "draw"],
  "difficulty": 2
}
```

**Response:** Created drill group object

**Status Codes:**
- 200: Success
- 422: Validation error

### Get Drill Group

```
GET /drill-groups/{drill_group_id}
```

Get details of a specific drill group.

**Response:** Drill group object

**Status Codes:**
- 200: Success
- 404: Drill group not found

### Update Drill Group

```
PUT /drill-groups/{drill_group_id}
```

Update an existing drill group.

**Authentication Required:** Yes (if owned by a user)

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "is_public": false
}
```

**Response:** Updated drill group object

**Status Codes:**
- 200: Success
- 403: Not authorized to modify this drill group
- 404: Drill group not found

### Delete Drill Group

```
DELETE /drill-groups/{drill_group_id}
```

Delete a drill group.

**Authentication Required:** Yes (if owned by a user)

**Response:** Deleted drill group object

**Status Codes:**
- 200: Success
- 403: Not authorized to delete this drill group
- 404: Drill group not found

### Add Drill to Group

```
POST /drill-groups/{drill_group_id}/drills/{drill_id}
```

Add a drill to a drill group.

**Authentication Required:** Yes (if owned by a user)

**Response:**
```json
{
  "message": "Drill added to group successfully"
}
```

**Status Codes:**
- 200: Success
- 403: Not authorized to modify this drill group
- 404: Drill group or drill not found

### Remove Drill from Group

```
DELETE /drill-groups/{drill_group_id}/drills/{drill_id}
```

Remove a drill from a drill group.

**Authentication Required:** Yes (if owned by a user)

**Response:**
```json
{
  "message": "Drill removed from group successfully"
}
```

**Status Codes:**
- 200: Success
- 403: Not authorized to modify this drill group
- 404: Drill group or drill not found

## Challenge Endpoints

### Send Challenge

```
POST /challenge/send
```

Send a challenge to another user.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "recipient_id": 456,
  "drill_id": 123,
  "message": "Let's see who can score better!",
  "expires_at": "2023-01-15T12:00:00"
}
```

**Response:** Created challenge object

**Status Codes:**
- 200: Success
- 404: Recipient not found

### List Challenges

```
GET /challenge
```

List all challenges for the current user.

**Authentication Required:** Yes

**Query Parameters:**
- status (string, optional): Filter by challenge status (PENDING, ACCEPTED, DECLINED, COMPLETED, EXPIRED)
- skip (int): Number of records to skip (default: 0)
- limit (int): Max number of records to return (default: 100)

**Response:** Array of challenge objects

**Status Codes:**
- 200: Success

### Get Challenge

```
GET /challenge/{challenge_id}
```

Get details of a specific challenge.

**Authentication Required:** Yes

**Response:** Challenge object with sender and recipient details

**Status Codes:**
- 200: Success
- 403: Not authorized to view this challenge
- 404: Challenge not found

### Accept Challenge

```
PUT /challenge/{challenge_id}/accept
```

Accept a challenge from another user.

**Authentication Required:** Yes (must be the recipient)

**Response:** Updated challenge object

**Status Codes:**
- 200: Success
- 400: Challenge not pending or expired
- 403: Not authorized to accept this challenge
- 404: Challenge not found

### Decline Challenge

```
PUT /challenge/{challenge_id}/decline
```

Decline a challenge from another user.

**Authentication Required:** Yes (must be the recipient)

**Response:** Updated challenge object

**Status Codes:**
- 200: Success
- 400: Challenge not pending
- 403: Not authorized to decline this challenge
- 404: Challenge not found

## Dashboard Endpoints

### Get Dashboard Metrics

```
GET /dashboard/{user_id}
```

Get dashboard metrics for a user.

**Authentication Required:** Yes (must be the user or an admin)

**Response:**
```json
{
  "username": "username",
  "total_sessions": 25,
  "total_shots": 500,
  "average_accuracy": 7.5,
  "total_challenges": 10,
  "completed_challenges": 8,
  "improvement_trend": 0.5
}
```

**Status Codes:**
- 200: Success
- 403: Not authorized to view this dashboard
- 404: User not found

## Administrator Endpoints

Administrator endpoints are available under `/admin` prefix but aren't covered in this documentation as they're intended for internal use only.

## Health Check

```
GET /health
```

Check if the API is running.

**Authentication Required:** No

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- 200: Success

## Error Handling

All error responses follow a consistent format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

Common HTTP status codes:
- 400: Bad Request - Invalid input or business rule violation
- 401: Unauthorized - Missing authentication
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource doesn't exist
- 422: Unprocessable Entity - Validation error
- 500: Internal Server Error - Unexpected server error

## Request and Response Examples

### Authentication Examples

#### Example: User Registration

**Request:**
```bash
curl -X POST https://your-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "phone_number": "+12025550189",
    "full_name": "John Doe"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1245,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "phone_number": "+12025550189",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-06-03T10:30:45.123Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "A user with this email already exists"
}
```

#### Example: Login

**Request:**
```bash
curl -X POST https://your-domain.com/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=SecurePass123!"
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect username or password"
}
```

### Practice Session Examples

#### Example: Create Practice Session

**Request:**
```bash
curl -X POST https://your-domain.com/api/v1/practice/sessions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "Morning Draw Practice",
    "location": "Central Bowling Club",
    "notes": "Focus on weight control",
    "duration_minutes": 45
  }'
```

**Response (200 OK):**
```json
{
  "id": 789,
  "name": "Morning Draw Practice",
  "location": "Central Bowling Club",
  "notes": "Focus on weight control",
  "duration_minutes": 45,
  "user_id": 1245,
  "created_at": "2025-06-03T14:22:16.789Z",
  "updated_at": "2025-06-03T14:22:16.789Z"
}
```

#### Example: Get Practice Session with Stats

**Request:**
```bash
curl -X GET https://your-domain.com/api/v1/practice/sessions/789 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200 OK):**
```json
{
  "id": 789,
  "name": "Morning Draw Practice",
  "location": "Central Bowling Club",
  "notes": "Focus on weight control",
  "duration_minutes": 45,
  "user_id": 1245,
  "created_at": "2025-06-03T14:22:16.789Z",
  "updated_at": "2025-06-03T14:22:16.789Z",
  "shot_count": 32,
  "average_accuracy": 7.6,
  "drill_count": 3
}
```

### Drill Examples

#### Example: Get Drills with Filtering

**Request:**
```bash
curl -X GET "https://your-domain.com/api/v1/drill?difficulty=3&search=draw" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200 OK):**
```json
[
  {
    "id": 45,
    "name": "Weighted Draw Shot",
    "description": "Practice drawing to different lengths with precise weight control",
    "difficulty": 3,
    "target_score": 8,
    "type": "DRAW",
    "duration_minutes": 15,
    "created_at": "2025-05-15T09:12:45.678Z"
  },
  {
    "id": 52,
    "name": "Draw to Target",
    "description": "Draw shots to a specific target area on the green",
    "difficulty": 3,
    "target_score": 10,
    "type": "DRAW",
    "duration_minutes": 20,
    "created_at": "2025-05-18T11:30:22.456Z"
  }
]
```

### Challenge Examples

#### Example: Send Challenge

**Request:**
```bash
curl -X POST https://your-domain.com/api/v1/challenge/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "recipient_id": 1246,
    "drill_id": 45,
    "message": "Let\'s see who can get closest to the jack!",
    "expires_at": "2025-06-10T23:59:59.999Z"
  }'
```

**Response (200 OK):**
```json
{
  "id": 567,
  "sender_id": 1245,
  "recipient_id": 1246,
  "drill_id": 45,
  "message": "Let's see who can get closest to the jack!",
  "status": "PENDING",
  "created_at": "2025-06-03T15:30:45.123Z",
  "expires_at": "2025-06-10T23:59:59.999Z"
}
```

#### Example: Accept Challenge

**Request:**
```bash
curl -X PUT https://your-domain.com/api/v1/challenge/567/accept \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200 OK):**
```json
{
  "id": 567,
  "sender_id": 1245,
  "recipient_id": 1246,
  "drill_id": 45,
  "message": "Let's see who can get closest to the jack!",
  "status": "ACCEPTED",
  "created_at": "2025-06-03T15:30:45.123Z",
  "expires_at": "2025-06-10T23:59:59.999Z",
  "accepted_at": "2025-06-03T16:45:12.345Z"
}
```

### Dashboard Examples

#### Example: Get Dashboard Metrics

**Request:**
```bash
curl -X GET https://your-domain.com/api/v1/dashboard/1245 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200 OK):**
```json
{
  "username": "johndoe",
  "total_sessions": 25,
  "total_shots": 752,
  "average_accuracy": 7.2,
  "total_challenges": 14,
  "completed_challenges": 12,
  "improvement_trend": 0.8,
  "recent_sessions": [
    {
      "id": 789,
      "name": "Morning Draw Practice",
      "created_at": "2025-06-03T14:22:16.789Z"
    },
    {
      "id": 788,
      "name": "Afternoon Weight Control",
      "created_at": "2025-06-02T16:15:30.456Z"
    }
  ]
}
```

## API Versioning and Migration

### Current API Version

The current API version is `v1`, which is reflected in the base URL:

```
https://your-domain.com/api/v1
```

### Versioning Strategy

BowlsAce API follows semantic versioning principles:

1. **Major Version Changes (v1 → v2)**
   - Breaking changes that require client updates
   - Removal of endpoints or significant changes in response structure
   - Changes in authentication methods

2. **Minor Version Changes**
   - New features that don't break existing functionality
   - Additional endpoints or parameters
   - Extended response objects with new fields

3. **Patch Version Changes**
   - Bug fixes
   - Performance improvements
   - Internal refactoring with no API changes

### Deprecation Policy

When features are scheduled for removal in future versions:

1. The endpoint will be marked as deprecated in the documentation
2. A `Deprecated` header will be included in responses from deprecated endpoints
3. Deprecated features will be maintained for at least 6 months before removal

Example of a deprecated endpoint response header:
```
Deprecated: true
Sunset: Sun, 01 Jan 2026 00:00:00 GMT
Link: <https://your-domain.com/api/v2/new-endpoint>; rel="successor-version"
```

### API Changelog

#### v1.0.0 (Current)
- Initial stable API release
- Authentication with JWT tokens
- User management endpoints
- Practice session tracking
- Drill and drill group management
- Challenge system
- Dashboard metrics

#### v0.9.0 (Beta)
- Pre-release version for testing
- Limited feature set

### Future Migration Guide

When a new major version is released, this section will contain a detailed guide for migrating from v1 to v2, including:

- Endpoint mapping from old to new versions
- Request and response format changes
- Authentication changes
- Code examples for key migrations

### Version Compatibility

For a smooth transition between versions, the API will:

1. Support multiple major versions concurrently for at least 12 months
2. Provide detailed migration documentation
3. Offer a test environment for trying the new version before migration

## WebSockets API (Preview)

In addition to the REST API, BowlsAce provides a WebSockets API for real-time features:

```
wss://your-domain.com/ws
```

### Authentication

WebSocket connections require authentication using the same JWT tokens:

```javascript
const socket = new WebSocket('wss://your-domain.com/ws');
socket.addEventListener('open', () => {
  socket.send(JSON.stringify({
    type: 'authenticate',
    token: 'your-jwt-token'
  }));
});
```

### Available Events

#### Subscribing to Events

```javascript
socket.send(JSON.stringify({
  type: 'subscribe',
  event: 'challenges'
}));
```

#### Event Types

- `challenge_received`: Triggered when you receive a new challenge
- `challenge_updated`: Triggered when a challenge status changes
- `session_updated`: Triggered when a session is updated
- `leaderboard_change`: Triggered when leaderboard positions change

#### Example Event

```javascript
// Incoming message
{
  "type": "challenge_received",
  "data": {
    "challenge_id": 567,
    "sender_name": "JohnDoe",
    "drill_name": "Weighted Draw Shot",
    "message": "Let's see who can get closest to the jack!"
  }
}
```

### Error Handling

Socket errors follow the same format as REST API errors:

```javascript
{
  "type": "error",
  "code": 401,
  "message": "Authentication failed"
}
```

## Rate Limiting

To ensure API stability, rate limits are enforced:

| Endpoint Category | Rate Limit         | Limit Reset |
|------------------|---------------------|-------------|
| Authentication   | 10 requests/minute  | 1 minute    |
| Practice Sessions| 60 requests/minute  | 1 minute    |
| Challenges       | 30 requests/minute  | 1 minute    |
| Dashboard        | 30 requests/minute  | 1 minute    |
| Other endpoints  | 120 requests/minute | 1 minute    |

When a rate limit is exceeded, the API will respond with a `429 Too Many Requests` status code and headers indicating the limit and reset time:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1654321899
```

## CORS Support

The API supports Cross-Origin Resource Sharing (CORS) for browser-based applications. The following headers are included in responses:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 3600
```

## Error Handling

All error responses follow a consistent format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

Common HTTP status codes:
- 400: Bad Request - Invalid input or business rule violation
- 401: Unauthorized - Missing authentication
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource doesn't exist
- 422: Unprocessable Entity - Validation error
- 500: Internal Server Error - Unexpected server error
