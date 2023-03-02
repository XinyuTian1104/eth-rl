import gym
from core.envs.rl_env import CustomEnv
import pytest


@pytest.mark.skip(reason="not implemented yet")
def test_env():
    env = CustomEnv()
    observation, info = env.reset()

    for _ in range(1000):
        # agent policy that uses the observation and info
        action = env.action_space.sample()
        observation, reward, terminated, info = env.step(action)

        if terminated:
            break

    env.close()
