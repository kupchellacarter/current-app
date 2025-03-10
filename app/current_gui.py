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
        self.root.attributes("-fullscreen", False)
        self.root.config(cursor="none")
        # self.root.overrideredirect(True)
        self.root.geometry("800x480")  # Set to your screen size
        self.root.config(bg="black")

        # Frame Nest
        self.outer_frame = tk.Frame(self.root, bg="black", width=760, height=360)
        self.outer_frame.pack(padx=40, pady=40)

        # Top Frame (SOC)
        self.top_frame = tk.Frame(self.outer_frame, bg="black", width=760, height=100)
        self.top_frame.pack(side="top", fill="x")

        # Bottom Frame
        self.bottom_frame = tk.Frame(self.outer_frame, bg="blue", width=760, height=100)
        self.bottom_frame.pack(side="bottom", fill="x")

        # Central Frame
        self.central_frame = tk.Frame(
            self.outer_frame, bg="black", width=560, height=160
        )
        self.central_frame.pack(side="left", fill="y")

        # Right Frame
        self.right_frame = tk.Frame(self.root, bg="black", width=200, height=160)
        self.right_frame.pack(side="right", fill="y")

        # Battery SOC Display
        self.soc_canvas = tk.Canvas(self.top_frame, width=700, height=50, bg="black")
        self.soc_canvas.pack(pady=10)
        self.soc_text = tk.Label(
            self.top_frame,
            text="pack_voltage",
            font=(self.font, 20),
            bg="black",
            fg="white",
        )
        self.soc_text.pack(pady=5)

        # Central Metrics
        self.voltage_label = tk.Label(
            self.central_frame,
            text="Voltage: 0V",
            font=(self.font, 32),
            bg="black",
            fg="white",
        )
        self.voltage_label.grid(row=0, column=0, pady=5)

        self.current_label = tk.Label(
            self.central_frame,
            text="Current: 0A",
            font=(self.font, 32),
            bg="black",
            fg="white",
        )
        self.current_label.grid(row=1, column=0, pady=5)

        self.power_label = tk.Label(
            self.central_frame,
            text="Power: 0kW",
            font=(self.font, 32),
            bg="black",
            fg="white",
        )
        self.power_label.grid(row=2, column=0, pady=5)

        # Power and Temperature Bars (vertical)
        self.kw_canvas = tk.Canvas(self.right_frame, width=30, height=100, bg="blue")
        self.kw_canvas.grid(row=0, column=0, pady=5)

        self.temp_canvas = tk.Canvas(self.right_frame, width=30, height=100, bg="blue")
        self.temp_canvas.grid(row=0, column=1, pady=5)

        # Cell Voltage Range
        self.cell_voltage_label = tk.Label(
            self.bottom_frame,
            text="Cell Voltage: 0.000V",
            font=(self.font, 24),
            bg="black",
            fg="white",
        )
        self.cell_voltage_label.pack(pady=5)

        # Error Display
        self.system_error_label = tk.Label(
            self.central_frame,
            text="System Errors:",
            font=(self.font, 32),
            bg="black",
            fg="white",
        )
        self.current_label.grid(row=1, column=0, pady=5)

    def update_error_label(self, system_errors: set[str]):
        if system_errors:
            error_lines = system_errors.split("\n")
            formatted_message = "/n".join(error_lines)
            self.system_error_label.config(
                text=formatted_message, bg="red", fg="yellow"
            )
        else:
            self.system_error_label.config(text="All OK", bg="black", fg="blue")

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def update_soc(self, soc):
        """Update the State of Charge (SOC) bar"""
        self.soc_canvas.delete("all")
        bar_width = int(300 * (soc / 100))
        color = "green" if soc > 50 else "yellow" if soc > 20 else "red"
        self.soc_canvas.create_rectangle(0, 0, bar_width, 50, fill=color)
        self.soc_canvas.create_text(
            150, 25, text=f"{soc:.1f}%", fill="white", font=(self.font, 20)
        )

    def update_metrics(self, voltage, current, power):
        """Update the voltage, current, and power labels"""
        self.voltage_label.config(text=f"Voltage: {voltage:.2f}V")
        self.current_label.config(text=f"Current: {current:.1f}A")
        self.power_label.config(text=f"Power: {power:.1f}kW")

    def update_bars(self, kw, temp):
        """Update the power (kW) and temperature bars"""
        self.kw_canvas.delete("all")
        self.temp_canvas.delete("all")

        kw_width = int(200 * (kw / 5))  # Assuming max 5kW
        temp_width = int(200 * (temp / 100))  # Assuming max 100°C

        self.kw_canvas.create_rectangle(0, 0, kw_width, 30, fill="red")
        self.temp_canvas.create_rectangle(0, 0, temp_width, 30, fill="orange")

    def update_cell_voltage(self, cell_voltage):
        """Update the cell voltage label"""
        self.cell_voltage_label.config(text=f"Cell Voltage: {cell_voltage:.3f}V")

    def show_errors(self, errors):
        """Display errors if any"""
        if errors:
            self.error_label.config(text=f"ERRORS: {', '.join(errors)}")
        else:
            self.error_label.config(text="")

    def refresh_ui(self):
        """Refresh the UI periodically"""
        self.root.update_idletasks()
        self.root.update()
