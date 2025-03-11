import tkinter as tk
import logging
import threading

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
        self.charge_level=0
        self.root.attributes("-fullscreen", False)
        # self.root.config(cursor="none")
        # self.root.overrideredirect(True)
        self.root.geometry("800x480")  # Set to your screen size
        self.root.config(bg="black")

        # Frame Nest
        self.outer_frame = tk.Frame(self.root, bg="black", width=760, height=360)
        self.outer_frame.pack(padx=40, pady=40)


    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def display_defualt_ui(self):
        # Top Frame
        self.top_frame = tk.Frame(self.outer_frame, bg="black", width=700, height=100)
        self.top_frame.pack(side="top", fill="x")
        self._create_soc_frame()  
        self.set_soc()

        # Bottom Frame
        self.bottom_frame = tk.Frame(self.outer_frame, bg="black", width=760, height=80)
        self.bottom_frame.pack(side="bottom", fill="x")

        # Central Frame
        self.central_frame = tk.Frame(self.outer_frame, bg="black", width=560)
        self.central_frame.pack(side="left", fill="y")

        # Central Metrics
        self.runtime_label = tk.Label(
            self.central_frame,
            text="MCU Runtime: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.runtime_label.grid(row=0, column=0, pady=4)

        self.voltage_label = tk.Label(
            self.central_frame,
            text="Pack Voltage: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.voltage_label.grid(row=1, column=0, pady=5)

        self.current_label = tk.Label(
            self.central_frame,
            text="Current: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.current_label.grid(row=2, column=0, pady=5)

        self.power_label = tk.Label(
            self.central_frame,
            text="Power: ",
            font=(self.font, self.metric_font_size),
            bg="black",
            fg="white",
        )
        self.power_label.grid(row=3, column=0, pady=5)

        # Right Frame
        self.right_frame = tk.Frame(self.root, bg="black", width=100, height=160)
        self.right_frame.pack(side="right", fill="y")

        # Power and Temperature Bars (Right)
        self.kw_canvas = tk.Canvas(self.right_frame, width=10, height=100, bg="blue")
        self.kw_canvas.grid(row=0, column=0, pady=5)

        self.temp_canvas = tk.Canvas(self.right_frame, width=10, height=100, bg="blue")
        self.temp_canvas.grid(row=0, column=1, pady=5)

        # Cell Voltage Display
        self.cell_voltage_label = tk.Label(
            self.bottom_frame,
            text="Cell Voltage: 0.000V",
            font=(self.font, 24),
            bg="black",
            fg="white",
        )
        self.cell_voltage_label.grid(row=0, column=0, pady=5)

        # Error Display
        self.system_error_label = tk.Label(
            self.bottom_frame,
            text="System Errors:",
            font=(self.font, 32),
            bg="black",
            fg="white",
        )
        self.system_error_label.grid(row=1, column=0, pady=5)


    def _create_soc_frame(self):
        # Battery soc Display (Top)
        self.soc_canvas = tk.Canvas(self.top_frame, width=700, height=50, bg="black")
        self.soc_canvas.pack(side="top", fill="x")
        # Labels "E" and "F" inside the battery
        self.soc_canvas.create_text(25, 25, text="E", fill="white", font=("Arial", 14, "bold"))
        self.soc_canvas.create_text(675, 25, text="F", fill="white", font=("Arial", 14, "bold"))
    
    def set_soc(self,charge_level=0):
        self.charge_level = charge_level
        num_sections = 100
        section_width = (670 - 30) / num_sections  # Calculate section width
        for i in range(num_sections):
            x1 = 30 + i * section_width
            space = 3 if (i+1)%10 == 0 else 0
            x2 = x1 + section_width - space  # Add small gap for spacing

            # Green for filled sections, black for empty, with blue outline for empty ones
            if i < (self.charge_level/100) * num_sections:
                fill_color = "green"
                outline_color = "green"
            else:
                fill_color = "#36454F"
                outline_color = "#36454F"

            self.soc_canvas.create_rectangle(x1, 5, x2, 45, outline=outline_color, width=1, fill=fill_color)

        # Battery percentage text below
        self.soc_canvas.create_text(550, 48, text=f"{self.charge_level * 2.5:.1f}/20.0 kWh", fill="white", font=("Arial", 12))

    
    def update_runtime(self, runtime_value):
        """
        Method to update the displayed variables dynamically
        """
        # Update the labels with new values
        logger.warning(f"Updating runtime value: {runtime_value}")
        self.runtime_label.config(text=f"Runtime: {runtime_value}")

    def update_voltage(self, voltage_value):
        logger.warning(f"Updating voltage value: {voltage_value}")
        self.voltage_label.config(text=f"Voltage: {voltage_value} V")

    def update_soc(self, soc):
        """Update the State of Charge (soc) bar"""
        self.soc_canvas.delete("all")
        bar_width = int(300 * (soc / 100))
        color = "green" if soc > 50 else "yellow" if soc > 20 else "red"
        self.soc_canvas.create_rectangle(0, 0, bar_width, 50, fill=color)
        self.soc_canvas.create_text(
            150, 25, text=f"{soc:.1f}%", fill="white", font=(self.font, 20)
        )

    # def update_metrics(self, voltage, current, power):
    #     """Update the voltage, current, and power labels"""
    #     self.voltage_label.config(text=f"Voltage: {voltage:.2f}V")
    #     self.current_label.config(text=f"Current: {current:.1f}A")
    #     self.power_label.config(text=f"Power: {power:.1f}kW")

    # def update_bars(self, kw, temp):
    #     """Update the power (kW) and temperature bars"""
    #     self.kw_canvas.delete("all")
    #     self.temp_canvas.delete("all")

    #     kw_fill = int(100 * (kw / 5))  # Assuming max 5kW
    #     temp_fill = int(200 * (temp / 100))  # Assuming max 100°C

    #     self.kw_canvas.create_rectangle(0, 100 - kw_fill, 30, 100, fill="red")
    #     self.temp_canvas.create_rectangle(0, 100 - temp_fill, 30, 100, fill="orange")

    # def update_cell_voltage(self, cell_voltage):
    #     """Update the cell voltage label"""
    #     self.cell_voltage_label.config(text=f"Cell Voltage: {cell_voltage:.3f}V")

    def update_error_label(self, system_errors: set[str]):
        if len(system_errors) > 0:
            error_lines = system_errors.split("\n")
            formatted_message = "/n".join(error_lines)
            self.system_error_label.config(
                text=formatted_message, bg="red", fg="yellow"
            )
        else:
            self.system_error_label.config(text="All OK", bg="black", fg="blue")

    # def show_errors(self, errors):
    #     """Display errors if any"""
    #     if errors:
    #         self.errors.config(text=f"ERRORS: {', '.join(errors)}")
    #     else:
    #         self.error_label.config(text="")

    def refresh_ui(self):
        """Refresh the UI periodically"""
        self.root.update_idletasks()
        self.root.update()

if __name__ == "__main__":
    gui = GUI()
    gui.display_defualt_ui()
    gui.run()
