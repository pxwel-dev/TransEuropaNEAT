import copy


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
        # print(len(self.tracksPlaced))
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
        trackCosts = []

        for move in allMoves:
            formatted = []
            temp = copy.deepcopy(self.currentBoard)
            trackCosts.append(self.currentBoard[move[0]][move[1]])
            temp[move[0]][move[1]] = 8
            choice_coords.append(move)
            for i in range(0, len(temp)):
                for j in range(0, len(temp[i])):
                    if temp[i][j] != '*':
                        formatted.append(temp[i][j])
            reformatted.append(formatted)
        return [reformatted, choice_coords, trackCosts]

    def make_move(self, moves):
        try:
            outputs = []
            for move in moves[0]:
                outputs.append(self.neuralNetwork.activate(move))
            while True:
                choice = moves[1][outputs.index(max(outputs))]
                cost = moves[2][outputs.index(max(outputs))]
                # print(moves[2][outputs.index(max(outputs))])
                # if len(self.citiesToCapture) == 5:
                #     self.tracksToPlace -= 2
                #     self.currentBoard[choice[0]][choice[1]] = 0
                #     self.tracksPlaced.append(choice)
                #     print(self.name + ":" + str(choice))
                #     break
                # else:
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
                    outputs.pop(outputs.index(max(outputs)))
                    moves[1].pop(moves[1].index(moves[1][outputs.index(max(outputs))]))
                    moves[2].pop(moves[2].index(moves[2][outputs.index(max(outputs))]))

            return [choice, self.city_capture_validation(), cost]
        except ValueError:
            print("Player {0} has an empty list".format(self.name))
            return ValueError

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
                    print("City captured: {0} | Move: {1}\n==========".format(str(i[0]), str(j)))
                    return True
        print("==========")
        return False

    def find_track_details(self, choice):
        for i in range(0, len(self.allEdgeNeighbours)):
            if self.allEdgeNeighbours[i][1] == choice:
                return [self.allEdgeNeighbours[i][0], self.allEdgeNeighbours[i][2]]
        return None

    # def find_shortest_path(self, start, end, dist):
    #     distances = []
    #     x = self.find_track_details(start)
    #     if end in x:
    #         return dist
    #     else:
    #         for i in x[1]:
    #             distances.append(self.find_shortest_path(i, end, dist+x[0]))
    #     return min(distances)
# playerBoard = Board()
# p = Player(playerBoard, "", "")
# p.set_cities(playerBoard)
# print(p.citiesToCapture)
# p.set_map_targets()
# print(playerBoard.return_board_nodes())
# print(p.currentBoard)
