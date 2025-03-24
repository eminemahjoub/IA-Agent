# Personal Productivity Assistant

An AI-powered assistant designed to help users manage their daily tasks, schedules, and workflows through natural language interaction.

## Features

- **Natural Language Processing**: Understand and respond to user commands in natural language
- **Task Management**: Add, prioritize, and remind users of tasks
- **Calendar Integration**: Sync with Google Calendar or Outlook to schedule meetings
- **Email Automation**: Draft emails, categorize incoming messages, and suggest responses
- **Focus Mode**: Monitor user activity and suggest breaks or focus periods
- **Habit Tracking**: Encourage users to build healthy habits (e.g., drinking water, exercising)

## Artificial Intelligence Capabilities

This application leverages Natural Language Processing (NLP) to provide an intuitive conversational interface. The AI assistant functions as a personal productivity coach that understands context and user habits.

### NLP Architecture

- **Intent Recognition**: Identifies the user's goal from natural language input
- **Entity Extraction**: Pulls out key information like dates, names, and task descriptions
- **Contextual Understanding**: Maintains conversation context for follow-up commands
- **Action Execution**: Translates understood commands into system actions
- **Conversational Response**: Generates human-like responses with appropriate information

### Supported Command Categories

1. **Task Management**
   - "Add task finish report by tomorrow"
   - "Create a new task to call John"
   - "Remind me to buy groceries at 5pm"
   - "Show me all my high priority tasks"
   - "What tasks are due today?"

2. **Habit Tracking**
   - "Create a habit to drink water"
   - "Track my meditation habit"
   - "Log 30 minutes of exercise for today"
   - "Show my habit progress for this week"
   - "Which habits am I currently tracking?"

3. **Focus Mode**
   - "Start a focus session for 25 minutes"
   - "Begin pomodoro timer"
   - "End current focus session"
   - "How long have I been focusing?"

4. **Calendar & Scheduling**
   - "Schedule a meeting with Sarah tomorrow at 2pm"
   - "Add dentist appointment on Friday at 10am"
   - "Show my calendar for next week"
   - "What meetings do I have today?"

5. **Email Management**
   - "Draft an email to boss@company.com about project status"
   - "Check my recent emails"
   - "Show unread messages"

### Technical Implementation

The AI system uses:

- **Node-NLP Library**: For intent classification and entity extraction
- **Custom Training Data**: Domain-specific examples for productivity tasks
- **Confidence Scoring**: Evaluates certainty of understanding before taking actions
- **Intent Handlers**: JavaScript functions that process specific user intents
- **Fallback Mechanisms**: Graceful handling of misunderstood commands

### Speech Recognition

The assistant supports voice commands through the Web Speech API, allowing users to:
- Activate the microphone for hands-free operation
- Convert spoken language to text commands
- Receive audio feedback for key notifications

### AI Learning & Improvement

- **Command Patterns**: Identifies common user command patterns
- **Suggestion Refinement**: Improves suggestions based on user habits
- **Vocabulary Expansion**: Adds new terminology based on user interaction

### Future AI Enhancements

- Integration with larger language models for more complex understanding
- Sentiment analysis to detect user stress levels
- Predictive task creation based on historical patterns
- Multi-language support for global users
- Advanced context tracking across conversation sessions

### Python AI Microservice

The application includes a Python-based AI microservice that provides enhanced natural language processing and machine learning capabilities:

- **Advanced NLP Analysis** using spaCy and Hugging Face transformers
- **Named Entity Recognition** with custom domain-specific entities
- **Sentiment Analysis** with emotion detection and productivity insights
- **Task Recommendation** using machine learning and user behavior patterns
- **Text Completion** for command prediction and suggestions

The Python service communicates with the Node.js backend through a REST API, providing seamless integration between the two technologies.

#### Python Stack:

- **Flask**: Lightweight web framework for the API
- **spaCy**: Industrial-strength NLP library
- **Transformers**: State-of-the-art NLP models
- **scikit-learn**: Machine learning library
- **pandas**: Data analysis and manipulation

#### Installing and Running the Python Service:

```bash
cd python-ai-service
pip install -r requirements.txt
python -m spacy download en_core_web_md
python app.py
```

The service will run on port 5001 by default and will be automatically used by the Node.js backend when available.

## Tech Stack

- Frontend: React with Material-UI
- Backend: Node.js and Express
- Database: MySQL with Sequelize ORM
- Natural Language Processing: node-nlp
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

You can interact with the assistant by:
1. Typing natural language commands in the command bar
2. Using the microphone button for voice commands
3. Accessing specific features through the UI components

## License

MIT 