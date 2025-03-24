const { NlpManager } = require('node-nlp');
const pythonAI = require('./pythonAI');

class NLPService {
  constructor() {
    this.manager = new NlpManager({ languages: ['en'], forceNER: true });
    this.initialized = false;
    this.usePythonAI = false; // Will be set to true if Python service is available
  }

  async init() {
    if (this.initialized) return;

    // Check if Python AI service is available
    try {
      this.usePythonAI = await pythonAI.isAvailable();
      console.log(`Python AI service is ${this.usePythonAI ? 'available' : 'not available'}`);
    } catch (error) {
      console.log('Python AI service is not available:', error.message);
      this.usePythonAI = false;
    }

    // Add task-related intents
    this.manager.addDocument('en', 'add task %task%', 'task.create');
    this.manager.addDocument('en', 'create task %task%', 'task.create');
    this.manager.addDocument('en', 'new task %task%', 'task.create');
    this.manager.addDocument('en', 'remind me to %task%', 'task.create');
    this.manager.addDocument('en', 'i need to %task%', 'task.create');

    this.manager.addDocument('en', 'list my tasks', 'task.list');
    this.manager.addDocument('en', 'show me my tasks', 'task.list');
    this.manager.addDocument('en', 'what are my tasks', 'task.list');
    this.manager.addDocument('en', 'show tasks for today', 'task.list.today');
    this.manager.addDocument('en', 'what do I have to do today', 'task.list.today');

    this.manager.addDocument('en', 'mark task %task% as done', 'task.complete');
    this.manager.addDocument('en', 'complete task %task%', 'task.complete');
    this.manager.addDocument('en', 'finish task %task%', 'task.complete');
    this.manager.addDocument('en', 'i finished %task%', 'task.complete');

    // Add habit-related intents
    this.manager.addDocument('en', 'track habit %habit%', 'habit.create');
    this.manager.addDocument('en', 'create habit %habit%', 'habit.create');
    this.manager.addDocument('en', 'new habit %habit%', 'habit.create');
    this.manager.addDocument('en', 'help me build habit of %habit%', 'habit.create');

    this.manager.addDocument('en', 'show my habits', 'habit.list');
    this.manager.addDocument('en', 'list my habits', 'habit.list');
    this.manager.addDocument('en', 'what habits am I tracking', 'habit.list');

    this.manager.addDocument('en', 'log %habit% for today', 'habit.log');
    this.manager.addDocument('en', 'completed %habit% today', 'habit.log');
    this.manager.addDocument('en', 'i did %habit% today', 'habit.log');

    // Add focus mode intents
    this.manager.addDocument('en', 'start focus mode', 'focus.start');
    this.manager.addDocument('en', 'begin focus session', 'focus.start');
    this.manager.addDocument('en', 'help me focus', 'focus.start');
    this.manager.addDocument('en', 'start pomodoro', 'focus.start');

    this.manager.addDocument('en', 'end focus mode', 'focus.stop');
    this.manager.addDocument('en', 'stop focus session', 'focus.stop');
    this.manager.addDocument('en', 'finish pomodoro', 'focus.stop');

    // Add email-related intents
    this.manager.addDocument('en', 'send email to %recipient% about %subject%', 'email.send');
    this.manager.addDocument('en', 'email %recipient% about %subject%', 'email.send');
    this.manager.addDocument('en', 'compose email to %recipient%', 'email.send');

    this.manager.addDocument('en', 'check my emails', 'email.check');
    this.manager.addDocument('en', 'any new emails', 'email.check');
    this.manager.addDocument('en', 'show me my inbox', 'email.check');

    // Add calendar-related intents
    this.manager.addDocument('en', 'schedule meeting with %person% on %date%', 'calendar.schedule');
    this.manager.addDocument('en', 'add event %event% on %date%', 'calendar.schedule');
    this.manager.addDocument('en', 'create appointment for %event% on %date%', 'calendar.schedule');

    this.manager.addDocument('en', 'show my calendar', 'calendar.view');
    this.manager.addDocument('en', 'what meetings do I have today', 'calendar.view.today');
    this.manager.addDocument('en', 'show my schedule for tomorrow', 'calendar.view.tomorrow');

    // Add sentiment analysis intents
    this.manager.addDocument('en', 'how am I feeling', 'sentiment.analyze');
    this.manager.addDocument('en', 'analyze my mood', 'sentiment.analyze');
    this.manager.addDocument('en', 'detect my sentiment', 'sentiment.analyze');

    // Add task suggestion intents
    this.manager.addDocument('en', 'suggest tasks', 'task.suggest');
    this.manager.addDocument('en', 'what should I work on', 'task.suggest');
    this.manager.addDocument('en', 'recommend tasks', 'task.suggest');
    this.manager.addDocument('en', 'what should I do next', 'task.suggest');

    // Add responses
    this.manager.addAnswer('en', 'task.create', 'I\'ll create a task for: {{task}}');
    this.manager.addAnswer('en', 'task.list', 'Here are your tasks:');
    this.manager.addAnswer('en', 'task.list.today', 'Here are your tasks for today:');
    this.manager.addAnswer('en', 'task.complete', 'I\'ve marked "{{task}}" as complete!');

    this.manager.addAnswer('en', 'habit.create', 'I\'ll help you track your habit: {{habit}}');
    this.manager.addAnswer('en', 'habit.list', 'Here are the habits you\'re currently tracking:');
    this.manager.addAnswer('en', 'habit.log', 'I\'ve logged your progress for {{habit}}');

    this.manager.addAnswer('en', 'focus.start', 'Starting focus mode. I\'ll help you stay on track!');
    this.manager.addAnswer('en', 'focus.stop', 'Focus mode ended. You did great!');

    this.manager.addAnswer('en', 'email.send', 'I\'ll prepare an email to {{recipient}} about {{subject}}');
    this.manager.addAnswer('en', 'email.check', 'Checking your emails...');

    this.manager.addAnswer('en', 'calendar.schedule', 'I\'ll schedule {{event}} on {{date}}');
    this.manager.addAnswer('en', 'calendar.view', 'Here\'s your calendar:');
    this.manager.addAnswer('en', 'calendar.view.today', 'Here are your meetings for today:');
    this.manager.addAnswer('en', 'calendar.view.tomorrow', 'Here\'s your schedule for tomorrow:');

    this.manager.addAnswer('en', 'sentiment.analyze', 'Let me analyze your recent messages...');
    this.manager.addAnswer('en', 'task.suggest', 'Here are some tasks I recommend:');

    // Train and save model
    await this.manager.train();
    this.initialized = true;
  }

