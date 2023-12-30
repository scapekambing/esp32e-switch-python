import paho.mqtt.client as mqtt
import threading
import time

class User:

    def __init__(self, id, client, broker):
        self.id = id
        self.client = client
        self.broker = broker
        self.is_spraying = False
        self.stop_event = threading.Event()

    def connect(self):
        self.client.connect(self.broker)

    def send(self, msg):
        if msg == "spray":
            print("Spraying... \U0001F608")
            self.is_spraying = True
        elif msg == "stop":
            print("Stopping... \U0001F607")
            self.is_spraying = False
        else:
            print("Invalid input. Valid inputs are 'spray' or 'stop'.")

        self.client.publish("esp32e-switch/switch", str(msg))

    def input_timer(self):
        time.sleep(5)
        self.stop_event.set()  # Set the event to signal input timeout

    def disconnect(self):
        if self.is_spraying:
            print("Stopping spray before disconnecting... \U0001F607")
            self.client.publish("esp32e-switch/switch", "stop")
            time.sleep(1)
        self.client.disconnect()

def main():
    mqttBroker = "broker.emqx.io"

    user = User(id=1,
                client=mqtt.Client("exec"),
                broker=mqttBroker)

    try:
        user.connect()

        # Create and start threads
        input_thread = threading.Thread(target=user.input_timer)
        input_thread.start()

        while not user.stop_event.is_set():
            msg = input("Enter 'spray' to start spraying or 'stop' to stop spraying: ")
            user.send(msg)

        print("Timeout. Disconnecting and stopping spray...")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting gracefully...")
    finally:
        user.disconnect()
        input_thread.join()
        print("Program exited gracefully.")

if __name__ == "__main__":
    main()
