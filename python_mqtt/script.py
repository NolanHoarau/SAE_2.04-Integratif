import paho.mqtt.client as mqtt
import mariadb
import json
from datetime import datetime

# Configuration DB
db_config = {
    "host": "localhost",
    "user": "toto",
    "password": "toto",
    "database": "sae204"
}

# Connexion DB
try:
    conn = mariadb.connect(**db_config)
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Erreur de connexion à MariaDB: {e}")
    exit(1)

# Création des tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS capteur (
        capteur_id INT AUTO_INCREMENT PRIMARY KEY,
        capteur_nom VARCHAR(100),
        piece VARCHAR(100),
        emplacement VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS data (
        data_id INT AUTO_INCREMENT PRIMARY KEY,
        datetime DATETIME,
        temperature FLOAT,
        capteur_id INT,
        FOREIGN KEY(capteur_id) REFERENCES capteur(capteur_id)
    )
""")

# Fonction pour obtenir l'ID du capteur (ou le créer)
def get_or_create_capteur_id(capteur_nom, piece, emplacement):
    cursor.execute(
        "SELECT capteur_id FROM capteur WHERE capteur_nom=? AND piece=? AND emplacement=?",
        (capteur_nom, piece, emplacement)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute(
            "INSERT INTO capteur (capteur_nom, piece, emplacement) VALUES (?, ?, ?)",
            (capteur_nom, piece, emplacement)
        )
        conn.commit()
        return cursor.lastrowid

# Callback MQTT
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        print(f"Reçu sur {topic} : {payload}")

        # Parsing du payload (ex: Id=A72E3F6B79BB,piece=chambre1,date=23/06/2025,time=10:11:27,temp=14.25)
        data_dict = dict(part.split("=") for part in payload.split(","))
        
        capteur_nom = data_dict["Id"]
        piece = data_dict["piece"]
        date_str = data_dict["date"]
        time_str = data_dict["time"]
        temp = float(data_dict["temp"])
        emplacement = topic.split("/")[-1]  # "Maison1" ou "Maison2"

        # Conversion en datetime
        datetime_str = f"{date_str} {time_str}"
        timestamp = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")

        # Récupération ou insertion du capteur
        capteur_id = get_or_create_capteur_id(capteur_nom, piece, emplacement)

        # Insertion dans la table data
        cursor.execute(
            "INSERT INTO data (datetime, temperature, capteur_id) VALUES (?, ?, ?)",
            (timestamp, temp, capteur_id)
        )
        conn.commit()
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

# Configuration client MQTT
client = mqtt.Client()
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("IUT/Colmar2025/SAE2.04/Maison1")
client.subscribe("IUT/Colmar2025/SAE2.04/Maison2")

print("En attente de messages MQTT...")
client.loop_forever()
