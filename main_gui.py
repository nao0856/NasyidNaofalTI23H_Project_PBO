# main_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import json
from db_connector import connect_to_db
from models.war_models import RegularWar, WarParticipant

class CoCWarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CoC War Schedule Manager")
        self.root.geometry("400x200")

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Buat Jadwal War Baru", command=self.open_create_war_window).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Lihat Semua Jadwal War", command=self.open_history_window).pack(pady=5, fill=tk.X)

    def open_create_war_window(self):
        win = Toplevel(self.root)
        win.title("Jadwal War Baru")
        
        frame = ttk.Frame(win, padding="20")
        frame.pack()

        ttk.Label(frame, text="Nama Clan Lawan:").grid(row=0, column=0, sticky="w", pady=2)
        opponent_entry = ttk.Entry(frame, width=30)
        opponent_entry.grid(row=0, column=1, pady=2)

        ttk.Label(frame, text="Ukuran War (misal: 15):").grid(row=1, column=0, sticky="w", pady=2)
        size_entry = ttk.Entry(frame, width=30)
        size_entry.grid(row=1, column=1, pady=2)

        ttk.Label(frame, text="Tanggal (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=2)
        date_entry = ttk.Entry(frame, width=30)
        date_entry.grid(row=2, column=1, pady=2)

        ttk.Label(frame, text="Peserta (nama,th):").grid(row=3, column=0, sticky="w", pady=2)
        participants_text = tk.Text(frame, width=30, height=10)
        participants_text.grid(row=3, column=1, pady=2)
        participants_text.insert(tk.END, "Contoh:\nPlayer1,14\nPlayer2,13")

        def save_war():
            opponent = opponent_entry.get()
            size = size_entry.get()
            date = date_entry.get()
            participants_str = participants_text.get("1.0", tk.END)

            if not all([opponent, size, date]):
                messagebox.showerror("Error", "Lawan, ukuran, dan tanggal harus diisi!")
                return
            
            new_war = RegularWar(opponent, int(size), date)
            
            # Parse participants from text area
            lines = participants_str.strip().split("\n")
            for line in lines:
                if "Contoh:" in line: continue
                try:
                    name, th = line.split(',')
                    participant = WarParticipant(name.strip(), int(th.strip()))
                    new_war.add_participant(participant)
                except ValueError:
                    continue # Abaikan baris yang formatnya salah
            
            conn = connect_to_db()
            if conn:
                new_war.save(conn)
                conn.close()
                messagebox.showinfo("Sukses", "Jadwal War baru berhasil dibuat!")
                win.destroy()
            else:
                messagebox.showerror("Error", "Gagal terhubung ke database.")

        ttk.Button(frame, text="Simpan Jadwal", command=save_war).grid(row=4, columnspan=2, pady=10)


    def open_history_window(self):
        win = Toplevel(self.root)
        win.title("Riwayat & Jadwal War")
        win.geometry("600x400")
        
        text_area = tk.Text(win, wrap=tk.WORD, font=("Courier New", 10))
        scrollbar = ttk.Scrollbar(win, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        conn = connect_to_db()
        if conn:
            wars = RegularWar.get_all(conn)
            conn.close()
            
            if not wars:
                text_area.insert(tk.END, "Belum ada data war.")
            else:
                for war in wars:
                    summary = f"""
----------------------------------------
War ID: {war.id} | Lawan: {war.opponent_clan}
Ukuran: {war.war_size} vs {war.war_size} | Status: {war.status}
Peserta:
"""
                    if not war.participants:
                        summary += "  (Belum ada peserta)\n"
                    for p in war.participants:
                        summary += f"  - {p.name} (TH{p.th_level}), Serangan: {len(p.attacks)}/2\n"
                        for attack_note in p.attacks:
                            summary += f"    * {attack_note}\n"
                    text_area.insert(tk.END, summary)
        else:
            text_area.insert(tk.END, "Gagal terhubung ke database.")
        
        text_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoCWarApp(root)
    root.mainloop()