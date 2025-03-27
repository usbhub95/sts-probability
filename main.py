# Copyright (C) 2025  Cooper Lockrey
# See LICENSE for more details.
import random

node_probabilities = {
    "monster": 0.45,
    "event": 0.22,
    "elite": 0.16,
    "rest_site": 0.12,
    "merchant": 0.05
}

def gen_node(level):
    while True:
        rand = random.random()
        cumulative_probability = 0
        for node_type, prob in node_probabilities.items():
            cumulative_probability += prob
            if rand <= cumulative_probability:
                if level[-1] == "elite" or level[-1] == "rest_site" or level[-1] == "merchant":
                    if node_type != level[-1]:
                        return node_type
                    else:
                        break
                else:
                    return node_type

def gen_map():
    level = []
    for i in range(15):
        if i == 0:
            level.append("monster")
        elif i < 5:
            node = gen_node(level)
            while node == "elite" or node == "rest_site":
                node = gen_node(level)
            level.append(node)
        elif i == 8:
            level.append("treasure")
        elif i == 13:
            node = gen_node(level)
            while node == "rest_site":
                node = gen_node(level)
            level.append(node)
        elif i == 14:
            level.append("rest_site")
        else:
            level.append(gen_node(level))
    return level

def gen_world():
    world = []
    for _ in range(3):
        world += gen_map()
    return world

world = gen_world()
print(world)