# Cybertruck Airflow Calculator - User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Command-Line Interface](#command-line-interface)
5. [Graphical User Interface](#graphical-user-interface)
6. [Understanding the Results](#understanding-the-results)
7. [Advanced Usage](#advanced-usage)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)
10. [Updating and Uninstalling](#updating-and-uninstalling)

---

## Introduction

The Cybertruck Airflow Calculator is a comprehensive aerodynamic analysis tool designed to calculate airflow properties and aerodynamic forces acting on the Tesla Cybertruck. This tool provides:

- **Drag Force Calculations**: Accurate drag force computation based on vehicle speed
- **Lift Force Analysis**: Calculate aerodynamic lift (or downforce)
- **Power Requirements**: Estimate power needed to overcome air resistance
- **Reynolds Number**: Calculate flow regime characteristics
- **Boundary Layer Analysis**: Estimate boundary layer thickness at various points
- **Energy Consumption**: Analyze impact on vehicle range and efficiency

### Key Features

- ✅ Easy-to-use command-line interface
- ✅ Beautiful graphical user interface with real-time visualization
- ✅ Multiple unit support (m/s, km/h, mph)
- ✅ Environmental condition adjustments (altitude, temperature)
- ✅ Speed range analysis with graphs
- ✅ JSON export capability
- ✅ All three Cybertruck variants supported

---

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection (for initial installation)

### Installation Steps

1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/IceNet-01/Airflow-Calc.git
   cd Airflow-Calc
   ```

2. **Run the installer:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Restart your terminal or source your shell configuration:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc for zsh users
   ```

4. **Verify installation:**
   ```bash
   airflow-calc --version
   ```

---

## Quick Start

### Basic Usage

Calculate airflow at 65 mph:
```bash
airflow-calc -s 65 --unit mph
```

Calculate at 100 km/h:
```bash
airflow-calc -s 100 --unit kmh
```

Quick summary mode:
```bash
airflow-calc -q -s 30
```

### Launch the GUI

For a visual, interactive experience:
```bash
airflow-calc-gui
```

---

## Command-Line Interface

### Basic Syntax

```bash
airflow-calc [OPTIONS]
```

### Speed Settings

| Option | Description | Example |
|--------|-------------|---------|
| `-s, --speed` | Speed value | `-s 65` |
| `-u, --unit` | Speed unit (ms, kmh, mph) | `--unit mph` |
| `--range MIN MAX` | Analyze speed range | `--range 0 120` |

### Vehicle Settings

| Option | Description | Values |
|--------|-------------|--------|
| `--variant` | Cybertruck variant | `single_motor`, `dual_motor`, `tri_motor` |
| `--show-specs` | Display vehicle specs | Flag (no value) |

### Environmental Conditions

| Option | Description | Default |
|--------|-------------|---------|
| `-a, --altitude` | Altitude in meters | 0 (sea level) |
| `-t, --temperature` | Temperature in Celsius | 15°C |

### Output Options

| Option | Description |
|--------|-------------|
| `-q, --quick` | Quick summary output |
| `-o, --output FILE` | Export to JSON file |
| `--no-color` | Disable colored output |
| `--verbose` | Detailed output |

### Analysis Options

| Option | Description | Example |
|--------|-------------|---------|
| `--boundary-layer DIST` | Boundary layer at distance | `--boundary-layer 2.5` |
| `--energy-analysis` | Energy consumption analysis | Flag |

---

## Graphical User Interface

### Launching the GUI

```bash
airflow-calc-gui
```

### GUI Features

1. **Speed Input Section**
   - Enter speed value
   - Select unit (m/s, km/h, mph)
   - Choose Cybertruck variant

2. **Environmental Controls**
   - Set altitude (affects air density)
   - Set temperature (affects air properties)

3. **Visualization Panel**
   - Real-time drag force vs speed graph
   - Power requirements visualization
   - Interactive plots with zoom and pan

4. **Results Display**
   - Drag force in multiple units
   - Lift force calculations
   - Power requirements (kW and hp)
   - Reynolds number
   - Energy consumption estimates

5. **Export Options**
   - Save results to JSON
   - Export graphs as PNG images
   - Copy results to clipboard

---

## Understanding the Results

### Drag Force

The aerodynamic drag force is calculated using:

```
F_drag = 0.5 × ρ × v² × Cd × A
```

Where:
- `ρ` (rho) = air density (kg/m³)
- `v` = velocity (m/s)
- `Cd` = drag coefficient (~0.30 for Cybertruck)
- `A` = frontal area (~4.2 m² for Cybertruck)

**What it means:**
- Higher drag = more resistance to movement
- Drag increases with the **square** of velocity
- Doubling speed = 4× the drag force

### Lift Force

Vertical aerodynamic force (positive = lift, negative = downforce):

```
F_lift = 0.5 × ρ × v² × Cl × A
```

**What it means:**
- Positive lift reduces tire grip
- Negative lift (downforce) improves traction
- Important for stability at high speeds

### Power Requirements

Power needed to overcome drag:

```
P = F_drag × v
```

**What it means:**
- Direct impact on energy consumption
- Power increases with the **cube** of velocity
- Doubling speed = 8× the power requirement

### Reynolds Number

Dimensionless number indicating flow regime:

```
Re = (ρ × v × L) / μ
```

Where:
- `L` = characteristic length (vehicle length)
- `μ` = dynamic viscosity

**Flow regimes:**
- `Re < 5×10⁵`: Laminar flow (smooth, predictable)
- `Re > 5×10⁵`: Turbulent flow (chaotic, higher drag)

### Boundary Layer

Thin layer of air directly affected by the vehicle surface.

**What it means:**
- Thicker boundary layer = more drag
- Transition from laminar to turbulent affects efficiency
- Important for aerodynamic design

---

## Advanced Usage

### Example 1: High-Altitude Analysis

Analyze performance at Denver altitude (1,609 m):

```bash
airflow-calc -s 75 --unit mph -a 1609 -t 15
```

Air density is lower at altitude, resulting in:
- Reduced drag force
- Lower power requirements
- Different cooling requirements

### Example 2: Temperature Effects

Compare cold vs hot conditions:

```bash
# Cold day (-10°C)
airflow-calc -s 100 --unit kmh -t -10

# Hot day (35°C)
airflow-calc -s 100 --unit kmh -t 35
```

### Example 3: Speed Range with Export

Analyze 0-120 mph and export data:

```bash
airflow-calc --range 0 120 --unit mph -o highway_analysis.json
```

### Example 4: Variant Comparison

Compare tri-motor variant:

```bash
airflow-calc -s 80 --unit mph --variant tri_motor --show-specs
```

### Example 5: Complete Analysis

Full analysis with all options:

```bash
airflow-calc -s 70 --unit mph \
  --variant tri_motor \
  -a 500 \
  -t 20 \
  --boundary-layer 3.0 \
  --energy-analysis \
  --verbose \
  -o complete_analysis.json
```

---

## Examples

### City Driving Analysis

Typical city speeds (0-50 km/h):

```bash
airflow-calc --range 0 50 --unit kmh -q
```

### Highway Cruising

Typical highway speed (70 mph):

```bash
airflow-calc -s 70 --unit mph --energy-analysis
```

### Performance Testing

High-speed run (0-160 km/h):

```bash
airflow-calc --range 0 160 --unit kmh -o performance_test.json
```

### Weather Impact Study

Compare drag in different conditions:

```bash
# Sea level, standard conditions
airflow-calc -s 100 --unit kmh -a 0 -t 15

# Mountain driving
airflow-calc -s 100 --unit kmh -a 2000 -t 10

# Desert conditions
airflow-calc -s 100 --unit kmh -a 300 -t 40
```

---

## Troubleshooting

### Command Not Found

**Problem:** `airflow-calc: command not found`

**Solutions:**
1. Restart your terminal
2. Source your shell config: `source ~/.bashrc`
3. Check PATH: `echo $PATH` (should include `~/.local/bin`)
4. Reinstall: `./install.sh`

### Python Version Error

**Problem:** `Python 3.7 or higher is required`

**Solution:**
1. Check Python version: `python3 --version`
2. Install/upgrade Python 3.7+
3. On Ubuntu/Debian: `sudo apt install python3.9`

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
```bash
cd ~/.local/airflow-calc
source venv/bin/activate
pip install -r requirements.txt
```

### GUI Won't Launch

**Problem:** GUI fails to start

**Solution:**
1. Install GUI dependencies: `pip install matplotlib tkinter`
2. Check display: `echo $DISPLAY`
3. For WSL: Install X server (VcXsrv or Xming)

### Incorrect Results

**Problem:** Results seem wrong

**Checks:**
1. Verify speed and unit: `100 mph ≠ 100 km/h`
2. Check variant: Different masses affect calculations
3. Verify altitude: Affects air density significantly
4. Check temperature: Reasonable range is -50°C to 50°C

---

## Updating and Uninstalling

### Updating

Check for and install updates:

```bash
cd Airflow-Calc
bash scripts/update.sh
```

The updater will:
1. Check your current version
2. Fetch the latest version
3. Create a backup
4. Install updates
5. Verify installation

### Manual Update

```bash
git pull origin main
./install.sh
```

### Uninstalling

Complete removal of Airflow Calculator:

```bash
cd Airflow-Calc
bash scripts/uninstall.sh
```

The uninstaller will:
1. Remove installation directory
2. Remove wrapper scripts
3. Clean up backups (optional)
4. Remove PATH modifications (optional)
5. Verify complete removal

### Partial Uninstall

Keep some files:
- Answer "No" when asked about backups
- Answer "No" for PATH modifications

---

## Tips and Best Practices

### 1. Unit Consistency

Always double-check your units:
- US users: `--unit mph`
- International: `--unit kmh`
- Scientific: `--unit ms` (default)

### 2. Realistic Scenarios

For accurate energy estimates:
- Use actual driving conditions (altitude, temperature)
- Consider typical speeds for your area
- Include weather variations

### 3. Data Export

Export important analyses:
```bash
airflow-calc -s 65 --unit mph -o my_analysis.json
```

### 4. Batch Analysis

Create a script for multiple analyses:

```bash
#!/bin/bash
for speed in 40 50 60 70 80; do
  airflow-calc -s $speed --unit mph -o speed_${speed}mph.json
done
```

### 5. GUI for Exploration

- Use CLI for automated/scripted analyses
- Use GUI for interactive exploration
- GUI is great for presentations

---

## Performance Data

### Typical Cybertruck Values (Dual Motor, Sea Level, 15°C)

| Speed | Drag Force | Power | Energy Impact |
|-------|------------|-------|---------------|
| 30 mph (48 km/h) | ~150 N | ~2 kW | Low |
| 50 mph (80 km/h) | ~416 N | ~9.3 kW | Medium |
| 65 mph (105 km/h) | ~707 N | ~20.7 kW | High |
| 80 mph (129 km/h) | ~1,071 N | ~38.6 kW | Very High |
| 100 mph (161 km/h) | ~1,674 N | ~75.4 kW | Extreme |

*Note: These are aerodynamic drag only. Total power includes rolling resistance, drivetrain losses, etc.*

---

## Technical Specifications

### Cybertruck Dimensions

| Parameter | Value |
|-----------|-------|
| Length | 5.885 m (231.7 in) |
| Width | 2.413 m (95.0 in) |
| Height | 1.905 m (75.0 in) |
| Wheelbase | 3.807 m (149.9 in) |
| Frontal Area | ~4.2 m² |
| Drag Coefficient | ~0.30 |

### Calculation Accuracy

- **Drag Force**: ±5% (based on published Cd values)
- **Power Requirements**: ±10% (aerodynamic only)
- **Reynolds Number**: ±2% (atmospheric model accuracy)
- **Boundary Layer**: ±15% (simplified model)

---

## Additional Resources

### Official Documentation
- [GitHub Repository](https://github.com/IceNet-01/Airflow-Calc)
- [Issue Tracker](https://github.com/IceNet-01/Airflow-Calc/issues)

### Learn More About Aerodynamics
- NASA Aerodynamics Tutorial
- Vehicle Aerodynamics Basics
- CFD (Computational Fluid Dynamics) Introduction

### Tesla Cybertruck
- [Tesla Official Site](https://www.tesla.com/cybertruck)
- Technical Specifications
- Performance Data

---

## Support

### Getting Help

1. **Check this guide** - Most questions are answered here
2. **Run with --help** - See all available options
3. **Check examples** - See practical use cases
4. **Report issues** - Use GitHub issue tracker

### Contact

For bugs, feature requests, or questions:
- GitHub Issues: https://github.com/IceNet-01/Airflow-Calc/issues
- Discussions: https://github.com/IceNet-01/Airflow-Calc/discussions

---

## License

This software is released under the MIT License. See LICENSE file for details.

---

## Changelog

### Version 1.0.0 (2025-11-10)

- Initial release
- CLI interface with full functionality
- GUI interface with visualization
- Support for all Cybertruck variants
- Environmental condition adjustments
- Speed range analysis
- JSON export capability
- Comprehensive documentation
- Install/update/uninstall scripts

---

**Happy Calculating! 🚗💨**
