import random
import string
import json
import xml.etree.ElementTree as ET
import os
import io
import wave
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .constants import CARD_PREFIXES, BANK_BINS, fake_ru, fake_en
from .utils import luhn_checksum, calculate_luhn
from tkinter import messagebox

def generate_card_number(card_type, length):
    prefix = CARD_PREFIXES[card_type]
    number = [int(x) for x in str(prefix)]
    while len(number) < length - 1:
        number.append(random.randint(0, 9))
    check_digit = calculate_luhn(int(''.join(map(str, number))))
    return ''.join(map(str, number)) + str(check_digit)

def generate_turkish_iban():
    country_code = "TR"
    check_digits = "00"
    bank_code = str(random.randint(10000, 99999))
    account_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    iban = f"{country_code}{check_digits}{bank_code}0{account_number}"
    return iban

def generate_russian_phone_number():
    return f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

def generate_phone_number_01():
    return f"01{random.randint(100000000, 999999999)}"

def generate_upi_id(language):
    # Всегда используем fake_en для генерации имени, игнорируя параметр language
    name = fake_en.name().lower().replace(' ', '')
    return f"{name}@{random.choice(['ybl', 'oksbi', 'ibl', 'axl'])}"

def generate_ifsc_code():
    bank_codes = ["SBIN", "HDFC", "ICIC", "AXIS", "PUNB"]
    return f"{random.choice(bank_codes)}0{random.randint(100000, 999999)}"

def generate_utr_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def generate_address():
    return fake_ru.address() if random.choice([True, False]) else fake_en.address()

def generate_postcode():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def generate_cuil():
    dni = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    prefix = random.choice(['20', '27', '23', '24'])
    multipliers = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(a) * b for a, b in zip(prefix + dni, multipliers))
    control = 11 - (total % 11)
    if control == 11:
        control = 0
    elif control == 10:
        control = 9
    return f"{prefix}-{dni}-{control}"

def generate_card_number_by_bin(bin_prefix):
    number = [int(x) for x in str(bin_prefix)]
    while len(number) < 15:
        number.append(random.randint(0, 9))
    check_digit = calculate_luhn(int(''.join(map(str, number))))
    return ''.join(map(str, number)) + str(check_digit)

def generate_file(file_type, size_mb, output_path, progress_var):
    size_bytes = int(size_mb * 1024 * 1024)
    
    if file_type in ['.txt', '.csv', '.json', '.xml', '.html']:
        generate_text_file(file_type, size_bytes, output_path, progress_var)
    elif file_type in ['.bin', '.exe', '.dll']:
        generate_binary_file(file_type, size_bytes, output_path, progress_var)
    elif file_type in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        generate_image_file(file_type, size_bytes, output_path, progress_var)
    elif file_type == '.wav':
        generate_audio_file(file_type, size_bytes, output_path, progress_var)
    elif file_type == '.pdf':
        generate_pdf_file(size_bytes, output_path, progress_var)
    else:
        messagebox.showerror("Error", f"Unsupported file type: {file_type}")

def generate_text_file(file_type, size_bytes, output_path, progress_var):
    fake = fake_ru if random.choice([True, False]) else fake_en
    with open(output_path, 'wb') as f:
        bytes_written = 0
        while bytes_written < size_bytes:
            if file_type == '.txt':
                content = fake.text() + '\n'
            elif file_type == '.csv':
                content = f"{fake.name()},{fake.email()},{fake.phone_number()}\n"
            elif file_type == '.json':
                content = json.dumps({'name': fake.name(), 'email': fake.email()}) + '\n'
            elif file_type == '.xml':
                root = ET.Element("person")
                ET.SubElement(root, "name").text = fake.name()
                ET.SubElement(root, "email").text = fake.email()
                content = ET.tostring(root, encoding='unicode') + '\n'
            elif file_type == '.html':
                content = f"<p>{fake.text()}</p>\n"
            
            content_bytes = content.encode('utf-8')
            if bytes_written + len(content_bytes) > size_bytes:
                content_bytes = content_bytes[:size_bytes - bytes_written]
            
            f.write(content_bytes)
            bytes_written += len(content_bytes)
            progress_var.set(min(100, int(bytes_written / size_bytes * 100)))
        
        if bytes_written < size_bytes:
            f.write(b'\0' * (size_bytes - bytes_written))

def generate_binary_file(file_type, size_bytes, output_path, progress_var):
    with open(output_path, 'wb') as f:
        bytes_written = 0
        chunk_size = 1024 * 1024
        while bytes_written < size_bytes:
            remaining = size_bytes - bytes_written
            chunk = os.urandom(min(chunk_size, remaining))
            f.write(chunk)
            bytes_written += len(chunk)
            progress_var.set(min(100, int(bytes_written / size_bytes * 100)))

def generate_image_file(file_type, size_bytes, output_path, progress_var):
    width = height = int((size_bytes / 3) ** 0.5)
    image = Image.new('RGB', (width, height), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    image_format = file_type[1:].upper()
    if image_format == 'JPG':
        image_format = 'JPEG'
    
    buffer = io.BytesIO()
    image.save(buffer, format=image_format)
    
    with open(output_path, 'wb') as f:
        if buffer.tell() > size_bytes:
            f.write(buffer.getvalue()[:size_bytes])
        else:
            f.write(buffer.getvalue())
            f.write(b'\0' * (size_bytes - buffer.tell()))
    
    progress_var.set(100)

def generate_audio_file(file_type, size_bytes, output_path, progress_var):
    sample_rate = 44100
    num_channels = 2
    sample_width = 2
    
    num_samples = (size_bytes - 44) // (num_channels * sample_width)
    
    audio_data = np.random.randint(-32768, 32767, num_samples * num_channels, dtype=np.int16)
    
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    current_size = os.path.getsize(output_path)
    if current_size < size_bytes:
        with open(output_path, 'ab') as f:
            f.write(b'\0' * (size_bytes - current_size))
    
    progress_var.set(100)

def generate_pdf_file(size_bytes, output_path, progress_var):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    bytes_written = 0
    page_number = 1
    
    while bytes_written < size_bytes:
        c.setFont("Helvetica", 12)
        y = height - 50
        
        while y > 50 and bytes_written < size_bytes:
            text = f"Page {page_number}, Line {height - y}"
            c.drawString(50, y, text)
            y -= 15
            bytes_written += len(text.encode('utf-8'))
            progress_var.set(min(100, int(bytes_written / size_bytes * 100)))
        
        c.showPage()
        page_number += 1
    
    c.save()
    
    pdf_data = buffer.getvalue()
    with open(output_path, 'wb') as f:
        if len(pdf_data) > size_bytes:
            f.write(pdf_data[:size_bytes])
        else:
            f.write(pdf_data)
            f.write(b'\0' * (size_bytes - len(pdf_data)))
    
    progress_var.set(100)