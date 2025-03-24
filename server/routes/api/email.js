const express = require('express');
const router = express.Router();
const { protect } = require('../../middleware/auth');

// @route   GET api/email
// @desc    Get user emails (placeholder)
// @access  Private
router.get('/', protect, (req, res) => {
  res.json({
    success: true,
    message: 'Email API is working (placeholder)',
    data: []
  });
});

// @route   POST api/email
// @desc    Send an email (placeholder)
// @access  Private
router.post('/', protect, (req, res) => {
  res.json({
    success: true,
    message: 'Email sending endpoint (placeholder)'
  });
});

module.exports = router; 