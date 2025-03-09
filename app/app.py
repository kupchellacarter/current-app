from current_gui import GUI
from message_handler import MessageHandler


def query_data(gui: GUI, handler: MessageHandler):
    """
    queries data
    """
    while True:
        # handler.request_runtime_data()
        handler.set_runtime_data(12)
        runtime = handler.get_runtime_data()
        runtime = handler.get_runtime_data()


def main():
    """
    description here
    """
    gui = GUI()
    handler = MessageHandler()


if __name__ == "__main__":
    main()
