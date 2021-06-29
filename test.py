from kaggle_environments import make

env = make("hungry_geese", debug=True)

# Training agent in first position (player 1) against the default random agent.
#help(env)
trainer = env.train([None, "greedy", "greedy", "greedy"])
#help(trainer)

obs = trainer.reset()
for i in range(100):
    env.render()
    action = 'NORTH' # Action for the agent being trained.
    obs, reward, done, info = trainer.step(action)
    print("step : "+str(i))
    print(obs)
    print(reward)
    print(done)
    print(info)
    if done:
        obs = trainer.reset()