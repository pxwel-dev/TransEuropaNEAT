import csv
import random
from FindNeighboursCorrected import FindNeighbours


class Board:
    def __init__(self):
        self.board = []
        self.boardEdgeNeighbours = []
        self.boardRowLengths = []

        with open("TransEuropaBoardCorrected") as file:
            reader = csv.reader(file)
            self.board = list(reader)

        for i in range(0, len(self.board)):
            self.boardRowLengths.append(len(self.board[i]))
            for j in range(0, len(self.board[i])):
                if self.board[i][j] != '*':
                    self.board[i][j] = int(self.board[i][j])
                    if self.board[i][j] == 1:
                        self.board[i][j] = -1
                    elif self.board[i][j] == 2:
                        self.board[i][j] = -2
                    else:
                        pass
                    edgeNeighbours = FindNeighbours(self.board)
                    edgeNeighbours.test_neighbouring_edges(i, j)
                    self.boardEdgeNeighbours.append([self.board[i][j], list([i, j]), edgeNeighbours.neighbours])
                else:
                    pass

        self.yellowCities = {
            'Glasgow': [[0, 3], [0, 4], [1, 8], [1, 9]],
            'Oslo': [[0, 6], [0, 7], [1, 14], [1, 15]],
            'Stockholm': [[0, 8], [0, 9], [1, 18], [1, 19]],
            'Helsinki': [[0, 10], [0, 11], [1, 22], [1, 23]],
            'StPeter': [[0, 12], [0, 13], [1, 26], [1, 27]],
            'Malmo': [[3, 16], [3, 17], [4, 7], [4, 8], [5, 16], [5, 17]],
            'Moscow': [[3, 30], [4, 14], [5, 30], [5, 31]]
        }
        self.redCities = {
            'Dublin': [[3, 4], [3, 5], [4, 1], [4, 2], [5, 4], [5, 5]],
            'London': [[5, 7], [5, 8], [6, 3], [6, 4], [7, 7], [7, 8]],
            'Plymouth': [[7, 2], [7, 3], [8, 0], [8, 1], [9, 2], [9, 3]],
            'Brest': [[9, 1], [9, 2], [10, 1], [11, 1], [11, 2]],
            'Bilbao': [[15, 2], [15, 3], [16, 0], [16, 1], [17, 2], [17, 3]],
            'Madrid': [[19, 0], [19, 1], [20, 0], [21, 1]],
            'Barcelona': [[21, 5], [21, 6], [22, 2], [22, 3], [23, 5], [23, 6]]
        }
        self.orangeCities = {
            'Amsterdam': [[7, 10], [7, 11], [8, 4], [8, 5], [9, 10], [9, 11]],
            'Berlin': [[9, 15], [9, 16], [10, 7], [10, 8], [11, 15], [11, 16]],
            'Warsaw': [[9, 21], [9, 22], [10, 10], [10, 11], [11, 21], [11, 22]],
            'Paris': [[11, 8], [11, 9], [12, 3], [12, 4], [13, 8], [13, 9]],
            'Zurich': [[15, 12], [15, 13], [16, 5], [16, 6], [17, 12], [17, 13]],
            'Vienna': [[15, 16], [15, 17], [16, 7], [16, 8], [17, 16], [17, 17]],
            'Budapest': [[15, 20], [15, 21], [16, 9], [16, 10], [17, 20], [17, 21]]
        }
        self.greenCities = {
            'Riga': [[1, 23], [1, 24], [2, 11], [2, 12], [3, 23], [3, 24]],
            'Vilnius': [[5, 23], [5, 24], [6, 11], [6, 12], [7, 23], [7, 24]],
            'Minsk': [[7, 26], [7, 27], [8, 12], [8, 13], [9, 26], [9, 27]],
            'Kiev': [[11, 28], [11, 29], [12, 13], [12, 14], [13, 28], [13, 29]],
            'Kharkiv': [[13, 31], [13, 32], [14, 15], [15, 31], [15, 32]],
            'Odessa': [[17, 29], [17, 30], [18, 14], [18, 15], [19, 29], [19, 30]],
            'Bucharest': [[19, 26], [19, 27], [20, 12], [20, 13], [21, 26], [21, 27]]
        }
        self.blueCities = {
            'Marseille': [[19, 8], [19, 9], [20, 3], [20, 4], [21, 8], [21, 9]],
            'Florence': [[19, 12], [19, 13], [20, 5], [20, 6], [21, 12], [21, 13]],
            'Sofia': [[21, 23], [21, 24], [22, 11], [22, 12], [23, 23], [23, 24]],
            'Rome': [[23, 14], [23, 15], [24, 6], [24, 7], [25, 14], [25, 15]],
            'Tirana': [[23, 18], [23, 19], [24, 8], [24, 9], [25, 18], [25, 19]],
            'Istanbul': [[23, 26], [23, 27], [24, 12], [24, 13], [25, 26], [25, 27]],
            'Thessaloniki': [[25, 23], [25, 24], [26, 11], [26, 12]]
        }

    def init_player_cities(self):
        yellow = random.choice(list(self.yellowCities.keys()))
        red = random.choice(list(self.redCities.keys()))
        orange = random.choice(list(self.orangeCities.keys()))
        green = random.choice(list(self.greenCities.keys()))
        blue = random.choice(list(self.blueCities.keys()))
        yellowCoords = self.yellowCities.pop(yellow)
        redCoords = self.redCities.pop(red)
        orangeCoords = self.orangeCities.pop(orange)
        greenCoords = self.greenCities.pop(green)
        blueCoords = self.blueCities.pop(blue)
        return [[yellow, yellowCoords], [red, redCoords], [orange, orangeCoords], [green, greenCoords],
                [blue, blueCoords]]

    def return_board(self):
        return self.board

    def return_board_nodes(self):
        temp = 0
        for i in self.board:
            for _ in i:
                if _ != '*':
                    temp += 1
                else:
                    pass
        return temp