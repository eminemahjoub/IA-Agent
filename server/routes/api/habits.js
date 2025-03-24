const express = require('express');
const router = express.Router();
const { Habit, HabitProgress } = require('../../models/Habit');
const { protect } = require('../../middleware/auth');
const { Op } = require('sequelize');

// @route   GET api/habits
// @desc    Get all user habits
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const habits = await Habit.findAll({
      where: { userId: req.user.id },
      order: [['createdAt', 'DESC']]
    });
    
    res.json({
      success: true,
      count: habits.length,
      data: habits,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   POST api/habits
// @desc    Create a habit
// @access  Private
router.post('/', protect, async (req, res) => {
  const {
    name,
    description,
    type,
    target,
    unit,
    reminderTime,
    color,
    icon,
    startDate,
    endDate,
  } = req.body;

  try {
    const habit = await Habit.create({
      userId: req.user.id,
      name,
      description,
      type,
      target,
      unit,
      reminderTime,
      color,
      icon,
      startDate,
      endDate,
    });

    res.status(201).json({
      success: true,
      data: habit,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   GET api/habits/:id
// @desc    Get habit by ID
// @access  Private
router.get('/:id', protect, async (req, res) => {
  try {
    const habit = await Habit.findByPk(req.params.id);

    if (!habit) {
      return res.status(404).json({
        success: false,
        error: 'Habit not found',
      });
    }

    // Make sure user owns habit
    if (habit.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    res.json({
      success: true,
      data: habit,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   PUT api/habits/:id
// @desc    Update habit
// @access  Private
router.put('/:id', protect, async (req, res) => {
  const {
    name,
    description,
    type,
    target,
    unit,
    reminderTime,
    color,
    icon,
    active,
    startDate,
    endDate,
  } = req.body;

  try {
    const habit = await Habit.findByPk(req.params.id);

    if (!habit) {
      return res.status(404).json({
        success: false,
        error: 'Habit not found',
      });
    }

    // Make sure user owns habit
    if (habit.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    // Update habit fields
    if (name !== undefined) habit.name = name;
    if (description !== undefined) habit.description = description;
    if (type !== undefined) habit.type = type;
    if (target !== undefined) habit.target = target;
    if (unit !== undefined) habit.unit = unit;
    if (reminderTime !== undefined) habit.reminderTime = reminderTime;
    if (color !== undefined) habit.color = color;
    if (icon !== undefined) habit.icon = icon;
    if (active !== undefined) habit.active = active;
    if (startDate !== undefined) habit.startDate = startDate;
    if (endDate !== undefined) habit.endDate = endDate;

    await habit.save();

    res.json({
      success: true,
      data: habit,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   DELETE api/habits/:id
// @desc    Delete habit
// @access  Private
router.delete('/:id', protect, async (req, res) => {
  try {
    const habit = await Habit.findByPk(req.params.id);

    if (!habit) {
      return res.status(404).json({
        success: false,
        error: 'Habit not found',
      });
    }

    // Make sure user owns habit
    if (habit.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    // Remove habit (and associated progress will be cascade deleted)
    await habit.destroy();

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

// @route   POST api/habits/:id/progress
// @desc    Add habit progress
// @access  Private
router.post('/:id/progress', protect, async (req, res) => {
  const { date, value, notes } = req.body;

  try {
    const habit = await Habit.findByPk(req.params.id);

    if (!habit) {
      return res.status(404).json({
        success: false,
        error: 'Habit not found',
      });
    }

    // Make sure user owns habit
    if (habit.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    // Check if progress already exists for this date
    let progress = await HabitProgress.findOne({
      where: {
        habitId: req.params.id,
        date: date
      }
    });

    if (progress) {
      // Update existing progress
      progress.value = value;
      progress.notes = notes;
      progress.completed = value >= habit.target;
      await progress.save();
    } else {
      // Create new progress
      progress = await HabitProgress.create({
        userId: req.user.id,
        habitId: req.params.id,
        date: date,
        value,
        notes,
        completed: value >= habit.target,
      });
    }

    res.status(201).json({
      success: true,
      data: progress,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   GET api/habits/:id/progress
// @desc    Get habit progress
// @access  Private
router.get('/:id/progress', protect, async (req, res) => {
  try {
    const habit = await Habit.findByPk(req.params.id);

    if (!habit) {
      return res.status(404).json({
        success: false,
        error: 'Habit not found',
      });
    }

    // Make sure user owns habit
    if (habit.userId !== req.user.id) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized',
      });
    }

    const { startDate, endDate } = req.query;
    let whereClause = { habitId: req.params.id };

    if (startDate && endDate) {
      whereClause.date = {
        [Op.between]: [startDate, endDate]
      };
    }

    const progress = await HabitProgress.findAll({
      where: whereClause,
      order: [['date', 'ASC']]
    });

    res.json({
      success: true,
      count: progress.length,
      data: progress,
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