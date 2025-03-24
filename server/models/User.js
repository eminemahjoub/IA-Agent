const { DataTypes } = require('sequelize');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { sequelize } = require('../config/db');

const User = sequelize.define('User', {
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: { msg: 'Please add a name' }
    }
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: { msg: 'Please add a valid email' },
      notEmpty: { msg: 'Please add an email' }
    }
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: { msg: 'Please add a password' },
      len: { args: [6, 100], msg: 'Password must be at least 6 characters' }
    }
  },
  googleCalendarToken: {
    type: DataTypes.STRING,
    allowNull: true,
    defaultValue: null
  },
  outlookToken: {
    type: DataTypes.STRING,
    allowNull: true,
    defaultValue: null
  },
  emailSettings: {
    type: DataTypes.JSONB,
    defaultValue: {
      service: null,
      connected: false,
      token: null
    }
  },
  focusSettings: {
    type: DataTypes.JSONB,
    defaultValue: {
      workDuration: 25,
      breakDuration: 5,
      longBreakDuration: 15,
      longBreakInterval: 4
    }
  },
  habitSettings: {
    type: DataTypes.JSONB,
    defaultValue: {
      reminderTime: null,
      trackingEnabled: true
    }
  }
}, {
  timestamps: true,
  createdAt: 'createdAt',
  defaultScope: {
    attributes: { exclude: ['password'] }
  },
  scopes: {
    withPassword: {
      attributes: { include: ['password'] }
    }
  }
});

// Encrypt password before save
User.beforeCreate(async (user) => {
  const salt = await bcrypt.genSalt(10);
  user.password = await bcrypt.hash(user.password, salt);
});

User.beforeUpdate(async (user) => {
  if (user.changed('password')) {
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(user.password, salt);
  }
});

// Instance methods need to be defined differently in Sequelize
User.prototype.getSignedJwtToken = function() {
  return jwt.sign({ id: this.id }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRE || '30d'
  });
};

User.prototype.matchPassword = async function(enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password);
};

module.exports = User; 