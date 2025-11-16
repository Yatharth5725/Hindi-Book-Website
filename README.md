# Hindi Book Website

A full-stack Hindi book e-commerce website built with React, TypeScript, FastAPI, and SQLite.

## Features

- Book catalog with pagination and filtering
- User authentication with JWT
- Shopping cart functionality
- Category browsing
- Search functionality
- Admin panel for book management

## Technologies

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Shadcn/ui, React Query
- **Backend**: FastAPI, SQLAlchemy, SQLite, JWT Authentication

## Getting Started

### Backend Setup

```bash
cd Backend
python -m venv backend-env
source backend-env/bin/activate  # On Windows: backend-env\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on: `http://localhost:8000`

### Frontend Setup

```bash
npm install
npm run dev
```

Frontend runs on: `http://localhost:8080`

## Project Structure

```
├── Backend/          # FastAPI backend
├── src/             # React frontend
│   ├── components/  # UI components
│   ├── pages/      # Page components
│   ├── hooks/      # Custom hooks
│   └── lib/        # Utilities
└── public/          # Static assets
```

## License

© 2024 Hindi Book Website. All rights reserved.
