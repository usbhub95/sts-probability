# Copyright (C) 2025  Cooper Lockrey
# See LICENSE for more details.
import random
from collections import Counter
from tqdm import tqdm

# probability for each type of node to appear
node_probabilities = {
    "monster": 0.45,
    "event": 0.22,
    "elite": 0.16,
    "rest_site": 0.12,
    "merchant": 0.05
}

def gen_node(level):
    # generates a node based on probabilites in "node_probabilites", following some rules:
    # elites, rest sites and merchants can never be adjacent to themselves
    # we take a list "level" so we can check the last node that was generated for our level
    # takes the current level list
    # returns a node

    # we loop until we get a valid node
    while True:
        # standard random level picker
        rand = random.random()
        cumulative_probability = 0
        for node_type, prob in node_probabilities.items():
            cumulative_probability += prob
            if rand <= cumulative_probability:
                # we check the most recent node generated for the current level by taking level[-1] and use it to make sure we arent violating the rules
                if level[-1] == "elite" or level[-1] == "rest_site" or level[-1] == "merchant":
                    if node_type != level[-1]:
                        # send it now that we have determined it doesnt violate rules
                        return node_type
                    else:
                        # retry if invalid
                        break
                else:
                    # send it because it cant possibly violate rules
                    return node_type

def gen_map():
    # generates a map which consists of 16 nodes, following some rules:
    # node 1 is always a monster, node 9 is always a treasure, node 14 is never a rest site, node 15 is always a rest site and node 16 is always the boss
    # nodes 1-5 can never be an elite or rest site
    # returns a list of 16 nodes

    # this is a list containing all the nodes for the current level
    level = []
    for i in range(16):
        if i == 0:
            level.append("monster")
        elif i < 5:
            node = gen_node(level)
            # retry node gen if we get an elite or rest site
            while node == "elite" or node == "rest_site":
                node = gen_node(level)
            level.append(node)
        elif i == 8:
            level.append("treasure")
        elif i == 13:
            node = gen_node(level)
            # retry node gen if we get a rest site
            while node == "rest_site":
                node = gen_node(level)
            level.append(node)
        elif i == 14:
            level.append("rest_site")
        elif i == 15:
            level.append("boss")
        else:
            level.append(gen_node(level))
    return level

def gen_world():
    # generates a world (list of 48 nodes which is just 3 levels joined together)
    # returns a list of 48 nodes (3 levels)

    world = []
    # 3 levels per world
    for _ in range(3):
        world += gen_map()
    return world

# card probabilites for each type of draw
monster_card_probs = {
    "rare": 3,
    "uncommon": 37,
    "common": 60
}
elite_card_probs = {
    "rare": 10,
    "uncommon": 40,
    "common": 50
}
merchant_card_probs = {
    "rare": 9,
    "uncommon": 37,
    "common": 54
}

# the offset value the game uses for altering the rare drop rate
offset = -5

def gen_card_probabilites(base_probabilities, offset):
    # this function generates a dict of probabilites based off an input set of probabilites and an offset value according to some rules the game uses
    #                          negative offset
    #         rare                 uncommon                     common
    # less likely until 0 | less likely if rare is 0 | always more likely until 100

    #                          positive offset
    #          rare                     uncommon                         common
    # more likely until 100 | less likely if common is at 0 | always less likely until 0

    # the function takes a dict of base probabilites and an offset value
    # it returns a dict of probabilites in the same format as the base probabilities
    uncommon_offset = 0
    rare_prob = base_probabilities["rare"]
    uncommon_prob = base_probabilities["uncommon"]
    common_prob = base_probabilities["common"]

    # this is the logic for altering the probabilities
    if offset * -1 >= rare_prob:
        # this handles the case of a negative offset that would take rare to negative
        common_offset = offset * -1
        uncommon_offset = offset + rare_prob
        rare_offset = rare_prob * -1
    elif offset <= 0:
        # this handles the case of a negative or 0 offset that wouldnt take rare to negative
        common_offset = offset * -1
        rare_offset = offset
    elif offset > 0 and offset <= common_prob:
        # this handles the case of a positive offset that wouldnt take uncommon down
        rare_offset = offset
        common_offset = offset * -1
    elif offset > common_prob:
        # this handles the case of a positive offset that would take uncommon down
        rare_offset = offset
        uncommon_offset = (offset - common_prob) * -1
        common_offset = common_prob * -1

    # we now adjust the probabilites how we want
    rare_prob += rare_offset
    uncommon_prob += uncommon_offset
    common_prob += common_offset

    # we return the new probs
    return {
        "rare": rare_prob / 100,
        "uncommon": uncommon_prob / 100,
        "common": common_prob / 100
    }

def gen_card(base_probabilities, offset):
    # this function generates a card based on the current probabilities with offset
    # it takes in a dict of probabilities and an offset
    # it returns a card type according to the probabilities

    # we get the probabilities for the draw
    card_probabilities = gen_card_probabilites(base_probabilities, offset)
    # same standard random choice 
    rand = random.random()
    cumulative_probability = 0
    for card_type, prob in card_probabilities.items():
        cumulative_probability += prob
        if rand <= cumulative_probability:
            return card_type

# lets try to make a game and generate cards for it
# scratch that, 1 million games
games = 1000000
rare_draws = 0
uncommon_draws = 0
common_draws = 0
colourless_rare_draws = 0
colourless_uncommon_draws = 0
for i in tqdm(range(games)):
    world = gen_world()
    for node in world:
        match node:
            case "monster":
                for i in range(3):
                    match gen_card(monster_card_probs, offset):
                        case "rare":
                            offset = -5
                            rare_draws += 1
                        case "uncommon":
                            uncommon_draws += 1
                        case "common":
                            offset += 1
                            common_draws += 1
            case "elite":
                for i in range(3):
                    match gen_card(elite_card_probs, offset):
                        case "rare":
                            offset = -5
                            rare_draws += 1
                        case "uncommon":
                            uncommon_draws += 1
                        case "common":
                            offset += 1
                            common_draws += 1
            case "merchant":
                for i in range(5):
                    match gen_card(merchant_card_probs, offset):
                        case "rare":
                            rare_draws += 1
                        case "uncommon":
                            uncommon_draws += 1
                        case "common":
                            common_draws += 1
                for i in range(2):
                    card = gen_card(merchant_card_probs, offset)
                    while card == "common":
                        card = gen_card(merchant_card_probs, offset)
                    match gen_card(merchant_card_probs, offset):
                        case "rare":
                            colourless_rare_draws += 1
                        case "uncommon":
                            colourless_uncommon_draws += 1
            case "boss":
                offset = -5
                for i in range(3):
                    rare_draws += 1

print([rare_draws/games, uncommon_draws/games, common_draws/games], [colourless_rare_draws/games, colourless_uncommon_draws/games])