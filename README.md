# Faculty Hours Gateway

API Gateway service for Faculty Hours system that handles authentication and routing between microservices.

## Tech Stack

- **Python 3.11**
- **FastAPI** - Modern, fast web framework for building APIs
- **Strawberry GraphQL** - GraphQL implementation for Python
- **Auth0** - Authentication and authorization platform
- **Poetry** - Dependency management
- **Docker** - Containerization
- **Uvicorn** - ASGI web server implementation

## Features

- Authentication and authorization using Auth0
- API Gateway routing to microservices
- GraphQL endpoint for payroll queries
- CORS support for frontend applications
- Session management
- Routing for faculty and report services

## Prerequisites

- Python 3.11
- Poetry
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd faculty-hours-gateway
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create `.env` file in the root directory with the following variables:
```
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_SESSION_SECRET=your-session-secret
```

## Running the Service

### Using Poetry

```bash
poetry run uvicorn gateway.main:app --reload --port 8000
```

### Using Docker

1. Build the Docker image:
```bash
docker build -t faculty-hours-gateway .
```

2. Run the container:
```bash
docker run -p 8000:8000 faculty-hours-gateway
```

## Service Connections

The gateway service connects to the following services:

- **Faculty Service** (`/faculty` endpoint)
- **Report Service** (`/report` endpoint)
- **Payroll Service** (`/payrolls` GraphQL endpoint)

## Development

1. Install development dependencies:
```bash
poetry install --with dev
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

## API Documentation

Once the service is running, you can access:
- REST API documentation at: `http://localhost:8000/docs`
- GraphQL playground at: `http://localhost:8000/payrolls`

## Testing

Run tests using pytest:
```bash
poetry run pytest
