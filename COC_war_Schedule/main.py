# main.py
from db_connector import connect_to_db
from models.war_models import RegularWar, WarParticipant

def create_new_war():
    print("\n--- Membuat Jadwal War Baru ---")
    opponent = input("Nama Clan Lawan: ")
    size = int(input("Ukuran War (misal: 15): "))
    date = input("Tanggal Mulai (YYYY-MM-DD): ")
    
    # Buat objek war, ID masih None karena belum disimpan
    new_war = RegularWar(opponent_clan=opponent, war_size=size, start_date=date)
    
    print("Masukkan nama peserta:")
    for i in range(size):
        name = input(f"  Nama Peserta #{i+1}: ")
        th = int(input(f"  Level TH {name}: "))
        participant = WarParticipant(name=name, th_level=th)
        new_war.add_participant(participant)

    conn = connect_to_db()
    if conn:
        new_war.save(conn)
        conn.close()
        print(f"\nJadwal War baru dengan ID {new_war.id} berhasil dibuat!")
    else:
        print("Gagal terhubung ke database.")

def add_attack_note():
    print("\n--- Tambah Catatan Serangan ---")
    conn = connect_to_db()
    if not conn:
        print("Gagal terhubung ke database.")
        return

    wars = RegularWar.get_all(conn)
    if not wars:
        print("Belum ada jadwal war.")
        conn.close()
        return

    for war in wars:
        print(f"ID: {war.id} - Lawan: {war.opponent_clan} ({war.start_date})")
    
    try:
        war_id_choice = int(input("Pilih ID war: "))
        selected_war = next((w for w in wars if w.id == war_id_choice), None)

        if not selected_war:
            print("ID tidak ditemukan.")
            return

        print("\nPilih peserta:")
        for i, p in enumerate(selected_war.participants):
            print(f"{i+1}. {p.name}")
        
        p_choice = int(input("Pilih nomor peserta: ")) - 1
        selected_participant = selected_war.participants[p_choice]

        note = input("Masukkan catatan serangan (misal: 'Serang no.10, dpt 2 bintang'): ")
        if selected_participant.add_attack(note):
            # Simpan perubahan ke database
            selected_war.save(conn)
            print("Catatan berhasil ditambahkan!")
        else:
            print("Peserta ini sudah melakukan 2 serangan.")
            
    except (ValueError, IndexError):
        print("Pilihan tidak valid.")
    finally:
        conn.close()

def view_schedule():
    print("\n--- Jadwal dan Catatan War Clan ---")
    conn = connect_to_db()
    if not conn:
        print("Gagal terhubung ke database.")
        return
    
    wars = RegularWar.get_all(conn)
    conn.close()
    
    if not wars:
        print("Tidak ada jadwal untuk ditampilkan.")
        return
    
    for war in wars:
        war.display_summary() # Menggunakan polymorphism

def main_menu():
    while True:
        print("\n===== CoC War Schedule Manager (DB Version) =====")
        print("1. Buat Jadwal War Baru")
        print("2. Tambah Catatan Serangan")
        print("3. Lihat Semua Jadwal War")
        print("4. Keluar")
        choice = input("Pilihan Anda: ")

        if choice == '1':
            create_new_war()
        elif choice == '2':
            add_attack_note()
        elif choice == '3':
            view_schedule()
        elif choice == '4':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main_menu()