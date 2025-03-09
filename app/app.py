from current_gui import GUI
from message_handler import MessageHandler
import threading


def query_data(gui: GUI, handler: MessageHandler):
    """
    queries data
    """
    while True:
        handler.request_runtime_data()
        runtime = handler.get_runtime_data()
        gui.update_runtime(runtime)
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
