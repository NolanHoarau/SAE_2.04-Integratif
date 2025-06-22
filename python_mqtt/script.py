import paho.mqtt.client as mqtt
import mariadb
import json
from datetime import datetime

# Configuration de la base de données
db_config = {
    "host": "localhost",
    "user": "toto",
    "password": "toto",
    "database": "sae204"
}

# Connexion à la base de données
try:
    conn = mariadb.connect(**db_config)
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Erreur de connexion à MariaDB: {e}")
    exit(1)

# Création de la table si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mqtt_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        topic VARCHAR(255),
        message TEXT,
        timestamp DATETIME
    )
""")

# Callback quand on reçoit un message MQTT
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        timestamp = datetime.now()

        print(f"Reçu sur {topic} : {payload}")

        # Insertion dans la base de données
        cursor.execute(
            "INSERT INTO mqtt_data (topic, message, timestamp) VALUES (?, ?, ?)",
            (topic, payload, timestamp)
        )
        conn.commit()
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

# Configuration du client MQTT
client = mqtt.Client()
client.on_message = on_message

# Connexion au broker
client.connect("test.mosquitto.org", 1883, 60)

# Souscription aux topics
client.subscribe("IUT/Colmar2025/SAE2.04/Maison1")
client.subscribe("IUT/Colmar2025/SAE2.04/Maison2")

# Boucle infinie pour écouter les messages
print("En attente de messages MQTT...")
client.loop_forever()

