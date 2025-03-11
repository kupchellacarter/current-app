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
        system_errors = handler.system_errors
        handler.request_and_parse("soc")
        soc = handler.get_soc()
        # errors = handler.get_errors()
        # gui.show_errors(errors)
        gui.update_error_label(system_errors)
        gui.update_runtime(runtime)
        gui.update_soc(soc)
        gui.update_voltage(voltage)
        gui.refresh_ui()


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