  async process(text) {
    if (!this.initialized) {
      await this.init();
    }

    // Basic intent recognition with node-nlp
    const result = await this.manager.process('en', text);
    
    let entities = result.entities;
    let enhancedResult = { ...result };

    // Use Python AI for enhanced processing if available
    if (this.usePythonAI) {
      try {
        // Extract entities using spaCy (more accurate than node-nlp)
        const pythonEntities = await pythonAI.extractEntities(text);
        if (pythonEntities && pythonEntities.length > 0) {
          enhancedResult.pythonEntities = pythonEntities;
          
          // Merge Python entities with node-nlp entities
          // This combines the strengths of both systems
          entities = this._mergeEntities(entities, pythonEntities);
        }

        // For certain intents, get additional context from Python
        if (result.intent === 'sentiment.analyze') {
          const sentimentAnalysis = await pythonAI.analyzeSentiment(text);
          enhancedResult.sentimentAnalysis = sentimentAnalysis;
        }
        
        // For task suggestions, use the ML model
        if (result.intent === 'task.suggest') {
          const suggestions = await pythonAI.suggestTasks('default-user');
          enhancedResult.taskSuggestions = suggestions;
        }
        
        // Get text completion suggestions for ambiguous commands
        if (result.score < 0.7) {
          const completion = await pythonAI.predictCompletion(text);
          enhancedResult.suggestedCompletion = completion;
        }
        
      } catch (error) {
        console.error('Error using Python AI service:', error.message);
        // Continue with basic processing if Python fails
      }
    }
    
    return {
      intent: enhancedResult.intent,
      score: enhancedResult.score,
      entities: entities,
      answer: enhancedResult.answer,
      utterance: enhancedResult.utterance,
      // Include any enhanced data from Python
      ...(enhancedResult.pythonEntities && { pythonEntities: enhancedResult.pythonEntities }),
      ...(enhancedResult.sentimentAnalysis && { sentimentAnalysis: enhancedResult.sentimentAnalysis }),
      ...(enhancedResult.taskSuggestions && { taskSuggestions: enhancedResult.taskSuggestions }),
      ...(enhancedResult.suggestedCompletion && { suggestedCompletion: enhancedResult.suggestedCompletion })
    };
  }
  
  // Helper method to merge entities from node-nlp and Python spaCy
  _mergeEntities(nodeEntities, pythonEntities) {
    // Start with all node entities
    const mergedEntities = [...nodeEntities];
    
    // Add Python entities that don't overlap with existing ones
    for (const pyEntity of pythonEntities) {
      // Check if this entity overlaps with any existing entity
      const overlaps = mergedEntities.some(
        e => e.entity === pyEntity.label || 
             (e.start <= pyEntity.end_char && e.end >= pyEntity.start_char)
      );
      
      if (!overlaps) {
        mergedEntities.push({
          entity: pyEntity.label,
          value: pyEntity.text,
          start: pyEntity.start_char,
          end: pyEntity.end_char,
          source: 'python'
        });
      }
    }
    
    return mergedEntities;
  }

  // Extract task content from a task creation command
  extractTask(text, intent) {
    if (intent === 'task.create') {
      // Extract task from phrases like "add task finish report"
      const matches = text.match(/(add|create|new) task (.*)/i);
      if (matches && matches.length > 2) {
        return matches[2];
      }
      
      // Extract task from phrases like "remind me to call mom"
      const remindMatches = text.match(/remind me to (.*)/i);
      if (remindMatches && remindMatches.length > 1) {
        return remindMatches[1];
      }
      
      // Extract task from phrases like "i need to buy groceries"
      const needMatches = text.match(/i need to (.*)/i);
      if (needMatches && needMatches.length > 1) {
        return needMatches[1];
      }
    }
    
    return null;
  }
}

module.exports = new NLPService(); 