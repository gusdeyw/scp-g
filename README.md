# SCP-G (Code Generator)

A modern full-stack web application with an integrated code generation system. Generate complete Go Fiber API projects with CRUD operations based on your database models.

## 🚀 Features

- **Full-Stack Architecture**: Astro frontend + Python Flask backend + Go API generation
- **Code Generation**: Generate complete Go Fiber projects with REST APIs
- **Database Management**: SQLite-based model and field management
- **Modern UI**: Clean Astro-based interface with Tailwind CSS
- **API-First**: RESTful APIs with comprehensive CRUD operations
- **Development Ready**: Hot reload, testing, and production deployment support

## 🏗️ Architecture

```
scp-g/
├── apps/                    # Frontend (Astro + Tailwind CSS)
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── layouts/         # Page layouts
│   │   ├── pages/           # Route pages
│   │   └── styles/          # Global styles
│   └── public/              # Static assets
├── api/                     # Backend API (Python Flask)
│   ├── app.py              # Main Flask application
│   ├── routes.py           # API endpoints
│   ├── generate_go.py      # Go code generation
│   ├── requirements.txt    # Python dependencies
│   └── test_api.py         # API tests
└── go/                     # Generated Go projects (example)
    ├── main.go            # Fiber application
    ├── models/            # Data models
    └── handlers/          # CRUD handlers
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Astro](https://astro.build/) v5.14.6
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) v4.1.14
- **Build Tool**: Vite (integrated with Astro)

### Backend
- **API Framework**: [Flask](https://flask.palletsprojects.com/) 3.0.3
- **Database**: SQLite3
- **Code Generation**: Python-based Go project generator

### Generated Go Projects
- **Framework**: [Fiber](https://gofiber.io/) v2.52.5
- **Language**: Go 1.21+
- **Features**: REST API, CRUD operations, in-memory storage

## 📋 Prerequisites

- **Node.js** 18+ (for Astro frontend)
- **Python** 3.8+ (for Flask backend)
- **Go** 1.21+ (for generated projects)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/gusdeyw/scp-g.git
cd scp-g
```

### 2. Setup Backend (Python Flask)
```bash
cd api
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python app.py
```
Backend runs on: `http://localhost:5000`

### 3. Setup Frontend (Astro)
```bash
cd apps
npm install
npm run dev
```
Frontend runs on: `http://localhost:4321`

## 🎯 API Endpoints

### Configuration Management
```http
GET    /api/config           # Get all configs
GET    /api/config/{key}     # Get config by key
PUT    /api/config/{key}     # Update config value
```

### Model Management
```http
GET    /api/model            # Get all models
POST   /api/model            # Create new model
GET    /api/model/{code}     # Get model by code
PUT    /api/model/{code}     # Update model
DELETE /api/model/{code}     # Delete model
```

### Model Details (Fields)
```http
GET    /api/model_detail              # Get all model details
POST   /api/model_detail              # Create model detail
GET    /api/model_detail/{code}       # Get detail by code
PUT    /api/model_detail/{code}       # Update detail
DELETE /api/model_detail/{code}       # Delete detail
```

### Code Generation
```http
GET    /api/generate_go      # Generate and download Go project ZIP
```

## 🔧 Configuration

Set the language for code generation:
```bash
curl -X PUT http://localhost:5000/api/config/LANG \
  -H "Content-Type: application/json" \
  -d '{"value_conf": "Go"}'
```

## 📝 Creating Models

### 1. Create a Model
```bash
curl -X POST http://localhost:5000/api/model \
  -H "Content-Type: application/json" \
  -d '{
    "table_code": "users",
    "table_name": "Users"
  }'
```

### 2. Add Model Fields
```bash
curl -X POST http://localhost:5000/api/model_detail \
  -H "Content-Type: application/json" \
  -d '{
    "model_code": "users",
    "model_detail_code": "id",
    "model_detail_name": "ID",
    "model_detail_type": "id"
  }'

curl -X POST http://localhost:5000/api/model_detail \
  -H "Content-Type: application/json" \
  -d '{
    "model_code": "users",
    "model_detail_code": "name",
    "model_detail_name": "Name",
    "model_detail_type": "varchar"
  }'
```

### 3. Generate Go Project
```bash
curl -O -J http://localhost:5000/api/generate_go
```

## 🏃‍♂️ Development

### Backend Development
```bash
cd api
python app.py              # Start Flask server
pytest                    # Run tests
black .                   # Format code
flake8 .                  # Lint code
```

### Frontend Development
```bash
cd apps
npm run dev              # Start dev server
npm run build            # Build for production
npm run preview          # Preview production build
```

### Generated Go Projects
```bash
cd generated_project
go mod tidy              # Install dependencies
go run main.go           # Start the generated API
```

## 🧪 Testing

### API Testing
```bash
cd api
pytest test_api.py
```

### Manual Testing
Import `api/postman_collection.json` into Postman for comprehensive API testing.

## 🚢 Deployment

### Backend (Production)
```bash
cd api
gunicorn --bind 0.0.0.0:8000 app:app
```

### Frontend (Production)
```bash
cd apps
npm run build
# Deploy the dist/ folder to your web server
```

## 📁 Project Structure Details

### Frontend (`apps/`)
- `src/components/` - Reusable Astro components
- `src/layouts/` - Page layout templates
- `src/pages/` - File-based routing
- `src/styles/` - Global CSS and Tailwind config

### Backend (`api/`)
- `app.py` - Flask application factory
- `routes.py` - API route definitions
- `generate_go.py` - Go code generation logic
- `production.db` - SQLite database

### Generated Go Projects
- `main.go` - Fiber application with routes
- `models/` - Go structs for data models
- `handlers/` - CRUD operation handlers
- `go.mod` - Go module dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Astro](https://astro.build/) - The web framework for content-driven websites
- [Flask](https://flask.palletsprojects.com/) - The Python micro framework
- [Fiber](https://gofiber.io/) - Express-inspired web framework for Go
- [Tailwind CSS](https://tailwindcss.com/) - A utility-first CSS framework

---

**Made with ❤️ for developers who want to generate code faster**

