const express = require('express');
const router = express.Router();
const User = require('../../models/User');
const { protect } = require('../../middleware/auth');

// @route   POST api/auth
// @desc    Authenticate user & get token
// @access  Public
router.post('/', async (req, res) => {
  const { email, password } = req.body;

  try {
    // Check for user
    const user = await User.scope('withPassword').findOne({ where: { email } });

    if (!user) {
      return res.status(401).json({
        success: false,
        error: 'Invalid credentials',
      });
    }

    // Check if password matches
    const isMatch = await user.matchPassword(password);

    if (!isMatch) {
      return res.status(401).json({
        success: false,
        error: 'Invalid credentials',
      });
    }

    // Return jsonwebtoken
    const token = user.getSignedJwtToken();

    res.json({
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

// @route   GET api/auth
// @desc    Get logged in user
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const user = await User.findByPk(req.user.id);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found',
      });
    }
    
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