const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const User = require('../../models/User');
const { protect } = require('../../middleware/auth');

// @route   POST api/users
// @desc    Register user
// @access  Public
router.post('/', async (req, res) => {
  const { name, email, password } = req.body;

  try {
    // See if user exists
    const userExists = await User.findOne({ where: { email } });

    if (userExists) {
      return res.status(400).json({
        success: false,
        error: 'User already exists',
      });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    // Return jsonwebtoken
    const token = user.getSignedJwtToken();

    res.status(201).json({
      success: true,
      token,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: err.message || 'Server error',
    });
  }
});

// @route   GET api/users/me
// @desc    Get current user profile
// @access  Private
router.get('/me', protect, async (req, res) => {
  try {
    const user = await User.findByPk(req.user.id);
    
    res.json({
      success: true,
      data: user,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({
      success: false,
      error: 'Server error',
    });
  }
});

// @route   PUT api/users/me
// @desc    Update user profile
// @access  Private
router.put('/me', protect, async (req, res) => {
  const {
    name,
    email,
    focusSettings,
    habitSettings,
  } = req.body;

  try {
    const user = await User.findByPk(req.user.id);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found',
      });
    }

    // Update user fields
    if (name) user.name = name;
    if (email) user.email = email;
    if (focusSettings) user.focusSettings = { ...user.focusSettings, ...focusSettings };
    if (habitSettings) user.habitSettings = { ...user.habitSettings, ...habitSettings };

    await user.save();

    res.json({
      success: true,
      data: user,
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