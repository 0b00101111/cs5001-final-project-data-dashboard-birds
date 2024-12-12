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
        self.original_data = bird_observation.data.copy()  # Preserve the original dataset
        self.bird_observation = bird_observation
        self.snowy_owl_trend = snowy_owl_trend
        self.current_selected_year = None  # Store the currently selected year

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

        # Define grid positions for other plots
        plot_positions = [
            (0, 0, fig1, ""),
            (1, 0, fig3, ""),
            (1, 1, fig4, "")
        ]

        # Place the other three plots
        for row, col, fig, title in plot_positions:
            if fig:
                canvas = FigureCanvasTkAgg(fig, master=self.plot_grid_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                label = ttk.Label(self.plot_grid_frame, text=title, anchor="center")
                label.grid(row=row+1, column=col, padx=10, pady=(0, 10))

        # Create a frame for the top-right cell to host the monthly observations plot
        top_right_frame = ttk.Frame(self.plot_grid_frame)
        top_right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        top_right_frame.columnconfigure(0, weight=1)
        top_right_frame.rowconfigure(0, weight=1)

        # Initialize the monthly observations canvas
        self.fig2_canvas = FigureCanvasTkAgg(fig2, master=top_right_frame)
        self.fig2_canvas.draw()
        self.fig2_widget = self.fig2_canvas.get_tk_widget()
        self.fig2_widget.grid(row=0, column=0, sticky="nsew")

        # Extract unique years for the dropdown
        unique_years = sorted(set(self.bird_observation.data['Year'].dropna().astype(int)))
        self.selected_year = tk.StringVar(value=str(unique_years[0]))

        # Add a label to indicate what the dropdown is for
        self.year_label = ttk.Label(top_right_frame, text="Select Year:")
        self.year_label.place(relx=0.35, rely=0.16, anchor="n")

        # Add a dropdown directly on top of the graph
        self.year_selector = ttk.Combobox(
            top_right_frame,
            textvariable=self.selected_year,
            values=[str(y) for y in unique_years],
            state='readonly'
        )
        # Use absolute positioning to overlap the dropdown at the top middle of the graph
        self.year_selector.place(relx=0.5, rely=0.15, anchor="n", width=100)

        # Bind a selection event to the dropdown
        self.year_selector.bind("<<ComboboxSelected>>", self.on_year_selected)

    def on_year_selected(self, event):
        """
        Callback function triggered when a year is selected from the dropdown.
        """
        # Read the currently selected year
        selected_year = int(self.selected_year.get())
        self.current_selected_year = selected_year  # Update the selected year state
        print(f"Year selected: {selected_year}")

        # Filter the bird observation data to include only records for the selected year
        filtered_data = self.original_data[
            self.original_data['Year'] == selected_year
        ]

        # Recalculate the monthly data based on the filtered subset
        monthly_data = filtered_data.groupby('Month')['OBSERVATION COUNT'].sum().reset_index()

        # Store the filtered data and monthly aggregation for further use
        self.filtered_monthly_data = monthly_data
        self.selected_year_data = filtered_data

        # Debug: Print the recalculated monthly data
        print("Filtered Monthly Data:")
        print(monthly_data)

        # Update the plot with the new data
        self.update_monthly_plot(monthly_data)

    def update_monthly_plot(self, monthly_data):
        """
        Updates the monthly observations plot with new data.
        """
        # Clear the existing figure
        self.fig2_canvas.figure.clear()

        # Create a new plot
        ax = self.fig2_canvas.figure.add_subplot(111)  # Add a new subplot
        ax.plot(
            monthly_data['Month'],
            monthly_data['OBSERVATION COUNT'],
            marker='o',
            linestyle='-',
            color='seagreen'
        )

        # Customize the plot
        ax.set_title("Snowy Owl Observations by Month")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Observations")
        ax.set_facecolor('#ECECEC')
        ax.grid(True, linestyle='--', alpha=0.5)

        # Redraw the canvas with the updated plot
        self.fig2_canvas.draw()

    def run(self):
        self.master.mainloop()