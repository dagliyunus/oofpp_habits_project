
# Habit Tracker - Terminal-Based Python CLI App

Developer: Yunus Emre Dagli  
Version: 1.0  
Execution Environment: Terminal (macOS/Linux/Windows)  
Main File: `main.py`

---

## Project Overview

This Habit Tracker app is a professional CLI application built in Python using Object-Oriented Programming (OOP) and Functional Programming (FP) paradigms. 
It allows users to create and manage daily or weekly habits, check them off, and analyze progress using visual summaries (streaks and misses).

The app uses SQLite for persistent storage, the `click` library for command-line interaction, and `pytest` for full unit testing coverage. 
Preloaded fixtures and terminal interaction logic offer a complete development and testing environment.

---

## Design Philosophy

- OOP: Encapsulates habit state and behavior (e.g., streaks, missed deadlines)
- FP: Pure functions for analytics module (testable & reusable)
- DB: SQLite + repo pattern (`storage_manager`) for maintainability
- CLI: Powered by `click`, providing intuitive navigation and testability
- Testability: Fully covered with `pytest`, `pytest-cov`, and mocks

---

## Project Structure

```
├── analytics/                         #  Pure functional logic for analysis (e.g., longest streaks, missed habits)
│   └── analytics_module.py            #  Contains FP-style functions (no side effects)
├── cli/                               #  CLI command definitions using `click`
│   └── commands.py                    #  Handles CLI subcommands (create, delete, check-off, analyze)
├── config/                            #  Configuration layer (e.g., DB connection)
│   └── db_config.py                   #  Reads .env and connects to SQLite
├── db/                                #  Static DB resources
│   ├── habits.sql                     #  SQL schema for `User`, `Habit`, `Habit_Logs`
│   └── fixtures.json                  #  Preloaded test/demo data (5 habits + logs)
├── models/                            #  Core OOP models (entities)
│   ├── habits.py                      #  `Habit` class: attributes and logic (OOP-based)
│   ├── user.py                        #  `User` class for sign-up/login handling
│   └── __init__.py                    #  Marks folder as a Python package
├── repository/                        #  Data access layer (DAL/DAO)
│   └── storage_manager.py             #  Functions to save/load from SQLite (e.g.,save_habit, load_checkoffs)
├── services/                          #  Application-level logic / coordination
│   ├── auth.py                        #  Handles user authentication (sign_up, log_in)
│   └── habit_service.py               #  Orchestrates habit lifecycle logic (create, checkoff, etc.)
├── utils/                             #  Reusable utilities
│   ├── cli_helper.py                  #  Terminal password masking using low-level termios
│   └── validators.py                  #  Input format checks, e.g. time, frequency
├── tests/                             #  Test suite 
│   ├── analytics_test/                #  Unit tests for analytics module (pure FP)
│   ├── auth_test/                     #  Tests for sign-up / log-in functionality
│   ├── cli_test/                      #  Tests for `click` CLI commands + full flow
│   ├── habit_test/                    #  OOP logic tests for Habit model (add_checkoff,streaks)
│   ├── storage_test/                  #  DB interaction tests (insert/select habit data)
│   └── __init__.py                    #  Makes test suite discoverable as a Python package
├── main.py                            #  CLI entry point — interactive login + main menu loop
├── requirements.txt                   #  Pinned dependencies (`pip freeze > requirements.txt`)
├── .coveragerc                        #  Coverage configuration for pytest-cov
├── .env                               #  Environment config (e.g. DB_PATH)
├── load_fixtures.py                   #  Loads `fixtures.json` on first run (skips if already loaded)
├── init_db.py                         #  Creates SQLite tables from `habits.sql`
└── README.md                          #  Project documentation & instructions
```

---

## Setup Instructions

### 1. Clone & Environment Setup

```bash
git clone https://github.com/dagliyunus/habit_tracker.git
cd habit_tracker
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python db/init_db.py
python load_fixtures.py  # loads demo habits
```

> Note: This application should be **run in a terminal only** (not via IDE) due to secure password input constraints.

---

## Running the App

```bash
python main.py
```

---

## Running Tests

```bash
# Run tests with coverage
PYTHONPATH=. pytest --cov=. --cov-report=term --cov-config=.coveragerc

# Optional HTML coverage report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

## .coveragerc Configuration

```ini
[run]
omit =
    tests/*
    */__init__.py
    config/*
    db/*
    *.venv/*

[report]
exclude_lines =
    pragma: no cover
    if __name__ == '__main__':
    def __repr__
    raise NotImplementedError

show_missing = True
```

---

## Python Environment (`pyvenv.cfg` Summary)

```
Python Version : 3.9.6.final.0
Virtualenv     : 20.24.5
Implementation : CPython
Includes system site packages: No
```

---

## Requirements Summary (via `requirements.txt`)

Includes (not limited to):

```txt
click==8.1.8
pytest==8.3.5
pytest-cov==6.1.1
python-dotenv==1.1.0
requests==2.32.3
auth==0.5.3
Werkzeug==3.1.3
mongoengine==0.29.1
```
> Full list in `requirements.txt`


---

## Future Additions

- Password hashing (bcrypt)
- Export logs as JSON/CSV
- Reminder notifications
- Flask/FastAPI-based GUI  
