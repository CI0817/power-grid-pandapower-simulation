import argparse
import json
import pandapower as pp
from pandapower.plotting import simple_plot
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.network_analysis import run_diagnosis, run_contingency_analysis
from src.simple_network import create_simple_network
from src.complex_network import create_complex_network
from src.data_driven_network import create_data_driven_network
from src.case14 import create_case14_network

def main():
    parser = argparse.ArgumentParser(description="Power Grid Simulation Tool")
    parser.add_argument('simulation', choices=['simple', 'complex', 'data_driven', 'case14', 'contingency'], help='The simulation to run.')

    args = parser.parse_args()

    if args.simulation == 'simple':
        net = create_simple_network()
        run_diagnosis(net, 'Simple Network')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'complex':
        net = create_complex_network()
        run_diagnosis(net, 'Complex Network')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'data_driven':
        with open('data/network_config.json', 'r') as f:
            config = json.load(f)
        net = create_data_driven_network(config)
        run_diagnosis(net, 'Data-Driven Network')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'case14':
        net = create_case14_network()
        run_diagnosis(net, 'IEEE Case 14')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'contingency':
        with open('data/network_config.json', 'r') as f:
            config = json.load(f)
        net = create_data_driven_network(config)
        run_contingency_analysis(net)


if __name__ == "__main__":
    main()
