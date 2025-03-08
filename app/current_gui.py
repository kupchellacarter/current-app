import tkinter as tk
# import can  # Commented out because CAN integration is not needed yet
# import threading  # Commented out because threading is not needed yet

# Commented out CAN-related function for now
# def read_can(bus, text_widget):
#     for msg in bus:
#         display_msg = f"ID: {msg.arbitration_id:03X} Data: {msg.data.hex()}"
#         text_widget.insert(tk.END, display_msg + "\n")
#         text_widget.see(tk.END)

# Commented out CAN-related listener setup
# def start_can_listener(text_widget):
#     bus = can.interface.Bus(channel='can0', bustype='socketcan')
#     threading.Thread(target=read_can, args=(bus, text_widget), daemon=True).start()

def create_gui():
    root = tk.Tk()
    root.title("Electric Boat Dashboard")
    # Set the window to full screen
    root.attributes('-fullscreen', True)
    # Hide the window cursor
    root.config(cursor="none")

    # Remove window decorations (title bar, borders, etc.)
    root.overrideredirect(True)
    root.geometry("800x480")  # Set to your screen size

    # Create a title label
    label = tk.Label(root, text="Electric Boat Control", font=("Helvetica", 24))
    label.pack(pady=20)

    # Placeholder for any live data or messages
    text_widget = tk.Text(root, wrap=tk.WORD, font=("Courier", 16))
    text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Example of adding buttons to the interface (you can add more as needed)
    button = tk.Button(root, text="Start Motor", font=("Helvetica", 16), width=20)
    button.pack(pady=20)

    # Placeholder for a speed slider
    speed_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Speed", font=("Helvetica", 16))
    speed_slider.pack(pady=20)

    # Placeholder for battery status (can be updated later)
    battery_label = tk.Label(root, text="Battery: 100%", font=("Helvetica", 16))
    battery_label.pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
