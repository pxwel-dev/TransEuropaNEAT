import random

from HumanPlayer import HumanPlayer
from NEAT_COMPLEX import NEATPlayer
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
            file = open("fitnessDataAveragesMean", 'a')
            file.write(str((sum(fitness) / len(fitness))) + "\n")
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
                    NEATPlayer("1", neat.nn.FeedForwardNetwork.create(playerGenomes[0], conf)),
                    NEATPlayer("2", neat.nn.FeedForwardNetwork.create(playerGenomes[1], conf)),
                    NEATPlayer("3", neat.nn.FeedForwardNetwork.create(playerGenomes[2], conf)),
                    NEATPlayer("4", neat.nn.FeedForwardNetwork.create(playerGenomes[3], conf)),
                    NEATPlayer("5", neat.nn.FeedForwardNetwork.create(playerGenomes[4], conf)),
                    NEATPlayer("6", neat.nn.FeedForwardNetwork.create(playerGenomes[5], conf))]
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
                      "Game statistic for game {2}/{10}:\n"
                      "=================================\n"
                      "| Name     | Fitness | Cities Left |Tracks Used | ColTracks Left | Skipped Turns | No Moves "
                      "Error Count |\n"
                      "| Player 1 |   {3}   |     {35}    |    {11}    |      {17}      |      {23}     |          "
                      "{29}        |\n"
                      "| Player 2 |   {4}   |     {36}    |    {12}    |      {18}      |      {24}     |          "
                      "{30}        |\n"
                      "| Player 3 |   {5}   |     {37}    |    {13}    |      {19}      |      {25}     |          "
                      "{31}        |\n"
                      "| Player 4 |   {6}   |     {38}    |    {14}    |      {20}      |      {26}     |          "
                      "{32}        |\n"
                      "| Player 5 |   {7}   |     {39}    |    {15}    |      {21}      |      {27}     |          "
                      "{33}        |\n"
                      "| Player 6 |   {8}   |     {40}    |    {16}    |      {22}      |      {28}     |          "
                      "{34}        |\n"
                      "=================================".format(count, int(len(genomes) / 6), j + 1,
                                                                 round(fitnessScore[0], 2),
                                                                 round(fitnessScore[1], 2),
                                                                 round(fitnessScore[2], 2),
                                                                 round(fitnessScore[3], 2),
                                                                 round(fitnessScore[4], 2),
                                                                 round(fitnessScore[5], 2),
                                                                 game.turn_count,
                                                                 NUMBER_OF_GAMES,
                                                                 game.get_players_post_game()[0].tracksUsed,
                                                                 game.get_players_post_game()[1].tracksUsed,
                                                                 game.get_players_post_game()[2].tracksUsed,
                                                                 game.get_players_post_game()[3].tracksUsed,
                                                                 game.get_players_post_game()[4].tracksUsed,
                                                                 game.get_players_post_game()[5].tracksUsed,
                                                                 game.get_players_post_game()[0].colouredTracks,
                                                                 game.get_players_post_game()[1].colouredTracks,
                                                                 game.get_players_post_game()[2].colouredTracks,
                                                                 game.get_players_post_game()[3].colouredTracks,
                                                                 game.get_players_post_game()[4].colouredTracks,
                                                                 game.get_players_post_game()[5].colouredTracks,
                                                                 game.get_players_post_game()[0].movesSkipped,
                                                                 game.get_players_post_game()[1].movesSkipped,
                                                                 game.get_players_post_game()[2].movesSkipped,
                                                                 game.get_players_post_game()[3].movesSkipped,
                                                                 game.get_players_post_game()[4].movesSkipped,
                                                                 game.get_players_post_game()[5].movesSkipped,
                                                                 # None,
                                                                 # None,
                                                                 # None,
                                                                 # None,
                                                                 # None,
                                                                 # None,
                                                                 game.get_players_post_game()[0].noMovesLeftErrors,
                                                                 game.get_players_post_game()[1].noMovesLeftErrors,
                                                                 game.get_players_post_game()[2].noMovesLeftErrors,
                                                                 game.get_players_post_game()[3].noMovesLeftErrors,
                                                                 game.get_players_post_game()[4].noMovesLeftErrors,
                                                                 game.get_players_post_game()[5].noMovesLeftErrors,
                                                                 len(game.get_players_post_game()[0].citiesToCapture),
                                                                 len(game.get_players_post_game()[1].citiesToCapture),
                                                                 len(game.get_players_post_game()[2].citiesToCapture),
                                                                 len(game.get_players_post_game()[3].citiesToCapture),
                                                                 len(game.get_players_post_game()[4].citiesToCapture),
                                                                 len(game.get_players_post_game()[5].citiesToCapture)))

            playerGenomes.clear()
    return genomes


def test_best_network(conf):
    f = open("NEAT-COMPLEX-V2.pickle", "rb")
    best_player = pickle.load(f)
    game = TransEuropa(
        [NEATPlayer("NeuralNetwork", neat.nn.FeedForwardNetwork.create(best_player, conf)), HumanPlayer("Pawel")],
        "classic.txt")
    game.play_game()


def run_neat(conf, name):
    # pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-71')
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

    config_path = os.path.join(local_dir, "NEAT_COMPLEX_Config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                           neat.DefaultSpeciesSet, neat.DefaultStagnation,
                           config_path)

    # run_neat(config, "NEAT-COMPLEX-V2.pickle")
    test_best_network(config)
