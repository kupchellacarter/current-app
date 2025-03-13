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
        self.charge_level = 0
        self.mean_voltage = 0
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor="none")
        self.root.overrideredirect(True)
        self.root.geometry("800x480")  # Set to your screen size
        self.root.config(bg="black")

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def display_defualt_ui(self):
        # Frame Nest
        self.outer_frame = tk.Frame(self.root, bg="white", width=780, height=460)
        self.outer_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.top_frame = tk.Frame(self.outer_frame, bg="red", width=760, height=100)
        self.top_frame.pack(side="top", fill="x")
        self._create_soc_frame()
        self.set_soc(55)

        # Runtime Frame
        self.runtime_frame = tk.Frame(self.root, bg="white", width=50, height=20)
        self.runtime_frame.pack(anchor="sw", side="bottom", padx=10, pady=5)
        self.runtime_label = tk.Label(
            self.runtime_frame,
            text="Runtime:",
            font=(self.font, 14),
            bg="black",
            fg="white",
        )
        self.runtime_label.pack(side="bottom")

        # Bottom Frame
        self.bottom_frame = tk.Frame(self.outer_frame, bg="green", width=760, height=80)
        self.bottom_frame.pack(anchor="s", side="bottom", fill="x")

        # Voltage Frame
        self.voltage_frame = tk.Frame(
            self.outer_frame, bg="white", width=760, height=80
        )
        self.voltage_frame.pack(side="bottom", fill="x")
        self._create_cell_voltage_frame()

        # Central Frame
        self.central_frame = tk.Frame(
            self.outer_frame, bg="blue", height=200, width=560
        )
        self.central_frame.pack(side="left", fill="y")

        # Central Metrics
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

        # Error Display
        self.system_error_label = tk.Label(
            self.bottom_frame,
            text="All OK",
            font=(self.font, 32),
            bg="white",
            fg="blue",
        )
        self.system_error_label.pack(anchor="s", side="bottom")

    def _create_soc_frame(self):
        # Battery soc Display (Top)
        self.soc_canvas = tk.Canvas(self.top_frame, width=760, height=50, bg="black")
        self.soc_canvas.pack(side="top", fill="x")

    def _create_cell_voltage_frame(self):
        # Battery soc Display (Top)
        self.cell_voltage_canvas = tk.Canvas(
            self.voltage_frame, width=700, height=50, bg="black"
        )
        self.cell_voltage_canvas.pack(side="top", fill="x")

    def set_pack_kwh(self, current_kwh, max_kwh):
        # Battery percentage text below
        self.soc_canvas.create_text(
            550,
            40,
            text=f"{current_kwh}/{max_kwh}",
            fill="white",
            font=(self.font, 12),
        )

    def set_cell_voltage(self, mean_voltage=80):
        # only update the charge level if it has changed
        if self.mean_voltage != mean_voltage:
            logger.warning(f"Updating Cell Voltage to {mean_voltage}")
            self.cell_voltage_canvas.delete("all")
            self.mean_voltage = mean_voltage
            num_sections = 100
            section_width = (690 - 30) / num_sections  # Calculate section width
            for i in range(num_sections):
                x1 = 30 + i * section_width
                space = 3 if (i + 1) % 10 == 0 else 0
                x2 = x1 + section_width - space  # Add small gap for spacing

                # Green for filled sections, black for empty, with blue outline for empty ones
                if i < (self.charge_level / 100) * num_sections:
                    fill_color = "green"
                    outline_color = "green"
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
                675, 25, text="F", fill="white", font=(self.font, 30, "bold")
            )
            self.soc_canvas.create_text(
                350,
                25,
                text=f"{mean_voltage}%",
                fill="white",
                font=(self.font, 30, "bold"),
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

    def set_cell_voltage(self, mean_cell_v):
        """Update the cell voltage label"""
        pass
        # self.cell_voltage_label.config(text=f"Cell Voltage: {mean_cell_v}")
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
    gui.run()
