#!/usr/bin/env python3
"""
Graphical User Interface for Cybertruck Airflow Calculator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import json
from datetime import datetime

from .calculator import AirflowCalculator
from .vehicle import Cybertruck
from .utils import mph_to_ms, kmh_to_ms, ms_to_mph, ms_to_kmh
from . import __version__


class AirflowCalculatorGUI:
    """
    Main GUI application for Airflow Calculator
    """

    def __init__(self, root):
        self.root = root
        self.root.title(f"Cybertruck Airflow Calculator v{__version__}")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        # Set color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'fg': '#e0e0e0',
            'accent': '#00ff00',
            'secondary': '#00aa00',
            'dark': '#0d0d0d',
            'light': '#2a2a2a',
            'error': '#ff0000',
            'warning': '#ffaa00',
            'info': '#00aaff'
        }

        # Configure style
        self.setup_style()

        # Initialize variables
        self.speed_var = tk.DoubleVar(value=65.0)
        self.unit_var = tk.StringVar(value='mph')
        self.variant_var = tk.StringVar(value='dual_motor')
        self.altitude_var = tk.DoubleVar(value=0.0)
        self.temperature_var = tk.DoubleVar(value=15.0)

        # Results storage
        self.current_analysis = None

        # Create GUI components
        self.create_header()
        self.create_input_panel()
        self.create_visualization_panel()
        self.create_results_panel()
        self.create_status_bar()

        # Initial calculation
        self.calculate()

    def setup_style(self):
        """Configure ttk style"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton', background=self.colors['secondary'], foreground=self.colors['fg'])
        style.map('TButton', background=[('active', self.colors['accent'])])
        style.configure('Header.TLabel', font=('Arial', 20, 'bold'), foreground=self.colors['accent'])
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'), foreground=self.colors['accent'])
        style.configure('Result.TLabel', font=('Arial', 11), foreground=self.colors['fg'])

    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title = ttk.Label(header_frame, text="🚗💨 CYBERTRUCK AIRFLOW CALCULATOR",
                         style='Header.TLabel')
        title.pack()

        subtitle = ttk.Label(header_frame, text=f"Version {__version__} • Aerodynamic Analysis Tool")
        subtitle.pack()

    def create_input_panel(self):
        """Create input controls panel"""
        # Main container
        container = ttk.Frame(self.root)
        container.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)

        # Speed section
        speed_frame = ttk.LabelFrame(container, text="  Speed Settings  ", padding=10)
        speed_frame.pack(fill=tk.X, pady=5)

        # Speed value
        ttk.Label(speed_frame, text="Speed:").grid(row=0, column=0, sticky=tk.W, pady=5)
        speed_spinbox = ttk.Spinbox(speed_frame, from_=0, to=200, textvariable=self.speed_var,
                                    width=10, command=self.on_input_change)
        speed_spinbox.grid(row=0, column=1, padx=5, pady=5)

        # Unit selector
        ttk.Label(speed_frame, text="Unit:").grid(row=1, column=0, sticky=tk.W, pady=5)
        unit_combo = ttk.Combobox(speed_frame, textvariable=self.unit_var,
                                  values=['mph', 'kmh', 'ms'], width=8, state='readonly')
        unit_combo.grid(row=1, column=1, padx=5, pady=5)
        unit_combo.bind('<<ComboboxSelected>>', lambda e: self.on_input_change())

        # Speed slider
        speed_slider = tk.Scale(speed_frame, from_=0, to=200, orient=tk.HORIZONTAL,
                               variable=self.speed_var, command=lambda v: self.on_input_change(),
                               length=250, bg=self.colors['light'], fg=self.colors['fg'],
                               activebackground=self.colors['accent'], troughcolor=self.colors['dark'])
        speed_slider.grid(row=2, column=0, columnspan=2, pady=5)

        # Vehicle section
        vehicle_frame = ttk.LabelFrame(container, text="  Vehicle Configuration  ", padding=10)
        vehicle_frame.pack(fill=tk.X, pady=5)

        ttk.Label(vehicle_frame, text="Variant:").grid(row=0, column=0, sticky=tk.W, pady=5)
        variant_combo = ttk.Combobox(vehicle_frame, textvariable=self.variant_var,
                                     values=['single_motor', 'dual_motor', 'tri_motor'],
                                     width=18, state='readonly')
        variant_combo.grid(row=0, column=1, padx=5, pady=5)
        variant_combo.bind('<<ComboboxSelected>>', lambda e: self.on_input_change())

        # Show specs button
        specs_btn = ttk.Button(vehicle_frame, text="Show Specifications",
                              command=self.show_vehicle_specs)
        specs_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # Environmental section
        env_frame = ttk.LabelFrame(container, text="  Environmental Conditions  ", padding=10)
        env_frame.pack(fill=tk.X, pady=5)

        # Altitude
        ttk.Label(env_frame, text="Altitude (m):").grid(row=0, column=0, sticky=tk.W, pady=5)
        alt_spinbox = ttk.Spinbox(env_frame, from_=0, to=5000, textvariable=self.altitude_var,
                                  width=10, command=self.on_input_change)
        alt_spinbox.grid(row=0, column=1, padx=5, pady=5)

        alt_slider = tk.Scale(env_frame, from_=0, to=5000, orient=tk.HORIZONTAL,
                             variable=self.altitude_var, command=lambda v: self.on_input_change(),
                             length=250, bg=self.colors['light'], fg=self.colors['fg'],
                             activebackground=self.colors['info'], troughcolor=self.colors['dark'])
        alt_slider.grid(row=1, column=0, columnspan=2, pady=5)

        # Temperature
        ttk.Label(env_frame, text="Temperature (°C):").grid(row=2, column=0, sticky=tk.W, pady=5)
        temp_spinbox = ttk.Spinbox(env_frame, from_=-50, to=50, textvariable=self.temperature_var,
                                   width=10, command=self.on_input_change)
        temp_spinbox.grid(row=2, column=1, padx=5, pady=5)

        temp_slider = tk.Scale(env_frame, from_=-50, to=50, orient=tk.HORIZONTAL,
                              variable=self.temperature_var, command=lambda v: self.on_input_change(),
                              length=250, bg=self.colors['light'], fg=self.colors['fg'],
                              activebackground=self.colors['warning'], troughcolor=self.colors['dark'])
        temp_slider.grid(row=3, column=0, columnspan=2, pady=5)

        # Action buttons
        action_frame = ttk.Frame(container)
        action_frame.pack(fill=tk.X, pady=10)

        ttk.Button(action_frame, text="Calculate", command=self.calculate,
                  width=15).pack(pady=5)
        ttk.Button(action_frame, text="Export JSON", command=self.export_json,
                  width=15).pack(pady=5)
        ttk.Button(action_frame, text="Export Graph", command=self.export_graph,
                  width=15).pack(pady=5)
        ttk.Button(action_frame, text="Reset", command=self.reset,
                  width=15).pack(pady=5)

    def create_visualization_panel(self):
        """Create matplotlib visualization panel"""
        viz_frame = ttk.Frame(self.root)
        viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create figure with multiple subplots
        self.fig = Figure(figsize=(10, 8), facecolor=self.colors['bg'])

        # Create subplots
        self.ax1 = self.fig.add_subplot(221, facecolor=self.colors['light'])
        self.ax2 = self.fig.add_subplot(222, facecolor=self.colors['light'])
        self.ax3 = self.fig.add_subplot(223, facecolor=self.colors['light'])
        self.ax4 = self.fig.add_subplot(224, facecolor=self.colors['light'])

        # Configure axes colors
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.tick_params(colors=self.colors['fg'])
            ax.spines['bottom'].set_color(self.colors['fg'])
            ax.spines['top'].set_color(self.colors['fg'])
            ax.spines['left'].set_color(self.colors['fg'])
            ax.spines['right'].set_color(self.colors['fg'])
            ax.xaxis.label.set_color(self.colors['fg'])
            ax.yaxis.label.set_color(self.colors['fg'])
            ax.title.set_color(self.colors['accent'])

        self.fig.tight_layout(pad=3.0)

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, viz_frame)
        toolbar.update()

    def create_results_panel(self):
        """Create results display panel"""
        results_frame = ttk.LabelFrame(self.root, text="  Analysis Results  ", padding=10)
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=5)

        # Create text widget for results
        self.results_text = tk.Text(results_frame, width=35, height=40,
                                    bg=self.colors['dark'], fg=self.colors['fg'],
                                    font=('Courier', 10), wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)

        # Configure text tags for colors
        self.results_text.tag_config('header', foreground=self.colors['accent'], font=('Courier', 11, 'bold'))
        self.results_text.tag_config('label', foreground=self.colors['info'])
        self.results_text.tag_config('value', foreground=self.colors['fg'], font=('Courier', 10, 'bold'))

    def create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_input_change(self):
        """Handle input changes"""
        # Auto-calculate on change
        self.root.after(300, self.calculate)  # Debounce

    def calculate(self):
        """Perform aerodynamic calculations"""
        try:
            # Get input values
            speed = self.speed_var.get()
            unit = self.unit_var.get()
            variant = self.variant_var.get()
            altitude = self.altitude_var.get()
            temperature = self.temperature_var.get()

            # Convert speed to m/s
            if unit == 'mph':
                speed_ms = mph_to_ms(speed)
            elif unit == 'kmh':
                speed_ms = kmh_to_ms(speed)
            else:
                speed_ms = speed

            # Create vehicle and calculator
            vehicle = Cybertruck(variant=variant)
            calculator = AirflowCalculator(vehicle, altitude=altitude, temperature=temperature)

            # Perform analysis
            self.current_analysis = calculator.get_full_analysis(speed_ms)

            # Update visualizations
            self.update_plots(calculator, speed_ms)

            # Update results display
            self.update_results_display()

            self.status_var.set(f"✓ Calculated at {speed:.1f} {unit}")

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error during calculation:\n{str(e)}")
            self.status_var.set("✗ Calculation failed")

    def update_plots(self, calculator, current_speed):
        """Update all plots"""
        # Generate speed range data
        max_speed = max(current_speed * 1.5, 50)
        results = calculator.analyze_speed_range(0, max_speed, num_points=100)

        unit = self.unit_var.get()
        if unit == 'mph':
            speeds = results['speeds_mph']
            unit_label = 'mph'
        elif unit == 'kmh':
            speeds = results['speeds_kmh']
            unit_label = 'km/h'
        else:
            speeds = results['speeds_ms']
            unit_label = 'm/s'

        # Clear all axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Plot 1: Drag Force vs Speed
        self.ax1.plot(speeds, results['drag_force_n'], color=self.colors['accent'], linewidth=2)
        self.ax1.axvline(x=speeds[int(current_speed/max_speed*100)], color=self.colors['warning'],
                         linestyle='--', linewidth=1.5, label='Current Speed')
        self.ax1.set_xlabel(f'Speed ({unit_label})')
        self.ax1.set_ylabel('Drag Force (N)')
        self.ax1.set_title('Drag Force vs Speed')
        self.ax1.grid(True, alpha=0.3, color=self.colors['fg'])
        self.ax1.legend()

        # Plot 2: Power Requirements vs Speed
        self.ax2.plot(speeds, results['power_kw'], color=self.colors['info'], linewidth=2)
        self.ax2.axvline(x=speeds[int(current_speed/max_speed*100)], color=self.colors['warning'],
                         linestyle='--', linewidth=1.5, label='Current Speed')
        self.ax2.set_xlabel(f'Speed ({unit_label})')
        self.ax2.set_ylabel('Power (kW)')
        self.ax2.set_title('Power Required vs Speed')
        self.ax2.grid(True, alpha=0.3, color=self.colors['fg'])
        self.ax2.legend()

        # Plot 3: Lift Force vs Speed
        self.ax3.plot(speeds, results['lift_force_n'], color=self.colors['warning'], linewidth=2)
        self.ax3.axvline(x=speeds[int(current_speed/max_speed*100)], color=self.colors['warning'],
                         linestyle='--', linewidth=1.5, label='Current Speed')
        self.ax3.axhline(y=0, color=self.colors['fg'], linestyle='-', linewidth=0.5)
        self.ax3.set_xlabel(f'Speed ({unit_label})')
        self.ax3.set_ylabel('Lift Force (N)')
        self.ax3.set_title('Lift Force vs Speed')
        self.ax3.grid(True, alpha=0.3, color=self.colors['fg'])
        self.ax3.legend()

        # Plot 4: Reynolds Number vs Speed
        self.ax4.plot(speeds, results['reynolds_number'], color='#ff00ff', linewidth=2)
        self.ax4.axvline(x=speeds[int(current_speed/max_speed*100)], color=self.colors['warning'],
                         linestyle='--', linewidth=1.5, label='Current Speed')
        self.ax4.axhline(y=5e5, color=self.colors['error'], linestyle=':', linewidth=1,
                         label='Turbulent Transition')
        self.ax4.set_xlabel(f'Speed ({unit_label})')
        self.ax4.set_ylabel('Reynolds Number')
        self.ax4.set_title('Reynolds Number vs Speed')
        self.ax4.set_yscale('log')
        self.ax4.grid(True, alpha=0.3, color=self.colors['fg'])
        self.ax4.legend()

        # Reconfigure axes colors (they get reset on clear)
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.tick_params(colors=self.colors['fg'])
            ax.spines['bottom'].set_color(self.colors['fg'])
            ax.spines['top'].set_color(self.colors['fg'])
            ax.spines['left'].set_color(self.colors['fg'])
            ax.spines['right'].set_color(self.colors['fg'])
            ax.xaxis.label.set_color(self.colors['fg'])
            ax.yaxis.label.set_color(self.colors['fg'])
            ax.title.set_color(self.colors['accent'])
            ax.set_facecolor(self.colors['light'])

        self.fig.tight_layout(pad=3.0)
        self.canvas.draw()

    def update_results_display(self):
        """Update results text display"""
        if not self.current_analysis:
            return

        self.results_text.delete(1.0, tk.END)

        # Header
        self.results_text.insert(tk.END, "╔═══════════════════════════════╗\n", 'header')
        self.results_text.insert(tk.END, "║   AERODYNAMIC ANALYSIS RESULTS   ║\n", 'header')
        self.results_text.insert(tk.END, "╚═══════════════════════════════╝\n\n", 'header')

        # Velocity
        vel = self.current_analysis['velocity']
        self.results_text.insert(tk.END, "─── VELOCITY ───\n", 'header')
        self.results_text.insert(tk.END, f"  {vel['m_s']:.2f} m/s\n", 'value')
        self.results_text.insert(tk.END, f"  {vel['km_h']:.2f} km/h\n", 'value')
        self.results_text.insert(tk.END, f"  {vel['mph']:.2f} mph\n\n", 'value')

        # Aerodynamic Forces
        forces = self.current_analysis['aerodynamic_forces']
        self.results_text.insert(tk.END, "─── AERODYNAMIC FORCES ───\n", 'header')
        self.results_text.insert(tk.END, "Drag Force:\n", 'label')
        self.results_text.insert(tk.END, f"  {forces['drag_force_n']:.2f} N\n", 'value')
        self.results_text.insert(tk.END, f"  {forces['drag_force_lbf']:.2f} lbf\n\n", 'value')
        self.results_text.insert(tk.END, "Lift Force:\n", 'label')
        self.results_text.insert(tk.END, f"  {forces['lift_force_n']:.2f} N\n", 'value')
        self.results_text.insert(tk.END, f"  {forces['lift_force_lbf']:.2f} lbf\n\n", 'value')

        # Power Requirements
        power = self.current_analysis['power_requirements']
        self.results_text.insert(tk.END, "─── POWER REQUIREMENTS ───\n", 'header')
        self.results_text.insert(tk.END, f"  {power['power_w']:.1f} W\n", 'value')
        self.results_text.insert(tk.END, f"  {power['power_kw']:.2f} kW\n", 'value')
        self.results_text.insert(tk.END, f"  {power['power_hp']:.2f} hp\n\n", 'value')

        # Flow Characteristics
        flow = self.current_analysis['flow_characteristics']
        self.results_text.insert(tk.END, "─── FLOW CHARACTERISTICS ───\n", 'header')
        self.results_text.insert(tk.END, "Reynolds Number:\n", 'label')
        self.results_text.insert(tk.END, f"  {flow['reynolds_number']:.3e}\n", 'value')
        self.results_text.insert(tk.END, "Dynamic Pressure:\n", 'label')
        self.results_text.insert(tk.END, f"  {flow['dynamic_pressure_pa']:.2f} Pa\n", 'value')
        self.results_text.insert(tk.END, "Mach Number:\n", 'label')
        self.results_text.insert(tk.END, f"  {flow['mach_number']:.4f}\n\n", 'value')

        # Atmospheric Conditions
        atm = self.current_analysis['atmospheric_conditions']
        self.results_text.insert(tk.END, "─── ATMOSPHERIC CONDITIONS ───\n", 'header')
        self.results_text.insert(tk.END, f"Density: {atm['density_kg_m3']:.4f} kg/m³\n", 'value')
        self.results_text.insert(tk.END, f"Temperature: {atm['temperature_c']:.1f} °C\n", 'value')
        self.results_text.insert(tk.END, f"Altitude: {atm['altitude_m']:.0f} m\n", 'value')
        self.results_text.insert(tk.END, f"Pressure: {atm['pressure_pa']:.1f} Pa\n\n", 'value')

        # Timestamp
        self.results_text.insert(tk.END, f"\n{'─'*35}\n", 'label')
        self.results_text.insert(tk.END, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", 'label')

    def show_vehicle_specs(self):
        """Show vehicle specifications in a dialog"""
        vehicle = Cybertruck(variant=self.variant_var.get())
        specs_window = tk.Toplevel(self.root)
        specs_window.title("Cybertruck Specifications")
        specs_window.geometry("500x400")
        specs_window.configure(bg=self.colors['bg'])

        text = tk.Text(specs_window, bg=self.colors['dark'], fg=self.colors['fg'],
                      font=('Courier', 10), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text.insert(tk.END, str(vehicle))
        text.config(state=tk.DISABLED)

    def export_json(self):
        """Export results to JSON file"""
        if not self.current_analysis:
            messagebox.showwarning("No Data", "Please calculate results first")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_analysis, f, indent=2)
                messagebox.showinfo("Success", f"Results exported to:\n{filename}")
                self.status_var.set(f"✓ Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")

    def export_graph(self):
        """Export graph to image file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if filename:
            try:
                self.fig.savefig(filename, dpi=300, facecolor=self.colors['bg'])
                messagebox.showinfo("Success", f"Graph exported to:\n{filename}")
                self.status_var.set(f"✓ Graph saved to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export graph:\n{str(e)}")

    def reset(self):
        """Reset to default values"""
        self.speed_var.set(65.0)
        self.unit_var.set('mph')
        self.variant_var.set('dual_motor')
        self.altitude_var.set(0.0)
        self.temperature_var.set(15.0)
        self.calculate()
        self.status_var.set("Reset to default values")


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = AirflowCalculatorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
