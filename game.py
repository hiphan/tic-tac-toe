import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import ttk
from random import randint
import sys
import os
from ai import SmartAgent


BLACK = (0, 0, 0)
RED = (255, 0, 0)
TEAL = (0, 128, 128)
X = 1
O = 0


class TicTacToe:
    def __init__(self, width, height, human, ai):
        self.width = width
        self.height = height
        # Square size
        self.row_gap = self.width / 3
        self.col_gap = self.height / 3
        self.state = [[-1] * 3 for _ in range(3)]      # Empty board
        self.human_player = human
        self.ai_player = ai
        self.turn = X
        self.turn_counter = 0
        self.winner = None

    def draw_board(self, surf):
        # White board
        surf.fill((255, 255, 255))

        # Draw grid
        for i in range(4):
            pygame.draw.line(surf, BLACK, (0, i * self.row_gap), (height, i * self.row_gap), 5)
            pygame.draw.line(surf, BLACK, (i * self.col_gap, 0), (i * self.col_gap, width), 5)

        # Draw Xs and Os
        for ix in range(3):
            for iy in range(3):
                if self.state[iy][ix] == X:
                    self.draw_x(surf, ix, iy)
                elif self.state[iy][ix] == O:
                    self.draw_o(surf, ix, iy)
        pygame.display.update()

    def place_next(self, x, y):
        if self.turn == X:
            if self.place_x(x, y):
                self.turn = O
        else:
            if self.place_o(x, y):
                self.turn = X

    def place_x(self, x, y):
        ix = int(x // self.col_gap)
        iy = int(y // self.row_gap)

        # Update board
        if self.state[iy][ix] == -1:
            self.state[iy][ix] = X
            self.turn_counter += 1
            return True
        return False

    def draw_x(self, surf, ix, iy):
        # Draw X
        pygame.draw.line(surf, TEAL, (self.col_gap * (ix + 0.25), self.row_gap * (iy + 0.25)), (self.col_gap * (ix + 0.75), self.row_gap * (iy + 0.75)), 5)
        pygame.draw.line(surf, TEAL, (self.col_gap * (ix + 0.25), self.row_gap * (iy + 0.75)), (self.col_gap * (ix + 0.75), self.row_gap * (iy + 0.25)), 5)

    def place_o(self, x, y):
        ix = int(x // self.col_gap)
        iy = int(y // self.row_gap)

        # Update board
        if self.state[iy][ix] == -1:
            self.state[iy][ix] = O
            self.turn_counter += 1
            return True
        return False

    def draw_o(self, surf, ix, iy):
        # Draw O
        center_x = int(self.col_gap * (ix + 0.5))
        center_y = int(self.row_gap * (iy + 0.5))
        pygame.draw.circle(surf, RED, (center_x, center_y), int(self.col_gap // 3), 5)

    def check_winner(self):
        # Check rows
        def check_rows():
            for r in range(3):
                curr_row = self.state[r]
                if curr_row[0] != -1 and curr_row[0] == curr_row[1] and curr_row[1] == curr_row[2]:
                    self.winner = curr_row[0]
                    return True
            return False

        # Check columns
        def check_cols():
            for c in range(3):
                if self.state[0][c] != -1 and self.state[0][c] == self.state[1][c] and self.state[1][c] == self.state[2][c]:
                    self.winner = self.state[0][c]
                    return True
            return False

        # Check diagonals
        def check_diags():
            if self.state[0][0] != -1 and self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]:
                self.winner = self.state[0][0]
                return True
            if self.state[0][2] != -1 and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]:
                self.winner = self.state[0][2]
                return True
            return False

        if check_rows() or check_cols() or check_diags():
            return True
        return False

    def over(self):
        if self.check_winner() or self.turn_counter == 9:
            return True
        else:
            return False

    def restart(self):
        self.state = [[-1] * 3 for _ in range(3)]
        self.turn = X
        self.turn_counter = 0

    def end_popup_msg(self, winner, popup_width=300, popup_height=100):
        popup = tk.Tk()
        popup.wm_title('Game Over!')
        if winner:
            text = winner + ' Won.'
        else:
            text = 'It\'s a tie.'
        label = ttk.Label(popup, text=text)
        label.pack(side="top", padx=10, pady=10)

        def restart_callback():
            global replay
            replay = True
            popup.destroy()

        b1 = ttk.Button(popup, text='Play Again', command=restart_callback)
        b1.pack()

        def exit_callback():
            global replay
            replay = False
            popup.destroy()

        b2 = ttk.Button(popup, text='Exit', command=exit_callback)
        b2.pack()

        # Set position of tkinter pop-up window to the middle of pygame window
        global winfo_x, winfo_y, width, height
        x = winfo_x + width / 2 - popup_width / 2
        y = winfo_y + height / 2 - popup_height / 2
        popup.geometry('%dx%d+%d+%d' % (popup_width, popup_height, x, y))

        # Make sure the popup window is always on top of others
        popup.attributes('-topmost', True)
        popup.update()

        popup.mainloop()


def start_popup_msg(popup_width=300, popup_height=100):
    popup = tk.Tk()
    popup.wm_title('Start a Game')
    label = ttk.Label(popup, text='Choose a side')
    label.pack(side="top", padx=10, pady=10)

    def choose_x_callback():
        global human, ai
        human = X
        ai = O
        popup.destroy()

    b1 = ttk.Button(popup, text='X', command=choose_x_callback)
    b1.pack()

    def choose_o_callback():
        global human, ai
        human = O
        ai = X
        popup.destroy()

    b2 = ttk.Button(popup, text='O', command=choose_o_callback)
    b2.pack()

    # Set position of tkinter pop-up window to the middle of pygame window
    global winfo_x, winfo_y, width, height
    x = winfo_x + width / 2 - popup_width / 2
    y = winfo_y + height / 2 - popup_height / 2
    popup.geometry('%dx%d+%d+%d' % (popup_width, popup_height, x, y))

    popup.attributes('-topmost', True)
    popup.update()

    popup.mainloop()


if __name__ == '__main__':

    # Set the position of pygame window
    winfo_x = 250
    winfo_y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (winfo_x, winfo_y)

    pygame.init()

    width = 900
    height = 900

    playground = pygame.display.set_mode((width, height))
    playground.fill((128, 128, 128))
    pygame.display.update()
    clock = pygame.time.Clock()

    human, ai = -1, -1
    start_popup_msg()

    game = TicTacToe(width, height, human, ai)
    tictactoe_agent = SmartAgent(ai)

    game.draw_board(playground)

    # If AI has the first turn, place X in a corner which has been proven to be optimal (if the opponent does not play
    # the game perfectly)
    # This also helps prevent unnecessary expensive search which might crash
    def play_first_round():

        corner = randint(0, 3)
        if corner == 0:             # TOP LEFT CORNER
            first_move = (0, 0)
        elif corner == 1:
            first_move = (0, 2)     # TOP RIGHT CORNER
        elif corner == 2:
            first_move = (2, 0)     # BOTTOM LEFT CORNER
        else:
            first_move = (2, 2)     # BOTTOM RIGHT CORNER

        first_move_x = first_move[1] * height / 3 + 1
        first_move_y = first_move[0] * width / 3 + 1
        game.place_next(first_move_x, first_move_y)
        game.draw_board(playground)

    def play_next_round():
        next_move = tictactoe_agent.minimax(game, 1000, ai)[0]
        if next_move:
            next_move_x = next_move[1] * height / 3 + 1
            next_move_y = next_move[0] * width / 3 + 1
            game.place_next(next_move_x, next_move_y)
            game.draw_board(playground)

    if ai == X:
        play_first_round()

    replay = True
    running = True
    while running:
        pygame.time.delay(60)
        clock.tick(60)

        if game.over():
            if game.winner == 1:
                winner = 'X'
            elif game.winner == 0:
                winner = 'O'
            else:
                winner = None

            game.end_popup_msg(winner)

            if replay:
                start_popup_msg()
                game = TicTacToe(width, height, human, ai)
                tictactoe_agent.maximizing_player = ai
                if ai == X:
                    play_first_round()
                else:
                    game.draw_board(playground)
            else:
                running = False

        if game.turn == human:
            m = pygame.mouse.get_pressed()
            if m[0]:
                curr_x, curr_y = pygame.mouse.get_pos()
                game.place_next(curr_x, curr_y)
                game.draw_board(playground)
        else:
            print('AI TURN')
            play_next_round()

        k = pygame.key.get_pressed()
        if k[K_r]:
            game = TicTacToe(width, height, human, ai)

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False

    pygame.quit()
    sys.exit()
