from RPLCD.i2c import CharLCD

class LCDDisplay:
    def __init__(self, i2c_address=0x27):
        # 0x27 adalah alamat I2C standar, bisa juga 0x3f tergantung modul PCF8574 kamu
        # Menggunakan format LCD 16x2
        self.lcd = CharLCD('PCF8574', i2c_address, port=1, charmap='A00', cols=16, rows=2)
        self.clear()
        
    def show_message(self, line1, line2=""):
        self.clear()
        # Menulis di baris pertama
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(line1)
        
        # Menulis di baris kedua jika ada teksnya
        if line2:
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(line2)
            
    def clear(self):
        self.lcd.clear()