# Contributing to SCP-G

Thank you for your interest in contributing to SCP-G! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Documentation](#documentation)

## 🤝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ (for Astro frontend)
- **Python** 3.8+ (for Flask backend)
- **Go** 1.21+ (for generated projects and testing)
- **Git** for version control

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/scp-g.git
   cd scp-g
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/gusdeyw/scp-g.git
   ```

## 🛠️ Development Setup

### Backend Setup (Python Flask)

```bash
cd api
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

### Frontend Setup (Astro)

```bash
cd apps
npm install
npm run dev
```

### Database Setup

The project uses SQLite. The database is automatically created when you run the Flask app for the first time.

## 🏗️ Project Structure

```
scp-g/
├── apps/                    # Frontend (Astro)
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── layouts/         # Page layouts
│   │   ├── pages/           # Routes
│   │   └── styles/          # Stylesheets
│   ├── public/              # Static assets
│   └── package.json
├── api/                     # Backend (Flask)
│   ├── app.py              # Main application
│   ├── routes.py           # API routes
│   ├── generate_go.py      # Code generation
│   ├── requirements.txt    # Dependencies
│   ├── test_api.py         # Tests
│   └── production.db       # Database
├── go/                     # Example Go project
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
└── LICENSE                # License information
```

## 🔄 Development Workflow

### 1. Choose an Issue

- Check the [Issues](https://github.com/gusdeyw/scp-g/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes

- Write clear, focused commits
- Test your changes thoroughly
- Follow the coding standards below

### 4. Test Your Changes

```bash
# Backend tests
cd api
pytest

# Frontend build check
cd apps
npm run build
```

### 5. Submit a Pull Request

- Push your branch to your fork
- Create a Pull Request with a clear description
- Reference any related issues

## 💻 Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Use meaningful variable and function names
- Keep functions small and focused (single responsibility)

**Code Formatting:**
```bash
cd api
black .                    # Format code
flake8 .                   # Check style
```

**Example:**
```python
def get_user(user_id: int) -> dict:
    """
    Retrieve a user by ID.

    Args:
        user_id: The user's unique identifier

    Returns:
        User data as a dictionary

    Raises:
        ValueError: If user_id is invalid
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    # Implementation here
    pass
```

### JavaScript/TypeScript (Frontend)

- Use modern ES6+ syntax
- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use meaningful component and variable names
- Write JSDoc comments for complex functions
- Use TypeScript for type safety

**Code Formatting:**
```bash
cd apps
npm run format            # Format code (if configured)
npm run lint              # Check for issues
```

**Example:**
```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

const UserCard: React.FC<{ user: User }> = ({ user }) => {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
};
```

### Go (Generated Code)

- Follow standard Go formatting (`go fmt`)
- Use meaningful package, struct, and function names
- Write comments for exported functions and types
- Handle errors appropriately
- Follow Go naming conventions

## 🧪 Testing

### Backend Testing

```bash
cd api
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -k "test_name"     # Run specific test
pytest --cov=.           # Coverage report
```

**Writing Tests:**
```python
import pytest
from app import app

def test_get_user():
    with app.test_client() as client:
        response = client.get('/api/user/1')
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert 'name' in data

def test_create_user():
    with app.test_client() as client:
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        response = client.post('/api/user',
                             json=user_data,
                             content_type='application/json')
        assert response.status_code == 201
```

### Frontend Testing

```bash
cd apps
npm test                 # Run tests (if configured)
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
```

### API Testing

Use the provided Postman collection (`api/postman_collection.json`) or test manually:

```bash
# Test health endpoint
curl http://localhost:5000/

# Test API endpoints
curl http://localhost:5000/api/config
```

## 📝 Submitting Changes

### Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep commits focused on a single change
- Reference issue numbers when applicable

**Examples:**
```
Add user authentication endpoint
Fix database connection timeout issue
Update README with installation instructions
Remove deprecated API endpoints
```

### Pull Request Process

1. **Create a Pull Request**
   - Use a clear, descriptive title
   - Provide a detailed description of changes
   - Reference related issues with `#issue-number`

2. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of the changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing completed
   - [ ] All tests pass

   ## Screenshots (if applicable)
   Add screenshots of UI changes

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Tests added for new features
   - [ ] All tests pass
   ```

3. **Code Review**
   - Address review comments promptly
   - Make requested changes
   - Keep the PR updated with main branch

4. **Merge**
   - PR will be merged by maintainers once approved
   - Delete your branch after merge

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python/Node versions)
- **Screenshots** if applicable
- **Error messages** or stack traces

### Feature Requests

For new features, please:

- **Check existing issues** to avoid duplicates
- **Describe the problem** the feature would solve
- **Explain the solution** you'd like to see
- **Consider alternatives** you've thought about

## 📚 Documentation

### Code Documentation

- Add docstrings to all Python functions
- Comment complex logic in all languages
- Update README.md for significant changes
- Update API documentation for endpoint changes

### README Updates

When making changes that affect users:

- Update installation instructions
- Add new features to the features list
- Update API documentation
- Include examples for new functionality

## 🎯 Areas for Contribution

### High Priority
- [ ] Frontend UI improvements
- [ ] Additional code generation templates
- [ ] Database integration options
- [ ] Authentication system
- [ ] API documentation improvements

### Medium Priority
- [ ] Unit test coverage improvements
- [ ] Performance optimizations
- [ ] Error handling improvements
- [ ] Logging system

### Good First Issues
- [ ] Documentation improvements
- [ ] Code formatting fixes
- [ ] Simple UI enhancements
- [ ] Test case additions

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the README and this file first

## 🙏 Recognition

Contributors will be recognized in:
- GitHub's contributor insights
- Release notes for significant contributions
- Project documentation

Thank you for contributing to SCP-G! 🚀