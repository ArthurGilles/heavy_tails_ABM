# Script to produce Figure 4

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from models import ContBouchaudModel

c_values = np.linspace(0.1, 3.0, 40)
giant_cluster_fractions = []
n_agents = 100000

for c in tqdm(c_values, desc="Mapping Phase Transition"):
    model = ContBouchaudModel(connectivity=c, n_traders=n_agents, prob=0.05, liquidity=1.0)
    # Find the largest connected component
    largest_cc = max(model.clusters, key=len)
    giant_cluster_fractions.append(len(largest_cc) / n_agents)

plt.figure(figsize=(8, 5))
plt.plot(c_values, giant_cluster_fractions, marker='o', markersize=4, linestyle='-', color='indigo')
plt.axvline(x=1.0, color='red', linestyle='--', label='Critical Point ($c=1$)')
plt.title('Emergence of the Giant Cluster (ER Graph)')
plt.xlabel('Mean Degree / Connectivity ($c$)')
plt.ylabel('Fraction of Traders in Largest Cluster')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()