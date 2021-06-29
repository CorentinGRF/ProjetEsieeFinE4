from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, random_agent

def agent(obs_dict, config_dict):
    """default random_agent"""
    return random_agent(obs_dict, config_dict)
    
    