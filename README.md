# MINEDOKU

A web-based puzzle game combining Sudoku-style logic with Minecraft blocks.

## Overview

MINEDOKU is a logic-based puzzle game where players complete a 3×3 grid using Minecraft blocks that satisfy both row and column categories.

The application is designed to be simple and accessible, allowing users to quickly start playing without requiring an account. It focuses on combining logical reasoning with knowledge of Minecraft blocks, while encouraging players to think creatively through a uniqueness-based scoring system.

## Features

* 3×3 condition-based puzzle grid
* Uniqueness Score (US) based scoring
* Progress saving
* Optional login
* Friends leaderboard system
* Inventory unlock system
* Persistent account statistics

## How It Works

* Each row and column has a category
* Fill each cell with a block that satisfies both
* Each block can only be used once

Your score is based on how unique your answers are compared to other players.

## How to Launch the Application

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MineDoku
```

### 2. Create and Activate a Virtual Environment

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If any packages are missing:

```bash
pip install flask-migrate flask-sqlalchemy flask-login selenium flask-wtf email-validator
```

### 4. Create the Database

Run:

```bash
python3 minedoku.py
```

The application will automatically create and populate the database on first launch.

### 5. Open in Browser

Open the local server URL shown in the terminal (usually):

```text
http://127.0.0.1:5000
```

---

## Testing

MINEDOKU includes both unit tests and Selenium browser tests.

### Unit Tests

Unit tests verify backend logic, database models, and route behaviour.

Covered functionality includes:

* Block condition compatibility validation
* User creation and database persistence
* Friend relationship creation
* Login route rendering
* Signup route rendering
* Authentication protection for account pages

Run unit tests with:

```bash
python3 -m unittest app.tests -v
```

### Selenium Browser Tests

Selenium tests verify end-to-end browser functionality and user interactions.

Covered functionality includes:

* Login page rendering
* Signup page rendering
* Navigation from login to signup
* Back-to-game button navigation

Before running Selenium tests, start the Flask server:

```bash
python3 minedoku.py
```

Then in a separate terminal:

```bash
python3 -m unittest app.selenium_tests -v
```

---

## Development Team

Developed as part of a university project for CITS3403.

| Student ID | Name              | GitHub Username |
| ---------- | ----------------- | --------------- |
| 244443977  | Ben Holiday       | DigBatt         |
| 24222455   | Hamsa Yusuf Ahmed | Hamsa123346     |
| 23484347   | Nate Htut         | tnh06           |
| 24650953   | Sam McCrum        | SamMc016        |◊