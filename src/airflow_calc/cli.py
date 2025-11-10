#!/usr/bin/env python3
"""
Command-line interface for Cybertruck Airflow Calculator
"""

import argparse
import sys
import os
from typing import Optional

from .calculator import AirflowCalculator
from .vehicle import Cybertruck
from .utils import (
    mph_to_ms, kmh_to_ms, ms_to_mph, ms_to_kmh,
    print_section_header, print_result_table,
    export_to_json, create_ascii_graph, Colors,
    format_colored, validate_positive_number, validate_speed
)
from . import __version__


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description="Cybertruck Airflow Calculator - Aerodynamic analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze at 65 mph
  airflow-calc -s 65 --unit mph

  # Quick analysis at 100 km/h
  airflow-calc -q -s 100 --unit kmh

  # Full analysis with altitude and temperature
  airflow-calc -s 30 -a 1000 -t 20

  # Speed range analysis from 0 to 120 km/h
  airflow-calc --range 0 120 --unit kmh

  # Export results to JSON
  airflow-calc -s 70 --unit mph -o results.json

  # Different Cybertruck variant
  airflow-calc -s 60 --variant tri_motor --unit mph
        """
    )

    parser.add_argument('-v', '--version', action='version',
                        version=f'Airflow-Calc {__version__}')

    # Speed settings
    speed_group = parser.add_argument_group('Speed Settings')
    speed_group.add_argument('-s', '--speed', type=float,
                            help='Speed value (default unit: m/s)')
    speed_group.add_argument('-u', '--unit', choices=['ms', 'kmh', 'mph'],
                            default='ms', help='Speed unit (default: ms)')
    speed_group.add_argument('--range', nargs=2, type=float, metavar=('MIN', 'MAX'),
                            help='Analyze speed range from MIN to MAX')

    # Vehicle settings
    vehicle_group = parser.add_argument_group('Vehicle Settings')
    vehicle_group.add_argument('--variant', choices=['single_motor', 'dual_motor', 'tri_motor'],
                              default='dual_motor', help='Cybertruck variant (default: dual_motor)')
    vehicle_group.add_argument('--show-specs', action='store_true',
                              help='Show vehicle specifications')

    # Environmental conditions
    env_group = parser.add_argument_group('Environmental Conditions')
    env_group.add_argument('-a', '--altitude', type=float, default=0.0,
                          help='Altitude in meters (default: 0 - sea level)')
    env_group.add_argument('-t', '--temperature', type=float, default=15.0,
                          help='Temperature in Celsius (default: 15)')

    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('-q', '--quick', action='store_true',
                             help='Quick summary output')
    output_group.add_argument('-o', '--output', type=str, metavar='FILE',
                             help='Export results to JSON file')
    output_group.add_argument('--no-color', action='store_true',
                             help='Disable colored output')
    output_group.add_argument('--verbose', action='store_true',
                             help='Verbose output with detailed calculations')

    # Analysis options
    analysis_group = parser.add_argument_group('Analysis Options')
    analysis_group.add_argument('--boundary-layer', type=float, metavar='DISTANCE',
                               help='Calculate boundary layer at distance from front (meters)')
    analysis_group.add_argument('--energy-analysis', action='store_true',
                               help='Include energy consumption analysis')

    return parser


def display_vehicle_specs(vehicle):
    """Display vehicle specifications"""
    print_section_header("CYBERTRUCK SPECIFICATIONS")
    print(vehicle)
    print()


def display_quick_summary(analysis, speed_unit='ms'):
    """Display quick summary of analysis"""
    velocity_data = analysis['velocity']
    forces = analysis['aerodynamic_forces']
    power = analysis['power_requirements']

    print_section_header("QUICK ANALYSIS SUMMARY")

    speed_val = velocity_data[speed_unit] if speed_unit in velocity_data else velocity_data['m_s']
    speed_label = {'ms': 'm/s', 'kmh': 'km/h', 'mph': 'mph'}.get(speed_unit, 'm/s')

    print(f"\nSpeed: {format_colored(f'{speed_val:.1f} {speed_label}', Colors.CYAN)}")
    print(f"Drag Force: {format_colored(f'{forces["drag_force_n"]:.1f} N', Colors.YELLOW)} "
          f"({forces['drag_force_lbf']:.1f} lbf)")
    print(f"Power Required: {format_colored(f'{power["power_kw"]:.2f} kW', Colors.GREEN)} "
          f"({power['power_hp']:.1f} hp)")
    print()


def display_full_analysis(analysis):
    """Display complete analysis results"""
    print_section_header("COMPLETE AERODYNAMIC ANALYSIS")
    print_result_table(analysis)
    print()


def display_speed_range_analysis(results, unit='ms'):
    """Display speed range analysis with graphs"""
    print_section_header("SPEED RANGE ANALYSIS")

    speeds = results[f'speeds_{unit}']
    unit_label = {'ms': 'm/s', 'kmh': 'km/h', 'mph': 'mph'}.get(unit, 'm/s')

    # Sample points for graph (show 5 points)
    indices = [0, len(speeds)//4, len(speeds)//2, 3*len(speeds)//4, -1]
    sample_speeds = [speeds[i] for i in indices]
    sample_drags = [results['drag_force_n'][i] for i in indices]
    sample_powers = [results['power_kw'][i] for i in indices]

    # Drag force graph
    print(f"\n{format_colored('Drag Force vs Speed', Colors.BOLD)}")
    labels = [f"{s:.0f} {unit_label}" for s in sample_speeds]
    print(create_ascii_graph(sample_drags, labels, title="Drag Force (N)"))

    # Power graph
    print(f"\n{format_colored('Power Required vs Speed', Colors.BOLD)}")
    print(create_ascii_graph(sample_powers, labels, title="Power (kW)"))

    # Summary statistics
    print(f"\n{format_colored('Summary Statistics:', Colors.BOLD)}")
    print(f"  Speed Range: {speeds[0]:.1f} - {speeds[-1]:.1f} {unit_label}")
    print(f"  Drag Range: {results['drag_force_n'][0]:.1f} - {results['drag_force_n'][-1]:.1f} N")
    print(f"  Power Range: {results['power_kw'][0]:.2f} - {results['power_kw'][-1]:.2f} kW")
    print(f"  Max Reynolds: {results['reynolds_number'][-1]:.2e}")
    print()


def display_boundary_layer(boundary_layer, velocity):
    """Display boundary layer analysis"""
    print_section_header("BOUNDARY LAYER ANALYSIS")
    print(f"\nVelocity: {velocity:.1f} m/s ({ms_to_kmh(velocity):.1f} km/h)")
    print(f"Distance from front: {boundary_layer['distance_from_front_m']:.2f} m")
    print(f"Flow regime: {format_colored(boundary_layer['regime'].upper(), Colors.CYAN)}")
    print(f"Boundary layer thickness: {boundary_layer['thickness_mm']:.2f} mm")
    print(f"Local Reynolds number: {boundary_layer['reynolds_number']:.2e}")
    print()


def convert_speed(speed, from_unit):
    """Convert speed to m/s"""
    conversions = {
        'ms': lambda x: x,
        'kmh': kmh_to_ms,
        'mph': mph_to_ms
    }
    return conversions[from_unit](speed)


def main():
    """Main CLI entry point"""
    parser = create_parser()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        Colors.disable()

    # Print header
    print(format_colored(f"\n{'='*60}", Colors.BOLD))
    print(format_colored("  CYBERTRUCK AIRFLOW CALCULATOR", Colors.BOLD + Colors.CYAN))
    print(format_colored(f"  Version {__version__}", Colors.BOLD))
    print(format_colored(f"{'='*60}\n", Colors.BOLD))

    try:
        # Initialize vehicle
        vehicle = Cybertruck(variant=args.variant)

        # Show specs if requested
        if args.show_specs:
            display_vehicle_specs(vehicle)
            if args.speed is None and args.range is None:
                return

        # Initialize calculator
        calculator = AirflowCalculator(
            vehicle=vehicle,
            altitude=args.altitude,
            temperature=args.temperature
        )

        # Display environmental conditions
        if args.verbose:
            print_section_header("ENVIRONMENTAL CONDITIONS")
            print(f"Altitude: {args.altitude:.0f} m")
            print(f"Temperature: {args.temperature:.1f} °C")
            print(f"Air density: {calculator.air_density:.4f} kg/m³")
            print(f"Air pressure: {calculator.atmospheric_pressure:.1f} Pa")
            print()

        # Speed range analysis
        if args.range:
            min_speed = convert_speed(args.range[0], args.unit)
            max_speed = convert_speed(args.range[1], args.unit)

            validate_speed(min_speed)
            validate_speed(max_speed)

            results = calculator.analyze_speed_range(min_speed, max_speed, num_points=50)
            display_speed_range_analysis(results, unit=args.unit)

            if args.output:
                # Convert numpy arrays to lists for JSON serialization
                export_data = {k: (v.tolist() if hasattr(v, 'tolist') else v)
                             for k, v in results.items()}
                export_to_json(export_data, args.output)

        # Single speed analysis
        elif args.speed is not None:
            velocity_ms = convert_speed(args.speed, args.unit)
            validate_speed(velocity_ms)

            # Get full analysis
            analysis = calculator.get_full_analysis(velocity_ms)

            # Display results
            if args.quick:
                display_quick_summary(analysis, speed_unit=args.unit)
            else:
                display_full_analysis(analysis)

            # Boundary layer analysis
            if args.boundary_layer:
                distance = validate_positive_number(args.boundary_layer, "distance")
                boundary_layer = calculator.estimate_boundary_layer(velocity_ms, distance)
                display_boundary_layer(boundary_layer, velocity_ms)

            # Energy analysis
            if args.energy_analysis:
                print_section_header("ENERGY CONSUMPTION ANALYSIS")
                baseline = 180  # Wh/km typical for electric vehicles
                energy = calculator.calculate_fuel_economy_impact(
                    velocity_ms, baseline, distance=100000
                )
                print_result_table(energy)
                print()

            # Export if requested
            if args.output:
                export_to_json(analysis, args.output)

        else:
            print(format_colored("Error: Please specify a speed (-s) or speed range (--range)",
                               Colors.RED))
            parser.print_help()
            sys.exit(1)

    except ValueError as e:
        print(format_colored(f"\nError: {e}", Colors.RED))
        sys.exit(1)
    except KeyboardInterrupt:
        print(format_colored("\n\nOperation cancelled by user", Colors.YELLOW))
        sys.exit(0)
    except Exception as e:
        print(format_colored(f"\nUnexpected error: {e}", Colors.RED))
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
