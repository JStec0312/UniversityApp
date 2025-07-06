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

#### Isolated Database Approach

Each API test file uses its own isolated SQLite database to ensure test isolation. This approach:

1. Prevents test interdependencies
2. Allows parallel test execution
3. Makes tests more reliable and predictable

Example setup for a test file:

```python
# Create a unique database file for this test module
TEST_DB_FILE = f"./test_user_api_{uuid.uuid4()}.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_FILE}"

# Register database file for cleanup
register_db_for_cleanup(TEST_DB_FILE)

# Create engine and session factory
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Override the dependency
@pytest.fixture(scope="module")
def override_get_db():
    """Override the get_db dependency for testing."""
    def _override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Apply the override
    app.dependency_overrides[get_db] = _override_get_db
    
    # Return the override function for potential direct usage in tests
    return _override_get_db

@pytest.fixture(scope="module")
def client(override_get_db):
    """Create a test client for the FastAPI application."""
    with TestClient(app) as c:
        yield c
    
    # Clean up after all tests in this module are done
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    
    # Remove the test database file
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
```

#### Test Database Cleanup

The project includes a robust system to ensure all test database files are cleaned up after tests run:

1. Each test file registers its database file with the cleanup utility
2. A pytest session-level fixture removes all registered database files after tests complete
3. An `atexit` handler provides fallback cleanup if pytest exits unexpectedly
4. Stale database files (older than 1 hour) from failed previous runs are automatically cleaned up

This approach ensures that no test database files are left behind after test runs, keeping the workspace clean.

### Common Testing Issues

1. **Circular Import Dependencies**: Ensure your models and repositories avoid circular imports by:
   - Using string-based relationship references
   - Using explicit foreign key declarations in relationships
   - Implementing lazy imports in repository factory classes

2. **Test Isolation**: Each test should start with a clean database state. Use fixtures with `scope="function"` to reset the database between tests.

3. **Dependency Overrides**: Make sure to properly override database dependencies in tests to use the test database instead of the production one.

4. **Cleanup**: Always clean up resources after tests, including dropping tables and removing temporary database files.

## Code Documentation

### Documentation Standards

The project follows these documentation standards:

1. **Module Documentation**: Each Python module should start with a docstring that explains its purpose and contents:

   ```python
   """
   Student API endpoints module.

   This module provides routes for student registration, authentication, 
   and profile management.
   """
   ```

2. **Class Documentation**: Classes should have docstrings explaining their purpose, attributes, and usage:

   ```python
   class StudentRepository(BaseRepository[Student]):
       """
       Repository for Student entity database operations.
       
       This class provides methods for querying and manipulating Student records
       in the database, extending the base repository functionality.
       """
   ```

3. **Method Documentation**: Methods should have docstrings with descriptions, parameters, return values, and exceptions:

   ```python
   def get_by_email(self, email: str) -> Student | None:
       """
       Get a student by their email address.
       
       Args:
           email: The email address to search for
           
       Returns:
           Student: The found student or None if not found
           
       Raises:
           SQLAlchemyError: If there's a database error
       """
   ```

4. **Code Comments**: Use inline comments to explain complex logic, but prefer clear code that's self-documenting:

   ```python
   # Calculate age based on birth date
   age = (datetime.now().date() - birth_date).days // 365
   ```

### Documentation Tools

- **Type Hints**: Use Python type hints for better code understanding and IDE support
- **Docstrings**: Use Google-style or reST docstrings for consistency
- **Markdown**: Use Markdown for project documentation files
