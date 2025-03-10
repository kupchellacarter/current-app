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

        # Create a title label
        label = tk.Label(self.root, text="Current", font=(self.font, 50))
        label.pack(pady=20)

        self.runtime_label = tk.Label(self.root, text="Runtime: ", font=(self.font, 32))
        self.runtime_label.pack(pady=10)
        self.volage_label = tk.Label(
            self.root, text="Pack Voltage: ", font=(self.font, 32)
        )
        self.voltage_label.pack(pady=10)

        self.error_label = tk.Label(
            self.root,
            font=(self.font, 15),
            fg="red",
        )
        self.error_label.pack(pady=10)

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def update_runtime(self, runtime_value):
        """
        Method to update the displayed variables dynamically
        """
        # Update the labels with new values
        logger.warning(f"Updating runtime value: {runtime_value}")
        self.runtime_label.config(text=f"Runtime: {runtime_value}")

    def update_voltage(self, runtime_value):
        """
        Method to update the displayed variables dynamically
        """
        # Update the labels with new values
        # logger.warning(f"Updating runtime value: {runtime_value}")
        # self.runtime_label.config(text=f"Runtime: {runtime_value}")
        pass

    def show_errors(self, errors: list[str]):
        """
        Method to display errors in the user interface
        """
        if len(errors) > 0:
            self.error_label.config(text=f"ERRORS: {', '.join(errors)}")

    def refresh_ui(self):
        """
        Method to refresh the UI
        """
        self.root.update_idletasks()
        self.root.update()
