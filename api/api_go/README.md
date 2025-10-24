# Go API Backend

This is a Go backend implementation using Fiber and GORM that mimics the Python Flask API for the SCP-G CRUD Generator.

## Features

- RESTful API with the same endpoints as the Python version
- SQLite database with GORM ORM
- Fiber web framework
- Docker support

## API Endpoints

### Root
- `GET /` - Welcome message

### Configuration
- `GET /api/config` - Get all configurations
- `GET /api/config/{var_conf}` - Get specific configuration
- `PUT /api/config/{var_conf}` - Update configuration

### Models
- `GET /api/model` - Get all models
- `POST /api/model` - Create new model
- `GET /api/model/{table_code}` - Get specific model
- `PUT /api/model/{table_code}` - Update model
- `DELETE /api/model/{table_code}` - Delete model

### Model Details
- `GET /api/model_detail` - Get all model details
- `POST /api/model_detail` - Create new model detail
- `GET /api/model_detail/{model_detail_code}` - Get specific model detail
- `PUT /api/model_detail/{model_detail_code}` - Update model detail
- `DELETE /api/model_detail/{model_detail_code}` - Delete model detail

### Code Generation
- `GET /api/generate_go` - Generate Go project (requires LANG=Go config)

## Running Locally

### Prerequisites
- Go 1.21 or later
- SQLite

### Installation
```bash
cd api_go
go mod tidy
go run .
```

The API will be available at `http://localhost:5000`

## Running with Docker

### Build and Run
```bash
cd api_go
docker build -t scp-g-api-go .
docker run -p 5000:5000 scp-g-api-go
```

## Database

The application uses SQLite with a file named `production.db`. The database schema is automatically migrated on startup.

### Initial Configuration
The following configurations are seeded on first run:
- LANG: Go
- FRAMEWORK: Fiber
- DATABASE: SQLite

## Development

### Project Structure
```
api_go/
├── main.go          # Application entry point and routing
├── handlers.go      # API endpoint handlers
├── go.mod          # Go module dependencies
├── Dockerfile      # Docker configuration
├── .gitignore     # Git ignore rules
└── README.md      # This file
```

### Adding New Endpoints
1. Define the route in `main.go`
2. Implement the handler in `handlers.go`
3. Add any new models to the database models section

## Testing

You can test the API using the same Postman collection as the Python version, or use curl:

```bash
# Get all configs
curl http://localhost:5000/api/config

# Create a model
curl -X POST http://localhost:5000/api/model \
  -H "Content-Type: application/json" \
  -d '{"table_code": "users", "table_name": "Users"}'
```