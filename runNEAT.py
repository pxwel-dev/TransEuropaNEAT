import copy
import random

from HumanPlayer import HumanPlayer
from NEAT_SIMPLEv6Player import NEATPlayer as NEAT_SIMPLEv6
from NEAT_SIMPLEv5Player import NEATPlayer as NEAT_SIMPLEv5
from NEAT_SIMPLEv4Player import NEATPlayer as NEAT_SIMPLEv4
from NEAT_SIMPLEv3Player import NEATPlayer as NEAT_SIMPLEv3
from NEAT_SIMPLEv2Player import NEATPlayer as NEAT_SIMPLEv2
from NEAT_SIMPLEPlayer import NEATPlayer as NEAT_SIMPLE
from ImperfectMaxN import ImpMaxNPlayer
from ImperfectMaxNv2 import ImpMaxNPlayer as ImpMaxNPlayerV2
from ImperfectMaxNv3 import ImpMaxNPlayer as ImpMaxNPlayerV3
from TransEuropa import TransEuropa
import neat
import os
from multiprocessing import Pool
import numpy as np
import pickle

POP_SIZE = 72
NUMBER_OF_GAMES = 10
GENERATIONS = 100


def eval_genomes(genomes, conf):
    random.seed()
    random.shuffle(genomes)
    fitness = []
    while True:
        if len(genomes) % 6 == 0:
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

            file = open("fitnessDataTest", 'a')
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
    playerGenomes = []
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0  # if genome.fitness is None else genome.fitness
        playerGenomes.append(genome)
        if len(playerGenomes) == 6:
            count += 1
            for j in range(0, NUMBER_OF_GAMES):
                print("Starting game {0}/{1}:{2}...".format(count, int(len(genomes) / 6), j + 1))
                formattedPlayers = [
                    NEAT_SIMPLEv6("1", neat.nn.FeedForwardNetwork.create(playerGenomes[0], conf), playerGenomes[0]),
                    NEAT_SIMPLEv6("2", neat.nn.FeedForwardNetwork.create(playerGenomes[1], conf), playerGenomes[1]),
                    NEAT_SIMPLEv6("3", neat.nn.FeedForwardNetwork.create(playerGenomes[2], conf), playerGenomes[2]),
                    NEAT_SIMPLEv6("4", neat.nn.FeedForwardNetwork.create(playerGenomes[3], conf), playerGenomes[3]),
                    NEAT_SIMPLEv6("5", neat.nn.FeedForwardNetwork.create(playerGenomes[4], conf), playerGenomes[4]),
                    NEAT_SIMPLEv6("6", neat.nn.FeedForwardNetwork.create(playerGenomes[5], conf), playerGenomes[5])]
                game = TransEuropa(formattedPlayers, "classic.txt")
                fitnessScore = game.play_game()
                playerGenomes[0].fitness += fitnessScore[0]
                playerGenomes[1].fitness += fitnessScore[1]
                playerGenomes[2].fitness += fitnessScore[2]
                playerGenomes[3].fitness += fitnessScore[3]
                playerGenomes[4].fitness += fitnessScore[4]
                playerGenomes[5].fitness += fitnessScore[5]
                print("=================================\n"
                      "Game {0}/{1}:{2} Summary\n"
                      "Rounds: {9}\n"
                      "=================================\n"
                      "Cumulative fitness in {10} games:\n"
                      "=================================\n"
                      "Player 1: {3}\n"
                      "Player 2: {4}\n"
                      "Player 3: {5}\n"
                      "Player 4: {6}\n"
                      "Player 5: {7}\n"
                      "Player 6: {8}\n"
                      "=================================".format(count, int(len(genomes) / 6), j + 1,
                                                                 playerGenomes[0].fitness,
                                                                 playerGenomes[1].fitness,
                                                                 playerGenomes[2].fitness,
                                                                 playerGenomes[3].fitness,
                                                                 playerGenomes[4].fitness,
                                                                 playerGenomes[5].fitness,
                                                                 game.turn_count,
                                                                 NUMBER_OF_GAMES))


            playerGenomes.clear()
    return genomes

def test_best_network(conf):
    f = open("NEAT-SIMPLEv6.pickle", "rb")
    best_player = pickle.load(f)
    game = TransEuropa([NEAT_SIMPLEv6("NeuralNetwork", neat.nn.FeedForwardNetwork.create(best_player, conf), best_player), HumanPlayer("Pawel"), HumanPlayer("Jan")], "classic.txt")
    game.play_game()


def run_neat(conf, name):
    # pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-182')
    pop = neat.Population(conf)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))

    best_genome = pop.run(eval_genomes, GENERATIONS)
    with open(name, "wb") as file:
        pickle.dump(best_genome, file)
    # final_match(best_genome, conf)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEATconfig.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    configV2_path = os.path.join(local_dir, "NEATconfigV2.txt")

    configV2 = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configV2_path)

    configV3_path = os.path.join(local_dir, "NEATconfigV3.txt")

    configV3 = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,


                           neat.DefaultSpeciesSet, neat.DefaultStagnation,
                           configV3_path)

    configV4_path = os.path.join(local_dir, "NEATconfigV4.txt")

    configV4 = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                           neat.DefaultSpeciesSet, neat.DefaultStagnation,
                           configV4_path)

    # run_neat(config, "NEAT-SIMPLE.pickle")
    # run_neat(configV2, "NEAT-SIMPLEv2.pickle")
    # run_neat(configV3, "NEAT-SIMPLEv3.pickle")
    # run_neat(configV4, "NEAT-SIMPLEv5.pickle")
    # run_neat(configV4, "NEAT-SIMPLEv6.pickle")
    #test_best_network(configV4)
    # bot_battle1v1(config, configV4)
    # bot_battle1v1(config, configV2, configV3, configV4)
    # imp_max_n_battle()
    # neat_v6_vs_imp_max_n(configV4)
    # final_tests_for_poster(config, configV2, configV3, configV4)
