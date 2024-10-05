import pygame
import sys
from typing import List, Dict
import random

class TicTac:
    def __init__(self):
        pygame.init()

        self.size = width, height = 600, 600
        self.background = (224, 241, 244)
        self.color_game = (0, 55, 61)
        self.screen = pygame.display.set_mode(self.size)
        self.playerX = pygame.image.load('assets/X.png')
        self.playerO = pygame.image.load('assets/O.png')
        self.playerPos = {
            1: [],
            2: []
        }
        self.currentPlayer = random.randint(1,2)
        self.crossWinnner = None
        self.winner = None
        self.cellTicTac = {}
        char_rect = self.playerX.get_rect()
        for col in range(3):
            for row in range(3):
                centerx = (width/3)*(col) + width/6
                centery = (height/3)*(row) + height/6
                self.cellTicTac[(row,col)] = pygame.Rect(centerx - char_rect.width/2, centery - char_rect.height/2, char_rect.width, char_rect.height)  
        self.play_game()

    def play_game(self):
        while True:
            self.screen.fill(self.background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    posMouse = pygame.mouse.get_pos()
                    clicked_rect = [pos_rect for pos_rect in self.cellTicTac if self.cellTicTac[pos_rect].collidepoint(posMouse)]

                    if len(clicked_rect) > 0 and self.winner is None:
                        next_player = 1 if self.currentPlayer == 2 else 2
                        if clicked_rect[0] not in self.playerPos[self.currentPlayer] and clicked_rect[0] not in self.playerPos[next_player]:
                            self.playerPos[self.currentPlayer].append(clicked_rect[0])
                            self.check_winner()
                            self.currentPlayer = next_player

            self.draw_border()
            self.showPlayerPos()
            self.drawCross()
            pygame.display.flip()

    def draw_border(self):
        screen_width, screen_height = self.size

        lines: List[Dict[str, List[float]]] = [
            {
                'start': [screen_width / 3, 0],
                'end': [screen_width / 3, screen_height]
            },
            {
                'start': [screen_width / 3 * 2, 0],
                'end': [screen_width / 3 * 2, screen_height]
            },
            {
                'start': [0, screen_height / 3],
                'end': [screen_width, screen_height / 3]
            },
            {
                'start': [0, screen_height / 3 * 2],
                'end': [screen_width, screen_height / 3 * 2]
            }
        ]
        for line in lines:
            pygame.draw.line(self.screen, self.color_game, line['start'], line['end'], width=3)

    def showPlayerPos(self):
        width_board, height_board = self.size

        for player in self.playerPos:
            char = self.playerX if player == 1 else self.playerO
            char_rect = char.get_rect()
            positions = self.playerPos[player]

            for pos in positions:
                char_rect.centerx = (width_board/3)*(pos[1]+1) - char_rect.width/2
                char_rect.centery = (height_board/3)*(pos[0]+1) - char_rect.height/2
                self.screen.blit(char,char_rect)

    def check_winner(self):
        posWin1 = self.is_win(self.playerPos[1], "X")
        posWin2 = self.is_win(self.playerPos[2], "O")
        if posWin1 is not None or posWin2 is not None:
            self.crossWinnner = posWin1 if posWin1 is not None else posWin2
        if self.winner is None and len(self.playerPos[1]) + len(self.playerPos[2]) >= 9:
            self.winner = "Draw"

    def is_win(self, player, name):
        winByRow = {}
        winByCol = {}
        winByDiag = {
            1:[],
            2:[]
        }
        for pos in player:
            if pos[0] not in winByRow:
                winByRow[pos[0]] = 1
            else:
                winByRow[pos[0]] += 1
                if winByRow[pos[0]] == 3:
                    self.winner = name
                    return [(pos[0], x) for x in range(3)]
        
            if pos[1] not in winByCol:
                winByCol[pos[1]] = 1
            else:
                winByCol[pos[1]] += 1
                if winByCol[pos[1]] == 3:
                    self.winner = name
                    return [(x, pos[1]) for x in range(3)]

            
            if pos[0] == pos[1]:
                winByDiag[1].append(pos)
                if len(winByDiag[1]) == 3:
                    self.winner = name
                    return [(x, x) for x in range(3)]

            posDiagWin2 = ([0,2],[1,1],[2,0])
            if pos in posDiagWin2:
                winByDiag.append(pos)
                if len(winByDiag[2]) == 3:
                    self.winner = name
                    return posDiagWin2
            

        return None

    def drawCross(self):
        if self.crossWinnner is not None:
            line_1 = {
                'Start': self.cellTicTac[self.crossWinnner[0]].center,
                'End': self.cellTicTac[self.crossWinnner[1]].center,
            }
            line_2 = {
                'Start': self.cellTicTac[self.crossWinnner[1]].center,
                'End': self.cellTicTac[self.crossWinnner[2]].center,
            }
            colorCross = 255, 82, 3
            pygame.draw.line(self.screen, colorCross, line_1['Start'], line_1['End'], width=5)
            pygame.draw.line(self.screen, colorCross, line_2['Start'], line_2['End'], width=5)


if __name__ == "__main__":
    TicTac()