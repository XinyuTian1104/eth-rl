import gymnasium as gym
from gymnasium import spaces
import numpy as np

def _get_obs(self):
    return {"validators": self._strategies,
            "proposing_order": self._proposing_order}

def _get_info(self):
    return {
        "honest_proportion": sum(self._strategies == 0) / self.validator_size,
    }

class CustomEnv(gym.Env):
    def __init__(self):
        """
        Initialize your custom environment.

        Parameters:
            self. validator_size : The size of the validators
            self. strategy_space : The space of strategies: malicious v.s honest
            self. _strategy_to_name : The mapping from strategy to name
            self. status_spaces : The space of statuses: propose, vote, committee
            self. _status_to_name : The mapping from status to name
            self. action_space : The space of actions: reward, penalty
            self. _action_to_name : The mapping from action to name
            self. observation_space : The space of observations: validators, proposing_order
        ----------
        """
        # ENVIRONMENT: The validators
        self.validator_size = 100 # The size of the validators
        
        # The strategies of the validators
        self.strategy_space = spaces.Discrete(2) # The space of strategies: malicious v.s. honest
        self._strategy_to_name = {0: "honest", 
                                  1: "malicious"} # The mapping from strategy to name
    
        # The status of the validators
        self.status_spaces = spaces.Discrete(2) # The space of statuses: propose, vote, committee
        self._status_to_name = {0: "propose", 
                                1: "vote"} # The mapping from status to name

        # So each validator has a strategy and an status


        # AGENT: The PoS Ethereum Blockchain, to learn the reward and penalty policies
        self.action_space = spaces.Discrete(2)
        self._action_to_alpha = {0: 0,
                                1: 0} # The mapping from action to name
        
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
 

        # Generate the strategies of the validators
        self._strategies = self.np_random.randint(
            0, self.strategy_space.n, size=self.validator_size
        )

        # Generate the proposing order
        self._proposing_order = self.np_random.permutation(self.validator_size)

        # Generate the initial value of alpha
        """
            Question to be answered:
            How to generate the initial value of alpha?
        """
        self._alpha_penalty = 1

        observation = self._get_obs()
        info = self._get_info()

        return observation, info


    def step(self, action, validator_action, strategy, status):
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

        # Get the action of the PoS Ethereum: reward or penalty
        action = self._action_to_alpha[validator_action]

        # Update the value of alpha in penalty
        self._alpha_penalty = self._alpha_penalty + action # Action is a float

        terminated = np.array_equal(sum(self._strategy_to_name == 1), 0)
        reward = sum(self._strategy_to_name == 0) / self.validator_size

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
