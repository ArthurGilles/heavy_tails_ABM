# Script used to produce Figure 3
# Be careful, yfinance might not work on your computer (it did not work
# on mine, so I ran it on Colab instead)

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


tickers = ['^FCHI', '^GSPC']
print("Downloadign")
data = yf.download(tickers, start="2000-01-01", end="2023-12-31")['Close']

data = data.dropna()

# Compute daily log-returns
returns = np.log(data / data.shift(1)).dropna()

# Plot
plt.figure(figsize=(12, 8))

colors = {'^FCHI': 'blue', '^GSPC': 'red'}
labels = {'^FCHI': 'CAC 40', '^GSPC': 'S&P 500'}

# We make the regression only on the tail
tail_min = 0.02
tail_max = 0.08

for ticker in tickers:
    abs_returns = np.abs(returns[ticker].values)

    sorted_returns = np.sort(abs_returns)
    n = len(sorted_returns)
    survival_prob = 1.0 - np.arange(1, n + 1) / n

    # Avoid log(0)
    x_data = sorted_returns[:-1]
    y_data = survival_prob[:-1]

    plt.loglog(x_data, y_data, marker='.', linestyle='none',
               color=colors[ticker], label=f'{labels[ticker]} (Data)', alpha=0.2)

    # Linear regression betweel tail_min and tail_max
    mask = (x_data >= tail_min) & (x_data <= tail_max)
    x_tail = x_data[mask]
    y_tail = y_data[mask]

    if len(x_tail) > 0:
        slope, intercept, r_value, p_value, std_err = linregress(np.log(x_tail), np.log(y_tail))
        alpha = -slope
        y_fit = np.exp(intercept) * (x_tail ** slope)

        # Plot the regression
        plt.loglog(x_tail, y_fit, color="black", linestyle='-', linewidth=2.5,
                   label=f'{labels[ticker]} Regression ($\\alpha \\approx {alpha:.2f}$)')

plt.title("Survival function of absolute daily returns (Log-Log scale)", fontsize=14)
plt.xlabel('Absolute yields $|r|$', fontsize=12)
plt.ylabel('Probability $P(|R| > |r|)$', fontsize=12)

plt.axvline(x=tail_min, color='gray', linestyle='--', alpha=0.5, label=f'Beginning of tail ({tail_min*100:.0f}%)')
plt.axvline(x=tail_max, color='gray', linestyle=':', alpha=0.5, label=f'End of tail ({tail_max*100:.0f}%)')

plt.legend(fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.tight_layout()
plt.show()