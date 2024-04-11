import copy
import networkx
from Player import Player
from GameBoard import GameBoard


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.citiesToCapture = []

    def choose_start_pos(self, game_board: GameBoard) -> str:
        coord = ""
        while len(coord) != 4 and (not coord.isnumeric()):
            coord = input("{0}'s turn: Input co-ordinates of starting position:".format(self.name))
        self.add_start_node(game_board.get_nodes().get(coord))
        return coord

    def make_move(self, game_board: GameBoard) -> [str, str]:  # node to add to network should always be first
        self.network_merge(game_board)
        if not self.has_won():
            while True:
                coords = []
                coord = ""
                while len(coord) != 4 and (not coord.isnumeric()):
                    coord = input("{0}'s turn: Input co-ordinates of first node to connect:".format(self.name))
                coords.append(coord)
                coord = ""
                while len(coord) != 4 and (not coord.isnumeric()):
                    coord = input("{0}'s turn: Input co-ordinates of second node to connect:".format(self.name))
                coords.append(coord)
                try:
                    self.tracksToPlace -= game_board.get_edges()[coords[0] + coords[1]][2]
                    break
                except KeyError:
                    pass
                try:
                    self.tracksToPlace -= game_board.get_edges()[coords[1] + coords[0]][2]
                    break
                except KeyError:
                    print("Invalid move, try again.")
            self.has_won()
            return coords
        else:
            return 'w'

    def set_cities(self, cities):
        self._cities = cities
        self.citiesToCapture = copy.copy(cities)

    def has_won(self):
        for city in self.citiesToCapture:
            if city in self.get_network().nodes:
                print("{0} has captured: {1}"
                      .format(self.name, str(city.get_name())))
                self.citiesToCapture.remove(city)
        return Player.has_won(self)
