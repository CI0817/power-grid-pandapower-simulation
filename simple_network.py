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
    print("\n=======================================================")
    print("=================NETWORK INFORMATION===================")
    print("=======================================================\n")
    bus_df = net.bus
    line_df = net.line
    load_df = net.load
    transformer_df = net.trafo
    ext_grid_df = net.ext_grid

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

def check_power_flow(net:pp.pandapowerNet) -> bool:
    """
    Check if the power flow was successful.
    """
    print("\n======================================================")
    print("=================POWER FLOW CHECK=====================")
    print("======================================================\n")
    if net.converged:
        print("Power flow converged successfully.")
        return True
    else:
        print("Power flow did not converge.")
        return False

def check_bus_voltage(net: pp.pandapowerNet) -> None:
    """
    Checks if bus voltages are within the ideal and acceptable ranges, 0.95-1.05 pu.
    """
    print("\n======================================================")
    print("=================BUS VOLTAGE CHECK====================")
    print("======================================================\n")
    bus_vm = net.res_bus.vm_pu
    voltage_violations = net.res_bus[(bus_vm < 0.95) | (bus_vm > 1.05)]
    if not voltage_violations.empty:
        print("Voltage violations detected at the following buses:")
        print(tabulate(voltage_violations[['vm_pu']], headers='keys', tablefmt='pretty'))
    else:
        print("All bus voltages are within the acceptable range (0.95 - 1.05 pu).")

def check_line_loading(net: pp.pandapowerNet) -> None:
    """
    Check if line loadings are within the acceptable range: Ideal is < 80%, acceptable is < 100%.
    """
    print("\n======================================================")
    print("=================LINE LOADING CHECK===================")
    print("======================================================\n")
    line_loading = net.res_line.loading_percent
    overload_lines = net.res_line[line_loading > 100]
    warning_lines = net.res_line[(line_loading > 80) & (line_loading <= 100)]

    if not overload_lines.empty:
        print("Overloaded lines detected (>100):")
        print(tabulate(overload_lines[['loading_percent']], headers='keys', tablefmt='pretty'))
    elif not warning_lines.empty:
        print("Lines with high loading (80 - 100):")
        print(tabulate(warning_lines[['loading_percent']], headers='keys', tablefmt='pretty'))
    else:
        print("All lines are within the acceptable loading range (< 80%).")

def check_transformer_loading(net: pp.pandapowerNet) -> None:
    """
    Check if transformer loadings are within the acceptable range: Ideal is < 80%, acceptable is < 100%.
    """
    print("\n======================================================")
    print("================TRANSFORMER LOADING CHECK=============")
    print("======================================================\n")
    transformer_loading = net.res_trafo.loading_percent
    overload_transformers = net.trafo[transformer_loading > 100]
    warning_transformers = net.trafo[(transformer_loading > 80) & (transformer_loading <= 100)]

    if not overload_transformers.empty:
        print("Overloaded transformers detected (>100):")
        print(tabulate(overload_transformers[['loading_percent']], headers='keys', tablefmt='pretty'))
    elif not warning_transformers.empty:
        print("Transformers with high loading (80 - 100):")
        print(tabulate(warning_transformers[['loading_percent']], headers='keys', tablefmt='pretty'))
    else:
        print("All transformers are within the acceptable loading range (< 80%).")

def check_line_voltage_angle(net: pp.pandapowerNet) -> None:
    """
    Checks the voltage angle difference across lines, indicating grid stress: Ideal is < 20 degs, acceptable is < 30 degs.
    """
    print("\n======================================================")
    print("=================LINE VOLTAGE ANGLE CHECK=============")
    print("======================================================\n")
    line_data = []
    for i, line in net.line.iterrows():
        from_bus = line.from_bus
        to_bus = line.to_bus
        angle_from = net.res_bus.va_degree.at[from_bus]
        angle_to = net.res_bus.va_degree.at[to_bus]
        diff = abs(angle_from - angle_to)
        line_data.append([i, diff])
    
    line_df = pd.DataFrame(line_data, columns=['line_index', 'angle_diff_deg'])

    high_angle_lines = line_df[line_df['angle_diff_deg'] > 30]
    warning_angle_lines = line_df[(line_df['angle_diff_deg'] > 20) & (line_df['angle_diff_deg'] <= 30)]

    if not high_angle_lines.empty:
        print("High voltage angle differences detected (>30 degrees):")
        print(tabulate(high_angle_lines, headers='keys', tablefmt='pretty'))
    elif not warning_angle_lines.empty:
        print("Voltage angle differences with warning (20 - 30 degrees):")
        print(tabulate(warning_angle_lines, headers='keys', tablefmt='pretty'))
    else:
        print("All voltage angle differences are within the acceptable range (< 20 degrees).")


if __name__ == "__main__":
    # Create the simple network
    net = create_simple_network()

    # Print network information
    print_network_info(net)

    # Run power flow analysis
    pp.runpp(net)

    # Print power flow results
    print_power_flow_results(net)

    # Check power flow convergence
    if check_power_flow(net):
        # Check bus voltages
        check_bus_voltage(net)

        # Check line loading
        check_line_loading(net)

        # Check transformer loading
        check_transformer_loading(net)

        # Check line voltage angle differences
        check_line_voltage_angle(net)
    else:
        print("Power flow did not converge, skipping further checks.")

    # Plot the network
    plot_network(net)