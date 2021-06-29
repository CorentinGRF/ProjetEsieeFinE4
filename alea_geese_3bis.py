from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, greedy_agent, adjacent_positions, translate, min_distance
from kaggle_environments import make
from random import choice, sample

class AleaAgent3bis:
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

        #Risky move
        resky_move = {position: 1.0 for goose in geese for position in goose if position != goose[-1]}
        
         # Don't move adjacent to any heads
        resky_move.update({
            opponent_head_adjacent: 1/3
            for opponent in opponents
            for opponent_head in [opponent[0]]
            for opponent_head_adjacent in adjacent_positions(opponent_head, columns, rows)
            if not opponent_head_adjacent in resky_move
        })
        
        # Do the safiest action
        position = geese[observation.index][0]
        actions = {
        
            action: (resky_move[new_position] if new_position in resky_move else 0.0)
            for action in Action
            for new_position in [translate(position, action, columns, rows)]
            if (self.last_action is None or action != self.last_action.opposite())
            
        }
        
        min_value = min(actions.values())
        sefiest_actions = [action for action in actions.keys() if actions[action] == min_value]
        action = choice(sefiest_actions)
        self.last_action = action
        print("choice")
        print(action)
        print(actions[action])
        return action.name


cached_alea_agents_3bis = {}


def alea_agent_3bis(obs, config):
    index = obs["index"]
    if index not in cached_alea_agents_3bis:
        cached_alea_agents_3bis[index] = AleaAgent3bis(Configuration(config))
    return cached_alea_agents_3bis[index](Observation(obs))
    return last_action
