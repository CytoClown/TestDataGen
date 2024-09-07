import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from .generators import (
    generate_card_number, generate_turkish_iban, generate_russian_phone_number,
    generate_phone_number_01, generate_upi_id, generate_ifsc_code,
    generate_utr_number, generate_address, generate_postcode, generate_file,
    generate_cuil, generate_card_number_by_bin
)
from .utils import on_copy
from .constants import CARD_PREFIXES, BANK_BINS, fake_ru, fake_en
import random

def on_generate():
    card_type = card_type_var.get()
    length = int(entry_length.get())
    language = language_var.get()
    
    card_number = generate_card_number(card_type, length)
    entry_card_number.delete(0, tk.END)
    entry_card_number.insert(0, card_number)
    
    if language == "Russian":
        fake = fake_ru
    else:
        fake = fake_en
    
    cardholder_name = fake.name()
    email = fake.email()
    address = fake.address()
    postcode = fake.postcode()
    
    entry_cardholder_name.delete(0, tk.END)
    entry_cardholder_name.insert(0, cardholder_name)
    
    entry_email.delete(0, tk.END)
    entry_email.insert(0, email)
    
    entry_iban.delete(0, tk.END)
    entry_iban.insert(0, generate_turkish_iban())
    
    entry_russian_phone_number.delete(0, tk.END)
    entry_russian_phone_number.insert(0, generate_russian_phone_number())
    
    entry_phone_number_01.delete(0, tk.END)
    entry_phone_number_01.insert(0, generate_phone_number_01())
    
    entry_upi_id.delete(0, tk.END)
    entry_upi_id.insert(0, generate_upi_id(language))
    
    entry_ifsc.delete(0, tk.END)
    entry_ifsc.insert(0, generate_ifsc_code())
    
    entry_utr.delete(0, tk.END)
    entry_utr.insert(0, generate_utr_number())
    
    entry_address.delete(0, tk.END)
    entry_address.insert(0, address)
    
    entry_postcode.delete(0, tk.END)
    entry_postcode.insert(0, postcode)
    
    entry_cuil.delete(0, tk.END)
    entry_cuil.insert(0, generate_cuil())

def on_generate_by_bin():
    selected_bank = bank_var.get()
    result_text.config(state='normal')
    result_text.delete(1.0, tk.END)
    
    for payment_system, bins in BANK_BINS[selected_bank].items():
        bin_prefix = random.choice(bins)
        card_number = generate_card_number_by_bin(bin_prefix)
        result_text.insert(tk.END, f"{payment_system}: {card_number}\n")
    
    result_text.config(state='disabled')

