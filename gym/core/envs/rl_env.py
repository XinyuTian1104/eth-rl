import datetime
import json
import os

import numpy as np
from core.envs.validators import Validator

import gym
from gym import spaces


class CustomEnv(gym.Env):
    def __init__(self, validator_size=100):
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
        self.validator_size = validator_size  # The size of the validators
        self.validators = []  # The list of the validators
        self.alpha = 1
        self.total_active_balance = 0
        self.proportion_of_honest = 0
        self.counter = 0

        # create the log directory if not exist
        if not os.path.exists("logs"):
            os.makedirs("logs")
        # create logging file with timestamp
        self.log_file = open(
            "logs/log_" + str(datetime.datetime.now()) + ".txt", "w")
        # create the file and make it empty
        self.log_file.write("")

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

        # self.observation_space = spaces.Box(0, 1, shape=(1,))
        self.observation_space = spaces.Dict(
            {"honest_proportion": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
             "target_honest_proportion": spaces.Box(0, 1, shape=(1,), dtype=np.float32)},
        )

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
            # if i < self.validator_size / 2:
            #     strategy = 0
            # else:
            #     strategy = 1
            strategy = np.random.randint(0, 2)
            status = 1
            current_balance = 32
            effective_balance = 32
            self.validators.append(
                Validator(strategy, status, current_balance, effective_balance))
            # print(f"validator {i} has strategy {strategy}, status {status}, current balance {current_balance}, and effective balance {effective_balance}.")

        proportion = 0
        for i in range(self.validator_size):
            proportion += (self.validators[i].strategy ==
                           0) / self.validator_size
        self.initial_honest_proportion = proportion
        # print(f"The initial proportion of honest: {self.proportion_of_honest}.")

        # Generate the initial value of alpha
        self.alpha = 1
        self.total_active_balance = 32 * self.validator_size

        observation = self._get_obs()
        info = self._get_info()

        self.counter = 0

        # return observation
        return observation

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

        proportion = 0
        for i in range(self.validator_size):
            proportion += (self.validators[i].strategy ==
                           0) / self.validator_size
        self.proportion_of_honest = proportion
        # print("proportion_of_honest: ", self.proportion_of_honest)

        # Update the validators
        for i in range(self.validator_size):
            if i == proposer:
                self.validators[i].status = 0
            else:
                self.validators[i].status = 1
            self.validators[i].update_balances(
                self.proportion_of_honest, self.alpha, self.total_active_balance)
            # print(f"validator {i} current_balance: ", self.validators[i].current_balance)
            # print(f"total_active_balance for round {i}: ", self.total_active_balance)

        total_active_balance = 0
        for i in range(self.validator_size):
            total_active_balance = total_active_balance + \
                self.validators[i].current_balance
        self.total_active_balance = total_active_balance
        # print(f"total_active_balance: ", self.total_active_balance)

        # Update the value of alpha in penalty
        self.alpha = self.alpha + action[0]  # Action is a float

        # terminated = np.array_equal(self.proportion_of_honest, 1)
        reward = self.proportion_of_honest

        observation = self._get_obs()

        info = self._get_info()

        # Update the strategies of validators
        probability = 0
        for i in range(self.validator_size):
            if self.validators[i].strategy == 0:
                probability += self.validators[i].current_balance / \
                    self.total_active_balance
            else:
                pass
            # print(f"validator {i} has current balance: ", self.validators[i].current_balance)
            # print(f"total_active_balance: ", self.total_active_balance)
        # print("probability: ", probability)

        terminated = False
        if self.proportion_of_honest == 1:
            terminated = True
        elif probability >= 1:
            terminated = True

        payload = self.render()
        self.log_file.write(str(payload) + "\n")

        if terminated:
            return observation, reward, terminated, info

        for i in range(self.validator_size):
            self.validators[i].strategy = np.random.choice(
                [0, 1], p=[probability, 1-probability])
        # log observation
        with open("observation.txt", "a") as f:
            f.write(str(observation) + "\n")

        # counter increment
        self.counter += 1

        return observation, reward, terminated, info

    def render(self):
        """
        Render the environment.

        Parameters
        ----------
        mode : str
            The mode to render the environment in.
        """
        payload = dict(
            alpha=self.alpha,
            proportion_of_honest=self.proportion_of_honest,
            rounds=self.counter,
            initial_honest_proportion=self.initial_honest_proportion,
        )
        return payload

    def _get_obs(self):
        return {"honest_proportion": self.proportion_of_honest,
                "target_honest_proportion": 1}

    def _get_info(self):
        return {"the honest proportion": self.proportion_of_honest}
