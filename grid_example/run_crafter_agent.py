import crafter
import imageio as imageio
from stable_baselines3 import PPO

# Load the trained model
model = PPO.load("ppo_crafter")

# Create environment (no render_mode arg here)
env = crafter.Env()
obs = env.reset()
done = False

frames = []
obs = env.reset()
done = False

# Run the agent
while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    frame = env.render()
    frames.append(frame)

imageio.mimsave("crafter_agent_run.mp4", frames, fps=10)
