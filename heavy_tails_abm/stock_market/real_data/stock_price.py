# Script to produce Figure 1 and 2
# Be careful, yfinance might not work on your computer (it did not work
# on mine, so I ran it on Colab instead)

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

tickers = ['^FCHI', '^GSPC']
print("Downloading")
data = yf.download(tickers, start="2000-01-01", end="2023-12-31")['Close']

data = data.dropna()


# Stock price over time
plt.figure(figsize=(14, 6))

(data / data.iloc[0] * 100).plot(ax=plt.gca(), linewidth=1.5)

plt.title('Evolution of CAC 40 and S&P 500 (Basis 100 in year 2000)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Normalized value')
plt.legend(['CAC 40', 'S&P 500'])
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()


# Compute daily log-returns
returns = np.log(data / data.shift(1)).dropna()

# Plot
plt.figure(figsize=(10, 7))

colors = {'^FCHI': 'blue', '^GSPC': 'red'}
labels = {'^FCHI': 'CAC 40', '^GSPC': 'S&P 500'}

for ticker in tickers:
    # Plot the survival function
    abs_returns = np.abs(returns[ticker].values)
    sorted_returns = np.sort(abs_returns)
    n = len(sorted_returns)
    survival_prob = 1.0 - np.arange(1, n + 1) / n

    # Avoid log(0)
    plt.loglog(sorted_returns[:-1], survival_prob[:-1], marker='.',
               linestyle='none', color=colors[ticker], label=labels[ticker], alpha=0.3)

plt.title("Survival function of absolute daily returns (Log-Log scale)", fontsize=14)
plt.xlabel('Absolute Yields $|r|$', fontsize=12)
plt.ylabel('Probability $P(|R| > |r|)$', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()
plt.show()