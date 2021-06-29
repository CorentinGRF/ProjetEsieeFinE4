from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, random_agent

class AleaAgent2:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.last_action = None

    def __call__(self, observation: Observation):
        action = choice([action for action in Action if(self.last_action == None or action !=  self.last_action.opposite())])
        #print("==Action_choice==")
        #print(self.last_action)
        #print(action)
        self.last_action = action
        return action.name

cached_alea_agents_2 = {}

def alea_agent_2(obs, config):
    index = obs["index"]
    if index not in cached_alea_agents_2:
        cached_alea_agents_2[index] = AleaAgent2(Configuration(config))
    return cached_alea_agents_2[index](Observation(obs))
    return last_action