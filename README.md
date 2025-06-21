# UniversityApp

A comprehensive university management application with features for students, administrators, and university staff.

## Project Overview

UniversityApp is a full-stack application designed to streamline university-related processes and enhance the student experience. The application includes features for managing student profiles, university news, events, forums, and administrative functions.

## Project Structure

The project is divided into two main components:

- **Backend**: A Python-based API built with FastAPI and SQLAlchemy
- **Frontend**: A web interface (technology details to be added)

## Backend Architecture

The backend follows a layered architecture pattern:

1. **Models**: Database entity definitions
2. **Repositories**: Data access layer for CRUD operations
3. **Schemas**: Data validation and serialization
4. **Services**: Business logic implementation
5. **API**: HTTP endpoints and controllers

### Key Features

- User authentication and authorization
- Student profile management
- University news and events
- Forum for student discussions
- Event RSVP system
- Student discounts management

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL or SQLite database

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/UniversityApp.git
   cd UniversityApp
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost/universityapp
   SECRET_KEY=your_secret_key
   ```

5. Initialize the database:
   ```
   python -m app.db_init
   ```

## Development

### Running the Application

```
uvicorn app.main:app --reload
```

### Running Tests

```
pytest
```

## Documentation

For more detailed documentation, please refer to:

- [Backend Documentation](./Backend/docs/README.md)
- [API Documentation](./Backend/docs/api.md)
- [Database Schema](./Backend/docs/database.md)

## License

[MIT License](LICENSE)
