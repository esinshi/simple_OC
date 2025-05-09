import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

env = gym.make("MiniGrid-Empty-5x5-v0", render_mode=None)
env = RGBImgPartialObsWrapper(env)
env = ImgObsWrapper(env)

model = PPO("CnnPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_minigrid")

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Mean reward: {mean_reward:.2f} ± {std_reward:.2f}")


