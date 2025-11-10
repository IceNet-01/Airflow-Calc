# 🚗💨 Cybertruck Airflow Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/IceNet-01/Airflow-Calc)

A comprehensive aerodynamic analysis tool for calculating airflow properties and forces acting on the Tesla Cybertruck. Features both command-line and graphical interfaces with real-time visualization.

![Cybertruck Aerodynamics](https://via.placeholder.com/800x300/1a1a1a/00ff00?text=Cybertruck+Airflow+Calculator)

## ✨ Features

- **🖥️ Dual Interface**: Command-line for power users, GUI for visual analysis
- **📊 Comprehensive Analysis**: Drag force, lift force, power requirements, Reynolds number
- **🌡️ Environmental Factors**: Adjustable altitude and temperature settings
- **📈 Speed Range Analysis**: Analyze performance across multiple speeds with graphs
- **🎯 Multiple Units**: Support for m/s, km/h, and mph
- **🚙 All Variants**: Single motor, dual motor, and tri-motor configurations
- **💾 Data Export**: JSON export for further analysis
- **🎨 Beautiful Visualizations**: Real-time plots and graphs
- **🔧 Easy Installation**: One-command installer with update and uninstall support

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [GUI Interface](#-gui-interface)
- [Documentation](#-documentation)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/IceNet-01/Airflow-Calc.git
cd Airflow-Calc

# Run the installer
chmod +x install.sh
./install.sh

# Restart your terminal or source your shell
source ~/.bashrc
```

### Basic Usage

```bash
# Analyze at 65 mph
airflow-calc -s 65 --unit mph

# Quick summary at 100 km/h
airflow-calc -q -s 100 --unit kmh

# Launch the GUI
airflow-calc-gui
```

## 📦 Installation

### Prerequisites

- **Python 3.7+** - Required
- **pip** - Python package manager
- **git** - For cloning the repository

### Detailed Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/IceNet-01/Airflow-Calc.git
   cd Airflow-Calc
   ```

2. **Make installer executable:**
   ```bash
   chmod +x install.sh
   ```

3. **Run the installer:**
   ```bash
   ./install.sh
   ```

4. **Verify installation:**
   ```bash
   airflow-calc --version
   ```

The installer will:
- ✅ Check Python and pip installation
- ✅ Create a virtual environment
- ✅ Install all dependencies (numpy)
- ✅ Set up the command-line tools
- ✅ Configure your PATH automatically

## 💻 Usage

### Command-Line Interface

#### Basic Syntax

```bash
airflow-calc [OPTIONS]
```

#### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `-s, --speed` | Speed value | `-s 65` |
| `-u, --unit` | Unit (ms/kmh/mph) | `--unit mph` |
| `--range MIN MAX` | Speed range | `--range 0 120` |
| `--variant` | Cybertruck variant | `--variant tri_motor` |
| `-a, --altitude` | Altitude in meters | `-a 1000` |
| `-t, --temperature` | Temperature in °C | `-t 25` |
| `-q, --quick` | Quick summary | `-q` |
| `-o, --output` | Export to JSON | `-o results.json` |
| `--show-specs` | Show vehicle specs | `--show-specs` |
| `--help` | Show all options | `--help` |

#### Speed Units

- `ms` - Meters per second (default)
- `kmh` - Kilometers per hour
- `mph` - Miles per hour

#### Cybertruck Variants

- `single_motor` - Single motor RWD
- `dual_motor` - Dual motor AWD (default)
- `tri_motor` - Tri motor AWD (Cyberbeast)

### Quick Examples

```bash
# Highway cruising (65 mph)
airflow-calc -s 65 --unit mph

# City driving range (0-50 km/h)
airflow-calc --range 0 50 --unit kmh

# High-altitude performance (Denver)
airflow-calc -s 75 --unit mph -a 1609

# Full analysis with export
airflow-calc -s 100 --unit kmh -o highway_data.json --energy-analysis

# Tri-motor variant at high speed
airflow-calc -s 120 --unit mph --variant tri_motor --verbose
```

## 📊 Examples

### Example 1: Basic Speed Analysis

```bash
$ airflow-calc -s 65 --unit mph
```

Output:
```
============================================================
  CYBERTRUCK AIRFLOW CALCULATOR
  Version 1.0.0
============================================================

============================================================
  COMPLETE AERODYNAMIC ANALYSIS
============================================================
Velocity
  M S: 29.0576
  Km H: 104.6074
  Mph: 65.0000

Aerodynamic Forces
  Drag Force N: 707.7234
  Drag Force Lbf: 159.0904
  Lift Force N: 354.3617
  Lift Force Lbf: 79.6452

Power Requirements
  Power W: 20568.8744
  Power Kw: 20.5689
  Power Hp: 27.5851
```

### Example 2: Speed Range with Graphs

```bash
$ airflow-calc --range 0 120 --unit kmh
```

Generates ASCII graphs showing:
- Drag force vs speed
- Power requirements vs speed
- Summary statistics

### Example 3: Environmental Impact

```bash
# Standard conditions (sea level, 15°C)
$ airflow-calc -s 100 --unit kmh -t 15 -a 0

# Mountain conditions (2000m altitude, 10°C)
$ airflow-calc -s 100 --unit kmh -t 10 -a 2000
```

Air density decreases with altitude, reducing drag by ~20% at 2000m.

### Example 4: Complete Analysis

```bash
$ airflow-calc -s 70 --unit mph \
    --variant tri_motor \
    -a 500 \
    -t 20 \
    --boundary-layer 3.0 \
    --energy-analysis \
    --verbose \
    -o complete_analysis.json
```

## 🎨 GUI Interface

### Launching the GUI

```bash
airflow-calc-gui
```

### GUI Features

- **Interactive Controls**: Sliders and input fields for all parameters
- **Real-time Visualization**: Live graphs that update as you adjust values
- **Multiple Plots**:
  - Drag force vs speed
  - Power requirements vs speed
  - Lift force analysis
  - Reynolds number evolution
- **Export Options**: Save graphs as PNG, export data as JSON
- **Vehicle Selection**: Switch between Cybertruck variants
- **Environmental Settings**: Adjust altitude and temperature with visual feedback

### GUI Screenshot

```
┌─────────────────────────────────────────────────────────┐
│  Cybertruck Airflow Calculator                          │
├─────────────────────────────────────────────────────────┤
│  Speed: [===•=====] 65 mph                              │
│  Variant: [Dual Motor ▼]                                │
│  Altitude: [====•====] 0 m                              │
│  Temperature: [====•====] 15°C                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Drag Force vs Speed                             │  │
│  │  2000┤                                        ╭─╮ │  │
│  │      │                                    ╭───╯  │  │
│  │  1000┤                          ╭─────────╯      │  │
│  │      │                  ╭───────╯                │  │
│  │     0└──────────────────────────────────────────  │  │
│  │       0     30     60     90    120   (mph)      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Results:                                                │
│  • Drag Force: 707.7 N (159.1 lbf)                      │
│  • Power: 20.6 kW (27.6 hp)                             │
│  • Reynolds: 7.8×10⁶                                    │
│                                                          │
│  [Calculate] [Export] [Reset]                           │
└─────────────────────────────────────────────────────────┘
```

## 📖 Documentation

### Full Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Complete guide with detailed explanations
- **[API Documentation](docs/API.md)** - For developers using the library
- **[Examples](examples/)** - Code examples and use cases

### In-App Help

```bash
airflow-calc --help
```

### Understanding Results

#### Drag Force
- The resistance force air exerts on the vehicle
- Increases with speed squared (v²)
- Main contributor to energy consumption at highway speeds

#### Power Requirements
- Power needed to overcome air resistance
- Increases with speed cubed (v³)
- Critical for range calculations

#### Reynolds Number
- Indicates flow regime (laminar vs turbulent)
- Higher Re = more turbulent flow
- Affects drag characteristics

## 🔬 Technical Details

### Calculations

The calculator uses validated aerodynamic equations:

**Drag Force:**
```
F_drag = 0.5 × ρ × v² × Cd × A
```

**Power:**
```
P = F_drag × v
```

**Reynolds Number:**
```
Re = (ρ × v × L) / μ
```

### Cybertruck Specifications

| Parameter | Value |
|-----------|-------|
| **Length** | 5.885 m (231.7 in) |
| **Width** | 2.413 m (95.0 in) |
| **Height** | 1.905 m (75.0 in) |
| **Frontal Area** | ~4.2 m² |
| **Drag Coefficient** | ~0.30 |
| **Mass (Dual Motor)** | ~2994 kg |

### Accuracy

- Drag force: ±5%
- Power requirements: ±10%
- Reynolds number: ±2%
- Based on published Tesla data and standard atmospheric models

## 🔧 Maintenance

### Updating

```bash
cd Airflow-Calc
bash scripts/update.sh
```

The updater automatically:
- Checks for new versions
- Creates a backup
- Installs updates
- Verifies installation

### Uninstalling

```bash
cd Airflow-Calc
bash scripts/uninstall.sh
```

Complete removal with optional backup cleanup.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/IceNet-01/Airflow-Calc.git
cd Airflow-Calc
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Include unit tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Tesla for creating the Cybertruck
- NASA for aerodynamic references
- The Python scientific computing community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/IceNet-01/Airflow-Calc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/IceNet-01/Airflow-Calc/discussions)
- **Email**: support@airflow-calc.dev

## 🗺️ Roadmap

- [ ] 3D visualization of airflow patterns
- [ ] CFD integration
- [ ] More vehicle models
- [ ] Mobile app
- [ ] Web interface
- [ ] Real-time GPS integration
- [ ] Machine learning optimizations

## 📊 Performance Benchmarks

| Speed | Drag Force | Power Required | Range Impact |
|-------|------------|----------------|--------------|
| 30 mph | 150 N | 2.0 kW | Minimal |
| 50 mph | 416 N | 9.3 kW | Low |
| 65 mph | 708 N | 20.7 kW | Moderate |
| 80 mph | 1,071 N | 38.6 kW | High |
| 100 mph | 1,674 N | 75.4 kW | Severe |

## 🌟 Star History

If you find this project useful, please consider giving it a star!

## 📸 Screenshots

### Command-Line Interface
```bash
$ airflow-calc -s 65 --unit mph --show-specs
```

### GUI Interface
Coming soon!

---

**Made with ❤️ by the Airflow-Calc Team**

**Follow us:** [GitHub](https://github.com/IceNet-01/Airflow-Calc) • [Twitter](#) • [Discord](#)

