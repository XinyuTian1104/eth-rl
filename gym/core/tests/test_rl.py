import os

import matplotlib.pyplot as plt
from core.envs.rl_env import CustomEnv
from core.utils.helper_functions import SaveOnBestTrainingRewardCallback
from stable_baselines3 import A2C
from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import plot_results

EPOCHS = 30


def test_a2c():
    env = CustomEnv()

    # Create log dir
    log_dir = "tmp/"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # Create and wrap the environment
    env = Monitor(env, log_dir)

    timesteps = 32 * (2 ** 8)

    model = A2C("MultiInputPolicy", env, verbose=1)
    callback = SaveOnBestTrainingRewardCallback(
        check_freq=1000, log_dir=log_dir)
    model.learn(total_timesteps=timesteps,
                progress_bar=True, callback=callback)
    model.save("models/a2c")

    plot_results([log_dir], timesteps,
                 results_plotter.X_TIMESTEPS, "A2C")
    plt.savefig("results/a2c.png")
    plt.show()
