import networkx as nx
import random
from Nodes import *


class GameBoard:
	def __add_node(self, cities: dict, node_id: str):
		"""Add a node to the map, deciding whether to add a city or normal node should be added
		:param cities: Cities Dictionary
		:param node_id: ID of node to add
		:return: None
		"""
		if node_id in cities.keys():
			colour = cities.get(node_id)[1]
			if colour == "blue":
				node = City(node_id, cities.get(node_id)[0], Colour.blue)
			elif colour == "red":
				node = City(node_id, cities.get(node_id)[0], Colour.red)
			elif colour == "orange":
				node = City(node_id, cities.get(node_id)[0], Colour.orange)
			elif colour == "yellow":
				node = City(node_id, cities.get(node_id)[0], Colour.yellow)
			else:
				node = City(node_id, cities.get(node_id)[0], Colour.green)
			self._cities[node_id] = node
			self.__map.add_node(node)
		else:
			node = Node(node_id)
			self.__map.add_node(node)
		self._nodes[node_id] = node

	def __add_edge(self, double_tracks: dict, start: Node, end: Node):
		if (start.get_id() in double_tracks.keys() and end.get_id() in double_tracks.get(start.get_id())) \
				or (end.get_id() in double_tracks.keys() and start.get_id() in double_tracks.get(end.get_id())):
			self.__map.add_edge(start, end, weight=2)
			self._edges[start.get_id() + end.get_id()] = (start, end, 2)
		else:
			self.__map.add_edge(start, end, weight=1)
			self._edges[start.get_id() + end.get_id()] = (start, end, 1)

	@staticmethod
	def __map_city_dict(city_list: str) -> dict:
		""" turn cities list into a dictionary
		:param city_list: List of cities in form of a string from config file
		:return: a dictionary of all cities where: node_id -> name
		"""
		city_dict = {}
		city_list = city_list.splitlines()
		for city in city_list:
			city_data = city.split(',')
			city_dict[city_data[0]] = [city_data[1], city_data[2]]
		return city_dict

	@staticmethod
	def __map_double_tracks(track_list: []) -> dict:
		track_dict = {}
		track_list = track_list.splitlines()
		for track in track_list:
			track = track.split(',')
			if track_dict.keys().__contains__(track[0]):
				track_dict[track[0]].append(track[1])
			else:
				track_dict[track[0]] = [track[1]]
		return track_dict

	def __generate_map(self, filepath: str):
		"""Generate a game map from a config file
		:param filepath: File path of the map config file
		:return: none
		"""
		# Read map file
		map_file = open(filepath)
		# "#" splits config sections
		map_data = map_file.read().split('#')
		# ":\n" denotes end of config title
		rows = map_data[1].split(':\n')[1].splitlines()
		cities = self.__map_city_dict(map_data[2].split(':\n')[1])
		double_tracks = self.__map_double_tracks(map_data[3].split(':\n')[1])
		# build map nodes and edges
		for i in range(0, len(rows)):
			# Add initial node for each row at starting position
			row_data = rows[i].split(',')
			start_val = int(row_data[0])
			row_len = int(row_data[1])
			prev_node_id = "0000"
			for j in range(0, row_len):
				node_id = str(start_val + (2 * j)).rjust(2, '0') + str(i).rjust(2, '0')
				self.__add_node(cities, node_id)
				if j != 0:  # no horizontal edge needed for first node in row
					self.__add_edge(double_tracks, self._nodes[node_id], self._nodes[prev_node_id])
				if i != 0:  # no intermediate edges needed for first row
					top_left = str((start_val - 1) + (2 * j)).rjust(2, '0') + str(i - 1).rjust(2, '0')
					top_right = str((start_val + 1) + (2 * j)).rjust(2, '0') + str(i - 1).rjust(2, '0')
					if top_left in self._nodes.keys():
						self.__add_edge(double_tracks, self._nodes.get(node_id), self._nodes.get(top_left))
					if top_right in self._nodes.keys():
						self.__add_edge(double_tracks, self._nodes.get(node_id), self._nodes.get(top_right))
				prev_node_id = node_id

	def __set_player_cities(self):
		random.seed()
		group_map = {}
		city_groups = []
		for city in self._cities.values():
			if city.get_colour() not in group_map.keys():
				group_map[city.get_colour()] = len(group_map)
				city_groups.append([])
			city_groups[group_map.get(city.get_colour())].append(city)
		for group in city_groups:
			random.shuffle(group)
		for player in self._players:
			player_cities = []
			for i in range(0, len(city_groups)):
				r = random.randint(0, len(city_groups[i]) - 1)
				player_cities.append(city_groups[i][r])
				city_groups[i].remove(city_groups[i][r])
			random.shuffle(player_cities)
			player.set_cities(player_cities)

	def __init__(self, players: [], map_filepath: str):
		self._players = players
		self._nodes = {}
		self._cities = {}
		self._edges = {}
		self.__map = nx.Graph()
		self.__generate_map(map_filepath)
		self.__set_player_cities()

	def get_map(self):
		return self.__map

	def get_cities(self):
		return self._cities

	def get_nodes(self):
		return self._nodes

	def get_players(self):
		return self._players

	def get_edges(self):
		return self._edges

	def place_track(self, edge0, edge1):
		self.__map[edge0][edge1]['weight'] = 0

	def place_coloured_track(self, edge0, edge1):
		self.__map[edge0][edge1]['weight'] = 100

	def get_cities_grouped(self):
		cities = [0, 0, 0, 0, 0]
		for city in self._cities.values():
			if city.get_colour() == Colour.red:
				cities[0] += 1
			elif city.get_colour() == Colour.yellow:
				cities[1] += 1
			elif city.get_colour() == Colour.orange:
				cities[2] += 1
			elif city.get_colour() == Colour.green:
				cities[3] += 1
			elif city.get_colour() == Colour.blue:
				cities[4] += 1
		return cities


	@staticmethod
	def is_valid_move(player, co_ords):
		return True
		# TODO: implement valid move check
