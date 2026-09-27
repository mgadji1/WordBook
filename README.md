# WordBook

WordBook is a simple web application for learning vocabulary.

The application allows users to:

* add words and their translations;
* view all saved words;
* search for a specific word;
* edit translations;
* delete words.

All vocabulary data is stored in a PostgreSQL database.

## Tech Stack

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Pydantic

### Frontend

* HTML
* CSS
* JavaScript
* Python `http.server`

### Infrastructure

* Docker
* Docker Compose

## Project Structure

```text
WordBook/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── config.py
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Running the Application

### Requirements

You only need:

* Docker
* Docker Compose

No local Python or PostgreSQL installation is required.

### 1. Clone the repository

```bash
git clone <repository-url>
cd WordBook
```

### 2. Create the environment file

Copy the example environment file:

```bash
cp .env.example .env
```

The default configuration is suitable for local development.

### 3. Start the application

Run:

```bash
docker compose up --build
```

Docker Compose will:

1. start PostgreSQL;
2. wait until PostgreSQL is ready;
3. run database migrations;
4. start the backend;
5. start the frontend.

### 4. Open the application

Open the following URL in your browser:

```text
http://localhost:3000
```

The backend API is available at:

```text
http://localhost:8080
```

## API

The backend provides the following endpoints:

| Method | Endpoint            | Description          |
| ------ | ------------------- | -------------------- |
| GET    | `/api/words`        | Get all words        |
| GET    | `/api/words/{word}` | Get a word by name   |
| POST   | `/api/words`        | Create a new word    |
| PUT    | `/api/words/{word}` | Update a translation |
| DELETE | `/api/words/{word}` | Delete a word        |

## Database Migrations

Database migrations are managed with Alembic.

Migrations are applied automatically when the application is started with Docker Compose.

To run migrations manually:

```bash
docker compose run --rm migrate
```

## Running Tests

Tests can be run inside the backend container:

```bash
docker compose exec backend python -m pytest
```

## Stopping the Application

To stop the containers:

```bash
docker compose stop
```

To stop and remove the containers and network:

```bash
docker compose down
```

To remove the database volume as well, if one is added later:

```bash
docker compose down -v
```

## Configuration

Application configuration is provided through environment variables.

The main variables are:

```env
POSTGRES_DB=wordbook
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/wordbook
BACKEND_PORT=8080
FRONTEND_PORT=3000
```

For local development, `.env` can be created from `.env.example`.
