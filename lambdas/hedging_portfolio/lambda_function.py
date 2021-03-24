import numpy as np
import math
from datetime import datetime
from scipy.stats import norm

def bs_delta(S, K, sigma, r, T):    
    n_steps = S.shape[0]
    d1 = (np.log(S/K) + (0.5 * sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    DF = np.exp(-r * T)
    return DF * norm.cdf(d1)

    
def simulate_hedging_cost(S0, K, sigma, r, T, mu, n_steps):
    dt = 1. / n_steps
    dW = np.random.normal((mu - 0.5 * sigma ** 2) * dt,
        math.sqrt(dt) * sigma, n_steps-1)
    dW = np.insert(dW, 0, 0)

    S = S0 * np.exp(dW.cumsum())
    prev_S = np.roll(S, 1)

    t = T - np.linspace(0, 1-dt, n_steps-1)
    
    S_T = S[-1]
    V_T = max(S_T - K, 0)    
    delta = bs_delta(S[:-1], K, sigma, r, t)
    delta = np.append(delta, 0.)
    
    pos = delta
    pos[-1] = 0   
    prev_pos = np.roll(pos, 1)
    prev_pos[0] = 0

    pos_pnl = prev_pos * (S - prev_S)
    pos_pnl[0] = 0.
    return (pos_pnl.sum() - V_T) * math.exp(-r * T)

def lambda_handler(event, context):
    print(event)
    before = datetime.now()
    sim_kwargs = event['sim_kwargs']
    n_sims = sim_kwargs['n_sims']
    
    costs = [simulate_hedging_cost(**event['bs_kwargs']) \
        for _ in range(n_sims)]
        
    result = {
        'costs': costs,
    }
        
    timing = {
        'start': before.timestamp(),
        'end': datetime.now().timestamp(),
    }
    
    body = {
        'timing': timing,
        'result': result
    }
    
    return {
        'statusCode': 200,
        'body': body
    }
