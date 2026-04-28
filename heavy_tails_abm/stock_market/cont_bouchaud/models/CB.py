import numpy as np
import networkx as nx


class ContBouchaudModel:
    """
    Class representing a Cont-Bouchaud model. It can be used to simulate one
    and carry experiments and simulations on it.
    """
    def __init__(self, connectivity, n_traders, prob, liquidity, init_price=100, annealed=True):
        assert prob >= 0 and prob <= 0.5
        assert connectivity >= 0

        self.connectivity = connectivity
        self.n_traders = n_traders
        self.prob = prob
        self.liquidity = liquidity
        self.price = init_price
        self.annealed = annealed
        self.rng = np.random.default_rng()

        self.generate_graph()

    def generate_graph(self):
        edge_prob = self.connectivity / self.n_traders
        self.graph = nx.fast_gnp_random_graph(self.n_traders, edge_prob, seed=self.rng)
        self.clusters = list(nx.connected_components(self.graph))
        self.n_clusters = len(self.clusters)
        self.cluster_sizes = np.array([len(cluster) for cluster in self.clusters])

    def step(self):
        if self.annealed:
            # Regenerate the network at each step if annealed is True
            # This leads to better (but more costly) simulations because
            # if a weird graph is generated at the beginning, it will be used
            # at every step in the simulation, which usually give weird returns 
            # and stock prices
            self.generate_graph()

        values = [-1, 0, 1]
        probs  = [self.prob, 1 - 2*self.prob, self.prob]
        choices = self.rng.choice(values, p=probs, size=self.n_clusters)

        # Calculate demand. Here, it is scaled by 1/N (it is not in Eq 27 of the
        # report but it allows to keep the same liquidity for different N,
        # while keeping approximately the same distribution returns)
        demand = np.sum(choices * self.cluster_sizes)
        current_yield = self.liquidity * (demand / self.n_traders)
        self.price = self.price * np.exp(current_yield)

        return self.price, current_yield