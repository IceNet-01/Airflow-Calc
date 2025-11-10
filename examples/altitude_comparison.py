#!/usr/bin/env python3
"""
Compare aerodynamic performance at different altitudes
"""

from airflow_calc import AirflowCalculator, Cybertruck


def main():
    """Compare performance at different altitudes"""

    print("="*70)
    print("  ALTITUDE COMPARISON EXAMPLE")
    print("="*70)
    print()

    # Create vehicle
    truck = Cybertruck(variant="dual_motor")

    # Test speed (70 mph)
    speed_mph = 70
    speed_ms = speed_mph * 0.44704

    # Altitudes to test (in meters)
    altitudes = {
        "Sea Level (Miami)": 0,
        "Low (Chicago)": 180,
        "Medium (Denver)": 1609,
        "High (Albuquerque)": 1619,
        "Very High (Leadville, CO)": 3094
    }

    print(f"Comparing performance at {speed_mph} mph across different altitudes:\n")
    print(f"{'Location':<30} {'Altitude (m)':<15} {'Air Density':<15} {'Drag (N)':<15} {'Power (kW)':<15}")
    print("-" * 85)

    for location, altitude in altitudes.items():
        # Create calculator for this altitude
        calc = AirflowCalculator(truck, altitude=altitude, temperature=15)

        # Calculate forces
        drag = calc.calculate_drag_force(speed_ms)
        power = calc.calculate_power_required(speed_ms) / 1000

        print(f"{location:<30} {altitude:<15.0f} {calc.air_density:<15.4f} {drag:<15.2f} {power:<15.2f}")

    print()
    print("Key Observations:")
    print("  • Air density decreases with altitude")
    print("  • Lower air density = less drag force")
    print("  • Power requirements decrease at high altitude")
    print("  • At 3000m, drag is ~30% less than sea level")
    print()

    # Calculate percentage differences
    calc_sea = AirflowCalculator(truck, altitude=0, temperature=15)
    calc_high = AirflowCalculator(truck, altitude=3094, temperature=15)

    drag_sea = calc_sea.calculate_drag_force(speed_ms)
    drag_high = calc_high.calculate_drag_force(speed_ms)

    reduction = ((drag_sea - drag_high) / drag_sea) * 100

    print(f"Drag reduction at 3094m vs sea level: {reduction:.1f}%")
    print()
    print("="*70)


if __name__ == '__main__':
    main()
