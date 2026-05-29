# ============================================================
#  Word Counter — Codveda Technologies Internship Project
#  Level  : Basic  |  Task 3
#  Author : [Your Name]
#  Date   : 2026
# ============================================================

import os


# ─────────────────────────────────────────────
#  DISPLAY: Welcome banner
# ─────────────────────────────────────────────
def show_banner():
    """Print a simple welcome banner when the program starts."""
    print("=" * 50)
    print("       WORD COUNTER — Codveda Technologies")
    print("             Internship Project")
    print("=" * 50)


# ─────────────────────────────────────────────
#  FUNCTION 1: Read file content
# ─────────────────────────────────────────────
def read_file(file_name):
    """
    Open and read a text file safely.

    Parameters:
        file_name (str): Name/path of the .txt file to read.

    Returns:
        str: The full text content of the file,
             or None if an error occurred.
    """
    try:
        # Check that the input is not blank
        if not file_name.strip():
            print("\n[ERROR] File name cannot be empty. Please enter a valid name.")
            return None

        # Make sure the user is working with a .txt file
        if not file_name.lower().endswith(".txt"):
            print("\n[ERROR] Invalid file type. Please provide a '.txt' file.")
            return None

        # Try to open and read the file
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()

        return content  # Return the raw text

    except FileNotFoundError:
        print(f"\n[ERROR] File '{file_name}' was not found.")
        print("        Please check the file name and try again.")
        return None

    except PermissionError:
        print(f"\n[ERROR] Permission denied. Cannot read '{file_name}'.")
        return None

    except UnicodeDecodeError:
        print(f"\n[ERROR] Could not read '{file_name}'. Make sure it is a plain text file.")
        return None


# ─────────────────────────────────────────────
#  FUNCTION 2: Count words in text
# ─────────────────────────────────────────────
def count_words(content):
    """
    Count the number of words in a given text string.

    Uses Python's split() which automatically ignores
    extra spaces, tabs, and blank lines.

    Parameters:
        content (str): The text content read from the file.

    Returns:
        int: Total word count, or None if the file is empty.
    """
    # split() without arguments splits on ANY whitespace
    # and removes empty strings — perfect for clean counting
    words = content.split()

    # Check if the file has any content at all
    if len(words) == 0:
        print("\n[WARNING] The file is empty. No words to count.")
        return None

    return len(words)


# ─────────────────────────────────────────────
#  FUNCTION 3: Display the result
# ─────────────────────────────────────────────
def display_result(file_name, word_count):
    """
    Print the analysis result in a clean, readable format.

    Parameters:
        file_name  (str): Name of the file that was analysed.
        word_count (int): Total number of words found.
    """
    print("\n" + "-" * 50)
    print("          WORD COUNT RESULT")
    print("-" * 50)
    print(f"  File Name  : {file_name}")
    print(f"  Word Count : {word_count} word(s)")
    print("-" * 50)


# ─────────────────────────────────────────────
#  FUNCTION 4: Ask user for a file name
# ─────────────────────────────────────────────
def get_file_name():
    """
    Prompt the user to enter a file name and return it.

    Returns:
        str: The file name entered by the user.
    """
    print()
    file_name = input("  Enter the text file name (e.g., sample.txt): ").strip()
    return file_name


# ─────────────────────────────────────────────
#  FUNCTION 5: Ask to analyse another file
# ─────────────────────────────────────────────
def ask_to_continue():
    """
    Ask the user whether they want to analyse another file.

    Returns:
        bool: True if user wants to continue, False otherwise.
    """
    print()
    choice = input("  Analyse another file? (yes / no): ").strip().lower()
    return choice in ("yes", "y")


# ─────────────────────────────────────────────
#  MAIN: Program entry point
# ─────────────────────────────────────────────
def main():
    """
    Main controller function.
    Runs the word counter in a loop until the user exits.
    """
    show_banner()

    # Keep running until the user decides to quit
    while True:
        # Step 1 — Get the file name from the user
        file_name = get_file_name()

        # Step 2 — Read the file
        content = read_file(file_name)

        # Step 3 — Count words only if reading succeeded
        if content is not None:
            word_count = count_words(content)

            # Step 4 — Display result only if words were found
            if word_count is not None:
                display_result(file_name, word_count)

        # Step 5 — Ask if the user wants to try another file
        if not ask_to_continue():
            print("\n  Thank you for using Word Counter!")
            print("  Goodbye!\n")
            break


# ─────────────────────────────────────────────
#  Run the program
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
