import gymnasium as gym
from gymnasium import spaces
import numpy as np

from validators import Validator

class CustomEnv(gym.Env):
    def __init__(self, validator_size = 100):
        """
        Initialize your custom environment.

        Parameters:
            self. validator_size : The size of the validators
            self. validators : The list of the validators
            self. action_space : The space of actions: reward, penalty
            self. observation_space : The space of observations: validators, proposing_order
        ----------
        """
        # ENVIRONMENT: The validators
        self.validator_size = validator_size # The size of the validators
        self.validators = [] # The list of the validators
        
        # The strategies of the validators
        # self.strategy_space = spaces.Discrete(2) # The space of strategies: malicious v.s. honest
        # self._strategy_to_name = {0: "honest", 
        #                           1: "malicious"} # The mapping from strategy to name
    
        # The status of the validators
        # self.status_spaces = spaces.Discrete(2) # The space of statuses: propose, vote, committee
        # self._status_to_name = {0: "propose", 
        #                         1: "vote"} # The mapping from status to name

        # So each validator has a strategy and an status

        # AGENT: The PoS Ethereum Blockchain, to learn the value of alpha
        # The action to learn: the value of alpha in penalty
        self.action_space = spaces.Box(-1, 1, shape=(1,), dtype=np.float32)

        self.observation_space = spaces.Box(0, 1, shape=(2,))

        self.window = None
        self.clock = None


        super(CustomEnv, self).__init__()

    def reset(self, seed = None, options = None):
        """
        Reset the environment and return an initial observation.

        Returns
        -------
        observation : numpy array
            The initial observation of the environment.
        """

        for i in range(self.validator_size):
            strategy = np.random.randint(0, 2)
            status = 1
            current_balance = 32
            effective_balance = 32
            self.validators.append(Validator(strategy, status, current_balance, effective_balance))
        
        # # Generate the proposing order
        # proposing_order = np.random.permutation(self.validator_size)

        # Generate the initial value of alpha
        self.alpha = 1
        self.total_active_balance = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info


    def step(self, action):
        """
        Take a step in the environment.

        Parameters
        ----------
        action : int
            The action to take in the environment.

        Returns
        -------
        observation : numpy array
            The new observation of the environment after taking the action.
        reward : float
            The reward obtained after taking the action.
        done : bool
            Whether the episode has ended or not.
        info : dict
            Additional information about the step.
        """

        # Update the environment: validators
        # Generate a proposer
        proposer = np.random.randint(0, self.validator_size)
        
        proportion_of_honest = 0
        for i in range(self.validator_size):
            proportion_of_honest += (self.validators[i].strategy == 0) / self.validator_size

        # Update the validators
        for i in range(self.validator_size):
            if i == proposer:
                self.validators[i].status = 0
            else:
                self.validators[i].status = 1

            if self.validators[i].strategy == 0:
                # generate random number 0 and 1 with probability 0.7 and 0.3
                self.validators[i].strategy = np.random.choice([0, 1], p=[0.7, 0.3])
            else:
                pass
            self.validators[i].current_balance, self.validators[i].effective_balance = self.validators[i].get_balance(proportion_of_honest, self.alpha, self.total_active_balance)
            self.total_active_balance += self.validators[i].current_balance

        # Update the value of alpha in penalty
        self.alpha = self.alpha + action # Action is a float

        terminated = np.array_equal(sum(self._strategy_to_name == 1), 0)
        reward = proportion_of_honest

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info


    def render(self, mode='human'):
        """
        Render the environment.

        Parameters
        ----------
        mode : str
            The mode to render the environment in.
        """
        raise NotImplementedError

def _get_obs(self):
    return {"validators": self._strategies,
            "proposing_order": self._proposing_order}

def _get_info(self):
    return {
        "honest_proportion": sum(self._strategies == 0) / self.validator_size,
    }