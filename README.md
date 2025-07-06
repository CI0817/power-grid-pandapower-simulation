# Power Grid Simulation with `pandapower`

This project uses the `pandapower` library to simulate and analyze electrical power grids. It includes examples ranging from simple networks to more complex, multi-layered grid structures, demonstrating power flow analysis, fault calculations, and the impact of renewable energy integration.

## Project Aims

-   **Simulate Power Grids**: Model and simulate the behavior of various power networks, from simple configurations to a multi-layered grid inspired by real-world systems.
-   **Analyze Network Health**: Perform critical analyses, including power flow, to check for overloads, voltage violations, and other operational issues.
-   **Simulate Fault Scenarios**: Conduct short-circuit calculations to understand the impact of electrical faults and ensure the safety and reliability of the grid.
-   **Data-Driven Configuration**: Demonstrate how to build and manage networks programmatically using a data-driven approach with configuration files.

## Project Structure

The project is organized into the following directories:

-   `src/`: Contains the Python source code for the project.
    -   `main.py`: The main entry point for running simulations.
    -   `simple_network.py`: Defines a basic network.
    -   `complex_network.py`: Implements a more realistic, four-layered network.
    -   `data_driven_network.py`: Builds a network from a configuration file.
    -   `case14.py`: Loads a standard IEEE 14-bus test case.
    -   `network_analysis.py`: Contains functions for analyzing network health.
-   `data/`: Contains data files for the project.
    -   `network_config.json`: A JSON configuration file defining a network.

## Getting Started

### Prerequisites

-   Python 3.6+
-   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/power-grid-pandapower-simulation.git
    cd power-grid-pandapower-simulation
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Simulations

Use the `main.py` script to run the simulations. You can choose which simulation to run by passing a command-line argument.

```bash
python src/main.py <simulation_name>
```

Available simulations:

-   `simple`: Runs the simple network simulation.
-   `complex`: Runs the complex network simulation.
-   `data_driven`: Runs the data-driven network simulation using `data/network_config.json`.
-   `case14`: Runs the IEEE 14-bus test case.

### Examples

```bash
# Run the simple network simulation
python src/main.py simple

# Run the complex network simulation
python src/main.py complex
```


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

-   `bus`: The bus where the main grid connects.
-   `vm_pu`: The voltage magnitude (in per-unit) that the grid holds at this point. Typically 1.0.
-   `va_degree`: The voltage angle reference for the system. Almost always 0.

What to Check (Results):

-   `p_mw` (`net.res_ext_grid`): How much power your network is drawing from (positive value) or sending back to (negative value) the main grid.

**Bus (`net.bus`)**: These are the nodes or connection points in your network.

What to Define (Inputs):

-   `vn_kv`: The rated voltage of the bus in kilovolts (kV). This is the most important property of a bus.

What to Check (Results):

-   `vm_pu` (`net.res_bus`): The actual voltage magnitude. Why? You must check that this is within a safe range (e.g., 0.95 to 1.05) to ensure equipment operates correctly.

**Line (`net.line`)**: These are the power lines connecting your buses.

What to Define (Inputs):

-   `from_bus` & `to_bus`: The start and end buses for the connection.
-   `length_km`: The length of the line.
-   `std_type`: A standard library type (e.g., "NAYY 4x50 SE") that defines the line's electrical properties (resistance/reactance).

What to Check (Results):

-   `loading_percent` (`net.res_line`): How loaded the line is. Why? You must ensure this is below 100% to prevent overheating and physical damage.
-   Voltage Angle Difference: The difference in `va_degree` between the `from_bus` and `to_bus`. Why? A large difference indicates the line is under high stress and may be approaching its stability limit.

**Load (`net.load`)**: These represent the power consumers in your network.

What to Define (Inputs):

-   `bus`: The bus where the load is connected.
-   `p_mw`: The active power consumed by the load in megawatts (MW).

What to Check (Results):
The `p_mw` and `q_mvar` in `net.res_load` will simply reflect the power consumed, confirming the load was part of the simulation.

**Generator (`net.gen`)**: These are local power sources in your network, like a diesel generator or a power plant.

What to Define (Inputs):

-   `bus`: The bus where the generator is connected.
-   `p_mw`: The active power it supplies to the grid.
-   `vm_pu`: The voltage setpoint it tries to maintain at its bus.

What to Check (Results):

-   `p_mw` and `q_mvar` (`net.res_gen`): The actual active and reactive power the generator is producing to meet the grid's needs

