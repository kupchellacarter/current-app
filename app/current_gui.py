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

        # Battery SOC Display
        self.soc_canvas = tk.Canvas(self.root, width=300, height=50, bg="black")
        self.soc_canvas.pack(pady=10)

        # Central Metrics
        self.voltage_label = tk.Label(
            self.root, text="Voltage: 0V", font=(self.font, 32)
        )
        self.voltage_label.pack(pady=5)

        self.current_label = tk.Label(
            self.root, text="Current: 0A", font=(self.font, 32)
        )
        self.current_label.pack(pady=5)

        self.power_label = tk.Label(self.root, text="Power: 0kW", font=(self.font, 32))
        self.power_label.pack(pady=5)

        # Power and Temperature Bars
        self.kw_canvas = tk.Canvas(self.root, width=200, height=30, bg="black")
        self.kw_canvas.pack(pady=5)

        self.temp_canvas = tk.Canvas(self.root, width=200, height=30, bg="black")
        self.temp_canvas.pack(pady=5)

        # Cell Voltage Range
        self.cell_voltage_label = tk.Label(
            self.root, text="Cell Voltage: 0.000V", font=(self.font, 24)
        )
        self.cell_voltage_label.pack(pady=5)

        # Error Display
        self.error_label = tk.Label(self.root, font=(self.font, 15), fg="red")
        self.error_label.pack(pady=10)

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
