import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class GameNode:
    def __init__(self, numbers, scores, current_player):
        self.numbers = numbers
        self.scores = scores
        self.current_player = current_player

class NumberPairGame:
    def __init__(self, root, bot_enabled=False, num_count=15, player_starts=True, algorithm='minimax'):
        self.root = root
        self.root.title("Number Pair Game")

        self.bot_enabled = bot_enabled
        self.numbers = [random.randint(1, 9) for _ in range(num_count)]
        self.scores = {1: 0, 2: 0}
        self.current_player = 1 if player_starts else 2
        self.selected = []
        self.bot_playing = False
        self.algorithm = algorithm

        self.create_widgets()
        self.update_display()

        if self.bot_enabled and self.current_player == 2:
            self.bot_play()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Number Pair Game", font=("Arial", 16))
        self.title_label.pack()

        self.score_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.score_label.pack()

        self.turn_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.turn_label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

    def update_display(self):
        self.score_label.config(text=f"Player 1: {self.scores[1]} | Player 2: {self.scores[2]}")
        self.turn_label.config(text=f"Turn: {'Player 1' if self.current_player == 1 else 'Bot' if self.bot_enabled else 'Player 2'}")

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for i, num in enumerate(self.numbers):
            btn = tk.Button(self.button_frame, text=str(num), width=3,
                            command=lambda idx=i: self.on_number_click(idx))
            btn.grid(row=0, column=i, padx=2, pady=5)

        if len(self.numbers) <= 1:
            self.declare_winner()

    def on_number_click(self, index):
        if self.current_player == 2 and self.bot_enabled:
            return

        if index in self.selected:
            self.selected.remove(index)
        elif len(self.selected) < 2 and (not self.selected or abs(self.selected[0] - index) == 1):
            self.selected.append(index)

        if len(self.selected) == 2:
            self.process_turn(self.selected[0], self.selected[1])

    def process_turn(self, index1, index2):
        if abs(index1 - index2) != 1:
            return

        num1, num2 = self.numbers[index1], self.numbers[index2]
        score_bonus = 3 if (num1 + num2) > 7 else 2 if (num1 + num2) == 7 else 1
        self.scores[self.current_player] += score_bonus

        if index1 < index2:
            del self.numbers[index2]
            del self.numbers[index1]
        else:
            del self.numbers[index1]
            del self.numbers[index2]

        self.selected = []
        self.current_player = 1 if self.current_player == 2 else 2
        self.update_display()

        if self.bot_enabled and self.current_player == 2:
            self.root.after(500, self.bot_play)

    def bot_play(self):
        self.bot_playing = True

        possible_moves = self.get_possible_moves(self.numbers)
        if not possible_moves:
            messagebox.showinfo("Game Over", "Bot has no valid move!")
            self.declare_winner()
            return
        
        if self.algorithm == 'minimax':
            _, best_move = self.minimax(GameNode(self.numbers, self.scores.copy(), 2), depth=3, maximizing=True)
        elif self.algorithm == 'alpha_beta':
            _, best_move = self.alpha_beta(GameNode(self.numbers, self.scores.copy(), 2), depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True)

        if best_move:
            self.process_turn(*best_move)

        self.bot_playing = False

    def minimax(self, node, depth, maximizing):
        if depth == 0 or not self.get_possible_moves(node.numbers):
            return self.heuristic_evaluation(node), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves(node.numbers):
                new_node = self.create_child_node(node, move, 2)
                eval_score, _ = self.minimax(new_node, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(node.numbers):
                new_node = self.create_child_node(node, move, 1)
                eval_score, _ = self.minimax(new_node, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def alpha_beta(self, node, depth, alpha, beta, maximizing):
        if depth == 0 or not self.get_possible_moves(node.numbers):
            return self.heuristic_evaluation(node), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves(node.numbers):
                new_node = self.create_child_node(node, move, 2)
                eval_score, _ = self.alpha_beta(new_node, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(node.numbers):
                new_node = self.create_child_node(node, move, 1)
                eval_score, _ = self.alpha_beta(new_node, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def create_child_node(self, node, move, player):
        num1, num2 = node.numbers[move[0]], node.numbers[move[1]]
        score_bonus = 3 if (num1 + num2) > 7 else 2 if (num1 + num2) == 7 else 1
        new_numbers = node.numbers[:move[0]] + node.numbers[move[0] + 1:move[1]] + node.numbers[move[1] + 1:]
        new_scores = node.scores.copy()
        new_scores[player] += score_bonus
        return GameNode(new_numbers, new_scores, 1 if player == 2 else 2)

    def get_possible_moves(self, numbers):
        return [(i, i + 1) for i in range(len(numbers) - 1)]

    def heuristic_evaluation(self, node):
        player_score = node.scores[2]
        opponent_score = node.scores[1]
        
        score_difference = player_score - opponent_score

        remaining_pairs = len(node.numbers)

        heuristic_value = score_difference + (remaining_pairs / 10)
        
        return heuristic_value

    def declare_winner(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.score_label.config(text="")
        self.turn_label.config(text="")

        if self.scores[1] > self.scores[2]:
            messagebox.showinfo("Game Over", "Player 1 Wins!")
        elif self.scores[2] > self.scores[1]:
            messagebox.showinfo("Game Over", "Bot Wins!" if self.bot_enabled else "Player 2 Wins!")
        else:
            messagebox.showinfo("Game Over", "It's a Draw!")

        self.ask_restart()

    def ask_restart(self):
        restart = messagebox.askyesno("Restart?", "Do you want to play again?")
        if restart:
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.root.destroy()
        choose_mode()

def choose_mode():
    mode_window = tk.Tk()
    mode_window.title("Select Game Mode")

    def start_game(bot_enabled, algorithm):
        while True:
            try:
                num_count = int(simpledialog.askstring("Number Count", "Enter number count (15-25):"))
                if 15 <= num_count <= 25:
                    break
                else:
                    messagebox.showerror("Invalid Input", "Please enter a number between 15 and 25.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

        player_starts = messagebox.askyesno("First Player", "Do you want Player 1 to start? (No = Bot starts)")
        mode_window.destroy()
        root = tk.Tk()
        NumberPairGame(root, bot_enabled, num_count, player_starts, algorithm)
        root.mainloop()

    tk.Label(mode_window, text="Select Game Mode", font=("Arial", 14)).pack(pady=10)
    tk.Button(mode_window, text="Single Player (vs. Bot, Minimax)", command=lambda: start_game(True, 'minimax')).pack(pady=5)
    tk.Button(mode_window, text="Single Player (vs. Bot, Alpha-Beta)", command=lambda: start_game(True, 'alpha_beta')).pack(pady=5)
    tk.Button(mode_window, text="Multiplayer (PvP)", command=lambda: start_game(False, 'minimax')).pack(pady=5)

    mode_window.mainloop()

choose_mode()
