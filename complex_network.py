import pandapower as pp
from network_analysis import run_diagnosis, plot_network
from tabulate import tabulate

def create_complex_network(
    bus_voltage_pu=1.02,
    residential_load_p_mw=0.15,
    residential_load_q_mvar=0.05,
    commercial_load_p_mw=0.25,
    commercial_load_q_mvar=0.1,
    solar_p_mw=0.05,
    main_line_length_km=50,
    feeder_section1_length_km=2.5,
    feeder_section2_length_km=1.5,
    trafo_terminal_station_sn_mva=100,
    trafo_zone_substation_sn_mva=25,
    network_name="Simplified Melbourne Grid Section"
):
    """
    Creates a complex power grid network using pandapower.
    """
    # Create an Empty Network
    net = pp.create_empty_network(name=network_name)

    # Define Standard Component Types
    # Transmission Line Type (220kV)
    pp.create_std_type(net, name="220kV_line", data={
        "c_nf_per_km": 11.14, "r_ohm_per_km": 0.066, "x_ohm_per_km": 0.303, "max_i_ka": 0.795
    }, element='line')

    # Distribution Line Type (11kV)
    pp.create_std_type(net, name="11kV_line", data={
        "c_nf_per_km": 10, "r_ohm_per_km": 0.25, "x_ohm_per_km": 0.35, "max_i_ka": 0.350
    }, element='line')

    # Terminal Station Transformer (220kV/66kV)
    terminal_trafo_name = f"{trafo_terminal_station_sn_mva} MVA 220/66 kV"
    pp.create_std_type(net, name=terminal_trafo_name, data={
        "sn_mva": trafo_terminal_station_sn_mva, "vn_hv_kv": 220, "vn_lv_kv": 66, "vk_percent": 12.0,
        "vkr_percent": 0.26, "pfe_kw": 50, "i0_percent": 0.06, "shift_degree": 0
    }, element="trafo")

    # Zone Substation Transformer (66kV/11kV)
    zone_trafo_name = f"{trafo_zone_substation_sn_mva} MVA 66/11 kV"
    pp.create_std_type(net, name=zone_trafo_name, data={
        "sn_mva": trafo_zone_substation_sn_mva, "vn_hv_kv": 66, "vn_lv_kv": 11, "vk_percent": 10.0,
        "vkr_percent": 0.3, "pfe_kw": 20, "i0_percent": 0.07, "shift_degree": 0
    }, element="trafo")

    # Distribution Substation Transformer (11kV/0.4kV) - Pole-top
    pp.create_std_type(net, name="0.4 MVA 11/0.4 kV", data={
        "sn_mva": 0.4, "vn_hv_kv": 11, "vn_lv_kv": 0.4, "vk_percent": 4.0,
        "vkr_percent": 0.5, "pfe_kw": 1, "i0_percent": 0.2, "shift_degree": 0
    }, element="trafo")

    # Distribution Substation Transformer (11kV/0.4kV) - Pad-mount
    pp.create_std_type(net, name="0.63 MVA 11/0.4 kV", data={
        "sn_mva": 0.63, "vn_hv_kv": 11, "vn_lv_kv": 0.4, "vk_percent": 5.0,
        "vkr_percent": 0.6, "pfe_kw": 1.5, "i0_percent": 0.25, "shift_degree": 0
    }, element="trafo")

    # Build the Transmission and Sub-Transmission Layer (220kV & 66kV)
    bus_220kv_infeed = pp.create_bus(net, vn_kv=220, name="220kV Infeed (NEM)")
    pp.create_ext_grid(net, bus=bus_220kv_infeed, vm_pu=bus_voltage_pu, name="External Grid")

    bus_220kv_terminal = pp.create_bus(net, vn_kv=220, name="220kV Terminal Station")
    bus_66kv_subtrans = pp.create_bus(net, vn_kv=66, name="66kV Sub-transmission")

    pp.create_line(net, from_bus=bus_220kv_infeed, to_bus=bus_220kv_terminal, length_km=main_line_length_km,
                  std_type="220kV_line", name="Main Transmission Line")

    pp.create_transformer(net, hv_bus=bus_220kv_terminal, lv_bus=bus_66kv_subtrans,
                         std_type=terminal_trafo_name, name="Terminal Station Trafo")

    # Build the Medium Voltage Distribution Layer (11kV)
    bus_11kv_dist = pp.create_bus(net, vn_kv=11, name="11kV Distribution Feeder Start")

    pp.create_transformer(net, hv_bus=bus_66kv_subtrans, lv_bus=bus_11kv_dist,
                         std_type=zone_trafo_name, name="Zone Substation Trafo")

    bus_11kv_mid = pp.create_bus(net, vn_kv=11, name="11kV Feeder Midpoint")
    bus_11kv_end = pp.create_bus(net, vn_kv=11, name="11kV Feeder End")

    pp.create_line(net, from_bus=bus_11kv_dist, to_bus=bus_11kv_mid, length_km=feeder_section1_length_km,
                  std_type="11kV_line", name="Feeder Section 1")
    pp.create_line(net, from_bus=bus_11kv_mid, to_bus=bus_11kv_end, length_km=feeder_section2_length_km,
                  std_type="11kV_line", name="Feeder Section 2")

    # Build the Low Voltage (LV) Layer and connect Customers (0.4kV)
    bus_lv_1 = pp.create_bus(net, vn_kv=0.4, name="LV Bus - Residential Area 1")
    pp.create_transformer(net, hv_bus=bus_11kv_mid, lv_bus=bus_lv_1,
                         std_type="0.4 MVA 11/0.4 kV", name="Pole-top Trafo 1")

    bus_lv_2 = pp.create_bus(net, vn_kv=0.4, name="LV Bus - Commercial Area")
    pp.create_transformer(net, hv_bus=bus_11kv_end, lv_bus=bus_lv_2,
                         std_type="0.63 MVA 11/0.4 kV", name="Pad-mount Trafo 2")

    pp.create_load(net, bus=bus_lv_1, p_mw=residential_load_p_mw, q_mvar=residential_load_q_mvar, name="Residential Load")
    pp.create_load(net, bus=bus_lv_2, p_mw=commercial_load_p_mw, q_mvar=commercial_load_q_mvar, name="Commercial Load")

    pp.create_sgen(net, bus=bus_lv_1, p_mw=solar_p_mw, q_mvar=0, name="Rooftop Solar")
    
    return net

if __name__ == "__main__":
    complex_net = create_complex_network()
    complex_net = run_diagnosis(complex_net, scenario_name="Complex Network")
    plot_network(complex_net)