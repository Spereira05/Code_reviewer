# Backend II Project

[![CI](https://github.com/USERNAME/backend_ii_project/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/backend_ii_project/actions/workflows/ci.yml)

## Project Structure

This project follows a standard FastAPI application structure with clear separation between models, schemas, and API endpoints.

### Directory Structure

```
backend_ii_project/
├── app/
│   ├── ai/                # AI-related functionality
│   ├── api/               # API endpoints and dependencies
│   │   ├── endpoints/     # API route handlers
│   │   └── dependencies.py
│   ├── crud/              # CRUD operations for database interaction
│   ├── db/                # Database configuration
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── base_model.py         # Base model class
│   │   ├── user_model.py         # User database model
│   │   └── submission_model.py   # Submission database model
│   ├── schemas/           # Pydantic schemas for request/response validation
│   │   ├── base_schema.py        # Base schema classes
│   │   ├── user_schema.py        # User API schemas
│   │   └── submission_schema.py  # Submission API schemas
│   └── main.py            # Application entry point
├── uploads/               # Directory for uploaded files
├── scripts/               # Utility scripts
├── compose.yaml           # Docker Compose configuration
├── Dockerfile             # Docker build configuration
└── tests/                 # Test directory
```

## Key Components

### Models vs Schemas

- **Models** (`app/models/`): SQLAlchemy ORM models that represent database tables
  - `base_model.py`: Base model class with common fields
  - `user_model.py`: User database model
  - `submission_model.py`: Submission and review database models
- **Schemas** (`app/schemas/`): Pydantic models used for request/response validation and serialization
  - `base_schema.py`: Base schema classes with common settings
  - `user_schema.py`: User API schemas
  - `submission_schema.py`: Submission and review API schemas

### API Structure

- **Endpoints** (`app/api/endpoints/`): Route handlers for API endpoints
- **Dependencies** (`app/api/dependencies.py`): FastAPI dependency functions

### AI Integration

- **Ollama Integration**: The application uses Ollama to analyze code submissions
- **Model**: The application uses the `tinyllama` model for code analysis (a smaller, faster alternative to `llama3`)
- **Process**: Code files are submitted, processed by Ollama, and results are stored in the database
- **Diagnostics**: Use the provided scripts to check Ollama status and models
  - `scripts/check-ollama.sh`: Bash script to check Ollama status and available models
  - `scripts/check_ollama_simple.py`: Python script for checking and testing Ollama models

### CRUD Operations

- **CRUD** (`app/crud/`): Database interaction functions for each model

## Running the Application

### Using Docker Compose (Recommended)

The application includes a Docker Compose configuration that sets up:
- The FastAPI application
- PostgreSQL database
- Ollama LLM service for code analysis

To run with Docker Compose:

```bash
cd backend_ii_project
docker compose up -d
```

This will:
1. Build the application image
2. Start the PostgreSQL database
3. Start the Ollama service with health checks
4. Pull the necessary Ollama model (`tinyllama`)
5. Test the model to ensure it's working properly
6. Start the FastAPI application

### Running Locally

To run the application without Docker:

```bash
cd backend_ii_project
uvicorn app.main:app --reload
```

Note: When running locally, you'll need to:
- Set up a PostgreSQL database
- Run Ollama separately at localhost:11434
- Pull the `tinyllama` model in Ollama using: `ollama pull tinyllama`
- If you encounter a 404 error, verify your model is properly installed using one of these commands:
  - `./scripts/check-ollama.sh localhost` (Bash script)
  - `python scripts/check_ollama_simple.py --host localhost` (Python script)

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Model Size Issues

The application now uses `tinyllama` instead of `llama3` because:
- It's much smaller (only ~1.1GB vs ~4.7GB for llama3)
- It downloads much faster
- It requires less memory to run
- It's suitable for code analysis tasks

If you want to use llama3 instead, you can set the `OLLAMA_MODEL` environment variable to `llama3` in the compose.yaml file, but be aware that it will take much longer to download and require more resources.

### Ollama Issues

If you encounter a 404 error when analyzing code:

1. Check if Ollama is running:
   ```bash
   # Inside Docker:
   curl http://ollama:11434/api/version
   
   # Running locally:
   curl http://localhost:11434/api/version
   ```

2. Check if the tinyllama model is available using our diagnostic tools:
   ```bash
   # Inside Docker:
   ./scripts/check-ollama.sh
   
   # Running locally:
   ./scripts/check-ollama.sh localhost
   
   # Alternative Python script:
   python scripts/check_ollama_simple.py --host localhost
   ```

3. Pull the model manually if needed:
   ```bash
   # Inside Docker:
   curl -X POST http://ollama:11434/api/pull -d '{"name":"tinyllama"}'
   
   # Running locally:
   curl -X POST http://localhost:11434/api/pull -d '{"name":"tinyllama"}'
   
   # Or use Ollama CLI:
   ollama pull tinyllama
   ```

4. Check the application logs for detailed error information:
   ```bash
   # View Docker container logs
   docker compose logs web
   
   # Filtering for errors
   docker compose logs web | grep ERROR
   ```

5. If you continue to have issues:
   - Make sure your system has enough resources (RAM, disk space)
   - Check if there are network issues between containers
   - Try restarting the Ollama service and the application