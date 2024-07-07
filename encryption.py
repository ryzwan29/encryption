from cryptography.fernet import Fernet
import os
from time import sleep
from rich.console import Console
from rich.prompt import Prompt

console = Console()

# Fungsi untuk generate key
def generate_key():
    return Fernet.generate_key()

# Fungsi untuk enkripsi file 
def encrypt_file(key, filename):
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Fungsi untuk dekripsi file
def decrypt_file(key, filename):
    fernet = Fernet(key)
    with open(filename, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

# Fungsi untuk melakukan enkripsi pada semua file gambar dalam direktori
def encrypt_images_in_directory(directory, key):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.webp') or filename.lower().endswith('.png') or filename.lower().endswith('.mp4') or filename.lower().endswith('.MOV')): 
            try:
                encrypt_file(key, filepath)
                console.print(f" [bold green]{filename} berhasil dienkripsi.[/bold green]")
            except Exception as e:
                console.print(f" [bold red]Gagal mengenkripsi {filename}: {str(e)}[/bold red]")

# Fungsi untuk melakukan dekripsi pada semua file gambar dalam direktori
def decrypt_images_in_directory(directory, key):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.webp') or filename.lower().endswith('.png') or filename.lower().endswith('.mp4') or filename.lower().endswith('.MOV')): 
            try:
                decrypt_file(key, filepath)
                console.print(f" [bold green]{filename} berhasil didekripsi.[/bold green]")
            except Exception as e:
                console.print(f" [bold red]Gagal mendekripsi {filename}: {str(e)}[/bold red]")

# Fungsi untuk menampilkan menu utama
def display_main_menu():
    console.clear()
    console.print("[bold cyan]Pilih aksi:[/bold cyan]")
    console.print("1: Enkripsi")
    console.print("2: Dekripsi")
    console.print("3: Keluar")

# Fungsi untuk menampilkan sub menu
def display_sub_menu():
    console.clear()
    console.print("[bold cyan]Pilih aksi:[/bold cyan]") 
    console.print("1: Masukkan Direktori")
    console.print("2: Kembali")

# Fungsi untuk memilih aksi di menu utama
def main_menu():
    while True:
        display_main_menu()
        action = Prompt.ask("[bold cyan]Masukkan pilihan [/bold cyan]", choices=["1", "2", "3"])
        if action == '1':
            sub_menu("enkripsi")
        elif action == '2':
            sub_menu("dekripsi")
        elif action == '3':
            console.print("[bold cyan]Keluar dari program. Sampai jumpa![/bold cyan]")
            break

# Fungsi untuk memilih aksi di sub menu (enkripsi/dekripsi)
def sub_menu(action_type):
    while True:
        display_sub_menu()
        action = Prompt.ask("[bold cyan]Masukkan pilihan [/bold cyan]", choices=["1", "2"]) 
        if action == '1':
            directory = Prompt.ask("Masukkan direktori tempat file gambar/video berada") 
            if not os.path.isdir(directory):
                console.print("[bold red]Direktori tidak ditemukan. Silakan coba lagi.[/bold red]")
                sleep(2)
                continue
            if action_type == "enkripsi":
                key = generate_key()
                encrypt_images_in_directory(directory, key)
                console.print(f"[bold yellow] Kunci enkripsi Anda: {key.decode()}[/bold yellow]") 
                while True:
                    confirmed = Prompt.ask("[bold cyan] Apakah Anda sudah mencatat kunci enkripsi? (y/n) [/bold cyan]", choices=["y", "n"])
                    if confirmed == 'y':
                        break
            elif action_type == "dekripsi":
                key = Prompt.ask("Masukkan kunci enkripsi").encode()
                decrypt_images_in_directory(directory, key)
            break
        elif action == '2':
            return  # Return to main menu

# Assuming you have a main_menu function defined somewhere
main_menu()
