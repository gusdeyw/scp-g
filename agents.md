# SCP-G Project Architecture

## Overview
This is a full-stack web application with a modern frontend and backend architecture. The project consists of an Astro-based frontend application and a Python Flask backend API.

## Project Structure

```
scp-g/
├── apps/                    # Frontend Application (Astro)
│   ├── src/
│   │   ├── components/      # Reusable Astro components
│   │   ├── layouts/         # Page layouts
│   │   ├── pages/           # Route pages
│   │   └── styles/          # Global styles
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   └── astro.config.mjs     # Astro configuration
├── api/                     # Backend API (Python Flask)
│   ├── app.py              # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── test_api.py         # API tests
└── old/                    # Legacy PHP files (deprecated)
```

## Frontend (Astro) - `/apps`

### Technology Stack
- **Framework**: Astro v5.14.6
- **Styling**: Tailwind CSS v4.1.14
- **Build Tool**: Vite (integrated with Astro)
- **Language**: TypeScript/JavaScript

### Key Features
- Static Site Generation (SSG) with partial hydration
- Component-based architecture
- Tailwind CSS for styling
- Modern ES modules

### Available Scripts
```bash
cd apps
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Components Structure
- `Navbar.astro` - Navigation component
- `Sidebar.astro` - Sidebar navigation
- `Welcome.astro` - Welcome/landing component

### Pages
- `index.astro` - Homepage
- `database.astro` - Database interface page

## Backend (Python Flask) - `/api`

### Technology Stack
- **Framework**: Flask 3.0.3
- **HTTP Client**: Requests 2.32.3
- **Language**: Python

### API Endpoints
- `GET /` - Welcome message
- `GET /api/data` - Retrieve sample data
- `POST /api/data` - Create new data entry

### Running the Backend
```bash
cd api
pip install -r requirements.txt
python app.py
```

The API runs on `http://localhost:5000` by default in debug mode.

## Development Workflow

### Frontend Development
1. Navigate to the `apps` directory
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`
4. Access at `http://localhost:4321` (default Astro port)

### Backend Development
1. Navigate to the `api` directory
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the Flask app: `python app.py`
6. Access at `http://localhost:5000`

## Agent Instructions

### For Frontend Changes
- Work primarily in the `/apps` directory
- Use Astro component syntax (.astro files)
- Follow Tailwind CSS conventions for styling
- Maintain TypeScript types where applicable
- Test components in isolation when possible

### For Backend Changes
- Work primarily in the `/api` directory
- Follow Flask best practices and patterns
- Maintain RESTful API conventions
- Add appropriate error handling
- Update `requirements.txt` when adding new dependencies
- Write tests in `test_api.py` for new endpoints

### For Full-Stack Features
- Ensure proper CORS configuration if needed
- Maintain consistent data formats between frontend and backend
- Document API changes in this file
- Consider both development and production environments

## Configuration Notes

### Astro Configuration
- Configured with Tailwind CSS via Vite plugin
- Uses ES modules (`"type": "module"`)
- Tailwind CSS v4 with PostCSS integration

### Flask Configuration
- Debug mode enabled for development
- CORS may need configuration for frontend integration
- Environment variables should be used for production settings

## Legacy Code
The `/old` directory contains deprecated PHP files that are no longer in active use. These should not be modified and are kept for reference only.

## Next Steps for Agents
1. **API Integration**: Connect the Astro frontend to the Flask backend
2. **Database**: Implement proper database integration (currently using sample data)
3. **Authentication**: Add user authentication system
4. **Deployment**: Set up production deployment configuration
5. **Testing**: Expand test coverage for both frontend and backend
6. **Documentation**: Keep this agents.md file updated with any architectural changes