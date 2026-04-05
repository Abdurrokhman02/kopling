import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input("Ketik data yang ingin disimpan di kartu: ")
    print("tempelkan kartu")

    id,text_written = reader.write(text)

    print(f"Berhasil! Data '{text_written}' telah ditulis pada ID= {id}")
    
finally:
    GPIO.cleanup()