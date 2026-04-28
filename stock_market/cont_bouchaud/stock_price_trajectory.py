# Script used to produce figure 6

import matplotlib.pyplot as plt
from tqdm import tqdm
from models import ContBouchaudModel

# Parameters found that fit real data
n_steps = 2500
n_traders = 5000
connectivity = 0.894 
prob = 0.05
liquidity = 1.2  

model = ContBouchaudModel(
    connectivity=connectivity,
    n_traders=n_traders,
    prob=prob,
    liquidity=liquidity,
    init_price=100
)

# Run the simulation
prices = [model.price]
for _ in tqdm(range(n_steps), desc="Simulating Stock Price"):
    p, _ = model.step()
    prices.append(p)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(prices, color='dodgerblue', linewidth=1.2)

plt.title(f'Simulated Stock Price Trajectory (ER Graph, $c={connectivity}$)', fontsize=12)
plt.xlabel('Time Step', fontsize=10)
plt.ylabel('Asset Price', fontsize=10)

plt.grid(True, which='major', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()