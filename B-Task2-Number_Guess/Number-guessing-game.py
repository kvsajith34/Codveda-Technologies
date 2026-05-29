# ============================================================
#  Number Guessing Game
#  Author   : [Your Name]
#  Company  : Codveda Technologies Internship
#  Level    : 1 – Basic  |  Task 2
#  Language : Python 3
# ============================================================
#
#  Description:
#  The program randomly selects a number between 1 and 100.
#  The user gets up to MAX_ATTEMPTS tries to guess it.
#  After every guess the program replies "Too high", "Too low",
#  or "Correct!". Invalid inputs are handled gracefully.
#  A replay option is offered at the end of every round.
# ============================================================

import random

# ── Constants ────────────────────────────────────────────────
MIN_NUMBER   = 1
MAX_NUMBER   = 100
MAX_ATTEMPTS = 10          # maximum guesses allowed per round


# ── Helper Functions ─────────────────────────────────────────

def generate_number():
    """Return a random integer between MIN_NUMBER and MAX_NUMBER (inclusive)."""
    return random.randint(MIN_NUMBER, MAX_NUMBER)


def get_user_guess(attempt_number, attempts_left):
    """
    Prompt the user for a guess and return a validated integer.

    Keeps asking until the user enters:
      • a numeric value
      • within the range [MIN_NUMBER, MAX_NUMBER]

    Returns the validated integer guess.
    """
    while True:
        prompt = (
            f"\n  Attempt {attempt_number}/{MAX_ATTEMPTS}  "
            f"({attempts_left} left)  →  Your guess: "
        )
        raw = input(prompt).strip()

        # Guard: empty input
        if not raw:
            print("  ⚠  Please enter a number. Don't leave it blank.")
            continue

        # Guard: non-numeric input
        if not raw.lstrip("-").isdigit():
            print("  ⚠  That doesn't look like a number. Try again.")
            continue

        guess = int(raw)

        # Guard: out-of-range input
        if guess < MIN_NUMBER or guess > MAX_NUMBER:
            print(f"  ⚠  Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
            continue

        return guess          # valid guess – exit the loop


def give_feedback(guess, secret_number):
    """
    Compare the guess with the secret number and print feedback.

    Returns:
        True  – if the guess is correct
        False – otherwise
    """
    if guess < secret_number:
        print("  📉  Too low!  Try a higher number.")
        return False
    elif guess > secret_number:
        print("  📈  Too high! Try a lower number.")
        return False
    else:
        print("  🎉  Correct! You guessed it!")
        return True


def display_banner():
    """Print the welcome banner at the start of the program."""
    print("=" * 55)
    print("       NUMBER GUESSING GAME – Codveda Technologies")
    print("=" * 55)
    print(f"  Guess the secret number between {MIN_NUMBER} and {MAX_NUMBER}.")
    print(f"  You have {MAX_ATTEMPTS} attempts. Good luck!\n")


def display_result(won, secret_number, attempts_used):
    """Print the end-of-round summary."""
    print("\n" + "-" * 55)
    if won:
        print(f"  ✅  You won in {attempts_used} attempt(s)! Well done!")
    else:
        print(f"  ❌  Out of attempts! The secret number was {secret_number}.")
    print("-" * 55)


def ask_replay():
    """
    Ask the user if they want to play again.

    Returns:
        True  – user wants another round
        False – user wants to quit
    """
    while True:
        choice = input("\n  Play again? (yes / no): ").strip().lower()
        if choice in ("yes", "y"):
            return True
        elif choice in ("no", "n"):
            return False
        else:
            print("  ⚠  Please type 'yes' or 'no'.")


# ── Core Game Function ────────────────────────────────────────

def play_game():
    """
    Run one complete round of the number guessing game.

    Flow:
      1. Generate a secret number.
      2. Loop: get a guess → give feedback → check win/loss.
      3. Display the final result.

    Returns:
        True  – player won
        False – player lost
    """
    secret_number = generate_number()
    won           = False

    for attempt in range(1, MAX_ATTEMPTS + 1):
        attempts_left = MAX_ATTEMPTS - attempt   # remaining after this attempt

        guess = get_user_guess(attempt, attempts_left)
        won   = give_feedback(guess, secret_number)

        if won:
            display_result(won=True, secret_number=secret_number, attempts_used=attempt)
            return True

    # Reached here → all attempts exhausted without a correct guess
    display_result(won=False, secret_number=secret_number, attempts_used=MAX_ATTEMPTS)
    return False


# ── Entry Point ───────────────────────────────────────────────

def main():
    """
    Program entry point.
    Displays the banner, then repeatedly calls play_game()
    until the user chooses to quit.
    """
    display_banner()

    while True:
        play_game()

        if not ask_replay():
            print("\n  Thanks for playing! Goodbye 👋\n")
            break

        print("\n" + "=" * 55)
        print("       Starting a new round …")
        print("=" * 55)


# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    main()