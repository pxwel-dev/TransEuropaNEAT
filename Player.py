import networkx
import networkx as nx
from networkx import Graph
from abc import abstractmethod

from GameBoard import GameBoard
from Nodes import *


class Player:
    def __init__(self, name):
        self.name = name
        self.tracksToPlace = 2
        self.colouredTracks = 3
        self.fitness = 0
        self.capturedCityCols = []
        self._networkAllTracks = Graph()
        self._networkNoColTracks = Graph()
        self._cities = {}
        self.skippedTurn = False

    def reset(self):
        self.tracksToPlace = 2
        self.colouredTracks = 3
        self.fitness = 0
        self.capturedCityCols = []
        self._networkAllTracks = Graph()
        self._networkNoColTracks = Graph()
        self._cities = {}
        self.skippedTurn = False

    def set_cities(self, cities):
        """ Set cities for a player, any overide must run Player.set_cities()

        :param cities: cities for the player
        :return: none
        """
        self._cities = cities

    def get_networkNoColTracks(self):
        return self._networkNoColTracks

    def get_networkAllTracks(self):
        return self._networkAllTracks

    def add_start_node(self, node: Node):
        self._networkAllTracks.add_node(node)
        self._networkNoColTracks.add_node(node)

    def add_node_to_network(self, game_board: GameBoard, chosen_node: [str, str], coloured: bool = False):
        edge = game_board.get_edges().get(chosen_node[0] + chosen_node[1])
        if edge is None:
            edge = game_board.get_edges().get(chosen_node[1] + chosen_node[0])

        if coloured:
            self._networkAllTracks.add_node(game_board.get_nodes().get(chosen_node[0]))
            self._networkAllTracks.add_edge(edge[0], edge[1], weight=0)
        else:
            self._networkNoColTracks.add_node(game_board.get_nodes().get(chosen_node[0]))
            self._networkNoColTracks.add_edge(edge[0], edge[1], weight=0)
            game_board.place_track(edge[0], edge[1])

    def network_merge(self, game_board: GameBoard):
        ret = False
        for player in game_board.get_players():
            if player != self:
                for node in player.get_networkNoColTracks().nodes:
                    if node in self._networkAllTracks:
                        self._networkAllTracks = networkx.compose(self._networkAllTracks,
                                                                  player.get_networkNoColTracks())
                        if node in self._networkNoColTracks:
                            self._networkNoColTracks = networkx.compose(self._networkNoColTracks,
                                                                        player.get_networkNoColTracks())
                        ret = True
                        break
        return ret

    @abstractmethod
    def choose_start_pos(self, game_board: GameBoard) -> str:
        print(self.name + " chose their starting position")
        return "0000"

    @abstractmethod
    def make_move(self, game_board: GameBoard) -> [str]:
        print(self.name + " took a turn")
        return ["0000", "0000"]

    def has_won(self) -> bool:
        """Has won function, any override must return Player.has_won(self)

        :return: if player has won
        """
        for city in self._cities:
            if city not in self._networkAllTracks.nodes:
                return False
        return True

    def _end_game_score(self, game_board: GameBoard) -> int:
        score = 0
        for city in self._cities:
            if city not in self._networkAllTracks:
                shortest_path = 999
                for node in self._networkAllTracks:
                    path_len = nx.shortest_path_length(game_board, city, node)
                    if path_len < shortest_path:
                        shortest_path = path_len
                score += shortest_path
        return score
