# Recruitment System

A full-stack application for managing recruitment processes, built with Vue.js frontend and FastAPI backend.

## Project Structure

- `RKSD_Assignment/` - Main project directory
  - `frontend/`: Vue.js application with Tailwind CSS
  - `fastapi-app/`: FastAPI backend application with SQLAlchemy

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/yourusername/recruitment-system.git
cd recruitment-system/RKSD_Assignment
```

### Using Docker (Recommended)

The easiest way to run the application is using Docker Compose:

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup (Development)

#### Frontend Setup

```bash
cd RKSD_Assignment/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend development server will be available at http://localhost:5173

#### Backend Setup

```bash
cd RKSD_Assignment/fastapi-app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## GitHub Setup

1. Create a new repository on GitHub
2. Initialize the local repository and push to GitHub:

```bash
# Navigate to the project root
cd RKSD_Assignment

# Initialize git repository
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/recruitment-system.git
git push -u origin main
```

## License

[MIT](LICENSE) 