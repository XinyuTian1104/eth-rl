import gym


class CustomEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        """
        Initialize your custom environment.

        Parameters
        ----------
        """
        super(CustomEnv, self).__init__()
        raise NotImplementedError

    def reset(self):
        """
        Reset the environment and return an initial observation.

        Returns
        -------
        observation : numpy array
            The initial observation of the environment.
        """
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
