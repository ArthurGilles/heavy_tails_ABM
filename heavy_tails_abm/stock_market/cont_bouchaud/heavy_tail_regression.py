# Script used to produce figure 5

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from tqdm import tqdm
from models import ContBouchaudModel

# Simulate a large dataset
model = ContBouchaudModel(connectivity=0.894, n_traders=5000, prob=0.05, liquidity=1.2)
yields = []
for _ in tqdm(range(5000), desc="Generating Calibration Data"):
    _, y = model.step()
    if y != 0: # Ignore zero-return days
        yields.append(np.abs(y))

sorted_yields = np.sort(yields)
ccdf = 1.0 - np.arange(1, len(sorted_yields) + 1) / len(sorted_yields)

# Tail thresholsd (where to do the regression)
threshold_low = np.percentile(sorted_yields, 80)
threshold_high = np.percentile(sorted_yields, 98)

mask = (sorted_yields > threshold_low) & (sorted_yields < threshold_high)
x_tail = sorted_yields[mask]
y_tail = ccdf[mask]

# linear regression in log-log 
log_x = np.log10(x_tail)
log_y = np.log10(y_tail)
slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)

alpha_estimate = -slope

plt.figure(figsize=(8, 6))
plt.plot(sorted_yields, ccdf, color='grey', marker='.', linestyle='none', markersize=2, label='Simulated Data')

# Plot the regression
fit_x = np.linspace(threshold_low, threshold_high, 100)
fit_y = (10**intercept) * (fit_x**slope)
plt.plot(fit_x, fit_y, color='black', linewidth=2, label=f'Regression Fit $\\alpha \\approx {alpha_estimate:.2f}$')

plt.xscale('log')
plt.yscale('log')
plt.title('Tail Exponent Estimation (S&P 500 Calibration)')
plt.xlabel('Absolute Yield ($|r|$)')
plt.ylabel('Probability $P(|Yield| > r)$')
plt.axvline(threshold_low, color='red', linestyle=':', alpha=0.5, label='Fit Range')
plt.axvline(threshold_high, color='red', linestyle=':', alpha=0.5)
plt.grid(True, which="both", ls="--", alpha=0.3)
plt.legend()
plt.show()