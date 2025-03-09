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
        self.root.title("Electric Boat Dashboard")
        # Set the window to full screen
        self.root.attributes("-fullscreen", False)
        # Hide the window cursor
        self.root.config(cursor="none")
        # Remove window decorations (title bar, borders, etc.)
        # self.root.overrideredirect(True)
        self.root.geometry("800x480")  # Set to your screen size

        # Create a title label
        label = tk.Label(
            self.root, text="Electric Boat Control", font=("Helvetica", 50)
        )
        label.pack(pady=20)

        # Placeholder for displaying variables (runtime and Var2) with larger font size
        self.runtime_label = tk.Label(
            self.root, text="Runtime: ", font=("Helvetica", 32)  # Increased font size
        )
        self.runtime_label.pack(pady=10)

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def update_runtime(self, runtime_value):
        """
        Method to update the displayed variables dynamically
        """
        # Update the labels with new values
        logger.info(f"Updating runtime value: {runtime_value}")
        self.runtime_label.config(text=f"Runtime: {runtime_value}")

    def refresh_ui(self):
        """
        Method to refresh the UI
        """
        self.root.update_idletasks()
        self.root.update()
