import copy
import random

import neat
import os
from multiprocessing import Pool
import numpy as np
from PlayerBoardCities import Player
from GlobalBoardCities import Board

POP_SIZE = 72
NUMBER_OF_GAMES = 10
GENERATIONS = 100


class TransEuropaGame:
    def __init__(self, board, genomes, conf):
        self.round = 0
        self.winner = False
        self.winnerPlayer = None
        self.genomes = genomes
        self.conf = conf
        self.board = board
        self.player1 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[0], self.conf), genomes[0],
                              "1")
        self.player2 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[1], self.conf), genomes[1],
                              "2")
        self.player3 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[2], self.conf), genomes[2],
                              "3")
        self.player4 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[3], self.conf), genomes[3],
                              "4")
        self.player5 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[4], self.conf), genomes[4],
                              "5")
        self.player6 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[5], self.conf), genomes[5],
                              "6")

    def init_game(self):
        self.player1.citiesToCapture = self.board.init_player_cities()
        self.player2.citiesToCapture = self.board.init_player_cities()
        self.player3.citiesToCapture = self.board.init_player_cities()
        self.player4.citiesToCapture = self.board.init_player_cities()
        self.player5.citiesToCapture = self.board.init_player_cities()
        self.player6.citiesToCapture = self.board.init_player_cities()

        self.player1.set_map_targets()
        self.player2.set_map_targets()
        self.player3.set_map_targets()
        self.player4.set_map_targets()
        self.player5.set_map_targets()
        self.player6.set_map_targets()

    def play_moves(self):
        self.round += 1
        print("==========\nRound: " + str(self.round) + "\n==========")

        self.player1.tracksToPlace = 2
        self.player2.tracksToPlace = 2
        self.player3.tracksToPlace = 2
        self.player4.tracksToPlace = 2
        self.player5.tracksToPlace = 2
        self.player6.tracksToPlace = 2

        while self.player1.tracksToPlace != 0 and not self.winner:
            move1 = self.player1.make_move(self.player1.create_network_inputs(self.player1.find_all_possible_moves()))
            if move1 == ValueError:
                self.genomes[0].fitness -= 1
                return False
            self.update_board(self.player1.currentBoard)
            if move1[2] == 1:
                self.genomes[0].fitness -= 0.01
            elif move1[2] == 2:
                self.genomes[0].fitness -= 0.02

            edge = self.player1.check_network_merge()

            if edge:
                if edge in self.player2.tracksPlaced:
                    self.player1.merge_networks(self.player2.tracksPlaced)
                    self.player2.merge_networks(self.player1.tracksPlaced)
                if edge in self.player3.tracksPlaced:
                    self.player1.merge_networks(self.player3.tracksPlaced)
                    self.player3.merge_networks(self.player1.tracksPlaced)
                if edge in self.player4.tracksPlaced:
                    self.player1.merge_networks(self.player4.tracksPlaced)
                    self.player4.merge_networks(self.player1.tracksPlaced)
                if edge in self.player5.tracksPlaced:
                    self.player1.merge_networks(self.player5.tracksPlaced)
                    self.player5.merge_networks(self.player1.tracksPlaced)
                if edge in self.player6.tracksPlaced:
                    self.player1.merge_networks(self.player6.tracksPlaced)
                    self.player6.merge_networks(self.player1.tracksPlaced)

            if self.player1.won:
                self.winner = True
                self.winnerPlayer = 1
                self.genomes[0].fitness += 1
                break

        while self.player2.tracksToPlace != 0 and not self.winner:
            move2 = self.player2.make_move(self.player2.create_network_inputs(self.player2.find_all_possible_moves()))
            if move2 == ValueError:
                self.genomes[1].fitness -= 1
                return False
            self.update_board(self.player2.currentBoard)
            if move2[2] == 1:
                self.genomes[1].fitness -= 0.01
            elif move2[2] == 2:
                self.genomes[1].fitness -= 0.02

            edge = self.player2.check_network_merge()

            if edge:
                if edge in self.player1.tracksPlaced:
                    self.player2.merge_networks(self.player1.tracksPlaced)
                    self.player1.merge_networks(self.player2.tracksPlaced)
                if edge in self.player3.tracksPlaced:
                    self.player2.merge_networks(self.player3.tracksPlaced)
                    self.player3.merge_networks(self.player2.tracksPlaced)
                if edge in self.player4.tracksPlaced:
                    self.player2.merge_networks(self.player4.tracksPlaced)
                    self.player4.merge_networks(self.player2.tracksPlaced)
                if edge in self.player5.tracksPlaced:
                    self.player2.merge_networks(self.player5.tracksPlaced)
                    self.player5.merge_networks(self.player2.tracksPlaced)
                if edge in self.player6.tracksPlaced:
                    self.player2.merge_networks(self.player6.tracksPlaced)
                    self.player6.merge_networks(self.player2.tracksPlaced)

            if self.player2.won:
                self.winner = True
                self.winnerPlayer = 2
                self.genomes[1].fitness += 1
                break

        while self.player3.tracksToPlace != 0 and not self.winner:
            move3 = self.player3.make_move(self.player3.create_network_inputs(self.player3.find_all_possible_moves()))
            if move3 == ValueError:
                self.genomes[2].fitness -= 1
                return False
            self.update_board(self.player3.currentBoard)
            if move3[2] == 1:
                self.genomes[2].fitness -= 0.01
            elif move3[2] == 2:
                self.genomes[2].fitness -= 0.02

            edge = self.player3.check_network_merge()

            if edge:
                if edge in self.player1.tracksPlaced:
                    self.player3.merge_networks(self.player1.tracksPlaced)
                    self.player1.merge_networks(self.player3.tracksPlaced)
                if edge in self.player2.tracksPlaced:
                    self.player3.merge_networks(self.player2.tracksPlaced)
                    self.player2.merge_networks(self.player3.tracksPlaced)
                if edge in self.player4.tracksPlaced:
                    self.player3.merge_networks(self.player4.tracksPlaced)
                    self.player4.merge_networks(self.player3.tracksPlaced)
                if edge in self.player5.tracksPlaced:
                    self.player3.merge_networks(self.player5.tracksPlaced)
                    self.player5.merge_networks(self.player3.tracksPlaced)
                if edge in self.player6.tracksPlaced:
                    self.player3.merge_networks(self.player6.tracksPlaced)
                    self.player6.merge_networks(self.player3.tracksPlaced)

            if self.player3.won:
                self.winner = True
                self.winnerPlayer = 3
                self.genomes[2].fitness += 1
                break

        while self.player4.tracksToPlace != 0 and not self.winner:
            move4 = self.player4.make_move(self.player4.create_network_inputs(self.player4.find_all_possible_moves()))
            if move4 == ValueError:
                self.genomes[3].fitness -= 1
                return False
            self.update_board(self.player4.currentBoard)
            if move4[2] == 1:
                self.genomes[3].fitness -= 0.01
            elif move4[2] == 2:
                self.genomes[3].fitness -= 0.02

            edge = self.player4.check_network_merge()

            if edge:
                if edge in self.player2.tracksPlaced:
                    self.player4.merge_networks(self.player2.tracksPlaced)
                    self.player2.merge_networks(self.player4.tracksPlaced)
                if edge in self.player3.tracksPlaced:
                    self.player4.merge_networks(self.player3.tracksPlaced)
                    self.player3.merge_networks(self.player4.tracksPlaced)
                if edge in self.player1.tracksPlaced:
                    self.player4.merge_networks(self.player1.tracksPlaced)
                    self.player1.merge_networks(self.player4.tracksPlaced)
                if edge in self.player5.tracksPlaced:
                    self.player4.merge_networks(self.player5.tracksPlaced)
                    self.player5.merge_networks(self.player4.tracksPlaced)
                if edge in self.player6.tracksPlaced:
                    self.player4.merge_networks(self.player6.tracksPlaced)
                    self.player6.merge_networks(self.player4.tracksPlaced)

            if self.player4.won:
                self.winner = True
                self.winnerPlayer = 4
                self.genomes[3].fitness += 1
                break

        while self.player5.tracksToPlace != 0 and not self.winner:
            move5 = self.player5.make_move(self.player5.create_network_inputs(self.player5.find_all_possible_moves()))
            if move5 == ValueError:
                self.genomes[4].fitness -= 1
                return False
            self.update_board(self.player5.currentBoard)
            if move5[2] == 1:
                self.genomes[4].fitness -= 0.01
            elif move5[2] == 2:
                self.genomes[4].fitness -= 0.02

            edge = self.player5.check_network_merge()

            if edge:
                if edge in self.player2.tracksPlaced:
                    self.player5.merge_networks(self.player2.tracksPlaced)
                    self.player2.merge_networks(self.player5.tracksPlaced)
                if edge in self.player3.tracksPlaced:
                    self.player5.merge_networks(self.player3.tracksPlaced)
                    self.player3.merge_networks(self.player5.tracksPlaced)
                if edge in self.player4.tracksPlaced:
                    self.player5.merge_networks(self.player4.tracksPlaced)
                    self.player4.merge_networks(self.player5.tracksPlaced)
                if edge in self.player1.tracksPlaced:
                    self.player5.merge_networks(self.player1.tracksPlaced)
                    self.player1.merge_networks(self.player5.tracksPlaced)
                if edge in self.player6.tracksPlaced:
                    self.player5.merge_networks(self.player6.tracksPlaced)
                    self.player6.merge_networks(self.player5.tracksPlaced)

            if self.player5.won:
                self.winner = True
                self.winnerPlayer = 5
                self.genomes[4].fitness += 1
                break

        while self.player6.tracksToPlace != 0 and not self.winner:
            move6 = self.player6.make_move(self.player6.create_network_inputs(self.player6.find_all_possible_moves()))
            if move6 == ValueError:
                self.genomes[5].fitness -= 1
                return False
            self.update_board(self.player6.currentBoard)
            if move6[2] == 1:
                self.genomes[5].fitness -= 0.01
            elif move6[2] == 2:
                self.genomes[5].fitness -= 0.02

            edge = self.player6.check_network_merge()

            if edge:
                if edge in self.player2.tracksPlaced:
                    self.player6.merge_networks(self.player2.tracksPlaced)
                    self.player2.merge_networks(self.player6.tracksPlaced)
                if edge in self.player3.tracksPlaced:
                    self.player6.merge_networks(self.player3.tracksPlaced)
                    self.player3.merge_networks(self.player6.tracksPlaced)
                if edge in self.player4.tracksPlaced:
                    self.player6.merge_networks(self.player4.tracksPlaced)
                    self.player4.merge_networks(self.player6.tracksPlaced)
                if edge in self.player5.tracksPlaced:
                    self.player6.merge_networks(self.player5.tracksPlaced)
                    self.player5.merge_networks(self.player6.tracksPlaced)
                if edge in self.player1.tracksPlaced:
                    self.player6.merge_networks(self.player1.tracksPlaced)
                    self.player1.merge_networks(self.player6.tracksPlaced)

            if self.player6.won:
                self.winner = True
                self.winnerPlayer = 6
                self.genomes[5].fitness += 1
                break

        if self.winner:
            print("Winner found!\nWinner: Player {0}".format(str(self.winnerPlayer)))

            # self.genomes[0].fitness += ((5 - len(self.player1.citiesToCapture)) * 2 / 10)
            # self.genomes[1].fitness += ((5 - len(self.player2.citiesToCapture)) * 2 / 10)
            # self.genomes[2].fitness += ((5 - len(self.player3.citiesToCapture)) * 2 / 10)
            # self.genomes[3].fitness += ((5 - len(self.player4.citiesToCapture)) * 2 / 10)
            # self.genomes[4].fitness += ((5 - len(self.player5.citiesToCapture)) * 2 / 10)
            # self.genomes[5].fitness += ((5 - len(self.player6.citiesToCapture)) * 2 / 10)

            # self.city_distance_fitness(self.player1, 0)
            # self.city_distance_fitness(self.player2, 1)
            # self.city_distance_fitness(self.player3, 2)
            # self.city_distance_fitness(self.player4, 3)
            # self.city_distance_fitness(self.player5, 4)
            # self.city_distance_fitness(self.player6, 5)

            # for i in range(1, 7):
            #     if i != self.winnerPlayer:
            #         self.genomes[i-1].fitness -= 1

            return False
        else:
            return True

    def update_board(self, board):
        self.player1.update_player_board_view(board)
        self.player2.update_player_board_view(board)
        self.player3.update_player_board_view(board)
        self.player4.update_player_board_view(board)
        self.player5.update_player_board_view(board)
        self.player6.update_player_board_view(board)

    # def city_distance_fitness(self, player, player_number):
    #     cityDistances = []
    #     cityStartEnd = []
    #     if len(player.citiesToCapture) != 0:
    #         for city in player.citiesToCapture:
    #             temp = []
    #             temp1 = []
    #             for city_track in city[1]:
    #                 temp2 = []
    #                 start_end = []
    #                 for track in player.tracksPlaced:
    #                     temp2.append((abs(city_track[0] - track[0]) + abs(city_track[1] - track[1])))
    #                     start_end.append([track, city_track])
    #                 temp.append(start_end[temp2.index(min(temp2))])
    #                 temp1.append(min(temp2))
    #             cityDistances.append(min(temp1))
    #             cityStartEnd.append(temp[temp1.index(min(temp1))])
    #         total = 0
    #         for i in cityDistances:
    #             total += i
    #         self.genomes[player_number].fitness -= (total / 100)
    #     else:
    #         pass


