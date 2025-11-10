#!/usr/bin/env python3
"""
Compare all three Cybertruck variants
"""

from airflow_calc import AirflowCalculator, Cybertruck


def main():
    """Compare all Cybertruck variants"""

    print("="*70)
    print("  CYBERTRUCK VARIANT COMPARISON")
    print("="*70)
    print()

    # Variants to compare
    variants = ["single_motor", "dual_motor", "tri_motor"]

    # Test speeds
    test_speeds_mph = [30, 50, 65, 80]

    print("Variant Specifications:")
    print("-" * 70)

    for variant in variants:
        truck = Cybertruck(variant=variant)
        specs = truck.get_specs()
        print(f"\n{variant.replace('_', ' ').title()}:")
        print(f"  Mass: {specs['mass_kg']:.0f} kg ({specs['mass_kg'] * 2.20462:.0f} lbs)")
        print(f"  Drag Coefficient: {specs['drag_coefficient']:.2f}")
        print(f"  Frontal Area: {specs['frontal_area_m2']:.2f} m²")

    print("\n" + "="*70)
    print("Performance Comparison at Different Speeds")
    print("="*70)

    for speed_mph in test_speeds_mph:
        speed_ms = speed_mph * 0.44704

        print(f"\nAt {speed_mph} mph:")
        print(f"{'Variant':<20} {'Drag Force (N)':<20} {'Power (kW)':<20}")
        print("-" * 60)

        for variant in variants:
            truck = Cybertruck(variant=variant)
            calc = AirflowCalculator(truck, altitude=0, temperature=15)

            drag = calc.calculate_drag_force(speed_ms)
            power = calc.calculate_power_required(speed_ms) / 1000

            print(f"{variant.replace('_', ' ').title():<20} {drag:<20.2f} {power:<20.2f}")

    print("\n" + "="*70)
    print("Key Observations:")
    print("  • All variants have the same aerodynamics (same Cd and frontal area)")
    print("  • Drag force is identical across variants at the same speed")
    print("  • Mass difference doesn't affect aerodynamic drag")
    print("  • Mass affects rolling resistance and acceleration (not shown here)")
    print("="*70)


if __name__ == '__main__':
    main()
