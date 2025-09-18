import tkinter as tk
import random

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player, computer):
    if player == computer:
        return 'tie'
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'paper' and computer == 'rock') or \
         (player == 'scissors' and computer == 'paper'):
        return 'player'
    else:
        return 'computer'

class RPSGame:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")

        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0  # Track number of ties

        self.label = tk.Label(master, text="Choose your move:")
        self.label.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        # Scoreboard label now includes ties
        self.score_label = tk.Label(master, text="Player Wins: 0 | Computer Wins: 0 | Ties: 0")
        self.score_label.pack()

        self.rock_button = tk.Button(master, text="Rock", command=lambda: self.play('rock'))
        self.rock_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.paper_button = tk.Button(master, text="Paper", command=lambda: self.play('paper'))
        self.paper_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.scissors_button = tk.Button(master, text="Scissors", command=lambda: self.play('scissors'))
        self.scissors_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10, pady=10)

    def play(self, player_choice):
        computer_choice = get_computer_choice()
        winner = determine_winner(player_choice, computer_choice)

        if winner == 'tie':
            self.tie_score += 1
            result = f"Both chose {player_choice}. It's a tie!"
        elif winner == 'player':
            self.player_score += 1
            result = f"You chose {player_choice}, computer chose {computer_choice}. You win!"
        else:
            self.computer_score += 1
            result = f"You chose {player_choice}, computer chose {computer_choice}. Computer wins!"

        self.result_label.config(text=result)
        # Update scoreboard with ties
        self.score_label.config(
            text=f"Player Wins: {self.player_score} | Computer Wins: {self.computer_score} | Ties: {self.tie_score}"
        )

if __name__ == "__main__":
    # Create the main window for the Tkinter GUI
    root = tk.Tk()
    # Initialize the GUI and game logic
    game = RPSGame(root)
    # Start the Tkinter event loop; this keeps the window open and responsive
    root.mainloop()