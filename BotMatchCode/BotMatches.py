from AllBots.NEAT_SIMPLEv6Player import NEATPlayer as NEAT_SIMPLEv6
from AllBots.NEAT_SIMPLEv5Player import NEATPlayer as NEAT_SIMPLEv5
from AllBots.NEAT_SIMPLEv4Player import NEATPlayer as NEAT_SIMPLEv4
from AllBots.NEAT_SIMPLEv3Player import NEATPlayer as NEAT_SIMPLEv3
from AllBots.NEAT_SIMPLEv2Player import NEATPlayer as NEAT_SIMPLEv2
from AllBots.NEAT_SIMPLEPlayer import NEATPlayer as NEAT_SIMPLE
from AllBots.ImperfectMaxN import ImpMaxNPlayer
from AllBots.ImperfectMaxNv2 import ImpMaxNPlayer as ImpMaxNPlayerV2
from AllBots.ImperfectMaxNv3 import ImpMaxNPlayer as ImpMaxNPlayerV3
from TransEuropa import TransEuropa
import neat
import os
from multiprocessing import Pool
import pickle
def neat_v6_vs_imp_max_n(conf):
    f = open("../AllBots/NEAT-SIMPLEv6.pickle", "rb")
    simpleV6 = pickle.load(f)

    pool = Pool(processes=6)

    p1 = pool.apply_async(func=imp_max_n1_neat_v6_4, args=(conf, simpleV6))
    p2 = pool.apply_async(func=imp_max_n1_neat_v6_6, args=(conf, simpleV6))
    p3 = pool.apply_async(func=imp_max_n2_neat_v6_4, args=(conf, simpleV6))
    p4 = pool.apply_async(func=imp_max_n2_neat_v6_6, args=(conf, simpleV6))
    p5 = pool.apply_async(func=imp_max_n3_neat_v6_4, args=(conf, simpleV6))
    p6 = pool.apply_async(func=imp_max_n3_neat_v6_6, args=(conf, simpleV6))

    pool.close()
    pool.join()


def final_tests_for_poster(conf, confV2, confV3, confV4):
    f = open("../AllBots/NEAT-SIMPLEv4.pickle", "rb")
    simpleV4 = pickle.load(f)

    pool = Pool(processes=6)

    p1 = pool.apply_async(func=imp_max_n_battle_4, args=())
    p2 = pool.apply_async(func=imp_max_n_battle_6, args=())
    p3 = pool.apply_async(func=imp_max_n3_neat_v4_4, args=(confV4, simpleV4))
    p4 = pool.apply_async(func=imp_max_n3_neat_v4_6, args=(confV4, simpleV4))
    p5 = pool.apply_async(func=neural_network_battle, args=(conf, confV2, confV3, confV4))

    pool.close()
    pool.join()


