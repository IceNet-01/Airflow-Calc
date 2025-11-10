# Airflow Calculator Examples

This directory contains example scripts demonstrating various use cases of the Cybertruck Airflow Calculator.

## Running the Examples

Make sure you have installed the airflow-calc package first:

```bash
cd ..
./install.sh
```

Then run any example:

```bash
python3 examples/basic_usage.py
```

## Available Examples

### 1. basic_usage.py

Demonstrates fundamental usage of the calculator library:
- Creating vehicle instances
- Initializing the calculator
- Calculating drag, lift, and power
- Getting Reynolds number
- Comparing multiple speeds

**Run it:**
```bash
python3 examples/basic_usage.py
```

### 2. altitude_comparison.py

Compares aerodynamic performance at different altitudes:
- Sea level vs high altitude
- Air density effects
- Drag force reduction at elevation
- Real-world locations (Denver, Leadville, etc.)

**Run it:**
```bash
python3 examples/altitude_comparison.py
```

**Key Takeaway:** At 3000m altitude, drag is ~30% less than at sea level.

### 3. variant_comparison.py

Compares all three Cybertruck variants:
- Single motor vs dual motor vs tri-motor
- Mass differences
- Aerodynamic performance (spoiler: it's the same!)

**Run it:**
```bash
python3 examples/variant_comparison.py
```

**Key Takeaway:** All variants have identical aerodynamics; mass affects acceleration, not drag.

### 4. speed_range_analysis.py

Analyzes performance across a complete speed range:
- 0 to 140 mph analysis
- 50 data points
- Statistical summary
- JSON export for further analysis

**Run it:**
```bash
python3 examples/speed_range_analysis.py
```

**Output:** Creates `speed_range_results.json` with full data.

### 5. energy_analysis.py

Energy consumption and range analysis:
- Power requirements at different speeds
- Energy consumption per km
- Range impact calculations
- Efficiency insights

**Run it:**
```bash
python3 examples/energy_analysis.py
```

**Key Takeaway:** Energy consumption increases with speed cubed; slowing down saves significant energy.

## Example Output

### Basic Usage
```
==============================================================
  CYBERTRUCK AIRFLOW CALCULATOR - BASIC USAGE EXAMPLE
==============================================================

1. Creating Cybertruck instance (dual motor variant)...
Tesla Cybertruck - Dual Motor
==================================================
Length: 5.885 m (19.3 ft)
Width: 2.413 m (7.9 ft)
Height: 1.905 m (6.3 ft)
Mass: 2994 kg (6600 lbs)
Frontal Area: 4.20 m²
Drag Coefficient (Cd): 0.30

3. Analyzing at highway speed (65 mph)...

   Drag Force: 707.72 N (159.09 lbf)
   Lift Force: 353.86 N (79.54 lbf)
   Power Required: 20.57 kW (27.58 hp)
   Reynolds Number: 7.848e+06
```

## Creating Your Own Examples

Use these examples as templates for your own analysis:

```python
from airflow_calc import AirflowCalculator, Cybertruck

# Create vehicle
truck = Cybertruck(variant="dual_motor")

# Create calculator
calc = AirflowCalculator(truck, altitude=0, temperature=15)

# Calculate at a specific speed (m/s)
speed_ms = 30  # ~67 mph
drag = calc.calculate_drag_force(speed_ms)
power = calc.calculate_power_required(speed_ms)

print(f"Drag: {drag:.2f} N")
print(f"Power: {power/1000:.2f} kW")
```

## Advanced Usage

### Custom Analysis

Create your own analysis scripts:

```python
import numpy as np
from airflow_calc import AirflowCalculator, Cybertruck

# Compare temperature effects
temperatures = np.linspace(-20, 40, 10)
truck = Cybertruck(variant="tri_motor")

for temp in temperatures:
    calc = AirflowCalculator(truck, temperature=temp)
    drag = calc.calculate_drag_force(30)  # 30 m/s
    print(f"Temp: {temp}°C, Drag: {drag:.2f} N")
```

### Export Data

All examples can export data to JSON:

```python
import json

results = calc.analyze_speed_range(0, 50, num_points=100)

# Convert numpy arrays to lists
export_data = {k: (v.tolist() if hasattr(v, 'tolist') else v)
               for k, v in results.items()}

with open('my_results.json', 'w') as f:
    json.dump(export_data, f, indent=2)
```

## Tips

1. **Units:** Always be aware of units. The calculator uses m/s internally. Use conversion functions:
   ```python
   from airflow_calc.utils import mph_to_ms, kmh_to_ms
   speed_ms = mph_to_ms(65)  # Convert 65 mph to m/s
   ```

2. **Environmental Conditions:** Altitude and temperature significantly affect results:
   ```python
   calc_sealevel = AirflowCalculator(truck, altitude=0)
   calc_denver = AirflowCalculator(truck, altitude=1609)
   ```

3. **Speed Ranges:** Use `analyze_speed_range()` for comprehensive analysis:
   ```python
   results = calc.analyze_speed_range(min_speed=0, max_speed=50, num_points=100)
   ```

## Further Reading

- [User Guide](../docs/USER_GUIDE.md) - Complete documentation
- [README](../README.md) - Quick start guide
- API Documentation - Coming soon

## Contributing Examples

Have a interesting use case? Submit a pull request with your example!

Requirements for new examples:
- Clear, commented code
- Descriptive output
- Documentation in this README
- Focus on a specific use case

---

**Questions?** Open an issue at https://github.com/IceNet-01/Airflow-Calc/issues
