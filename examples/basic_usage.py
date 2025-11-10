#!/usr/bin/env python3
"""
Basic usage example for Cybertruck Airflow Calculator
"""

from airflow_calc import AirflowCalculator, Cybertruck


def main():
    """Demonstrate basic usage of the calculator"""

    print("="*60)
    print("  CYBERTRUCK AIRFLOW CALCULATOR - BASIC USAGE EXAMPLE")
    print("="*60)
    print()

    # Create a Cybertruck instance
    print("1. Creating Cybertruck instance (dual motor variant)...")
    truck = Cybertruck(variant="dual_motor")
    print(truck)
    print()

    # Create calculator with standard conditions
    print("2. Creating calculator with standard atmospheric conditions...")
    calc = AirflowCalculator(truck, altitude=0, temperature=15)
    print(f"   Air density: {calc.air_density:.4f} kg/m³")
    print(f"   Temperature: {calc.temperature:.1f}°C")
    print()

    # Calculate at highway speed (65 mph = 29.06 m/s)
    speed_mph = 65
    speed_ms = speed_mph * 0.44704
    print(f"3. Analyzing at highway speed ({speed_mph} mph)...")
    print()

    # Calculate drag force
    drag = calc.calculate_drag_force(speed_ms)
    print(f"   Drag Force: {drag:.2f} N ({drag * 0.224809:.2f} lbf)")

    # Calculate lift force
    lift = calc.calculate_lift_force(speed_ms)
    print(f"   Lift Force: {lift:.2f} N ({lift * 0.224809:.2f} lbf)")

    # Calculate power required
    power = calc.calculate_power_required(speed_ms)
    print(f"   Power Required: {power/1000:.2f} kW ({power/745.7:.2f} hp)")

    # Calculate Reynolds number
    reynolds = calc.calculate_reynolds_number(speed_ms)
    print(f"   Reynolds Number: {reynolds:.3e}")
    print()

    # Get full analysis
    print("4. Getting complete analysis...")
    analysis = calc.get_full_analysis(speed_ms)

    print("\n   Full Analysis Results:")
    print(f"   - Dynamic Pressure: {analysis['flow_characteristics']['dynamic_pressure_pa']:.2f} Pa")
    print(f"   - Mach Number: {analysis['flow_characteristics']['mach_number']:.4f}")
    print()

    # Compare different speeds
    print("5. Comparing different speeds...")
    print()
    print(f"   {'Speed (mph)':<15} {'Drag (N)':<15} {'Power (kW)':<15}")
    print(f"   {'-'*15} {'-'*15} {'-'*15}")

    for mph in [30, 50, 65, 80, 100]:
        ms = mph * 0.44704
        d = calc.calculate_drag_force(ms)
        p = calc.calculate_power_required(ms) / 1000
        print(f"   {mph:<15} {d:<15.2f} {p:<15.2f}")

    print()
    print("="*60)
    print("  Example completed successfully!")
    print("="*60)


if __name__ == '__main__':
    main()
