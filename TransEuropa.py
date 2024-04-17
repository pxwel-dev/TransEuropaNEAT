from GameBoard import GameBoard
from HumanPlayer import HumanPlayer
from AllBots.NEAT_SIMPLEv6Player import NEATPlayer
from AllBots.ImperfectMaxN import ImpMaxNPlayer


class TransEuropa:
	def __init__(self, players: [], map_filepath: str):
		self.__players = players
		self._map_filepath = map_filepath
		self.__board = GameBoard(self.__players, self._map_filepath)
		self.turn_count = 0

	def reset_game(self):
		self.__board = GameBoard(self.__players, self._map_filepath)
		self.turn_count = 0
		for player in self.__players:
			player.reset()

	def play_game(self):
		for player in self.__board.get_players():
			if isinstance(player, HumanPlayer):
				print("{0}'s cities to capture:".format(player.name))
				while input("\nPress enter to view cities: ") != '':
					continue
				print([[city.get_name(), city.get_id()] for city in player.citiesToCapture])
				while input("\nPress enter to continue: ") != '':
					continue
		#
		# 		for i in range(0, 100):
		# 			print("=====FLUSHING TERMINAL=====")
		for player in self.__board.get_players():
			# if isinstance(player, NEATPlayer):
			# 	print(player.name + ': ' + player.choose_start_pos(self.__board))
			# 	#player.choose_start_pos(self.__board)
			# elif isinstance(player, ImpMaxNPlayer):
			# 	print(player.name + ': ' + player.choose_start_pos(self.__board))
			# 	#player.choose_start_pos(self.__board)
			# else:
			# 	player.choose_start_pos(self.__board)
			player.choose_start_pos(self.__board)
		game_won = False
		self.turn_count = 0
		while not game_won:
			self.turn_count += 1
			print("==========\nRound: " + str(self.turn_count) + "\n==========")
			for player in self.__board.get_players():
				if not player.has_won() and not game_won:
					player.tracksToPlace = 2
					player.skippedTurn = False
					while player.tracksToPlace > 0 and not player.has_won():
						player.network_merge(self.__board)
						player_move_state = player.make_move(self.__board)
						if player_move_state == 'w':
							game_won = True
							break
						elif player_move_state is None:
							pass
						elif player_move_state == -1:
							break
						else:
							player.add_node_to_network(self.__board, player_move_state[0], player_move_state[1])
							player.network_merge(self.__board)
							if player.has_won():
								game_won = True
								break
				else:
					game_won = True
					break
		return self.end_game(self.turn_count)

	def end_game(self, turns):
		for player in self.__players:
			if player.has_won():
				print("Round {0} | Winner found! | Winner: {1}".format(str(turns), player.name))
		fitnessScore = []
		for player in self.__board.get_players():
			if isinstance(player, NEATPlayer):
				print("Neural Network Cities Left: \n ", [city.get_name() for city in player.citiesToCapture])
				fitnessScore.append(player.fitness)
		return fitnessScore

	def get_players(self) -> []:
		return self.__players

	def get_winner(self):
		for player in self.__players:
			if player.has_won():
				return player.name


