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

# Création des tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS capteurs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        capteur_id VARCHAR(255) UNIQUE,
        lieu VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS donnees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        capteur_id INT,
        temperature FLOAT,
        timestamp DATETIME,
        FOREIGN KEY (capteur_id) REFERENCES capteurs(id)
    )
""")

# Callback MQTT
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        capteur_id_str = payload.get("capteur_id")
        lieu = payload.get("lieu")
        temperature = float(payload.get("temperature"))
        timestamp = datetime.now()

        if not capteur_id_str or lieu is None or temperature is None:
            print("Message incomplet, ignoré.")
            return

        # Vérifier si le capteur existe déjà
        cursor.execute("SELECT id FROM capteurs WHERE capteur_id = ?", (capteur_id_str,))
        result = cursor.fetchone()

        if result:
            capteur_db_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO capteurs (capteur_id, lieu) VALUES (?, ?)",
                (capteur_id_str, lieu)
            )
            conn.commit()
            capteur_db_id = cursor.lastrowid

        # Insertion de la donnée
        cursor.execute(
            "INSERT INTO donnees (capteur_id, temperature, timestamp) VALUES (?, ?, ?)",
            (capteur_db_id, temperature, timestamp)
        )
        conn.commit()
        print(f"Donnée insérée pour {capteur_id_str} à {timestamp} : {temperature}°C")

    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

# Configuration MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("IUT/Colmar2025/SAE2.04/Maison1")
client.subscribe("IUT/Colmar2025/SAE2.04/Maison2")

# Écoute
print("En attente de messages MQTT...")
client.loop_forever()
