import paho.mqtt.client as mqtt
import random
import time

# Configurazione del client MQTT
broker = "mqtt-dashboard.com"  # Puoi cambiare con il broker MQTT che preferisci
port = 1883
topic_light = "home/livingRoom/lightsStatus"
topic_shutters = "home/bedRoom/shuttersStatus"
topic_alarm = "home/alarmStatus"


# Creazione del client MQTT
client = mqtt.Client()

# Connessione al broker
client.connect(broker, port, 60)

# Funzione per inviare messaggi casuali
def publish_random_messages():
    while True:
        # Genera un valore casuale per il topic "home/lightStatus"
        light_status = random.choice(["on", "off"])
        client.publish(topic_light, light_status)
        print(f"Published to {topic_light}: {light_status}")

        # Genera un valore casuale per il topic "home/shuttersStatus"
        shutters_status = random.choice(["up", "down"])
        client.publish(topic_shutters, shutters_status)
        print(f"Published to {topic_shutters}: {shutters_status}")

        # Genera un valore casuale per il topic "home/alarmStatus"
        alarm_status = random.choice([1, 0])
        client.publish(topic_alarm, alarm_status)
        print(f"Published to {topic_alarm}: {alarm_status}")

        # Attendi un po' prima di inviare il prossimo messaggio
        time.sleep(10)

# Avvia la pubblicazione dei messaggi
try:
    publish_random_messages()
except KeyboardInterrupt:
    print("Publisher interrotto.")
finally:
    client.disconnect()