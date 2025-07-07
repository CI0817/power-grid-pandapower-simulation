import argparse
import json
from pandapower.plotting import simple_plot
import sys
import os
import warnings

# Suppress the FutureWarning from pandapower regarding build_branch
# This warning is related to the `build_branch` module and can be ignored for now.
warnings.filterwarnings("ignore", category=FutureWarning, module="pandapower.build_branch")

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.network_analysis import run_diagnosis, run_contingency_analysis, run_shortcircuit_analysis
from src.simple_network import create_simple_network
from src.complex_network import create_complex_network
from src.case14 import create_case14_network

def main():
    parser = argparse.ArgumentParser(description="Power Grid Simulation Tool")
    parser.add_argument('simulation', choices=['simple', 'complex', 'case14', 'contingency', 'shortcircuit'], help='The simulation to run.')

    args = parser.parse_args()

    if args.simulation == 'simple':
        net = create_simple_network()
        run_diagnosis(net, 'Simple Network')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'complex':
        with open('data/network_config.json', 'r') as f:
            config = json.load(f)
        net = create_complex_network(config)
        run_diagnosis(net, 'Data-Driven Network')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'case14':
        net = create_case14_network()
        run_diagnosis(net, 'IEEE Case 14')
        simple_plot(net, plot_loads=True, plot_sgens=True, plot_gens=True)
    elif args.simulation == 'contingency':
        with open('data/network_config.json', 'r') as f:
            config = json.load(f)
        net = create_complex_network(config)
        run_diagnosis(net, 'Contingency Analysis Network')
        run_contingency_analysis(net)
    elif args.simulation == 'shortcircuit':
        with open('data/network_config.json', 'r') as f:
            config = json.load(f)
        net = create_complex_network(config)
        run_diagnosis(net, 'Short-Circuit Analysis Network')
        run_shortcircuit_analysis(net, bus=None)


if __name__ == "__main__":
    main()
