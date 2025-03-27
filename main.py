# Copyright (C) 2025  Cooper Lockrey
# See LICENSE for more details.
import random

# probability for each type of node to appear
node_probabilities = {
    "monster": 0.45,
    "event": 0.22,
    "elite": 0.16,
    "rest_site": 0.12,
    "merchant": 0.05
}

def gen_node(level):
    # we loop until we get a valid node
    while True:
        # standard random level picker
        rand = random.random()
        cumulative_probability = 0
        for node_type, prob in node_probabilities.items():
            cumulative_probability += prob
            if rand <= cumulative_probability:
                # check if we violate rules of world gen, no adjacent elites, rest sites or merchants
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
    level = []
    # 15 nodes per level
    for i in range(15):
        # first node is always a monster
        if i == 0:
            level.append("monster")
        # first 5 nodes are never an elite or rest site
        elif i < 5:
            node = gen_node(level)
            # retry node gen if we get an elite or rest site
            while node == "elite" or node == "rest_site":
                node = gen_node(level)
            level.append(node)
        # 9th node is always treasure
        elif i == 8:
            level.append("treasure")
        # 14th node is never a rest site because the 15th is always a rest site
        elif i == 13:
            node = gen_node(level)
            # retry node gen if we get a rest site
            while node == "rest_site":
                node = gen_node(level)
            level.append(node)
        # 15th node is always a rest site
        elif i == 14:
            level.append("rest_site")
        else:
            # all other nodes are standardly generated
            level.append(gen_node(level))
    return level

def gen_world():
    world = []
    # 3 levels per world
    for _ in range(3):
        world += gen_map()
    return world

world = gen_world()
print(world)