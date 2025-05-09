import crafter
import gymnasium as gym
import gym.wrappers
from stable_baselines3 import PPO

env = crafter.Env()
env = gym.wrappers.RecordEpisodeStatistics(env)
model = PPO("CnnPolicy", env, verbose=1)
model.learn(total_timesteps=200_000)
model.save("ppo_crafter")

eval_env = crafter.Env()
obs = eval_env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = eval_env.step(action)
    done = terminated or truncated
    eval_env.render()
