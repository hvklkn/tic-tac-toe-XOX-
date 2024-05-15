import tkinter as tk
from tkinter import messagebox
from tic_tac_toe import TicTacToe, QLearningAgent

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        # Ekran boyutunu belirleme
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 500
        window_height = 500

        # Ekranı ortala
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Arka plan rengini mavi yapma ve metin eklemek
        self.master.configure(bg="pink")
        self.background_label = tk.Label(self.master, text="Tic Tac Toe", font=("Arial", 24, "bold"), fg="black", bg="pink")
        self.background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Zorluk seviyesi menüsünü oluşturma
        self.level_var = tk.StringVar()
        self.level_var.set("Easy")
        self.level_menu = tk.OptionMenu(self.master, self.level_var, "Easy", "Medium", "Hard")
        self.level_menu.config(width=10, height=1, font=("Arial", 12))
        self.level_menu.pack(pady=20)

        # Oyun başlatma düğmesini oluşturma
        self.start_button = tk.Button(self.master, text="Oyunu Başlat", command=self.start_game, width=10, height=1, font=("Arial", 15, "italic"), fg="black")
        self.start_button.pack()



        # Oyun tahtası çerçevesini oluşturma
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.game = None
        self.agent = None
        self.buttons = None

    def start_game(self):
        self.game = TicTacToe()
        self.agent = QLearningAgent()

        if self.level_var.get() == "Easy":
            self.agent.level = "easy"
        elif self.level_var.get() == "Medium":
            self.agent.level = "medium"
        elif self.level_var.get() == "Hard":
            self.agent.level = "hard"

        self.create_board()

    def create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.board_frame, text='', width=10, height=3,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def make_move(self, row, col):
        if self.game.make_move(row * 3 + col, 'X'):
            self.update_board()
            if self.game.current_winner is None and self.game.num_empty_squares() > 0:
                self.agent_move()

            # Kullanıcıdan önceki hamlenin ardından gelen durumu al
            next_state = self.game.board
            # Belirttiğiniz kısıtlamaya göre, yanyana, alt alta ve çapraz hamlelerde 'X' olmasını engelle
            if self.game.winner(row * 3 + col, 'X') or self.game.winner(row + 3 * col, 'X'):
                reward = -10  # Eğer kullanıcı böyle bir hamle yaparsa, ödülü azalt
                next_state[row * 3 + col] = ' '  # Kullanıcının hamlesini geri al
                self.agent.update_q_table(self.game.board, row * 3 + col, reward, next_state)
            else:
                reward = 0  # Eğer kullanıcı istenilen hamleyi yaparsa, ödülü sıfıra eşitle
                self.agent.update_q_table(self.game.board, row * 3 + col, reward, next_state)


    def agent_move(self):
        state = self.game.board
        available_actions = self.game.available_moves()
        action = self.agent.choose_action(state, available_actions)
        self.game.make_move(action, 'O')
        self.update_board()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                if self.game.board[i * 3 + j] == 'X':
                    self.buttons[i][j].config(text='X', state='disabled')
                elif self.game.board[i * 3 + j] == 'O':
                    self.buttons[i][j].config(text='O', state='disabled')

        if self.game.current_winner:
            messagebox.showinfo("Game Over", f"{self.game.current_winner} wins!")
            self.reset_game()
        elif not self.game.empty_squares():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_game()

    def reset_game(self):
        self.game = None
        self.agent = None
        self.buttons = None
        self.start_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
