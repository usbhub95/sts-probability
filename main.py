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
    # generates a map which consists of 15 nodes, following some rules:
    # node 1 is always a monster, node 9 is always a treasure, node 14 is never a rest site and node 15 is always a rest site
    # nodes 1-5 can never be an elite or rest site
    # returns a list of 15 nodes

    # this is a list containing all the nodes for the current level
    level = []
    for i in range(15):
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
        else:
            level.append(gen_node(level))
    return level

def gen_world():
    # generates a world (list of 45 nodes which is just 3 levels joined together)
    # returns a list of 45 nodes (3 levels)

    world = []
    # 3 levels per world
    for _ in range(3):
        world += gen_map()
    return world

world = gen_world()
print(world)