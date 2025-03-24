const express = require('express');
const router = express.Router();
const { protect } = require('../../middleware/auth');
const nlpService = require('../../services/nlp');
const User = require('../../models/User');
const Task = require('../../models/Task');
const Habit = require('../../models/Habit');
const HabitProgress = require('../../models/HabitProgress');

/**
 * @route   POST api/commands
 * @desc    Process natural language commands
 * @access  Private
 */
router.post('/', protect, async (req, res) => {
  try {
    const { text } = req.body;

    if (!text) {
      return res.status(400).json({ msg: 'Command text is required' });
    }

    // Process the text using NLP
    const result = await nlpService.process(text);
    
    // Handle the command based on intent
    let response = await handleIntent(result, req.user.id);
    
    res.json({
      success: true,
      nlpResult: result,
      response
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// Handle different intents and take action
async function handleIntent(nlpResult, userId) {
  const { intent, entities } = nlpResult;
  
  // Default response is the NLP's generated answer
  let response = {
    message: nlpResult.answer || "I'm not sure how to handle that request.",
    data: null
  };

  try {
    // Task-related intents
    if (intent === 'task.create') {
      const taskContent = nlpService.extractTask(nlpResult.utterance, intent) || 
                         entities.find(e => e.entity === 'task')?.value;
      
      if (taskContent) {
        const task = await Task.create({
          title: taskContent,
          description: '',
          userId: userId,
          priority: 'medium',
          status: 'not-started',
          dueDate: new Date(Date.now() + 24 * 60 * 60 * 1000) // Default due date is tomorrow
        });

        response.message = `I've created a task: "${taskContent}"`;
        response.data = task;
      }
    } 
    else if (intent === 'task.list' || intent === 'task.list.today') {
      let query = { userId };
      
      // If looking for today's tasks only
      if (intent === 'task.list.today') {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        query.dueDate = {
          $gte: today,
          $lt: tomorrow
        };
      }
      
      const tasks = await Task.findAll({ 
        where: query, 
        order: [['dueDate', 'ASC']] 
      });
      
      response.message = intent === 'task.list.today' 
        ? "Here are your tasks for today:" 
        : "Here are all your tasks:";
      response.data = tasks;
    }
    // Habit-related intents
    else if (intent === 'habit.create') {
      const habitName = entities.find(e => e.entity === 'habit')?.value;
      
      if (habitName) {
        const habit = await Habit.create({
          name: habitName,
          description: '',
          userId: userId,
          type: 'daily', // Default type
          target: 1,
          unit: 'times'
        });

        response.message = `I've created a habit to track: "${habitName}"`;
        response.data = habit;
      }
    }
    else if (intent === 'habit.list') {
      const habits = await Habit.findAll({ 
        where: { userId }, 
        order: [['createdAt', 'DESC']] 
      });
      
      response.message = "Here are your habits:";
      response.data = habits;
    }
    else if (intent === 'habit.log') {
      const habitName = entities.find(e => e.entity === 'habit')?.value;
      
      if (habitName) {
        // Find the habit by name
        const habit = await Habit.findOne({
          where: {
            name: {
              [Op.like]: `%${habitName}%`
            },
            userId
          }
        });
        
        if (habit) {
          // Check if there's already progress for today
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          
          let progress = await HabitProgress.findOne({
            where: {
              habitId: habit.id,
              date: today
            }
          });
          
          if (progress) {
            progress.value += 1;
            await progress.save();
          } else {
            progress = await HabitProgress.create({
              habitId: habit.id,
              date: today,
              value: 1
            });
          }
          
          response.message = `I've logged your progress for "${habitName}"`;
          response.data = progress;
        } else {
          response.message = `I couldn't find a habit named "${habitName}"`;
        }
      }
    }
    
    // Focus-related intents
    else if (intent === 'focus.start') {
      response.message = "Focus mode activated. I'll help you stay on track!";
      // Here you would implement starting a focus session
    }
    else if (intent === 'focus.stop') {
      response.message = "Focus mode ended. Great job staying focused!";
      // Here you would implement ending a focus session
    }
    
    // Email-related intents
    else if (intent === 'email.send') {
      const recipient = entities.find(e => e.entity === 'recipient')?.value;
      const subject = entities.find(e => e.entity === 'subject')?.value;
      
      response.message = `I'll prepare an email to ${recipient || 'your contact'} about ${subject || 'your topic'}`;
      // Here you would implement email composition
    }
    else if (intent === 'email.check') {
      response.message = "I'll check your emails";
      // Here you would implement email checking
    }
    
    // Calendar-related intents
    else if (intent === 'calendar.schedule') {
      const event = entities.find(e => e.entity === 'event')?.value;
      const date = entities.find(e => e.entity === 'date')?.value;
      const person = entities.find(e => e.entity === 'person')?.value;
      
      response.message = `I'll schedule ${event || (person ? `a meeting with ${person}` : 'your event')} on ${date || 'the specified date'}`;
      // Here you would implement calendar scheduling
    }
    else if (intent.startsWith('calendar.view')) {
      response.message = intent === 'calendar.view.today' 
        ? "Here are your events for today" 
        : (intent === 'calendar.view.tomorrow' 
          ? "Here are your events for tomorrow" 
          : "Here's your calendar");
      // Here you would implement calendar viewing
    }
  } catch (err) {
    console.error('Error handling intent:', err);
    response.message = "I had trouble processing that request.";
  }
  
  return response;
}

module.exports = router; 