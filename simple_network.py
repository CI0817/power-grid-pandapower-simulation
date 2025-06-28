import pandapower as pp
import network_analysis as na

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

if __name__ == "__main__":
    # Create the simple network
    net = create_simple_network()

    # Run diaganosis on the network
    na.run_diagnosis(net, scenario_name="Simple Network Scenario")
