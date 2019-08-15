import torch
import numpy as np

from collections import deque

def run_gym(env, get_action=None, max_t=200):
    
    if get_action is None:
        get_action = lambda _: env.action_space.sample()
        
    state = env.reset()
    env.render()
    
    for i in range(max_t):
        action = get_action(state)
        state, reward, done, _ = env.step(action)
        env.render()
    
        if done: break
         
    env.close()

def train_agent(agent, env, n_episodes=2000, max_t=1000, eps_start=1.0, eps_end=0.01, eps_decay=0.995):
    """Deep Q-Learning training
    
    Params
    ======
        env (Environment): OpenAI Gym environment https://gym.openai.com/envs
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    
    scores = []                        # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start                    # initialize epsilon
    
    for i_episode in range(1, n_episodes+1):
        state = env.reset()
        score = 0
        for t in range(max_t):
            action = agent.act(state, eps)
            next_state, reward, done, _ = env.step(action)
            agent.step(state, action, reward, next_state, done)
            state = next_state
            score += reward
            
            if done: break
        
        scores_window.append(score)       # save most recent score
        scores.append(score)              # save most recent score
        eps = max(eps_end, eps_decay*eps) # decrease epsilon
        
        print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)), end="")
        
        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)))
            
        if np.mean(scores_window)>=200.0:
            print('\nEnvironment solved in {:d} episodes!'.format(i_episode-100))
            print('\nAverage Score: {:.2f}'.format(np.mean(scores_window)))
            
            torch.save(agent.qnetwork_local.state_dict(), 'checkpoint.pth')
            
            break
        
    return scores