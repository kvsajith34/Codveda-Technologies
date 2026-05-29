# 🎯 Number Guessing Game


A beginner-friendly, terminal-based Python game where the computer secretly picks a number between 1 and 100, and the player tries to guess it within 10 attempts using "Too high" or "Too low" feedback.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Objectives](#objectives)
- [Folder Structure](#folder-structure)
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [Gameplay Demo](#gameplay-demo)
- [Features](#features)
- [Input Validation](#input-validation)
- [Code Structure](#code-structure)
- [Author](#author)

---

## 📖 About the Project

This project is **Task 2 of Level 1 (Basic)** from the Codveda Technologies Python Internship program.

The game uses Python's built-in `random` module to generate a secret number between **1 and 100**. The player is given up to **10 attempts** to guess the number. After each guess, the program provides clear directional feedback. The game ends when the player guesses correctly or exhausts all attempts, and a **replay option** is offered at the end of every round.

---

## 🎯 Objectives

- [x] Use the `random` module to generate a random number
- [x] Give the user multiple attempts to guess the number
- [x] Provide feedback — `Too high`, `Too low`, or `Correct!`
- [x] Exit the game when the user guesses correctly or runs out of attempts
- [x] Handle invalid inputs gracefully (blank, non-numeric, out-of-range)
- [x] Display attempts used at the end of each round
- [x] Offer a replay option after every game

---

## 📁 Folder Structure

```
Codveda-Technologies/
└── B-Task2-Number_Guess/
    ├── number_guessing_game.py    ← Main game file
    └── README.md                  ← Project documentation
```

---

## ✅ Prerequisites

- **Python 3.x** installed on your system
- No external libraries required — uses only Python's built-in `random` module

To check your Python version:

```bash
python --version
```

---

## ▶️ How to Run

**Step 1 — Clone or download the project folder**

```bash
git clone https://github.com/your-username/B-Task2-Number_Guess.git
```

Or simply download `number_guessing_game.py` directly.

**Step 2 — Navigate to the project directory**

```bash
cd Codveda-Technologies/B-Task2-Number_Guess
```

**Step 3 — Run the game**

```bash
python number_guessing_game.py
```

> On some systems, use `python3` instead of `python`.

---

## 🖥️ Gameplay Demo

```
=======================================================
       NUMBER GUESSING GAME – Codveda Technologies
=======================================================
  Guess the secret number between 1 and 100.
  You have 10 attempts. Good luck!

  Attempt 1/10  (9 left)  →  Your guess: 48
  📈  Too high! Try a lower number.

  Attempt 2/10  (8 left)  →  Your guess: 32
  📉  Too low!  Try a higher number.

  Attempt 3/10  (7 left)  →  Your guess: 39
  📉  Too low!  Try a higher number.

  Attempt 4/10  (6 left)  →  Your guess: 42
  🎉  Correct! You guessed it!

-------------------------------------------------------
  ✅  You won in 4 attempt(s)! Well done!
-------------------------------------------------------

  Play again? (yes / no): no

  Thanks for playing! Goodbye 👋
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎲 Random Number | Generates a new secret number every round |
| 🔁 Multiple Attempts | Player gets up to 10 chances per game |
| 📢 Clear Feedback | "Too high", "Too low", or "Correct!" after every guess |
| 🛡️ Input Validation | Handles blank, non-numeric, and out-of-range inputs |
| 📊 Attempt Counter | Shows current attempt and remaining attempts live |
| 🏁 End Summary | Displays win/loss result and total attempts used |
| 🔄 Replay Option | Player can choose to start a new round instantly |
| 🧹 Clean Code | Well-commented, function-based, beginner-readable |

---

## 🛡️ Input Validation

The game safely handles all edge cases:

| Invalid Input | Example | Response |
|---|---|---|
| Empty input | *(just pressing Enter)* | `⚠ Please enter a number. Don't leave it blank.` |
| Non-numeric text | `hello`, `abc` | `⚠ That doesn't look like a number. Try again.` |
| Out-of-range number | `0`, `101`, `-5` | `⚠ Please enter a number between 1 and 100.` |

The attempt counter is **not penalized** for invalid inputs — only valid guesses count.

---

## 🧩 Code Structure

```python
number_guessing_game.py
│
├── generate_number()     → Generates the secret random number
├── get_user_guess()      → Prompts and validates user input
├── give_feedback()       → Prints Too high / Too low / Correct
├── display_banner()      → Shows the welcome screen
├── display_result()      → Shows the end-of-round summary
├── ask_replay()          → Handles the play-again prompt
├── play_game()           → Runs one complete game round
└── main()                → Program entry point
```

---

## 👤 Author

**KVS Ajith**
Python Internship — Level 1, Task 2
Codveda Technologies

---

> *This project was built as part of the Codveda Technologies Internship Program to demonstrate core Python skills including loops, conditionals, functions, input handling, and error management.*