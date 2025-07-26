# guessing_game.py

import random

def guessing_game():
    """
    A simple number guessing game where the user tries to guess a number
    between 1 and 100 chosen by the computer.
    """
    print("=======================================")
    print("   Welcome to the Number Guessing Game!  ")
    print("=======================================")
    print("I'm thinking of a number between 1 and 100.")

    # Generate a random secret number
    secret_number = random.randint(1, 100)
    attempts = 0
    guess = 0

    # Game loop continues until the user guesses the correct number
    while guess != secret_number:
        try:
            # Get the user's guess
            guess_input = input("Enter your guess: ")
            guess = int(guess_input)
            attempts += 1 # Increment the attempt counter

            # Provide feedback to the user
            if guess < secret_number:
                print("Too low! Try again. 🤔")
            elif guess > secret_number:
                print("Too high! Try again. 😳")
            else:
                # The guess is correct
                print("\n🎉 Congratulations! You got it! 🎉")
                print(f"You guessed the number in {attempts} attempts.")
                print("=======================================")

        except ValueError:
            # Handle cases where the user enters non-numeric input
            print("Invalid input. Please enter a whole number.")

# This line makes the script runnable
if __name__ == "__main__":
    guessing_game()
