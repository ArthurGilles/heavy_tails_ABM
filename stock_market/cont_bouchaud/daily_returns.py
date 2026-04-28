# Script to produce time series of the daily returns of some stocks, simulated 
# with our ContBouchaudModel class (ended up not being put in the report, but still
# interesting)

import matplotlib.pyplot as plt
from tqdm import tqdm
from models import ContBouchaudModel


n_steps = 1000
# 0.5: Sub-critical (Conspiracy), 1.0: Critical (Heavy Tails), 2.0: Super-critical (Catastrophe)
regimes = [0.5, 1.0, 2.0]
results = {}

for c in tqdm(regimes, desc="Simulating Regimes"):
    model = ContBouchaudModel(connectivity=c, n_traders=2000, prob=0.05, liquidity=2.0)
    prices, yields = [model.price], []
    for _ in range(n_steps):
        p, y = model.step()
        prices.append(p)
        yields.append(y)
    results[c] = {'prices': prices, 'yields': yields}

fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
titles = ['Sub-critical ($c=0.5$)', 'Critical ($c=1.0$)', 'Super-critical ($c=2.0$)']
colors = ['teal', 'darkorange', 'crimson']

for i, (c, data) in enumerate(results.items()):
    axes[i].plot(data['yields'], color=colors[i], linewidth=0.8)
    axes[i].set_title(titles[i])
    axes[i].set_ylabel('Returns')
    axes[i].grid(True, alpha=0.3)

axes[-1].set_xlabel('Time Step')
plt.tight_layout()
plt.show()