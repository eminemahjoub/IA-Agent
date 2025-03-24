const express = require('express');
const router = express.Router();
const auth = require('../../middleware/auth');
const { check, validationResult } = require('express-validator');
const { Op } = require('sequelize');

// Models
const Habit = require('../../models/Habit');
const HabitProgress = require('../../models/HabitProgress');

// @route   GET api/habit-progress
// @desc    Get all habit progress entries for the authenticated user
// @access  Private
router.get('/', auth, async (req, res) => {
  try {
    const habitProgress = await HabitProgress.findAll({
      include: [{
        model: Habit,
        where: { userId: req.user.id },
        attributes: ['name', 'type', 'target', 'unit']
      }],
      order: [['date', 'DESC']]
    });

    res.json(habitProgress);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   GET api/habit-progress/by-date
// @desc    Get habit progress for a specific date range
// @access  Private
router.get('/by-date', auth, async (req, res) => {
  try {
    const { startDate, endDate } = req.query;
    
    if (!startDate || !endDate) {
      return res.status(400).json({ msg: 'Start date and end date are required' });
    }

    const habitProgress = await HabitProgress.findAll({
      include: [{
        model: Habit,
        where: { userId: req.user.id },
        attributes: ['name', 'type', 'target', 'unit']
      }],
      where: {
        date: {
          [Op.between]: [new Date(startDate), new Date(endDate)]
        }
      },
      order: [['date', 'ASC']]
    });

    res.json(habitProgress);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   GET api/habit-progress/:habitId
// @desc    Get all progress for a specific habit
// @access  Private
router.get('/:habitId', auth, async (req, res) => {
  try {
    // Verify the habit belongs to the user
    const habit = await Habit.findOne({
      where: {
        id: req.params.habitId,
        userId: req.user.id
      }
    });

    if (!habit) {
      return res.status(404).json({ msg: 'Habit not found or not authorized' });
    }

    const habitProgress = await HabitProgress.findAll({
      where: { habitId: req.params.habitId },
      order: [['date', 'DESC']]
    });

    res.json(habitProgress);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST api/habit-progress/:habitId
// @desc    Add or update progress for a habit
// @access  Private
router.post(
  '/:habitId',
  [
    auth,
    [
      check('date', 'Date is required').not().isEmpty(),
      check('value', 'Progress value is required').not().isEmpty(),
      check('notes', 'Notes must be a string').optional().isString()
    ]
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { date, value, notes } = req.body;

    try {
      // Verify the habit belongs to the user
      const habit = await Habit.findOne({
        where: {
          id: req.params.habitId,
          userId: req.user.id
        }
      });

      if (!habit) {
        return res.status(404).json({ msg: 'Habit not found or not authorized' });
      }

      // Check if there's already progress for this date
      let habitProgress = await HabitProgress.findOne({
        where: {
          habitId: req.params.habitId,
          date: new Date(date)
        }
      });

      if (habitProgress) {
        // Update existing progress
        habitProgress.value = value;
        if (notes) habitProgress.notes = notes;
        await habitProgress.save();
      } else {
        // Create new progress entry
        habitProgress = await HabitProgress.create({
          habitId: req.params.habitId,
          date: new Date(date),
          value,
          notes: notes || ''
        });
      }

      res.json(habitProgress);
    } catch (err) {
      console.error(err.message);
      res.status(500).send('Server Error');
    }
  }
);

// @route   DELETE api/habit-progress/:id
// @desc    Delete a habit progress entry
// @access  Private
router.delete('/:id', auth, async (req, res) => {
  try {
    const habitProgress = await HabitProgress.findByPk(req.params.id);

    if (!habitProgress) {
      return res.status(404).json({ msg: 'Progress entry not found' });
    }

    // Verify the habit belongs to the user
    const habit = await Habit.findOne({
      where: {
        id: habitProgress.habitId,
        userId: req.user.id
      }
    });

    if (!habit) {
      return res.status(401).json({ msg: 'Not authorized to delete this progress entry' });
    }

    await habitProgress.destroy();
    res.json({ msg: 'Progress entry removed' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router; 