import pystray
from pystray import MenuItem as item
from PIL import Image
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

class TrayIconApp:
    def __init__(self, root):
        self.root = root
        self.icon = None
        self.gui_running = False
        self.create_gui()  # Setup GUI tanpa menampilkannya

    def create_image(self):
        """Membuat gambar ikon untuk tray."""
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images', 'hevion.ico')
        return Image.open(icon_path)

    def create_gui(self):
        """Setup Tkinter GUI tanpa menampilkan dulu."""
        self.root.title("Hevion Assistant Console")

        # Menambahkan teks scroll untuk log
        self.text_area = ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Contoh log yang ditambahkan ke GUI
        self.text_area.insert(tk.END, "Aplikasi sedang berjalan...\n")

        # Event handler saat GUI ditutup
        self.root.protocol("WM_DELETE_WINDOW", self.hide_gui)
        self.hide_gui()  # Sembunyikan GUI saat startup

    def show_gui(self):
        """Menampilkan GUI, ini harus dipanggil dari main thread."""
        if not self.gui_running:
            self.root.after(0, self.root.deiconify)  # Buka GUI
            self.gui_running = True

    def hide_gui(self):
        """Menutup GUI tapi tetap menjaga aplikasi berjalan."""
        if self.gui_running:
            self.root.withdraw()  # Sembunyikan GUI
            self.gui_running = False

    def on_quit(self, icon, item):
        """Keluar dari aplikasi secara keseluruhan."""
        if self.gui_running:
            self.root.quit()  # Tutup GUI jika terbuka
        icon.stop()  # Hentikan tray icon
        # Hentikan proses utama
        os._exit(0)  # Paksa keluar dari aplikasi

    def run_tray(self):
        """Menjalankan tray icon di system tray."""
        self.icon = pystray.Icon("Hevion")

        # Membaca ikon dari path
        self.icon.icon = self.create_image()
        self.icon.title = "Hevion Assistant"

        # Menggunakan pystray.Menu dan pystray.MenuItem
        self.icon.menu = pystray.Menu(
            item('Open Console', lambda icon, item: self.root.after(0, self.show_gui)),
            item('Quit', self.on_quit)
        )

        # Menjalankan tray icon
        self.icon.run()

def start_tray_icon(root):
    """Menjalankan tray icon di thread terpisah."""
    tray_app = TrayIconApp(root)
    tray_thread = threading.Thread(target=tray_app.run_tray)
    tray_thread.daemon = True
    tray_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    start_tray_icon(root)
    root.mainloop()  # Memulai loop Tkinter
