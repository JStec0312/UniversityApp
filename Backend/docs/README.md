# UniversityApp Backend

This document provides a detailed overview of the backend architecture and components of the UniversityApp project.

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL/SQLite
- **Testing**: pytest
- **Authentication**: JWT (to be implemented)

## Project Structure

```
Backend/
├── app/
│   ├── __init__.py
│   ├── db_init.py
│   ├── main.py
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality and configuration
│   │   └── db.py
│   ├── models/           # Database models
│   ├── repositories/     # Data access layer
│   ├── schemas/          # Pydantic models for validation
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
└── tests/                # Test suite
    └── RepositoryTest/   # Repository tests
```

## Components

### Models

Database models represent the application's data structure. Each model corresponds to a table in the database.

Key models include:
- `User`: Base user entity
- `Student`: User with student-specific attributes
- `Admin`: User with administrative privileges
- `University`: University entity
- `Faculty`: Faculty within a university
- `Major`: Academic majors
- `News`: University news items
- `Event`: University events
- `EventRSVP`: Event registrations
- `Discount`: Student discounts
- `ForumPost`: Forum discussions

### Repositories

Repositories implement the data access layer, providing CRUD operations for each model. The repository pattern abstracts the database interactions from the business logic.

The `BaseRepository` class provides common operations that are inherited by model-specific repositories:
- `get_by_id`: Retrieve an entity by ID
- `create`: Create a new entity
- `update_by_id`: Update an existing entity
- `delete_by_id`: Delete an entity by ID

### Schemas

Schemas define the data validation and serialization rules using Pydantic models. They ensure that data passing through the API conforms to expected formats.

### Database

The application uses SQLAlchemy ORM with a configurable database backend. The default is SQLite for development, but it can be configured to use PostgreSQL for production.

Database connection is managed in `app/core/db.py`.

## Development Guidelines

### Adding a New Model

1. Create a new model file in the `app/models` directory
2. Define the model class extending `BaseModel`
3. Create a corresponding repository in `app/repositories`
4. Define schemas in `app/schemas`
5. Implement services in `app/services` if needed
6. Create API endpoints in `app/api`
7. Add tests in the `tests` directory

### Testing

The project uses pytest for testing. Repository tests are located in the `tests/RepositoryTest` directory.

Run tests with:
```
pytest
```

## Future Enhancements

- Implement authentication and authorization
- Add API documentation with Swagger/ReDoc
- Implement caching
- Add logging
- Set up CI/CD pipeline
