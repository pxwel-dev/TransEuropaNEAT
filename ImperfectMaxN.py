from Nodes import Colour
from Player import Player
from GameBoard import GameBoard
import networkx
import copy
import random


class ImpMaxNPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.citiesToCapture = []

    def set_cities(self, cities):
        self._cities = cities
        self.citiesToCapture = copy.copy(cities)

    def find_all_possible_moves(self, game_board: GameBoard):
        self.network_merge(game_board)
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

    def select_best_move(self, moves, game_board: GameBoard):
        reformatted = []
        for move in moves:
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

            formatted = []
            for i in minCityDistances:
                formatted.append(i)

            formatted.append(edgeCost)
            formatted.append(move)
            reformatted.append(formatted)

        totalDistances = []
        totalSingleTrackDists = []
        singleTrackMoves = []
        for formattedMove in reformatted:
            temp = []
            for i in [formattedMove[0], formattedMove[1], formattedMove[2], formattedMove[3], formattedMove[4]]:
                if i != -1:
                    temp.append(i)

            totalDistances.append(min(temp))
            if formattedMove[5] == 1:
                for i in [formattedMove[0], formattedMove[1], formattedMove[2], formattedMove[3], formattedMove[4]]:
                    if i != -1:
                        temp.append(i)
                totalSingleTrackDists.append(min(temp))
                singleTrackMoves.append(formattedMove)
        if self.tracksToPlace == 1:
            if len(totalSingleTrackDists) != 0:
                return singleTrackMoves[totalSingleTrackDists.index(min(totalSingleTrackDists))]
        else:
            if len(totalDistances) != 0:
                return reformatted[totalDistances.index(min(totalDistances))]
        return None

    def make_move(self, game_board: GameBoard) -> [str]:
        if not self.has_won():
            bestMove = self.select_best_move(self.find_all_possible_moves(game_board), game_board)
            while True:
                choice = bestMove[6]
                cost = bestMove[5]
                if self.tracksToPlace != -1:
                    if cost == 1 and self.tracksToPlace - 1 >= 0:
                        self.tracksToPlace -= 1
                        # print("{0} Move: {1} -> {2}"
                        #       .format(self.name, str(choice[1].get_id()), str(choice[0].get_id())))
                        break
                    elif cost == 2 and self.tracksToPlace - 2 == 0:
                        self.tracksToPlace -= 2
                        # print("{0} Move: {1} -> {2}"
                        #       .format(self.name, str(choice[1].get_id()), str(choice[0].get_id())))
                        break
                    else:
                        return None
                else:
                    # print("{0} City Captured: {1}"
                    #       .format(self.name, str(choice[1].get_name())))
                    break
            if self.has_won():
                return 'w'
            else:
                return [choice[0].get_id(), choice[1].get_id()]
        else:
            return 'w'

    def choose_start_pos(self, game_board: GameBoard) -> str:
        self.tracksToPlace = -1
        city_id = self.make_move(game_board)[1]
        self.add_start_node(game_board.get_nodes().get(city_id))
        self.tracksToPlace = 2
        return city_id

    def has_won(self):
        for city in self.citiesToCapture:
            if city in self.get_network().nodes:
                # print("{0} has captured: {1}"
                #       .format(self.name, str(city.get_name())))
                self.capturedCityCols.append(city.get_colour())
                self.citiesToCapture.remove(city)
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
