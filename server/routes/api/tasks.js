const express = require('express');
const router = express.Router();
const Task = require('../../models/Task');
const { protect } = require('../../middleware/auth');
const { Op } = require('sequelize');

// @route   GET api/tasks
// @desc    Get all user tasks
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const tasks = await Task.findAll({
      where: { userId: req.user.id },
      order: [['dueDate', 'ASC']]
    });
    
    res.json({
      success: true,
      count: tasks.length,
      data: tasks,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   POST api/tasks
// @desc    Create a task
// @access  Private
router.post('/', protect, async (req, res) => {
  const {
    title,
    description,
    priority,
    status,
    dueDate,
    reminderTime,
    tags,
    isRecurring,
    recurringPattern,
  } = req.body;

  try {
    const task = await Task.create({
      userId: req.user.id,
      title,
      description,
      priority,
      status,
      dueDate,
      reminderTime,
      tags,
      isRecurring,
      recurringPattern,
    });

    res.status(201).json({
      success: true,
      data: task,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   GET api/tasks/:id
// @desc    Get task by ID
// @access  Private
router.get('/:id', protect, async (req, res) => {
  try {
    const task = await Task.findByPk(req.params.id);

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found',
      });
    }

    // Make sure user owns task
    if (task.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    res.json({
      success: true,
      data: task,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   PUT api/tasks/:id
// @desc    Update task
// @access  Private
router.put('/:id', protect, async (req, res) => {
  const {
    title,
    description,
    priority,
    status,
    dueDate,
    reminderTime,
    tags,
    isRecurring,
    recurringPattern,
    completedAt,
  } = req.body;

  try {
    let task = await Task.findByPk(req.params.id);

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found',
      });
    }

    // Make sure user owns task
    if (task.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    // Update task fields
    if (title !== undefined) task.title = title;
    if (description !== undefined) task.description = description;
    if (priority !== undefined) task.priority = priority;
    if (status !== undefined) task.status = status;
    if (dueDate !== undefined) task.dueDate = dueDate;
    if (reminderTime !== undefined) task.reminderTime = reminderTime;
    if (tags !== undefined) task.tags = tags;
    if (isRecurring !== undefined) task.isRecurring = isRecurring;
    if (recurringPattern !== undefined) task.recurringPattern = recurringPattern;
    if (completedAt !== undefined) task.completedAt = completedAt;

    await task.save();

    res.json({
      success: true,
      data: task,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   DELETE api/tasks/:id
// @desc    Delete task
// @access  Private
router.delete('/:id', protect, async (req, res) => {
  try {
    const task = await Task.findByPk(req.params.id);

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found',
      });
    }

    // Make sure user owns task
    if (task.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    await task.destroy();

    res.json({
      success: true,
      data: {},
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

module.exports = router; 