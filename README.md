# BowlsAce Backend

Backend API for the BowlsAce application - A practice and challenge tracking platform for lawn bowls players.

## Features

- 👤 **User Authentication**: Register, login, manage profiles
- 📊 **Practice Tracking**: Log practice sessions, shots, and drills
- 🏆 **Challenges**: Send and compete in challenges with other players
- 📈 **Performance Dashboard**: Track progress and view statistics
- 📋 **Advisor System**: Get AI-based recommendations based on practice data
- 🔑 **Admin Panel**: User management and content moderation

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy (Async)
- **Database**: PostgreSQL
- **Authentication**: JWT
- **API Documentation**: Swagger UI / ReDoc
- **Containerization**: Docker & Docker Compose
- **Migrations**: Alembic

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Setup and Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bowlsace-backend.git
   cd bowlsace-backend
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```ini
   POSTGRES_USER=bowlsace
   POSTGRES_PASSWORD=supersecret
   POSTGRES_DB=bowlsacedb
   DATABASE_URL=postgresql+asyncpg://bowlsace:supersecret@db:5432/bowlsacedb
   SECRET_KEY=your_jwt_secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Start the services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Run database migrations:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

5. Access the API documentation at:
   ```
   http://localhost:8000/api/v1/docs
   ```

### Development

To run the application in development mode:

```bash
# Start dependencies
docker-compose up -d db

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server with reload
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token

### User Management
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Practice Tracking
- `POST /api/v1/practice/sessions` - Create new practice session
- `GET /api/v1/practice/sessions` - List user's practice sessions
- `GET /api/v1/practice/sessions/{session_id}` - Get session details

### Challenges
- `POST /api/v1/challenge/send` - Send a challenge to another user
- `GET /api/v1/challenge` - List user's challenges
- `PUT /api/v1/challenge/{challenge_id}/accept` - Accept a challenge
- `PUT /api/v1/challenge/{challenge_id}/decline` - Decline a challenge

### Dashboard
- `GET /api/v1/dashboard/{user_id}` - Get user's performance metrics

### Advisor
- `GET /api/v1/advisor/recommendation/{user_id}` - Get practice recommendations

### Admin
- `GET /api/v1/admin/users` - List all users (admin only)
- `PUT /api/v1/admin/users/{user_id}/make-admin` - Make user admin
- `PUT /api/v1/admin/users/{user_id}/deactivate` - Deactivate a user

## Database Schema

The application uses the following key models:

- **User**: Authentication and profile data
- **Session**: Practice session details
- **Shot**: Individual shots during practice
- **Drill**: Structured practice activities
- **Challenge**: Competitions between users

## License

[MIT License](LICENSE)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
