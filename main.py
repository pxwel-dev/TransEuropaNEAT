import neat
import os
from PlayerBoardCities import Player
from GlobalBoardCities import Board


class TransEuropaGame:
    def __init__(self, board, genomes, conf):
        self.round = 0
        self.genomes = genomes
        self.conf = conf
        self.board = board
        self.player1 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[0], config), genomes[0])
        self.player2 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[1], config), genomes[1])
        self.player3 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[2], config), genomes[2])
        self.player4 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[3], config), genomes[3])
        self.player5 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[4], config), genomes[4])
        self.player6 = Player(self.board, neat.nn.FeedForwardNetwork.create(self.genomes[5], config), genomes[5])

    def start_game(self):
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

        if self.round == 0:
            print(self.round)

            val1 = self.player1.make_move()
            val2 = self.player2.make_move()
            val3 = self.player3.make_move()
            val4 = self.player4.make_move()
            val5 = self.player5.make_move()
            val6 = self.player6.make_move()
            vals = [val1[1], val2[1], val3[1], val4[1], val5[1], val6[1]]
            for i in range(0, len(vals)):
                if vals[i]:
                    self.genomes[i].fitness += 10

                    self.player1.update_player_board_view(self.board)
                    self.player2.update_player_board_view(self.board)
                    self.player3.update_player_board_view(self.board)
                    self.player4.update_player_board_view(self.board)
                    self.player5.update_player_board_view(self.board)
                    self.player6.update_player_board_view(self.board)
                elif not vals[i]:
                    self.genomes[i].fitness -= 1

            if all(vals):
                self.round += 1
                print(self.round)
            else:
                pass

            distancesToCities = [self.player1.closest_target_distance(val1[0], [j for i in self.player1.citiesToCapture for j in i[1]]),
                                 self.player2.closest_target_distance(val2[0], [j for i in self.player2.citiesToCapture for j in i[1]]),
                                 self.player3.closest_target_distance(val3[0], [j for i in self.player3.citiesToCapture for j in i[1]]),
                                 self.player4.closest_target_distance(val4[0], [j for i in self.player4.citiesToCapture for j in i[1]]),
                                 self.player5.closest_target_distance(val5[0], [j for i in self.player5.citiesToCapture for j in i[1]]),
                                 self.player6.closest_target_distance(val6[0], [j for i in self.player6.citiesToCapture for j in i[1]])]
            print(distancesToCities)
            for i in range(0, len(distancesToCities)):
                score = 5
                if 3 >= distancesToCities[i] > 0:
                    score -= 1
                elif 6 >= distancesToCities[i] > 3:
                    score -= 2
                elif 9 >= distancesToCities[i] > 6:
                    score -= 3
                elif 12 >= distancesToCities[i] > 9:
                    score -= 4
                else:
                    score -= 15
                self.genomes[i].fitness += score

        if self.round == 1:
            while True:
                val1 = self.player1.make_move()
                val2 = self.player2.make_move()
                val3 = self.player3.make_move()
                val4 = self.player4.make_move()
                val5 = self.player5.make_move()
                val6 = self.player6.make_move()
                vals = [val1, val2, val3, val4, val5, val6]
                for i in range(0, len(vals)):
                    if vals[i]:
                        self.genomes[i].fitness += 10

                        self.player1.update_player_board_view(self.board)
                        self.player2.update_player_board_view(self.board)
                        self.player3.update_player_board_view(self.board)
                        self.player4.update_player_board_view(self.board)
                        self.player5.update_player_board_view(self.board)
                        self.player6.update_player_board_view(self.board)
                    if not vals[i]:
                        self.genomes[i].fitness -= 1
                if all(vals):
                    distancesToCities = [self.player1.closest_target_distance(val1[0],
                                                                              [j for i in self.player1.citiesToCapture for j in i[1]]),
                                         self.player2.closest_target_distance(val2[0],
                                                                              [j for i in self.player2.citiesToCapture
                                                                               for j in i[1]]),
                                         self.player3.closest_target_distance(val3[0],
                                                                              [j for i in self.player3.citiesToCapture
                                                                               for j in i[1]]),
                                         self.player4.closest_target_distance(val4[0],
                                                                              [j for i in self.player4.citiesToCapture
                                                                               for j in i[1]]),
                                         self.player5.closest_target_distance(val5[0],
                                                                              [j for i in self.player5.citiesToCapture
                                                                               for j in i[1]]),
                                         self.player6.closest_target_distance(val6[0],
                                                                              [j for i in self.player6.citiesToCapture
                                                                               for j in i[1]])]
                    for i in range(0, len(distancesToCities)):
                        score = 5
                        if distancesToCities[i] == 0:
                            score += 15
                        elif 3 >= distancesToCities[i] > 0:
                            score -= 1
                        elif 6 >= distancesToCities[i] > 3:
                            score -= 2
                        elif 9 >= distancesToCities[i] > 6:
                            score -= 3
                        elif 12 >= distancesToCities[i] > 9:
                            score -= 4
                        else:
                            score -= 15
                        self.genomes[i].fitness += score

                    self.round += 1
                    print(self.round)
                else:
                    break
            distancesToTracks = [
                self.player1.closest_target_distance(val1[0], [i for i in self.player1.tracksPlaced]),
                self.player2.closest_target_distance(val2[0], [i for i in self.player2.tracksPlaced]),
                self.player3.closest_target_distance(val3[0], [i for i in self.player3.tracksPlaced]),
                self.player4.closest_target_distance(val4[0], [i for i in self.player4.tracksPlaced]),
                self.player5.closest_target_distance(val5[0], [i for i in self.player5.tracksPlaced]),
                self.player6.closest_target_distance(val6[0], [i for i in self.player6.tracksPlaced])]
            print(distancesToTracks)
            for i in range(0, len(distancesToTracks)):
                score = 5
                if 1 >= distancesToTracks[i] > 0:
                    score -= 1
                elif 3 >= distancesToTracks[i] > 1:
                    score -= 2
                elif 6 >= distancesToTracks[i] > 3:
                    score -= 3
                elif 9 >= distancesToTracks[i] > 6:
                    score -= 4
                else:
                    score -= 15
                self.genomes[i].fitness += score


def eval_genomes(genomes, conf):
    if len(genomes) % 6 == 0:
        player_genomes = []
        for i, (genome_id, genome) in enumerate(genomes):
            genome.fitness = 0 if genome.fitness is None else genome.fitness
            player_genomes.append(genome)
            if len(player_genomes) == 6:
                print("Starting game...")
                board = Board()
                game = TransEuropaGame(board, player_genomes, conf)
                game.start_game()
                player_genomes.clear()
            else:
                pass

    else:
        if len(genomes) != 0:
            temp_fitness = []
            for i, (genome_id, genome) in enumerate(genomes):
                temp_fitness.append(genome.fitness)
            while len(genomes) % 6 != 0:
                index = temp_fitness.index(min(temp_fitness))
                temp_fitness.pop(index)
                genomes.pop(index)


def run_neat(conf):
    pop = neat.Population(conf)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(10))

    pop.run(eval_genomes, 100)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEATconfig.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
