"""
Airflow calculator for aerodynamic analysis
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Optional


class AirflowCalculator:
    """
    Calculate airflow properties and aerodynamic forces on a vehicle
    """

    def __init__(self, vehicle, air_density=1.225, temperature=15.0, altitude=0.0):
        """
        Initialize the airflow calculator

        Args:
            vehicle: Vehicle object (e.g., Cybertruck instance)
            air_density (float): Air density in kg/m³ (default: sea level, 15°C)
            temperature (float): Air temperature in Celsius (default: 15°C)
            altitude (float): Altitude in meters (default: 0 - sea level)
        """
        self.vehicle = vehicle
        self.altitude = altitude
        self.temperature = temperature

        # Calculate air density based on altitude if at sea level default
        self.air_density = self._calculate_air_density(altitude, temperature)

        # Standard atmospheric pressure (Pa)
        self.atmospheric_pressure = 101325 * math.exp(-altitude / 8400)

        # Dynamic viscosity of air (Pa·s) at given temperature
        self.dynamic_viscosity = self._calculate_dynamic_viscosity(temperature)

    def _calculate_air_density(self, altitude, temperature):
        """
        Calculate air density based on altitude and temperature

        Args:
            altitude (float): Altitude in meters
            temperature (float): Temperature in Celsius

        Returns:
            float: Air density in kg/m³
        """
        # Standard atmosphere model
        T_kelvin = temperature + 273.15
        T_sea_level = 288.15  # 15°C in Kelvin
        p_sea_level = 101325  # Pa

        # Pressure at altitude
        pressure = p_sea_level * math.exp(-altitude / 8400)

        # Air density using ideal gas law
        # ρ = P / (R_specific * T)
        R_specific = 287.05  # J/(kg·K) for dry air
        density = pressure / (R_specific * T_kelvin)

        return density

    def _calculate_dynamic_viscosity(self, temperature):
        """
        Calculate dynamic viscosity of air using Sutherland's formula

        Args:
            temperature (float): Temperature in Celsius

        Returns:
            float: Dynamic viscosity in Pa·s
        """
        T_kelvin = temperature + 273.15
        T_ref = 273.15  # Reference temperature (0°C)
        mu_ref = 1.716e-5  # Reference viscosity at 0°C (Pa·s)
        S = 110.4  # Sutherland's constant for air (K)

        mu = mu_ref * ((T_kelvin / T_ref) ** 1.5) * ((T_ref + S) / (T_kelvin + S))
        return mu

    def calculate_reynolds_number(self, velocity):
        """
        Calculate Reynolds number for the flow

        Args:
            velocity (float): Velocity in m/s

        Returns:
            float: Reynolds number (dimensionless)
        """
        characteristic_length = self.vehicle.length
        Re = (self.air_density * velocity * characteristic_length) / self.dynamic_viscosity
        return Re

    def calculate_drag_force(self, velocity):
        """
        Calculate aerodynamic drag force

        Args:
            velocity (float): Velocity in m/s

        Returns:
            float: Drag force in Newtons
        """
        # F_drag = 0.5 * ρ * v² * Cd * A
        drag_force = 0.5 * self.air_density * (velocity ** 2) * \
                     self.vehicle.drag_coefficient * self.vehicle.frontal_area
        return drag_force

    def calculate_lift_force(self, velocity):
        """
        Calculate aerodynamic lift force (positive = lift, negative = downforce)

        Args:
            velocity (float): Velocity in m/s

        Returns:
            float: Lift force in Newtons
        """
        # F_lift = 0.5 * ρ * v² * Cl * A
        lift_force = 0.5 * self.air_density * (velocity ** 2) * \
                     self.vehicle.lift_coefficient * self.vehicle.frontal_area
        return lift_force

    def calculate_power_required(self, velocity):
        """
        Calculate power required to overcome drag

        Args:
            velocity (float): Velocity in m/s

        Returns:
            float: Power in Watts
        """
        drag_force = self.calculate_drag_force(velocity)
        power = drag_force * velocity
        return power

    def calculate_pressure_coefficient(self, velocity, local_velocity):
        """
        Calculate pressure coefficient at a point

        Args:
            velocity (float): Freestream velocity in m/s
            local_velocity (float): Local velocity at point in m/s

        Returns:
            float: Pressure coefficient (dimensionless)
        """
        # Cp = 1 - (v_local / v_freestream)²
        if velocity == 0:
            return 0
        Cp = 1 - (local_velocity / velocity) ** 2
        return Cp

    def calculate_dynamic_pressure(self, velocity):
        """
        Calculate dynamic pressure

        Args:
            velocity (float): Velocity in m/s

        Returns:
            float: Dynamic pressure in Pa
        """
        q = 0.5 * self.air_density * (velocity ** 2)
        return q

    def calculate_fuel_economy_impact(self, velocity, baseline_consumption, distance=100000):
        """
        Estimate fuel/energy economy impact due to aerodynamic drag

        Args:
            velocity (float): Velocity in m/s
            baseline_consumption (float): Baseline consumption in Wh/km
            distance (float): Distance in meters (default: 100 km)

        Returns:
            dict: Energy consumption analysis
        """
        power_required = self.calculate_power_required(velocity)
        time_hours = distance / (velocity * 3600)
        energy_kwh = (power_required * time_hours) / 1000

        distance_km = distance / 1000
        consumption_per_km = (energy_kwh / distance_km) * 1000  # Wh/km

        return {
            "power_watts": power_required,
            "energy_kwh": energy_kwh,
            "consumption_wh_per_km": consumption_per_km,
            "distance_km": distance_km,
            "time_hours": time_hours
        }

    def analyze_speed_range(self, min_speed=0, max_speed=50, num_points=50):
        """
        Analyze aerodynamic properties over a range of speeds

        Args:
            min_speed (float): Minimum speed in m/s
            max_speed (float): Maximum speed in m/s
            num_points (int): Number of data points

        Returns:
            dict: Analysis results with arrays for each parameter
        """
        speeds = np.linspace(min_speed, max_speed, num_points)

        results = {
            "speeds_ms": speeds,
            "speeds_kmh": speeds * 3.6,
            "speeds_mph": speeds * 2.23694,
            "drag_force_n": [],
            "lift_force_n": [],
            "power_kw": [],
            "reynolds_number": [],
            "dynamic_pressure_pa": []
        }

        for v in speeds:
            results["drag_force_n"].append(self.calculate_drag_force(v))
            results["lift_force_n"].append(self.calculate_lift_force(v))
            results["power_kw"].append(self.calculate_power_required(v) / 1000)
            results["reynolds_number"].append(self.calculate_reynolds_number(v))
            results["dynamic_pressure_pa"].append(self.calculate_dynamic_pressure(v))

        # Convert lists to numpy arrays
        for key in results:
            if isinstance(results[key], list):
                results[key] = np.array(results[key])

        return results

    def estimate_boundary_layer(self, velocity, distance_from_front):
        """
        Estimate boundary layer thickness at a distance from front

        Args:
            velocity (float): Freestream velocity in m/s
            distance_from_front (float): Distance from leading edge in meters

        Returns:
            dict: Boundary layer properties
        """
        Re_x = (self.air_density * velocity * distance_from_front) / self.dynamic_viscosity

        if Re_x < 5e5:  # Laminar flow
            # Blasius boundary layer solution
            delta = 5.0 * distance_from_front / math.sqrt(Re_x)
            regime = "laminar"
        else:  # Turbulent flow
            # Turbulent boundary layer approximation
            delta = 0.37 * distance_from_front / (Re_x ** 0.2)
            regime = "turbulent"

        return {
            "thickness_m": delta,
            "thickness_mm": delta * 1000,
            "reynolds_number": Re_x,
            "regime": regime,
            "distance_from_front_m": distance_from_front
        }

    def get_full_analysis(self, velocity):
        """
        Get comprehensive aerodynamic analysis at a specific velocity

        Args:
            velocity (float): Velocity in m/s

        Returns:
            dict: Complete analysis results
        """
        drag = self.calculate_drag_force(velocity)
        lift = self.calculate_lift_force(velocity)
        power = self.calculate_power_required(velocity)
        reynolds = self.calculate_reynolds_number(velocity)
        dynamic_pressure = self.calculate_dynamic_pressure(velocity)

        return {
            "velocity": {
                "m_s": velocity,
                "km_h": velocity * 3.6,
                "mph": velocity * 2.23694
            },
            "atmospheric_conditions": {
                "density_kg_m3": self.air_density,
                "temperature_c": self.temperature,
                "altitude_m": self.altitude,
                "pressure_pa": self.atmospheric_pressure,
                "dynamic_viscosity_pa_s": self.dynamic_viscosity
            },
            "aerodynamic_forces": {
                "drag_force_n": drag,
                "drag_force_lbf": drag * 0.224809,
                "lift_force_n": lift,
                "lift_force_lbf": lift * 0.224809
            },
            "power_requirements": {
                "power_w": power,
                "power_kw": power / 1000,
                "power_hp": power / 745.7
            },
            "flow_characteristics": {
                "reynolds_number": reynolds,
                "dynamic_pressure_pa": dynamic_pressure,
                "mach_number": velocity / 343.0  # Speed of sound at 15°C
            }
        }