### Typical Values Bus Voltage, Line and Transformer Loading, and Voltage Angle Difference (Across a Line)

**Bus Voltage, `vm_pu` in `net.res_bus`**: This tells you if the voltage level at your connection points is correct. The value is in "per-unit," which is a ratio of the actual voltage to the rated voltage.

-   Ideal: 1.0, the voltage is exactly at its specified rating.
-   Acceptable: 0.95 to 1.05, the standard range for normal operation (±5%).
    -   In Australia, the official range at the connection point is 230V +10%/-6%.
-   Critical: <0.95 or >1.05, low voltage (brownout) can cause motors to run hot and inefficiently, and high voltage and permanently damage components.

**Line and Transformer Loading, `loading_percent`**: This shows you how much of a component's maximum capacity is being used. It is the most important indicator for preventing physical damage.

-   Ideal: <80%, it provides a good safety margin for unexpected changes in load or generation.
-   Acceptable: 80%-100%, While acceptable, running consistently in this range gives you very little room for error or future growth.
-   Critical: >100%, it means the component is overloaded.
    -   For lines, they will overheat and physically sag, which can cause them to touch trees or the ground, leading to a dangerous short-circuit.
    -   For transformers, they will overheat, which rapidly degrades their internal insulation and can lead to catastrophic failure.

**Voltage Angle Difference (Across a Line)**: This isn't a direct pandapower result, but you calculate it by taking the difference between the va_degree at a line's from_bus and to_bus. It is a key indicator of grid stability.

-   Ideal: <20 degrees, a small angle difference means power is flowing easily without stressing the system.
-   Acceptable: 20-30 degrees, this indicates that the connection is becoming stressed. It's working very hard to push power across.
-   Critical: >30 degrees, it can potentially lead to a blackout.
    -   A very large angle difference means the system is on the verge of losing synchronism. If the angle gets too large, the connection between the generator and the load breaks, which can trigger a cascading failure across the grid.

### Complex Network Setup

A complex network, like Melbourne's power grid, can we separated into four layers:

1.  **Transmission Network**

This network transports power from large generators (far outside of the city) to the outskirt of the city.

-   **Voltage**: Very high voltages, typically 220,000 Volts (220 kV) or 500,000 Volts (500 kV).

-   **Key Components**:
    -   Large Generators: Power stations (e.g., gas, renewables) that produce electricity. This is known as `External Grid` or `Generator` in `pandapower`.
    -   Transmission Lines: The large, high-strung power lines in rural areas and along freeways. These are known as `Lines` in `pandapower`.
    -   Terminal Stations: Major hubs that connect the transmission lines and begin the process of stepping down the voltage. This is the connection point between Transmission Network and Sub-transmission Network. These are collections of `Transformers` and `Buses` in `pandapower`.

2.  **Sub-Transmission Network**

This network distributes power across large areas of the city to local zone substations.

-   **Voltage**: High voltages, typically 66,000 Volts (66 kV).

-   **Key Components**:
    -   High-Voltage Transformers: Step voltage down from 220 kV to 66 kV; these transformers are in the terminal stations.
    -   Sub-Transmission Lines: These lines feed the zone substations. They are also known as `Lines` in `pandapower` but with different electrical characteristics from the main transmission lines.
    -   Zone Substations: The connection point between Sub-transmission Network and Distribution Network.

3.  **Distribution Network**

This network runs through suburbs and commercial areas.

-   **Voltage**: Medium voltage, typically 11,000 Volts (11 kV) or 22,000 Volts (22 kV).

-   **Key Components**:
    -   Medium-Voltage Transformers: Step voltage down from 66 kV to 22 kV or 11 kV; these transformers are in the zone substations.
    -   Distribution Feeders: These are the power lines on the streets, running from pole to pole.

4.  **Low Voltage (LV) Network**

This is the final stage. Small transformers on power poles step the medium voltage down to the level used in homes nad businesses.

-   **Voltage**: Low voltage, 400 Volts (three-phase) or 230 Volts (single-phase).

-   **Key Components**:
    -   Distribution Transformers: Small pole-top transformers that step 11/22 kV down to 0.4 kV.
    -   LV Lines: The final cables that connect from the pole to houses.
    -   Loads: The electricity consumers, like houses, offices, and factories. These are known as `Loads` in `pandapower`.
    -   Rooftop Solar: Small, distributed generators. These are known as `Static Generators (sgen)` in `pandapower`.

