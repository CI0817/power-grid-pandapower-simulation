import pandapower as pp
import pandapower.networks as nw
from tabulate import tabulate
# Display the network information
def display_network_info(net):
    bus_df = net.bus
    line_df = net.line
    load_df = net.load
    gen_df = net.gen
    ext_grid_df = net.ext_grid

    print("Bus Data:")
    print(tabulate(bus_df[['vn_kv']], headers='keys', tablefmt='pretty'))
    
    print("\nLine Data:")
    print(tabulate(line_df[['from_bus','to_bus','length_km','std_type']], headers='keys', tablefmt='pretty'))
    
    print("\nLoad Data:")
    print(tabulate(load_df[['bus','p_mw','q_mvar']], headers='keys', tablefmt='pretty'))
    
    print("\nGenerator Data:")
    print(tabulate(gen_df[['bus','p_mw','vm_pu']], headers='keys', tablefmt='pretty'))

    print("\nExternal Grid Data:")
    print(tabulate(ext_grid_df[['bus','vm_pu','va_degree']], headers='keys', tablefmt='pretty'))

# Display the power flow results
def display_power_flow_results(net):
    print("\nPower Flow Results:")
    print("\nBus Results:")
    print(tabulate(net.res_bus, headers='keys', tablefmt='pretty'))
    print("\nLine Results:")
    print(tabulate(net.res_line[['p_from_mw','q_from_mvar','p_to_mw','q_to_mvar','loading_percent']], headers='keys', tablefmt='pretty'))
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
    # plot.simple_plot(net, plot_loads=True, plot_gens=True)
