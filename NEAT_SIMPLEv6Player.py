import Nodes
from Nodes import Colour
from Player import Player
from GameBoard import GameBoard
import networkx
import copy
import random


class NEATPlayer(Player):
    def __init__(self, name, neuralNet, genome):
        Player.__init__(self, name)
        self.citiesToCapture = []
        self.neuralNetwork = neuralNet
        self.genome = genome
        self.allCities = None

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
            for node in self.get_network().nodes:
                for neighbour in board.neighbors(node):
                    if [neighbour, node] not in valid_moves and \
                            neighbour not in self.get_network().nodes:
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
                            game_board.get_map(), player.get_network().nodes, weight='weight')
                        if networkx.utils.graphs_equal(player.get_network(), self.get_network()):
                            opponentNetworkDistances.append(-1)
                        else:
                            opponentNetworkDistances.append(network[move[0]] + edgeCost)
                    except ValueError:
                        opponentNetworkDistances.append(-1)

            for i in opponentNetworkDistances:
                if i == -1:
                    opponentNetworkDistances.remove(i)

            opponentNum = len(game_board.get_players()) - 1
            opponentCityColoursLeft = [opponentNum, opponentNum, opponentNum, opponentNum, opponentNum]

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

            temp = copy.deepcopy(self.allCities)
            for city in game_board.get_cities().values():
                city_in_network = 0
                for player in game_board.get_players():
                    if city in player.get_network().nodes:
                        city_in_network += 1
                if city_in_network > 0:
                    if city.get_colour() == Colour.red:
                        temp[0] -= 1
                    elif city.get_colour() == Colour.yellow:
                        temp[1] -= 1
                    elif city.get_colour() == Colour.orange:
                        temp[2] -= 1
                    elif city.get_colour() == Colour.green:
                        temp[3] -= 1
                    elif city.get_colour() == Colour.blue:
                        temp[4] -= 1

            if isinstance(move[0], Nodes.City) and move[0] not in self.citiesToCapture:
                if move[0].get_colour() == Colour.red:
                    formatted.append(1)
                    if temp[0] != 0:
                        formatted.append(1 - (opponentCityColoursLeft[0] / temp[0]))
                    else:
                        notCaptured = 0
                        for player in self.check_players_in_network(game_board):
                            if Colour.red not in player.capturedCityCols:
                                notCaptured += 1
                        if notCaptured != 0:
                            formatted.append(1 - (notCaptured / opponentCityColoursLeft[0]))
                        else:
                            formatted.append(1 - (opponentCityColoursLeft[0] / opponentNum))
                elif move[0].get_colour() == Colour.yellow:
                    formatted.append(2)
                    if temp[1] != 0:
                        formatted.append(1 - (opponentCityColoursLeft[1] / temp[1]))
                    else:
                        notCaptured = 0
                        for player in self.check_players_in_network(game_board):
                            if Colour.yellow not in player.capturedCityCols:
                                notCaptured += 1
                        if notCaptured != 0:
                            formatted.append(1 - (notCaptured / opponentCityColoursLeft[1]))
                        else:
                            formatted.append(1 - (opponentCityColoursLeft[1] / opponentNum))
                elif move[0].get_colour() == Colour.orange:
                    formatted.append(3)
                    if temp[2] != 0:
                        formatted.append(1 - (opponentCityColoursLeft[2] / temp[2]))
                    else:
                        notCaptured = 0
                        for player in self.check_players_in_network(game_board):
                            if Colour.orange not in player.capturedCityCols:
                                notCaptured += 1
                        if notCaptured != 0:
                            formatted.append(1 - (notCaptured / opponentCityColoursLeft[2]))
                        else:
                            formatted.append(1 - (opponentCityColoursLeft[2] / opponentNum))
                elif move[0].get_colour() == Colour.green:
                    formatted.append(4)
                    if temp[3] != 0:
                        formatted.append(1 - (opponentCityColoursLeft[3] / temp[3]))
                    else:
                        notCaptured = 0
                        for player in self.check_players_in_network(game_board):
                            if Colour.green not in player.capturedCityCols:
                                notCaptured += 1
                        if notCaptured != 0:
                            formatted.append(1 - (notCaptured / opponentCityColoursLeft[3]))
                        else:
                            formatted.append(1 - (opponentCityColoursLeft[3] / opponentNum))
                elif move[0].get_colour() == Colour.blue:
                    formatted.append(5)
                    if temp[4] != 0:
                        formatted.append(1 - (opponentCityColoursLeft[4] / temp[4]))
                    else:
                        notCaptured = 0
                        for player in self.check_players_in_network(game_board):
                            if Colour.blue not in player.capturedCityCols:
                                notCaptured += 1
                        if notCaptured != 0:
                            formatted.append(1 - (notCaptured / opponentCityColoursLeft[4]))
                        else:
                            formatted.append(1 - (opponentCityColoursLeft[4] / opponentNum))
            elif isinstance(move[0], Nodes.City) and move[0] in self.citiesToCapture:
                if move[0].get_colour() == Colour.red:
                    formatted.append(1)
                    formatted.append(1)
                elif move[0].get_colour() == Colour.yellow:
                    formatted.append(2)
                    formatted.append(1)
                elif move[0].get_colour() == Colour.orange:
                    formatted.append(3)
                    formatted.append(1)
                elif move[0].get_colour() == Colour.green:
                    formatted.append(4)
                    formatted.append(1)
                elif move[0].get_colour() == Colour.blue:
                    formatted.append(5)
                    formatted.append(1)
            else:
                formatted.append(0)
                formatted.append(1)

            formatted.append(edgeCost)
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
            outputs = []
            for move in inputs:
                outputs.append(self.neuralNetwork.activate([move[0], move[1], move[2], move[3], move[4], move[5],
                                                            move[6], move[7], move[8]]))
            while True:
                choice = inputs[outputs.index(max(outputs))][9]
                # print(inputs[outputs.index(max(outputs))])
                cost = abs(inputs[outputs.index(max(outputs))][8])
                if self.tracksToPlace != -1:
                    if cost == 1 and self.tracksToPlace - 1 >= 0:
                        self.tracksToPlace -= 1
                        self.fitness -= 0.01


                        break
                    elif cost == 2 and self.tracksToPlace - 2 == 0:
                        self.tracksToPlace -= 2
                        self.fitness -= 0.02
                        print("{0} Move: {1} -> {2}"
                              .format(self.name, str(choice[1].get_id()), str(choice[0].get_id())))
                        break
                    else:
                        if len(outputs) > 1:
                            inputs.pop(outputs.index(max(outputs)))
                            outputs.pop(outputs.index(max(outputs)))
                        else:
                            # self.tracksToPlace -= 1
                            self.fitness -= 1
                            # print("NO MOVES LEFT: TTP: {0} T: {1} MOVES: {2}".format(self.tracksToPlace, cost, [i[6] for i in temp]))
                            return None
                else:
                    print("{0} City Captured: {1}"
                          .format(self.name, str(choice[1].get_name())))
                    break
            if self.has_won():
                return 'w'
            else:
                return [choice[0].get_id(), choice[1].get_id()]
        else:
            return 'w'

    def check_players_in_network(self, game_board: GameBoard):
        players = []
        for player in game_board.get_players():
            if player != self:
                if networkx.utils.graphs_equal(player.get_network(), self.get_network()):
                    players.append(player)
        return players

    def choose_start_pos(self, game_board: GameBoard) -> str:
        self.allCities = game_board.get_cities_grouped()
        self.tracksToPlace = -1
        city_id = self.make_move(game_board)[1]
        self.add_start_node(game_board.get_nodes().get(city_id))
        self.tracksToPlace = 2
        return city_id

    def has_won(self):
        for city in self.citiesToCapture:
            if city in self.get_network().nodes:
                print("{0} has captured: {1}"
                      .format(self.name, str(city.get_name())))
                self.capturedCityCols.append(city.get_colour())
                self.citiesToCapture.remove(city)
                self.fitness += 0.2
        return Player.has_won(self)

    def network_merge(self, game_board: GameBoard):
        ret = False
        for player in game_board.get_players():
            if player != self:
                for node in player.get_network().nodes:
                    if node in self._network:
                        self._network = networkx.compose(self._network,
                                                         player.get_network())
                        ret = True
                        break
        return ret
