# Database Schema

This document outlines the database schema for the UniversityApp.

## Entity Relationship Diagram

```
┌───────────┐       ┌───────────┐       ┌───────────┐
│           │       │           │       │           │
│  Users    │───────│  Students │───────│  Majors   │
│           │       │           │       │           │
└───────────┘       └───────────┘       └───────────┘
      │                   │                   │
      │                   │                   │
      │               ┌───────────┐       ┌───────────┐
      │               │           │       │           │
      └───────────────│ Universities│─────│ Faculties │
      │               │           │       │           │
      │               └───────────┘       └───────────┘
      │                   │                   
      │                   │                   
┌───────────┐       ┌───────────┐       ┌───────────┐
│           │       │           │       │           │
│  Admins   │       │   News    │       │  Events   │
│           │       │           │       │           │
└───────────┘       └───────────┘       └───────────┘
                                              │
                                              │
┌───────────┐       ┌───────────┐       ┌───────────┐
│           │       │           │       │           │
│ForumPosts │       │ Discounts │       │EventRSVPs │
│           │       │           │       │           │
└───────────┘       └───────────┘       └───────────┘
```

## Tables

### Users

The core user entity for all system users.

| Column          | Type         | Constraints                |
|-----------------|--------------|----------------------------|
| id              | Integer      | Primary Key, Auto-increment |
| email           | String(255)  | Unique, Not Null, Indexed  |
| hashed_password | String(255)  | Not Null                   |
| display_name    | String(255)  | Nullable                   |
| verified        | Boolean      | Not Null, Default: false   |
| university_id   | Integer      | Foreign Key, Nullable      |
| created_at      | DateTime     | Not Null, Default: now     |
| updated_at      | DateTime     | Not Null, Default: now     |

### Students

Extends the User entity with student-specific attributes.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| user_id          | Integer      | Foreign Key, Not Null      |
| faculty_id       | Integer      | Foreign Key, Nullable      |
| major_id         | Integer      | Foreign Key, Nullable      |
| graduation_year  | Integer      | Nullable                   |
| student_id_number| String(50)   | Unique, Not Null          |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### Admins

Extends the User entity with admin-specific attributes.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| user_id          | Integer      | Foreign Key, Not Null      |
| role             | String(50)   | Not Null                   |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### Universities

Represents university entities.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| name             | String(255)  | Not Null                   |
| location         | String(255)  | Nullable                   |
| website          | String(255)  | Nullable                   |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### Faculties

Represents faculties within universities.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| name             | String(255)  | Not Null                   |
| university_id    | Integer      | Foreign Key, Not Null      |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### Majors

Represents academic majors within faculties.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| name             | String(255)  | Not Null                   |
| faculty_id       | Integer      | Foreign Key, Not Null      |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### News

Represents university news items.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| title            | String(255)  | Not Null                   |
| content          | Text         | Not Null                   |
| university_id    | Integer      | Foreign Key, Not Null      |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### Events

Represents university events.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| title            | String(255)  | Not Null                   |
| description      | Text         | Not Null                   |
| start_time       | DateTime     | Not Null                   |
| end_time         | DateTime     | Not Null                   |
| location         | String(255)  | Nullable                   |
| university_id    | Integer      | Foreign Key, Not Null      |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### EventRSVPs

Represents user registrations for events.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| event_id         | Integer      | Foreign Key, Not Null      |
| user_id          | Integer      | Foreign Key, Not Null      |
| status           | String(20)   | Not Null                   |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### ForumPosts

Represents forum discussions.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| title            | String(255)  | Not Null                   |
| content          | Text         | Not Null                   |
| category         | String(50)   | Nullable                   |
| user_id          | Integer      | Foreign Key, Not Null      |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

### Discounts

Represents student discounts.

| Column           | Type         | Constraints                |
|------------------|--------------|----------------------------|
| id               | Integer      | Primary Key, Auto-increment |
| title            | String(255)  | Not Null                   |
| description      | Text         | Not Null                   |
| valid_from       | DateTime     | Not Null                   |
| valid_to         | DateTime     | Not Null                   |
| university_id    | Integer      | Foreign Key, Not Null      |
| created_at       | DateTime     | Not Null, Default: now     |
| updated_at       | DateTime     | Not Null, Default: now     |

## Relationships

- **User to University**: Many-to-One (A user belongs to at most one university)
- **User to Student**: One-to-One (A user can have one student profile)
- **User to Admin**: One-to-One (A user can have one admin profile)
- **Student to Faculty**: Many-to-One (A student belongs to one faculty)
- **Student to Major**: Many-to-One (A student has one major)
- **Faculty to University**: Many-to-One (A faculty belongs to one university)
- **Major to Faculty**: Many-to-One (A major belongs to one faculty)
- **News to University**: Many-to-One (A news item belongs to one university)
- **Event to University**: Many-to-One (An event belongs to one university)
- **EventRSVP to Event**: Many-to-One (An RSVP is for one event)
- **EventRSVP to User**: Many-to-One (An RSVP is made by one user)
- **ForumPost to User**: Many-to-One (A forum post is created by one user)
- **Discount to University**: Many-to-One (A discount belongs to one university)

## Indexes

- `users.email`: For fast user lookup by email
- `students.student_id_number`: For fast student lookup by ID number
- `events.start_time`: For efficient querying of upcoming events
- `forum_posts.category`: For filtering posts by category
