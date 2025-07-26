# rps_game.py

import random

print("Rock, Paper, Scissors - Let's Play! 🪨 📄 ✂️")
print("Type 'quit' to end the game.")

# Initialize scores
player_score = 0
computer_score = 0

while True:
    print("-" * 20)
    
    # Player's choice
    player_choice = input("Your choice (rock, paper, scissors): ").lower()

    if player_choice == 'quit':
        break

    # Validate player's input
    if player_choice not in ['rock', 'paper', 'scissors']:
        print("Invalid choice. Please choose rock, paper, or scissors.")
        continue

    # Computer's choice
    options = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(options)

    print(f"You chose: {player_choice.title()}")
    print(f"Computer chose: {computer_choice.title()}")

    # Determine the winner
    if player_choice == computer_choice:
        print("It's a tie! 🤝")
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'scissors' and computer_choice == 'paper') or \
         (player_choice == 'paper' and computer_choice == 'rock'):
        print("You win this round! 🎉")
        player_score += 1
    else:
        print("Computer wins this round! 💻")
        computer_score += 1
    
    # Display the current score
    print(f"Score -> You: {player_score} | Computer: {computer_score}")


# Final message after quitting
print("\nThanks for playing!")
print(f"Final Score -> You: {player_score} | Computer: {computer_score}")
