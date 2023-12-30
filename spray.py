import paho.mqtt.client as mqtt
import threading
import time

TOPIC = "home/esp32e/turret"

class User:

    def __init__(self, id, client, broker):
        self.id = id
        self.client = client
        self.broker = broker
        self.is_spraying = False
        self.done_spraying = True
        self.active = True

    def connect(self):
        self.client.connect(self.broker)
        self.client.subscribe(TOPIC)  # Subscribe to the switch topic
        self.client.on_message = self.on_message  # Set the on_message callback

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")

        if message == "spray":
            print("Spraying... \U0001F608")
            self.is_spraying = True
        elif message == "stop":
            print("Stopping... \U0001F607")
            self.is_spraying = False
        elif message == "end":
            print("Spraying complete. \U0001F60E")
            self.is_spraying = False
            self.active = False
        else:
            print("Invalid input. Valid inputs are 'spray', 'stop' or 'end'.")
        
        self.done_spraying = True

    def send(self, msg):
        self.client.publish(TOPIC, str(msg))
        self.done_spraying = False

    def disconnect(self):
        if self.is_spraying:
            print("Stopping spray before disconnecting...")
            self.send("stop")
            time.sleep(1)
        self.client.disconnect()

def main():
    mqttBroker = "broker.emqx.io"

    user = User(id=1,
                client=mqtt.Client("exec"),
                broker=mqttBroker)

    try:
        user.connect()
        user.client.loop_start()  # Start the MQTT client's threaded loop

        while (user.active):
            if(user.done_spraying):
                msg = input("Enter 'spray' to start spraying, 'stop' to stop spraying or 'end' to terminate the program: ")
                user.send(msg)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting gracefully...")
    finally:
        user.disconnect()
        print("Program exited gracefully.")

if __name__ == "__main__":
    main()
