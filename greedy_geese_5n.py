from kaggle_environments.envs.hungry_geese.hungry_geese import Observation, Configuration, Action, row_col, greedy_agent, adjacent_positions, translate, min_distance
from kaggle_environments import make
from random import choice, sample
"""
    Les IA de la serie 'GreedyAgent' cherchent avant tout à manger le plus de fruit possible
    cependant dès 'GreedyAgent2' l'ia cherche à le faire de manière plus sécurisé en fesant des choix qui minimise le risque de rencontre d'obstacle
    """
class GreedyAgent4n:

    def __init__(self, configuration: Configuration,n: int):
        self.configuration = configuration
        self.last_action = None
        self.n = n

    def __call__(self, observation: Observation):
        rows, columns = self.configuration.rows, self.configuration.columns

        food = observation.food #l'ensemble des fruits présent sur le tableau
        geese = observation.geese #l'ensemble des oies présentes sur le tableau
         #l'ensemble des oies présentes sur le tableau autre que l'oie controlée par l'IA
        
        #Risky move
        resky_move = self.createRiskTable(geese,food)
        
        # Move to the closest food
        position = geese[observation.index][0]
        actions_risk = self.riskProbability(resky_move,position,self.last_action,1,self.n)
        
        min_risk = min(actions_risk.values())
        actions = {
            action: min_distance(new_position, food, columns)
            for action in Action
            for new_position in [translate(position, action, columns, rows)]
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
        
    """
        Fonction qui crée un tableau de risque de présense d'un obstacle sur n cycle
    """
    def createRiskTable(self,geese,food):
        rows, columns = self.configuration.rows, self.configuration.columns
        
        #Création de tableaux
        opponents = [
            goose
            for index, goose in enumerate(geese)
            if index != observation.index and len(goose) > 0
        ]
        resky_move = [None] * (self.n+1) #Creation du tableau des risque 
        opponents_head = [None] * (self.n+1) #Creation d'un tableau contenant l'emplacement potentiel des têtes des oie
        
        #Iniatiasation des tableaux avec les valeurs actuels
        distFoodMin = min([min_distance(fruit,head) for head in opponents_head[0] for fruit in food])
        #À chaque case où se situe une oie on associe un risque de 1 et un emplacement relatif 
        #dans l'oie (1 pour la dernière case, 2 pour l'avant dernière etc.)
        resky_move[0] = {goose[i]: (len(goose)-i,1.0) for goose in geese for i in range(len(goose))} 
        
        #On mets chaque case ou se situe la tête d'un opposant dans le tableau
        opponents_head[0] = {opponent[0] for opponent in opponents}
        
        #Boucle pour estimer les risque de présence d'un obstable sur un case dans n cycle
        for i in range(1,self.n+1):

            
            resky_move[i] = {
            position: ((resky_move[i-1][position][0]-1,resky_move[i-1][position][1]) 
                        if resky_move[i-1][position][0] != 1 
                        else (1,resky_move[i-1][position][1]*0.5))
                        #Si la case est potentielement la dernière d'une oie alors on divise par deux le risque par rapport au cylce précédant 
                        #Sinon on diminue la distance avec la fin de l'oie de 1
            for position in resky_move[i-1].keys()
            }
            
            resky_move[i].update({
            opponent_head_adjacent: ((resky_move[i-1][opponent_head][0]+1,resky_move[i-1][opponent_head][1]*1/2) 
                                      if opponent_head in resky_move[i-1]
                                      else (1,1/2))
                                    #On divise le risque de présence d'un obtacle par deux par rapport à l'emplacement d'ont la case est adjacente
            for opponent_head in opponents_head[i-1]
            for opponent_head_adjacent in adjacent_positions(opponent_head, columns, rows)
            if opponent_head_adjacent not in resky_move[i-1] #On modifie unique si il n'est pas déjà définie
            })
            #Calcul des nouvels emplacement des têtes des oie adverse
            opponents_head[i] = {
                                opponent_head_adjacent 
                                for opponent_head in opponents_head[i-1]
                                for opponent_head_adjacent in adjacent_positions(opponent_head, columns, rows)
                                }
        return resky_move
    
    """
        Calcul les risque d'obstacle pour les differents mouvement
    """    
    def riskProbability(self,resky_move,position,last_action,start,end):
        rows, columns = self.configuration.rows, self.configuration.columns
        result = {}
        
        for action in [action for action in Action if last_action is None or action != last_action.opposite()]: #Pas de retour arière
            new_position = translate(position, action, columns, rows)
            risk = resky_move[start][new_position][1] if new_position in resky_move[start] else 0.0
            if(start != end and risk != 1): #Si la présence d'un obstacle n'est pas certaine 
                next_risks = self.riskProbability(resky_move,new_position,action,start+1,end)
                next_risk = min(next_risks.values())
                  
                #Permet de privilégier le chemun le plus long en cas de defaite inévitable 
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
    
def greedy_agent_45(obs, config):
    index = obs["index"]
    if index not in cached_greedy_agents_4n:
        cached_greedy_agents_4n[index] = GreedyAgent4n(Configuration(config),5)
    return cached_greedy_agents_4n[index](Observation(obs))