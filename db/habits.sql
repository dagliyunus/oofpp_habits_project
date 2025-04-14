-- db/habits.sql

CREATE TABLE IF NOT EXISTS User (
                                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username TEXT NOT NULL UNIQUE,
                                    email TEXT,
                                    password TEXT,
                                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Habit (
                                     habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     user_id INTEGER NOT NULL,
                                     name TEXT NOT NULL,
                                     frequency TEXT NOT NULL,
                                     description TEXT,
                                     deadline_time DATETIME,
                                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                     FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS Habit_Logs (
                                          log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          habit_id INTEGER NOT NULL,
                                          user_id INTEGER NOT NULL,
                                          completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                          note TEXT,
                                          missed BOOLEAN DEFAULT 0,
                                          FOREIGN KEY (habit_id) REFERENCES Habit(habit_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    );