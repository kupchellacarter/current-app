from current_gui import GUI
from message_handler import MessageHandler
import threading


def query_data(gui: GUI, handler: MessageHandler):
    """
    queries data and updates GUI
    """
    while True:
        handler.request_and_parse("runtime")
        runtime = handler.get_runtime()

        handler.request_and_parse("voltage")
        voltage = handler.get_voltage()

        handler.request_and_parse("current")
        current = handler.get_current()

        handler.request_and_parse("power")
        power = handler.get_power()

        handler.request_and_parse("cell_voltage")
        cell_voltage = handler.get_cell_voltage()

        handler.request_and_parse("errors")
        errors = handler.get_errors()

        # Schedule updates on the main thread using root.after
        gui.root.after(0, gui.update_metrics, voltage, current, power)
        gui.root.after(0, gui.update_cell_voltage, cell_voltage)
        gui.root.after(0, gui.show_errors, errors)


def main():
    """
    description here
    """
    gui = GUI()
    # Create MessageHandler instance
    handler = MessageHandler()

    # Start the query_data function in a separate background thread
    query_thread = threading.Thread(target=query_data, args=(gui, handler), daemon=True)
    query_thread.start()
    gui.run()


if __name__ == "__main__":
    main()
