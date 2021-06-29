from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, greedy_agent, adjacent_positions, translate, min_distance
from kaggle_environments import make
from random import choice, sample
import numpy as np

class GreedyAgent4n:
    def __init__(self, configuration: Configuration,n: int):
        self.configuration = configuration
        self.last_action = None
        self.n = n

    def __call__(self, observation: Observation):
        rows, cols = self.configuration.rows, self.configuration.columns

        food = observation.food
        geese = observation.geese
        opponents = [
            goose
            for index, goose in enumerate(geese)
            if index != observation.index and len(goose) > 0
        ]
        #------------------
        nbr_geese = len(observation.geese)
        
        geese2    = np.zeros((self.n+1,nbr_geese-1,rows,cols))
        heads     = np.zeros((self.n+1,nbr_geese-1,rows,cols))
        foods     = np.zeros((self.n+1,rows,cols))
            
        for goose in observation.geese: 
            for pos in goose : geese2[0,0,pos//cols,pos%cols ] = 1
            
        for goose in observation.geese: heads[0,0,pos//cols,pos%cols ] = 1

        for pos in observation.food: foods[0,pos//cols,pos%cols] = 1
        
        #n/len(nbr_geese)
        #n%len(nbr_geese)
        print(geese2)
        print(heads)
        print(foods)
        print("-------------------")
        #-------------------
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
            for opponent_head_adjacent in adjacent_positions(opponent_head, cols, rows)
            if opponent_head_adjacent not in resky_move[i-1]
            })
            opponents_head[i] = {
                                opponent_head_adjacent 
                                for opponent_head in opponents_head[i-1]
                                for opponent_head_adjacent in adjacent_positions(opponent_head, cols, rows)
                                }

        # Move to the closest food
        position = geese[observation.index][0]
        actions_risk = self.riskProbability(resky_move,position,self.last_action,1,self.n)
        
        min_risk = min(actions_risk.values())
        actions = {
            action: min_distance(new_position, food, cols)
            for action in Action
            for new_position in [translate(position, action, cols, rows)]
            if (action in actions_risk and actions_risk[action] == min_risk)
            }
        action = min(actions, key=actions.get)
        self.last_action = action
        #print("----------")
        #print("choice")
        #print(action)
        #print(min_risk)
        #print(observation.index)
        return action.name
    
    def riskProbability(self,resky_move,position,last_action,start,end):
        rows, cols = self.configuration.rows, self.configuration.columns
        result = {}
        for action in [action for action in Action if last_action is None or action != last_action.opposite()]:
            new_position = translate(position, action, cols, rows)
            risk = resky_move[start][new_position][1] if new_position in resky_move[start] else 0.0
            if(start != end and risk != 1):
                next_risks = self.riskProbability(resky_move,new_position,action,start+1,end)
                next_risk = min(next_risks.values())
                  
                if next_risk < 1 :
                    risk = next_risk if risk < next_risk else risk
                elif next_risk == end :
                    risk = risk + (end - start)
                else :
                    risk = next_risk if risk < next_risk%1 else next_risk//1 + risk
                 
            elif risk == 1 :
                risk = end
            result[action] = risk
        return result
        
cached_greedy_agents_4n = {}


def greedy_agent_41(obs, config):
    index = obs["index"]
    if index not in cached_greedy_agents_4n:
        cached_greedy_agents_4n[index] = GreedyAgent4n(Configuration(config),1)
    return cached_greedy_agents_4n[index](Observation(obs))
    
def greedy_agent_42(obs, config):
    index = obs["index"]
    if index not in cached_greedy_agents_4n:
        cached_greedy_agents_4n[index] = GreedyAgent4n(Configuration(config),2)
    return cached_greedy_agents_4n[index](Observation(obs))
    
def greedy_agent_43(obs, config):
    index = obs["index"]
    if index not in cached_greedy_agents_4n:
        cached_greedy_agents_4n[index] = GreedyAgent4n(Configuration(config),3)
    return cached_greedy_agents_4n[index](Observation(obs))
    
def greedy_agent_44(obs, config):
    index = obs["index"]
    if index not in cached_greedy_agents_4n:
        cached_greedy_agents_4n[index] = GreedyAgent4n(Configuration(config),4)
    return cached_greedy_agents_4n[index](Observation(obs))
    
def greedy_agent_45(obs, config):
    index = obs["index"]
    if index not in cached_greedy_agents_4n:
        cached_greedy_agents_4n[index] = GreedyAgent4n(Configuration(config),5)
    return cached_greedy_agents_4n[index](Observation(obs))