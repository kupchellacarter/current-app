import tkinter as tk
import logging

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
        self.outer_frame = tk.Frame(self.root, bg="black", width=780, height=460)
        self.outer_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.top_frame = tk.Frame(self.outer_frame, bg="red", width=760, height=100)
        self.top_frame.pack(side="top", fill="x")
        self._create_soc_frame()
        self.set_soc(55)

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

        # self.cell_count_frame = tk.Frame(self.root, bg="black", width=50, height=20)
        self.runtime_frame.pack(anchor="se", side="bottom", padx=10, pady=5)
        self.cell_count_label = tk.Label(
            self.runtime_frame,
            text=" Cells Connected",
            font=(self.font, 14),
            bg="black",
            fg="white",
        )
        self.cell_count_label.pack(anchor="se", padx=10, pady=10)

        # Bottom (error message) Frame
        self.bottom_frame = tk.Frame(
            self.outer_frame, bg="black", width=760, height=100
        )
        self.bottom_frame.pack(anchor="s", side="bottom", fill="x")

        # Central Left Frame
        self.central_frame = tk.Frame(
            self.outer_frame, bg="black", height=200, width=560
        )
        self.central_frame.pack(side="left", fill="y", expand=True)

        # Central Right Frame
        self.right_frame = tk.Frame(self.outer_frame, bg="black", height=200, width=200)
        self.right_frame.pack(side="right", fill="y")

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

        self.cell_voltage_canvas = tk.Canvas(
            self.right_frame, bg="white", width=360, height=20
        )
        self.cell_voltage_canvas.pack(anchor="e", padx=10, pady=10)

        # Error Display
        self.system_error_label = tk.Label(
            self.bottom_frame,
            text="All OK",
            font=(self.font, 32),
            bg="blue",
            fg="white",
        )
        self.system_error_label.pack(anchor="s", side="bottom")

    def _create_soc_frame(self):
        # Battery soc Display (Top)
        self.soc_canvas = tk.Canvas(self.top_frame, width=760, height=50, bg="black")
        self.soc_canvas.pack(side="top", fill="x")

    # def _create_cell_voltage_canvas(self):
    #     self.cell_voltage_canvas = tk.Canvas(
    #         self.central_frame, width=350, height=50, bg="black"
    #     )
    #     self.cell_voltage_canvas.pack(side="top", fill="x")

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
            self.cell_voltage_label.config(text=f"Cell Voltage: {mean_voltage}")
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

    def set_temp(self, temp):
        self.temp_label.config(text=f"Temperature: {temp}")

    def set_cell_count(self, cell_count):
        if cell_count == 16:
            self.cell_count_label.config(text=f"{cell_count} Cells OK!")
        else:
            self.cell_count_label.config(
                text=f"Check Cells! {cell_count} Cells Connected"
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
