complex_network_config = {
    "name": "Complex Customizable Grid",
    "buses": [
        {"name": "220kV Infeed", "vn_kv": 220},
        {"name": "220kV Terminal", "vn_kv": 220},
        {"name": "66kV Sub-trans", "vn_kv": 66},
        {"name": "11kV Dist Feeder", "vn_kv": 11},
        {"name": "11kV Midpoint", "vn_kv": 11},
        {"name": "11kV Feeder End", "vn_kv": 11},
        {"name": "LV Residential", "vn_kv": 0.4},
        {"name": "LV Commercial", "vn_kv": 0.4}
    ],
    "std_lines": [
        {
            "name": "220kV_line",
            "data": {"c_nf_per_km": 11.14, "r_ohm_per_km": 0.066, "x_ohm_per_km": 0.303, "max_i_ka": 0.795}
        },
        {
            "name": "11kV_line",
            "data": {"c_nf_per_km": 10, "r_ohm_per_km": 0.25, "x_ohm_per_km": 0.35, "max_i_ka": 0.350}
        }
    ],
    "std_trafos": [
        {
            "name": "100 MVA 220/66 kV",
            "data": {"sn_mva": 100, "vn_hv_kv": 220, "vn_lv_kv": 66, "vk_percent": 12.0, "vkr_percent": 0.26, "pfe_kw": 50, "i0_percent": 0.06, "shift_degree": 0}
        },
        {
            "name": "25 MVA 66/11 kV",
            "data": {"sn_mva": 25, "vn_hv_kv": 66, "vn_lv_kv": 11, "vk_percent": 10.0, "vkr_percent": 0.3, "pfe_kw": 20, "i0_percent": 0.07, "shift_degree": 0}
        },
        {
            "name": "0.4 MVA 11/0.4 kV",
            "data": {"sn_mva": 0.4, "vn_hv_kv": 11, "vn_lv_kv": 0.4, "vk_percent": 4.0, "vkr_percent": 0.5, "pfe_kw": 1, "i0_percent": 0.2, "shift_degree": 0}
        },
        {
            "name": "0.63 MVA 11/0.4 kV",
            "data": {"sn_mva": 0.63, "vn_hv_kv": 11, "vn_lv_kv": 0.4, "vk_percent": 5.0, "vkr_percent": 0.6, "pfe_kw": 1.5, "i0_percent": 0.25, "shift_degree": 0}
        }
    ],
    "ext_grids": [
        {"name": "External Grid", "bus": "220kV Infeed", "vm_pu": 1.02}
    ],
    "lines": [
        {"name": "Main Transmission Line", "from_bus": "220kV Infeed", "to_bus": "220kV Terminal", "length_km": 50, "std_type": "220kV_line"},
        {"name": "Feeder Section 1", "from_bus": "11kV Dist Feeder", "to_bus": "11kV Midpoint", "length_km": 2.5, "std_type": "11kV_line"},
        {"name": "Feeder Section 2", "from_bus": "11kV Midpoint", "to_bus": "11kV Feeder End", "length_km": 1.5, "std_type": "11kV_line"}
    ],
    "transformers": [
        {"name": "Terminal Station Trafo", "hv_bus": "220kV Terminal", "lv_bus": "66kV Sub-trans", "std_type": "100 MVA 220/66 kV"},
        {"name": "Zone Substation Trafo", "hv_bus": "66kV Sub-trans", "lv_bus": "11kV Dist Feeder", "std_type": "25 MVA 66/11 kV"},
        {"name": "Pole-top Trafo 1", "hv_bus": "11kV Midpoint", "lv_bus": "LV Residential", "std_type": "0.4 MVA 11/0.4 kV"},
        {"name": "Pad-mount Trafo 2", "hv_bus": "11kV Feeder End", "lv_bus": "LV Commercial", "std_type": "0.63 MVA 11/0.4 kV"}
    ],
    "loads": [
        {"name": "Residential Load", "bus": "LV Residential", "p_mw": 0.15, "q_mvar": 0.05},
        {"name": "Commercial Load", "bus": "LV Commercial", "p_mw": 0.25, "q_mvar": 0.1}
    ],
    "sgens": [
        {"name": "Rooftop Solar", "bus": "LV Residential", "p_mw": 0.05}
    ]
}
