# 🐍 Codveda-Technologies

> **Codveda Technologies — Python Development Internship**
>
> **Venkata Sai Ajith Kancheti** · Python Development Intern · CSE (AIML) Student · Aspiring AI/ML Engineer

---

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Web_Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-Markup-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)
  

## 📌 Overview

Each task folder is self-contained with its own source code and, where applicable, a `requirements.txt` file. The repository is organized to make navigation simple for reviewers, recruiters, and fellow learners.

---

## 🎯 Internship Objectives

- Strengthen Python programming fundamentals through practical, task-based projects
- Build real-world mini-applications spanning CLI tools, web apps, and automation scripts
- Practice backend web development using the Django framework
- Implement algorithmic problem-solving techniques (e.g., backtracking)
- Work with external REST APIs and handle live data programmatically
- Apply web scraping techniques using BeautifulSoup and requests
- Maintain clean, structured GitHub documentation throughout the internship

---

## 🗂️ Repository Structure

```
Codveda-Technologies/
│
├── A-Task1-Django_Web_Application/   # Advanced · Django web app with authentication
├── A-Task2-File_Encryption/          # Advanced · File encryption & decryption
├── A-Task3-N-Queens/                 # Advanced · N-Queens backtracking solver
│
├── B-Task1-Smart_Calculator/         # Basic · Four-operation arithmetic calculator
├── B-Task2-Number_Guess/             # Basic · Number guessing game
├── B-Task3-Words_Counter/            # Basic · Word counter for text files
│
├── I-Task1-TO_DO_List/               # Intermediate · CLI to-do list application
├── I-Task2-Web-Data-Scraper/         # Intermediate · Web data scraper
├── I-Task3-API_Integration/          # Intermediate · External API integration script
│
└── README.md                         # This file
```

---

## 🚀 Projects Included

| Level | Folder | Project Name | Description | Key Skills | Status |
|-------|--------|--------------|-------------|------------|--------|
| 🔵 Basic | `B-Task1-Smart_Calculator` | Smart Calculator | CLI calculator performing addition, subtraction, multiplication, and division with division-by-zero handling | Functions, user input, error handling | ✅ Completed |
| 🔵 Basic | `B-Task2-Number_Guess` | Number Guessing Game | Random number generator game with multi-attempt feedback (Too High / Too Low) | `random` module, loops, conditionals | ✅ Completed |
| 🔵 Basic | `B-Task3-Words_Counter` | Word Counter | Reads a text file and counts words; handles file-not-found exceptions | File I/O, string methods, exception handling | ✅ Completed |
| 🟡 Intermediate | `I-Task1-TO_DO_List` | To-Do List App | Command-line task manager with add, delete, view, and mark-as-done features; tasks stored in CSV/JSON | File persistence, CRUD operations, error handling | ✅ Completed |
| 🟡 Intermediate | `I-Task2-Web-Data-Scraper` | Web Data Scraper | Scrapes structured data (headlines / product details) from a website and saves results to CSV | `requests`, `BeautifulSoup`, CSV output | ✅ Completed |
| 🟡 Intermediate | `I-Task3-API_Integration` | API Integration | Fetches and displays live data from an external REST API; handles request failures gracefully | `requests`, JSON parsing, error handling | ✅ Completed |
| 🔴 Advanced | `A-Task1-Django_Web_Application` | Django Web Application | Full-stack Django web app with user registration, login, logout, role-based access, and password reset via email | Django, HTML, authentication, ORM | ✅ Completed |
| 🔴 Advanced | `A-Task2-File_Encryption` | File Encryption / Decryption | Encrypts and decrypts text files using Caesar cipher or Fernet symmetric encryption | Cryptography, file handling, `cryptography` library | ✅ Completed |
| 🔴 Advanced | `A-Task3-N-Queens` | N-Queens Solver | Solves the classic N-Queens problem using backtracking on an N×N chessboard | Recursion, backtracking, 2D arrays, constraint satisfaction | ✅ Completed |

---

## 🛠️ Technology Stack

**Programming Languages**
- Python 3.11

**Frameworks**
- Django (web application development)