def eval_genomes(genomes, conf):
    fitness = []
    while True:
        if len(genomes) % 6 == 0:
            random.shuffle(genomes)
            genome_subtasks = [array for array in np.array_split(genomes, 6)]

            pool = Pool(processes=6)

            p1 = pool.apply_async(func=multiprocessing_eval, args=(genome_subtasks[0], conf))
            p2 = pool.apply_async(func=multiprocessing_eval, args=(genome_subtasks[1], conf))
            p3 = pool.apply_async(func=multiprocessing_eval, args=(genome_subtasks[2], conf))
            p4 = pool.apply_async(func=multiprocessing_eval, args=(genome_subtasks[3], conf))
            p5 = pool.apply_async(func=multiprocessing_eval, args=(genome_subtasks[4], conf))
            p6 = pool.apply_async(func=multiprocessing_eval, args=(genome_subtasks[5], conf))

            pool.close()
            pool.join()

            temp = []

            for i in [p1.get(), p2.get(), p3.get(), p4.get(), p5.get(), p6.get()]:
                for j in i:
                    temp.append(j)

            for (genome_id, genome), (temp_genome_id, temp_genome) in zip(genomes, temp):
                genome.fitness = temp_genome.fitness
                fitness.append(genome.fitness)

            file = open("fitnessDataTest2", 'a')
            file.write(str(max(fitness)) + "\n")
            file.close()
            break
        else:
            if len(genomes) != 0:
                temp_fitness = []
                for i, (genome_id, genome) in enumerate(genomes):
                    genome.fitness = 0 if genome.fitness is None else genome.fitness
                    temp_fitness.append(genome.fitness)
                while len(genomes) % 6 != 0:
                    index = temp_fitness.index(min(temp_fitness))
                    temp_fitness.pop(index)
                    genomes.pop(index)


def multiprocessing_eval(genomes, conf):
    count = 0
    player_genomes = []
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0  # if genome.fitness is None else genome.fitness
        player_genomes.append(genome)
        if len(player_genomes) == 6:
            count += 1
            for j in range(0, NUMBER_OF_GAMES):
                print("Starting game {0}/{1}:{2}...".format(count, int(len(genomes) / 6), j + 1))
                board = Board()
                game = TransEuropaGame(board, player_genomes, conf)
                game.init_game()
                while True:
                    if not game.play_moves():
                        break
            player_genomes.clear()
    return genomes


def final_match(best_player, conf):
    players = []
    for i in range(0, 6):
        players.append(copy.deepcopy(best_player))
    board = Board()
    game = TransEuropaGame(board, players, conf)
    game.init_game()
    while True:
        if not game.play_moves():
            break


def run_neat(conf):
    # pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-99')
    pop = neat.Population(conf)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))

    best_genome = pop.run(eval_genomes, GENERATIONS)
    final_match(best_genome, conf)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEATconfig.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
