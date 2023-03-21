import copy
import random


class Player:
    def __init__(self, board, neuralNet, genome, name):
        self.score = 0
        self.won = False
        self.tracksToPlace = 2
        self.citiesToCapture = []
        self.tracksPlaced = []
        self.currentBoard = board.return_board()

        self.boardRowLengths = board.boardRowLengths
        self.allEdgeNeighbours = board.boardEdgeNeighbours
        self.genome = genome
        self.neuralNetwork = neuralNet
        self.name = name

    def set_map_targets(self):
        cities = []
        for i in self.citiesToCapture:
            for j in i[1]:
                cities.append(j)
                if self.currentBoard[j[0]][j[1]] == -1:
                    self.currentBoard[j[0]][j[1]] = 1
                elif self.currentBoard[j[0]][j[1]] == -2:
                    self.currentBoard[j[0]][j[1]] = 2
        for i in range(0, len(self.currentBoard)):
            for j in range(0, len(self.currentBoard[i])):
                if [i, j] not in cities and self.currentBoard[i][j] != '*' and self.currentBoard[i][j] > 0:
                    if self.currentBoard[i][j] == 1:
                        self.currentBoard[i][j] = -1
                    elif self.currentBoard[i][j] == 2:
                        self.currentBoard[i][j] = -2

    def remove_map_target(self, city):
        for i in city[1]:
            if self.currentBoard[i[0]][i[1]] == 1:
                self.currentBoard[i[0]][i[1]] = -1
            elif self.currentBoard[i[0]][i[1]] == 2:
                self.currentBoard[i[0]][i[1]] = -2

    def update_player_board_view(self, board):
        self.currentBoard = board
        self.set_map_targets()

    # ==================================================================================================================== #
    def find_all_possible_moves(self):
        temp = []
        if len(self.tracksPlaced) == 0:
            for i in self.citiesToCapture:
                for j in i[1]:
                    temp.append(j)
        elif len(self.tracksPlaced) > 0:
            for i in self.tracksPlaced:
                for j in self.allEdgeNeighbours:
                    if i == j[1]:
                        for k in j[2]:
                            temp.append(k)
        deduplicated = []
        for i in temp:
            if i not in deduplicated and self.currentBoard[i[0]][i[1]] != 0:
                deduplicated.append(i)
        return deduplicated

    def create_network_inputs(self, allMoves):
        reformatted = []
        choice_coords = []
        if len(self.tracksPlaced) == 0:
            for move in allMoves:
                reformatted.append([0, 0, 0, 0, 0, 1000, self.currentBoard[move[0]][move[1]], move])
                choice_coords.append(move)

        else:
            for move in allMoves:
                min_city_distances = []

                for i in self.citiesToCapture:
                    distances = []
                    for j in i[1]:
                        distances.append(self.find_shortest_path(move, j))
                    min_city_distances.append(min(distances))
                while len(min_city_distances) != 5:
                    min_city_distances.append(1000)

                temp = []
                track_distances = []
                for i in range(0, len(self.currentBoard)):
                    for j in range(0, len(self.currentBoard[i])):
                        if [i, j] not in self.tracksPlaced and self.currentBoard[i][j] == 0:
                            temp.append([i, j])

                for i in temp:
                    track_distances.append(self.find_shortest_path(move, i))

                if len(track_distances) == 0:
                    track_distances.append(1000)

                formatted = []
                for i in min_city_distances:
                    formatted.append(i)
                formatted.append(min(track_distances))
                formatted.append(self.currentBoard[move[0]][move[1]])
                formatted.append(move)
                reformatted.append(formatted)
        return reformatted

    def make_move(self, moves):
        outputs = []
        random.shuffle(moves)
        for move in moves:
            outputs.append(abs(self.neuralNetwork.activate([move[0], move[1], move[2], move[3], move[4], move[5], move[6]])[0]))
        while True:
            choice = moves[outputs.index(max(outputs))][7]
            cost = moves[outputs.index(max(outputs))][6]
            if (cost == -1 or cost == 1) and self.tracksToPlace - 1 >= 0:
                self.tracksToPlace -= 1
                self.currentBoard[choice[0]][choice[1]] = 0
                self.tracksPlaced.append(choice)
                print(self.name + ":" + str(choice))
                break
            elif (cost == -2 or cost == 2) and self.tracksToPlace - 2 == 0:
                self.tracksToPlace -= 2
                self.currentBoard[choice[0]][choice[1]] = 0
                self.tracksPlaced.append(choice)
                print(self.name + ":" + str(choice))
                break
            else:
                if len(outputs) > 1:
                    moves.pop(moves.index(moves[outputs.index(max(outputs))]))
                    outputs.pop(outputs.index(max(outputs)))
                else:
                    self.tracksToPlace -= 1
                    return None
        return [choice, cost]

    # ==================================================================================================================== #
    def check_network_merge(self):
        for i in self.tracksPlaced:
            neighbours = self.find_track_details(i)[1]
            for j in neighbours:
                if self.currentBoard[j[0]][j[1]] == 0 and j not in self.tracksPlaced:
                    return j
        return False

    def merge_networks(self, opponent_network):
        for i in opponent_network:
            if i not in self.tracksPlaced:
                self.tracksPlaced.append(i)

    # ==================================================================================================================== #

    def city_capture_validation(self):
        for i in self.citiesToCapture:
            for j in i[1]:
                if j in self.tracksPlaced:
                    self.remove_map_target(i)
                    self.citiesToCapture.remove(i)
                    self.currentBoard[j[0]][j[1]] = 0
                    self.score += 1
                    if self.score == 5:
                        self.won = True
                    print("City captured: {0} | Edge: {1}\n==========".format(str(i[0]), str(j)))
                    return True
        print("==========")
        return False

    def find_track_details(self, choice):
        for i in range(0, len(self.allEdgeNeighbours)):
            if self.allEdgeNeighbours[i][1] == choice:
                return [self.allEdgeNeighbours[i][0], self.allEdgeNeighbours[i][2]]
        return None

    def find_shortest_path(self, start, end):
        if (start[0] % 2 == 0 and end[0] % 2 == 0) or (start[0] % 2 != 0 and end[0] % 2 != 0):
            return abs(end[0] - start[0]) + abs(end[1] - start[1])
        else:
            distances = []
            neighbours = self.find_track_details(start)[1]
            for i in neighbours:
                if i[0] > start[0] or i[0] < start[0]:
                    distances.append(abs(end[0] - i[0]) + abs(end[1] - i[1]))
            return min(distances)
