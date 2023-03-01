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
            self. observation_space : The space of observations: validators
        ----------
        """
        # ENVIRONMENT: The validators
        self.validator_size = validator_size # The size of the validators
        self.validators = [] # The list of the validators
        self.alpha = 1
        self.total_active_balance = 0
        self.proportion_of_honest = 0
        
        """
            matching from strategy to name:{0: "honest", 
                                            1: "malicious"}
            matching from status to name: {0: "propose",
                                           1: "vote"}
            So each validator has a strategy and an status.
        """

        # AGENT: The PoS Ethereum Blockchain, to learn the value of alpha
        # The action to learn: the value of alpha in penalty
        self.action_space = spaces.Box(-1, 1, shape=(1,), dtype=np.float32)

        self.observation_space = spaces.Box(0, 1, shape=(1,))

        self.window = None
        self.clock = None


        super(CustomEnv, self).__init__()

    def reset(self):
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
        
        for i in range(self.validator_size):
            self.proportion_of_honest += (self.validators[i].strategy == 0) / self.validator_size

        # Update the validators
        for i in range(self.validator_size):
            if i == proposer:
                self.validators[i].status = 0
            else:
                self.validators[i].status = 1
            self.validators[i].current_balance, self.validators[i].effective_balance = self.validators[i].get_balances(proportion_of_honest, self.alpha, self.total_active_balance)
            self.total_active_balance += self.validators[i].current_balance

        # Update the value of alpha in penalty
        self.alpha = self.alpha + action # Action is a float

        terminated = np.array_equal(sum(self._strategy_to_name == 1), 0)
        reward = self.proportion_of_honest

        observation = self._get_obs()
        info = self._get_info()

        # Update the strategies of validators
        probability = 0
        for i in range(self.validator_size):
            probability += self.validators[i].current_balance / self.total_active_balance
        
        for i in range(self.validator_size):
            self.validators[i].strategy = np.random.choice([0, 1], p=[1 - probability, probability])

        return observation, reward, terminated, False, info


    def render(self):
        """
        Render the environment.

        Parameters
        ----------
        mode : str
            The mode to render the environment in.
        """
        raise NotImplementedError

    def _get_obs(self):
        return {"validators": self.validators}

    def _get_info(self):
        return {"honest_proportion": sum(self._strategies == 0) / self.validator_size}