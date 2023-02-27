import neat
import os
import multiprocessing
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
        print("Round: " + str(self.round))

        temp1 = [len(self.player1.citiesToCapture), len(self.player2.citiesToCapture),
                 len(self.player3.citiesToCapture),
                 len(self.player4.citiesToCapture), len(self.player5.citiesToCapture),
                 len(self.player6.citiesToCapture)]

        vals = [self.player1.make_move(), self.player2.make_move(), self.player3.make_move(),
                self.player4.make_move(), self.player5.make_move(), self.player6.make_move()]

        temp2 = [len(self.player1.citiesToCapture), len(self.player2.citiesToCapture),
                 len(self.player3.citiesToCapture),
                 len(self.player4.citiesToCapture), len(self.player5.citiesToCapture),
                 len(self.player6.citiesToCapture)]

        for i in range(0, len(vals)):
            if vals[i][1]:
                self.genomes[i].fitness += 25

                self.player1.update_player_board_view(self.board)
                self.player2.update_player_board_view(self.board)
                self.player3.update_player_board_view(self.board)
                self.player4.update_player_board_view(self.board)
                self.player5.update_player_board_view(self.board)
                self.player6.update_player_board_view(self.board)

                if temp2[i] < temp1[i]:
                    self.genomes[i].fitness += 50
            else:
                self.genomes[i].fitness -= 1000

        self.city_distance_fitness(vals[0][0], vals[1][0], vals[2][0], vals[3][0], vals[4][0], vals[5][0])

        #if self.round > 1:
        #   self.track_network_distance_fitness(vals[0][0], vals[1][0], vals[2][0], vals[3][0], vals[4][0], vals[5][0])

        if all([vals[0][1], vals[1][1], vals[2][1], vals[3][1], vals[4][1], vals[5][1]]):
            print("All bots have played valid moves")
            return True
        else:
            return False

    def city_distance_fitness(self, val1, val2, val3, val4, val5, val6):
        distancesToCities = [
            self.player1.closest_target_distance(val1, [j for i in self.player1.citiesToCapture for j in i[1]]),
            self.player2.closest_target_distance(val2, [j for i in self.player2.citiesToCapture for j in i[1]]),
            self.player3.closest_target_distance(val3, [j for i in self.player3.citiesToCapture for j in i[1]]),
            self.player4.closest_target_distance(val4, [j for i in self.player4.citiesToCapture for j in i[1]]),
            self.player5.closest_target_distance(val5, [j for i in self.player5.citiesToCapture for j in i[1]]),
            self.player6.closest_target_distance(val6, [j for i in self.player6.citiesToCapture for j in i[1]])]

        print("Distances to cities: " + str(distancesToCities))

        for i in range(0, len(distancesToCities)):
            if 2 >= distancesToCities[i] > 0:
                self.genomes[i].fitness += 10
            elif 4 >= distancesToCities[i] > 2:
                self.genomes[i].fitness += 5
            elif 6 >= distancesToCities[i] > 4:
                self.genomes[i].fitness += 2.5
            elif 8 >= distancesToCities[i] > 6:
                self.genomes[i].fitness += 1.25
            elif 10 >= distancesToCities[i] > 8:
                self.genomes[i].fitness += 0.625

    def track_network_distance_fitness(self, val1, val2, val3, val4, val5, val6):
        distancesToTracks = [
            self.player1.closest_target_distance(val1, [i for i in self.player1.tracksPlaced]),
            self.player2.closest_target_distance(val2, [i for i in self.player2.tracksPlaced]),
            self.player3.closest_target_distance(val3, [i for i in self.player3.tracksPlaced]),
            self.player4.closest_target_distance(val4, [i for i in self.player4.tracksPlaced]),
            self.player5.closest_target_distance(val5, [i for i in self.player5.tracksPlaced]),
            self.player6.closest_target_distance(val6, [i for i in self.player6.tracksPlaced])]

        print("Distances to tracks: " + str(distancesToTracks))

        for i in range(0, len(distancesToTracks)):
            if 2 >= distancesToTracks[i] > 0:
                self.genomes[i].fitness += 10
            elif 4 >= distancesToTracks[i] > 2:
                self.genomes[i].fitness += 5
            elif 6 >= distancesToTracks[i] > 4:
                self.genomes[i].fitness += 2.5
            elif 8 >= distancesToTracks[i] > 6:
                self.genomes[i].fitness += 1.25
            elif 10 >= distancesToTracks[i] > 8:
                self.genomes[i].fitness += 0.625


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
                game.init_game()
                while True:
                    if not game.play_moves():
                        break
                    else:
                        pass
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
