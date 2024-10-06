import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys
import os
import platform
import threading

def create_image():
    """Membuat gambar ikon untuk tray."""
    # Ikon aplikasi berada di assets/images/hevion.ico
    icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images', 'hevion.ico')
    return icon_path

def on_quit(icon, item):
    """Fungsi untuk keluar dari aplikasi."""
    icon.stop()

def run_tray():
    """Menjalankan tray icon di system tray."""
    icon = pystray.Icon("Hevion")
    
    # Membaca ikon dari path
    icon.icon = Image.open(create_image())  # Pastikan ini mengarah ke assets/images/hevion.ico
    icon.title = "Hevion Assistant"
    
    # Menggunakan pystray.Menu dan pystray.MenuItem
    icon.menu = pystray.Menu(
        item('Quit', on_quit)  # Pastikan menggunakan Menu dan bukan tuple
    )
    
    # Menjalankan tray icon di thread terpisah agar tidak memblokir aplikasi utama
    tray_thread = threading.Thread(target=icon.run)
    tray_thread.daemon = True
    tray_thread.start()

    # Menjaga aplikasi tetap berjalan
    while True:
        pass
