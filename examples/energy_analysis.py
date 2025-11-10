#!/usr/bin/env python3
"""
Energy consumption analysis example
"""

from airflow_calc import AirflowCalculator, Cybertruck


def main():
    """Analyze energy consumption at different speeds"""

    print("="*70)
    print("  ENERGY CONSUMPTION ANALYSIS")
    print("="*70)
    print()

    # Create vehicle and calculator
    truck = Cybertruck(variant="dual_motor")
    calc = AirflowCalculator(truck, altitude=0, temperature=15)

    # Baseline consumption (typical for electric vehicles)
    baseline_consumption = 180  # Wh/km

    # Test scenarios
    scenarios = [
        ("City driving", 30, 50),      # 30 mph, 50 km
        ("Suburban", 45, 100),          # 45 mph, 100 km
        ("Highway cruise", 65, 200),    # 65 mph, 200 km
        ("Fast highway", 80, 150),      # 80 mph, 150 km
    ]

    print("Aerodynamic Energy Consumption Analysis")
    print("-" * 70)
    print()

    total_aero_energy = 0
    total_distance = 0

    for scenario_name, speed_mph, distance_km in scenarios:
        speed_ms = speed_mph * 0.44704
        distance_m = distance_km * 1000

        # Calculate energy impact
        analysis = calc.calculate_fuel_economy_impact(
            velocity=speed_ms,
            baseline_consumption=baseline_consumption,
            distance=distance_m
        )

        print(f"{scenario_name}:")
        print(f"  Speed: {speed_mph} mph ({speed_ms:.1f} m/s)")
        print(f"  Distance: {distance_km} km")
        print(f"  Time: {analysis['time_hours']:.2f} hours")
        print(f"  Aerodynamic drag power: {analysis['power_watts']/1000:.2f} kW")
        print(f"  Aero energy consumption: {analysis['consumption_wh_per_km']:.1f} Wh/km")
        print(f"  Total aero energy: {analysis['energy_kwh']:.2f} kWh")
        print()

        total_aero_energy += analysis['energy_kwh']
        total_distance += distance_km

    print("-" * 70)
    print(f"Total aerodynamic energy: {total_aero_energy:.2f} kWh")
    print(f"Total distance: {total_distance} km")
    print(f"Average aero consumption: {(total_aero_energy/total_distance)*1000:.1f} Wh/km")
    print()

    # Compare speeds for energy efficiency
    print("="*70)
    print("Speed vs Aerodynamic Efficiency")
    print("="*70)
    print()
    print(f"{'Speed (mph)':<15} {'Aero Power (kW)':<20} {'Aero Wh/km':<20} {'Impact':<15}")
    print("-" * 70)

    test_speeds = [25, 35, 45, 55, 65, 75, 85]
    distance_m = 100000  # 100 km

    for speed_mph in test_speeds:
        speed_ms = speed_mph * 0.44704

        analysis = calc.calculate_fuel_economy_impact(
            velocity=speed_ms,
            baseline_consumption=baseline_consumption,
            distance=distance_m
        )

        power_kw = analysis['power_watts'] / 1000
        wh_per_km = analysis['consumption_wh_per_km']

        # Determine impact level
        if wh_per_km < 50:
            impact = "Low"
        elif wh_per_km < 100:
            impact = "Moderate"
        elif wh_per_km < 150:
            impact = "High"
        else:
            impact = "Very High"

        print(f"{speed_mph:<15} {power_kw:<20.2f} {wh_per_km:<20.1f} {impact:<15}")

    print()
    print("Key Insights:")
    print("-" * 70)
    print("  • Aerodynamic drag is the dominant force at highway speeds")
    print("  • Energy consumption increases with the cube of speed")
    print("  • Reducing speed from 75 to 65 mph can save significant energy")
    print("  • At city speeds (25-35 mph), aero drag is minimal")
    print()

    # Calculate range impact
    print("Range Impact Analysis (assuming 100 kWh battery):")
    print("-" * 70)

    battery_capacity = 100  # kWh
    cruise_speed_mph = 65
    cruise_speed_ms = cruise_speed_mph * 0.44704

    # Calculate for different distances until battery is depleted
    power = calc.calculate_power_required(cruise_speed_ms)

    # Simple estimation (aero only)
    time_hours = battery_capacity / (power / 1000)
    range_km = (cruise_speed_ms * time_hours * 3600) / 1000

    print(f"  Cruising at {cruise_speed_mph} mph:")
    print(f"  Aerodynamic power draw: {power/1000:.2f} kW")
    print(f"  Theoretical range (aero only): {range_km:.0f} km ({range_km*0.621371:.0f} miles)")
    print()
    print("  Note: Actual range includes rolling resistance, HVAC, and")
    print("  other factors, typically 350-500 km (217-310 miles)")
    print()
    print("="*70)


if __name__ == '__main__':
    main()
