import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [script_name]")
        return

    script_map = {
        "regression_returns_data": "stock_market/real_data/regression_data.py",
        "stock_price_data": "stock_market/real_data/stock_price.py",
        "cluster_size_CB": "stock_market/cont_bouchaud/cluster_size.py",
        "daily_returns_simulated": "stock_market/cont_bouchaud/daily_returns.py",
        "regression_simulated_returns": "stock_market/cont_bouchaud/heavy_tail_regression.py",
        "stock_price_simulated": "stock_market/cont_bouchaud/stock_price_trajectory.py"
    }

    command = sys.argv[1]

    if command in script_map:
        subprocess.run(["python", script_map[command]])
    else:
        print(f"Unknown command. Available: {list(script_map.keys())}")

if __name__ == "__main__":
    main()