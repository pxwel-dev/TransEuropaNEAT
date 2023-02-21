class Player:

    def __init__(self, board, neuralNet, genome):
        self.score = 0
        self.citiesToCapture = []
        self.tracksPlaced = []
        self.currentBoard = board.return_board()

        self.boardRowLengths = board.boardRowLengths
        self.allEdgeNeighbours = board.boardEdgeNeighbours
        self.genome = genome
        self.neuralNetwork = neuralNet

    def set_map_targets(self):
        for i in self.citiesToCapture:
            for j in i[1]:
                if self.currentBoard[j[0]][j[1]] == -1:
                    self.currentBoard[j[0]][j[1]] = 1
                elif self.currentBoard[j[0]][j[1]] == -2:
                    self.currentBoard[j[0]][j[1]] = 2
                else:
                    pass

    def remove_map_target(self, city):
        for i in city[1]:
            if self.currentBoard[i[0]][i[1]] == 1:
                self.currentBoard[i[0]][i[1]] = -1
            elif self.currentBoard[i[0]][i[1]] == 2:
                self.currentBoard[i[0]][i[1]] = -2
            else:
                pass

    def update_player_board_view(self, board):
        temp = board.return_board()
        for i in range(0, len(self.currentBoard)):
            for j in range(0, len(self.currentBoard[i])):
                if temp[i][j] == 0:
                    self.currentBoard[i][j] = 0
                else:
                    pass

    def make_move(self):
        reformatted = []
        for i in range(0, len(self.currentBoard)):
            for j in range(0, len(self.currentBoard[i])):
                if self.currentBoard[i][j] != '*':
                    reformatted.append(self.currentBoard[i][j])
                else:
                    pass
        output = self.neuralNetwork.activate(reformatted)
        decision = output.index(max(output))
        choice = self.find_move_choice(decision)
        validation = self.move_validation(choice)
        #print([choice, validation])
        return [choice, validation]

    def find_move_choice(self, decision):
        index = decision
        row_num = 0
        for rowLength in self.boardRowLengths:
            if index - rowLength < 0:
                break
            else:
                index -= rowLength
            row_num += 1
        return [row_num, index]

    def move_validation(self, choice):
        trackVal = self.track_placement_validation(choice)
        cityCapVal = self.city_capture_validation(choice, trackVal)
        if 1 >= len(self.tracksPlaced) >= 0:
            if cityCapVal:
                return True
            else:
                return False
        elif len(self.tracksPlaced) > 1:
            if (cityCapVal and trackVal) or trackVal:
                return True
            else:
                return False

    def city_capture_validation(self, choice, trackVal):
        for i in self.citiesToCapture:
            for j in i[1]:
                if (j == choice and trackVal) or (j == choice and len(self.tracksPlaced) == 0):
                    self.remove_map_target(i)
                    self.tracksPlaced.append(choice)
                    print("City captured")
                    return True
                else:
                    pass
        return False

    def track_placement_validation(self, choice):
        track = self.find_track_details(choice)
        if track is not None:
            if track[0] != '0':
                for i in track[1]:
                    if i in self.tracksPlaced:
                        self.tracksPlaced.append(choice)
                        return True
            else:
                return False
        else:
            return False

    def find_track_details(self, choice):
        for i in range(0, len(self.allEdgeNeighbours)):
            if self.allEdgeNeighbours[i][1] == choice:
                return [self.allEdgeNeighbours[i][0], self.allEdgeNeighbours[i][2]]
            else:
                pass
        return None

    def closest_target_distance(self, move, targets):
        distances = []
        for i in targets:
            distances.append(abs(i[0] - move[0]) + abs(i[1] - move[1]))
        print(move, targets[distances.index(min(distances))], min(distances))
        return min(distances)




# playerBoard = Board()
# p = Player(playerBoard, "", "")
# p.set_cities(playerBoard)
# print(p.citiesToCapture)
# p.set_map_targets()
# print(playerBoard.return_board_nodes())
# print(p.currentBoard)
