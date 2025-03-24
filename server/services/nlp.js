const { NlpManager } = require('node-nlp');

class NLPService {
  constructor() {
    this.manager = new NlpManager({ languages: ['en'], forceNER: true });
    this.initialized = false;
  }

  async init() {
    if (this.initialized) return;

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

    // Train and save model
    await this.manager.train();
    this.initialized = true;
  }

  async process(text) {
    if (!this.initialized) {
      await this.init();
    }
    
    const result = await this.manager.process('en', text);
    return {
      intent: result.intent,
      score: result.score,
      entities: result.entities,
      answer: result.answer,
      utterance: result.utterance,
    };
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