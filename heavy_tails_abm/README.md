# Emergence of Power Laws in Financial Markets and Seismic Activity: An Agent-Based Modelling Approach

## Installation

NB : this paragraph describes how to install the required packages with a vanilla virtual environment. You are free to install them via conda, or globally.

To install the required packages, you first need to install python 3.11.9 (note that it may, and probably does work in some other versions) and create a virtual environment :

`python3 -m venv <name of your virtual environment>`

Then, activate it and install the packages via :

`source <name of your virtual environment>/bin/activate`

`pip install -r requirements.txt`

## General structure of the repository

The repository is made of two main directories: `OFC` and `stock_market`, corresponding to the two models studied experimentally in the project. 


#### stock_market
The `stock_market` directory contains two folders, one for the empirical data gathered on the market and download with Yahoo Finance (`real_data`), and one implementing the Cont-Bouchaud model used to obtain the simulated theoretical results.

#### OFC

The OFC directory contains the code needed to create the core of the OFC simulations. It is organised with many packages (with `__init__.py`files). All those modules are then imported, to run all the code and display all the figures in a notebook. See directly the notebook to view how the figures were obtained.


## Running the scripts in stock_market

The `stock_market` folder contains all the scripts necessary to obtain the figures presented in the corresponding section of the report (and even more). To run those scripts you need to go to the root directory of the project, and use the `run.py` file with a specified option (list below):

`python run.py [name_of_the_option]`

Here is the exhaustive list of the available options to run.

- `stock_price_data`: displays the stock price of S&P500 and CAC40 over time, from the year 2000 up to 2024, as well as the distribution of the returns in log-log scale. Used to get Figure 1 and 2
- `regression_returns_data`: displays the distribution of the returns of S&P500 and CAC40 over time in log-log scale, does a linear regression over the second regime (see report section 5.1) and plots it on top of the distribution. Used to get Figure 3
- `cluster_size_CB`: given Erdős–Rényi graph (graph used in Cont-Bouchaud), plots the fraction of the nodes in the largest cluster as a function of the connectivity with `N=100 000` nodes. Used to get Figure 4
- `regression_simulated_returns`: using the Cont-Bouchaud model, simulates the distribution of the returns in log-log scale with the parameters matching the empirical data and does a linear regression on the tail. Used to get Figure 5
- `stock_price_simulated`: simulates a stock price trajectory over time, simulated with the Cont-Bouchaud model with the parameters that adjust to the empirical data. Used to get Figure 6
- `daily_returns_simulated`: Simulates the daily returns of some stocks using the Cont-Bouchaud model in three different regime (sub-critical, super-critical and critical), and plots the time series of the daily returns.
    





