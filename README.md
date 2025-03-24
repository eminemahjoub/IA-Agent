# Personal Productivity Assistant

An AI-powered assistant designed to help users manage their daily tasks, schedules, and workflows.

## Features

- **Natural Language Processing**: Understand and respond to user commands in natural language
- **Task Management**: Add, prioritize, and remind users of tasks
- **Calendar Integration**: Sync with Google Calendar or Outlook to schedule meetings
- **Email Automation**: Draft emails, categorize incoming messages, and suggest responses
- **Focus Mode**: Monitor user activity and suggest breaks or focus periods
- **Habit Tracking**: Encourage users to build healthy habits (e.g., drinking water, exercising)

## AI Capabilities

This application leverages Natural Language Processing (NLP) to provide an intuitive interface for users. The AI assistant can:

- Process natural language commands like "add task finish report by tomorrow"
- Recognize user intents and extract relevant entities
- Perform actions based on understood commands
- Respond conversationally to user queries
- Learn from interactions to improve over time

## Tech Stack

- Frontend: React with Material-UI
- Backend: Node.js and Express
- Database: MySQL with Sequelize ORM
- Natural Language Processing (NLP) for understanding user commands
- APIs for calendar (Google Calendar, Outlook) and email services
- Machine learning models for habit prediction and task prioritization

## Setup Instructions

1. Clone the repository
2. Install server dependencies:
   ```
   npm install
   ```
3. Install client dependencies:
   ```
   npm run install-client
   ```
4. Set up a MySQL database and create a database named `productivity_assistant`
5. Create a `.env` file in the root directory with the following variables:
   ```
   NODE_ENV=development
   PORT=5000
   JWT_SECRET=your_jwt_secret
   JWT_EXPIRE=30d
   
   # MySQL Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=productivity_assistant
   DB_USER=root
   DB_PASSWORD=your_password
   
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   EMAIL_SERVICE=your_email_service
   EMAIL_USER=your_email_user
   EMAIL_PASSWORD=your_email_password
   ```
6. Run both the server and client:
   ```
   npm run dev
   ```

## Database Structure

The application uses MySQL with Sequelize ORM. The main tables are:

- **Users**: Store user information and settings
- **Tasks**: Track user tasks with priorities and due dates
- **Habits**: Track habits the user wants to build
- **HabitProgress**: Log daily progress for habits

## Usage

After setup, the application will be available at `http://localhost:3000`

## License

MIT 