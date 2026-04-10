import os
import json
import time
import threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

MQTT_CONNACK_REASONS = {
    0: "Connection accepted",
    1: "Connection refused: unacceptable protocol version",
    2: "Connection refused: identifier rejected",
    3: "Connection refused: server unavailable",
    4: "Connection refused: bad user name or password",
    5: "Connection refused: not authorized",
    7: "Connection lost / unexpected disconnect",
}

class MQTTClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # MQTT Configuration
        self.broker = os.getenv('MQTT_BROKER')
        self.port = int(os.getenv('MQTT_PORT', 8883))
        self.username = os.getenv('MQTT_USERNAME')
        self.password = os.getenv('MQTT_PASSWORD')
        self.client_id = os.getenv('MQTT_CLIENT_ID', 'kopling-device-001')
        self.topic_base = os.getenv('MQTT_TOPIC_BASE', 'kopling/')
        self.use_tls = os.getenv('MQTT_USE_TLS', 'true').lower() == 'true'
        self.ca_cert = os.getenv('MQTT_CA_CERT', None)
        self.connect_timeout = int(os.getenv('MQTT_CONNECT_TIMEOUT', 10))

        # Validate required config
        if not self.broker:
            raise ValueError("MQTT_BROKER tidak ditemukan di .env")

        # Initialize MQTT client
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.username_pw_set(self.username, self.password)

        # Configure TLS if needed (port 8883)
        if self.use_tls:
            try:
                if self.ca_cert:
                    self.client.tls_set(ca_certs=self.ca_cert)
                else:
                    # Use default system CA certificates
                    self.client.tls_set()
                self.client.tls_insecure_set(False)
                print("[MQTT] TLS enabled")
            except Exception as e:
                print(f"[MQTT] TLS configuration warning: {e}")

        # Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        # Auto reconnect delay
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)

        self.connected = False
        
        # Response handling untuk autentikasi dan topik lainnya
        self.response_event = threading.Event()
        self.response_data = None
        self.last_response_topic = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"[MQTT] Connected to {self.broker}:{self.port}")
        else:
            self.connected = False
            reason = MQTT_CONNACK_REASONS.get(rc, "Unknown reason")
            print(f"[MQTT] Connection failed with code {rc}: {reason}")

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        reason = MQTT_CONNACK_REASONS.get(rc, "Unknown reason")
        print(f"[MQTT] Disconnected with code {rc}: {reason}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"[MQTT] Received: {msg.topic} -> {payload}")
        
        # Handle response dari auth/response dan topik lainnya
        if "auth/response" in msg.topic:
            try:
                self.response_data = json.loads(payload)
            except:
                self.response_data = payload
            self.last_response_topic = msg.topic
            self.response_event.set()

    def connect(self, timeout=None):
        if self.connected:
            return True

        if timeout is None:
            timeout = self.connect_timeout

        try:
            print(f"[MQTT] Connecting to {self.broker}:{self.port} (timeout: {timeout}s)...")
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()

            waited = 0.0
            while waited < timeout and not self.connected:
                time.sleep(0.1)
                waited += 0.1

            if not self.connected:
                print(f"[MQTT] Connection did not succeed within timeout ({timeout}s)")
                print(f"[MQTT] Check: broker address, credentials, TLS settings, and network connectivity")
            return self.connected
        except ConnectionRefusedError:
            print(f"[MQTT] Connection refused by {self.broker}:{self.port}")
            return False
        except OSError as e:
            print(f"[MQTT] Network error: {e}")
            return False
        except Exception as e:
            print(f"[MQTT] Connection error: {e}")
            return False

    def reconnect(self):
        if self.connected:
            return True

        print("[MQTT] Reconnecting...")
        return self.connect()

    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            try:
                self.client.disconnect()
            except Exception as e:
                print(f"[MQTT] Disconnect error: {e}")

    def publish(self, topic, payload, qos=1, retain=False):
        if not self.connected:
            print("[MQTT] Not connected, cannot publish")
            return False

        full_topic = self.topic_base + topic
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)

            result = self.client.publish(full_topic, payload, qos=qos, retain=retain)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[MQTT] Published to {full_topic}: {payload}")
                return True
            else:
                print(f"[MQTT] Publish failed with code {result.rc}")
                return False
        except Exception as e:
            print(f"[MQTT] Publish error: {e}")
            return False

    def subscribe(self, topic, qos=1):
        if not self.connected:
            print("[MQTT] Not connected, cannot subscribe")
            return False

        full_topic = self.topic_base + topic
        try:
            self.client.subscribe(full_topic, qos=qos)
            print(f"[MQTT] Subscribed to {full_topic}")
            return True
        except Exception as e:
            print(f"[MQTT] Subscribe error: {e}")
            return False

    def send_auth_request(self, card_id):
        """Kirim permintaan autentikasi ke server."""
        payload = {
            "userId": card_id,
        }
        return self.publish("auth", payload)

    def wait_for_auth_response(self, timeout=10):
        """
        Tunggu respon autentikasi dari server.
        
        Args:
            timeout: Waktu menunggu respon dalam detik
            
        Return:
            Dict respon jika diterima, None jika timeout
        """
        self.response_event.clear()
        
        # Tunggu event atau timeout
        if self.response_event.wait(timeout=timeout):
            result = self.response_data
            self.response_data = None
            return result
        else:
            print(f"[MQTT] Timeout menunggu auth response ({timeout}s)")
            return None

    def send_detection_result(self, uid, result):
        """Kirim hasil deteksi ke server dengan format payload standar."""
        payload = {
            "userId": uid,
            "wasteCategory": result.get("wasteCategory", "unknown"),
            "details": result.get("details", []),
            "total": result.get("jumlah", 0)
        }
        return self.publish("detection", payload)

    # def send_status(self, status, message=""):
    #     """Kirim status sistem"""
    #     payload = {
    #         "device_id": self.client_id,
    #         "status": status,
    #         "message": message
    #     }
    #     return self.publish("status", payload)

if __name__ == "__main__":
    # Test MQTT connection
    mqtt_client = MQTTClient()
    if mqtt_client.connect():
        # Test publish
        mqtt_client.publish("test", {"message": "Hello from Kopling!"})
        import time
        time.sleep(2)
        mqtt_client.disconnect()
    else:
        print("Failed to connect to MQTT broker")