**Libraries & Modules**
- `random` — number generation
- `os`, `csv`, `json` — file and data handling
- `requests` — HTTP requests and API calls
- `BeautifulSoup4` — HTML parsing and web scraping
- `cryptography` (Fernet) — file encryption/decryption
- `django.contrib.auth` — user authentication

**Frontend**
- HTML5 (Django templates)

**Tools & Platforms**
- Git & GitHub — version control and repository management
- Python `venv` — virtual environment management
- pip — package management
- Windows CMD / Terminal

**Concepts Practiced**
- Modular programming and function design
- CLI application development
- CRUD operations and persistent file storage
- Web scraping (ethical use)
- REST API consumption
- Backtracking and recursive algorithms
- User authentication and session management
- Exception handling and input validation

---

## ✨ Project Highlights

- **9 tasks completed** across three difficulty levels (Basic, Intermediate, Advanced)
- **Django web application** with a complete authentication system including user registration, login/logout, and password reset
- **File encryption** implemented using symmetric key cryptography for real-world applicability
- **N-Queens solver** demonstrating algorithmic thinking with backtracking — a classic computer science problem
- **Web scraper** built with BeautifulSoup that extracts and exports structured data to CSV
- **Live API integration** that fetches, parses, and displays data from an external service with robust error handling
- **CLI tools** (calculator, number game, word counter, to-do list) covering fundamental Python patterns
- **Organized, level-based repository structure** making navigation and review straightforward

---

## ▶️ How to Run the Projects

> **Note:** Commands may vary slightly depending on individual project requirements. Always check for a `requirements.txt` inside the task folder before running.

**Step 1 — Clone the repository**
```cmd
git clone https://github.com/kvsajith34/Codveda-Technologies.git
cd Codveda-Technologies
```

**Step 2 — Navigate into the desired task folder**
```cmd
cd B-Task1-Smart_Calculator
```
*(Replace with any folder name from the repository)*

**Step 3 — Create and activate a virtual environment**
```cmd
py -3.11 -m venv venv
venv\Scripts\activate
```

**Step 4 — Install dependencies (if applicable)**
```cmd
pip install -r requirements.txt
```

**Step 5 — Run the project**
```cmd
python main.py
```

> For the Django project (`A-Task1-Django_Web_Application`), additional steps such as `python manage.py migrate` and `python manage.py runserver` will apply. Refer to the task folder for specifics.

---

## 📚 Learning Outcomes

Through this internship, I developed and reinforced the following skills:

- **Python fundamentals** — data types, control flow, functions, modules, and OOP concepts
- **Modular coding** — breaking problems into reusable, well-structured functions
- **Debugging** — identifying and resolving runtime errors, logic bugs, and dependency issues
- **GitHub project organization** — maintaining a clean, navigable repository with meaningful commit messages
- **Web development basics** — building views, templates, and URL routing with Django
- **API handling** — making GET requests, parsing JSON responses, and handling API errors
- **Web scraping** — retrieving and parsing HTML content responsibly with BeautifulSoup
- **Problem-solving** — applying backtracking and algorithmic reasoning to classic CS problems
- **Technical documentation** — writing clear READMEs suitable for GitHub and internship review

---

## 📊 Internship Progress Summary

| Metric | Details |
|--------|---------|
| Total Tasks Completed | 9 / 9 |
| Basic Level Tasks (Level 1) | 3 |
| Intermediate Level Tasks (Level 2) | 3 |
| Advanced Level Tasks (Level 3) | 3 |
| Repository Documentation | ✅ Complete |
| GitHub Upload Status | ✅ All tasks uploaded |

---

## 🔮 Future Improvements

- Add basic unit tests for calculator, word counter, and to-do list projects
- Improve UI/UX for the Django web application
- Deploy selected projects (e.g., Django app on Render or Railway)
- Add live demo links where applicable
- Refactor code in earlier tasks for better readability and structure

---

## 👤 Author

**Venkata Sai Ajith Kancheti**
CSE (AIML) Student · Aspiring AI/ML Engineer

[![GitHub](https://img.shields.io/badge/GitHub-kvsajith34-181717?style=flat-square&logo=github)](https://github.com/kvsajith34)


---

## 📄 License

This repository is maintained for **educational and internship submission purposes**.
---

<p align="center">
  Made by Venkata Sai Ajith Kancheti &nbsp;
</p>
