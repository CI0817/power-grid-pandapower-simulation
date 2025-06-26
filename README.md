# power-grid-pandapower-simulation
## Expected Learning Outcomes
The expected learning outcomes:
- Become familiar with `pandapower`
- Learn the basics of power grid
- Learn the fundamentals of power system analysis using `pandapower`

## Project Aims
This project aims to:
- Simulate the power usage of a small network
- Simulate short-circuit fault at various points in the network and analyse their effects
- Incorporate renewable energy into the town and re-analyse the power consumption

## Project Stages
This project can be separated into three stages:
- Learn the basics of `pandapower` through test networks and reading the [documentation](https://pandapower.readthedocs.io/en/latest/index.html).
- Create a fairly simple grid and simulate its power usage and fault analysis.
- Add renewable energy power into the energy mix and re-analysis the power usage.

## Key Parameters in `pandapower`
**External Grid (`net.ext_grid`)**: This is the connection to the main power grid and the reference for your whole system.

What to Define (Inputs):
- `bus`: The bus where the main grid connects.
- `vm_pu`: The voltage magnitude (in per-unit) that the grid holds at this point. Typically 1.0.
- `va_degree`: The voltage angle reference for the system. Almost always 0.

What to Check (Results):
- `p_mw` (`net.res_ext_grid`): How much power your network is drawing from (positive value) or sending back to (negative value) the main grid.

**Bus (`net.bus`)**: These are the nodes or connection points in your network.

What to Define (Inputs):
- `vn_kv`: The rated voltage of the bus in kilovolts (kV). This is the most important property of a bus.

What to Check (Results):
- `vm_pu` (`net.res_bus`): The actual voltage magnitude. Why? You must check that this is within a safe range (e.g., 0.95 to 1.05) to ensure equipment operates correctly.

**Line (`net.line`)**: These are the power lines connecting your buses.

What to Define (Inputs):
- `from_bus` & `to_bus`: The start and end buses for the connection.
- `length_km`: The length of the line.
- `std_type`: A standard library type (e.g., "NAYY 4x50 SE") that defines the line's electrical properties (resistance/reactance).

What to Check (Results):
- `loading_percent` (`net.res_line`): How loaded the line is. Why? You must ensure this is below 100% to prevent overheating and physical damage.
- Voltage Angle Difference: The difference in `va_degree` between the `from_bus` and `to_bus`. Why? A large difference indicates the line is under high stress and may be approaching its stability limit.

**Load (`net.load`)**: These represent the power consumers in your network.

What to Define (Inputs):
- `bus`: The bus where the load is connected.
- `p_mw`: The active power consumed by the load in megawatts (MW).

What to Check (Results):
The `p_mw` and `q_mvar` in `net.res_load` will simply reflect the power consumed, confirming the load was part of the simulation.

**Generator (`net.gen`)**: These are local power sources in your network, like a diesel generator or a power plant.

What to Define (Inputs):
- `bus`: The bus where the generator is connected.
- `p_mw`: The active power it supplies to the grid.
- `vm_pu`: The voltage setpoint it tries to maintain at its bus.

What to Check (Results):
- `p_mw` and `q_mvar` (`net.res_gen`): The actual active and reactive power the generator is producing to meet the grid's needs