### A General Steps to Create a `pandapower` Network

1.  Plan out the different network layers and connection to the external grid.

-   For example, in Melbourne, we can separate into four network layers: Transmission network, sub-transmission network, distribution network, and low voltage (LV) network.
-   As outlined in the section above, each layer has different role and voltage level.
-   Each layer is bridge together with transformers (step-down or step-up) at substations.

2.  Create an empty network using `pp.create_empty_network`.

3.  (Optional) Create line and/or transformer standard types using `pp.create_std_type`.

-   If you choose not to create your own lines or transformers, you may choose to look at the available standard line and transformer types via `pp.available_std_types`.

4.  Build each network one by one, including its generators, buses, and loads.

### Short-Circuit Calculations

Short-circuit calculation is a critical analysis used to determine the impact of a fault (like a direct connection to the ground or between wires) on a power grid. `pandapower` provides the `shortcircuit` module, abbreviated as `sc`, to perform these calculations.

The primary function is `sc.calc_sc()`, which simulates a fault at a specified location and calculates the resulting currents and voltages across the network.

#### How `sc.calc_sc` Works

When you run `sc.calc_sc(net, bus=bus_index)`, `pandapower` simulates a bolted three-phase short-circuit at the specified bus. This is the most severe type of fault, where all three electrical phases are shorted together, resulting in the maximum possible fault current.

The calculation determines two key things:

1.  **Initial Symmetrical Short-Circuit Current (`ikss_ka`)**: This is the maximum current that flows at the very instant the fault occurs. It's critical for ensuring that circuit breakers are rated high enough to interrupt the fault safely. If a breaker's rating is too low, it can fail catastrophically.
2.  **Post-Fault Voltages (`vm_pu`)**: The simulation calculates the voltage at every bus in the network *during* the fault. Typically, the voltage at the faulted bus drops to zero, while voltages at nearby buses also drop significantly. This helps identify the extent of the voltage collapse and which parts of the network will be most affected.

#### How to Use `sc.calc_sc`

Using the function is straightforward. Here’s a typical workflow, as seen in `data_driven_network.py`:

1.  **Import the Module**: First, you need to import the `shortcircuit` module.
    ```python
    import pandapower.shortcircuit as sc
    ```

2.  **Identify the Fault Location**: Decide where the fault will occur. In the example, the fault is applied at a bus connected to a specific line.
    ```python
    # The bus where the fault will be simulated
    bus_to_fault = net.line.from_bus.at[line_index]
    ```

3.  **Run the Calculation**: Call `sc.calc_sc()` with the network object and the fault location.
    ```python
    sc.calc_sc(net, bus=bus_to_fault, case='max', branch_results=True)
    ```
    -   `net`: Your `pandapower` network.
    -   `bus`: The index of the bus where the fault occurs.
    -   `case='max'`: This calculates the maximum possible short-circuit currents. This is the standard for safety analysis.
    -   `branch_results=True`: This is a crucial parameter that tells `pandapower` to also calculate the fault currents flowing through lines and transformers, not just at the buses.

#### How to Analyze the Results

After running the calculation, `pandapower` stores the results in new dataframes attached to your `net` object:

1.  **Bus Results (`net.res_bus_sc`)**: This dataframe contains the fault analysis results for each bus.
    -   `ikss_ka`: The initial symmetrical short-circuit current in kiloamperes (kA). This is the most important value for checking equipment ratings. A high value at a bus means any equipment connected there must be able to withstand that current.
    -   `vm_pu`: The voltage magnitude at each bus *during* the fault. You will see that the voltage at the faulted bus is close to 0, and nearby buses have severely depressed voltages.

2.  **Line Results (`net.res_line_sc`)**: This dataframe shows the currents flowing through the power lines during the fault.
    -   `ikss_ka`: The fault current flowing through each line. This is critical for understanding how the fault current spreads through the network. You can identify which lines are carrying the most dangerous currents and might need enhanced protection.

3.  **Transformer Results (`net.res_trafo_sc`)**: If you have transformers, this dataframe shows the fault currents they are subjected to. This is essential for ensuring your transformers are protected.

By analyzing these results, you can answer critical questions like:
- Are my circuit breakers and other protective devices rated to handle the worst-case fault?
- How far does the voltage collapse extend from the fault location?
- Which lines and transformers are most stressed during a fault, and do they have adequate protection?

This analysis is fundamental to designing a safe and reliable power grid.