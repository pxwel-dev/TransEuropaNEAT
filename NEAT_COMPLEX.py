import Nodes
from Nodes import Colour
from Player import Player
from GameBoard import GameBoard
import networkx
import copy
import random


class NEATPlayer(Player):
    def __init__(self, name, neuralNet):
        Player.__init__(self, name)
        self.citiesToCapture = []
        self.neuralNetwork = neuralNet
        self.allCities = None
        self.tracksUsed = 0
        self.movesSkipped = 0
        self.noMovesLeftErrors = 0

    def set_cities(self, cities):
        self._cities = cities
        self.citiesToCapture = copy.copy(cities)

    def find_all_possible_moves(self, game_board: GameBoard):
        board = game_board.get_map()
        valid_moves = []
        if len(self.citiesToCapture) == 5:
            for city in self.citiesToCapture:
                for neighbour in board.neighbors(city):
                    if [neighbour, city] not in valid_moves:
                        valid_moves.append([neighbour, city])
        else:
            for node in self.get_networkAllTracks().nodes:
                for neighbour in board.neighbors(node):
                    if [neighbour, node] not in valid_moves and \
                            neighbour not in self.get_networkAllTracks().nodes:
                        valid_moves.append([neighbour, node])
        random.shuffle(valid_moves)
        return valid_moves

    def create_network_inputs(self, moves, game_board: GameBoard):
        reformatted = []

        for move in moves:
            formatted = []

            minCityDistances = [-1, -1, -1, -1, -1]

            edgeCost = int(game_board.get_map().get_edge_data(move[0], move[1]).get('weight'))

            for i in self.citiesToCapture:
                neighbourToCity = networkx.dijkstra_path_length(game_board.get_map(), move[0], i, weight='weight')
                if i.get_colour() == Colour.red:
                    minCityDistances[0] = neighbourToCity + edgeCost
                if i.get_colour() == Colour.yellow:
                    minCityDistances[1] = neighbourToCity + edgeCost
                if i.get_colour() == Colour.orange:
                    minCityDistances[2] = neighbourToCity + edgeCost
                if i.get_colour() == Colour.green:
                    minCityDistances[3] = neighbourToCity + edgeCost
                if i.get_colour() == Colour.blue:
                    minCityDistances[4] = neighbourToCity + edgeCost

            opponentNetworkDistances = []

            for player in game_board.get_players():
                if player != self:
                    try:
                        network = networkx.multi_source_dijkstra_path_length(
                            game_board.get_map(), player.get_networkNoColTracks().nodes, weight='weight')
                        if networkx.utils.graphs_equal(player.get_networkNoColTracks(), self.get_networkNoColTracks()):
                            opponentNetworkDistances.append(-1)
                        else:
                            opponentNetworkDistances.append(network[move[0]] + edgeCost)
                    except ValueError:
                        opponentNetworkDistances.append(-1)

            for i in opponentNetworkDistances:
                if i == -1:
                    opponentNetworkDistances.remove(i)

            opponentNum = len(game_board.get_players()) - 1
            opponentCityColoursLeft = [opponentNum] * 5

            for player in game_board.get_players():
                if player != self:
                    if len(player.capturedCityCols) != 0:
                        for col in player.capturedCityCols:
                            if col == Colour.red:
                                opponentCityColoursLeft[0] -= 1
                            if col == Colour.yellow:
                                opponentCityColoursLeft[1] -= 1
                            if col == Colour.orange:
                                opponentCityColoursLeft[2] -= 1
                            if col == Colour.green:
                                opponentCityColoursLeft[3] -= 1
                            if col == Colour.blue:
                                opponentCityColoursLeft[4] -= 1

            for i in minCityDistances:
                formatted.append(i)

            if len(opponentNetworkDistances) != 0:
                formatted.append(min(opponentNetworkDistances))
            else:
                formatted.append(-1)

            # citiesNotInPlayerNets = copy.deepcopy(self.allCities)
            # for city in game_board.get_cities().values():
            #     city_in_network = 0
            #     for player in game_board.get_players():
            #         if city in player.get_networkAllTracks().nodes:
            #             city_in_network += 1
            #     if city_in_network > 0:
            #         if city.get_colour() == Colour.red:
            #             citiesNotInPlayerNets[0] -= 1
            #         elif city.get_colour() == Colour.yellow:
            #             citiesNotInPlayerNets[1] -= 1
            #         elif city.get_colour() == Colour.orange:
            #             citiesNotInPlayerNets[2] -= 1
            #         elif city.get_colour() == Colour.green:
            #             citiesNotInPlayerNets[3] -= 1
            #         elif city.get_colour() == Colour.blue:
            #             citiesNotInPlayerNets[4] -= 1

                if isinstance(move[0], Nodes.City):
                    if move[0].get_colour() == Colour.red:
                        formatted.append(1)
                        if move[0] not in self.citiesToCapture:
                            formatted.append(self.evalNonTargetCityCapture(opponentCityColoursLeft,
                                                                           opponentNum, Colour.red,
                                                                           0, game_board, move[0]))
                        elif move[0] in self.citiesToCapture:
                            formatted.append(1)
                    elif move[0].get_colour() == Colour.yellow:
                        formatted.append(2)
                        if move[0] not in self.citiesToCapture:
                            formatted.append(self.evalNonTargetCityCapture(opponentCityColoursLeft,
                                                                           opponentNum, Colour.red,
                                                                           1, game_board, move[0]))
                        elif move[0] in self.citiesToCapture:
                            formatted.append(1)
                    elif move[0].get_colour() == Colour.orange:
                        formatted.append(3)
                        if move[0] not in self.citiesToCapture:
                            formatted.append(self.evalNonTargetCityCapture(opponentCityColoursLeft,
                                                                           opponentNum, Colour.red,
                                                                           2, game_board, move[0]))
                        elif move[0] in self.citiesToCapture:
                            formatted.append(1)
                    elif move[0].get_colour() == Colour.green:
                        formatted.append(4)
                        if move[0] not in self.citiesToCapture:
                            formatted.append(self.evalNonTargetCityCapture(opponentCityColoursLeft,
                                                                           opponentNum, Colour.red,
                                                                           3, game_board, move[0]))
                        if move[0] in self.citiesToCapture:
                            formatted.append(1)
                    elif move[0].get_colour() == Colour.blue:
                        formatted.append(5)
                        if move[0] not in self.citiesToCapture:
                            formatted.append(self.evalNonTargetCityCapture(opponentCityColoursLeft,
                                                                           opponentNum, Colour.red,
                                                                           4, game_board, move[0]))
                        if move[0] in self.citiesToCapture:
                            formatted.append(1)
                else:
                    formatted.append(0)
                    formatted.append(1)

                formatted.append(edgeCost)
                formatted.append(self.colouredTracks)
                formatted.append(move)
                reformatted.append(formatted)

            totalDistances = []
            totalSingleTrackDists = []
            singleTrackMoves = []
            for formattedMove in reformatted:
                temp = []
                for i in [formattedMove[0], formattedMove[1], formattedMove[2],
                          formattedMove[3], formattedMove[4]]:
                    if i != -1:
                        temp.append(i)

                totalDistances.append(min(temp))
                if formattedMove[8] == 1:
                    for i in [formattedMove[0], formattedMove[1], formattedMove[2],
                              formattedMove[3], formattedMove[4]]:
                        if i != -1:
                            temp.append(i)
                    totalSingleTrackDists.append(min(temp))
                    singleTrackMoves.append(formattedMove)
            bestMoves = []
            if self.tracksToPlace == 1:
                for i in range(0, 10):
                    if len(totalSingleTrackDists) != 0:
                        bestMoves.append(singleTrackMoves[totalSingleTrackDists.index(min(totalSingleTrackDists))])
                        totalSingleTrackDists.pop(totalSingleTrackDists.index(min(totalSingleTrackDists)))
            else:
                for i in range(0, 10):
                    if len(totalDistances) != 0:
                        bestMoves.append(reformatted[totalDistances.index(min(totalDistances))])
                        totalDistances.pop(totalDistances.index(min(totalDistances)))
            return bestMoves

    def make_move(self, game_board: GameBoard) -> [str]:
        if not self.has_won():
            inputs = self.create_network_inputs(self.find_all_possible_moves(game_board), game_board)
            inputIndex = []
            moveValues = []
            moveTypes = []
            for i in range(0, len(inputs)):
                output = self.neuralNetwork.activate([inputs[i][0], inputs[i][1], inputs[i][2], inputs[i][3],
                                                      inputs[i][4], inputs[i][5], inputs[i][6], inputs[i][7],
                                                      inputs[i][8], inputs[i][9]])
                for j in range(0, 3):
                    inputIndex.append(i)
                    moveValues.append(output[j])
                    moveTypes.append(j)
            while True:
                if len(moveValues) > 0:
                    currentBestMoveIndex = moveValues.index(max(moveValues))
                    bestMove = inputs[inputIndex[currentBestMoveIndex]][10]
                    bestMoveCost = abs(inputs[inputIndex[currentBestMoveIndex]][8])
                    bestMoveType = moveTypes[currentBestMoveIndex]
                else:
                    # print("NO MOVES LEFT - SKIP or NO COLOURED")
                    self.noMovesLeftErrors += 1
                    self.fitness -= 1
                    return -1
                if self.tracksToPlace != -1:
                    if bestMoveType == 0 or (bestMoveType == 1 and self.colouredTracks != 0):
                        if bestMoveCost == 1 and self.tracksToPlace - 1 >= 0:
                            self.tracksToPlace -= 1
                            self.tracksUsed += 1
                            print("{0} Move: {1} -> {2}, Coloured track: {3}"
                                  .format(self.name,
                                          str(bestMove[1].get_id()),
                                          str(bestMove[0].get_id()),
                                          bool(bestMoveType)))
                            break
                        elif bestMoveCost == 2 and self.tracksToPlace - 2 == 0 and not self.skippedTurn:
                            self.tracksToPlace -= 2
                            self.tracksUsed += 2
                            print("{0} Move: {1} -> {2}, Coloured track: {3}"
                                  .format(self.name,
                                          str(bestMove[1].get_id()),
                                          str(bestMove[0].get_id()),
                                          bool(bestMoveType)))
                            break
                        else:
                            if len(moveValues) > 1:
                                moveValues.pop(currentBestMoveIndex)
                                moveTypes.pop(currentBestMoveIndex)
                                inputIndex.pop(currentBestMoveIndex)
                            else:
                                # print("NO MOVES LEFT - TURNS")
                                self.noMovesLeftErrors += 1
                                self.fitness -= 1
                                return -1
                    elif bestMoveType == 2 and not self.skippedTurn and self.tracksToPlace != 2:
                        self.skippedTurn = True
                        self.movesSkipped += 1
                        return None
                    else:
                        if len(moveValues) > 1:
                            moveValues.pop(currentBestMoveIndex)
                            moveTypes.pop(currentBestMoveIndex)
                            inputIndex.pop(currentBestMoveIndex)
                        else:
                            # print("NO MOVES LEFT - SKIP or NO COLOURED")
                            self.noMovesLeftErrors += 1
                            self.fitness -= 1
                            return -1
                else:
                    print("{0} Chosen Starting City: {1}"
                          .format(self.name, str(bestMove[1].get_name())))
                    break

            if self.has_won():
                return 'w'
            else:
                self.colouredTracks -= bestMoveType
                return [[bestMove[0].get_id(), bestMove[1].get_id()], bool(bestMoveType)]
        else:
            return 'w'

    def evalNonTargetCityCapture(self, opponentCityColoursLeft: list, opponentNum: int, colour: Colour,
                                 colour_index: int, game_board: GameBoard, city: Nodes.City):

        inOppNetworksCount = self.check_city_in_opponent_networks(game_board, city)
        mergedOppsUncapCol = sum(1 for player in self.check_opponents_in_network(game_board) if
                                      colour not in player.capturedCityCols)

        # Avoid division by zero
        if opponentNum - inOppNetworksCount == 0:
            return 1

        # Calculate risk
        risk_from_merged_opponents = \
            (mergedOppsUncapCol / opponentCityColoursLeft[colour_index]) if (
                    opponentCityColoursLeft[colour_index] > 0) else 0
        risk_from_opponents = \
            (opponentCityColoursLeft[colour_index] / (opponentNum - inOppNetworksCount))

        # Combine risks and normalize
        combined_risk = (1 - risk_from_merged_opponents) * (1 - risk_from_opponents)
        normalized_risk = max(0, combined_risk)  # Ensure risk is non-negative

        return normalized_risk

    def check_city_in_opponent_networks(self, game_board: GameBoard, city: Nodes.City):
        total = 0
        for player in game_board.get_players():
            if player != self:
                if city in player.get_networkAllTracks().nodes:
                    total += 1
        return total

    def check_opponents_in_network(self, game_board: GameBoard):
        players = []
        for player in game_board.get_players():
            if player != self:
                if networkx.utils.graphs_equal(player.get_networkNoColTracks(), self.get_networkNoColTracks()):
                    players.append(player)
        return players

    def choose_start_pos(self, game_board: GameBoard) -> str:
        self.allCities = game_board.get_cities_grouped()
        self.tracksToPlace = -1
        city_id = self.make_move(game_board)[0][1]
        self.add_start_node(game_board.get_nodes().get(city_id))
        self.tracksToPlace = 2
        return city_id

    def has_won(self):
        for city in self.citiesToCapture:
            if city in self.get_networkAllTracks().nodes:
                print("{0} has captured: {1}"
                      .format(self.name, str(city.get_name())))
                self.capturedCityCols.append(city.get_colour())
                self.citiesToCapture.remove(city)
                self.fitness += 0.2
        return Player.has_won(self)