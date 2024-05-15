class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3'lük boş bir tahta oluşturuyoruz
        self.current_winner = None  # Şu an için kazanan yok

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Tahtadaki sayılandırma (kullanıcıya yardımcı olmak için)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # Oyunda hala boş olan kutucukların indekslerini döndürür
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        # Boş kutucuk sayısını döndürür
        return ' ' in self.board

    def num_empty_squares(self):
        # Boş kutucuk sayısını döndürür
        return self.board.count(' ')

    def make_move(self, square, letter):
        # Verilen kutucuğa hamle yapar
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Verilen hamlenin bir galibiyet getirip getirmediğini kontrol eder
        # Satır kontrolü
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Sütun kontrolü
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Çapraz kontrol
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # (0, 4, 8) diyagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # (2, 4, 6) diayonal
            if all([spot == letter for spot in diagonal2]):
                return True
        return False






import numpy as np
import random

class QLearningAgent:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=1.0):
        self.epsilon = epsilon  # Rastgele seçim olasılığı
        self.alpha = alpha      # Öğrenme oranı
        self.gamma = gamma      # Gelecekteki ödül indirgeme oranı
        self.q_table = {}       # Q-tablosu

    def choose_action(self, state, available_actions):
        # Epsilon-Greedy stratejisi ile bir aksiyon seç
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(available_actions)  # Rastgele aksiyon seç
        else:
            # Q-tablosundan en yüksek değeri seç
            state_str = self.convert_state_to_string(state)
            if state_str not in self.q_table:
                # Bu durum için bir giriş yoksa, rastgele bir aksiyon seç
                action = random.choice(available_actions)
            else:
                action = max(self.q_table[state_str], key=self.q_table[state_str].get)
        return action

    def update_q_table(self, state, action, reward, next_state):
        # Q-tablosunu güncelle
        state_str = self.convert_state_to_string(state)
        next_state_str = self.convert_state_to_string(next_state)
        if state_str not in self.q_table:
            self.q_table[state_str] = {action: 0}
        if next_state_str not in self.q_table:
            self.q_table[next_state_str] = {}
        if not self.q_table[next_state_str]:
            # Sonraki durum için bir giriş yoksa, varsayılan değer olarak 0 ata
            self.q_table[next_state_str] = {a: 0 for a in self.valid_actions(next_state)}
        # Q değerini güncelle
        self.q_table[state_str][action] += self.alpha * (reward + self.gamma * max(self.q_table[next_state_str].values()) - self.q_table[state_str][action])

    def convert_state_to_string(self, state):
        # Durumu bir stringe dönüştür
        return ''.join(state)

    def valid_actions(self, state):
        # Geçerli aksiyonları döndürür
        return [i for i, spot in enumerate(state) if spot == ' ']
