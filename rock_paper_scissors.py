"""
Create a Rock Paper Scissors game where players can put in their choice and the game will determine the winner.
and play against the computer that randomly selects a move with the game being able 
to show who won each round.
Add the score of who wins each round and allows the game to continue until the 
player types "quit".
"""

import random

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player, computer):
    if player == 'r':
        player = 'rock'
    elif player == 'p':
        player = 'paper'
    elif player == 's':
        player = 'scissors'

    if player == computer:
        return "It's a tie!"
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'paper' and computer == 'rock') or \
         (player == 'scissors' and computer == 'paper'):
        return "You win!"
    else:
        return "Computer wins!"

def main():
    player_score = 0
    computer_score = 0

    while True:
        player_choice = input("Enter rock, paper, scissors or quit to exit: ").lower()
        if player_choice == 'quit':
            break

        if player_choice not in ['rock', 'paper', 'scissors', 'r', 'p', 's']:
            print("Invalid choice. Please try again.")
            continue


        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")

        result = determine_winner(player_choice, computer_choice)
        print(result)

        if result == "You win!":
            player_score += 1
        elif result == "Computer wins!":
            computer_score += 1

        print(f"Score - You: {player_score}, Computer: {computer_score}\n")



# --- GUI Implementation ---
import tkinter as tk
from tkinter import messagebox


class RPSGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")
        master.configure(bg="#222831")  # Dark background
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.rounds = 0

        label_fg = "#eeeeee"
        label_bg = "#222831"
        button_bg = "#00adb5"
        button_fg = "#222831"
        scoreboard_bg = "#393e46"
        scoreboard_fg = "#ffd369"

        self.label = tk.Label(master, text="Choose Rock, Paper, or Scissors:", font=("Arial", 14, "bold"), fg=label_fg, bg=label_bg)
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(master, bg=label_bg)
        self.button_frame.pack()
        self.rock_button = tk.Button(self.button_frame, text="Rock", width=10, font=("Arial", 12, "bold"), bg=button_bg, fg=button_fg, activebackground="#ffd369", command=lambda: self.play('rock'))
        self.rock_button.grid(row=0, column=0, padx=5)
        self.paper_button = tk.Button(self.button_frame, text="Paper", width=10, font=("Arial", 12, "bold"), bg=button_bg, fg=button_fg, activebackground="#ffd369", command=lambda: self.play('paper'))
        self.paper_button.grid(row=0, column=1, padx=5)
        self.scissors_button = tk.Button(self.button_frame, text="Scissors", width=10, font=("Arial", 12, "bold"), bg=button_bg, fg=button_fg, activebackground="#ffd369", command=lambda: self.play('scissors'))
        self.scissors_button.grid(row=0, column=2, padx=5)

        self.result_label = tk.Label(master, text="", font=("Arial", 12), fg="#ffd369", bg=label_bg)
        self.result_label.pack(pady=10)

        self.scoreboard_label = tk.Label(master, text=self.get_scoreboard_text(), font=("Arial", 12, "bold"), justify="left", bg=scoreboard_bg, fg=scoreboard_fg, bd=2, relief="groove", padx=10, pady=5)
        self.scoreboard_label.pack(pady=5)

        self.quit_button = tk.Button(master, text="Quit", font=("Arial", 11, "bold"), bg="#ff2e63", fg="white", activebackground="#393e46", command=master.quit)
        self.quit_button.pack(pady=5)

    def get_scoreboard_text(self):
        return (f"Rounds Played: {self.rounds}\n"
                f"Player Wins: {self.player_score}\n"
                f"Computer Wins: {self.computer_score}\n"
                f"Ties: {self.tie_score}")

    def play(self, player_choice):
        computer_choice = get_computer_choice()
        result = determine_winner(player_choice, computer_choice)
        self.rounds += 1
        if result == "You win!":
            self.player_score += 1
        elif result == "Computer wins!":
            self.computer_score += 1
        elif result == "It's a tie!":
            self.tie_score += 1
        self.result_label.config(text=f"Computer chose: {computer_choice}\n{result}")
        self.scoreboard_label.config(text=self.get_scoreboard_text())
if __name__ == "__main__":
    # Uncomment the next line to use CLI version
    # main()
    root = tk.Tk()
    app = RPSGameGUI(root)
    root.mainloop()