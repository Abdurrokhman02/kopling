from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time

class RFIDReader:
    def __init__(self, mqtt_client=None):
        self.reader = SimpleMFRC522()

        try:
            self.reader = SimpleMFRC522(pin_mode=GPIO.BCM)
        except TypeError:
            self.reader = SimpleMFRC522()
        
        # MQTT client untuk autentikasi
        self.mqtt_client = mqtt_client
        
    def read_card(self):
        # Fungsi ini akan 'blocking' (menunggu) sampai ada kartu yang ditempel
        card_id, text = self.reader.read()
        return card_id
        
    def is_verified(self, card_id, auth_timeout=10):
        """
        Verifikasi kartu melalui MQTT ke database.
        Jika MQTT tersedia, kirim request dan tunggu respon dari server.
        Jika MQTT tidak tersedia, fallback ke pengecekan lokal.
        
        Args:
            card_id: ID kartu yang akan diverifikasi
            auth_timeout: Timeout menunggu respon autentikasi (detik)
            
        Return:
            True jika terverifikasi, False jika tidak
        """
        # Jika MQTT client tersedia, gunakan autentikasi via MQTT
        if self.mqtt_client and self.mqtt_client.connected:
            print(f"[RFID] Mengirim permintaan autentikasi untuk card_id: {card_id}")
            
            # Kirim request autentikasi
            if self.mqtt_client.send_auth_request(card_id):
                # Tunggu respon dari server
                response = self.mqtt_client.wait_for_auth_response(timeout=auth_timeout)
                
                if response:
                    # Cek status dari respon
                    status = response.get("status", False)
                    user_id = response.get("userId")
                    
                    print(f"[RFID] Response: status={status}, userId={user_id}")
                    
                    if status and user_id:
                        print(f"[RFID] User terverifikasi: {user_id}")
                        return True
                    else:
                        print(f"[RFID] Autentikasi ditolak - User tidak terverifikasi")
                        return False
                else:
                    print("[RFID] Timeout menunggu respon autentikasi, fallback ke pengecekan lokal")
                    # Fallback ke pengecekan lokal jika timeout
                    return self._check_local(card_id)
            else:
                print("[RFID] Gagal mengirim permintaan autentikasi, fallback ke pengecekan lokal")
                return self._check_local(card_id)
        else:
            # MQTT tidak tersedia, gunakan pengecekan lokal
            print("[RFID] MQTT tidak tersedia, menggunakan pengecekan lokal")
            return self._check_local(card_id)
    
    def _check_local(self, card_id):
        """Fallback tanpa autentikasi - selalu return False untuk force MQTT auth"""
        print(f"[RFID] No local fallback - MQTT auth required for card_id: {card_id}")
        return False