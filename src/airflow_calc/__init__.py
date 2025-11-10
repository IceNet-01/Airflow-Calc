"""
Cybertruck Airflow Calculator
A comprehensive tool for calculating airflow dynamics over the Tesla Cybertruck
"""

__version__ = "1.0.0"
__author__ = "Airflow-Calc Team"

from .calculator import AirflowCalculator
from .vehicle import Cybertruck

__all__ = ['AirflowCalculator', 'Cybertruck']
