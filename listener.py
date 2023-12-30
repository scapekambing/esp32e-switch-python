import paho.mqtt.client as mqtt

TOPIC = "home/esp32e/turret"

class Listener:

    def __init__(self, broker):
        self.client = mqtt.Client("listener")
        self.broker = broker

    def connect(self):
        self.client.connect(self.broker)
        self.client.subscribe(TOPIC)  # Subscribe to the switch topic
        self.client.on_message = self.on_message  # Set the on_message callback

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        print(f"Received message: {message}")

    def listen(self):
        self.client.loop_forever()

def main():
    mqttBroker = "broker.emqx.io"

    listener = Listener(broker=mqttBroker)

    try:
        listener.connect()
        listener.listen()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting gracefully...")
    finally:
        listener.client.disconnect()
        print("Program exited gracefully.")

if __name__ == "__main__":
    main()
