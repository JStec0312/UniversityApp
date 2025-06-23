# Development Guide

This guide provides instructions for developers contributing to the UniversityApp project.

## Environment Setup

### Prerequisites

- Python 3.10 or higher
- Git
- PostgreSQL (optional, SQLite can be used for development)

### Setting Up the Development Environment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/UniversityApp.git
   cd UniversityApp
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```
   DATABASE_URL=sqlite:///./dev.db
   SECRET_KEY=your_development_secret_key
   ```

5. Initialize the database:
   ```
   python -m app.db_init
   ```

## Development Workflow

### Running the Application

```
uvicorn app.main:app --reload
```

The application will be available at http://localhost:8000.

### FastAPI Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Adding New Features

#### Step 1: Create a new branch

```
git checkout -b feature/your-feature-name
```

#### Step 2: Implement your changes

Follow these steps when adding new functionality:

1. **Add/update model**: Define the data structure in `app/models/`
2. **Create/update repository**: Implement data access in `app/repositories/`
3. **Create/update schema**: Define validation in `app/schemas/`
4. **Implement service**: Add business logic in `app/services/`
5. **Create API endpoint**: Define API route in `app/api/`
6. **Write tests**: Add tests in `tests/`

#### Step 3: Run tests

```
pytest
```

#### Step 4: Submit a pull request

```
git push origin feature/your-feature-name
```

## Code Standards

### Python Style Guide

- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes with docstrings

### Commit Messages

Follow the conventional commits format:

```
feat: add user authentication
fix: correct database connection issue
docs: update API documentation
test: add tests for user repository
refactor: improve error handling
```

## Database Migrations

*Note: Migration system to be implemented*

## Testing

### Running Tests

Run all tests:
```
pytest
```

Run specific test files:
```
pytest tests/RepositoryTest/
pytest tests/ApiTests/
```

### Testing Approach

1. **Repository Tests**: Test database operations in isolation using SQLite in-memory database
2. **API Tests**: Test API endpoints using FastAPI TestClient with SQLite in-memory database
3. **Integration Tests**: Test full application flows including services

### Test Database Configuration

The tests use an in-memory SQLite database to avoid affecting the development or production database:

```python
# Example conftest.py for API tests
@pytest.fixture
def test_client():
    # Create an in-memory SQLite database for testing
    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Override the get_db dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    client = TestClient(app)
    
    # Return the test client
    yield client
    
    # Clean up - drop all tables
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
```

### Common Testing Issues

1. **Circular Import Dependencies**: Ensure your models and repositories avoid circular imports by:
   - Using string-based relationship references
   - Using explicit foreign key declarations in relationships
   - Implementing lazy imports in repository factory classes

2. **Test Isolation**: Each test should start with a clean database state. Use fixtures with scope="function" to reset the database between tests.