def on_generate_file():
    file_type = file_type_var.get()
    size_str = size_entry.get().strip()
    if not size_str:
        messagebox.showerror("Error", "Please enter a file size.")
        return
    try:
        size_mb = float(size_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid file size. Please enter a number.")
        return
    
    output_path = filedialog.asksaveasfilename(defaultextension=file_type)
    if output_path:
        progress_var.set(0)
        progress_bar.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        button_generate_file.config(state=tk.DISABLED)
        
        def generate():
            generate_file(file_type, size_mb, output_path, progress_var)
            app.after(0, lambda: messagebox.showinfo("Success", f"File generated: {output_path}"))
            app.after(0, lambda: progress_bar.grid_remove())
            app.after(0, lambda: button_generate_file.config(state=tk.NORMAL))
        
        threading.Thread(target=generate, daemon=True).start()

def create_ui():
    global app, card_type_var, entry_length, language_var, entry_card_number, entry_cardholder_name, entry_email
    global entry_iban, entry_russian_phone_number, entry_phone_number_01, entry_upi_id, entry_ifsc, entry_utr
    global entry_address, entry_postcode, bank_var, result_text, file_type_var, size_entry, progress_var, progress_bar
    global button_generate_file, entry_cuil

    app = tk.Tk()
    app.title("Test Data Generator")

    notebook = ttk.Notebook(app)
    notebook.pack(fill=tk.BOTH, expand=True)

    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="General Generator")

    frame = tk.Frame(tab1)
    frame.pack(padx=10, pady=10)

    label_card_type = tk.Label(frame, text="Card Type:")
    label_card_type.grid(row=0, column=0, pady=5, sticky="e")
    card_type_var = tk.StringVar(value="Visa")
    card_type_menu = tk.OptionMenu(frame, card_type_var, *CARD_PREFIXES.keys())
    card_type_menu.grid(row=0, column=1, pady=5, sticky="w")

    label_length = tk.Label(frame, text="Length:")
    label_length.grid(row=1, column=0, pady=5, sticky="e")
    entry_length = tk.Entry(frame, width=35)
    entry_length.grid(row=1, column=1, pady=5, sticky="w")
    entry_length.insert(0, "16")

    label_language = tk.Label(frame, text="Cardholder Name Language:")
    label_language.grid(row=2, column=0, pady=5, sticky="e")
    language_var = tk.StringVar(value="Russian")
    radiobutton_frame = tk.Frame(frame)
    radiobutton_frame.grid(row=2, column=1, pady=5, sticky="w")
    radiobutton_russian = tk.Radiobutton(radiobutton_frame, text="Russian", variable=language_var, value="Russian")
    radiobutton_russian.pack(side="left")
    radiobutton_english = tk.Radiobutton(radiobutton_frame, text="English", variable=language_var, value="English")
    radiobutton_english.pack(side="left")

    label_card_number = tk.Label(frame, text="Card Number:")
    label_card_number.grid(row=3, column=0, pady=5, sticky="e")
    entry_card_number = tk.Entry(frame, width=35)
    entry_card_number.grid(row=3, column=1, pady=5, sticky="w")
    button_copy_card_number = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_card_number), relief="flat")
    button_copy_card_number.grid(row=3, column=2, pady=5, padx=5, sticky="w")

    label_cardholder_name = tk.Label(frame, text="Cardholder Name:")
    label_cardholder_name.grid(row=4, column=0, pady=5, sticky="e")
    entry_cardholder_name = tk.Entry(frame, width=35)
    entry_cardholder_name.grid(row=4, column=1, pady=5, sticky="w")
    button_copy_cardholder_name = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_cardholder_name), relief="flat")
    button_copy_cardholder_name.grid(row=4, column=2, pady=5, padx=5, sticky="w")

    label_email = tk.Label(frame, text="Email:")
    label_email.grid(row=5, column=0, pady=5, sticky="e")
    entry_email = tk.Entry(frame, width=35)
    entry_email.grid(row=5, column=1, pady=5, sticky="w")
    button_copy_email = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_email), relief="flat")
    button_copy_email.grid(row=5, column=2, pady=5, padx=5, sticky="w")

    label_iban = tk.Label(frame, text="Turkish IBAN:")
    label_iban.grid(row=6, column=0, pady=5, sticky="e")
    entry_iban = tk.Entry(frame, width=35)
    entry_iban.grid(row=6, column=1, pady=5, sticky="w")
    button_copy_iban = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_iban), relief="flat")
    button_copy_iban.grid(row=6, column=2, pady=5, padx=5, sticky="w")

    label_russian_phone_number = tk.Label(frame, text="Russian Phone Number:")
    label_russian_phone_number.grid(row=7, column=0, pady=5, sticky="e")
    entry_russian_phone_number = tk.Entry(frame, width=35)
    entry_russian_phone_number.grid(row=7, column=1, pady=5, sticky="w")
    button_copy_russian_phone_number = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_russian_phone_number), relief="flat")
    button_copy_russian_phone_number.grid(row=7, column=2, pady=5, padx=5, sticky="w")

    label_phone_number_01 = tk.Label(frame, text="Phone Number (01xxxxxxxxx):")
    label_phone_number_01.grid(row=8, column=0, pady=5, sticky="e")
    entry_phone_number_01 = tk.Entry(frame, width=35)
    entry_phone_number_01.grid(row=8, column=1, pady=5, sticky="w")
    button_copy_phone_number_01 = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_phone_number_01), relief="flat")
    button_copy_phone_number_01.grid(row=8, column=2, pady=5, padx=5, sticky="w")

    label_upi_id = tk.Label(frame, text="UPI ID:")
    label_upi_id.grid(row=9, column=0, pady=5, sticky="e")
    entry_upi_id = tk.Entry(frame, width=35)
    entry_upi_id.grid(row=9, column=1, pady=5, sticky="w")
    button_copy_upi_id = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_upi_id), relief="flat")
    button_copy_upi_id.grid(row=9, column=2, pady=5, padx=5, sticky="w")

    label_ifsc = tk.Label(frame, text="IFSC Code:")
    label_ifsc.grid(row=10, column=0, pady=5, sticky="e")
    entry_ifsc = tk.Entry(frame, width=35)
    entry_ifsc.grid(row=10, column=1, pady=5, sticky="w")
    button_copy_ifsc = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_ifsc), relief="flat")
    button_copy_ifsc.grid(row=10, column=2, pady=5, padx=5, sticky="w")

    label_utr = tk.Label(frame, text="UTR Number:")
    label_utr.grid(row=11, column=0, pady=5, sticky="e")
    entry_utr = tk.Entry(frame, width=35)
    entry_utr.grid(row=11, column=1, pady=5, sticky="w")
    button_copy_utr = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_utr), relief="flat")
    button_copy_utr.grid(row=11, column=2, pady=5, padx=5, sticky="w")

    label_address = tk.Label(frame, text="Registration Address:")
    label_address.grid(row=12, column=0, pady=5, sticky="e")
    entry_address = tk.Entry(frame, width=35)
    entry_address.grid(row=12, column=1, pady=5, sticky="w")
    button_copy_address = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_address), relief="flat")
    button_copy_address.grid(row=12, column=2, pady=5, padx=5, sticky="w")

    label_postcode = tk.Label(frame, text="Postcode:")
    label_postcode.grid(row=13, column=0, pady=5, sticky="e")
    entry_postcode = tk.Entry(frame, width=35)
    entry_postcode.grid(row=13, column=1, pady=5, sticky="w")
    button_copy_postcode = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_postcode), relief="flat")
    button_copy_postcode.grid(row=13, column=2, pady=5, padx=5, sticky="w")

    label_cuil = tk.Label(frame, text="CUIL:")
    label_cuil.grid(row=14, column=0, pady=5, sticky="e")
    entry_cuil = tk.Entry(frame, width=35)
    entry_cuil.grid(row=14, column=1, pady=5, sticky="w")
    button_copy_cuil = tk.Button(frame, text="⧉", command=lambda: on_copy(entry_cuil), relief="flat")
    button_copy_cuil.grid(row=14, column=2, pady=5, padx=5, sticky="w")

    button_generate = tk.Button(tab1, text="Generate", command=on_generate, bg="blue", fg="white", font=("Helvetica", 12, "bold"))
    button_generate.pack(pady=20)
    button_generate.config(width=20)

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="BIN Generator")

    frame_bin = tk.Frame
    frame_bin = tk.Frame(tab2)
    frame_bin.pack(padx=10, pady=10)

    label_bank = tk.Label(frame_bin, text="Выберите банк:")
    label_bank.grid(row=0, column=0, pady=5, sticky="e")
    bank_var = tk.StringVar(value="Sberbank")
    bank_menu = tk.OptionMenu(frame_bin, bank_var, *BANK_BINS.keys())
    bank_menu.grid(row=0, column=1, pady=5, sticky="w")

    result_text = tk.Text(frame_bin, width=50, height=10, state='disabled')
    result_text.grid(row=1, column=0, columnspan=2, pady=10)

    button_generate_bin = tk.Button(tab2, text="Generate", command=on_generate_by_bin, bg="blue", fg="white", font=("Helvetica", 12, "bold"))
    button_generate_bin.pack(pady=20)
    button_generate_bin.config(width=20)

    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="File Generator")

    frame_file = tk.Frame(tab3)
    frame_file.pack(padx=10, pady=10)

    label_file_type = tk.Label(frame_file, text="File Type:")
    label_file_type.grid(row=0, column=0, pady=5, sticky="e")
    file_types = ['.txt', '.csv', '.json', '.xml', '.html', '.bin', '.exe', '.dll', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.wav', '.pdf']
    file_type_var = tk.StringVar(value=file_types[0])
    file_type_menu = tk.OptionMenu(frame_file, file_type_var, *file_types)
    file_type_menu.grid(row=0, column=1, pady=5, sticky="w")

    label_size = tk.Label(frame_file, text="File Size (MB):")
    label_size.grid(row=1, column=0, pady=5, sticky="e")

    size_var = tk.StringVar(value="1.00")
    size_entry = tk.Entry(frame_file, textvariable=size_var, width=10)
    size_entry.grid(row=1, column=1, pady=5, sticky="w")

    def validate_size(P):
        if P == "":
            return True
        try:
            value = float(P)
            if 0.01 <= value <= 100:
                size_scale.set(value)
                return True
            return False
        except ValueError:
            return False

    vcmd = (frame_file.register(validate_size), '%P')
    size_entry.config(validate="key", validatecommand=vcmd)

    def on_scale_change(value):
        size_var.set(f"{float(value):.2f}")

    size_scale = tk.Scale(frame_file, from_=0.01, to=100, resolution=0.01, orient=tk.HORIZONTAL, length=200, command=on_scale_change)
    size_scale.grid(row=2, column=0, columnspan=2, pady=5)
    size_scale.set(1.00)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame_file, variable=progress_var, maximum=100)

    button_generate_file = tk.Button(tab3, text="Generate File", command=on_generate_file, bg="blue", fg="white", font=("Helvetica", 12, "bold"))
    button_generate_file.pack(pady=20)
    button_generate_file.config(width=20)

    app.mainloop()
    app.mainloop()
    app.mainloop()