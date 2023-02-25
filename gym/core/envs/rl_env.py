import gymnasium as gym
from gymnasium import spaces

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

        Parameters
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

        # So every validator has a strategy and an status

        # AGENT: The PoS Ethereum Blockchain, to learn the reward and penalty policies
        self.action_space = spaces.Discrete(2)
        self._action_to_name = {0: "reward",
                                1: "penality"} # The mapping from action to name
        
        self.observation_space = spaces.Box(0, 1, shape=(2,))


        self.window = None
        self.clock = None


        super(CustomEnv, self).__init__()
        raise NotImplementedError

    def reset(self, seed = None, options = None):
        """
        Reset the environment and return an initial observation.

        Returns
        -------
        observation : numpy array
            The initial observation of the environment.
        """

        # We need the following line to seed self.np_random
        super().reset(seed = seed)

        # Generate the strategies of the validators
        self._strategies = self.np_random.randint(
            0, self.strategy_space.n, size=self.validator_size
        )

        # Generate the proposing order
        self._proposing_order = self.np_random.permutation(self.validator_size)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

        raise NotImplementedError

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
        raise NotImplementedError

    def render(self, mode='human'):
        """
        Render the environment.

        Parameters
        ----------
        mode : str
            The mode to render the environment in.
        """
        raise NotImplementedError

    def close(self):
        """
        Clean up any resources used by the environment.
        """
        raise NotImplementedError
