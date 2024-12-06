import tkinter as tk
from tkinter import ttk
from visualizations import (
    plot_observations_by_year,
    plot_correlation,
    plot_monthly_observations,
    plot_population_trend
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataDashboardGUI:
    def __init__(self, master, bird_observation, snowy_owl_trend):
        self.master = master
        self.bird_observation = bird_observation
        self.snowy_owl_trend = snowy_owl_trend
        self.master.title("Snowy Owl Data Dashboard")
        self.master.geometry("1400x800")

        # Configure the main frame
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the plots arranged in a 2x2 grid
        self.plot_grid_frame = ttk.Frame(self.main_frame)
        self.plot_grid_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for responsiveness
        for row in range(2):
            self.plot_grid_frame.grid_rowconfigure(row, weight=1)
        for col in range(2):
            self.plot_grid_frame.grid_columnconfigure(col, weight=1)

        # Initialize plots
        self.initialize_plots()

    def initialize_plots(self):
        """
        Generate and embed all four plots within the GUI.
        """
        # Generate Figures
        fig1 = plot_observations_by_year(self.bird_observation)
        fig2 = plot_monthly_observations(self.bird_observation)
        fig3 = plot_population_trend(self.snowy_owl_trend)
        fig4 = plot_correlation(self.bird_observation, self.snowy_owl_trend)

        # Define grid positions (switched fig3 and fig4)
        plot_positions = [
            (0, 0, fig1, ""),      # Top-Left
            (0, 1, fig2, ""),    # Top-Right
            (1, 0, fig4, ""),              # Bottom-Left
            (1, 1, fig3, "")    # Bottom-Right
        ]

        for row, col, fig, title in plot_positions:
            if fig:
                # Create a canvas and embed the figure
                canvas = FigureCanvasTkAgg(fig, master=self.plot_grid_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                # Add a label below each plot for titles
                label = ttk.Label(self.plot_grid_frame, text=title, anchor="center")
                label.grid(row=row+1, column=col, padx=10, pady=(0,10))

    def run(self):
        self.master.mainloop()