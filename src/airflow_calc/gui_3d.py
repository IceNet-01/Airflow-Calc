#!/usr/bin/env python3
"""
Advanced 3D Visualization GUI for Cybertruck Airflow Calculator
Professional interface with 3D vehicle model and airflow visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import json
from datetime import datetime

from .calculator import AirflowCalculator
from .vehicle import Cybertruck
from .utils import mph_to_ms, kmh_to_ms, ms_to_mph, ms_to_kmh
from . import __version__


class Airflow3DGUI:
    """
    Advanced 3D Visualization GUI for Airflow Calculator
    """

    def __init__(self, root):
        self.root = root
        self.root.title(f"Cybertruck Airflow Calculator 3D - v{__version__}")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)

        # Color scheme - Cybertruck inspired
        self.colors = {
            'bg': '#0a0a0a',
            'fg': '#e0e0e0',
            'accent': '#00ff41',
            'secondary': '#00cc33',
            'dark': '#050505',
            'light': '#1a1a1a',
            'panel': '#151515',
            'error': '#ff3333',
            'warning': '#ffcc00',
            'info': '#00ccff',
            'cyber_silver': '#c0c0c0',
            'cyber_orange': '#ff6600'
        }

        # Setup style
        self.setup_style()

        # Initialize variables
        self.speed_var = tk.DoubleVar(value=65.0)
        self.unit_var = tk.StringVar(value='mph')
        self.variant_var = tk.StringVar(value='dual_motor')
        self.altitude_var = tk.DoubleVar(value=0.0)
        self.temperature_var = tk.DoubleVar(value=15.0)
        self.show_streamlines_var = tk.BooleanVar(value=True)
        self.show_pressure_var = tk.BooleanVar(value=True)
        self.animation_speed = tk.DoubleVar(value=1.0)

        # Results storage
        self.current_analysis = None
        self.animation_running = False

        # Create GUI
        self.create_header()
        self.create_main_layout()
        self.create_status_bar()

        # Initial calculation and render
        self.calculate()

    def setup_style(self):
        """Configure modern dark theme"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'],
                       font=('Segoe UI', 10))
        style.configure('TButton', background=self.colors['secondary'], foreground=self.colors['fg'],
                       font=('Segoe UI', 10, 'bold'), borderwidth=0, relief='flat')
        style.map('TButton', background=[('active', self.colors['accent'])])

        style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['accent'])
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'),
                       foreground=self.colors['accent'])
        style.configure('Panel.TLabelframe', background=self.colors['panel'],
                       foreground=self.colors['accent'], borderwidth=2)
        style.configure('Panel.TLabelframe.Label', font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['accent'], background=self.colors['panel'])

    def create_header(self):
        """Create professional header"""
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Logo/Title
        title_label = tk.Label(header_frame, text="⚡ CYBERTRUCK AIRFLOW CALCULATOR 3D",
                              font=('Segoe UI', 28, 'bold'), fg=self.colors['accent'],
                              bg=self.colors['dark'])
        title_label.pack(pady=10)

        subtitle = tk.Label(header_frame,
                          text=f"Professional Aerodynamic Analysis Suite • Version {__version__}",
                          font=('Segoe UI', 10), fg=self.colors['cyber_silver'],
                          bg=self.colors['dark'])
        subtitle.pack()

    def create_main_layout(self):
        """Create main layout with panels"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel - Controls
        self.create_control_panel(main_container)

        # Center panel - 3D Visualization
        self.create_3d_visualization_panel(main_container)

        # Right panel - Results and metrics
        self.create_results_panel(main_container)

    def create_control_panel(self, parent):
        """Create control panel with all inputs"""
        control_frame = tk.Frame(parent, bg=self.colors['panel'], width=320)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        control_frame.pack_propagate(False)

        # Scrollable frame
        canvas = tk.Canvas(control_frame, bg=self.colors['panel'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['panel'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Speed Control Section
        speed_frame = tk.LabelFrame(scrollable_frame, text="  ⚡ SPEED CONTROL  ",
                                   bg=self.colors['panel'], fg=self.colors['accent'],
                                   font=('Segoe UI', 11, 'bold'), padx=10, pady=10)
        speed_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(speed_frame, text="Speed:", bg=self.colors['panel'],
                fg=self.colors['fg'], font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)

        speed_display = tk.Label(speed_frame, textvariable=self.speed_var,
                                bg=self.colors['dark'], fg=self.colors['accent'],
                                font=('Segoe UI', 24, 'bold'), relief=tk.SUNKEN, padx=10)
        speed_display.pack(fill=tk.X, pady=5)

        tk.Scale(speed_frame, from_=0, to=200, orient=tk.HORIZONTAL,
                variable=self.speed_var, command=lambda v: self.on_input_change(),
                length=280, bg=self.colors['panel'], fg=self.colors['fg'],
                activebackground=self.colors['accent'], troughcolor=self.colors['dark'],
                highlightthickness=0, showvalue=0).pack(pady=5)

        # Unit selector
        unit_frame = tk.Frame(speed_frame, bg=self.colors['panel'])
        unit_frame.pack(fill=tk.X, pady=5)

        for unit_text, unit_val in [('m/s', 'ms'), ('km/h', 'kmh'), ('mph', 'mph')]:
            tk.Radiobutton(unit_frame, text=unit_text, variable=self.unit_var,
                          value=unit_val, bg=self.colors['panel'], fg=self.colors['fg'],
                          selectcolor=self.colors['dark'], activebackground=self.colors['panel'],
                          activeforeground=self.colors['accent'], font=('Segoe UI', 10),
                          command=self.on_input_change).pack(side=tk.LEFT, expand=True)

        # Vehicle Configuration
        vehicle_frame = tk.LabelFrame(scrollable_frame, text="  🚗 VEHICLE CONFIG  ",
                                     bg=self.colors['panel'], fg=self.colors['accent'],
                                     font=('Segoe UI', 11, 'bold'), padx=10, pady=10)
        vehicle_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(vehicle_frame, text="Variant:", bg=self.colors['panel'],
                fg=self.colors['fg']).pack(anchor=tk.W)

        for variant, label in [('single_motor', 'Single Motor RWD'),
                              ('dual_motor', 'Dual Motor AWD'),
                              ('tri_motor', 'Tri Motor AWD (Cyberbeast)')]:
            tk.Radiobutton(vehicle_frame, text=label, variable=self.variant_var,
                          value=variant, bg=self.colors['panel'], fg=self.colors['fg'],
                          selectcolor=self.colors['dark'], activebackground=self.colors['panel'],
                          activeforeground=self.colors['accent'], font=('Segoe UI', 9),
                          command=self.on_input_change, wraplength=250,
                          justify=tk.LEFT).pack(anchor=tk.W, pady=2)

        # Environmental Conditions
        env_frame = tk.LabelFrame(scrollable_frame, text="  🌍 ENVIRONMENT  ",
                                 bg=self.colors['panel'], fg=self.colors['accent'],
                                 font=('Segoe UI', 11, 'bold'), padx=10, pady=10)
        env_frame.pack(fill=tk.X, padx=10, pady=10)

        # Altitude
        tk.Label(env_frame, text=f"Altitude: {self.altitude_var.get():.0f} m",
                bg=self.colors['panel'], fg=self.colors['fg']).pack(anchor=tk.W)
        alt_scale = tk.Scale(env_frame, from_=0, to=5000, orient=tk.HORIZONTAL,
                            variable=self.altitude_var, command=self.update_altitude_label,
                            length=280, bg=self.colors['panel'], fg=self.colors['fg'],
                            activebackground=self.colors['info'], troughcolor=self.colors['dark'],
                            highlightthickness=0, showvalue=0)
        alt_scale.pack(pady=5)
        self.altitude_label = tk.Label(env_frame, text="Sea Level",
                                      bg=self.colors['panel'], fg=self.colors['info'],
                                      font=('Segoe UI', 9, 'italic'))
        self.altitude_label.pack()

        # Temperature
        tk.Label(env_frame, text=f"Temperature: {self.temperature_var.get():.1f} °C",
                bg=self.colors['panel'], fg=self.colors['fg']).pack(anchor=tk.W, pady=(10, 0))
        temp_scale = tk.Scale(env_frame, from_=-50, to=50, orient=tk.HORIZONTAL,
                             variable=self.temperature_var, command=self.update_temp_label,
                             length=280, bg=self.colors['panel'], fg=self.colors['fg'],
                             activebackground=self.colors['warning'], troughcolor=self.colors['dark'],
                             highlightthickness=0, showvalue=0)
        temp_scale.pack(pady=5)
        self.temp_label = tk.Label(env_frame, text="Standard Conditions",
                                   bg=self.colors['panel'], fg=self.colors['warning'],
                                   font=('Segoe UI', 9, 'italic'))
        self.temp_label.pack()

        # Visualization Options
        viz_frame = tk.LabelFrame(scrollable_frame, text="  👁 VISUALIZATION  ",
                                 bg=self.colors['panel'], fg=self.colors['accent'],
                                 font=('Segoe UI', 11, 'bold'), padx=10, pady=10)
        viz_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Checkbutton(viz_frame, text="Show Streamlines", variable=self.show_streamlines_var,
                      bg=self.colors['panel'], fg=self.colors['fg'],
                      selectcolor=self.colors['dark'], activebackground=self.colors['panel'],
                      activeforeground=self.colors['accent'],
                      command=self.update_visualization).pack(anchor=tk.W)

        tk.Checkbutton(viz_frame, text="Show Pressure Field", variable=self.show_pressure_var,
                      bg=self.colors['panel'], fg=self.colors['fg'],
                      selectcolor=self.colors['dark'], activebackground=self.colors['panel'],
                      activeforeground=self.colors['accent'],
                      command=self.update_visualization).pack(anchor=tk.W)

        # Action Buttons
        action_frame = tk.Frame(scrollable_frame, bg=self.colors['panel'])
        action_frame.pack(fill=tk.X, padx=10, pady=20)

        btn_style = {'font': ('Segoe UI', 11, 'bold'), 'bg': self.colors['secondary'],
                    'fg': self.colors['fg'], 'activebackground': self.colors['accent'],
                    'relief': tk.FLAT, 'cursor': 'hand2', 'pady': 10}

        tk.Button(action_frame, text="🔄 RECALCULATE", command=self.calculate,
                 **btn_style).pack(fill=tk.X, pady=5)
        tk.Button(action_frame, text="💾 EXPORT JSON", command=self.export_json,
                 **btn_style).pack(fill=tk.X, pady=5)
        tk.Button(action_frame, text="📸 SAVE 3D VIEW", command=self.export_3d_view,
                 **btn_style).pack(fill=tk.X, pady=5)
        tk.Button(action_frame, text="🎬 ANIMATE", command=self.toggle_animation,
                 **btn_style).pack(fill=tk.X, pady=5)
        tk.Button(action_frame, text="🔄 RESET", command=self.reset,
                 **btn_style).pack(fill=tk.X, pady=5)

    def create_3d_visualization_panel(self, parent):
        """Create 3D visualization panel"""
        viz_container = tk.Frame(parent, bg=self.colors['bg'])
        viz_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Create matplotlib figure with 3D subplots
        self.fig = Figure(figsize=(12, 10), facecolor=self.colors['bg'])

        # Main 3D view
        self.ax_main = self.fig.add_subplot(221, projection='3d', facecolor=self.colors['light'])

        # Additional views
        self.ax_top = self.fig.add_subplot(222, projection='3d', facecolor=self.colors['light'])
        self.ax_side = self.fig.add_subplot(223, projection='3d', facecolor=self.colors['light'])
        self.ax_pressure = self.fig.add_subplot(224, facecolor=self.colors['light'])

        # Style axes
        for ax in [self.ax_main, self.ax_top, self.ax_side]:
            ax.set_facecolor(self.colors['light'])
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.grid(True, alpha=0.2, color=self.colors['accent'])
            ax.tick_params(colors=self.colors['fg'], labelsize=8)
            # Set pane edge colors
            ax.xaxis.pane.set_edgecolor(self.colors['fg'])
            ax.yaxis.pane.set_edgecolor(self.colors['fg'])
            ax.zaxis.pane.set_edgecolor(self.colors['fg'])

        self.ax_pressure.set_facecolor(self.colors['light'])
        self.ax_pressure.tick_params(colors=self.colors['fg'])
        self.ax_pressure.spines['bottom'].set_color(self.colors['fg'])
        self.ax_pressure.spines['left'].set_color(self.colors['fg'])
        self.ax_pressure.spines['top'].set_color(self.colors['fg'])
        self.ax_pressure.spines['right'].set_color(self.colors['fg'])

        self.fig.tight_layout(pad=2.0)

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        toolbar_frame = tk.Frame(viz_container, bg=self.colors['panel'])
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.config(background=self.colors['panel'])
        toolbar._message_label.config(background=self.colors['panel'], foreground=self.colors['fg'])
        toolbar.update()

    def create_results_panel(self, parent):
        """Create results display panel"""
        results_container = tk.Frame(parent, bg=self.colors['panel'], width=350)
        results_container.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        results_container.pack_propagate(False)

        # Title
        tk.Label(results_container, text="📊 ANALYSIS RESULTS",
                font=('Segoe UI', 14, 'bold'), fg=self.colors['accent'],
                bg=self.colors['panel']).pack(pady=10)

        # Results text widget
        text_frame = tk.Frame(results_container, bg=self.colors['panel'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.results_text = tk.Text(text_frame, bg=self.colors['dark'], fg=self.colors['fg'],
                                    font=('Consolas', 10), wrap=tk.WORD,
                                    insertbackground=self.colors['accent'])
        scrollbar = tk.Scrollbar(text_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure tags
        self.results_text.tag_config('header', foreground=self.colors['accent'],
                                    font=('Consolas', 11, 'bold'))
        self.results_text.tag_config('value', foreground=self.colors['cyber_orange'],
                                    font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('label', foreground=self.colors['info'])
        self.results_text.tag_config('metric', foreground=self.colors['fg'])

    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg=self.colors['dark'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready • System initialized")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg=self.colors['dark'], fg=self.colors['accent'],
                               font=('Segoe UI', 9), anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # FPS counter
        self.fps_var = tk.StringVar(value="FPS: 60")
        tk.Label(status_frame, textvariable=self.fps_var,
                bg=self.colors['dark'], fg=self.colors['info'],
                font=('Segoe UI', 9)).pack(side=tk.RIGHT, padx=10)

    def generate_cybertruck_mesh(self):
        """Generate simplified 3D mesh of Cybertruck"""
        # Cybertruck dimensions (simplified angular design)
        length = 5.885
        width = 2.413
        height = 1.905

        # Define vertices for angular Cybertruck shape
        vertices = [
            # Front vertices (angular front)
            [0, -width/2, 0], [0, width/2, 0],  # Front bottom
            [0, -width/2, height*0.3], [0, width/2, height*0.3],  # Front lower
            [length*0.1, -width/2, height*0.7], [length*0.1, width/2, height*0.7],  # Windshield base
            [length*0.3, -width/2, height], [length*0.3, width/2, height],  # Roof start

            # Rear vertices
            [length*0.7, -width/2, height], [length*0.7, width/2, height],  # Roof end
            [length, -width/2, height*0.6], [length, width/2, height*0.6],  # Rear top
            [length, -width/2, 0], [length, width/2, 0],  # Rear bottom
        ]

        vertices = np.array(vertices)

        # Define faces (triangles)
        faces = [
            # Front
            [0, 1, 3], [0, 3, 2],
            [2, 3, 5], [2, 5, 4],
            [4, 5, 7], [4, 7, 6],

            # Top (roof)
            [6, 7, 9], [6, 9, 8],
            [8, 9, 11], [8, 11, 10],

            # Rear
            [10, 11, 13], [10, 13, 12],

            # Sides
            [0, 2, 4], [0, 4, 6], [0, 6, 8], [0, 8, 10], [0, 10, 12],
            [1, 3, 5], [1, 5, 7], [1, 7, 9], [1, 9, 11], [1, 11, 13],

            # Bottom
            [0, 12, 13], [0, 13, 1],
        ]

        return vertices, faces

    def render_3d_vehicle(self, ax, view_angle='main'):
        """Render 3D Cybertruck in the given axes"""
        vertices, faces = self.generate_cybertruck_mesh()

        # Create polygon collection
        poly_collection = [[vertices[face[0]], vertices[face[1]], vertices[face[2]]]
                          for face in faces]

        # Create 3D polygon collection
        mesh = Poly3DCollection(poly_collection, alpha=0.7, linewidths=1,
                               edgecolors=self.colors['cyber_silver'])
        mesh.set_facecolor(self.colors['cyber_silver'])
        ax.add_collection3d(mesh)

        # Set view angles
        if view_angle == 'main':
            ax.view_init(elev=20, azim=135)
            ax.set_title('Main View', color=self.colors['accent'], fontsize=10, fontweight='bold')
        elif view_angle == 'top':
            ax.view_init(elev=90, azim=0)
            ax.set_title('Top View', color=self.colors['accent'], fontsize=10, fontweight='bold')
        elif view_angle == 'side':
            ax.view_init(elev=0, azim=0)
            ax.set_title('Side View', color=self.colors['accent'], fontsize=10, fontweight='bold')

        # Set limits
        ax.set_xlim(-1, 7)
        ax.set_ylim(-2, 2)
        ax.set_zlim(0, 3)

        ax.set_xlabel('X (m)', color=self.colors['fg'], fontsize=8)
        ax.set_ylabel('Y (m)', color=self.colors['fg'], fontsize=8)
        ax.set_zlabel('Z (m)', color=self.colors['fg'], fontsize=8)

    def add_streamlines(self, ax, velocity_ms):
        """Add airflow streamlines"""
        if not self.show_streamlines_var.get():
            return

        # Generate streamline points
        num_lines = 8
        y_positions = np.linspace(-1.5, 1.5, num_lines)
        z_positions = np.linspace(0.5, 2.5, num_lines)

        for y_pos in y_positions:
            for z_pos in z_positions:
                # Streamline coordinates
                x = np.linspace(-2, 8, 100)
                y = np.ones_like(x) * y_pos
                z = np.ones_like(x) * z_pos

                # Add perturbation near vehicle
                for i, x_val in enumerate(x):
                    if 0 < x_val < 6:
                        # Simulate flow around vehicle
                        dist_to_center = np.sqrt(y_pos**2 + (z_pos - 1.0)**2)
                        if dist_to_center < 1.5:
                            z[i] += 0.3 * np.sin(x_val * np.pi / 6) * (1 - dist_to_center/1.5)
                            y[i] += 0.2 * np.cos(x_val * np.pi / 6) * (1 - dist_to_center/1.5)

                # Color based on velocity
                colors = plt.cm.viridis(np.linspace(0.3, 1, len(x)))

                for i in range(len(x)-1):
                    ax.plot(x[i:i+2], y[i:i+2], z[i:i+2],
                           color=colors[i], alpha=0.6, linewidth=0.8)

    def render_pressure_field(self, ax, analysis):
        """Render pressure coefficient distribution"""
        if not self.show_pressure_var.get():
            return

        ax.clear()

        # Generate pressure field data along vehicle length
        x = np.linspace(0, 5.885, 50)

        # Simulate pressure coefficient (simplified)
        # Front: high pressure (stagnation)
        # Sides: lower pressure (acceleration)
        # Rear: low pressure (wake)
        Cp = []
        for x_val in x:
            if x_val < 0.5:  # Front stagnation
                cp = 1.0 - 0.5 * (x_val / 0.5)
            elif x_val < 3:  # Accelerating flow
                cp = 0.5 - 0.8 * ((x_val - 0.5) / 2.5)
            else:  # Wake region
                cp = -0.3 + 0.1 * ((x_val - 3) / 2.885)
            Cp.append(cp)

        Cp = np.array(Cp)

        # Plot
        ax.fill_between(x, Cp, 0, where=(Cp > 0), alpha=0.5,
                        color=self.colors['error'], label='High Pressure')
        ax.fill_between(x, Cp, 0, where=(Cp <= 0), alpha=0.5,
                        color=self.colors['info'], label='Low Pressure')
        ax.plot(x, Cp, color=self.colors['accent'], linewidth=2)
        ax.axhline(y=0, color=self.colors['fg'], linestyle='--', linewidth=1, alpha=0.5)

        ax.set_xlabel('Distance Along Vehicle (m)', color=self.colors['fg'])
        ax.set_ylabel('Pressure Coefficient (Cp)', color=self.colors['fg'])
        ax.set_title('Pressure Distribution', color=self.colors['accent'],
                    fontsize=10, fontweight='bold')
        ax.legend(loc='upper right', facecolor=self.colors['dark'],
                 edgecolor=self.colors['accent'], labelcolor=self.colors['fg'])
        ax.grid(True, alpha=0.2, color=self.colors['accent'])

        # Style
        ax.set_facecolor(self.colors['light'])
        ax.tick_params(colors=self.colors['fg'])
        for spine in ax.spines.values():
            spine.set_color(self.colors['fg'])

    def calculate(self):
        """Perform calculations"""
        try:
            # Get values
            speed = self.speed_var.get()
            unit = self.unit_var.get()
            variant = self.variant_var.get()
            altitude = self.altitude_var.get()
            temperature = self.temperature_var.get()

            # Convert speed
            if unit == 'mph':
                speed_ms = mph_to_ms(speed)
            elif unit == 'kmh':
                speed_ms = kmh_to_ms(speed)
            else:
                speed_ms = speed

            # Create calculator
            vehicle = Cybertruck(variant=variant)
            calculator = AirflowCalculator(vehicle, altitude=altitude, temperature=temperature)

            # Analyze
            self.current_analysis = calculator.get_full_analysis(speed_ms)

            # Update visualization
            self.update_visualization()

            # Update results
            self.update_results_display()

            self.status_var.set(f"✓ Analysis complete • {speed:.1f} {unit}")

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error:\n{str(e)}")
            self.status_var.set("✗ Calculation failed")

    def update_visualization(self):
        """Update 3D visualization"""
        if not self.current_analysis:
            return

        # Clear axes
        self.ax_main.clear()
        self.ax_top.clear()
        self.ax_side.clear()

        # Get velocity
        velocity_ms = self.current_analysis['velocity']['m_s']

        # Render vehicle in different views
        self.render_3d_vehicle(self.ax_main, 'main')
        self.render_3d_vehicle(self.ax_top, 'top')
        self.render_3d_vehicle(self.ax_side, 'side')

        # Add streamlines
        self.add_streamlines(self.ax_main, velocity_ms)
        self.add_streamlines(self.ax_top, velocity_ms)
        self.add_streamlines(self.ax_side, velocity_ms)

        # Render pressure field
        self.render_pressure_field(self.ax_pressure, self.current_analysis)

        # Redraw
        self.canvas.draw()

    def update_results_display(self):
        """Update results text"""
        if not self.current_analysis:
            return

        self.results_text.delete(1.0, tk.END)

        # Header
        self.results_text.insert(tk.END, "╔════════════════════════════╗\n", 'header')
        self.results_text.insert(tk.END, "║   AERODYNAMIC ANALYSIS    ║\n", 'header')
        self.results_text.insert(tk.END, "╚════════════════════════════╝\n\n", 'header')

        # Velocity
        vel = self.current_analysis['velocity']
        self.results_text.insert(tk.END, "⚡ VELOCITY\n", 'header')
        self.results_text.insert(tk.END, f"   {vel['m_s']:.2f} m/s\n", 'value')
        self.results_text.insert(tk.END, f"   {vel['km_h']:.2f} km/h\n", 'value')
        self.results_text.insert(tk.END, f"   {vel['mph']:.2f} mph\n\n", 'value')

        # Forces
        forces = self.current_analysis['aerodynamic_forces']
        self.results_text.insert(tk.END, "💨 DRAG FORCE\n", 'header')
        self.results_text.insert(tk.END, f"   {forces['drag_force_n']:.2f} N\n", 'value')
        self.results_text.insert(tk.END, f"   {forces['drag_force_lbf']:.2f} lbf\n\n", 'value')

        self.results_text.insert(tk.END, "⬆ LIFT FORCE\n", 'header')
        self.results_text.insert(tk.END, f"   {forces['lift_force_n']:.2f} N\n", 'value')
        self.results_text.insert(tk.END, f"   {forces['lift_force_lbf']:.2f} lbf\n\n", 'value')

        # Power
        power = self.current_analysis['power_requirements']
        self.results_text.insert(tk.END, "⚙ POWER REQUIRED\n", 'header')
        self.results_text.insert(tk.END, f"   {power['power_kw']:.2f} kW\n", 'value')
        self.results_text.insert(tk.END, f"   {power['power_hp']:.2f} hp\n\n", 'value')

        # Flow
        flow = self.current_analysis['flow_characteristics']
        self.results_text.insert(tk.END, "🌊 FLOW PROPERTIES\n", 'header')
        self.results_text.insert(tk.END, f"   Re: {flow['reynolds_number']:.3e}\n", 'metric')
        self.results_text.insert(tk.END, f"   q: {flow['dynamic_pressure_pa']:.2f} Pa\n", 'metric')
        self.results_text.insert(tk.END, f"   M: {flow['mach_number']:.4f}\n\n", 'metric')

        # Environment
        atm = self.current_analysis['atmospheric_conditions']
        self.results_text.insert(tk.END, "🌍 ENVIRONMENT\n", 'header')
        self.results_text.insert(tk.END, f"   ρ: {atm['density_kg_m3']:.4f} kg/m³\n", 'metric')
        self.results_text.insert(tk.END, f"   T: {atm['temperature_c']:.1f}°C\n", 'metric')
        self.results_text.insert(tk.END, f"   h: {atm['altitude_m']:.0f} m\n\n", 'metric')

        # Timestamp
        self.results_text.insert(tk.END, f"{'─'*30}\n", 'label')
        self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}\n", 'label')

    def update_altitude_label(self, val):
        """Update altitude description"""
        alt = float(val)
        if alt < 100:
            desc = "Sea Level"
        elif alt < 500:
            desc = "Low Altitude"
        elif alt < 1500:
            desc = "Medium Altitude"
        elif alt < 3000:
            desc = "High Altitude"
        else:
            desc = "Very High Altitude"

        self.altitude_label.config(text=f"{desc} ({alt:.0f} m)")
        self.on_input_change()

    def update_temp_label(self, val):
        """Update temperature description"""
        temp = float(val)
        if temp < -20:
            desc = "Very Cold"
        elif temp < 0:
            desc = "Cold"
        elif temp < 15:
            desc = "Cool"
        elif temp < 25:
            desc = "Standard"
        elif temp < 35:
            desc = "Warm"
        else:
            desc = "Hot"

        self.temp_label.config(text=f"{desc} ({temp:.1f}°C)")
        self.on_input_change()

    def on_input_change(self):
        """Handle input changes"""
        self.root.after(500, self.calculate)

    def toggle_animation(self):
        """Toggle animation"""
        self.animation_running = not self.animation_running
        if self.animation_running:
            self.animate_view()

    def animate_view(self):
        """Animate the 3D view"""
        if not self.animation_running:
            return

        # Rotate main view
        azim = self.ax_main.azim + 2
        self.ax_main.view_init(elev=20, azim=azim)

        self.canvas.draw()
        self.root.after(50, self.animate_view)

    def export_json(self):
        """Export to JSON"""
        if not self.current_analysis:
            messagebox.showwarning("No Data", "Please calculate first")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_analysis, f, indent=2)
                messagebox.showinfo("Success", f"Exported to:\n{filename}")
                self.status_var.set(f"✓ Exported • {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def export_3d_view(self):
        """Export 3D view"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf")]
        )

        if filename:
            try:
                self.fig.savefig(filename, dpi=300, facecolor=self.colors['bg'],
                               edgecolor='none')
                messagebox.showinfo("Success", f"Saved to:\n{filename}")
                self.status_var.set(f"✓ Saved • {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def reset(self):
        """Reset to defaults"""
        self.speed_var.set(65.0)
        self.unit_var.set('mph')
        self.variant_var.set('dual_motor')
        self.altitude_var.set(0.0)
        self.temperature_var.set(15.0)
        self.show_streamlines_var.set(True)
        self.show_pressure_var.set(True)
        self.calculate()
        self.status_var.set("Reset to defaults")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = Airflow3DGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
