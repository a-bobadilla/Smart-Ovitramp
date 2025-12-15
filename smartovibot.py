import paho.mqtt.client as mqtt
import time
import os

print("\nSistema automático para almacenar fotos de SMART OVI via MQTT")

# Configuración
BROKER = "192.168.100.125"
TOPIC_IMAGE = "smartovi/ovitramp1/imagen"
STORAGE_DIR = "./dataset/"

# Variables de estado
file_saved_in_period = False
current_period_minute = -1

# Asegurar que el directorio existe
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker MQTT con código: {rc}")
    client.subscribe(TOPIC_IMAGE)

def on_message(client, userdata, msg):
    global file_saved_in_period, current_period_minute
    
    current_time = time.localtime()
    minute = current_time.tm_min
    
    # Lógica de intervalo de 2 minutos (minutos pares)
    if minute % 2 == 0:
        # Si cambiamos de minuto o aún no guardamos en este periodo
        if minute != current_period_minute:
            file_saved_in_period = False
            current_period_minute = minute
            
        if not file_saved_in_period:
            timestamp = time.strftime("%Y%m%d%H%M")
            filename = os.path.join(STORAGE_DIR, f"{timestamp}.jpg")
            
            try:
                with open(filename, "wb") as f:
                    f.write(msg.payload)
                print(f"Imagen capturada y guardada: {filename}")
                file_saved_in_period = True
            except Exception as e:
                print(f"Error guardando imagen: {e}")
    else:
        # Resetear estado en minutos impares para estar listos para el siguiente par
        file_saved_in_period = False
        current_period_minute = minute

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"Conectando a {BROKER}...")
    client.connect(BROKER, 1883, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDesconectando...")
    client.disconnect()
except Exception as e:
    print(f"\nError de conexión: {e}")