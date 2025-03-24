# ProdigyAI Flask Backend

This is the Flask backend for ProdigyAI, an intelligent productivity assistant that adapts to your workflow using advanced AI and natural language processing.

## Features

- **User Authentication**: Secure JWT-based authentication with password hashing
- **Task Management**: Create, read, update, and delete tasks with priorities and categories
- **Habit Tracking**: Track habits with custom targets, types, and progress
- **Natural Language Processing**: Advanced text analysis using spaCy
- **Sentiment Analysis**: Detect user emotions and provide productivity insights
- **Machine Learning**: Task suggestions based on user patterns and context
- **API-First Design**: Clean, RESTful API endpoints for all features
- **SQL Database**: Robust data persistence with MySQL and SQLAlchemy ORM

## Technologies Used

- **Flask**: Lightweight and flexible Python web framework
- **SQLAlchemy**: SQL toolkit and ORM for database interactions
- **JWT**: JSON Web Tokens for secure authentication
- **spaCy**: Industrial-grade natural language processing
- **Pandas & NumPy**: Data analysis and manipulation
- **scikit-learn**: Machine learning utilities

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download the spaCy language model:
   ```
   python -m spacy download en_core_web_md
   ```

5. Copy `.env.example` to `.env` and configure your environment variables

6. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. Run the development server:
   ```
   flask run
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Authenticate user and receive token
- `GET /api/auth/me`: Get current user information
- `PUT /api/auth/update`: Update user information

### Tasks

- `GET /api/tasks`: Get all tasks for the current user
- `POST /api/tasks`: Create a new task
- `GET /api/tasks/:id`: Get a specific task
- `PUT /api/tasks/:id`: Update a task
- `DELETE /api/tasks/:id`: Delete a task

### Habits

- `GET /api/habits`: Get all habits for the current user
- `POST /api/habits`: Create a new habit
- `GET /api/habits/:id`: Get a specific habit
- `PUT /api/habits/:id`: Update a habit
- `DELETE /api/habits/:id`: Delete a habit

### Habit Progress

- `GET /api/habit-progress/:habitId`: Get progress for a specific habit
- `POST /api/habit-progress/:habitId`: Add progress for a habit
- `DELETE /api/habit-progress/:progressId/delete`: Delete a progress entry

## Project Structure

```
flask-backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── models/             # Database models
│   ├── __init__.py
│   ├── db.py           # Database instance
│   ├── user.py         # User model
│   ├── task.py         # Task model
│   ├── habit.py        # Habit model
│   └── habit_progress.py # Habit progress model
├── routes/             # API routes
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── tasks.py        # Task routes
│   ├── habits.py       # Habit routes
│   └── habit_progress.py # Habit progress routes
├── services/           # Business logic services
│   ├── __init__.py
│   ├── nlp_service.py  # Natural language processing service
│   ├── sentiment_service.py # Sentiment analysis service
│   └── ml_service.py   # Machine learning predictor service
└── utils/              # Utility functions
    ├── __init__.py
    └── auth.py         # Authentication helpers
```

## Integration with Frontend

The backend serves API endpoints that are consumed by the React frontend. Communication happens through HTTP requests with JSON payloads.

## License

MIT 