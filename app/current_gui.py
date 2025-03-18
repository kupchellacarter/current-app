import tkinter as tk
import logging
import matplotlib.colors as mcolors
import numpy as np

# import threading

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


class GUI:
    """
    The tkinter GUI
    """

    def __init__(self):
        self.root = tk.Tk()
        self.font = "Georgia"
        self.root.title("Electric Boat Dashboard")
        self.metric_font_size = 24
        self.charge_level = 0
        self.mean_voltage = 0
        self.low_voltage = 0
        self.high_voltage = 0
        self.root.attributes("-fullscreen", False)
        # self.root.config(cursor="none")
        # self.root.overrideredirect(True)
        self.root.geometry("800x480")  # Set to your screen size
        self.root.config(bg="black")

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def display_defualt_ui(self):
        # Frame Nest
        self.outer_frame = tk.Frame(self.root, bg="black", width=780, height=460)
        self.outer_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.top_frame = tk.Frame(self.outer_frame, bg="red", width=760, height=100)
        self.top_frame.pack(side="top", fill="x")
        self._create_soc_frame()
        self.set_soc(5)
        self._create_runtime_frame()

       

        # Bottom (error message) Frame
        self.bottom_frame = tk.Frame(
            self.outer_frame, bg="black", width=760, height=100
        )
        self.bottom_frame.pack(anchor="s", side="bottom", fill="x")

        # Central Left Frame
        self.central_frame = tk.Frame(
            self.outer_frame, bg="black", height=200, width=560
        )
        self.central_frame.pack(side="left", fill="y", expand=True, pady=(40, 0))

        # Central Right Frame
        self.right_frame = tk.Frame(self.outer_frame, bg="black", height=200, width=200)
        self.right_frame.pack(side="right", fill="y", pady=(40, 0))

        # Central Metrics
        self.voltage_label = tk.Label(
            self.central_frame,
            text="Pack Voltage: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.voltage_label.pack(anchor="nw", padx=5, pady=5)

        self.current_label = tk.Label(
            self.central_frame,
            text="Current: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.current_label.pack(anchor="w", padx=10, pady=10)

        self.power_label = tk.Label(
            self.central_frame,
            text="Power: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.power_label.pack(anchor="sw", padx=10, pady=10)

        self.temp_label = tk.Label(
            self.right_frame,
            text="Temperature: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.temp_label.pack(anchor="n", padx=10, pady=10)

        self.cell_voltage_label = tk.Label(
            self.right_frame,
            text="Cell Mean V: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.cell_voltage_label.pack(anchor="n", padx=10, pady=10)

        self._create_cell_voltage_slider()

        # Error Display
        self.system_error_label = tk.Label(
            self.bottom_frame,
            text="No Data",
            font=(self.font, 32),
            bg="black",
            fg="blue",
        )
        self.system_error_label.pack(anchor="s", side="bottom")

    def _create_soc_frame(self):
        # Battery soc Display (Top)
        self.soc_canvas = tk.Canvas(self.top_frame, width=760, height=50, bg="black")
        self.soc_canvas.pack(side="top", fill="x")

    def _create_runtime_frame(self):
         # Runtime Frame
        self.runtime_frame = tk.Frame(self.root, bg="black", height=20)
        self.runtime_frame.pack(anchor="sw", side="bottom", fill="x", padx=10, pady=5)
        self.runtime_label = tk.Label(
            self.runtime_frame,
            text="Runtime:",
            font=(self.font, 14),
            bg="black",
            fg="white",
        )
        self.runtime_label.grid(row=0, column=0, stick="w", padx=10)

        self.runtime_frame.grid_columnconfigure(0, weight=1)

        self.cell_count_label = tk.Label(
            self.runtime_frame,
            text="No Cells Connected",
            font=(self.font, 14),
            bg="black",
            fg="white",
        )
        self.cell_count_label.grid(
            row=0,
            column=1,
            sticky="e",
            padx=10,
        )

    def set_pack_kwh(self, current_kwh, max_kwh):
        # Battery percentage text below
        self.soc_canvas.create_text(
            550,
            40,
            text=f"{current_kwh}/{max_kwh}",
            fill="white",
            font=(self.font, 12),
        )

    def _create_cell_voltage_slider(self):
        self.cell_voltage_canvas = tk.Canvas(
            self.right_frame, bg="black", width=400, height=40, highlightthickness=0
        )
        self.cell_voltage_canvas.pack(padx=10, pady=10)

        num_sections = 20
        section_width = 360 / num_sections  # Calculate section width

        # Generate colors using a rainbow colormap
        colormap = mcolors.LinearSegmentedColormap.from_list("rainbow", 
                    ["red", "orange", "yellow", "green", "cyan", "aqua", "white"])
        colors = [mcolors.rgb2hex(colormap(i / (num_sections - 4))) for i in range(num_sections)]

        for i in range(num_sections-3):
            x1 = i * section_width + 45
            x2 = x1 + section_width
            fill_color = colors[i]
            outline_color = fill_color  # Keep outline same as fill for smooth effect

            self.cell_voltage_canvas.create_rectangle(
                x1, 10, x2, 30, outline=outline_color, width=1, fill=fill_color
            )
        self.low_voltage_label = self.cell_voltage_canvas.create_text(5, 20, text="0.0", fill="white", anchor="w", font=(self.font, 20, "bold"))
        self.high_voltage_label = self.cell_voltage_canvas.create_text(400, 20, text="0.0", fill="white", anchor="e", font=(self.font, 20, "bold"))
    
    def set_cell_voltage_slider(self, mean_voltage:float, low_voltage:float, high_voltage:float):
        if self.low_voltage != low_voltage:
            self.cell_voltage_canvas.itemconfig(self.low_voltage_label, text=str(low_voltage))
            self.low_voltage = low_voltage
        if self.high_voltage != high_voltage:
            self.cell_voltage_canvas.itemconfig(self.high_voltage_label, text=str(high_voltage))
            self.high_voltage = high_voltage
        if self.mean_voltage != mean_voltage:
            x1 = 45 + (mean_voltage - 2.5) * 360 / 2.5
            x2 = x1 + 30
            self.cell_voltage_canvas.create_rectangle(
                x1, 0, x2, 50, outline="white", width=1, fill="white"
            )

    def set_soc(self, charge_level=0):
        # only update the charge level if it has changed
        if self.charge_level != charge_level:
            logger.warning(f"Updating SOC to {charge_level}")
            self.soc_canvas.delete("all")
            self.charge_level = charge_level
            num_sections = 100
            section_width = (680 - 45) / num_sections  # Calculate section width
            for i in range(num_sections):
                x1 = 45 + i * section_width
                space = 3 if (i + 1) % 10 == 0 else 0
                x2 = x1 + section_width - space  # Add small gap for spacing

                # Green for filled sections, black for empty, with blue outline for empty ones
                if i < (self.charge_level / 100) * num_sections:
                    if self.charge_level < 20:
                        fill_color = "red"
                    elif self.charge_level < 40:
                        fill_color = "yellow"
                    else:
                        fill_color = "green"
                    outline_color = fill_color
                else:
                    fill_color = "#36454F"
                    outline_color = "#36454F"

                self.soc_canvas.create_rectangle(
                    x1, 5, x2, 45, outline=outline_color, width=1, fill=fill_color
                )

            # Labels "E" and "F" inside the battery
            self.soc_canvas.create_text(
                25, 25, text="E", fill="white", font=(self.font, 30, "bold")
            )
            self.soc_canvas.create_text(
                700, 25, text="F", fill="white", font=(self.font, 30, "bold")
            )
            self.soc_canvas.create_text(
                350,
                25,
                text=f"{charge_level}%",
                fill="white",
                font=(self.font, 30, "bold"),
            )

    def update_runtime(self, runtime_value):
        """
        Method to update the displayed variables dynamically
        """
        # Update the labels with new values
        self.runtime_label.config(text=f"Runtime: {runtime_value}")

    def set_pack_voltage(self, voltage_value):
        self.voltage_label.config(text=f"{voltage_value}")

    def set_pack_current(self, current_value):
        self.current_label.config(text=f"{current_value}")

    def set_power(self, power_value):
        self.power_label.config(text=f"{power_value}")

    def set_temp(self, temp):
        self.temp_label.config(text=f"Temperature: {temp}")

    def set_cell_count(self, cell_count):
        if cell_count == 16:
            self.cell_count_label.config(text=f"{cell_count} Cells OK!", fg="green")
        else:
            self.cell_count_label.config(
                text=f"Check Cells! {cell_count} Cells Connected", fg="red"
            )

    def set_cell_voltage(self, mean_cell_v):
        self.cell_voltage_label.config(text=f"Cell Voltage: {mean_cell_v}")
        # self.low_cell_v_label.config(text=f"Lowest: {lowest_cell_v}")
        # self.high_cell_v_label.config(text=f"Highest: {high_cell_v}")

    def update_error_label(self, system_errors: set[str]):
        if len(system_errors) > 0:
            error_lines = system_errors.split("\n")
            formatted_message = "/n".join(error_lines)
            self.system_error_label.config(
                text=formatted_message, bg="red", fg="yellow"
            )
        else:
            self.system_error_label.config(text="All OK", bg="black", fg="blue")

    def refresh_ui(self):
        """Refresh the UI periodically"""
        self.root.update_idletasks()
        self.root.update()

    def display_error_ui(self, error_message: str):
        self.outer_frame = tk.Frame(self.root, bg="black", width=780, height=460)
        self.outer_frame.pack(fill="both", expand=True, padx=20, pady=20)
        # Central Frame
        self.central_frame = tk.Frame(self.outer_frame, bg="black", width=560)
        self.central_frame.pack(side="left", fill="y")

        # Central Metrics
        self.error_label = tk.Label(
            self.central_frame,
            text=f"ERROR: {error_message}",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.error_label.grid(row=0, column=0, pady=4)


if __name__ == "__main__":
    gui = GUI()
    gui.display_defualt_ui()
    gui.set_cell_voltage_slider(3.2, 2.5, 4.0)
    gui.run()
    # gui.set_pack_voltage(57.2)
    # gui.set_pack_current(10.5)
    # gui.set_power(1.5)
    # gui.set_cell_voltage(3.20)
    # gui.set_temp(25)
    # gui.set_soc(55)
    # voltage_value = 57.2
    # current_value = 10.5
    # power_value = 1.5
    # mean_cell_v = 3.20
    # temp_value = 25
