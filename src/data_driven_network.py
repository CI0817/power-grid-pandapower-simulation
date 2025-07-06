
import pandapower as pp

def create_data_driven_network(config):
    """
    Creates a pandapower network from a configuration dictionary.

    :param config: A dictionary defining the network structure.
    :return: A pandapower network object.
    """
    net = pp.create_empty_network(name=config.get("name", "Default Network"))

    # Create buses
    bus_mapping = {}
    for bus_def in config.get("buses", []):
        bus_id = pp.create_bus(net, name=bus_def["name"], vn_kv=bus_def["vn_kv"])
        bus_mapping[bus_def["name"]] = bus_id

    # Create standard line types
    for line_type in config.get("std_lines", []):
        pp.create_std_type(net, name=line_type["name"], data=line_type["data"], element='line')

    # Create standard transformer types
    for trafo_type in config.get("std_trafos", []):
        pp.create_std_type(net, name=trafo_type["name"], data=trafo_type["data"], element='trafo')

    # Create external grids
    for ext_grid in config.get("ext_grids", []):
        pp.create_ext_grid(net, 
                           bus=bus_mapping[ext_grid["bus"]], 
                           vm_pu=ext_grid.get("vm_pu", 1.0), 
                           name=ext_grid.get("name"),
                           s_sc_max_mva=ext_grid.get("s_sc_max_mva"),
                           s_sc_min_mva=ext_grid.get("s_sc_min_mva"),
                           rx_max=ext_grid.get("rx_max"),
                           rx_min=ext_grid.get("rx_min"))

    # Create lines
    for line in config.get("lines", []):
        pp.create_line(net, from_bus=bus_mapping[line["from_bus"]], to_bus=bus_mapping[line["to_bus"]],
                      length_km=line["length_km"], std_type=line["std_type"], name=line.get("name"))

    # Create transformers
    for trafo in config.get("transformers", []):
        pp.create_transformer(net, hv_bus=bus_mapping[trafo["hv_bus"]], lv_bus=bus_mapping[trafo["lv_bus"]],
                             std_type=trafo["std_type"], name=trafo.get("name"))

    # Create loads
    for load in config.get("loads", []):
        pp.create_load(net, bus=bus_mapping[load["bus"]], p_mw=load["p_mw"], q_mvar=load.get("q_mvar", 0), name=load.get("name"))

    # Create static generators
    for sgen in config.get("sgens", []):
        pp.create_sgen(net, bus=bus_mapping[sgen["bus"]], p_mw=sgen["p_mw"], q_mvar=sgen.get("q_mvar", 0), name=sgen.get("name"), sn_mva=sgen.get("sn_mva"), k=sgen.get("k"))

    return net
