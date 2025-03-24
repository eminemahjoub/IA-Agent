# MongoDB to SQL Migration Guide

This document outlines the steps taken to migrate the Personal Productivity Assistant from MongoDB to MySQL using Sequelize ORM.

## Changes Made

1. **Dependencies**
   - Removed: mongoose
   - Added: mysql2, sequelize, sequelize-cli

2. **Configuration**
   - Created Sequelize configuration in `server/config/sequelize.js`
   - Added `.sequelizerc` file for Sequelize CLI configuration
   - Updated database connection in `server/config/db.js`
   - Modified `.env` format to use MySQL connection parameters

3. **Models**
   - Converted Mongoose schemas to Sequelize models
   - Implemented proper associations between models
   - Added DataTypes and validation to match Mongoose schemas

4. **Routes**
   - Updated all route files to use Sequelize query methods
   - Changed query patterns from Mongoose to Sequelize syntax
   - Added proper error handling for SQL-specific errors

5. **Scripts**
   - Added Sequelize-specific scripts to package.json for database management

## How to Complete the Migration

1. **Initialize the Database**
   ```
   npm run sequelize:init
   npm run db:create
   npm run db:migrate
   ```

2. **Data Migration**
   If you have existing MongoDB data, you'll need to export it and import it into MySQL.
   A data migration script can be created to handle this process.

3. **Environment Variables**
   Update your `.env` file with the following variables:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=productivity_assistant
   DB_USER=root
   DB_PASSWORD=your_password
   ```

4. **Testing**
   After migration, test all features to ensure they work properly with the new database system.

## SQL vs MongoDB Considerations

### Advantages of SQL
- Strong relational data support
- ACID transactions
- Mature ecosystem and tooling
- Better for complex queries and reporting

### Migration Challenges
- Schema rigidity compared to MongoDB's flexibility
- Need to normalize data that was previously denormalized
- Different query syntax and patterns

## Sequelize Model Examples

### User Model
```javascript
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      validate: {
        isEmail: true
      }
    },
    password: {
      type: DataTypes.STRING,
      allowNull: false
    }
  });

  User.associate = (models) => {
    User.hasMany(models.Task, {
      foreignKey: 'userId',
      onDelete: 'CASCADE'
    });
    User.hasMany(models.Habit, {
      foreignKey: 'userId',
      onDelete: 'CASCADE'
    });
  };

  return User;
};
```

### Query Pattern Changes

MongoDB:
```javascript
// Find user by ID
const user = await User.findById(id);

// Find with conditions
const tasks = await Task.find({ user: userId }).sort({ date: -1 });

// Create new document
const newTask = new Task({ title, description, user: userId });
await newTask.save();
```

Sequelize:
```javascript
// Find user by ID
const user = await User.findByPk(id);

// Find with conditions
const tasks = await Task.findAll({ 
  where: { userId }, 
  order: [['date', 'DESC']] 
});

// Create new document
const newTask = await Task.create({ title, description, userId });
``` 