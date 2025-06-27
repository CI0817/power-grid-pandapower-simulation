import pandas as pd
import pandapower as pp
from tabulate import tabulate
from pandapower.plotting import simple_plot

def create_simple_network() -> pp.pandapowerNet:
    """
    Create a simple pandapower network with three buses, one transformer, two loads, and one line.
    """
    net = pp.create_empty_network(name="Simple Network")

    # Create buses
    bus1 = pp.create_bus(net, vn_kv=20.0, name="Main Bus")
    bus2 = pp.create_bus(net, vn_kv=0.4, name="Load Bus 1")
    bus3 = pp.create_bus(net, vn_kv=0.4, name="Load Bus 2")

    # Create an external grid
    pp.create_ext_grid(net, bus=bus1, vm_pu=1.02, va_degree=0.0, name="External Grid")

    # Create a transformer
    pp.create_transformer(net, hv_bus=bus1, lv_bus=bus2, std_type="0.4 MVA 20/0.4 kV", name="Transformer")

    # Create loads
    pp.create_load(net, bus=bus2, p_mw=0.1, q_mvar=0.05, name="Load 1")
    pp.create_load(net, bus=bus3, p_mw=0.15, q_mvar=0.07, name="Load 2")

    # Create lines
    pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=0.1, std_type="NAYY 4x50 SE", name="Line")

    return net

def print_network_info(net: pp.pandapowerNet):
    """
    Print the network information including buses, lines, loads, transformers, and external grids.
    """
    bus_df = net.bus
    line_df = net.line
    load_df = net.load
    transformer_df = net.trafo
    ext_grid_df = net.ext_grid

    print("\n=======================================================")
    print("=================NETWORK INFORMATION===================")
    print("=======================================================\n")
    print("Bus Data:")
    print(tabulate(bus_df[['name', 'vn_kv']], headers='keys', tablefmt='pretty'))
    print("\nLine Data:")
    print(tabulate(line_df[['name', 'from_bus', 'to_bus', 'length_km', 'std_type']], headers='keys', tablefmt='pretty'))
    print("\nLoad Data:")
    print(tabulate(load_df[['name', 'bus', 'p_mw', 'q_mvar']], headers='keys', tablefmt='pretty'))
    print("\nTransformer Data:")
    print(tabulate(transformer_df[['name', 'hv_bus', 'lv_bus', 'std_type']], headers='keys', tablefmt='pretty'))
    print("\nExternal Grid Data:")
    print(tabulate(ext_grid_df[['name', 'bus', 'vm_pu', 'va_degree']], headers='keys', tablefmt='pretty'))

def print_power_flow_results(net: pp.pandapowerNet):
    """
    Print the results of the power flow analysis.
    """
    print("\n======================================================")
    print("=================POWER FLOW RESULTS===================")
    print("======================================================\n")
    print("Bus Results:")
    print(tabulate(net.res_bus, headers='keys', tablefmt='pretty'))
    print("\nLine Results:")
    print(tabulate(net.res_line[['pl_mw', 'loading_percent']], headers='keys', tablefmt='pretty'))
    print("\nLoad Results:")
    print(tabulate(net.res_load, headers='keys', tablefmt='pretty'))
    print("\nTransformer Results:")
    print(tabulate(net.res_trafo[['pl_mw', 'ql_mvar', 'vm_hv_pu', 'vm_lv_pu', 'loading_percent']], headers='keys', tablefmt='pretty'))
    print("\nExternal Grid Results:")
    print(tabulate(net.res_ext_grid, headers='keys', tablefmt='pretty'))

def plot_network(net: pp.pandapowerNet):
    """
    Plot the network using pandapower's simple_plot function.
    """
    print("\n======================================================")
    print("=================NETWORK PLOT=========================")
    print("======================================================\n")
    print("Network plot will be displayed in a separate window.\n")
    simple_plot(net, plot_loads=True, plot_gens=True)


if __name__ == "__main__":
    # Create the simple network
    net = create_simple_network()

    # Print network information
    print_network_info(net)

    # Run power flow analysis
    pp.runpp(net)

    # Print power flow results
    print_power_flow_results(net)

    # Plot the network
    plot_network(net)
