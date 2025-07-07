import pandapower as pp
import network_analysis as na

def create_simple_network(
    bus1_vn_kv=20.0,
    bus2_vn_kv=0.4,
    bus3_vn_kv=0.4,
    ext_grid_vm_pu=1.02,
    transformer_std_type="0.4 MVA 20/0.4 kV",
    load1_p_mw=0.08,
    load1_q_mvar=0.04,
    load2_p_mw=0.07,
    load2_q_mvar=0.03,
    line_length_km=0.1,
    line_std_type="NAYY 4x50 SE"
) -> pp.pandapowerNet:
    """
    Create a simple pandapower network with customizable parameters.
    """
    net = pp.create_empty_network(name="Simple Network")

    # Create buses
    bus1 = pp.create_bus(net, vn_kv=bus1_vn_kv, name="Main Bus")
    bus2 = pp.create_bus(net, vn_kv=bus2_vn_kv, name="Load Bus 1")
    bus3 = pp.create_bus(net, vn_kv=bus3_vn_kv, name="Load Bus 2")

    # Create an external grid
    pp.create_ext_grid(net, bus=bus1, vm_pu=ext_grid_vm_pu, va_degree=0.0, name="External Grid")

    # Create a transformer
    pp.create_transformer(net, hv_bus=bus1, lv_bus=bus2, std_type=transformer_std_type, name="Transformer")

    # Create loads
    pp.create_load(net, bus=bus2, p_mw=load1_p_mw, q_mvar=load1_q_mvar, name="Load 1")
    pp.create_load(net, bus=bus3, p_mw=load2_p_mw, q_mvar=load2_q_mvar, name="Load 2")

    # Create lines
    pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=line_length_km, std_type=line_std_type, name="Line")

    return net

