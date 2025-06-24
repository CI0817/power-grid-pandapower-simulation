import pandapower as pp
import pandapower.networks as nw
from tabulate import tabulate
import pandapower.plotting as plot

# Display the network information
def display_network_info(net):
    bus_df = net.bus
    line_df = net.line
    load_df = net.load
    gen_df = net.gen
    ext_grid_df = net.ext_grid

    print("Bus Data:")
    print(tabulate(bus_df, headers='keys', tablefmt='pretty'))
    
    print("\nLine Data:")
    print(tabulate(line_df, headers='keys', tablefmt='pretty'))
    
    print("\nLoad Data:")
    print(tabulate(load_df, headers='keys', tablefmt='pretty'))
    
    print("\nGenerator Data:")
    print(tabulate(gen_df, headers='keys', tablefmt='pretty'))

    print("\nExternal Grid Data:")
    print(tabulate(ext_grid_df, headers='keys', tablefmt='pretty'))

# Display the power flow results
def display_power_flow_results(net):
    print("\nPower Flow Results:")
    print("\nBus Results:")
    print(tabulate(net.res_bus, headers='keys', tablefmt='pretty'))
    print("\nLine Results:")
    print(tabulate(net.res_line, headers='keys', tablefmt='pretty'))
    print("\nLoad Results:")
    print(tabulate(net.res_load, headers='keys', tablefmt='pretty'))
    print("\nGenerator Results:")
    print(tabulate(net.res_gen, headers='keys', tablefmt='pretty'))
    print("\nExternal Grid Results:")
    print(tabulate(net.res_ext_grid, headers='keys', tablefmt='pretty'))


if __name__ == "__main__":
    net = nw.case14()

    display_network_info(net)

    # Run power flow on the created network
    pp.runpp(net)

    # Display power flow results
    display_power_flow_results(net)

    # Plot the network
    plot.simple_plot(net, plot_loads=True, plot_gens=True)
