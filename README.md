# 🐍 Python Development Internship 

> A curated collection of **9 Python projects** built progressively from Basic to Advanced level  

---

## 📌 Table of Contents

- [Repository Overview](#repository-overview)
- [Technology Stack](#technology-stack)
- [Skills Demonstrated](#skills-demonstrated)
- [Difficulty Level Guide](#difficulty-level-guide)
- [Project Catalog](#project-catalog)
- [Folder Structure](#folder-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Learning Outcomes](#learning-outcomes)
- [License](#license)

---

## 📂 Repository Overview

This repository contains **9 project submissions** organized into three progressive difficulty tiers:

| Tier | Prefix | Projects | Focus Area |
|---|---|---|---|
| 🟢 Basic | `B-` | 3 | Python fundamentals, CLI programs, logic building |
| 🟡 Intermediate | `I-` | 3 | Data handling, web scraping, external API usage |
| 🔴 Advanced | `A-` | 3 | Web frameworks, cryptography, algorithm design |

**Language Composition:** Python `76%` · TypeScript `13.2%` · HTML `10.1%` · Other `0.7%`

---

## 🛠 Technology Stack

| Category | Technologies |
|---|---|
| **Core Language** | Python 3.x |
| **Web Framework** | Django |
| **Web Scraping** | `requests`, `BeautifulSoup4` |
| **API Integration** | `requests`, REST APIs |
| **Cryptography** | `cryptography` (Fernet / AES) |
| **Frontend (Django)** | HTML5, CSS3, TypeScript |
| **Algorithms** | Backtracking, Recursion |
| **Data Handling** | File I/O, JSON, CSV |
| **CLI Tooling** | `argparse`, standard `input()` |
| **Dependency Management** | `pip`, `requirements.txt` |

---

## 💡 Skills Demonstrated

- **Python fundamentals** — variables, loops, conditionals, functions, error handling
- **Object-Oriented Programming** — classes, encapsulation, modular design
- **File I/O** — reading, writing, encrypting, and managing files
- **Web Scraping** — parsing HTML with BeautifulSoup, sending HTTP requests
- **API Consumption** — working with REST endpoints, handling JSON responses
- **Django Web Development** — MVC architecture, URL routing, views, templates, ORM
- **Cryptography** — symmetric file encryption and decryption using the `cryptography` library
- **Algorithm Design** — backtracking-based N-Queens solver with constraint satisfaction
- **CLI Application Design** — user input handling, validation, interactive menus
- **Dependency management** — virtual environments, `requirements.txt`

---

## 📊 Difficulty Level Guide

| Symbol | Level | Description |
|---|---|---|
| 🟢 `B-` | **Basic** | Single-file CLI scripts. Core Python syntax, control flow, and standard library. No external dependencies. |
| 🟡 `I-` | **Intermediate** | Multi-module projects. External libraries (`requests`, `bs4`), file persistence, real-world API calls. |
| 🔴 `A-` | **Advanced** | Full-stack and algorithmic complexity. Django MVC, symmetric-key cryptography, recursive backtracking. |

---

## 🗂 Project Catalog

### 🟢 Basic Level

| # | Project | Type | Description | Key Concepts |
|---|---|---|---|---|
| B-1 | [Smart Calculator](./B-Task1-Smart_Calculator/) | CLI App | Interactive calculator supporting arithmetic and potentially scientific operations | Operators, functions, input validation, error handling |
| B-2 | [Number Guess](./B-Task2-Number_Guess/) | CLI Game | Random number guessing game with feedback (higher/lower) and attempt tracking | `random` module, loops, conditionals, game logic |
| B-3 | [Words Counter](./B-Task3-Words_Counter/) | Utility Tool | Reads text input or a file and counts words, characters, and sentences | String methods, file I/O, text processing |

---

### 🟡 Intermediate Level

| # | Project | Type | Description | Key Concepts |
|---|---|---|---|---|
| I-1 | [To-Do List](./I-Task1-TO_DO_List/) | CLI / File App | Task manager supporting add, view, update, delete, and persist tasks to a file | CRUD logic, file persistence (JSON/txt), OOP |
| I-2 | [Web Data Scraper](./I-Task2-Web-Data-Scraper/) | Scraper | Scrapes structured data from a web page and exports to a readable format | `requests`, `BeautifulSoup4`, HTML parsing, CSV/JSON export |
| I-3 | [API Integration](./I-Task3-API_Integration/) | API Client | Consumes a public REST API (weather, news, or similar) and displays parsed results | REST APIs, `requests`, JSON parsing, key management |

---

### 🔴 Advanced Level

| # | Project | Type | Description | Key Concepts |
|---|---|---|---|---|
| A-1 | [Django Web Application](./A-Task1-Django_Web_Application/) | Web App | Full-featured Django web application with views, templates, URL routing, and a database-backed model | Django MVT, ORM, HTML/TS frontend, admin panel |
| A-2 | [File Encryption](./A-Task2-File_Encryption/) | Security Tool | Encrypts and decrypts files using symmetric-key cryptography | `cryptography` library, Fernet/AES, key generation, binary I/O |
| A-3 | [N-Queens Solver](./A-Task3-N-Queens/) | Algorithm | Solves the classic N-Queens problem using backtracking and visualizes all valid board configurations | Backtracking, recursion, constraint satisfaction, matrix manipulation |

---

## 🗃 Folder Structure

```
Codveda-Technologies/
│
├── B-Task1-Smart_Calculator/       # Basic: CLI arithmetic calculator
│   └── *.py
│
├── B-Task2-Number_Guess/           # Basic: Number guessing game
│   └── *.py
│
├── B-Task3-Words_Counter/          # Basic: Word & character counter
│   └── *.py
│
├── I-Task1-TO_DO_List/             # Intermediate: Persistent to-do manager
│   └── *.py
│
├── I-Task2-Web-Data-Scraper/       # Intermediate: Web scraper with export
│   ├── *.py
│   └── requirements.txt
│
├── I-Task3-API_Integration/        # Intermediate: REST API client
│   ├── *.py
│   └── requirements.txt
│
├── A-Task1-Django_Web_Application/ # Advanced: Django full-stack web app
│   ├── manage.py
│   ├── templates/
│   ├── static/
│   ├── <app>/
│   └── requirements.txt
│
├── A-Task2-File_Encryption/        # Advanced: File encryption tool
│   ├── *.py
│   └── requirements.txt
│
└── A-Task3-N-Queens/               # Advanced: N-Queens backtracking solver
    └── *.py
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)
- Git

### Clone the Repository

```bash
git clone https://github.com/kvsajith34/Codveda-Technologies.git
cd Codveda-Technologies
```

### Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### Install Project-Specific Dependencies

Each project with external dependencies contains its own `requirements.txt`. Navigate to the relevant folder and install:

```bash
cd <project-folder>
pip install -r requirements.txt
```

For Basic-level projects (no external dependencies), no installation is required beyond Python itself.

---

## ▶️ How to Run

### 🟢 Basic Projects

```bash
# Smart Calculator
cd B-Task1-Smart_Calculator
python calculator.py

# Number Guessing Game
cd B-Task2-Number_Guess
python number_guess.py

# Words Counter
cd B-Task3-Words_Counter
python words_counter.py
```

### 🟡 Intermediate Projects

```bash
# To-Do List Manager
cd I-Task1-TO_DO_List
python todo.py

# Web Data Scraper
cd I-Task2-Web-Data-Scraper
pip install -r requirements.txt
python scraper.py

# API Integration
cd I-Task3-API_Integration
pip install -r requirements.txt
python api_client.py
```

> **Note:** The API Integration project may require an API key. Check the project folder for a `.env.example` or configuration instructions.

### 🔴 Advanced Projects

```bash
# Django Web Application
cd A-Task1-Django_Web_Application
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Open http://127.0.0.1:8000 in your browser

# File Encryption Tool
cd A-Task2-File_Encryption
pip install -r requirements.txt
python encrypt.py

# N-Queens Solver
cd A-Task3-N-Queens
python nqueens.py
```

---

## 🎓 Learning Outcomes

By building these 9 projects across three difficulty levels, the following competencies were developed:

**Foundational Python**
- Writing clean, readable, and Pythonic code
- Handling user input, edge cases, and exceptions gracefully
- Working with strings, lists, dictionaries, and file I/O

**Intermediate Engineering**
- Structuring multi-module Python projects
- Integrating third-party libraries and managing dependencies
- Consuming REST APIs and processing JSON data
- Scraping and transforming web content programmatically

**Advanced Engineering**
- Building full-stack web applications with Django's MVT pattern
- Implementing symmetric encryption for secure file handling
- Designing recursive algorithms with backtracking for constraint problems
- Understanding application security fundamentals

---

## 🤝 Contributing

This repository was created as part of a structured internship program. Contributions are welcome for improvements, bug fixes, or documentation enhancements.

```
1. Fork this repository
2. Create a feature branch:  git checkout -b feature/improvement-name
3. Commit your changes:      git commit -m "Add: meaningful description"
4. Push to the branch:       git push origin feature/improvement-name
5. Open a Pull Request
```

Please ensure your code follows Python best practices (PEP 8) and includes clear comments or docstrings.

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this code with attribution.

```
MIT License — Copyright (c) 2025 kvsajith34
```

See the [LICENSE](./LICENSE) file for full terms.

---


<div align="center">

**Built with 🐍 Python · Submitted under the Python Development Internship**  

[![GitHub](https://img.shields.io/badge/GitHub-kvsajith34-181717?style=flat&logo=github)](https://github.com/kvsajith34)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](./LICENSE)

</div>
