const express = require('express');
const router = express.Router();
const { protect } = require('../../middleware/auth');

// @route   GET api/focus
// @desc    Get user focus settings
// @access  Private
router.get('/', protect, (req, res) => {
  // Return user's focus settings from the user object
  res.json({
    success: true,
    data: req.user.focusSettings || {
      workDuration: 25,
      breakDuration: 5,
      longBreakDuration: 15,
      longBreakInterval: 4
    }
  });
});

// @route   POST api/focus/session
// @desc    Start a focus session (placeholder)
// @access  Private
router.post('/session', protect, (req, res) => {
  res.json({
    success: true,
    message: 'Focus session started (placeholder)'
  });
});

module.exports = router; 