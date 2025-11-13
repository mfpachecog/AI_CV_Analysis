# Startup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` file with your configuration (optional for development with SQLite).

### 3. Initialize Database

Run the database initialization script:
```bash
python scripts/init_db.py
```

Or use Python directly:
```python
from src.services.database import DatabaseService
DatabaseService.init_db()
```

### 4. Run the Server

**Option 1: Using the run script**
```bash
python scripts/run_server.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using Python**
```python
from src.main import app
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000/

## API Endpoints

All user endpoints are prefixed with `/api/v1/users`:

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - List all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/username/{username}` - Get user by username
- `GET /api/v1/users/email/{email}` - Get user by email
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## Project Structure

```
Grupo04/
├── database/
│   └── user.py              # Database session and configuration
├── src/
│   ├── api/
│   │   └── routers/
│   │       └── user.py      # User API endpoints
│   ├── models/
│   │   └── user.py          # User database model
│   ├── schemas/
│   │   └── user.py          # Pydantic schemas for validation
│   ├── services/
│   │   ├── user.py          # User business logic
│   │   ├── database.py     # Database management
│   │   ├── config.py        # Configuration service
│   │   ├── lifecycle.py     # App lifecycle management
│   │   └── utils.py         # Utility functions
│   └── main.py              # FastAPI application
├── scripts/
│   ├── init_db.py           # Database initialization script
│   └── run_server.py        # Server startup script
└── .env.example             # Environment variables template
```

## Services Overview

### UserService
- User CRUD operations
- Password hashing and verification
- User authentication
- Validation checks

### DatabaseService
- Database initialization
- Table creation
- Connection management
- Database utilities

### ConfigService
- Application settings
- Environment variable management
- Configuration access

### LifecycleService
- Application startup/shutdown
- Database initialization on startup
- Resource cleanup on shutdown

### UtilsService
- File handling utilities
- File validation
- Common helper functions

## Development

### Database Management

**Initialize database:**
```python
from src.services.database import DatabaseService
DatabaseService.init_db()
```

**Recreate database (WARNING: Deletes all data):**
```python
from src.services.database import DatabaseService
DatabaseService.recreate_db()
```

**Check database connection:**
```python
from src.services.database import DatabaseService
DatabaseService.check_connection()
```

## Troubleshooting

### Database Connection Issues
- Check `DATABASE_URL` in `.env` file
- Ensure database server is running (if using PostgreSQL/MySQL)
- Check file permissions for SQLite database

### Import Errors
- Ensure you're running from project root
- Check Python path includes project directory
- Verify all dependencies are installed

### Port Already in Use
- Change port in `scripts/run_server.py` or uvicorn command
- Kill process using port 8000: `lsof -ti:8000 | xargs kill`

