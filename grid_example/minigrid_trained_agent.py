import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper
from stable_baselines3 import PPO

# Load environment and model
env = gym.make("MiniGrid-Empty-5x5-v0", render_mode="human")
env = RGBImgPartialObsWrapper(env)
env = ImgObsWrapper(env)
model = PPO.load("ppo_minigrid")

# Run one episode
obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    print("Action:", action)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    print(f"Reward: {reward}")
    env.render()
