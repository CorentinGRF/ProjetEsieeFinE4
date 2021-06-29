from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, greedy_agent, adjacent_positions, translate, min_distance
from kaggle_environments import make
from random import choice, sample

class FeardyAgent1n:
    def __init__(self, configuration: Configuration,n: int):
        self.configuration = configuration
        self.last_action = None
        self.n = n

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
        resky_move = [None] * (self.n+1)
        opponents_head = [None] * (self.n+1)
        resky_move[0] = {goose[i]: (len(goose)-i,1.0) for goose in geese for i in range(len(goose))}
        opponents_head[0] = {opponent[0] for opponent in opponents}
        
         # Don't move adjacent to any heads
        
        for i in range(1,self.n+1):

            resky_move[i] = {
            position: (resky_move[i-1][position][0],resky_move[i-1][position][1]) 
            for position in resky_move[i-1].keys()
            }
            resky_move[i].update({
            opponent_head_adjacent: ((resky_move[i-1][opponent_head][0]+1,resky_move[i-1][opponent_head][1]*1/2) if opponent_head in resky_move[i-1] else (1,1/2))
            for opponent_head in opponents_head[i-1]
            for opponent_head_adjacent in adjacent_positions(opponent_head, columns, rows)
            if opponent_head_adjacent not in resky_move[i-1]
            })
            opponents_head[i] = {
                                opponent_head_adjacent 
                                for opponent_head in opponents_head[i-1]
                                for opponent_head_adjacent in adjacent_positions(opponent_head, columns, rows)
                                }

        # Move to the closest food
        position = geese[observation.index][0]
        actions_risk = self.riskProbability(resky_move,position,self.last_action,1)
        min_risk = min(actions_risk.values())
        actions = {
            action: min_distance(new_position, food, columns)
            for action in Action
            for new_position in [translate(position, action, columns, rows)]
            if (action in actions_risk and actions_risk[action] == min_risk)
            }
            
        if(len(geese[observation.index]) > 1):
            action = choice(list(actions))
        else:
            action = min(actions, key=actions.get)
        
        self.last_action = action
        return action.name
        
    def riskProbability(self,resky_move,position,last_action,i):
        rows, columns = self.configuration.rows, self.configuration.columns
        result = {}
        for action in [action for action in Action if last_action is None or action != last_action.opposite()]:
            new_position = translate(position, action, columns, rows)
            risk = resky_move[i][new_position][1] if new_position in resky_move[i] else 0.0
            if(i != len(resky_move)-1 and risk != 1):
                next_risks = self.riskProbability(resky_move,new_position,action,i+1)
                next_risk = min(next_risks.values())
                risk = next_risk if risk < next_risk else risk
            result[action] = risk
        return result
cached_feardy_agents_1n = {}


def feardy_agent_11(obs, config):
    index = obs["index"]
    if index not in cached_feardy_agents_1n:
        cached_feardy_agents_1n[index] = FeardyAgent1n(Configuration(config),1)
    return cached_feardy_agents_1n[index](Observation(obs))

def feardy_agent_12(obs, config):
    index = obs["index"]
    if index not in cached_feardy_agents_1n:
        cached_feardy_agents_1n[index] = FeardyAgent1n(Configuration(config),1)
    return cached_feardy_agents_1n[index](Observation(obs))

def feardy_agent_13(obs, config):
    index = obs["index"]
    if index not in cached_feardy_agents_1n:
        cached_feardy_agents_1n[index] = FeardyAgent1n(Configuration(config),1)
    return cached_feardy_agents_1n[index](Observation(obs))

def feardy_agent_14(obs, config):
    index = obs["index"]
    if index not in cached_feardy_agents_1n:
        cached_feardy_agents_1n[index] = FeardyAgent1n(Configuration(config),1)
    return cached_feardy_agents_1n[index](Observation(obs))

def feardy_agent_15(obs, config):
    index = obs["index"]
    if index not in cached_feardy_agents_1n:
        cached_feardy_agents_1n[index] = FeardyAgent1n(Configuration(config),1)
    return cached_feardy_agents_1n[index](Observation(obs))