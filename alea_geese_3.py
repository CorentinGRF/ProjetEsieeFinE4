from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, greedy_agent, adjacent_positions, translate, min_distance
from kaggle_environments import make
from random import choice, sample

class AleaAgent3:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.last_action = None

    def __call__(self, observation: Observation):
        rows, columns = self.configuration.rows, self.configuration.columns

        food = observation.food
        geese = observation.geese
        opponents = [
            goose
            for index, goose in enumerate(geese)
            if index != observation.index and len(goose) > 0
        ]

        # Don't move adjacent to any heads
        head_adjacent_positions = {
            opponent_head_adjacent
            for opponent in opponents
            for opponent_head in [opponent[0]]
            for opponent_head_adjacent in adjacent_positions(opponent_head, columns, rows)
        }
        # Don't move into any bodies
        bodies = {position for goose in geese for position in goose}

        # Move to the closest food
        position = geese[observation.index][0]
        actions_1 = [
            action
            for action in Action
            for new_position in [translate(position, action, columns, rows)]
            if (
                new_position not in head_adjacent_positions and
                new_position not in bodies and
                (self.last_action is None or action != self.last_action.opposite())
            )
        ]
        actions_2 = [
            action
            for action in Action
            for new_position in [translate(position, action, columns, rows)]
            if (
                new_position not in bodies and
                (self.last_action is None or action != self.last_action.opposite())
            )
        ]
        if any(actions_1):
            action = choice(actions_1)
        elif any(actions_2):
            action = choice(actions_2)
        else: 
            action = choice([action for action in Action])
        self.last_action = action
        return action.name


cached_alea_agents_3 = {}

def alea_agent_3(obs, config):
    index = obs["index"]
    if index not in cached_alea_agents_3:
        cached_alea_agents_3[index] = AleaAgent3(Configuration(config))
    return cached_alea_agents_3[index](Observation(obs))
    return last_action
