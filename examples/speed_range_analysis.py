#!/usr/bin/env python3
"""
Analyze performance across a speed range
"""

from airflow_calc import AirflowCalculator, Cybertruck
import json


def main():
    """Analyze speed range with detailed output"""

    print("="*70)
    print("  SPEED RANGE ANALYSIS")
    print("="*70)
    print()

    # Create vehicle and calculator
    truck = Cybertruck(variant="dual_motor")
    calc = AirflowCalculator(truck, altitude=0, temperature=15)

    # Analyze speed range (0 to 140 mph)
    print("Analyzing speed range: 0 to 140 mph (0 to 62.6 m/s)")
    print("Calculating 50 data points...")
    print()

    results = calc.analyze_speed_range(min_speed=0, max_speed=62.6, num_points=50)

    # Display summary statistics
    print("Summary Statistics:")
    print("-" * 70)
    print(f"Speed range: {results['speeds_mph'][0]:.1f} - {results['speeds_mph'][-1]:.1f} mph")
    print(f"Drag range: {results['drag_force_n'][0]:.1f} - {results['drag_force_n'][-1]:.1f} N")
    print(f"Power range: {results['power_kw'][0]:.2f} - {results['power_kw'][-1]:.2f} kW")
    print(f"Max Reynolds: {results['reynolds_number'][-1]:.3e}")
    print()

    # Display sample data points
    print("Sample Data Points:")
    print("-" * 70)
    print(f"{'Speed (mph)':<15} {'Drag (N)':<15} {'Power (kW)':<15} {'Reynolds #':<15}")
    print("-" * 70)

    # Show every 10th point
    for i in range(0, len(results['speeds_mph']), 10):
        speed = results['speeds_mph'][i]
        drag = results['drag_force_n'][i]
        power = results['power_kw'][i]
        reynolds = results['reynolds_number'][i]
        print(f"{speed:<15.1f} {drag:<15.2f} {power:<15.2f} {reynolds:<15.3e}")

    print()

    # Key insights
    print("Key Insights:")
    print("-" * 70)

    # Find speed where power reaches certain thresholds
    thresholds = [10, 20, 30, 50]
    print("Speed required for different power levels:")
    for threshold in thresholds:
        for i, power in enumerate(results['power_kw']):
            if power >= threshold:
                print(f"  {threshold} kW: {results['speeds_mph'][i]:.1f} mph")
                break

    print()

    # Drag doubling analysis
    print("Drag force scaling:")
    base_speed_idx = 25  # Middle of the range
    base_speed = results['speeds_mph'][base_speed_idx]
    base_drag = results['drag_force_n'][base_speed_idx]

    print(f"  At {base_speed:.1f} mph: {base_drag:.1f} N")

    # Find approximately double the speed
    double_speed_idx = min(base_speed_idx * 2, len(results['speeds_mph']) - 1)
    double_speed = results['speeds_mph'][double_speed_idx]
    drag_at_double = results['drag_force_n'][double_speed_idx]

    print(f"  At {double_speed:.1f} mph: {drag_at_double:.1f} N")
    print(f"  Ratio: {drag_at_double/base_drag:.2f}x (theoretical: 4x for doubling speed)")

    print()

    # Export to JSON
    export_filename = "speed_range_results.json"
    print(f"Exporting results to {export_filename}...")

    # Convert numpy arrays to lists for JSON serialization
    export_data = {}
    for key, value in results.items():
        if hasattr(value, 'tolist'):
            export_data[key] = value.tolist()
        else:
            export_data[key] = value

    with open(export_filename, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"Results exported successfully!")
    print()
    print("="*70)


if __name__ == '__main__':
    main()
