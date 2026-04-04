from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

class RFIDReader:
    def __init__(self, registered_ids):
        self.reader = SimpleMFRC522()

        try:
            self.reader = SimpleMFRC522(pin_mode=GPIO.BCM)
        except TypeError:
            self.reader = SimpleMFRC522()

        # Menyimpan list ID kartu yang punya akses
        self.registered_ids = registered_ids
        
    def read_card(self):
        # Fungsi ini akan 'blocking' (menunggu) sampai ada kartu yang ditempel
        card_id, text = self.reader.read()
        return card_id
        
    def is_verified(self, card_id):
        # Mengecek apakah ID kartu ada di dalam list yang terdaftar
        return card_id in self.registered_ids