# power-grid-pandapower-simulation
## Project Overview
### Expected Learning Outcomes
The expected learning outcomes:
- Become familiar with `pandapower`
- Learn the basics of power grid
- Learn the fundamentals of power system analysis using `pandapower`

### Project Aims
This project aims to:
- Simulate the power usage of a small network
- Simulate short-circuit fault at various points in the network and analyse their effects
- Incorporate renewable energy into the town and re-analyse the power consumption

### Project Stages
This project can be separated into three stages:
- Learn the basics of `pandapower` through test networks and reading the [documentation](https://pandapower.readthedocs.io/en/latest/index.html).
- Create a fairly simple grid and simulate its power usage and fault analysis.
- Add renewable energy power into the energy mix and re-analysis the power usage.

## Key Information
### Main Usage of `pandapower`
The main function of `pandapower` is to run the power flow simulation, which simulates how a network behaves under operating conditions given a certain setup (the arrangement of generators, loads, transformers, etc.). The result of the power flow analysis would tell us the operating voltage of each bus and whether any lines are overloaded with power, etc.

This allows us to analyse the behaviour of the network before building it.

Other uses include analysing fault in the network. What if the a component in the network malfunctioned and became non-operational, what would happen to the network? This is crucial since we don't want the network to overload or cause further damages during malfunctions.

It is also useful when we want to know what happened when we add more loads or generators to an existing network.

### How `pandapower` Perform Power Flow Analysis
It uses the information (rated voltage, min, max values) of the components provided and put them in equations to make sure that at every single bus, the power flow into that bus is equal to the power flowing out of it. This obeys the fundamental law of physics applied to a power grid.

The calculation follows an iterative process in which it uses an algorithm called Newton-Raphson to predict the power flow at each bus. At first, it starts with a flat guess of 1.0 pu and 0 degrees for every bus. It uses those values to calculate the power flow throughout the network, and compare it to what it should be (using the values provided with the components), and the difference in those values are called errors. This guessing iterative process continues until the errors become very small, at which point it is said that the solution has been converged.

Once the solution is converged, it calculates the final values such as the voltage at each bus, the laoding percentage of each line, etc.

### Key Parameters in `pandapower`
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

### Typical Values Bus Voltage, Line and Transformer Loading, and Voltage Angle Difference (Across a Line)
**Bus Voltage, `vm_pu` in `net.res_bus`**: This tells you if the voltage level at your connection points is correct. The value is in "per-unit," which is a ratio of the actual voltage to the rated voltage.
- Ideal: 1.0, the voltage is exactly at its specified rating.
- Acceptable: 0.95 to 1.05, the standard range for normal operation (±5%).
    - In Australia, the official range at the connection point is 230V +10%/-6%.
- Critical: <0.95 or >1.05, low voltage (brownout) can cause motors to run hot and inefficiently, and high voltage and permanently damage components.

**Line and Transformer Loading, `loading_percent`**: This shows you how much of a component's maximum capacity is being used. It is the most important indicator for preventing physical damage.
- Ideal: <80%, it provides a good safety margin for unexpected changes in load or generation.
- Acceptable: 80%-100%, While acceptable, running consistently in this range gives you very little room for error or future growth.
- Critical: >100%, it means the component is overloaded.
    - For lines, they will overheat and physically sag, which can cause them to touch trees or the ground, leading to a dangerous short-circuit.
    - For transformers, they will overheat, which rapidly degrades their internal insulation and can lead to catastrophic failure.

**Voltage Angle Difference (Across a Line)**: This isn't a direct pandapower result, but you calculate it by taking the difference between the va_degree at a line's from_bus and to_bus. It is a key indicator of grid stability.
- Ideal: <20 degrees, a small angle difference means power is flowing easily without stressing the system.
- Acceptable: 20-30 degrees, this indicates that the connection is becoming stressed. It's working very hard to push power across.
- Critical: >30 degrees, it can potentially lead to a blackout.
    - A very large angle difference means the system is on the verge of losing synchronism. If the angle gets too large, the connection between the generator and the load breaks, which can trigger a cascading failure across the grid.