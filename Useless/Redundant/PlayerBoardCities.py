import copy
import random

PRECISE_SEARCH_THRESHOLD = 2


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
        for move in allMoves:
            min_city_distances = []

            for i in self.citiesToCapture:
                distances = []
                for j in i[1]:
                    distances.append(self.find_estimated_distance(move, j))
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
                track_distances.append(self.find_estimated_distance(move, i))

            if len(track_distances) == 0:
                track_distances.append(1000)

            single_edges = 0
            double_edges = 0
            neighbours = copy.deepcopy(self.find_track_details(move)[1])
            for i in neighbours:
                if abs(self.currentBoard[i[0]][i[1]]) == 1:
                    single_edges += 1
                elif abs(self.currentBoard[i[0]][i[1]]) == 2:
                    double_edges += 1

            formatted = []
            for i in min_city_distances:
                formatted.append(i)
            formatted.append(min(track_distances))
            formatted.append(self.currentBoard[move[0]][move[1]])
            formatted.append(single_edges)
            formatted.append(double_edges)
            formatted.append(move)
            reformatted.append(formatted)
        return reformatted

    def make_move(self, moves):
        outputs = []
        random.shuffle(moves)
        for move in moves:
            outputs.append(
                self.neuralNetwork.activate([move[0], move[1], move[2], move[3],
                                             move[4], move[5], move[6], move[7], move[8]])[0])
        while True:
            choice = moves[outputs.index(max(outputs))][9]
            cost = abs(moves[outputs.index(max(outputs))][6])
            if cost == 1 and self.tracksToPlace - 1 >= 0:
                self.tracksToPlace -= 1
                self.currentBoard[choice[0]][choice[1]] = 0
                self.tracksPlaced.append(choice)
                print(self.name + ":" + str(choice))
                break
            elif cost == 2 and self.tracksToPlace - 2 == 0:
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
                    print("Player {0} City captured: {1} | Edge: {2}\n==========".format(self.name, str(i[0]), str(j)))
                    return True
        return False

    def find_track_details(self, choice):
        for i in range(0, len(self.allEdgeNeighbours)):
            if self.allEdgeNeighbours[i][1] == choice:
                return [self.allEdgeNeighbours[i][0], self.allEdgeNeighbours[i][2]]
        return None

    def find_estimated_distance(self, start, end):
        '''
        Returns the estimated distance between two edges

            :param start: [row, column] of start edge
            :param end: [row, column] of end edge

            :returns: minimum estimated distance between edges

        '''
        if start[0] % 2 == 0 and end[0] % 2 == 0:
            return abs(end[0] - start[0]) + abs(end[1] - start[1])

        elif start[0] % 2 != 0 and end[0] % 2 != 0:
            targetRowEndNeighbours = []
            targetRow = end[0] - 1
            for i in self.find_track_details(end)[1]:
                if i[0] == targetRow:
                    targetRowEndNeighbours.append(i[1])
            verticalDistance = abs((targetRow - start[0]))
            horizontalStart = abs(-(-start[1] // 2))

            distances = []
            for target in targetRowEndNeighbours:
                distances.append(verticalDistance + abs(target - horizontalStart) + 1)
            return min(distances)

        else:
            if start[0] % 2 == 0 and end[0] % 2 != 0:
                targetRow = end[0] - 1
                rowDistance = abs(targetRow - start[0])
                rowAdd = abs(-(-rowDistance // 2))
                targetRowEndNeighbours = []

                for i in self.find_track_details(end)[1]:
                    if i[0] == targetRow:
                        targetRowEndNeighbours.append(i[1])

                distances = []

                for target in targetRowEndNeighbours:
                    rowLeft = start[1] - rowAdd
                    rowRight = start[1] + rowAdd
                    if rowLeft < 0:
                        if target - rowRight < target - targetRow[start[0]]:
                            distances.append(rowAdd + (target - rowRight) + 1)
                        elif target - rowRight > target - targetRow[start[0]]:
                            distances.append(rowAdd + (target - targetRow[start[0]]) + 1)
                    elif rowRight < 0:
                        if target - rowLeft < target - targetRow[start[0]]:
                            distances.append(rowAdd + (targetRow - rowLeft) + 1)
                        elif target - rowLeft > target - targetRow[start[0]]:
                            distances.append(rowAdd + (target - targetRow[start[0]]) + 1)
                    else:
                        if target - rowLeft <= target- rowRight and target - rowLeft <= target - targetRow[start[0]]:
                            distances.append(rowAdd + (target - rowLeft) + 1)
                        elif target - rowRight <= target - rowLeft and target - rowRight <= target - targetRow[start[0]]:
                            distances.append(rowAdd + (target - rowRight) + 1)
                        else:
                            distances.append(rowAdd + (target - targetRow[start[0]]) + 1)

            if start[0] % 2 != 0 and end[0] % 2 == 0:
                targetRow = end[0] - 1
                rowDistance = abs(targetRow - start[0])
                rowAdd = abs(-(-rowDistance // 2))
                targetRowEndNeighbours = []

                for i in self.find_track_details(end)[1]:
                    if i[0] == targetRow:
                        targetRowEndNeighbours.append(i[1])

                distances = []




    # def find_shortest_path(self, start, end, dist, excluded, depth_limit):
    #     '''
    #     Recursively searches up to the depth limit and returns the precise distance between two edges.
    #
    #         :param start: [row, column] of start edge
    #         :param end: [row, column] of end edge
    #         :param dist: cumulative distance, should be initialised to zero when running this function
    #         :param excluded: list of edges that have already been searched and should be ignored
    #         :param current_depth: current depth of the search
    #         :param depth_limit: ends further searches upon being reached
    #
    #         :returns: minimum precise distance between edges
    #
    #     '''
    #     # If start-end distance is greater than adjusted depth_limit, return estimated distance and propagate
    #     distance = self.find_estimated_distance(start, end)
    #     if distance > depth_limit:
    #         return 1000
    #     else:
    #         # Remove any excluded edges from current search queue
    #         track_details = copy.deepcopy(self.find_track_details(start))
    #         if len(excluded) != 0:
    #             for i in excluded:
    #                 if i in track_details[1]:
    #                     track_details[1].remove(i)
    #         # If end is found, return precise distance
    #         if end in track_details[1]:
    #             return dist + abs(track_details[0]) + abs(self.find_track_details(end)[0])
    #         else:
    #             # If all neighbours have been excluded or search depth has been reached, return 1000 and propagate
    #             if len(track_details[1]) == 0:
    #                 return 1000
    #             else:
    #                 # Recursively calls the function for each neighbouring edge and increments depth
    #                 distances = []
    #                 for i in track_details[1]:
    #                     temp = copy.deepcopy(excluded)
    #                     temp.append(start)
    #                     temp.append(i)
    #                     distances.append(
    #                         self.find_shortest_path(i, end, dist + abs(track_details[0]), temp,
    #                                                 distance))
    #                 return min(distances)

    # def astar_pathfinding(self, start, end):
    #     openList = [start]
    #     openListFScore = [0]
    #     openListGScore = [0]
    #     closedList = []
    #     dist = 0
    #
    #     print("Attempting {0} to {1}...".format(start, end))
    #     while len(openList) > 0:
    #         minFScore = openListFScore.index(min(openListFScore))
    #         openListFScore.pop(minFScore)
    #         openListGScore.pop(minFScore)
    #         currentEdge = openList.pop(minFScore)
    #         closedList.append(currentEdge)
    #
    #         if currentEdge == end:
    #             print(start, end, closedList)
    #             return closedList
    #         else:
    #             edgeInfo = self.find_track_details(currentEdge)
    #             dist += abs(edgeInfo[0])
    #             for edge in edgeInfo[1]:
    #                 if edge in closedList:
    #                     continue
    #
    #                 g = self.find_estimated_distance(start, end) * 2
    #                 h = self.find_estimated_distance(edge, end) * 2
    #                 f = g + h
    #
    #                 if edge in openList and g > openListGScore[openList.index(edge)]:
    #                     continue
    #
    #                 openList.append(edge)
    #                 openListFScore.append(f)
    #                 openListGScore.append(g)

