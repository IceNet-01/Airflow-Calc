#!/usr/bin/env python3
"""
Demo script to launch the 3D GUI with various scenarios
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from airflow_calc.gui_3d import main


def print_welcome():
    """Print welcome message"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ⚡ CYBERTRUCK AIRFLOW CALCULATOR 3D ⚡                   ║
║                                                            ║
║   Professional 3D Aerodynamic Analysis Suite               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

Features:
  🎨 Stunning 3D visualization of the Cybertruck
  💨 Interactive airflow streamlines
  📊 Real-time pressure distribution
  🔄 Smooth rotation animations
  📈 Multiple view angles (main, top, side)
  ⚙️ Full environmental control (altitude, temperature)
  💾 Export 3D views and analysis data

Controls:
  • Use sliders to adjust speed, altitude, and temperature
  • Toggle streamlines and pressure visualization
  • Click "ANIMATE" to rotate the 3D view
  • Export your results as JSON or high-res images

Quick Start:
  1. Adjust the speed slider to your desired velocity
  2. Select Cybertruck variant (Single/Dual/Tri motor)
  3. Set environmental conditions
  4. Watch the 3D visualization update in real-time!

Tips:
  • Click and drag in the 3D views to rotate manually
  • Use the matplotlib toolbar to zoom and pan
  • Enable streamlines for dramatic airflow visualization
  • Compare different altitudes to see air density effects

════════════════════════════════════════════════════════════

Launching 3D GUI...
""")


if __name__ == '__main__':
    print_welcome()

    try:
        # Launch the 3D GUI
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Application closed by user")
    except Exception as e:
        print(f"\n✗ Error launching 3D GUI: {e}")
        print("\nTroubleshooting:")
        print("  • Ensure matplotlib is installed: pip install matplotlib")
        print("  • Check that you have a display available (X server)")
        print("  • Try updating matplotlib: pip install --upgrade matplotlib")
        sys.exit(1)
