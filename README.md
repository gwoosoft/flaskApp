# FlaskApp

A Flask-based REST API application with JWT authentication, admin roles, and PostgreSQL database support. Designed as a base template for backend projects with scalable architecture.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **User Management** - User registration and login
- 🔑 **Admin Roles** - Role-based access control (admin/user)
- 🗄️ **PostgreSQL Database** - Robust database support
- 🐳 **Docker Support** - Containerized deployment
- ⚖️ **Load Balancing** - Nginx load balancer with multiple Flask instances
- ✅ **Type Checking** - MyPy support for type safety
- 📝 **Pydantic Validation** - Request/response validation

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- PostgreSQL (if running without Docker)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd flaskApp
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mydb
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
```

**Important:** Change `JWT_SECRET_KEY` to a secure random string in production!

## Running the Application

### Option 1: Local Development (without Docker)

1. **Start PostgreSQL database:**
   ```bash
   docker-compose up -d db
   ```

2. **Run the Flask app:**
   ```bash
   source venv/bin/activate
   python run.py
   ```

   The app will be available at `http://localhost:5000`

### Option 2: Docker Compose (Recommended)

**Run with load balancer (3 Flask instances + Nginx):**

```bash
./flaskdev.sh
```

Or manually:

```bash
docker-compose build
docker-compose up -d
```

The app will be available at `http://localhost` (port 80)

**Stop the application:**
```bash
docker-compose down
```

### Option 3: Database Only (Docker)

If you want to run only the database in Docker:

```bash
docker-compose up -d db
```

## Database Setup

### Initial Setup

The database tables are automatically created when the app starts. However, if you need to reset the database:

**Option 1: Drop and recreate (loses all data):**
```bash
docker exec -it <flask_container_name> python
```
Then in Python:
```python
from app import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
```

**Option 2: Fresh start with Docker:**
```bash
docker-compose down
docker volume rm flaskapp_db_data
docker-compose up -d
```

### Setup First Admin User

Before using admin features, create the first admin user:

```bash
# Using default credentials (admin@example.com / admin123)
docker exec -it <flask_container_name> python setup_admin.py

# Using custom credentials
docker exec -it <flask_container_name> python setup_admin.py \
  --email admin@example.com \
  --password your_secure_password \
  --name "Admin User"
```

## API Documentation

### Base URL

- **Local:** `http://localhost:5000`
- **Docker:** `http://localhost` (port 80)

### Authentication Endpoints

#### 1. Register User (Public)

```bash
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** Public registration always creates users with "user" role (admin role is ignored for security).

#### 2. Login

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:** Same as register endpoint (includes access_token)

#### 3. Get Current User (Protected)

```bash
GET /auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

### User Management Endpoints

#### 4. Create User (Admin Only)

```bash
POST /users
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "password456",
  "role": "user"  # or "admin"
}
```

#### 5. Get User by ID (Protected)

```bash
GET /users/<user_id>
Authorization: Bearer <token>
```

### Error Responses

**401 Unauthorized:**
```json
{
  "error": "Invalid email or password",
  "code": "unauthorized"
}
```

**403 Forbidden:**
```json
{
  "error": "Admin access required",
  "code": "forbidden"
}
```

**400 Validation Error:**
```json
{
  "error": "Name is required",
  "code": "validation_error",
  "field": "name"
}
```

For complete API examples with curl commands, see [CURL_EXAMPLES.md](./CURL_EXAMPLES.md).

## Project Structure

```
flaskApp/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── extensions.py        # Flask extensions (db, jwt)
│   ├── models/              # SQLAlchemy models
│   │   └── user.py
│   ├── repositories/        # Data access layer
│   │   └── user_repository.py
│   ├── services/            # Business logic
│   │   └── user_service.py
│   ├── facades/             # API layer
│   │   └── user_facade.py
│   ├── routes/              # API routes
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   ├── dtos/                # Data transfer objects
│   │   ├── user_dto.py
│   │   ├── login_dto.py
│   │   └── register_dto.py
│   ├── errors/               # Custom exceptions
│   │   └── errors.py
│   └── utils/               # Utility functions
│       └── auth_utils.py
├── docker-compose.yml       # Docker configuration
├── Dockerfile               # Flask container definition
├── nginx.conf               # Nginx load balancer config
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── setup_admin.py           # Admin user setup script
└── README.md                # This file
```

## Development

### Type Checking

Run MyPy to check for type errors:

```bash
mypy run.py
```

### Code Style

The project uses:
- **Pydantic** for data validation
- **SQLAlchemy** for ORM
- **Flask-JWT-Extended** for authentication

### Architecture

The application follows a layered architecture:

1. **Routes** - Handle HTTP requests/responses
2. **Facades** - Transform DTOs and coordinate services
3. **Services** - Business logic
4. **Repositories** - Data access
5. **Models** - Database models

## Security Notes

- ⚠️ **Always change `JWT_SECRET_KEY` in production**
- ⚠️ **Use strong passwords in production**
- ⚠️ **Enable HTTPS in production**
- ⚠️ **Regularly update dependencies**

## Future Enhancements

- [ ] Google OAuth authentication
- [ ] Facebook OAuth authentication
- [ ] Apple Sign-In
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Rate limiting
- [ ] API versioning

## Contributing

Feel free to use this as a base for your projects. If you make improvements, contributions are welcome!

## License

Copyright © 2026 gwsoft. All rights reserved.

## Support

For issues and questions, please open an issue in the repository.