def imp_max_n_neat_v1(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLE":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLE (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLE (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLE":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLE (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLE (6 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLE":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLE (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLE (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLE("NEAT-SIMPLE", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLE":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLE (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLE (6 Players): " + str(scores))
    file.close()


def imp_max_n_neat_v2(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv2":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv2 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv2 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv2":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv2 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv2 (6 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv2":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv2 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv2 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv2("NEAT-SIMPLEv2", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv2":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv2 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv2 (6 Players): " + str(scores))
    file.close()


def imp_max_n_neat_v3(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv3":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv3 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv3 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv3":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv3 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv3 (6 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv3":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv3 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv3 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv3("NEAT-SIMPLEv3", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv3":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv3 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv3 (6 Players): " + str(scores))
    file.close()


def imp_max_n_neat_v4(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv4":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv4 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv4 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv4":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv4 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv4 (6 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv4":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv4 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv4 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv4":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv4 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv4 (6 Players): " + str(scores))
    file.close()


def imp_max_n_neat_v5(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv5":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv5 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv5 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv5":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv5 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv5 (6 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv5":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv5 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv5 (4 Players): " + str(scores))
    file.close()

    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv5("NEAT-SIMPLEv5", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv5":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv5 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv5 (6 Players): " + str(scores))
    file.close()


def imp_max_n1_neat_v6_4(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv6":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv6 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv6 (4 Players): " + str(scores))
    file.close()


def imp_max_n1_neat_v6_6(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayer("ImpMaxN-1"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv6":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs NEAT-SIMPLEv6 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs NEAT-SIMPLEv6 (6 Players): " + str(scores))
    file.close()


def imp_max_n2_neat_v6_4(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv6":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv6 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv6 (4 Players): " + str(scores))
    file.close()


def imp_max_n2_neat_v6_6(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-2":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv6":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-2 vs NEAT-SIMPLEv6 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-2 vs NEAT-SIMPLEv6 (6 Players): " + str(scores))
    file.close()


def imp_max_n3_neat_v6_4(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-3":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv6":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-3 vs NEAT-SIMPLEv6 (4 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-3 vs NEAT-SIMPLEv6 (4 Players): " + str(scores))
    file.close()


def imp_max_n3_neat_v6_6(conf, simple):
    scores = [0, 0]
    for i in range(0, 1000):
        game = TransEuropa([ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv6("NEAT-SIMPLEv6", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-3":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv6":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-3 vs NEAT-SIMPLEv6 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-3 vs NEAT-SIMPLEv6 (6 Players): " + str(scores))
    file.close()


def imp_max_n3_neat_v4_4(conf, simple):
    scores = [0, 0]
    for i in range(1, 1001):
        game = TransEuropa([ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-3":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv4":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-3 vs NEAT-SIMPLEv4 (4 Players): " + str(scores))
        if i == 1:
            print(scores)
    file = open("matchData", 'a')
    file.write("ImpMaxN-3 vs NEAT-SIMPLEv4 (4 Players): " + str(scores))
    file.close()


def imp_max_n3_neat_v4_6(conf, simple):
    scores = [0, 0]
    for i in range(1, 1001):
        game = TransEuropa([ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple),
                            ImpMaxNPlayerV3("ImpMaxN-3"),
                            NEAT_SIMPLEv4("NEAT-SIMPLEv4", neat.nn.FeedForwardNetwork.create(simple, conf), simple)]
                           , "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-3":
            scores[0] += 1
        elif game.get_winner() == "NEAT-SIMPLEv4":
            scores[1] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-3 vs NEAT-SIMPLEv4 (6 Players): " + str(scores))
        if i == 1:
            print(scores)
    file = open("matchData", 'a')
    file.write("ImpMaxN-3 vs NEAT-SIMPLEv4 (6 Players): " + str(scores))
    file.close()


def imp_max_n_battle_4():
    scores = [0, 0, 0]
    for i in range(1, 1001):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            ImpMaxNPlayerV2("ImpMaxN-2"),
                            ImpMaxNPlayerV3("ImpMaxN-3")], "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "ImpMaxN-2":
            scores[1] += 1
        elif game.get_winner() == "ImpMaxN-3":
            scores[2] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs ImpMaxN-2 vs ImpMaxN-3 (3 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs ImpMaxN-2 vs ImpMaxN-3 (3 Players): " + str(scores))
    file.close()


def imp_max_n_battle_6():
    scores = [0, 0, 0]
    for i in range(1, 1001):
        game = TransEuropa([ImpMaxNPlayer("ImpMaxN-1"),
                            ImpMaxNPlayerV2("ImpMaxN-2"), ImpMaxNPlayer("ImpMaxN-1"),
                            ImpMaxNPlayerV2("ImpMaxN-2"), ImpMaxNPlayerV3("ImpMaxN-3"),
                            ImpMaxNPlayerV3("ImpMaxN-3")], "../classic.txt")
        game.play_game()
        if game.get_winner() == "ImpMaxN-1":
            scores[0] += 1
        elif game.get_winner() == "ImpMaxN-2":
            scores[1] += 1
        elif game.get_winner() == "ImpMaxN-3":
            scores[2] += 1
        if i % 100 == 0:
            print(i, ": ImpMaxN-1 vs ImpMaxN-2 vs ImpMaxN-3 (6 Players): " + str(scores))
    file = open("matchData", 'a')
    file.write("ImpMaxN-1 vs ImpMaxN-2 vs ImpMaxN-3 (6 Players): " + str(scores))
    file.close()

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