import paho.mqtt.client as mqtt
from datetime import datetime as dt
import time

mqtt_server = "mqtt-dashboard.com"
mqtt_port = 1883
mqtt_topic_temperature = "home/temperature"
mqtt_topic_humidity = "home/humidity"
mqtt_topic_lightPercent = "home/livingRoom/lightPercent"
mqtt_topic_shutters = "home/bedRoom/shuttersStatus"
mqtt_topic_lights = "home/livingRoom/lightsStatus"
mqtt_topic_alarm = "home/alarmStatus"

# Simulated devices
SHUTTER_OPEN = "up"
SHUTTER_CLOSED = "down"
LIGHT_ON = "on"
LIGHT_OFF = "off"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")

        # Subscribe to the topics
        client.subscribe(mqtt_topic_temperature, qos=1)
        client.subscribe(mqtt_topic_humidity, qos=1)
        client.subscribe(mqtt_topic_lightPercent, qos=1)
        client.subscribe(mqtt_topic_alarm, qos=1)
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    topic = message.topic
    retained = message.retain # Check if the message is a retained message

    if retained:
        print(f"This is a retained message from {topic} : {payload}")
        return

    current_time = dt.now().strftime("%d/%m/%Y - %H:%M:%S")

    print ("Message received at: " + str(current_time))
    print(f"Received message from '{topic}': {payload}")

    # Smart Home Logic
    check_and_control_shutters(client, current_time)
    check_and_control_lights(client, current_time, payload, topic)  # Pass payload and topic

def check_and_control_shutters(client, current_time):
    hour = current_time.hour
    day_of_week = current_time.weekday() # 0 = Monday, 6 = Sunday

    if day_of_week < 5: 
        if hour == 8 and current_time.minute == 30 and isDark():
            print("It's 8:30 AM on a weekday and it's dark. Opening shutters.")
            client.publish(mqtt_topic_shutters, SHUTTER_OPEN)  # Publish command to open shutters

    elif day_of_week >= 5:
        if hour == 10 and current_time.minute == 0 and isDark():
            print("It's 10:00 AM on a weekend and it's dark. Opening shutters.")
            client.publish(mqtt_topic_shutters, SHUTTER_OPEN) # Publish command to open shutters

def check_and_control_lights(client, current_time, payload, topic):
    hour = current_time.hour
    
    if topic == mqtt_topic_lightPercent:
        try: 
            lux_percent = float(payload)
            if 17 <= hour <= 22 and lux_percent < 20:
                print("It's evening/night and light level is low. Turning on soft lights.")
                client.publish(mqtt_topic_lights, LIGHT_ON)
        except ValueError:
            print(f"Invalid lightPercent Value: {payload}")
            

def isDark():
    return True  # Simulated function

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, mqtt_port, 60) # 60 seconds keepalive

print("Subscriber is running...")
client.loop_forever()