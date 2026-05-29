# Word Counter — Codveda Technologies Internship Project

---

## Project Overview

This Python program reads a `.txt` file provided by the user,
counts the total number of words in it, and displays the result
in a clean, readable format.

It is built using only Python's standard library and runs
entirely in the terminal.

---

## Folder Structure

```
word_counter_project/
│
├── word_counter.py          ← Main program (run this)
│
├── sample_files/
│   ├── sample.txt           ← Sample file with content (for testing)
│   └── Empty.txt            ← Empty file (to demo empty-file handling)
│
└── README.md                ← This file
```

---

## How to Run

### Step 1 — Make sure Python is installed
```
python --version
```

### Step 2 — Navigate to the project folder
```
cd word_counter_project
```

### Step 3 — Run the program
```
python word_counter.py
```

### Step 4 — Enter a file name when prompted
```
Enter the text file name (e.g., sample.txt): sample_files/sample.txt
```

---

## Sample Terminal Interaction

### ✅ Normal Run
```
==================================================
       WORD COUNTER — Codveda Technologies
             Internship Project
==================================================

  Enter the text file name (e.g., sample.txt): sample_files/sample.txt

--------------------------------------------------
          WORD COUNT RESULT
--------------------------------------------------
  File Name  : sample_files/sample.txt
  Word Count : 88 word(s)
--------------------------------------------------

  Analyse another file? (yes / no): no

  Thank you for using Word Counter!
  Goodbye!
```

### ❌ File Not Found
```
  Enter the text file name (e.g., sample.txt): missing.txt

[ERROR] File 'missing.txt' was not found.
        Please check the file name and try again.
```

### ⚠️ Empty File
```
  Enter the text file name (e.g., sample.txt): sample_files/empty.txt

[WARNING] The file is empty. No words to count.
```

### ❌ Wrong File Type
```
  Enter the text file name (e.g., sample.txt): notes.pdf

[ERROR] Invalid file type. Please provide a '.txt' file.
```

### ❌ Blank Input
```
  Enter the text file name (e.g., sample.txt):

[ERROR] File name cannot be empty. Please enter a valid name.
```

---

## Technologies Used

- Python 3 (standard library only)
- No external packages required

---

## Internship Review Explanation

> "This project is a beginner-level Python Word Counter built for
> the Codveda Technologies internship. The program reads a plain
> text file provided by the user, splits the content into words
> using Python's built-in string methods, and displays the total
> word count. I structured the code using modular functions —
> read_file(), count_words(), display_result(), and main() —
> to keep each responsibility separate and the code easy to
> maintain. I also implemented try-except blocks to handle
> errors such as file not found, empty file, invalid file type,
> and blank input, so the program never crashes unexpectedly.
> The user can also choose to analyse multiple files in one
> session without restarting the program."

---

*Submitted as part of Codveda Technologies Python Internship — Level 1, Task 3*
