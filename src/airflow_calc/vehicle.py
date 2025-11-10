"""
Cybertruck vehicle specifications and geometry
"""

import math


class Cybertruck:
    """
    Tesla Cybertruck specifications and geometric properties
    All measurements in SI units (meters, kg, etc.)
    """

    def __init__(self, variant="dual_motor"):
        """
        Initialize Cybertruck specifications

        Args:
            variant (str): Vehicle variant - "single_motor", "dual_motor", or "tri_motor"
        """
        self.variant = variant

        # Common dimensions (meters)
        self.length = 5.885  # Overall length
        self.width = 2.413   # Overall width (including mirrors)
        self.height = 1.905  # Overall height
        self.wheelbase = 3.807  # Wheelbase
        self.ground_clearance = 0.406  # 16 inches

        # Frontal area estimation (m²)
        # Cybertruck has angular design, frontal area is approximately
        self.frontal_area = 4.2  # Estimated frontal area in m²

        # Drag coefficient (estimated for Cybertruck's angular design)
        # Official: ~0.30 Cd (Tesla claim)
        self.drag_coefficient = 0.30

        # Mass (kg) - varies by variant
        self.mass = self._get_mass()

        # Reference areas for lift calculations
        self.plan_area = self.length * self.width  # Top-down area

        # Lift coefficient (negative = downforce)
        # Angular design may produce different lift characteristics
        self.lift_coefficient = 0.15  # Estimated

    def _get_mass(self):
        """Get vehicle mass based on variant"""
        masses = {
            "single_motor": 2722,  # kg (estimated)
            "dual_motor": 2994,    # kg (estimated)
            "tri_motor": 3266      # kg (estimated)
        }
        return masses.get(self.variant, 2994)

    def get_specs(self):
        """Return dictionary of all specifications"""
        return {
            "variant": self.variant,
            "length_m": self.length,
            "width_m": self.width,
            "height_m": self.height,
            "wheelbase_m": self.wheelbase,
            "ground_clearance_m": self.ground_clearance,
            "frontal_area_m2": self.frontal_area,
            "drag_coefficient": self.drag_coefficient,
            "lift_coefficient": self.lift_coefficient,
            "mass_kg": self.mass,
            "plan_area_m2": self.plan_area
        }

    def __repr__(self):
        return f"Cybertruck({self.variant})"

    def __str__(self):
        specs = self.get_specs()
        output = [f"Tesla Cybertruck - {self.variant.replace('_', ' ').title()}"]
        output.append("=" * 50)
        output.append(f"Length: {self.length:.3f} m ({self.length * 3.28084:.1f} ft)")
        output.append(f"Width: {self.width:.3f} m ({self.width * 3.28084:.1f} ft)")
        output.append(f"Height: {self.height:.3f} m ({self.height * 3.28084:.1f} ft)")
        output.append(f"Mass: {self.mass:.0f} kg ({self.mass * 2.20462:.0f} lbs)")
        output.append(f"Frontal Area: {self.frontal_area:.2f} m²")
        output.append(f"Drag Coefficient (Cd): {self.drag_coefficient:.2f}")
        return "\n".join(output)
