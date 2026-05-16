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
### 4. Create the Secret Key

Create a new file in the root directory named `.env`. Inside type:

```bash
SECRET_KEY=demo_secret_key
```
### 5. Create the Database and Launch the App

Run:

```bash
python minedoku.py
```

The application will automatically create and populate the database on first launch.

### 6. Open in Browser

Open the local server URL shown in the terminal (usually):

```text
http://127.0.0.1:5000
```

---

## Testing

MINEDOKU includes both unit and system tests, the later by way of Selenium browser tests.

### Unit Tests

Unit tests verify backend logic, database models, and route behaviour.

Covered functionality includes:

* Block condition compatibility validation
* User creation and database persistence
* Friend relationship creation
* User statistics validation
* Login route rendering
* Signup route rendering
* Authentication protection for account pages

Run unit tests with:

```bash
python -m unittest app.tests -v
```

### Selenium Browser System Tests

System tests verify end-to-end browser functionality and user interactions.

Covered functionality includes:

* Login page rendering
* Signup page rendering
* Navigation from login to signup
* Back-to-game button navigation
* Game button alteration on interaction
* Button redirection validity
* Game interaction checks
* Game logic checks

Before running Selenium tests, start the Flask server:

```bash
python minedoku.py
```

Then, in a separate terminal:

```bash
python -m unittest app.selenium_tests -v
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