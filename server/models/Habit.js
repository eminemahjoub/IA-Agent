const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db');
const User = require('./User');

const Habit = sequelize.define('Habit', {
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: { msg: 'Please add a habit name' },
      len: { args: [1, 100], msg: 'Name cannot be more than 100 characters' }
    }
  },
  description: {
    type: DataTypes.STRING(500),
    allowNull: true
  },
  type: {
    type: DataTypes.ENUM('daily', 'weekly', 'monthly'),
    defaultValue: 'daily'
  },
  target: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 1,
    validate: {
      min: { args: [1], msg: 'Target must be at least 1' }
    }
  },
  unit: {
    type: DataTypes.STRING,
    defaultValue: 'times'
  },
  reminderTime: {
    type: DataTypes.STRING,
    allowNull: true
  },
  color: {
    type: DataTypes.STRING,
    defaultValue: '#4285F4'
  },
  icon: {
    type: DataTypes.STRING,
    defaultValue: 'repeat'
  },
  active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  startDate: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  },
  endDate: {
    type: DataTypes.DATE,
    allowNull: true
  }
}, {
  timestamps: true,
  createdAt: 'createdAt',
  indexes: [
    {
      fields: ['userId', 'active']
    }
  ]
});

const HabitProgress = sequelize.define('HabitProgress', {
  date: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  value: {
    type: DataTypes.FLOAT,
    defaultValue: 0
  },
  notes: {
    type: DataTypes.STRING,
    allowNull: true
  },
  completed: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  }
}, {
  timestamps: true,
  createdAt: 'createdAt',
  indexes: [
    {
      fields: ['habitId', 'date']
    },
    {
      fields: ['userId', 'date']
    }
  ]
});

// Define associations
Habit.belongsTo(User, {
  foreignKey: {
    name: 'userId',
    allowNull: false
  },
  onDelete: 'CASCADE'
});

User.hasMany(Habit, {
  foreignKey: 'userId'
});

HabitProgress.belongsTo(Habit, {
  foreignKey: {
    name: 'habitId',
    allowNull: false
  },
  onDelete: 'CASCADE'
});

HabitProgress.belongsTo(User, {
  foreignKey: {
    name: 'userId',
    allowNull: false
  },
  onDelete: 'CASCADE'
});

Habit.hasMany(HabitProgress, {
  foreignKey: 'habitId'
});

User.hasMany(HabitProgress, {
  foreignKey: 'userId'
});

module.exports = { Habit, HabitProgress }; 